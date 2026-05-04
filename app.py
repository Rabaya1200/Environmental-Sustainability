import streamlit as st
import google.generativeai as genai # Using the stable library
from PIL import Image

st.set_page_config(page_title="Eco-Scanner AI", page_icon="🌍")
st.title("🌍 Environmental Sustainability Assistant")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please add your API key to Streamlit Secrets!")
else:
    # 1. Using the classic, stable library configuration
    genai.configure(api_key=api_key)

    uploaded_file = st.file_uploader("Upload waste/plant photo...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Analyzing...", use_container_width=True)

        if st.button("Analyze Eco-Impact"):
            with st.spinner("Scientist is thinking..."):
                try:
                    # 2. Using the most stable model ID for May 2026
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    response = model.generate_content([
                        "Identify this object and provide professional recycling/eco-advice.", 
                        img
                    ])
                    
                    st.success("### AI Sustainability Report")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
