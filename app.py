import streamlit as st
import cv2
import os
import smtplib
import av
from email.message import EmailMessage
from logic import get_risk_metrics
from datetime import datetime
from streamlit_webrtc import webrtc_streamer
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(page_title="Silent Risk AI | AMD Slingshot", layout="wide")

# --- SMTP CONFIG (Use your 16-char App Password) ---
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASS = "your-app-password-no-spaces" 
RECEIVER_EMAIL = "security-center@example.com"

def send_alert(img, lat, lon):
    msg = EmailMessage()
    msg['Subject'] = "🚨 EMERGENCY: Threat Detected"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(f"Location: {lat}, {lon}\nMaps: http://maps.google.com/?q={lat},{lon}")
    
    # Convert image for email
    ret, buffer = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    msg.add_attachment(buffer.tobytes(), maintype='image', subtype='jpeg', filename="evidence.jpg")
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASS)
            smtp.send_message(msg)
        return True
    except: return False

# --- UI & GPS ---
st.title("🛡️ Silent Risk Map AI")
location = streamlit_geolocation()
lat, lon = location.get('latitude'), location.get('longitude')

# --- WEBRTC VIDEO HANDLER ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="rgb24")
    data = get_risk_metrics(img)
    
    if data['threat_detected']:
        # Auto-dispatch email alert
        send_alert(data['raw_image'], lat, lon)
        
    return av.VideoFrame.from_ndarray(data['image'], format="rgb24")

webrtc_streamer(
    key="silent-risk-ai",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
