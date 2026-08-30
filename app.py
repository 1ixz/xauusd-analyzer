import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import feedparser
import requests
import time
from datetime import datetime, timezone
from streamlit_autorefresh import st_autorefresh
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator, ADXIndicator
from ta.volatility import AverageTrueRange, BollingerBands


# =========================================================
# إعدادات الصفحة
# =========================================================

st.set_page_config(
    page_title="XAUUSD AI Analyzer Pro",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CSS — تصميم عصري / زجاجي + متجاوب مع الجوال
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');

    :root {
        --bg-deep: #05070c;
        --bg-panel: #10141c;
        --bg-panel-soft: #151a24;
        --gold: #d4af37;
        --gold-soft: #f0d78c;
        --emerald: #29c48a;
        --rust: #ff5c5c;
        --blue: #4fa3ff;
        --text-primary: #f1efe9;
        --text-muted: #8b93a0;
        --border-soft: rgba(212,175,55,0.20);
    }

    html, body, [class*="css"]  { color: var(--text-primary); }
    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(212,175,55,0.06), transparent 40%),
            radial-gradient(circle at 85% 10%, rgba(79,163,255,0.05), transparent 45%),
            var(--bg-deep);
    }

    .main .block-container { padding-top: 1.2rem; max-width: 1280px; }

    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.01em; }

    h1 {
        background: linear-gradient(90deg, var(--gold) 0%, var(--gold-soft) 55%, var(--gold) 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }

    /* ===== شريط التيكر ===== */
    .ticker-bar {
        display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;
        gap: 16px;
        background: linear-gradient(135deg, rgba(21,26,36,0.9), rgba(10,13,20,0.9));
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-soft);
        border-left: 4px solid var(--gold);
        border-radius: 14px;
        padding: 16px 24px;
        margin: 10px 0 22px 0;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    }
    .ticker-item { display: flex; flex-direction: column; gap: 2px; min-width: 110px; }
    .ticker-label { font-size: 0.7rem; color: var(--text-muted); letter-spacing: 0.06em; text-transform: uppercase; }
    .ticker-value { font-size: 1.3rem; font-weight: 700; color: var(--text-primary); }
    .ticker-value.gold { color: var(--gold-soft); }

    /* ===== بطاقات المقاييس ===== */
    div[data-testid="stMetric"] {
        background: linear-gradient(160deg, rgba(212,175,55,0.08), rgba(212,175,55,0.015));
        border: 1px solid var(--border-soft);
        border-radius: 14px;
        padding: 14px 18px;
        transition: transform 0.15s ease;
    }
    div[data-testid="stMetricLabel"] { font-weight: 600; opacity: 0.8; font-size: 0.82rem; }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; color: var(--text-primary); }

    /* ===== بطاقات عامة ===== */
    .glass-card {
        background: linear-gradient(160deg, rgba(255,255,255,0.035), rgba(255,255,255,0.005));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 14px;
        backdrop-filter: blur(8px);
    }
    .strategy-card {
        background: var(--bg-panel);
        border: 1px solid var(--border-soft);
        border-right: 3px solid var(--gold);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 10px;
        line-height: 1.75;
    }

    .signal-badge {
        display: inline-block;
        padding: 8px 24px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.1rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.03em;
    }
    .badge-buy  { background: rgba(41,196,138,0.15); color: var(--emerald); border: 1px solid var(--emerald); }
    .badge-sell { background: rgba(255,92,92,0.15);  color: var(--rust);    border: 1px solid var(--rust); }
    .badge-wait { background: rgba(212,175,55,0.15); color: var(--gold-soft); border: 1px solid var(--gold); }

    .pill { display:inline-block; padding: 3px 12px; border-radius: 999px; font-size: 0.78rem; font-weight:600; margin-right:6px; }
    .pill-high { background: rgba(255,92,92,0.15); color: var(--rust); border:1px solid rgba(255,92,92,0.4);}
    .pill-med  { background: rgba(212,175,55,0.15); color: var(--gold-soft); border:1px solid rgba(212,175,55,0.4);}
    .pill-low  { background: rgba(139,147,160,0.15); color: var(--text-muted); border:1px solid rgba(139,147,160,0.3);}

    .stTabs [data-baseweb="tab"] { font-family: 'Space Grotesk', sans-serif; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: var(--gold-soft) !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: var(--gold) !important; }

    div[data-testid="stButton"] > button {
        border: 1px solid var(--border-soft);
        border-radius: 10px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(90deg, var(--gold), var(--gold-soft));
        color: #05070c; border: none;
    }

    hr { border-color: var(--border-soft) !important; }

    /* ===== تجاوب مع الجوال ===== */
    @media (max-width: 768px) {
        .main .block-container { padding-left: 0.6rem; padding-right: 0.6rem; }
        .ticker-bar { flex-direction: column; align-items: flex-start; gap: 10px; padding: 14px 16px; }
        .ticker-value { font-size: 1.05rem; }
        h1 { font-size: 1.5rem !important; }
        .signal-badge { font-size: 0.95rem; padding: 6px 16px; }
        div[data-testid="stMetricValue"] { font-size: 1.1rem; }
    }
</style>
""", unsafe_allow_html=True)

st.title("🥇 XAUUSD AI Analyzer Pro")
st.caption("منصة تحليل احترافية للذهب — 10 استراتيجيات + سيولة + فريمات متعددة + أخبار Forex Factory + تنبيهات تيليجرام")

st.info(
    "⚠️ تنويه مهم: لا توجد أي استراتيجية أو أداة بالعالم — بهذا الموقع أو غيره — تضمن نتيجة تداول 100%. "
    "كل الأرقام أدناه (نسب الربح، Profit Factor...) محسوبة من باك تست حقيقي على بيانات تاريخية، وهي **ليست** "
    "ضماناً للمستقبل. الصفقات المعلقة أدناه هي اقتراحات مبنية على التحليل الفني وليست صفقات مضمونة النتيجة. "
    "أدر رأس مالك بحذر دائمًا ولا تخاطر بأكثر مما تتحمل خسارته."
)


# =========================================================
# تعريف الاستراتيجيات (10 استراتيجيات)
# كل استراتيجية: sl/tp مضاعفات ATR + هل تستخدم سيولة/فريم أعلى + threshold + max_score التقريبي
# =========================================================

STRATEGIES = {
    "ICT / Smart Money Concepts": {
        "key": "ict", "sl_mult": 1.0, "tp1_mult": 1.8, "tp2_mult": 3.0,
        "use_liquidity": True, "use_higher_tf": True, "threshold": 5, "max_score": 5,
        "description": "كشف مناطق اصطياد السيولة (Liquidity Sweep) وتأكيد الاتجاه من فريم زمني أعلى قبل الدخول.",
    },
    "اتجاهي (Trend Following)": {
        "key": "trend", "sl_mult": 1.3, "tp1_mult": 2.5, "tp2_mult": 5.0,
        "use_liquidity": False, "use_higher_tf": True, "threshold": 3, "max_score": 4,
        "description": "يركب الاتجاه العام طالما EMA20/50/200 متوافقة، ويعطي الصفقة مجالاً أكبر للتنفس.",
    },
    "ارتدادي (Mean Reversion)": {
        "key": "mean_reversion", "sl_mult": 0.9, "tp1_mult": 1.2, "tp2_mult": 2.0,
        "use_liquidity": False, "use_higher_tf": False, "threshold": 2, "max_score": 3,
        "description": "يبحث عن تشبع شرائي/بيعي متطرف (RSI + بولينجر) ويراهن على ارتداد السعر لمتوسطه.",
    },
    "اختراق (Breakout)": {
        "key": "breakout", "sl_mult": 1.1, "tp1_mult": 2.0, "tp2_mult": 4.0,
        "use_liquidity": True, "use_higher_tf": True, "threshold": 3, "max_score": 4,
        "description": "يبحث عن كسر الدعم/المقاومة الأخيرة بزخم قوي مؤكد من MACD وRSI.",
    },
    "سكالبينج (EMA9/21 Cross)": {
        "key": "scalping", "sl_mult": 0.6, "tp1_mult": 1.0, "tp2_mult": 1.6,
        "use_liquidity": False, "use_higher_tf": False, "threshold": 2, "max_score": 3,
        "description": "تقاطع EMA9/21 السريع مع تأكيد MACD، مناسب للفريمات الصغيرة (1M-15M) والحركة السريعة.",
    },
    "فيبوناتشي (Fibonacci Retracement)": {
        "key": "fibonacci", "sl_mult": 1.0, "tp1_mult": 2.0, "tp2_mult": 3.5,
        "use_liquidity": False, "use_higher_tf": True, "threshold": 2, "max_score": 2,
        "description": "يرصد ارتداد السعر من مستوى فيبوناتشي 61.8% مع الاتجاه العام الأكبر.",
    },
    "أوردر بلوك / فجوة سعرية (Order Block/FVG)": {
        "key": "orderblock", "sl_mult": 1.0, "tp1_mult": 2.2, "tp2_mult": 4.0,
        "use_liquidity": True, "use_higher_tf": True, "threshold": 2, "max_score": 4,
        "description": "يرصد شموع الزخم القوي (اختلال بين العرض والطلب) ويتوقع استكمال الحركة بنفس الاتجاه.",
    },
    "دايفرجنس (RSI Divergence)": {
        "key": "divergence", "sl_mult": 1.0, "tp1_mult": 1.8, "tp2_mult": 3.0,
        "use_liquidity": False, "use_higher_tf": False, "threshold": 2, "max_score": 4,
        "description": "يقارن قمم/قيعان السعر مع RSI لرصد الانعكاسات المبكرة (تباعد سعري).",
    },
    "انعكاس VWAP": {
        "key": "vwap", "sl_mult": 0.8, "tp1_mult": 1.4, "tp2_mult": 2.2,
        "use_liquidity": False, "use_higher_tf": False, "threshold": 2, "max_score": 3,
        "description": "يقيس ابتعاد السعر عن متوسطه الموزون (VWAP تقريبي) ويراهن على العودة إليه.",
    },
    "انضغاط بولينجر (BB Squeeze)": {
        "key": "bbsqueeze", "sl_mult": 1.0, "tp1_mult": 2.0, "tp2_mult": 3.5,
        "use_liquidity": False, "use_higher_tf": True, "threshold": 2, "max_score": 3,
        "description": "يترقب انضغاط نطاق بولينجر (تذبذب منخفض) ثم يدخل مع أول اختراق بزخم.",
    },
}


# =========================================================
# الشريط الجانبي
# =========================================================

TIMEFRAMES = {"1M": "1min", "5M": "5min", "15M": "15min", "30M": "30min", "1H": "1h", "4H": "4h", "1D": "1day"}
HIGHER_TF_MAP = {"1M": "15min", "5M": "1h", "15M": "1h", "30M": "4h", "1H": "4h", "4H": "1day", "1D": "1day"}

with st.sidebar:
    st.header("⚙️ الإعدادات")

    # ملاحظة: حقل النص أدناه يعمل تلقائياً بمجرد الضغط Enter أو الخروج من الحقل —
    # لا يوجد زر "تأكيد" منفصل، Streamlit يعيد التشغيل تلقائياً بمجرد إدخال القيمة.
    api_key = st.text_input(
        "TwelveData API Key",
        type="password",
        help="سجل مجانًا بموقع twelvedata.com والصق مفتاحك هنا — يعمل الموقع مباشرة بدون أي زر تأكيد إضافي.",
    )

    tf_choice = st.selectbox("الفريم الزمني", list(TIMEFRAMES.keys()), index=4)
    strategy_choice = st.selectbox("🧠 الاستراتيجية", list(STRATEGIES.keys()), index=0)
    refresh_seconds = st.slider("تحديث تلقائي كل (ثانية)", 30, 300, 60, step=30)

    st.divider()
    st.header("🧪 إعدادات الباك تست")
    backtest_candles = st.slider("عدد الشموع التاريخية للاختبار", 300, 2000, 1000, step=100)

    st.divider()
    st.header("📲 تنبيهات تيليجرام")
    st.caption("أنشئ بوت عبر @BotFather واحصل على التوكن، واحصل على chat_id عبر @userinfobot (راجع README).")
    telegram_enabled = st.toggle("تفعيل إرسال التنبيهات لتيليجرام", value=False)
    tg_token = st.text_input("Bot Token", type="password") if telegram_enabled else ""
    tg_chat_id = st.text_input("Chat ID") if telegram_enabled else ""
    send_pending_alerts = st.checkbox("إرسال تنبيه أيضاً عند تفعيل صفقة معلقة", value=True) if telegram_enabled else False

if not api_key:
    st.warning("⬅️ الصق مفتاح TwelveData API بالشريط الجانبي حتى يشتغل الموقع بالسعر الحي — سيبدأ التحليل فوراً بدون أي خطوة إضافية.")
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
# جلب البيانات
# =========================================================

@st.cache_data(ttl=45)
def get_price_data(interval, key, outputsize=300):
    url = "https://api.twelvedata.com/time_series"
    params = {"symbol": "XAU/USD", "interval": interval, "outputsize": outputsize, "apikey": key, "order": "ASC"}
    try:
        r = requests.get(url, params=params, timeout=20)
        payload = r.json()
    except Exception as e:
        return pd.DataFrame(), f"خطأ اتصال: {e}"

    if "values" not in payload:
        return pd.DataFrame(), payload.get("message", "خطأ غير معروف بجلب البيانات (تحقق من صحة المفتاح أو حدود الطلبات المجانية)")

    df = pd.DataFrame(payload["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").sort_index()
    for col in ["open", "high", "low", "close"]:
        df[col] = df[col].astype(float)
    df = df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"})
    return df[["Open", "High", "Low", "Close"]], None


def compute_divergence(df, lookback=14):
    """يقارن نصفي نافذة متحركة لرصد تباعد السعر عن RSI (تقريبي، وليس اكتشاف قمم/قيعان دقيق)."""
    price, rsi = df["Close"], df["RSI"]
    div = pd.Series(0, index=df.index, dtype=int)
    half = max(2, lookback // 2)
    for i in range(lookback * 2, len(df)):
        wp = price.iloc[i - lookback: i + 1]
        wr = rsi.iloc[i - lookback: i + 1]
        if wr.isna().any():
            continue
        p1min, p2min = wp.iloc[:half].min(), wp.iloc[half:].min()
        r1min, r2min = wr.iloc[:half].min(), wr.iloc[half:].min()
        p1max, p2max = wp.iloc[:half].max(), wp.iloc[half:].max()
        r1max, r2max = wr.iloc[:half].max(), wr.iloc[half:].max()
        if p2min < p1min and r2min > r1min:
            div.iloc[i] = 1
        elif p2max > p1max and r2max < r1max:
            div.iloc[i] = -1
    return div


def add_indicators(df, with_divergence=True):
    df = df.copy()
    df["EMA9"] = EMAIndicator(close=df["Close"], window=9).ema_indicator()
    df["EMA20"] = EMAIndicator(close=df["Close"], window=20).ema_indicator()
    df["EMA21"] = EMAIndicator(close=df["Close"], window=21).ema_indicator()
    df["EMA50"] = EMAIndicator(close=df["Close"], window=50).ema_indicator()
    df["EMA200"] = EMAIndicator(close=df["Close"], window=200).ema_indicator()
    df["RSI"] = RSIIndicator(close=df["Close"], window=14).rsi()

    macd = MACD(close=df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    df["ATR"] = AverageTrueRange(high=df["High"], low=df["Low"], close=df["Close"], window=14).average_true_range()

    bb = BollingerBands(close=df["Close"], window=20, window_dev=2)
    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_LOWER"] = bb.bollinger_lband()
    df["BBWidth"] = (df["BB_UPPER"] - df["BB_LOWER"]) / df["Close"] * 100

    df["Resistance"] = df["High"].rolling(50).max()
    df["Support"] = df["Low"].rolling(50).min()
    df["PriorResistance"] = df["Resistance"].shift(1)
    df["PriorSupport"] = df["Support"].shift(1)

    df["ADX"] = ADXIndicator(high=df["High"], low=df["Low"], close=df["Close"], window=14).adx()

    # فيبوناتشي (سوينغ 34 شمعة)
    df["SwingHigh"] = df["High"].rolling(34).max()
    df["SwingLow"] = df["Low"].rolling(34).min()
    df["Fib618"] = df["SwingHigh"] - (df["SwingHigh"] - df["SwingLow"]) * 0.618
    df["Fib50"] = df["SwingHigh"] - (df["SwingHigh"] - df["SwingLow"]) * 0.5
    df["Fib382"] = df["SwingHigh"] - (df["SwingHigh"] - df["SwingLow"]) * 0.382

    # VWAP تقريبي (لا يوجد فوليوم موثوق لأزواج الفوركس/الذهب بالخطة المجانية، لذا نستخدم متوسط السعر النموذجي)
    df["TypicalPrice"] = (df["High"] + df["Low"] + df["Close"]) / 3
    df["VWAP"] = df["TypicalPrice"].rolling(20).mean()

    if with_divergence:
        df["Divergence"] = compute_divergence(df, lookback=14)
    else:
        df["Divergence"] = 0

    return df


def indicator_labels(price, ema20, ema50, ema200, rsi, macd_value, macd_signal):
    trend_label = "🟢 BULLISH" if price > ema200 else "🔴 BEARISH"
    momentum_label = "🟢 STRONG" if ema20 > ema50 else "🔴 WEAK"
    if rsi > 55: rsi_label = "🟢 BULLISH"
    elif rsi < 45: rsi_label = "🔴 BEARISH"
    else: rsi_label = "🟡 NEUTRAL"
    macd_label = "🟢 BULLISH" if macd_value > macd_signal else "🔴 BEARISH"
    ema200_label = "🟢 ABOVE" if price > ema200 else "🔴 BELOW"
    return trend_label, momentum_label, rsi_label, macd_label, ema200_label


def safe(row, col, default=np.nan):
    v = row[col] if col in row and not pd.isna(row[col]) else default
    return v


def strategy_score(strategy_key, row):
    """يحسب نقاط الإشارة لأي استراتيجية من الصف الكامل (يحتوي كل المؤشرات المحسوبة مسبقاً)."""
    price = row["Close"]
    ema20, ema50, ema200 = safe(row, "EMA20", price), safe(row, "EMA50", price), safe(row, "EMA200", price)
    ema9, ema21 = safe(row, "EMA9"), safe(row, "EMA21")
    rsi = safe(row, "RSI", 50)
    macd_value, macd_signal = safe(row, "MACD", 0), safe(row, "MACD_SIGNAL", 0)
    bb_upper, bb_lower = safe(row, "BB_UPPER", price), safe(row, "BB_LOWER", price)
    prior_resistance, prior_support = safe(row, "PriorResistance"), safe(row, "PriorSupport")
    atr_value = safe(row, "ATR", 0)
    fib618, fib50 = safe(row, "Fib618"), safe(row, "Fib50")
    vwap = safe(row, "VWAP")
    divergence = row["Divergence"] if "Divergence" in row and not pd.isna(row["Divergence"]) else 0

    if strategy_key == "ict":
        score = 0
        score += 1 if price > ema200 else -1
        score += 1 if ema20 > ema50 else -1
        score += 1 if price > ema20 else -1
        score += 1 if rsi > 55 else (-1 if rsi < 45 else 0)
        score += 1 if macd_value > macd_signal else -1
        return score

    if strategy_key == "trend":
        score = 0
        if ema20 > ema50 > ema200: score += 2
        elif ema20 < ema50 < ema200: score -= 2
        score += 1 if price > ema20 else -1
        score += 1 if macd_value > macd_signal else -1
        return score

    if strategy_key == "mean_reversion":
        score = 0
        if rsi < 25: score += 2
        elif rsi > 75: score -= 2
        if price < bb_lower: score += 1
        elif price > bb_upper: score -= 1
        return score

    if strategy_key == "breakout":
        score = 0
        buffer = atr_value * 0.25
        if not pd.isna(prior_resistance) and price > prior_resistance + buffer: score += 2
        elif not pd.isna(prior_support) and price < prior_support - buffer: score -= 2
        score += 1 if macd_value > macd_signal else -1
        score += 1 if rsi > 50 else -1
        return score

    if strategy_key == "scalping":
        score = 0
        if not pd.isna(ema9) and not pd.isna(ema21):
            score += 1 if ema9 > ema21 else -1
        score += 1 if price > (ema9 if not pd.isna(ema9) else price) else -1
        score += 1 if macd_value > macd_signal else -1
        return score

    if strategy_key == "fibonacci":
        score = 0
        trend_up = price > ema200
        if not pd.isna(fib618) and atr_value > 0 and abs(price - fib618) / atr_value < 0.6:
            score += 2 if trend_up else -2
        elif not pd.isna(fib50) and atr_value > 0 and abs(price - fib50) / atr_value < 0.6:
            score += 1 if trend_up else -1
        return score

    if strategy_key == "orderblock":
        score = 0
        candle_range = row["High"] - row["Low"] if "High" in row else 0
        strong_candle = atr_value > 0 and candle_range > 1.4 * atr_value
        if strong_candle and row["Close"] > row.get("Open", row["Close"]):
            score += 2
        elif strong_candle and row["Close"] < row.get("Open", row["Close"]):
            score -= 2
        score += 1 if macd_value > macd_signal else -1
        score += 1 if price > ema50 else -1
        return score

    if strategy_key == "divergence":
        score = divergence * 3
        score += 1 if macd_value > macd_signal else -1
        return score

    if strategy_key == "vwap":
        score = 0
        if not pd.isna(vwap) and atr_value > 0:
            deviation = (price - vwap) / atr_value
            if deviation > 1.2: score -= 2
            elif deviation < -1.2: score += 2
        score += 1 if rsi < 30 else (-1 if rsi > 70 else 0)
        return score

    if strategy_key == "bbsqueeze":
        score = 0
        if price > bb_upper: score += 2
        elif price < bb_lower: score -= 2
        score += 1 if macd_value > macd_signal else -1
        return score

    return 0


def percentile_rank(series, index_pos, lookback=100):
    start = max(0, index_pos - lookback)
    window = series.iloc[start:index_pos]
    current = series.iloc[index_pos]
    valid = window.dropna()
    if valid.empty or pd.isna(current):
        return 50.0
    return (valid < current).mean() * 100


def classify_market_regime(df, index_pos):
    row = df.iloc[index_pos]
    adx_val = row["ADX"] if not pd.isna(row["ADX"]) else 0
    rsi_val = row["RSI"] if not pd.isna(row["RSI"]) else 50
    bbw_percentile = percentile_rank(df["BBWidth"], index_pos)

    if adx_val >= 25:
        return "📈 اتجاه قوي (Trending)", "اتجاهي (Trend Following)"
    elif rsi_val <= 25 or rsi_val >= 75:
        return "🎯 تشبع/تمدد قوي (Stretched)", "ارتدادي (Mean Reversion)"
    elif bbw_percentile <= 30:
        return "🔒 انضغاط بنطاق ضيق (Compression)", "انضغاط بولينجر (BB Squeeze)"
    else:
        return "🌊 سوق متقلب بدون نمط واضح (Choppy)", "ICT / Smart Money Concepts"


def volatility_ok(atr_series, index_pos, lookback=100, min_percentile=35):
    start = max(0, index_pos - lookback)
    window = atr_series.iloc[start:index_pos]
    current = atr_series.iloc[index_pos]
    if window.empty or pd.isna(current) or len(window.dropna()) < 20:
        return True
    pr = (window.dropna() < current).mean() * 100
    return pr >= min_percentile


def get_higher_tf_bias(interval, key):
    hdata, err = get_price_data(interval, key, outputsize=250)
    if hdata.empty:
        return 0, "🟡 غير متوفر"
    hdata = add_indicators(hdata, with_divergence=False)
    hlast = hdata.iloc[-1]
    hprice = float(hlast["Close"])
    hema200 = float(hlast["EMA200"]) if not pd.isna(hlast["EMA200"]) else hprice
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
        return 1, "🟢 سحب سيولة صعودي (كسر قاع ثم ارتداد) — انعكاس محتمل للأعلى"
    elif bearish_sweep and not bullish_sweep:
        return -1, "🔴 سحب سيولة هبوطي (كسر قمة ثم ارتداد) — انعكاس محتمل للأسفل"
    return 0, "🟡 ما كو نمط سحب سيولة واضح حاليًا"


# =========================================================
# التيليجرام
# =========================================================

def send_telegram(token, chat_id, message):
    if not token or not chat_id:
        return False, "التوكن أو Chat ID فارغ"
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        resp = requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"}, timeout=10)
        if resp.status_code == 200:
            return True, "تم الإرسال"
        return False, f"فشل الإرسال ({resp.status_code}): {resp.text[:200]}"
    except Exception as e:
        return False, f"خطأ اتصال: {e}"


# =========================================================
# الأخبار: RSS عام + Forex Factory Calendar
# =========================================================

BULLISH_WORDS = ["rate cut", "cuts rates", "inflation rises", "safe haven", "geopolitical", "tension",
                  "recession", "weak dollar", "dollar falls", "fed dovish", "war", "conflict",
                  "uncertainty", "yields fall", "risk aversion"]
BEARISH_WORDS = ["rate hike", "hikes rates", "strong dollar", "dollar rises", "fed hawkish",
                  "jobs data strong", "risk appetite", "yields rise", "stocks rally",
                  "inflation falls", "strong economy", "rate increase"]
NEWS_FEEDS = ["https://www.investing.com/rss/news_285.rss", "https://www.fxstreet.com/rss/news"]

# مصدر عام (community mirror) لتقويم Forex Factory بصيغة JSON — قد يتوقف أحياناً، لذا نتعامل معه بحذر
FF_CALENDAR_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"


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
                bullish_hits += 1; matched.append((h, "🟢 BULLISH")); break
        else:
            for w in BEARISH_WORDS:
                if w in h_lower:
                    bearish_hits += 1; matched.append((h, "🔴 BEARISH")); break
    if bullish_hits + bearish_hits == 0:
        return 0, "🟡 NEUTRAL", matched
    elif bullish_hits > bearish_hits:
        return 1, "🟢 BULLISH", matched
    elif bearish_hits > bullish_hits:
        return -1, "🔴 BEARISH", matched
    return 0, "🟡 MIXED", matched


@st.cache_data(ttl=600)
def get_forex_factory_events():
    try:
        r = requests.get(FF_CALENDAR_URL, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None, f"تعذر الوصول لتقويم Forex Factory (كود {r.status_code})"
        events = r.json()
        rows = []
        for e in events:
            currency = e.get("country") or e.get("currency", "")
            if currency not in ("USD", "XAU", "ALL", ""):
                if currency != "USD":
                    continue
            rows.append({
                "الوقت": e.get("date", ""),
                "العملة": currency,
                "الحدث": e.get("title", ""),
                "الأهمية": e.get("impact", "Low"),
                "متوقع": e.get("forecast", ""),
                "سابق": e.get("previous", ""),
                "فعلي": e.get("actual", ""),
            })
        return rows, None
    except Exception as e:
        return None, f"تعذر جلب تقويم Forex Factory: {e}"


headlines = get_news()
news_score, news_label, matched_news = analyze_news(headlines)


# =========================================================
# جلب بيانات التحليل الحي
# =========================================================

tf_settings = TIMEFRAMES[tf_choice]
data, error_msg = get_price_data(tf_settings, api_key, outputsize=300)

if data.empty:
    st.error(f"لم نستطع جلب بيانات الذهب الحية. السبب: {error_msg}")
    st.stop()

data = add_indicators(data)
regime_label, recommended_strategy = classify_market_regime(data, len(data) - 1)

last = data.iloc[-1]
price = float(last["Close"])
ema20 = float(safe(last, "EMA20", price))
ema50 = float(safe(last, "EMA50", price))
ema200 = float(safe(last, "EMA200", price))
rsi = float(safe(last, "RSI", 50))
macd_value = float(safe(last, "MACD", 0))
macd_signal = float(safe(last, "MACD_SIGNAL", 0))
atr = float(safe(last, "ATR", 0))

lookback = min(50, len(data))
recent = data.tail(lookback)
resistance = float(recent["High"].max())
support = float(recent["Low"].min())

trend_label, momentum_label, rsi_label, macd_label, ema200_label = indicator_labels(
    price, ema20, ema50, ema200, rsi, macd_value, macd_signal
)

base_score = strategy_score(strategy_cfg["key"], last)
max_possible_base = strategy_cfg["max_score"]

vol_ok = volatility_ok(data["ATR"], len(data) - 1)

higher_bias_score, higher_bias_label = (0, "🟡 غير مستخدم بهذه الاستراتيجية")
if strategy_cfg["use_higher_tf"]:
    higher_bias_score, higher_bias_label = get_higher_tf_bias(HIGHER_TF_MAP[tf_choice], api_key)

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

max_possible_score = max_possible_base + extra_weight
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

entry = price
sl_mult, tp1_mult, tp2_mult = strategy_cfg["sl_mult"], strategy_cfg["tp1_mult"], strategy_cfg["tp2_mult"]

if signal == "BUY":
    sl, tp1, tp2 = entry - atr * sl_mult, entry + atr * tp1_mult, entry + atr * tp2_mult
elif signal == "SELL":
    sl, tp1, tp2 = entry + atr * sl_mult, entry - atr * tp1_mult, entry - atr * tp2_mult
else:
    sl, tp1, tp2 = entry - atr * sl_mult, entry + atr * tp1_mult, entry + atr * tp2_mult

risk = abs(entry - sl)
rr1 = round(abs(tp1 - entry) / risk, 2) if risk > 0 else 0
rr2 = round(abs(tp2 - entry) / risk, 2) if risk > 0 else 0


# =========================================================
# منطق تنبيهات تيليجرام (يرسل فقط عند تغيّر الإشارة)
# =========================================================

if "last_alert_key" not in st.session_state:
    st.session_state.last_alert_key = None
if "pending_orders" not in st.session_state:
    st.session_state.pending_orders = []
if "tg_log" not in st.session_state:
    st.session_state.tg_log = []

alert_key = f"{strategy_choice}|{tf_choice}|{signal}"
if telegram_enabled and signal in ("BUY", "SELL") and alert_key != st.session_state.last_alert_key:
    msg = (
        f"🥇 <b>XAUUSD — إشارة جديدة</b>\n"
        f"الاستراتيجية: {strategy_choice}\n"
        f"الفريم: {tf_choice}\n"
        f"الإشارة: {'🟢 BUY' if signal == 'BUY' else '🔴 SELL'}\n"
        f"السعر الحالي: ${price:,.2f}\n"
        f"الدخول: ${entry:,.2f}\n"
        f"وقف الخسارة SL: ${sl:,.2f}\n"
        f"الهدف TP1: ${tp1:,.2f} (1:{rr1})\n"
        f"الهدف TP2: ${tp2:,.2f} (1:{rr2})\n"
        f"مستوى الثقة: {confidence}%\n\n"
        f"⚠️ إشارة تحليلية آلية وليست توصية مضمونة — أدر رأس مالك بحذر."
    )
    ok, info = send_telegram(tg_token, tg_chat_id, msg)
    st.session_state.tg_log.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] {'✅' if ok else '❌'} {info}")
    st.session_state.last_alert_key = alert_key


# =========================================================
# صفقات معلقة مقترحة (Pending Orders) — تتبّع تلقائي، وليست مضمونة النتيجة
# =========================================================

def refresh_pending_orders(current_price, support, resistance, atr, sl_mult, tp1_mult, tp2_mult, strategy_name):
    orders = st.session_state.pending_orders
    ids_now = {o["id"] for o in orders}
    base_id = f"{strategy_name}-{tf_choice}"

    buy_id, sell_id = f"{base_id}-BUYLIMIT", f"{base_id}-SELLLIMIT"
    if buy_id not in ids_now:
        orders.append({
            "id": buy_id, "type": "BUY LIMIT", "level": round(support, 2),
            "sl": round(support - atr * sl_mult, 2), "tp1": round(support + atr * tp1_mult, 2),
            "tp2": round(support + atr * tp2_mult, 2), "status": "PENDING", "strategy": strategy_name,
        })
    if sell_id not in ids_now:
        orders.append({
            "id": sell_id, "type": "SELL LIMIT", "level": round(resistance, 2),
            "sl": round(resistance + atr * sl_mult, 2), "tp1": round(resistance - atr * tp1_mult, 2),
            "tp2": round(resistance - atr * tp2_mult, 2), "status": "PENDING", "strategy": strategy_name,
        })

    for o in orders:
        if o["strategy"] != strategy_name or o["id"] not in (buy_id, sell_id):
            continue
        if o["status"] == "PENDING":
            triggered = (o["type"] == "BUY LIMIT" and current_price <= o["level"]) or \
                        (o["type"] == "SELL LIMIT" and current_price >= o["level"])
            if triggered:
                o["status"] = "ACTIVE"
                if telegram_enabled and send_pending_alerts:
                    m = (f"⚡ <b>تم تفعيل أمر معلق</b>\n{o['type']} XAUUSD @ ${o['level']:,.2f}\n"
                         f"SL: ${o['sl']:,.2f} | TP1: ${o['tp1']:,.2f} | TP2: ${o['tp2']:,.2f}\n"
                         f"⚠️ ليس ضماناً لتحقيق الهدف.")
                    ok, info = send_telegram(tg_token, tg_chat_id, m)
                    st.session_state.tg_log.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] {'✅' if ok else '❌'} {info}")
        elif o["status"] == "ACTIVE":
            if o["type"] == "BUY LIMIT":
                if current_price >= o["tp1"]: o["status"] = "TP1 ✅"
                elif current_price <= o["sl"]: o["status"] = "SL ❌"
            else:
                if current_price <= o["tp1"]: o["status"] = "TP1 ✅"
                elif current_price >= o["sl"]: o["status"] = "SL ❌"

    st.session_state.pending_orders = orders


refresh_pending_orders(price, support, resistance, atr, sl_mult, tp1_mult, tp2_mult, strategy_choice)


# =========================================================
# محرك الباك تست
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
            sc = strategy_score(strategy_key, row)
            side = "BUY" if sc >= threshold else ("SELL" if sc <= -threshold else None)
            if side:
                entry_price, atr_val = row["Close"], row["ATR"]
                if side == "BUY":
                    sl_price, tp_price = entry_price - atr_val * sl_mult, entry_price + atr_val * tp_mult
                else:
                    sl_price, tp_price = entry_price + atr_val * sl_mult, entry_price - atr_val * tp_mult
                position = {"side": side, "entry": entry_price, "sl": sl_price, "tp": tp_price, "entry_time": df.index[i]}
        else:
            side = position["side"]
            high, low = row["High"], row["Low"]
            hit = None
            if side == "BUY":
                if low <= position["sl"]: hit = "SL"
                elif high >= position["tp"]: hit = "TP"
            else:
                if high >= position["sl"]: hit = "SL"
                elif low <= position["tp"]: hit = "TP"
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


def summarize_trades(t_df):
    if t_df.empty:
        return {"trades": 0, "win_rate": 0.0, "loss_rate": 0.0, "profit_factor": 0.0, "total_pnl": 0.0, "expectancy": 0.0}
    total = len(t_df)
    wins = int((t_df["result"] == "WIN").sum())
    losses = total - wins
    win_rate = round(wins / total * 100, 1)
    loss_rate = round(losses / total * 100, 1)
    gross_win = t_df.loc[t_df["pnl"] > 0, "pnl"].sum()
    gross_loss = abs(t_df.loc[t_df["pnl"] < 0, "pnl"].sum())
    pf = round(gross_win / gross_loss, 2) if gross_loss > 0 else round(gross_win, 2)
    return {
        "trades": total, "win_rate": win_rate, "loss_rate": loss_rate,
        "profit_factor": pf, "total_pnl": round(t_df["pnl"].sum(), 1), "expectancy": round(t_df["pnl"].mean(), 2),
    }


# =========================================================
# التبويبات
# =========================================================

tab_live, tab_leaderboard, tab_backtest, tab_pending, tab_news = st.tabs(
    ["📈 التحليل الحي", "🏆 قائمة الاستراتيجيات", "🧪 باك تست", "📌 صفقات معلقة", "📰 الأخبار"]
)

# ---------- تبويب: التحليل الحي ----------
with tab_live:
    signal_emoji = {"BUY": "🟢", "SELL": "🔴", "WAIT": "🟡"}[signal]
    badge_class = {"BUY": "badge-buy", "SELL": "badge-sell", "WAIT": "badge-wait"}[signal]

    st.markdown(f"""
    <div class="ticker-bar">
        <div class="ticker-item"><span class="ticker-label">XAU/USD</span><span class="ticker-value gold">${price:,.2f}</span></div>
        <div class="ticker-item"><span class="ticker-label">الاتجاه</span><span class="ticker-value">{trend_label}</span></div>
        <div class="ticker-item"><span class="ticker-label">الإشارة</span><span class="signal-badge {badge_class}">{signal_emoji} {signal}</span></div>
        <div class="ticker-item"><span class="ticker-label">الثقة</span><span class="ticker-value gold">{confidence}%</span></div>
        <div class="ticker-item"><span class="ticker-label">آخر تحديث</span><span class="ticker-value" style="font-size:0.9rem;">{data.index[-1].strftime('%H:%M:%S')}</span></div>
    </div>
    """, unsafe_allow_html=True)

    if recommended_strategy == strategy_choice:
        st.success(f"🔎 **نظام السوق:** {regime_label} — استراتيجيتك ({strategy_choice}) مناسبة لهذا النظام ✅")
    else:
        st.info(f"🔎 **نظام السوق:** {regime_label} — الأنسب حالياً حسب النظام: **{recommended_strategy}**.")

    if conflict_warning:
        st.warning(conflict_warning)
    if not vol_ok:
        st.warning("💤 السوق هادئ حالياً (ATR منخفض) — تم تعطيل الإشارة تلقائياً لتفادي صفقات ضعيفة الجودة.")

    st.divider()
    st.subheader("🧠 التحليل متعدد الأبعاد")
    d1, d2 = st.columns(2)
    with d1: st.markdown(f"**📐 الاتجاه الأكبر:**\n\n{higher_bias_label}")
    with d2: st.markdown(f"**💧 تحليل السيولة:**\n\n{liquidity_msg}")

    st.divider()
    st.subheader("📊 المؤشرات الفنية")
    a1, a2, a3, a4, a5 = st.columns(5)
    with a1: st.markdown(f"**Trend**\n\n{trend_label}")
    with a2: st.markdown(f"**Momentum**\n\n{momentum_label}")
    with a3: st.markdown(f"**RSI**\n\n{rsi_label} ({rsi:.1f})")
    with a4: st.markdown(f"**MACD**\n\n{macd_label}")
    with a5: st.markdown(f"**EMA 200**\n\n{ema200_label}")

    st.divider()
    st.subheader("🎯 خطة الصفقة المقترحة")
    if signal == "WAIT":
        st.warning("لا يوجد توافق كافٍ حسب هذه الاستراتيجية الآن (WAIT). الأفضل الانتظار.")
    else:
        s1, s2, s3, s4 = st.columns(4)
        with s1: st.metric("الدخول (Entry)", f"${entry:,.2f}")
        with s2: st.metric("وقف الخسارة (SL)", f"${sl:,.2f}")
        with s3: st.metric("الهدف الأول (TP1)", f"${tp1:,.2f}")
        with s4: st.metric("الهدف الثاني (TP2)", f"${tp2:,.2f}")
        st.caption(f"Risk/Reward إلى TP1 = 1:{rr1} | إلى TP2 = 1:{rr2} | حجم الوقف: {atr*sl_mult:.2f} نقطة")
        st.info("💡 عند الوصول لـ TP1، فكر بإغلاق نصف الصفقة ونقل الوقف لنقطة الدخول (Break-Even).")

    st.caption(f"Support: ${support:,.2f} | Resistance: ${resistance:,.2f} | ATR: {atr:.2f}")

    st.divider()
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"],
                                  name="XAUUSD", increasing_line_color="#29c48a", decreasing_line_color="#ff5c5c",
                                  increasing_fillcolor="#29c48a", decreasing_fillcolor="#ff5c5c"))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA20"], name="EMA 20", line=dict(width=1, color="#f0d78c")))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA50"], name="EMA 50", line=dict(width=1, color="#8b93a0")))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA200"], name="EMA 200", line=dict(width=2, color="#d4af37")))
    fig.add_hline(y=resistance, line_dash="dash", line_color="#ff5c5c", annotation_text="Resistance")
    fig.add_hline(y=support, line_dash="dash", line_color="#29c48a", annotation_text="Support")
    fig.update_layout(title=f"شارت الذهب - {tf_choice} - {strategy_choice}", height=560,
                       xaxis_rangeslider_visible=False, template="plotly_dark",
                       paper_bgcolor="#05070c", plot_bgcolor="#10141c",
                       font=dict(family="JetBrains Mono, monospace", color="#f1efe9"),
                       legend=dict(bgcolor="rgba(0,0,0,0)"), margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.warning("هذه الإشارة تحليلية وليست ضماناً لحركة السوق. لا تخاطر بأكثر مما تتحمل خسارته.")


# ---------- تبويب: قائمة الاستراتيجيات (Leaderboard حقيقي بالباك تست) ----------
with tab_leaderboard:
    st.subheader("🏆 كل الاستراتيجيات — نسب ربح/خسارة محسوبة فعلياً من باك تست")
    st.caption(
        "الجدول أدناه يشغّل كل استراتيجية على نفس البيانات التاريخية (الفريم والعدد المختارين بالشريط الجانبي) "
        "ويحسب نسبة الصفقات الرابحة/الخاسرة الحقيقية — وليست أرقاماً ثابتة أو مُختلقة. النتائج تتغير حسب الفريم والفترة."
    )
    run_leaderboard = st.button("🔄 شغّل / حدّث المقارنة الآن", type="primary")

    if run_leaderboard or "leaderboard_df" in st.session_state:
        if run_leaderboard:
            with st.spinner("جاري تحميل البيانات وتشغيل الباك تست على كل الاستراتيجيات..."):
                lb_data, lb_err = get_price_data(tf_settings, api_key, outputsize=backtest_candles)
                if lb_data.empty:
                    st.error(f"تعذر جلب بيانات كافية. السبب: {lb_err}")
                else:
                    lb_data = add_indicators(lb_data)
                    rows = []
                    for name, cfg in STRATEGIES.items():
                        t_df = run_backtest(lb_data, cfg["key"], cfg["sl_mult"], cfg["tp2_mult"], cfg["threshold"])
                        s = summarize_trades(t_df)
                        rows.append({
                            "الاستراتيجية": name, "عدد الصفقات": s["trades"],
                            "نسبة الربح %": s["win_rate"], "نسبة الخسارة %": s["loss_rate"],
                            "Profit Factor": s["profit_factor"], "إجمالي النقاط": s["total_pnl"],
                            "Expectancy/صفقة": s["expectancy"],
                        })
                    st.session_state.leaderboard_df = pd.DataFrame(rows).sort_values("إجمالي النقاط", ascending=False).reset_index(drop=True)

        if "leaderboard_df" in st.session_state:
            df_lb = st.session_state.leaderboard_df
            st.dataframe(df_lb, use_container_width=True, hide_index=True)
            best = df_lb.iloc[0]
            if best["إجمالي النقاط"] > 0:
                st.success(f"🥇 الأفضل على هذه الفترة/الفريم: **{best['الاستراتيجية']}** — نسبة ربح {best['نسبة الربح %']}%، "
                           f"Profit Factor {best['Profit Factor']}، بـ {int(best['عدد الصفقات'])} صفقة.")
            else:
                st.warning("لم تحقق أي استراتيجية ربحاً إجمالياً موجباً على هذه الفترة/الفريم — جرّب فريماً أو فترة أطول.")
            st.caption("💡 النتائج تتغير مع الفريم وعدد الشموع — كرر التشغيل دورياً بدل الاعتماد على تشغيل واحد.")
    else:
        st.info("اضغط الزر أعلاه لتشغيل المقارنة على كل الاستراتيجيات العشر.")

    st.divider()
    st.subheader("📖 وصف كل استراتيجية")
    for name, cfg in STRATEGIES.items():
        st.markdown(f"""
        <div class="glass-card">
        <b>{name}</b><br>
        <span style="color:var(--text-muted);">{cfg['description']}</span><br><br>
        <span class="pill pill-med">SL × {cfg['sl_mult']} ATR</span>
        <span class="pill pill-low">TP1 × {cfg['tp1_mult']} ATR</span>
        <span class="pill pill-low">TP2 × {cfg['tp2_mult']} ATR</span>
        {"<span class='pill pill-high'>يستخدم السيولة</span>" if cfg['use_liquidity'] else ""}
        {"<span class='pill pill-high'>يستخدم فريم أعلى</span>" if cfg['use_higher_tf'] else ""}
        </div>
        """, unsafe_allow_html=True)


# ---------- تبويب: باك تست تفصيلي لاستراتيجية واحدة ----------
with tab_backtest:
    st.subheader(f"🧪 اختبار تفصيلي: {strategy_choice}")
    run_bt = st.button("▶️ شغّل الباك تست", type="primary")

    if run_bt:
        with st.spinner("جاري تحميل البيانات التاريخية وتشغيل الاختبار..."):
            bt_data, bt_error = get_price_data(tf_settings, api_key, outputsize=backtest_candles)
            if bt_data.empty:
                st.error(f"تعذر جلب بيانات كافية. السبب: {bt_error}")
            else:
                bt_data = add_indicators(bt_data)
                trades_df = run_backtest(bt_data, strategy_cfg["key"], strategy_cfg["sl_mult"], strategy_cfg["tp2_mult"], strategy_cfg["threshold"])

                if trades_df.empty:
                    st.info("ما صارت أي صفقة خلال الفترة المختارة. جرب تزيد عدد الشموع أو تغير الفريم.")
                else:
                    s = summarize_trades(trades_df)
                    b1, b2, b3, b4 = st.columns(4)
                    with b1: st.metric("عدد الصفقات", s["trades"])
                    with b2: st.metric("نسبة الربح", f"{s['win_rate']}%")
                    with b3: st.metric("نسبة الخسارة", f"{s['loss_rate']}%")
                    with b4: st.metric("إجمالي النقاط", f"{s['total_pnl']:,.1f}")
                    b5, b6 = st.columns(2)
                    with b5: st.metric("Profit Factor", f"{s['profit_factor']}")
                    with b6: st.metric("Expectancy/صفقة", f"{s['expectancy']:+.2f}")

                    trades_df["cumulative_pnl"] = trades_df["pnl"].cumsum()
                    eq_fig = go.Figure()
                    eq_fig.add_trace(go.Scatter(x=trades_df["exit_time"], y=trades_df["cumulative_pnl"],
                                                 mode="lines+markers", name="Cumulative PnL",
                                                 line=dict(color="#29c48a" if s["total_pnl"] >= 0 else "#ff5c5c", width=2),
                                                 marker=dict(size=5, color="#d4af37")))
                    eq_fig.update_layout(title="منحنى الأداء التراكمي (نقاط)", height=380, template="plotly_dark",
                                          paper_bgcolor="#05070c", plot_bgcolor="#10141c",
                                          font=dict(family="JetBrains Mono, monospace", color="#f1efe9"),
                                          margin=dict(l=10, r=10, t=50, b=10))
                    st.plotly_chart(eq_fig, use_container_width=True)

                    st.subheader("📋 سجل الصفقات")
                    disp = trades_df.copy()
                    disp["entry_time"] = disp["entry_time"].dt.strftime("%Y-%m-%d %H:%M")
                    disp["exit_time"] = disp["exit_time"].dt.strftime("%Y-%m-%d %H:%M")
                    for c in ["entry", "exit", "pnl"]:
                        disp[c] = disp[c].round(2)
                    disp = disp.rename(columns={"side": "الاتجاه", "entry_time": "الدخول", "exit_time": "الخروج",
                                                 "entry": "سعر الدخول", "exit": "سعر الخروج", "result": "النتيجة", "pnl": "النقاط"})
                    st.dataframe(disp, use_container_width=True, hide_index=True)
    else:
        st.info("اضغط الزر أعلاه لتشغيل الاختبار على البيانات التاريخية لهذه الاستراتيجية.")


# ---------- تبويب: صفقات معلقة ----------
with tab_pending:
    st.subheader("📌 صفقات معلقة مقترحة (متابَعة تلقائياً)")
    st.warning(
        "هذه أوامر معلقة **مقترحة** بناءً على الدعم/المقاومة الحاليين — **وليست مضمونة النتيجة**. "
        "يتابعها الموقع تلقائياً عند كل تحديث، وإذا كان تيليجرام مفعّلاً سيصلك تنبيه عند التفعيل أو الإغلاق."
    )
    if st.session_state.pending_orders:
        pend_df = pd.DataFrame(st.session_state.pending_orders)
        pend_df = pend_df.rename(columns={"id": "المعرف", "type": "النوع", "level": "السعر", "sl": "SL",
                                           "tp1": "TP1", "tp2": "TP2", "status": "الحالة", "strategy": "الاستراتيجية"})
        st.dataframe(pend_df[["الاستراتيجية", "النوع", "السعر", "SL", "TP1", "TP2", "الحالة"]],
                     use_container_width=True, hide_index=True)
        if st.button("🗑️ مسح كل الأوامر المعلقة"):
            st.session_state.pending_orders = []
            st.rerun()
    else:
        st.info("لا توجد أوامر معلقة حالياً.")

    if telegram_enabled:
        st.divider()
        st.subheader("📜 سجل إرسال تيليجرام")
        if st.session_state.tg_log:
            for line in st.session_state.tg_log[:10]:
                st.text(line)
        else:
            st.caption("لم يتم إرسال أي تنبيه بعد.")


# ---------- تبويب: الأخبار ----------
with tab_news:
    st.subheader("📰 تحليل الأخبار العامة")
    st.markdown(f"**الحالة العامة:** {news_label}")
    if matched_news:
        with st.expander("العناوين المؤثرة المرصودة"):
            for title, label in matched_news[:10]:
                st.write(f"{label} — {title}")
    else:
        st.caption("لا توجد عناوين واضحة التأثير حالياً.")

    st.divider()
    st.subheader("🗓️ تقويم Forex Factory (أحداث الدولار الأمريكي)")
    ff_rows, ff_err = get_forex_factory_events()
    if ff_err:
        st.warning(f"{ff_err} — جرّب لاحقاً، المصدر خارجي وقد يكون غير متاح مؤقتاً.")
    elif not ff_rows:
        st.info("لا توجد أحداث دولارية هذا الأسبوع حسب المصدر.")
    else:
        ff_df = pd.DataFrame(ff_rows)
        impact_order = {"High": 0, "Medium": 1, "Low": 2}
        ff_df["_sort"] = ff_df["الأهمية"].map(impact_order).fillna(3)
        ff_df = ff_df.sort_values("_sort").drop(columns="_sort")
        st.dataframe(ff_df, use_container_width=True, hide_index=True)
        st.caption("المصدر: تجميع مجتمعي لبيانات Forex Factory (غير رسمي) — تحقق دائماً من الموقع الرسمي forexfactory.com لأي قرار حساس.")
