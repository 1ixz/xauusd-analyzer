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

if not api_key:
    st.warning("⬅️ حط مفتاح TwelveData API بالشريط الجانبي حتى يشتغل الموقع بالسعر الحي الحقيقي.")
    st.stop()

# التحديث التلقائي للصفحة
st_autorefresh(interval=refresh_seconds * 1000, key="live_refresh")


# =========================================================
# 1) جلب بيانات الذهب الحية (Spot) من TwelveData
# =========================================================

@st.cache_data(ttl=30)
def get_price_data(interval, key):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "XAU/USD",
        "interval": interval,
        "outputsize": 300,
        "apikey": key,
        "order": "ASC",
    }
    r = requests.get(url, params=params, timeout=15)
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


tf_settings = TIMEFRAMES[tf_choice]
data, error_msg = get_price_data(tf_settings, api_key)

if data.empty:
    st.error(f"لم نستطع جلب بيانات الذهب الحية. السبب: {error_msg}")
    st.caption("تأكد أن مفتاح API صحيح، أو انتظر دقيقة إذا تجاوزت الحد المجاني للطلبات.")
    st.stop()

live_price_col1, live_price_col2 = st.columns([1, 3])
with live_price_col1:
    st.caption(f"🟢 بيانات حية — آخر تحديث: {data.index[-1].strftime('%Y-%m-%d %H:%M:%S')}")


# =========================================================
# 2) المؤشرات الفنية
# =========================================================

data["EMA20"] = EMAIndicator(close=data["Close"], window=20).ema_indicator()
data["EMA50"] = EMAIndicator(close=data["Close"], window=50).ema_indicator()
data["EMA200"] = EMAIndicator(close=data["Close"], window=200).ema_indicator()
data["RSI"] = RSIIndicator(close=data["Close"], window=14).rsi()

macd = MACD(close=data["Close"])
data["MACD"] = macd.macd()
data["MACD_SIGNAL"] = macd.macd_signal()

atr_ind = AverageTrueRange(high=data["High"], low=data["Low"], close=data["Close"], window=14)
data["ATR"] = atr_ind.average_true_range()

bb = BollingerBands(close=data["Close"], window=20, window_dev=2)
data["BB_UPPER"] = bb.bollinger_hband()
data["BB_LOWER"] = bb.bollinger_lband()

lookback = min(50, len(data))
recent = data.tail(lookback)
resistance = float(recent["High"].max())
support = float(recent["Low"].min())

last = data.iloc[-1]
price = float(last["Close"])
ema20 = float(last["EMA20"]) if not np.isnan(last["EMA20"]) else price
ema50 = float(last["EMA50"]) if not np.isnan(last["EMA50"]) else price
ema200 = float(last["EMA200"]) if not np.isnan(last["EMA200"]) else price
rsi = float(last["RSI"])
macd_value = float(last["MACD"])
macd_signal = float(last["MACD_SIGNAL"])
atr = float(last["ATR"])


# =========================================================
# 3) تحليل الأخبار (News Sentiment) - بدون API key
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
    "https://www.investing.com/rss/news_285.rss",   # Commodities news
    "https://www.fxstreet.com/rss/news",             # FX/Gold news
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
# 4) نظام التقييم الكلي (Technical + News)
# =========================================================

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

# إضافة وزن الأخبار للـ score الكلي
score += news_score

if score >= 4:
    signal = "BUY"
elif score <= -4:
    signal = "SELL"
else:
    signal = "WAIT"

max_possible_score = 6
confidence = min(90, 50 + int(abs(score) / max_possible_score * 40))


# =========================================================
# 5) Entry / SL / TP
# =========================================================

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
# عرض النتائج
# =========================================================

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

# الشارت
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
