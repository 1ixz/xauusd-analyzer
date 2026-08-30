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
# إعدادات الصفحة + تنسيق مخصص (CSS)
# =========================================================

st.set_page_config(
    page_title="XAUUSD AI Analyzer Pro",
    page_icon="🥇",
    layout="wide"
)

st.markdown("""
<style>
    .main .block-container {padding-top: 2rem;}
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(212,175,55,0.02));
        border: 1px solid rgba(212,175,55,0.25);
        border-radius: 12px;
        padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] { font-weight: 600; opacity: 0.85; }
    .strategy-card {
        background: rgba(212,175,55,0.06);
        border: 1px solid rgba(212,175,55,0.3);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 10px;
    }
    .signal-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .badge-buy { background: rgba(46,204,113,0.18); color: #2ecc71; border: 1px solid #2ecc71; }
    .badge-sell { background: rgba(231,76,60,0.18); color: #e74c3c; border: 1px solid #e74c3c; }
    .badge-wait { background: rgba(241,196,15,0.18); color: #f1c40f; border: 1px solid #f1c40f; }
    h1 { background: linear-gradient(90deg, #D4AF37, #F4E5A1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
""", unsafe_allow_html=True)

st.title("🥇 XAUUSD AI Analyzer Pro")
st.caption("منصة تحليل احترافية للذهب — استراتيجيات متعددة + سيولة + فريمات متعددة + أخبار — سعر حي (Spot)")

st.info(
    "⚠️ تنويه مهم: لا توجد أي استراتيجية أو أداة بالعالم تضمن نتيجة التداول 100%. "
    "هذه الأداة تحاكي منهجيات معروفة بين المتداولين المحترفين لتعطيك تحليلاً أعمق، "
    "مو وعداً بربح مؤكد. أدر رأس مالك بحذر دائمًا."
)


# =========================================================
# تعريف الاستراتيجيات
# =========================================================

STRATEGIES = {
    "ICT / Smart Money Concepts": {
        "key": "ict",
        "description": (
            "يعتمد على كشف مناطق اصطياد السيولة (Liquidity Sweep) وتأكيد الاتجاه من فريم زمني أعلى "
            "قبل الدخول. من أكثر المناهج انتشارًا بين متداولي الفوركس والذهب المحترفين حالياً، "
            "ويعرف بمنهج Smart Money Concepts."
        ),
        "sl_mult": 1.0,
        "tp1_mult": 1.8,
        "tp2_mult": 3.0,
        "use_liquidity": True,
        "use_higher_tf": True,
        "threshold": 5,
    },
    "اتجاهي (Trend Following)": {
        "key": "trend",
        "description": (
            "يركب الاتجاه العام طالما المتوسطات المتحركة (EMA20/50/200) متوافقة مع بعضها، "
            "ويعطي الصفقة مجالاً أكبر للتنفس بدل الخروج المبكر. مبدأ تداول معروف يعتمده متداولون "
            "يفضلون ركوب الاتجاهات القوية والمستمرة بدل الدخول والخروج السريع."
        ),
        "sl_mult": 1.3,
        "tp1_mult": 2.5,
        "tp2_mult": 5.0,
        "use_liquidity": False,
        "use_higher_tf": True,
        "threshold": 3,
    },
    "ارتدادي (Mean Reversion)": {
        "key": "mean_reversion",
        "description": (
            "يبحث عن مناطق التشبع الشرائي أو البيعي المتطرف (RSI + بولينجر باند) ويراهن على ارتداد "
            "السعر نحو متوسطه الطبيعي. مناسب أكثر بالأسواق المتذبذبة بدون اتجاه واضح طويل المدى."
        ),
        "sl_mult": 0.9,
        "tp1_mult": 1.2,
        "tp2_mult": 2.0,
        "use_liquidity": False,
        "use_higher_tf": False,
        "threshold": 2,
    },
    "اختراق (Breakout)": {
        "key": "breakout",
        "description": (
            "يبحث عن كسر مناطق الدعم أو المقاومة الأخيرة بزخم قوي مؤكد من MACD وRSI، ويدخل مع "
            "استمرار الزخم. مناسب أكثر وقت الأخبار المهمة والحركات القوية المفاجئة."
        ),
        "sl_mult": 1.1,
        "tp1_mult": 2.0,
        "tp2_mult": 4.0,
        "use_liquidity": True,
        "use_higher_tf": True,
        "threshold": 3,
    },
}


# =========================================================
# الشريط الجانبي
# =========================================================

TIMEFRAMES = {
    "1M": "1min", "5M": "5min", "15M": "15min", "30M": "30min",
    "1H": "1h", "4H": "4h", "1D": "1day",
}

HIGHER_TF_MAP = {
    "1M": "15min", "5M": "1h", "15M": "1h", "30M": "4h",
    "1H": "4h", "4H": "1day", "1D": "1day",
}

with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("TwelveData API Key", type="password",
                             help="سجل مجانًا بموقع twelvedata.com وحط مفتاحك هنا")
    tf_choice = st.selectbox("الفريم الزمني", list(TIMEFRAMES.keys()), index=4)
    strategy_choice = st.selectbox("🧠 الاستراتيجية", list(STRATEGIES.keys()), index=0)
    refresh_seconds = st.slider("تحديث تلقائي كل (ثانية)", 30, 300, 60, step=30)
    st.divider()
    st.header("🧪 إعدادات الباك تست")
    backtest_candles = st.slider("عدد الشموع التاريخية للاختبار", 300, 2000, 1000, step=100)

if not api_key:
    st.warning("⬅️ حط مفتاح TwelveData API بالشريط الجانبي حتى يشتغل الموقع بالسعر الحي الحقيقي.")
    st.stop()

st_autorefresh(interval=refresh_seconds * 1000, key="live_refresh")

strategy_cfg = STRATEGIES[strategy_choice]

st.markdown(f"""
<div class="strategy-card">
<b>🧠 الاستراتيجية النشطة: {strategy_choice}</b><br><br>
{strategy_cfg['description']}
</div>
""", unsafe_allow_html=True)


# =========================================================
# دوال مشتركة: جلب البيانات وحساب المؤشرات
# =========================================================

@st.cache_data(ttl=45)
def get_price_data(interval, key, outputsize=300):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "XAU/USD", "interval": interval, "outputsize": outputsize,
        "apikey": key, "order": "ASC",
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

    df = df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"})
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
    df["PriorResistance"] = df["Resistance"].shift(1)
    df["PriorSupport"] = df["Support"].shift(1)

    return df


def indicator_labels(price, ema20, ema50, ema200, rsi, macd_value, macd_signal):
    trend_label = "🟢 BULLISH" if price > ema200 else "🔴 BEARISH"
    momentum_label = "🟢 STRONG" if ema20 > ema50 else "🔴 WEAK"
    if rsi > 55:
        rsi_label = "🟢 BULLISH"
    elif rsi < 45:
        rsi_label = "🔴 BEARISH"
    else:
        rsi_label = "🟡 NEUTRAL"
    macd_label = "🟢 BULLISH" if macd_value > macd_signal else "🔴 BEARISH"
    ema200_label = "🟢 ABOVE" if price > ema200 else "🔴 BELOW"
    return trend_label, momentum_label, rsi_label, macd_label, ema200_label


def strategy_score(strategy_key, price, ema20, ema50, ema200, rsi, macd_value, macd_signal,
                    bb_upper, bb_lower, prior_resistance, prior_support, atr_value=np.nan):
    """كل استراتيجية عندها منطق تسجيل نقاط مختلف حسب فلسفتها"""

    if strategy_key == "ict":
        score = 0
        if price > ema200: score += 1
        else: score -= 1
        if ema20 > ema50: score += 1
        else: score -= 1
        if price > ema20: score += 1
        else: score -= 1
        if rsi > 55: score += 1
        elif rsi < 45: score -= 1
        if macd_value > macd_signal: score += 1
        else: score -= 1
        return score

    elif strategy_key == "trend":
        score = 0
        if ema20 > ema50 and ema50 > ema200:
            score += 2
        elif ema20 < ema50 and ema50 < ema200:
            score -= 2
        if price > ema20:
            score += 1
        else:
            score -= 1
        if macd_value > macd_signal:
            score += 1
        else:
            score -= 1
        return score

    elif strategy_key == "mean_reversion":
        # نشدد الشروط: تشبع أقوى (25/75 بدل 30/70) يقلل الإشارات الضعيفة
        score = 0
        if rsi < 25:
            score += 2
        elif rsi > 75:
            score -= 2
        if not np.isnan(bb_lower) and price < bb_lower:
            score += 1
        elif not np.isnan(bb_upper) and price > bb_upper:
            score -= 1
        return score

    elif strategy_key == "breakout":
        score = 0
        atr_buffer = atr_value * 0.25 if not np.isnan(atr_value) else 0
        if not np.isnan(prior_resistance) and price > prior_resistance + atr_buffer:
            score += 2
        elif not np.isnan(prior_support) and price < prior_support - atr_buffer:
            score -= 2
        if macd_value > macd_signal:
            score += 1
        else:
            score -= 1
        if rsi > 50:
            score += 1
        else:
            score -= 1
        return score

    return 0


STRATEGY_BASE_RANGE = {"ict": 5, "trend": 4, "mean_reversion": 3, "breakout": 4}


def volatility_ok(atr_series, index_pos, lookback=100, min_percentile=35):
    """
    يتأكد أن السوق فيه حركة حقيقية (تذبذب كافي) وقت الإشارة، بدل الدخول بسوق ميت/هادئ
    حيث تكون الإشارات عشوائية وغير موثوقة. يرجع False إذا كان ATR الحالي واطي جدًا
    مقارنة بالفترة الأخيرة.
    """
    start = max(0, index_pos - lookback)
    window = atr_series.iloc[start:index_pos]
    current = atr_series.iloc[index_pos]

    if window.empty or pd.isna(current) or len(window.dropna()) < 20:
        return True  # ما كو بيانات كافية للفلترة، نسمح بالإشارة

    percentile_rank = (window.dropna() < current).mean() * 100
    return percentile_rank >= min_percentile


def get_higher_tf_bias(interval, key):
    hdata, err = get_price_data(interval, key, outputsize=250)
    if hdata.empty:
        return 0, "🟡 غير متوفر"
    hdata = add_indicators(hdata)
    hlast = hdata.iloc[-1]
    hprice = float(hlast["Close"])
    hema200 = hlast["EMA200"]
    hema200 = float(hema200) if not pd.isna(hema200) else hprice
    if hprice > hema200:
        return 1, "🟢 الاتجاه الأكبر صاعد (BULLISH)"
    return -1, "🔴 الاتجاه الأكبر هابط (BEARISH)"


def detect_liquidity_sweep(df, lookback=30, recent_window=5):
    if len(df) < lookback + recent_window:
        return 0, "🟡 بيانات غير كافية لتحليل السيولة"

    recent = df.tail(lookback + recent_window)
    reference = recent.iloc[:lookback]
    last_candles = recent.iloc[lookback:]

    if reference.empty or last_candles.empty:
        return 0, "🟡 بيانات غير كافية لتحليل السيولة"

    swing_low = reference["Low"].min()
    swing_high = reference["High"].max()

    bullish_sweep = (last_candles["Low"].min() < swing_low) and (last_candles["Close"].iloc[-1] > swing_low)
    bearish_sweep = (last_candles["High"].max() > swing_high) and (last_candles["Close"].iloc[-1] < swing_high)

    if bullish_sweep and not bearish_sweep:
        return 1, "🟢 تم رصد سحب سيولة صعودي (كسر قاع سابق ثم ارتداد) — إشارة انعكاس محتملة للأعلى"
    elif bearish_sweep and not bullish_sweep:
        return -1, "🔴 تم رصد سحب سيولة هبوطي (كسر قمة سابقة ثم ارتداد) — إشارة انعكاس محتملة للأسفل"
    return 0, "🟡 ما كو نمط سحب سيولة واضح حاليًا"


# =========================================================
# جلب بيانات التحليل الحي
# =========================================================

tf_settings = TIMEFRAMES[tf_choice]
data, error_msg = get_price_data(tf_settings, api_key, outputsize=300)

if data.empty:
    st.error(f"لم نستطع جلب بيانات الذهب الحية. السبب: {error_msg}")
    st.stop()

data = add_indicators(data)


# =========================================================
# تحليل الأخبار
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
    bullish_hits, bearish_hits, matched = 0, 0, []
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
        return 0, "🟡 NEUTRAL", matched
    elif bullish_hits > bearish_hits:
        return 1, "🟢 BULLISH", matched
    elif bearish_hits > bullish_hits:
        return -1, "🔴 BEARISH", matched
    return 0, "🟡 MIXED", matched


headlines = get_news()
news_score, news_label, matched_news = analyze_news(headlines)


# =========================================================
# حساب الإشارة النهائية حسب الاستراتيجية المختارة
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
bb_upper = float(last["BB_UPPER"]) if not np.isnan(last["BB_UPPER"]) else price
bb_lower = float(last["BB_LOWER"]) if not np.isnan(last["BB_LOWER"]) else price
prior_resistance = float(last["PriorResistance"]) if not np.isnan(last["PriorResistance"]) else np.nan
prior_support = float(last["PriorSupport"]) if not np.isnan(last["PriorSupport"]) else np.nan

lookback = min(50, len(data))
recent = data.tail(lookback)
resistance = float(recent["High"].max())
support = float(recent["Low"].min())

trend_label, momentum_label, rsi_label, macd_label, ema200_label = indicator_labels(
    price, ema20, ema50, ema200, rsi, macd_value, macd_signal
)

base_score = strategy_score(
    strategy_cfg["key"], price, ema20, ema50, ema200, rsi, macd_value, macd_signal,
    bb_upper, bb_lower, prior_resistance, prior_support, atr
)
base_range = STRATEGY_BASE_RANGE[strategy_cfg["key"]]

vol_ok = volatility_ok(data["ATR"], len(data) - 1)

higher_bias_score, higher_bias_label = (0, "🟡 غير مستخدم بهذه الاستراتيجية")
if strategy_cfg["use_higher_tf"]:
    higher_tf_interval = HIGHER_TF_MAP[tf_choice]
    higher_bias_score, higher_bias_label = get_higher_tf_bias(higher_tf_interval, api_key)

liquidity_score, liquidity_msg = (0, "🟡 غير مستخدم بهذه الاستراتيجية")
if strategy_cfg["use_liquidity"]:
    liquidity_score, liquidity_msg = detect_liquidity_sweep(data)

WEIGHT_NEWS, WEIGHT_HIGHER_TF, WEIGHT_LIQUIDITY = 1, 2, 1

extra_weight = WEIGHT_NEWS
extra_weight += WEIGHT_HIGHER_TF if strategy_cfg["use_higher_tf"] else 0
extra_weight += WEIGHT_LIQUIDITY if strategy_cfg["use_liquidity"] else 0

score = base_score + (news_score * WEIGHT_NEWS)
score += (higher_bias_score * WEIGHT_HIGHER_TF) if strategy_cfg["use_higher_tf"] else 0
score += (liquidity_score * WEIGHT_LIQUIDITY) if strategy_cfg["use_liquidity"] else 0

max_possible_score = base_range + extra_weight
buy_threshold = strategy_cfg["threshold"] + (extra_weight // 2)
sell_threshold = -buy_threshold

if not vol_ok:
    signal = "WAIT"
elif score >= buy_threshold:
    signal = "BUY"
elif score <= sell_threshold:
    signal = "SELL"
else:
    signal = "WAIT"

confidence = min(92, 45 + int(abs(score) / max_possible_score * 47)) if max_possible_score > 0 else 50

conflict_warning = None
if strategy_cfg["use_higher_tf"]:
    if signal == "BUY" and higher_bias_score < 0:
        conflict_warning = "⚠️ الإشارة صاعدة على هذا الفريم، لكن الاتجاه الأكبر هابط — دخول بحذر أكثر."
    elif signal == "SELL" and higher_bias_score > 0:
        conflict_warning = "⚠️ الإشارة هابطة على هذا الفريم، لكن الاتجاه الأكبر صاعد — دخول بحذر أكثر."


# =========================================================
# Entry / SL / TP1 / TP2 — حسب مضاعفات الاستراتيجية المختارة
# =========================================================

entry = price
sl_mult = strategy_cfg["sl_mult"]
tp1_mult = strategy_cfg["tp1_mult"]
tp2_mult = strategy_cfg["tp2_mult"]

if signal == "BUY":
    sl = entry - atr * sl_mult
    tp1 = entry + atr * tp1_mult
    tp2 = entry + atr * tp2_mult
elif signal == "SELL":
    sl = entry + atr * sl_mult
    tp1 = entry - atr * tp1_mult
    tp2 = entry - atr * tp2_mult
else:
    sl = entry - atr * sl_mult
    tp1 = entry + atr * tp1_mult
    tp2 = entry + atr * tp2_mult

risk = abs(entry - sl)
rr1 = round(abs(tp1 - entry) / risk, 2) if risk > 0 else 0
rr2 = round(abs(tp2 - entry) / risk, 2) if risk > 0 else 0


# =========================================================
# محرك الباك تست (يدعم كل استراتيجية)
# =========================================================

def run_backtest(df, strategy_key, sl_mult, tp_mult, threshold):
    trades = []
    position = None
    start_idx = 200

    for i in range(start_idx, len(df)):
        row = df.iloc[i]

        if pd.isna(row["EMA200"]) or pd.isna(row["ATR"]):
            continue

        if position is None:
            if not volatility_ok(df["ATR"], i):
                continue

            sc = strategy_score(
                strategy_key, row["Close"], row["EMA20"], row["EMA50"], row["EMA200"],
                row["RSI"], row["MACD"], row["MACD_SIGNAL"], row["BB_UPPER"], row["BB_LOWER"],
                row["PriorResistance"], row["PriorSupport"], row["ATR"]
            )

            side = None
            if sc >= threshold:
                side = "BUY"
            elif sc <= -threshold:
                side = "SELL"

            if side:
                entry_price = row["Close"]
                atr_val = row["ATR"]

                if side == "BUY":
                    sl_price = entry_price - atr_val * sl_mult
                    tp_price = entry_price + atr_val * tp_mult
                else:
                    sl_price = entry_price + atr_val * sl_mult
                    tp_price = entry_price - atr_val * tp_mult

                position = {
                    "side": side, "entry": entry_price, "sl": sl_price,
                    "tp": tp_price, "entry_time": df.index[i],
                }
        else:
            side = position["side"]
            high, low = row["High"], row["Low"]
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
                pnl = (exit_price - position["entry"]) if side == "BUY" else (position["entry"] - exit_price)
                trades.append({
                    "side": side, "entry_time": position["entry_time"], "exit_time": df.index[i],
                    "entry": position["entry"], "exit": exit_price,
                    "result": "WIN" if hit == "TP" else "LOSS", "pnl": pnl,
                })
                position = None

    return pd.DataFrame(trades)


# =========================================================
# التبويبات
# =========================================================

tab_live, tab_backtest = st.tabs(["📈 التحليل الحي الذكي", "🧪 اختبار الاستراتيجية (Backtest)"])

with tab_live:

    st.caption(f"🟢 بيانات حية — آخر تحديث: {data.index[-1].strftime('%Y-%m-%d %H:%M:%S')}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("سعر الذهب", f"${price:,.2f}")
    with col2:
        st.metric("الاتجاه العام (فريم حالي)", trend_label)
    with col3:
        badge_class = {"BUY": "badge-buy", "SELL": "badge-sell", "WAIT": "badge-wait"}[signal]
        signal_emoji = {"BUY": "🟢", "SELL": "🔴", "WAIT": "🟡"}[signal]
        st.markdown(f"**الإشارة**<br><span class='signal-badge {badge_class}'>{signal_emoji} {signal}</span>", unsafe_allow_html=True)
    with col4:
        st.metric("نسبة الثقة", f"{confidence}%")

    if conflict_warning:
        st.warning(conflict_warning)

    if not vol_ok:
        st.warning("💤 السوق حاليًا هادئ وتذبذبه واطي (ATR منخفض مقارنة بالفترة الأخيرة) — تم تعطيل الإشارة تلقائيًا لتفادي صفقات ضعيفة الجودة.")

    st.divider()

    st.subheader("🧠 التحليل الذكي متعدد الأبعاد")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"**📐 الاتجاه الأكبر:**\n\n{higher_bias_label}")
    with d2:
        st.markdown(f"**💧 تحليل السيولة:**\n\n{liquidity_msg}")

    st.divider()

    st.subheader("📊 تحليل السوق (فني - الفريم الحالي)")
    a1, a2, a3, a4, a5 = st.columns(5)
    with a1: st.markdown(f"**Trend**\n\n{trend_label}")
    with a2: st.markdown(f"**Momentum**\n\n{momentum_label}")
    with a3: st.markdown(f"**RSI**\n\n{rsi_label} ({rsi:.1f})")
    with a4: st.markdown(f"**MACD**\n\n{macd_label}")
    with a5: st.markdown(f"**EMA 200**\n\n{ema200_label}")

    st.divider()

    st.subheader("📰 تحليل الأخبار")
    st.markdown(f"**الحالة العامة من الأخبار:** {news_label}")
    if matched_news:
        with st.expander("شوف العناوين المؤثرة اللي تم رصدها"):
            for title, label in matched_news[:10]:
                st.write(f"{label} — {title}")
    else:
        st.caption("ما كو عناوين إخبارية واضحة التأثير حاليًا.")

    st.divider()

    st.subheader("🎯 خطة الصفقة المقترحة")
    if signal == "WAIT":
        st.warning("السوق حاليًا بدون توافق كافي حسب هذه الاستراتيجية (WAIT). الأفضل الانتظار.")
    else:
        s1, s2, s3, s4 = st.columns(4)
        with s1: st.metric("نقطة الدخول (Entry)", f"${entry:,.2f}")
        with s2: st.metric("وقف الخسارة (SL)", f"${sl:,.2f}")
        with s3: st.metric("الهدف الأول (TP1)", f"${tp1:,.2f}")
        with s4: st.metric("الهدف الثاني (TP2)", f"${tp2:,.2f}")
        st.caption(f"Risk/Reward إلى TP1 = 1:{rr1}  |  إلى TP2 = 1:{rr2}  |  حجم الوقف: {atr*sl_mult:.2f} نقطة")
        st.info(
            "💡 عند الوصول لـ TP1، فكر بإغلاق نصف الصفقة ونقل وقف الخسارة لنقطة الدخول (Break-Even) "
            "لحماية رأس المال."
        )

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
    fig.update_layout(title=f"شارت الذهب - {tf_choice} - {strategy_choice}", height=600, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.warning("هذه الإشارة تحليلية وليست ضماناً لحركة السوق. لا تخاطر بأكثر مما تتحمل خسارته.")


with tab_backtest:

    st.subheader(f"🧪 اختبار استراتيجية: {strategy_choice}")
    st.caption(
        "هذا الاختبار يطبق منطق الاستراتيجية المختارة فقط (بدون أخبار/سيولة/فريم أعلى، لأنها تحتاج "
        "طلبات API إضافية غير متاحة بكثرة بالخطة المجانية). يعطيك فكرة واقعية عن قوة الأساس الفني."
    )

    run_bt = st.button("▶️ شغّل الباك تست الآن", type="primary")

    if run_bt:
        with st.spinner("جاري تحميل البيانات التاريخية وتشغيل الاختبار..."):
            bt_data, bt_error = get_price_data(tf_settings, api_key, outputsize=backtest_candles)

            if bt_data.empty:
                st.error(f"تعذر جلب بيانات كافية للاختبار. السبب: {bt_error}")
            else:
                bt_data = add_indicators(bt_data)
                trades_df = run_backtest(
                    bt_data, strategy_cfg["key"], strategy_cfg["sl_mult"],
                    strategy_cfg["tp2_mult"], strategy_cfg["threshold"]
                )

                if trades_df.empty:
                    st.info("ما صارت أي صفقة خلال الفترة المختارة. جرب تزيد عدد الشموع أو تغير الفريم.")
                else:
                    total_trades = len(trades_df)
                    wins = (trades_df["result"] == "WIN").sum()
                    losses = (trades_df["result"] == "LOSS").sum()
                    win_rate = round(wins / total_trades * 100, 1)
                    total_pnl = trades_df["pnl"].sum()

                    gross_win = trades_df.loc[trades_df["pnl"] > 0, "pnl"].sum()
                    gross_loss = abs(trades_df.loc[trades_df["pnl"] < 0, "pnl"].sum())
                    profit_factor = round(gross_win / gross_loss, 2) if gross_loss > 0 else float("inf")
                    expectancy = round(trades_df["pnl"].mean(), 2)

                    b1, b2, b3, b4 = st.columns(4)
                    with b1: st.metric("عدد الصفقات", total_trades)
                    with b2: st.metric("نسبة الصفقات الرابحة", f"{win_rate}%")
                    with b3: st.metric("رابحة / خاسرة", f"{wins} / {losses}")
                    with b4: st.metric("إجمالي النقاط", f"{total_pnl:,.1f}")

                    b5, b6 = st.columns(2)
                    with b5:
                        st.metric("Profit Factor", f"{profit_factor}",
                                  help="أكبر من 1 = الأرباح أكبر من الخسائر إجمالاً حتى لو نسبة الصفقات الرابحة أقل من 50%")
                    with b6:
                        st.metric("المتوسط لكل صفقة (Expectancy)", f"{expectancy:+.2f} نقطة")

                    st.caption(
                        "💡 **مهم:** نسبة الصفقات الرابحة وحدها لا تحدد نجاح الاستراتيجية. "
                        "استراتيجية بنسبة ربح 35% مع Profit Factor أكبر من 1.5 قد تكون أفضل من "
                        "استراتيجية بنسبة ربح 60% مع Profit Factor أقل من 1."
                    )

                    st.divider()

                    trades_df["cumulative_pnl"] = trades_df["pnl"].cumsum()
                    equity_fig = go.Figure()
                    equity_fig.add_trace(go.Scatter(
                        x=trades_df["exit_time"], y=trades_df["cumulative_pnl"],
                        mode="lines+markers", name="Cumulative PnL",
                        line=dict(color="#2ecc71" if total_pnl >= 0 else "#e74c3c")
                    ))
                    equity_fig.update_layout(title="منحنى الأداء التراكمي (بالنقاط)", height=400)
                    st.plotly_chart(equity_fig, use_container_width=True)

                    st.divider()
                    st.subheader("📋 سجل الصفقات")
                    display_df = trades_df.copy()
                    display_df["entry_time"] = display_df["entry_time"].dt.strftime("%Y-%m-%d %H:%M")
                    display_df["exit_time"] = display_df["exit_time"].dt.strftime("%Y-%m-%d %H:%M")
                    for c in ["entry", "exit", "pnl"]:
                        display_df[c] = display_df[c].round(2)
                    display_df = display_df.rename(columns={
                        "side": "الاتجاه", "entry_time": "وقت الدخول", "exit_time": "وقت الخروج",
                        "entry": "سعر الدخول", "exit": "سعر الخروج", "result": "النتيجة", "pnl": "النقاط"
                    })
                    st.dataframe(display_df, use_container_width=True, hide_index=True)

                    st.divider()
                    if profit_factor >= 1.3 and total_pnl > 0:
                        st.success(
                            f"Profit Factor = {profit_factor} ونتيجة إجمالية موجبة ({total_pnl:+.1f} نقطة) — "
                            f"رغم أن نسبة الربح {win_rate}%، هذه الاستراتيجية كانت مربحة إجمالاً على هذه الفترة "
                            "لأن حجم الأرباح أكبر من حجم الخسائر."
                        )
                    elif total_pnl > 0:
                        st.warning(
                            f"النتيجة الإجمالية موجبة ({total_pnl:+.1f} نقطة) بنسبة ربح {win_rate}%، "
                            f"لكن Profit Factor ({profit_factor}) ضعيف نسبيًا — الهامش الآمن قليل، "
                            "جرب فريم زمني آخر أو راقب الأداء على فترة أطول قبل الاعتماد عليها."
                        )
                    else:
                        st.error(
                            f"النتيجة الإجمالية سلبية ({total_pnl:+.1f} نقطة) بنسبة ربح {win_rate}% وProfit Factor {profit_factor} — "
                            "هذه الاستراتيجية غير مناسبة لهذا الفريم والفترة الحالية. جرب فريم زمني آخر أو استراتيجية مختلفة."
                        )
    else:
        st.info("اضغط الزر أعلاه لتشغيل الاختبار على البيانات التاريخية.")
