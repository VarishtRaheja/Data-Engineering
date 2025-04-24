import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
buf = BytesIO()
img = Image.open("Tesla.jpg")
img.save(buf, format="JPEG")
byte_im = buf.getvalue()
btn = st.download_button(label="Download Image",data=byte_im,file_name="imagename.jpg",mime="image/jpeg")