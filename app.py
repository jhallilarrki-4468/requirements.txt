import streamlit as st
from PIL import Image
import io
import zipfile

# Page Config
st.set_page_config(page_title="FactoVerse Pro Resizer", layout="centered")

st.title("FactoVerse Image Resizer (16:9)")
st.write("Upload your images to fit them into 1280x720 canvas without cropping.")

# File Uploader with Multiple Selection
uploaded_files = st.file_uploader("Choose Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    # Sorting files by name to maintain order
    uploaded_files.sort(key=lambda x: x.name)
    
    st.success(f"{len(uploaded_files)} images uploaded successfully.")
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for uploaded_file in uploaded_files:
            # Open image
            img = Image.open(uploaded_file)
            img = img.convert("RGB")
            
            # Create 16:9 Canvas (1280x720) - Black Background
            target_width, target_height = 1280, 720
            canvas = Image.new("RGB", (target_width, target_height), (0, 0, 0))
            
            # Resize image maintaining Aspect Ratio (Thumbnail method)
            img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Center the image on the canvas
            offset = ((target_width - img.width) // 2, (target_height - img.height) // 2)
            canvas.paste(img, offset)
            
            # Save to Zip
            img_byte_arr = io.BytesIO()
            canvas.save(img_byte_arr, format='JPEG', quality=95)
            zip_file.writestr(uploaded_file.name, img_byte_arr.getvalue())

    # Single Download Button for all images
    st.download_button(
        label="Download All Resized Images (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="FactoVerse_Resized_Images.zip",
        mime="application/zip"
    )
