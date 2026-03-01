import streamlit as st
import cv2
import av
import numpy as np
import smtplib
from email.message import EmailMessage
from logic import get_risk_metrics
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from streamlit_geolocation import streamlit_geolocation
import time

st.set_page_config(page_title="Silent Risk AI | AMD Slingshot", layout="wide")

# --- SMTP CONFIG (Replace with your 16-char App Password) ---
SENDER_EMAIL = "divyajalandj13@gmail.com"
SENDER_PASS = "vodgcbakcizrwbdr" 
RECEIVER_EMAIL = "gardenrajori3@gmail.com"

# Prevent spamming 100 emails per second
if 'last_alert' not in st.session_state:
    st.session_state.last_alert = 0

def send_alert(img, lat, lon):
    msg = EmailMessage()
    msg['Subject'] = "🚨 CRITICAL THREAT DETECTED"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(f"Location: {lat}, {lon}\nMaps: http://google.com/maps?q={lat},{lon}")
    
    ret, buffer = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    msg.add_attachment(buffer.tobytes(), maintype='image', subtype='jpeg', filename="evidence.jpg")
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASS)
            smtp.send_message(msg)
        return True
    except: return False

# --- UI & GEOLOCATION ---
st.title("🛡️ Silent Risk Map AI")
location = streamlit_geolocation()
lat, lon = location.get('latitude'), location.get('longitude')

# --- VIDEO & AUDIO CALLBACK ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    data = get_risk_metrics(img)
    
    # Alert Logic with Cooldown
    if data['threat_detected'] and (time.time() - st.session_state.last_alert > 60):
        send_alert(data['raw_image'], lat, lon)
        st.session_state.last_alert = time.time()
        
    return av.VideoFrame.from_ndarray(data['image'], format="bgr24")

# --- WEB DEPLOYMENT STREAMER ---
webrtc_streamer(
    key="silent-risk-ai",
    mode=WebRtcMode.SENDRECV, # Sends video/audio and receives AI feed
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": True},
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)
