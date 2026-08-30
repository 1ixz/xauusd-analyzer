
Claude finished the response

Thought for 18s
Thought for 18s
شكرًا لصراحتك، وهذا رقم مهم يخليني أشخص المشكلة صح. نسبة ربح تحت 40% مو معناها "الاستراتيجية فاشلة تمامًا" — أحيانًا الاستراتيجية ممكن تربح فلوس حتى بنسبة ربح 35% إذا كان حجم الأرباح أكبر من حجم الخسائر (Risk/Reward قوي)، بس أول شي، السبب الحقيقي غالبًا واحد من هذول:

الموقع يدخل صفقات كثيرة بجودة ضعيفة (السوق هادئ/متذبذب وما كو حركة حقيقية، بس الشروط تتحقق بالصدفة)
الاختراقات تطلع وهمية (Fake Breakout) — السعر يكسر المقاومة بمليمتر وبعدها يرجع
الرقم اللي نشوفه (Win Rate) وحده مو كافي — نحتاج نشوف Profit Factor (نسبة الأرباح للخسائر) مو بس عدد الصفقات الرابحة
راح أسوي 3 تحسينات حقيقية:


Edited 10 files, ran 8 commands, viewed 6 files · 11 notes
Edited 10 files, ran 8 commands, viewed 6 files · 11 notes
شنو تغير بالضبط وليش هذا حل حقيقي مو وعد فاضي:

فلتر التذبذب (Volatility Filter) — الموقع الحين ما يدخل أي صفقة إذا كان السوق "ميت" (تذبذب واطي)، لأن أغلب الإشارات الخاطئة تصير بهذي الأوقات بالضبط. هذا وحده غالبًا يرفع الجودة بشكل ملموس.
استراتيجية الاختراق صارت أدق — قبل، أي كسر بسيط (حتى مليمتر) كان يعتبر اختراق. الحين لازم يكسر بمسافة حقيقية (ربع الـ ATR) حتى نتجنب الاختراقات الوهمية اللي ترجع فورًا.
الاستراتيجية الارتدادية صارت أشد — بدل RSI عند 30/70، الحين لازم يوصل 25/75 (تشبع فعلي قوي)، يقلل عدد الإشارات بس يرفع جودتها.
مقياس Profit Factor و Expectancy — هذا الأهم. نسبة الربح لحالها رقم مخادع. استراتيجية بنسبة ربح 35% ممكن تكون رابحة فعليًا إذا كانت أرباحها الكبيرة تغطي خسائرها الصغيرة المتكررة. الموقع الحين يوريك هذا بوضوح.
اعمل نفس خطوات التحديث المعتادة (استبدال بـ GitHub → Reboot)، وبعدها شغل الباك تست من جديد على كل استراتيجية وشوف رقمين مو وحد: Win Rate و Profit Factor. ارسللي الصورة وأشوف وياك شنو أفضل استراتيجية وفريم زمني فعليًا يعطي نتيجة إيجابية حقيقية.


App
PY 
اريدك ايضا ان تقوم بفحص جميع استراتيجيات العالم بالذهب وتقوم باختبارهم وتعطيني افضل الاستراتيجات والتحليلات الذي حققت ربح اخر فتره


Thought for 13s
Thought for 13s
فهمتك، بس خليني أوضح شي مهم قبل ما أسوي هذا: "فحص جميع استراتيجيات العالم" غير ممكن حرفيًا (فيه آلاف الاستراتيجيات والتوليفات)، وأي مصدر يدعي "هذي الاستراتيجية حققت أرباح X% بالفترة الأخيرة" غالبًا كلام تسويقي غير موثق أو نتائج منتقاة (Cherry-picked) عشان تبيعلك كورس أو إشارات.

الطريقة الصحيحة والموثوقة فعليًا: نضيف أشهر الاستراتيجيات المعروفة عالميًا بتداول الذهب (فوق الأربعة الموجودة)، وبعدين موقعك نفسه يختبرهم على بيانات حقيقية حديثة بضغطة زر — هذا أدق بكثير من أي رقم أقوله لك من كلامي، لأنه مبني على بيانات فعلية مو ادعاءات.

خليني أول أشوف شنو الظروف الحالية بسوق الذهب حتى أعرف أضيف الاستراتيجيات المناسبة:


Searched the web
Searched the web
النتائج مثيرة للاهتمام — أهم شي طلع بالبحث: مافي استراتيجية وحدة "الأفضل" بشكل دائم أدلة من مصادر متعددة تقول التحليل الحديث بيعطهب الذهب يعتمد على تحديد "نظام السوق" (Market Regime) الحالي أولاً — هل هو متجه بقوة، متذبذب بنطاق ضيق، متشبع، أو متقلب بسبب أخبار — وبعدين تختار الاستراتيجية المناسبة لهذا النظام تحديدًا لأن كل استراتيجية تفشل بالبيئة الخطأ ماكو استراتيجية واحدة تكسب لأنه بحسب مصدر (LiteFinance) عمليات كسر الاتجاه (Breakout) والالتفاف حول الاتجاه (Trend-following) وتحليل الشموع الفنية أهم أساليب التداول بالذهب حاليًا.

هذا يعطيني فكرة أقوى بكثير من "أفضل استراتيجية ثابتة" — راح أضيف لك ميزتين حقيقيتين:

كاشف نظام السوق (Market Regime Detector) — يحلل السوق تلقائيًا ويقولك "هذا السوق متجه/متذبذب/متشبع" وينصحك بأنسب استراتيجية من الأربعة الموجودة الآن بالذات
مقارنة كل الاستراتيجيات دفعة وحدة — زر واحد يشغل الباك تست على الأربعة كلهم بنفس الفريم والفترة، ويطلع لك جدول مرتب حسب الأداء الحقيقي (مو كلامي أنا، بيانات حقيقية من موقعك)
خليني أطبقهم:


Edited 6 files, ran 5 commands, viewed 3 files · 7 notes
Edited 6 files, ran 5 commands, viewed 3 files · 7 notes
شنو أضفت بالضبط:

1. كاشف نظام السوق (Market Regime Detector)
الموقع الحين يحلل تلقائيًا:

ADX (قوة الاتجاه) — إذا فوق 25 يعني اتجاه قوي
RSI المتطرف — تشبع شرائي/بيعي حقيقي
عرض نطاقات بولينجر — انضغاط قبل انفجار محتمل
وبناءً عليها يقولك بأعلى الصفحة: "نظام السوق الحالي: كذا — الاستراتيجية الأنسب هي كذا". إذا كانت استراتيجيتك المختارة مو المناسبة، يوريك تحذير ويقترح تبدلها.

2. مقارنة الاستراتيجيات الأربعة دفعة وحدة
زر جديد بتبويب الباك تست: "🏆 قارن كل الاستراتيجيات الأربعة الآن" — يشغلهم كلهم على نفس البيانات بالضبط، ويطلع جدول مرتب حسب الأداء الحقيقي (نقاط + Profit Factor)، ويقولك بوضوح مين الأفضل بهذا الفريم وهذي الفترة تحديدًا.

⚠️ مهم أوضحه: النتيجة مو ثابتة للأبد — السوق يتغير، فالاستراتيجية الرابحة اليوم ممكن تختلف الأسبوع الجاي. لهذا الموقع يخليك تعيد المقارنة وقت ما تريد بدل ما يقولك رقم واحد ثابت للأبد.

اعمل نفس خطوات التحديث (استبدال app.py بـ GitHub → Reboot)، وبعدها روح لتبويب الباك تست واضغط زر المقارنة. ارسللي صورة من الجدول وأشوف وياك شنو طلع أفضل توليفة فعليًا على بياناتك.


App
PY 
غيرلي شكل الموقع وخليه modren والوان متناسقه


Check frontend design skill for cohesive color/typography guidance applicable to custom CSS styling
Check frontend design skill for cohesive color/typography guidance applicable to custom CSS styling
حلو، خلني أسوي لك هوية بصرية متكاملة ومتناسقة بدل الألوان الافتراضية. بما إن الموقع عن تداول الذهب، راح أستخدم طابع "منصة تداول احترافية" — خلفية داكنة عميقة، ذهبي عتيق (مو أصفر فاقع)، أخضر زمردي للصعود، أحمر خمري للهبوط، مع خط عرض حديث للأرقام يعطي إحساس شاشة تداول حقيقية.


Ran 4 commands, viewed 4 files, edited 4 files · 6 notes
Ran 4 commands, viewed 4 files, edited 4 files · 6 notes
شنو تغير بالتصميم:

🎨 هوية لونية متكاملة — بدل الألوان العشوائية:

خلفية داكنة عميقة (Trading Terminal الحقيقي)
ذهبي عتيق 
#C9A227 للعناصر الرئيسية (مو أصفر فاقع)
أخضر زمردي هادئ للصعود، أحمر خمري للهبوط (بدل الألوان الفاقعة)
🔤 خطوط احترافية — عنوان الموقع بخط "Space Grotesk" الهندسي الحديث، والأرقام والأسعار بخط "JetBrains Mono" (نفس النوع المستخدم بشاشات التداول الحقيقية) — يعطي إحساس دقة ورسمية.

📊 شريط تيكر مميز (العنصر الأبرز بالتصميم الجديد) — بأعلى صفحة التحليل الحي، يعرض السعر/الاتجاه/الإشارة/الثقة/آخر تحديث بشكل أفقي أنيق زي شاشات بلومبيرغ.

📈 الشارتات صارت متناسقة — الشمعات، المتوسطات، ومنحنى الأداء كلهم يستخدمون نفس لوحة الألوان بدل الألوان الافتراضية لـ Plotly.

🔘 تفاصيل صغيرة — التبويبات، الأزرار، البطاقات كلها منسقة بنفس الروح.

اعمل نفس خطوات التحديث (استبدال app.py بـ GitHub → Reboot)، وأرسل لي صورة من الشكل الجديد بعد ما يشتغل.


App
PY 

Write a message…


App · PY
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import feedparser
import requests
from streamlit_autorefresh import st_autorefresh
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator, ADXIndicator
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
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');
 
    :root {
        --bg-deep: #0A0E14;
        --bg-panel: #12161F;
        --gold: #C9A227;
        --gold-soft: #E4C55E;
        --emerald: #2E9E6D;
        --rust: #C1443B;
        --text-primary: #E8E6E1;
        --text-muted: #8B93A0;
        --border-soft: rgba(201,162,39,0.22);
    }
 
    .main .block-container { padding-top: 1.5rem; max-width: 1200px; }
 
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.01em; }
 
    h1 {
        background: linear-gradient(90deg, var(--gold) 0%, var(--gold-soft) 55%, var(--gold) 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
 
    /* شريط التيكر الرئيسي - العنصر المميز بالتصميم */
    .ticker-bar {
        display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;
        gap: 18px;
        background: linear-gradient(135deg, var(--bg-panel), #0D1119);
        border: 1px solid var(--border-soft);
        border-left: 4px solid var(--gold);
        border-radius: 10px;
        padding: 16px 24px;
        margin: 10px 0 22px 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .ticker-item { display: flex; flex-direction: column; gap: 2px; }
    .ticker-label { font-size: 0.72rem; color: var(--text-muted); letter-spacing: 0.06em; text-transform: uppercase; }
    .ticker-value { font-size: 1.35rem; font-weight: 700; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; }
    .ticker-value.gold { color: var(--gold-soft); }
 
    /* بطاقات المقاييس */
    div[data-testid="stMetric"] {
        background: linear-gradient(160deg, rgba(201,162,39,0.07), rgba(201,162,39,0.015));
        border: 1px solid var(--border-soft);
        border-radius: 12px;
        padding: 14px 18px;
    }
    div[data-testid="stMetricLabel"] { font-weight: 600; opacity: 0.8; font-size: 0.85rem; }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; color: var(--text-primary); }
 
    /* بطاقة الاستراتيجية */
    .strategy-card {
        background: var(--bg-panel);
        border: 1px solid var(--border-soft);
        border-right: 3px solid var(--gold);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 10px;
        line-height: 1.7;
    }
 
    /* شارات الإشارة */
    .signal-badge {
        display: inline-block;
        padding: 7px 22px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.15rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.03em;
    }
    .badge-buy  { background: rgba(46,158,109,0.16); color: var(--emerald); border: 1px solid var(--emerald); }
    .badge-sell { background: rgba(193,68,59,0.16);  color: var(--rust);    border: 1px solid var(--rust); }
    .badge-wait { background: rgba(201,162,39,0.16); color: var(--gold-soft); border: 1px solid var(--gold); }
 
    /* التبويبات */
    .stTabs [data-baseweb="tab"] { font-family: 'Space Grotesk', sans-serif; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: var(--gold-soft) !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: var(--gold) !important; }
 
    /* الأزرار */
    div[data-testid="stButton"] > button {
        border: 1px solid var(--border-soft);
        border-radius: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: var(--gold); color: #0A0E14; border: none;
    }
 
    hr { border-color: var(--border-soft) !important; }
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
 
    adx_ind = ADXIndicator(high=df["High"], low=df["Low"], close=df["Close"], window=14)
    df["ADX"] = adx_ind.adx()
    df["BBWidth"] = (df["BB_UPPER"] - df["BB_LOWER"]) / df["Close"] * 100
 
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
 
 
def percentile_rank(series, index_pos, lookback=100):
    start = max(0, index_pos - lookback)
    window = series.iloc[start:index_pos]
    current = series.iloc[index_pos]
    valid = window.dropna()
    if valid.empty or pd.isna(current):
        return 50.0
    return (valid < current).mean() * 100
 
 
def classify_market_regime(df, index_pos):
    """
    يحدد 'نظام السوق' الحالي حسب مفاهيم معروفة بتحليل الذهب:
    - اتجاه قوي (ADX عالي) -> يناسب الاستراتيجية الاتجاهية
    - تشبع شرائي/بيعي قوي (RSI متطرف) -> يناسب الاستراتيجية الارتدادية
    - انضغاط بنطاق ضيق (بولينجر ضيق) -> يناسب استراتيجية الاختراق (ينتظر الانفجار)
    - غير ذلك: سوق متقلب بدون نمط واضح -> يناسب ICT (سيولة + فريم أعلى)
    """
    row = df.iloc[index_pos]
    adx_val = row["ADX"] if not pd.isna(row["ADX"]) else 0
    rsi_val = row["RSI"] if not pd.isna(row["RSI"]) else 50
    bbw_percentile = percentile_rank(df["BBWidth"], index_pos)
 
    if adx_val >= 25:
        return "📈 اتجاه قوي (Trending)", "اتجاهي (Trend Following)"
    elif rsi_val <= 25 or rsi_val >= 75:
        return "🎯 تشبع/تمدد قوي (Stretched)", "ارتدادي (Mean Reversion)"
    elif bbw_percentile <= 30:
        return "🔒 انضغاط بنطاق ضيق (Compression)", "اختراق (Breakout)"
    else:
        return "🌊 سوق متقلب بدون نمط واضح (Choppy)", "ICT / Smart Money Concepts"
 
 
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
 
regime_label, recommended_strategy = classify_market_regime(data, len(data) - 1)
 
 
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
 
    signal_emoji = {"BUY": "🟢", "SELL": "🔴", "WAIT": "🟡"}[signal]
    badge_class = {"BUY": "badge-buy", "SELL": "badge-sell", "WAIT": "badge-wait"}[signal]
 
    st.markdown(f"""
    <div class="ticker-bar">
        <div class="ticker-item">
            <span class="ticker-label">XAU/USD</span>
            <span class="ticker-value gold">${price:,.2f}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">الاتجاه</span>
            <span class="ticker-value">{trend_label}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">الإشارة</span>
            <span class="signal-badge {badge_class}">{signal_emoji} {signal}</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">الثقة</span>
            <span class="ticker-value gold">{confidence}%</span>
        </div>
        <div class="ticker-item">
            <span class="ticker-label">آخر تحديث</span>
            <span class="ticker-value" style="font-size:0.95rem;">{data.index[-1].strftime('%H:%M:%S')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    if recommended_strategy == strategy_choice:
        st.success(f"🔎 **نظام السوق الحالي:** {regime_label} — استراتيجيتك المختارة ({strategy_choice}) مناسبة تمامًا لهذا النظام ✅")
    else:
        st.info(
            f"🔎 **نظام السوق الحالي:** {regime_label} — الاستراتيجية الأنسب حاليًا حسب تحليل النظام هي "
            f"**{recommended_strategy}**. أنت مستخدم **{strategy_choice}**، جرب تبدلها من الشريط الجانبي لمقارنة النتيجة."
        )
 
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
        low=data["Low"], close=data["Close"], name="XAUUSD",
        increasing_line_color="#2E9E6D", decreasing_line_color="#C1443B",
        increasing_fillcolor="#2E9E6D", decreasing_fillcolor="#C1443B",
    ))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA20"], name="EMA 20",
                              line=dict(width=1, color="#E4C55E")))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA50"], name="EMA 50",
                              line=dict(width=1, color="#8B93A0")))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA200"], name="EMA 200",
                              line=dict(width=2, color="#C9A227")))
    fig.add_hline(y=resistance, line_dash="dash", line_color="#C1443B", annotation_text="Resistance")
    fig.add_hline(y=support, line_dash="dash", line_color="#2E9E6D", annotation_text="Support")
    fig.update_layout(
        title=f"شارت الذهب - {tf_choice} - {strategy_choice}",
        height=600,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        paper_bgcolor="#0A0E14",
        plot_bgcolor="#12161F",
        font=dict(family="JetBrains Mono, monospace", color="#E8E6E1"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)
 
    st.divider()
    st.warning("هذه الإشارة تحليلية وليست ضماناً لحركة السوق. لا تخاطر بأكثر مما تتحمل خسارته.")
 
 
with tab_backtest:
 
    st.subheader(f"🧪 اختبار استراتيجية: {strategy_choice}")
    st.caption(
        "هذا الاختبار يطبق منطق الاستراتيجية المختارة فقط (بدون أخبار/سيولة/فريم أعلى، لأنها تحتاج "
        "طلبات API إضافية غير متاحة بكثرة بالخطة المجانية). يعطيك فكرة واقعية عن قوة الأساس الفني."
    )
 
    bt_col1, bt_col2 = st.columns(2)
    with bt_col1:
        run_bt = st.button("▶️ شغّل الباك تست لهذي الاستراتيجية فقط", type="primary")
    with bt_col2:
        run_all_bt = st.button("🏆 قارن كل الاستراتيجيات الأربعة الآن")
 
    if run_all_bt:
        with st.spinner("جاري تحميل البيانات وتشغيل الباك تست على الاستراتيجيات الأربعة..."):
            cmp_data, cmp_error = get_price_data(tf_settings, api_key, outputsize=backtest_candles)
 
            if cmp_data.empty:
                st.error(f"تعذر جلب بيانات كافية للمقارنة. السبب: {cmp_error}")
            else:
                cmp_data = add_indicators(cmp_data)
                comparison_rows = []
 
                for strat_name, cfg in STRATEGIES.items():
                    t_df = run_backtest(cmp_data, cfg["key"], cfg["sl_mult"], cfg["tp2_mult"], cfg["threshold"])
 
                    if t_df.empty:
                        comparison_rows.append({
                            "الاستراتيجية": strat_name, "عدد الصفقات": 0, "نسبة الربح %": 0,
                            "Profit Factor": 0, "إجمالي النقاط": 0, "Expectancy": 0
                        })
                        continue
 
                    t_total = len(t_df)
                    t_wins = (t_df["result"] == "WIN").sum()
                    t_win_rate = round(t_wins / t_total * 100, 1)
                    t_gross_win = t_df.loc[t_df["pnl"] > 0, "pnl"].sum()
                    t_gross_loss = abs(t_df.loc[t_df["pnl"] < 0, "pnl"].sum())
                    t_pf = round(t_gross_win / t_gross_loss, 2) if t_gross_loss > 0 else round(t_gross_win, 2)
                    t_total_pnl = round(t_df["pnl"].sum(), 1)
                    t_expectancy = round(t_df["pnl"].mean(), 2)
 
                    comparison_rows.append({
                        "الاستراتيجية": strat_name, "عدد الصفقات": t_total, "نسبة الربح %": t_win_rate,
                        "Profit Factor": t_pf, "إجمالي النقاط": t_total_pnl, "Expectancy": t_expectancy
                    })
 
                comparison_df = pd.DataFrame(comparison_rows).sort_values(
                    by="إجمالي النقاط", ascending=False
                ).reset_index(drop=True)
 
                st.subheader("🏆 نتيجة المقارنة — نفس البيانات ونفس الفترة لكل الاستراتيجيات")
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)
 
                best_row = comparison_df.iloc[0]
                if best_row["إجمالي النقاط"] > 0:
                    st.success(
                        f"🥇 **الأفضل على هذه الفترة والفريم:** {best_row['الاستراتيجية']} — "
                        f"إجمالي {best_row['إجمالي النقاط']:+.1f} نقطة، Profit Factor = {best_row['Profit Factor']}، "
                        f"بـ {int(best_row['عدد الصفقات'])} صفقة."
                    )
                else:
                    st.warning(
                        "⚠️ ولا وحدة من الاستراتيجيات الأربعة حققت ربح إجمالي موجب على هذه الفترة والفريم. "
                        "جرب فريم زمني آخر أو فترة تاريخية أطول من الشريط الجانبي."
                    )
 
                st.caption(
                    "💡 هذه المقارنة تتغير حسب الفريم الزمني وعدد الشموع المختار — النتيجة اليوم قد تختلف الأسبوع الجاي. "
                    "الأفضل تكرر هذا الاختبار بشكل دوري بدل الاعتماد على نتيجة واحدة بشكل دائم."
                )
 
        st.divider()
 
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
                        line=dict(color="#2E9E6D" if total_pnl >= 0 else "#C1443B", width=2),
                        marker=dict(size=5, color="#C9A227")
                    ))
                    equity_fig.update_layout(
                        title="منحنى الأداء التراكمي (بالنقاط)", height=400,
                        template="plotly_dark", paper_bgcolor="#0A0E14", plot_bgcolor="#12161F",
                        font=dict(family="JetBrains Mono, monospace", color="#E8E6E1"),
                    )
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
 


