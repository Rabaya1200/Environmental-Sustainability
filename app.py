import streamlit as st
from google import genai
from PIL import Image
import os

# 1. Page Configuration
st.set_page_config(page_title="Eco-Scanner AI", page_icon="🌍")
st.title("🌍 Environmental Sustainability Assistant")
st.write("Upload a photo of waste or a plant to learn how to help the planet.")

# 2. Secure API Connection
# We get the key from Streamlit's secret storage
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")
else:
    # Initialize the new 2026 Google GenAI Client
    client = genai.Client(api_key=api_key)

    uploaded_file = st.file_uploader("Capture or upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Target Image", use_container_width=True)

        if st.button("Analyze Eco-Impact"):
            with st.spinner("Consulting Gemini 3.1 Flash..."):
                try:
                    # Multi-modal prompt (Text + Image)
                    prompt = (
                        "You are an Environmental Scientist. Analyze this image and provide: "
                        "1. Identification of the object. "
                        "2. Sustainability advice (Recycling, composting, or care instructions). "
                        "3. A small tip to reduce carbon footprint related to this item."
                    )

                    response = client.models.generate_content(
                        model="gemini-3.1-flash",
                        contents=[prompt, img]
                    )

                    st.success("### AI Sustainability Report")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Analysis failed: {e}")