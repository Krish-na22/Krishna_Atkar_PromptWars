import streamlit as st
import google.generativeai as genai
import json

# ==========================================
# 1. PAGE CONFIG & PREMIUM CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Blind Spot Detector", page_icon="🧿", layout="centered")

st.markdown("""
<style>
    /* Gradient glowing Title */
    .main-title {
        background: -webkit-linear-gradient(45deg, #FF416C, #FF4B2B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #666666;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 35px;
    }
    /* Modern Input Area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #EEEEEE;
        font-size: 16px;
        padding: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.03);
    }
    /* Sleek Button */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        color: white;
        border-radius: 10px;
        height: 55px;
        font-size: 1.1rem;
        font-weight: bold;
        border: none;
        transition: 0.3s ease-in-out;
        box-shadow: 0px 5px 15px rgba(56, 239, 125, 0.4);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 20px rgba(56, 239, 125, 0.6);
    }
    /* Beautiful Colored Cards */
    .card {
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        color: #1A1A1A;
    }
    .card h3 { margin-top: 0px; font-size: 1.3rem; margin-bottom: 10px;}
    .card-blue { background-color: #F0F8FF; border-left: 6px solid #007BFF; }
    .card-yellow { background-color: #FFF9E6; border-left: 6px solid #FFC107; }
    .card-red { background-color: #FFEDED; border-left: 6px solid #DC3545; }
    .card-purple { background-color: #F8F0FF; border-left: 6px solid #6F42C1; }
    .card-green { background-color: #EAFBF1; border-left: 6px solid #28A745; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HIDDEN API KEY CONFIGURATION (Secure)
# ==========================================
try:
    # Ab API key UI se nahi, Streamlit Cloud ke backend se aayegi!
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ API Key missing! Streamlit Cloud ke 'Secrets' settings mein GEMINI_API_KEY daalo.")
    st.stop()

# ==========================================
# 3. ADVANCED JSON SYSTEM PROMPT
# ==========================================
system_prompt = """
You are a "Blind Spot Detector", a premium cognitive AI.
CRITICAL RULE: NEVER make the decision for the user. NEVER give direct advice.
You MUST respond ONLY in valid JSON format using this exact structure:
{
    "core_framework": "Summarize their logic in 1 sentence.",
    "unstated_assumptions": ["Assumption 1", "Assumption 2"],
    "overlooked_variables": ["Factor 1", "Factor 2"],
    "friction_point": "Point out the main internal conflict.",
    "questions_to_explore": ["Deep Question 1", "Deep Question 2"]
}
"""

# ==========================================
# 4. MAIN UI ELEMENTS
# ==========================================
st.markdown('<h1 class="main-title">🧿 Blind Spot Detector</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI-Powered Cognitive Mirror. Uncover what you missed.</p>', unsafe_allow_html=True)

user_decision = st.text_area(
    "🤔 What decision are you trying to make?",
    height=140,
    placeholder="E.g., I want to build my project on ESP32 instead of Arduino because of Wi-Fi, but I'm worried about the 3.3V logic..."
)

# ==========================================
# 5. GENERATION & BEAUTIFUL RENDERING
# ==========================================
if st.button("🚀 Reveal My Blind Spots", use_container_width=True):
    if len(user_decision) < 20:
        st.warning("⚠️ Please provide more detail about your decision.")
    else:
        with st.spinner("🧠 Scanning for logical gaps and cognitive biases..."):
            try:
                # Force AI to return pure JSON for perfect UI cards
                model = genai.GenerativeModel("gemini-3.5-flash")
                response = model.generate_content(
                    f"{system_prompt}\n\nUser Decision:\n{user_decision}",
                    generation_config=genai.GenerationConfig(response_mime_type="application/json")
                )
                
                # AI ka jawab JSON mein convert karna
                result = json.loads(response.text)
                
                st.balloons()
                st.markdown("<br><br><h2 style='text-align: center; color: #333;'>✨ Your Cognitive Analysis</h2><br>", unsafe_allow_html=True)
                
                # 1. Blue Card - Framework
                st.markdown(f'''
                <div class="card card-blue">
                    <h3 style="color: #007BFF;">🎯 Core Framework</h3>
                    <p>{result.get("core_framework", "")}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                # 2. Yellow Card - Assumptions
                assumptions = "".join([f"<li>{a}</li>" for a in result.get("unstated_assumptions", [])])
                st.markdown(f'''
                <div class="card card-yellow">
                    <h3 style="color: #FFC107;">👻 Unstated Assumptions</h3>
                    <ul>{assumptions}</ul>
                </div>
                ''', unsafe_allow_html=True)
                
                # 3. Red Card - Missing Variables
                variables = "".join([f"<li>{v}</li>" for v in result.get("overlooked_variables", [])])
                st.markdown(f'''
                <div class="card card-red">
                    <h3 style="color: #DC3545;">🔍 Overlooked Variables</h3>
                    <ul>{variables}</ul>
                </div>
                ''', unsafe_allow_html=True)
                
                # 4. Purple Card - Friction Point
                st.markdown(f'''
                <div class="card card-purple">
                    <h3 style="color: #6F42C1;">⚡ The Friction Point</h3>
                    <p>{result.get("friction_point", "")}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                # 5. Green Card - Socratic Questions
                questions = "".join([f"<li><strong>{q}</strong></li>" for q in result.get("questions_to_explore", [])])
                st.markdown(f'''
                <div class="card card-green">
                    <h3 style="color: #28A745;">🧭 Questions to Explore</h3>
                    <ul>{questions}</ul>
                </div>
                ''', unsafe_allow_html=True)
                
            except Exception as e:
                st.error("⚠️ Server error. Please try again later.")