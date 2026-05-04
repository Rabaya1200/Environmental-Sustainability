import streamlit as st
from google import genai
from google.genai import types  # <--- Added this to handle options
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Eco-Scanner AI", page_icon="🌍")
st.title("🌍 Sustainability Assistant")

# 2. Key Management
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please add your API key to Streamlit Secrets!")
else:
    # --- EXPERT REPAIR START ---
    # We use types.HttpOptions to force 'v1'. 
    # This fixes the 'v1beta' 404 error in your screenshot.
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(api_version='v1')
    )
    # --- EXPERT REPAIR END ---

    uploaded_file = st.file_uploader("Upload waste/plant photo...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Analyzing...", use_container_width=True)

        if st.button("Analyze Eco-Impact"):
            with st.spinner("Scientist is thinking..."):
                try:
                    # Model name is exactly gemini-3.1-flash
                    response = client.models.generate_content(
                        model="gemini-3.1-flash",
                        contents=["Explain how to recycle this object and its eco-impact.", img]
                    )
                    st.success("### AI Sustainability Report")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Technical Error: {e}")
