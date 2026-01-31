import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="FactoVerse Pro Resizer", layout="centered")

st.title("FactoVerse Ultra Stretch Resizer")
st.write("This tool will STRETCH your images to fill 1280x720 perfectly.")

uploaded_files = st.file_uploader("Choose Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    uploaded_files.sort(key=lambda x: x.name)
    st.success(f"{len(uploaded_files)} images uploaded.")
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for uploaded_file in uploaded_files:
            img = Image.open(uploaded_file)
            img = img.convert("RGB")
            
            # یہاں ہم زبردستی 1280x720 پر پھیلا رہے ہیں (No matter what)
            # Resize method: .resize instead of .thumbnail
            stretched_img = img.resize((1280, 720), Image.Resampling.LANCZOS)
            
            img_byte_arr = io.BytesIO()
            stretched_img.save(img_byte_arr, format='JPEG', quality=100) # Full Quality
            zip_file.writestr(uploaded_file.name, img_byte_arr.getvalue())

    st.download_button(
        label="Download Stretched Images (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="FactoVerse_Stretched.zip",
        mime="application/zip"
    )
