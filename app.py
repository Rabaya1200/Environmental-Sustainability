import streamlit as st
from google import genai
from google.genai import types 
from PIL import Image

st.set_page_config(page_title="Eco-Scanner AI", page_icon="🌍")
st.title("🌍 Sustainability Assistant")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please add your API key to Streamlit Secrets!")
else:
    # 1. We force the stable 'v1' version for the connection
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(api_version='v1')
    )

    uploaded_file = st.file_uploader("Upload waste/plant photo...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Analyzing...", use_container_width=True)

        if st.button("Analyze Eco-Impact"):
            with st.spinner("Scientist is thinking..."):
                try:
                    # 2. CRITICAL CHANGE: Use the PREVIEW ID for Gemini 3.1 Flash
                    # In May 2026, this is the required string for this model
                    response = client.models.generate_content(
                        model="gemini-3.1-flash-preview", 
                        contents=["Identify this and explain its eco-impact/recycling.", img]
                    )
                    st.success("### AI Sustainability Report")
                    st.write(response.text)
                except Exception as e:
                    # Helpful error for debugging
                    st.error(f"Technical Error: {e}")
