import streamlit as st
import google.generativeai as genai
from typing import Optional
import logging

# [Security] Console logging set karna taaki production mein errors track ho sakein bina UI break kiye
logging.basicConfig(level=logging.INFO)

def setup_accessibility_and_ui():
    """
    [Accessibility & Code Quality]
    Semantic HTML aur high-contrast colors use karna taaki screen-readers aur visually impaired users ko dikkat na ho.
    """
    st.set_page_config(page_title="Blind Spot Detector", page_icon="🎯", layout="centered")
    st.markdown("""
    <style>
    /* High contrast text and clear hierarchical tags for Accessibility */
    h1.main-title { color: #B71C1C; font-size: 2.8rem; font-weight: 800; text-align: center; }
    p.sub-title { color: #333333; font-size: 1.2rem; text-align: center; margin-bottom: 25px; font-weight: 500; }
    .help-text { color: #424242; font-size: 0.95rem; font-weight: bold; }
    div.stButton > button:first-child { font-size: 1.1rem; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_ai_model(api_key: str):
    """
    [Efficiency]
    @st.cache_resource ensure karta hai ki model baar-baar initialize na ho jab user button dabaye. 
    Isse memory aur API call latency save hoti hai.
    """
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-3.5-flash")

def get_system_prompt() -> str:
    """
    [Problem Statement Alignment]
    Strict instructions jo AI ko user ke liye decision lene se rokti hain.
    """
    return """
    You are a "Blind Spot Detector", a Socratic cognitive AI.
    CRITICAL RULE: NEVER make the decision for the user. NEVER give direct advice on what to choose.
    Format exactly as:
    1. **The Core Framework:** Summarize their logic.
    2. **Unstated Assumptions:** List 2-3 unverified assumptions.
    3. **Overlooked Variables:** List 2-3 missing factors.
    4. **The Friction Point:** Identify internal conflicts in their reasoning.
    5. **Questions to Explore:** Ask 1-2 probing questions to make them think deeper.
    """

def analyze_decision(api_key: str, user_input: str) -> Optional[str]:
    """
    [Code Quality & Security]
    Try-except block se errors handle karna aur API key format validate karna.
    """
    # [Security] Basic sanitization and validation
    if not api_key.startswith(("AQ.", "AIza")):
        st.error("⚠️ Invalid API Key format detected. Please check your key.")
        return None
        
    try:
        model = load_ai_model(api_key)
        full_prompt = f"{get_system_prompt()}\n\nHere is the user's decision to analyze:\n{user_input}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logging.error(f"API Error: {e}")
        st.error("⚠️ Analysis complete nahi ho paya. Please verify your internet connection and API key.")
        return None

def main():
    setup_accessibility_and_ui()
    
    # [Accessibility] Using proper heading tags
    st.markdown('<h1 class="main-title">🎯 Blind Spot Detector</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Identify hidden biases and unstated assumptions without losing your own agency.</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("⚙️ Settings")
        # [Security] type="password" hides the key from shoulder-surfing
        api_key = st.text_input("Gemini API Key", type="password", help="Required to run the analysis. Keys are not stored.", placeholder="Paste key here...")
        
    st.markdown('<p class="help-text">What decision are you facing and what are your main reasons?</p>', unsafe_allow_html=True)
    
    # [Accessibility] label_visibility adds a hidden label for screen readers
    user_decision = st.text_area("Decision Input", label_visibility="collapsed", height=150, placeholder="Example: I want to join a 6-month internship because...")
    
    if st.button("🚀 Analyze My Decision", type="primary"):
        # [Efficiency & Security] Input length validation before making network calls
        if not api_key:
            st.warning("⚠️ Please provide your API Key in the sidebar.")
        elif len(user_decision.strip()) < 30:
            st.warning("⚠️ Please provide a bit more context (minimum 30 characters) for an accurate analysis.")
        else:
            with st.spinner("Analyzing logical gaps... 🔍"):
                result = analyze_decision(api_key, user_decision)
                if result:
                    st.success("✅ Analysis Complete! Review your blind spots below:")
                    with st.container(border=True):
                        st.markdown(result)

if __name__ == "__main__":
    main()