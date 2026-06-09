import streamlit as st
import google.generativeai as genai

# Page setup for maximum senior readability
st.set_page_config(page_title="Abbu's Smart Market Guide", layout="centered")

st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 22px !important; /* Slightly larger text for easier reading */
    }
    .stButton>button {
        width: 100%;
        font-size: 22px !important;
        padding: 12px;
        background-color: #1e3d59;
        color: white;
        border-radius: 8px;
    }
    .disclaimer {
        background-color: #fff3cd;
        padding: 18px;
        border-radius: 8px;
        color: #856404;
        font-weight: bold;
        margin-bottom: 25px;
        border-right: 6px solid #ffc107;
    }
    .urdu-box {
        text-align: right; 
        direction: rtl; 
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 8px; 
        border-right: 5px solid #17a2b8;
        line-height: 1.8;
    }
    </style>
""", unsafe_allow_html=True)

# Configure AI Key
import streamlit as st
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"].replace("\n", "").strip()

# Permanent Urdu Disclaimer Visible on Top
st.markdown("""
<div class="disclaimer" style="text-align: right; direction: rtl;">
⚠️ <b>اہم انتباہ (Disclaimer):</b> یہ ایپ صرف تعلیمی اور معلوماتی مقاصد کے لیے ہے۔ سرمایہ کاری کا کوئی بھی فیصلہ کرنے سے پہلے اپنے فنانشل ایڈوائزر سے مشورہ کریں۔ مارکیٹ میں کسی قسم کے 'پیسے ڈبل یا ٹرپل' کرنے کی گارنٹی نہیں ہوتی اور تیز رفتار منافع کے پیچھے ہمیشہ بڑا نقصان کا خطرہ ہوتا ہے۔ آخری فیصلہ صرف آپ کا ہوگا۔
</div>
""", unsafe_allow_html=True)
# Abu's Direct Gemini Shortcut Button
st.link_button(
"گوگل جیمنی چیٹ کھولیں 🤖", 
"https://gemini.google.com/app?prompt=" + 
"آپ کا نام 'ابو کا مارکیٹ گائیڈ' ہے۔ آپ ایک انتہائی مؤدب، مخلص اور ماہر مالیاتی ساتھی ہیں۔ آپ ہمیشہ خالص، سادہ اور آسان اردو میں جواب دیں گے تاکہ پاکستان اور بین الاقوامی مارکیٹ کو آسانی سے سمجھا جا سکے۔ ہمیشہ یاد رکھیں کہ آپ ایک بزرگ پاکستانی والد سے گفتگو کر رہے ہیں۔ جوابات میں لائن بریکس استعمال کریں تاکہ پڑھنے میں آسانی ہو۔"
)

# Enhanced Brain: Guides the AI on exactly how to behave, what platforms to suggest, and how to stay safe
SYSTEM_PROMPT = """
You are a warm, deeply respectful, and expert financial companion for a 70+ year old Pakistani father. 
- Respond EXCLUSIVELY in warm, respectful Pakistani Urdu (using 'Aap', 'Ji', 'Tashreef rakhiye' tone). Keep sentences clear, short, and use large line breaks.
- If he asks about doubling or tripling money quickly, explain gently in Urdu that fast-paced wealth generation typically involves high-risk margin trading or speculative options, which can completely wipe out retirement life-savings. Advocate for safe compounding, capital protection, and steady dividend-paying investments.
- When explaining international investing from Pakistan, explicitly list legal and secure avenues: State Bank of Pakistan approved outward remittances, Roshan Digital Accounts (RDA) for overseas connections, or Asset Management Companies (AMCs) in Pakistan that offer Shariah-compliant or conventional Global Commodity/Equity Funds. Warn against illegal offshore trading apps.
- For local investing, guide him toward the Pakistan Stock Exchange (PSX), emphasizing blue-chip companies with strong dividend yields (e.g., energy, materials, top-tier tech leaders).
- Always terminate every answer with this exact string: 'یہ مارکیٹ کا ایک معلوماتی جائزہ ہے، لیکن سارا اختیار اور آخری فیصلہ مستقل طور پر آپ کا اپنا ہے۔'
"""

# Layout Option 1: Fast Tap Actions
st.write("### ⚡ کسی ایک سوال پر کلک کریں:")
col1, col2 = st.columns(2)

selected_query = ""
with col1:
    if st.button("🇵🇰 پاکستان میں قانونی انویسٹمنٹ کیسے شروع کریں؟"):
        selected_query = "پاکستان سے انٹرنیشنل مارکیٹ، سونے (Gold) اور مقامی اسٹاک مارکیٹ (PSX) میں قانونی طریقے سے انویسٹمنٹ شروع کرنے کا طریقہ کار کیا ہے؟"
    if st.button("💰 کم وقت بمقابلہ طویل مدت کا منافع"):
        selected_query = "شارٹ ٹرم (Short-term) اور لانگ ٹرم (Long-term) انویسٹمنٹ میں کیا فرق ہے، اور میری عمر (70+) کے لحاظ سے محفوظ طریقہ کون سا ہے؟"

with col2:
    if st.button("📉 مارکیٹ کے خطرات اور پیسے ڈبل کرنے کی حقیقت"):
        selected_query = "مارکیٹ میں 'پیسے ڈبل یا ٹرپل' کرنے کے دعووں کی حقیقت کیا ہے؟ مجھے اپنے سرمائے کو نقصان سے کیسے بچانا چاہیے؟"
    if st.button("🌟 سونے (Gold) میں انویسٹ کرنے کا طریقہ"):
        selected_query = "انٹرنیشنل مارکیٹ میں سونا خریدنے کے کون سے طریقے محفوظ ہیں اور کیا پاکستان مرکنٹائل ایکسچینج (PMEX) ایک اچھا ذریعہ ہے؟"

# Layout Option 2: Custom input text area
st.write("---")
custom_query = st.text_input("✍️ یا یہاں اپنا کوئی سوال اردو یا انگریزی میں ٹائپ کریں:")

final_query = custom_query if custom_query else selected_query

if st.button("اسسٹنٹ سے پوچھیں 🚀") and final_query:
    with st.spinner("مارکیٹ کا گہرا تجزیہ جاری ہے..."):
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
            response = model.generate_content(final_query)
            
            st.markdown(f"""
            <div class="urdu-box">
            {response.text}
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error("سسٹم عارضی طور پر جواب دینے سے قاصر ہے۔ براہ کرم انٹرنیٹ یا API کیلیے چیک کریں۔")

# HARDCODED EDUCATION HUB (Section 3)
st.write("---")
st.write("### 🎙️ ابّو کا لرننگ ہب (Recommended Podcasts & Channels)")
st.write("مارکیٹ کو گہرائی سے اور آسان زبان میں سمجھنے کے لیے نیچے دیے گئے معتبر لنکس پر کلک کریں:")

col_pod1, col_pod2 = st.columns(2)
with col_pod1:
    st.markdown("🔗 **Sarmaaya (Laeeq Ahmad)**\n\n*پاکستان اسٹاک مارکیٹ، میوچل فنڈز اور بنیادی فنانشل فہم کے لیے بہترین اردو گائیڈ اور معلوماتی لائیو سیشنز۔*")
with col_pod2:
    st.markdown("🔗 **Thought Behind Things (Muzamil Hasan)**\n\n*پاکستانی معیشت، کاروبار، اور فنانس کے وسیع تر رجحانات کو سادہ زبان میں سمجھنے کے لیے بہترین پوڈ کاسٹ۔*")
