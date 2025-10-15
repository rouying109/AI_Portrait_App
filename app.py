import streamlit as st
import replicate
import os
from dotenv import load_dotenv
from PIL import Image
import base64
import requests
from io import BytesIO

# 载入 API Key
load_dotenv()
replicate_api = os.getenv("REPLICATE_API_TOKEN")

st.set_page_config(page_title="AI Portrait Studio", page_icon="🎨", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #ff69b4;'>🎨 AI Portrait Studio</h1>
    <p style='text-align: center; font-size:18px;'>上传一张照片，让 AI 帮你变换风格、服装与氛围 ✨</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("上传一张照片（jpg / png）", type=["jpg", "jpeg", "png"])

style = st.selectbox(
    "选择风格：",
    ["韩系写真风", "日系制服风", "古风汉服", "西方油画风", "街拍模特风"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="你上传的照片", use_container_width=True)

    if st.button("✨ 生成 AI 写真"):
        with st.spinner("AI 正在生成中，请稍候..."):
            output = replicate.run(
                "lucataco/instantid:1a0cc3b3cbba693babe4cc37da58aa3c7950de22b8e7b60a4fa3d9de11cd6226",
                input={
                    "image": uploaded_file,
                    "prompt": f"{style}, portrait, professional lighting, studio background"
                }
            )

        result_url = output[0]
        st.success("✅ 完成！这是你的 AI 写真：")
        st.image(result_url, use_container_width=True)

        # 下载按钮
        response = requests.get(result_url)
        img_bytes = BytesIO(response.content)
        b64 = base64.b64encode(img_bytes.getvalue()).decode()
        href = f'<a href="data:file/jpg;base64,{b64}" download="AI_Portrait.jpg">📸 下载你的 AI 写真</a>'
        st.markdown(href, unsafe_allow_html=True)
