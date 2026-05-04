import streamlit as st
from google import genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Eco-Scanner AI", page_icon="🌍")
st.title("🌍 Environmental Sustainability Assistant")

# 2. Get API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please add your API key to the Streamlit Secrets dashboard!")
else:
    # --- CRITICAL FIX START ---
    # We force the client to use the stable 'v1' API version 
    # This stops the 'v1beta' 404 error you saw in your screenshot.
    client = genai.Client(
        api_key=api_key,
        http_options={'api_version': 'v1'}
    )
    # --- CRITICAL FIX END ---

    uploaded_file = st.file_uploader("Upload an image for analysis...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Analyzing this object...", use_container_width=True)

        if st.button("Analyze Eco-Impact"):
            with st.spinner("Scientist is working..."):
                try:
                    # Explicitly using the Gemini 3.1 Flash model
                    response = client.models.generate_content(
                        model="gemini-3.1-flash",
                        contents=["What is this object and how do I recycle it correctly?", img]
                    )
                    st.success("### AI Sustainability Report")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
