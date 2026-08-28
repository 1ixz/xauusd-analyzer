import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import feedparser
import requests
from streamlit_autorefresh import st_autorefresh
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import AverageTrueRange, BollingerBands


# =========================================================
# إعدادات الصفحة
# =========================================================

st.set_page_config(
    page_title="XAUUSD AI Analyzer",
    page_icon="🥇",
    layout="wide"
)

st.title("🥇 XAUUSD AI Analyzer")
st.caption("تحليل فني + تحليل إخباري لسوق الذهب (Gold / USD) — سعر حي (Spot)")

st.info(
    "⚠️ تنويه مهم: هذا الموقع أداة مساعدة للتحليل فقط. "
    "لا توجد أي أداة بالعالم تضمن نتيجة التداول 100%. "
    "استخدم هذه الإشارات كجزء من قرارك، مو كل القرار، وأدر رأس المال بحذر."
)


# =========================================================
# الشريط الجانبي - الإعدادات
# =========================================================

TIMEFRAMES = {
    "1M": "1min",
    "5M": "5min",
    "15M": "15min",
    "30M": "30min",
    "1H": "1h",
    "4H": "4h",
    "1D": "1day",
}

with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("TwelveData API Key", type="password",
                             help="سجل مجانًا بموقع twelvedata.com وحط مفتاحك هنا")
    tf_choice = st.selectbox("الفريم الزمني", list(TIMEFRAMES.keys()), index=4)
    refresh_seconds = st.slider("تحديث تلقائي كل (ثانية)", 30, 300, 60, step=30)
    st.caption("الشارت يتحدث لحاله بالمدة المحددة فوق")
    st.divider()
    st.header("🧪 إعدادات الباك تست")
    backtest_candles = st.slider("عدد الشموع التاريخية للاختبار", 300, 2000, 1000, step=100)
    st.caption("كل ما زاد الرقم، كل ما الاختبار أدق بس ياخذ وقت أطول بالتحميل")

if not api_key:
    st.warning("⬅️ حط مفتاح TwelveData API بالشريط الجانبي حتى يشتغل الموقع بالسعر الحي الحقيقي.")
    st.stop()

# التحديث التلقائي للصفحة (فقط لتبويب التحليل الحي)
st_autorefresh(interval=refresh_seconds * 1000, key="live_refresh")


# =========================================================
# دوال مشتركة: جلب البيانات وحساب المؤشرات
# =========================================================

@st.cache_data(ttl=30)
def get_price_data(interval, key, outputsize=300):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "XAU/USD",
        "interval": interval,
        "outputsize": outputsize,
        "apikey": key,
        "order": "ASC",
    }
    r = requests.get(url, params=params, timeout=20)
    payload = r.json()

    if "values" not in payload:
        return pd.DataFrame(), payload.get("message", "خطأ غير معروف بجلب البيانات")

    df = pd.DataFrame(payload["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").sort_index()

    for col in ["open", "high", "low", "close"]:
        df[col] = df[col].astype(float)

    df = df.rename(columns={
        "open": "Open", "high": "High", "low": "Low", "close": "Close"
    })

    return df[["Open", "High", "Low", "Close"]], None


def add_indicators(df):
    df = df.copy()
    df["EMA20"] = EMAIndicator(close=df["Close"], window=20).ema_indicator()
    df["EMA50"] = EMAIndicator(close=df["Close"], window=50).ema_indicator()
    df["EMA200"] = EMAIndicator(close=df["Close"], window=200).ema_indicator()
    df["RSI"] = RSIIndicator(close=df["Close"], window=14).rsi()

    macd = MACD(close=df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    atr_ind = AverageTrueRange(high=df["High"], low=df["Low"], close=df["Close"], window=14)
    df["ATR"] = atr_ind.average_true_range()

    bb = BollingerBands(close=df["Close"], window=20, window_dev=2)
    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_LOWER"] = bb.bollinger_lband()

    df["Resistance"] = df["High"].rolling(50).max()
    df["Support"] = df["Low"].rolling(50).min()

    return df


def technical_score(price, ema20, ema50, ema200, rsi, macd_value, macd_signal):
    """يرجع score ولايبلات كل مؤشر — نفس المنطق يستخدم بالتحليل الحي والباك تست"""
    score = 0

    if price > ema200:
        score += 1
        trend_label = "🟢 BULLISH"
    else:
        score -= 1
        trend_label = "🔴 BEARISH"

    if ema20 > ema50:
        score += 1
        momentum_label = "🟢 STRONG"
    else:
        score -= 1
        momentum_label = "🔴 WEAK"

    if price > ema20:
        score += 1

    if rsi > 55:
        score += 1
        rsi_label = "🟢 BULLISH"
    elif rsi < 45:
        score -= 1
        rsi_label = "🔴 BEARISH"
    else:
        rsi_label = "🟡 NEUTRAL"

    if macd_value > macd_signal:
        score += 1
        macd_label = "🟢 BULLISH"
    else:
        score -= 1
        macd_label = "🔴 BEARISH"

    ema200_label = "🟢 ABOVE" if price > ema200 else "🔴 BELOW"

    return score, trend_label, momentum_label, rsi_label, macd_label, ema200_label


# =========================================================
# جلب بيانات التحليل الحي
# =========================================================

tf_settings = TIMEFRAMES[tf_choice]
data, error_msg = get_price_data(tf_settings, api_key, outputsize=300)

if data.empty:
    st.error(f"لم نستطع جلب بيانات الذهب الحية. السبب: {error_msg}")
    st.caption("تأكد أن مفتاح API صحيح، أو انتظر دقيقة إذا تجاوزت الحد المجاني للطلبات.")
    st.stop()

data = add_indicators(data)


# =========================================================
# تحليل الأخبار (News Sentiment) - بدون API key
# =========================================================

BULLISH_WORDS = [
    "rate cut", "cuts rates", "inflation rises", "safe haven", "geopolitical",
    "tension", "recession", "weak dollar", "dollar falls", "fed dovish",
    "war", "conflict", "uncertainty", "yields fall", "risk aversion"
]

BEARISH_WORDS = [
    "rate hike", "hikes rates", "strong dollar", "dollar rises", "fed hawkish",
    "jobs data strong", "risk appetite", "yields rise", "stocks rally",
    "inflation falls", "strong economy", "rate increase"
]

NEWS_FEEDS = [
    "https://www.investing.com/rss/news_285.rss",
    "https://www.fxstreet.com/rss/news",
]


@st.cache_data(ttl=300)
def get_news():
    headlines = []
    for url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                headlines.append(entry.title)
        except Exception:
            continue
    return headlines


def analyze_news(headlines):
    bullish_hits = 0
    bearish_hits = 0
    matched = []

    for h in headlines:
        h_lower = h.lower()
        for w in BULLISH_WORDS:
            if w in h_lower:
                bullish_hits += 1
                matched.append((h, "🟢 BULLISH"))
                break
        else:
            for w in BEARISH_WORDS:
                if w in h_lower:
                    bearish_hits += 1
                    matched.append((h, "🔴 BEARISH"))
                    break

    if bullish_hits + bearish_hits == 0:
        news_score = 0
        news_label = "🟡 NEUTRAL"
    elif bullish_hits > bearish_hits:
        news_score = 1
        news_label = "🟢 BULLISH"
    elif bearish_hits > bullish_hits:
        news_score = -1
        news_label = "🔴 BEARISH"
    else:
        news_score = 0
        news_label = "🟡 MIXED"

    return news_score, news_label, matched


headlines = get_news()
news_score, news_label, matched_news = analyze_news(headlines)


# =========================================================
# نظام التقييم الكلي للتحليل الحي (فني + أخبار)
# =========================================================

last = data.iloc[-1]
price = float(last["Close"])
ema20 = float(last["EMA20"]) if not np.isnan(last["EMA20"]) else price
ema50 = float(last["EMA50"]) if not np.isnan(last["EMA50"]) else price
ema200 = float(last["EMA200"]) if not np.isnan(last["EMA200"]) else price
rsi = float(last["RSI"])
macd_value = float(last["MACD"])
macd_signal = float(last["MACD_SIGNAL"])
atr = float(last["ATR"])

lookback = min(50, len(data))
recent = data.tail(lookback)
resistance = float(recent["High"].max())
support = float(recent["Low"].min())

score, trend_label, momentum_label, rsi_label, macd_label, ema200_label = technical_score(
    price, ema20, ema50, ema200, rsi, macd_value, macd_signal
)
score += news_score

if score >= 4:
    signal = "BUY"
elif score <= -4:
    signal = "SELL"
else:
    signal = "WAIT"

max_possible_score = 6
confidence = min(90, 50 + int(abs(score) / max_possible_score * 40))

entry = price
atr_multiplier_sl = 1.5
atr_multiplier_tp = 3.0

if signal == "BUY":
    sl = min(entry - atr * atr_multiplier_sl, support)
    tp = max(entry + atr * atr_multiplier_tp, resistance)
elif signal == "SELL":
    sl = max(entry + atr * atr_multiplier_sl, resistance)
    tp = min(entry - atr * atr_multiplier_tp, support)
else:
    sl = entry - atr * atr_multiplier_sl
    tp = entry + atr * atr_multiplier_tp

risk = abs(entry - sl)
reward = abs(tp - entry)
rr_ratio = round(reward / risk, 2) if risk > 0 else 0


# =========================================================
# محرك الباك تست
# =========================================================

def run_backtest(df, sl_mult=1.5, tp_mult=3.0):
    """
    يمشي على البيانات التاريخية شمعة شمعة، ولما تتحقق شروط BUY/SELL
    (نفس منطق التحليل الحي بدون الأخبار) يفتح صفقة وهمية،
    ويتابعها لين توصل SL أو TP، ويسجل النتيجة.
    """
    trades = []
    position = None

    start_idx = 200  # نبدأ بعد ما تتوفر EMA200

    for i in range(start_idx, len(df)):
        row = df.iloc[i]

        if pd.isna(row["EMA200"]) or pd.isna(row["ATR"]) or pd.isna(row["Support"]):
            continue

        if position is None:
            sc, *_ = technical_score(
                row["Close"], row["EMA20"], row["EMA50"], row["EMA200"],
                row["RSI"], row["MACD"], row["MACD_SIGNAL"]
            )

            side = None
            if sc >= 3:
                side = "BUY"
            elif sc <= -3:
                side = "SELL"

            if side:
                entry_price = row["Close"]
                atr_val = row["ATR"]
                sup = row["Support"]
                res = row["Resistance"]

                if side == "BUY":
                    sl_price = min(entry_price - atr_val * sl_mult, sup)
                    tp_price = max(entry_price + atr_val * tp_mult, res)
                else:
                    sl_price = max(entry_price + atr_val * sl_mult, res)
                    tp_price = min(entry_price - atr_val * tp_mult, sup)

                position = {
                    "side": side,
                    "entry": entry_price,
                    "sl": sl_price,
                    "tp": tp_price,
                    "entry_time": df.index[i],
                }
        else:
            side = position["side"]
            high = row["High"]
            low = row["Low"]
            hit = None

            if side == "BUY":
                if low <= position["sl"]:
                    hit = "SL"
                elif high >= position["tp"]:
                    hit = "TP"
            else:
                if high >= position["sl"]:
                    hit = "SL"
                elif low <= position["tp"]:
                    hit = "TP"

            if hit:
                exit_price = position["tp"] if hit == "TP" else position["sl"]
                if side == "BUY":
                    pnl = exit_price - position["entry"]
                else:
                    pnl = position["entry"] - exit_price

                trades.append({
                    "side": side,
                    "entry_time": position["entry_time"],
                    "exit_time": df.index[i],
                    "entry": position["entry"],
                    "exit": exit_price,
                    "result": "WIN" if hit == "TP" else "LOSS",
                    "pnl": pnl,
                })
                position = None

    return pd.DataFrame(trades)


# =========================================================
# التبويبات
# =========================================================

tab_live, tab_backtest = st.tabs(["📈 التحليل الحي", "🧪 اختبار الاستراتيجية (Backtest)"])


# ---------------------------------------------------------
# تبويب 1: التحليل الحي
# ---------------------------------------------------------

with tab_live:

    st.caption(f"🟢 بيانات حية — آخر تحديث: {data.index[-1].strftime('%Y-%m-%d %H:%M:%S')}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("سعر الذهب", f"${price:,.2f}")
    with col2:
        st.metric("الاتجاه العام", trend_label)
    with col3:
        signal_emoji = {"BUY": "🟢", "SELL": "🔴", "WAIT": "🟡"}[signal]
        st.metric("الإشارة", f"{signal_emoji} {signal}")
    with col4:
        st.metric("نسبة الثقة", f"{confidence}%")

    st.divider()

    st.subheader("📊 تحليل السوق (فني)")
    a1, a2, a3, a4, a5 = st.columns(5)
    with a1:
        st.markdown(f"**Trend**\n\n{trend_label}")
    with a2:
        st.markdown(f"**Momentum**\n\n{momentum_label}")
    with a3:
        st.markdown(f"**RSI**\n\n{rsi_label} ({rsi:.1f})")
    with a4:
        st.markdown(f"**MACD**\n\n{macd_label}")
    with a5:
        st.markdown(f"**EMA 200**\n\n{ema200_label}")

    st.divider()

    st.subheader("📰 تحليل الأخبار")
    st.markdown(f"**الحالة العامة من الأخبار:** {news_label}")

    if matched_news:
        with st.expander("شوف العناوين المؤثرة اللي تم رصدها"):
            for title, label in matched_news[:10]:
                st.write(f"{label} — {title}")
    else:
        st.caption("ما كو عناوين إخبارية واضحة التأثير حاليًا، الاعتماد الأكبر على التحليل الفني.")

    st.divider()

    st.subheader("🎯 تفاصيل الإشارة")
    if signal == "WAIT":
        st.warning("السوق حاليًا بدون اتجاه واضح (WAIT). لا توجد صفقة موصى بها الآن — الأفضل الانتظار.")
    else:
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric("نقطة الدخول (Entry)", f"${entry:,.2f}")
        with s2:
            st.metric("وقف الخسارة (SL)", f"${sl:,.2f}")
        with s3:
            st.metric("جني الأرباح (TP)", f"${tp:,.2f}")
        with s4:
            st.metric("Risk/Reward", f"1 : {rr_ratio}")

    st.caption(f"Support: ${support:,.2f}  |  Resistance: ${resistance:,.2f}  |  ATR: {atr:.2f}")

    st.divider()

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index, open=data["Open"], high=data["High"],
        low=data["Low"], close=data["Close"], name="XAUUSD"
    ))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA20"], name="EMA 20", line=dict(width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA50"], name="EMA 50", line=dict(width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA200"], name="EMA 200", line=dict(width=2)))
    fig.add_hline(y=resistance, line_dash="dash", line_color="red", annotation_text="Resistance")
    fig.add_hline(y=support, line_dash="dash", line_color="green", annotation_text="Support")
    fig.update_layout(title=f"شارت الذهب - {tf_choice}", height=600, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.warning(
        "هذه الإشارة تحليلية وليست ضماناً لحركة السوق. "
        "لا تستخدمها وحدها لاتخاذ قرار تداول، وأدر المخاطرة دائمًا (لا تخاطر بأكثر مما تتحمل خسارته)."
    )


# ---------------------------------------------------------
# تبويب 2: الباك تست
# ---------------------------------------------------------

with tab_backtest:

    st.subheader("🧪 اختبار الاستراتيجية على بيانات تاريخية")
    st.caption(
        "هذا الاختبار يطبق نفس منطق التحليل الفني (بدون تحليل الأخبار، لأنه غير متوفر تاريخيًا) "
        "على بيانات ماضية، ويحسب لو دخلت كل إشارة فعليًا شنو كانت النتيجة."
    )

    run_bt = st.button("▶️ شغّل الباك تست الآن", type="primary")

    if run_bt:
        with st.spinner("جاري تحميل البيانات التاريخية وتشغيل الاختبار..."):
            bt_data, bt_error = get_price_data(tf_settings, api_key, outputsize=backtest_candles)

            if bt_data.empty:
                st.error(f"تعذر جلب بيانات كافية للاختبار. السبب: {bt_error}")
            else:
                bt_data = add_indicators(bt_data)
                trades_df = run_backtest(bt_data)

                if trades_df.empty:
                    st.info(
                        "ما صارت أي صفقة خلال الفترة المختارة حسب شروط الاستراتيجية الحالية. "
                        "جرب تزيد عدد الشموع من الشريط الجانبي أو تغير الفريم الزمني."
                    )
                else:
                    total_trades = len(trades_df)
                    wins = (trades_df["result"] == "WIN").sum()
                    losses = (trades_df["result"] == "LOSS").sum()
                    win_rate = round(wins / total_trades * 100, 1)
                    total_pnl = trades_df["pnl"].sum()
                    avg_pnl = trades_df["pnl"].mean()

                    b1, b2, b3, b4 = st.columns(4)
                    with b1:
                        st.metric("عدد الصفقات", total_trades)
                    with b2:
                        st.metric("نسبة الصفقات الرابحة", f"{win_rate}%")
                    with b3:
                        st.metric("رابحة / خاسرة", f"{wins} / {losses}")
                    with b4:
                        st.metric("إجمالي النقاط (Points)", f"{total_pnl:,.1f}")

                    st.divider()

                    trades_df["cumulative_pnl"] = trades_df["pnl"].cumsum()

                    equity_fig = go.Figure()
                    equity_fig.add_trace(go.Scatter(
                        x=trades_df["exit_time"],
                        y=trades_df["cumulative_pnl"],
                        mode="lines+markers",
                        name="Cumulative PnL",
                        line=dict(color="#2ecc71" if total_pnl >= 0 else "#e74c3c")
                    ))
                    equity_fig.update_layout(
                        title="منحنى الأداء التراكمي (Equity Curve) — بالنقاط",
                        height=400,
                        xaxis_title="الوقت",
                        yaxis_title="النقاط التراكمية"
                    )
                    st.plotly_chart(equity_fig, use_container_width=True)

                    st.divider()

                    st.subheader("📋 سجل الصفقات")
                    display_df = trades_df.copy()
                    display_df["entry_time"] = display_df["entry_time"].dt.strftime("%Y-%m-%d %H:%M")
                    display_df["exit_time"] = display_df["exit_time"].dt.strftime("%Y-%m-%d %H:%M")
                    display_df["entry"] = display_df["entry"].round(2)
                    display_df["exit"] = display_df["exit"].round(2)
                    display_df["pnl"] = display_df["pnl"].round(2)
                    display_df = display_df.rename(columns={
                        "side": "الاتجاه", "entry_time": "وقت الدخول", "exit_time": "وقت الخروج",
                        "entry": "سعر الدخول", "exit": "سعر الخروج", "result": "النتيجة", "pnl": "النقاط"
                    })
                    st.dataframe(display_df, use_container_width=True, hide_index=True)

                    st.divider()

                    if win_rate >= 55:
                        st.success(
                            f"نسبة النجاح التاريخية {win_rate}% — الاستراتيجية عندها أداء إيجابي على هذه الفترة، "
                            "بس تذكر أن الأداء الماضي لا يضمن نتائج مستقبلية."
                        )
                    elif win_rate >= 45:
                        st.warning(
                            f"نسبة النجاح التاريخية {win_rate}% — أداء متوسط، يفضل تحسين الاستراتيجية "
                            "أو دمجها مع تحليل إضافي قبل الاعتماد عليها."
                        )
                    else:
                        st.error(
                            f"نسبة النجاح التاريخية {win_rate}% فقط — الاستراتيجية الحالية بهذا الفريم "
                            "ما عندها أداء موثوق كفاية. جرب فريم زمني آخر أو راجع الإعدادات."
                        )
    else:
        st.info("اضغط الزر أعلاه لتشغيل الاختبار على البيانات التاريخية.")
