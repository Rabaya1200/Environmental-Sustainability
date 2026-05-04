import streamlit as st
from google import genai
from PIL import Image

# --- 1. SET UP THE PAGE ---
st.set_page_config(page_title="Eco-Scanner Assistant", page_icon="🌍")
st.title("🌍 Sustainability & Eco-Scanner AI")
st.write("Upload an image of an object to check its environmental impact and recycling potential.")

# --- 2. CONNECT TO THE API SECURELY ---
# We use st.secrets so your API key is never visible in the code
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
else:
    # We initialize the client using the stable V1 path to avoid 404 errors
    client = genai.Client(
        api_key=api_key,
        http_options={'api_version': 'v1'}
    )

    # --- 3. UI FOR IMAGE UPLOAD ---
    uploaded_file = st.file_uploader("Take a photo or upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Analyzed Object", use_container_width=True)

        # --- 4. THE AI INFERENCE ---
        if st.button("Analyze Eco-Impact"):
            with st.spinner("Scientist is analyzing..."):
                try:
                    # Expert Prompt for Sustainability
                    prompt = (
                        "Act as a professional Environmental Scientist. Analyze the image and provide:\n"
                        "1. Identification: What is this object?\n"
                        "2. Material: What is it made of?\n"
                        "3. Disposal: Is it recyclable, compostable, or landfill?\n"
                        "4. Eco-Tip: One way to reduce the footprint of this specific item."
                    )

                    # Calling Gemini 3.1 Flash (The fastest and smartest for 2026)
                    response = client.models.generate_content(
                        model="gemini-3.1-flash",
                        contents=[prompt, img]
                    )

                    st.success("### 📊 AI Sustainability Report")
                    st.markdown(response.text)
                
                except Exception as e:
                    st.error(f"Analysis failed. This is often a VPN or API path issue. Error: {e}")
