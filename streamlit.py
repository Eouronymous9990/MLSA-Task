import cv2
import streamlit as st
import numpy as np
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from moviepy.editor import ImageSequenceClip
import base64
def add_bg_from_local(path_to_image):
    with open(path_to_image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# تشغيل الدالة لإضافة الخلفية من ملف محلي
path ="bg.jpg"

add_bg_from_local(path)

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frames = []

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)

        self.frames.append(img)
        return img

    def getimg(self):
        return self.frames

def run():

    st.title("Face Detection with haarcascade")


    if st.button("Save Video"):
        if len(VideoTransformer.getimg()) > 0:
            clip = ImageSequenceClip(VideoTransformer.getimg(), fps=30)
            filename = st.text_input("Enter filename (default: output.mp4):", "output.mp4")
            clip.write_videofile(filename)
            st.success("Video saved successfully!")
        else:
            st.warning("No frames captured yet.")

    webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

# Download the face cascade classifier (replace with your path)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default(2).xml")

if __name__ == '__main__':
    run()
