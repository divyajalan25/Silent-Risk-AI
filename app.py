import streamlit as st
import cv2
import numpy as np
import speech_recognition as sr
import smtplib
import os
import time
from email.message import EmailMessage
from logic import get_risk_metrics
from datetime import datetime
from streamlit_geolocation import streamlit_geolocation
from PIL import Image

# --- CONFIG & SESSION STATE ---
st.set_page_config(page_title="Silent Risk AI | AMD Slingshot", layout="wide")
if 'run_system' not in st.session_state:
    st.session_state.run_system = False

# --- 📧 GMAIL SMTP CONFIGURATION ---
SENDER_EMAIL = "divyajalandj13@gmail.com" # Your Gmail
SENDER_PASS = "vodgcbakcizrwbdr"   # Your 16-char App Password
RECEIVER_EMAIL = "gardenrajori3@gmail.com"

def send_alert_email(img_path, lat, lon, timestamp):
    msg = EmailMessage()
    msg['Subject'] = f"🚨 PROACTIVE THREAT ALERT: {timestamp}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    
    # Include GPS data in the body
    maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat else "Unavailable"
    content = f"""
    Emergency Triggered!
    Time: {timestamp}
    Coordinates: {lat}, {lon}
    Google Maps: {maps_link}
    
    See attached evidence captured by Silent Risk AI.
    """
    msg.set_content(content)

    # Attach the evidence image
    with open(img_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename="evidence.jpg")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Mail Error: {e}")
        return False

# --- UI LAYOUT ---
st.title("🛡️ Silent Risk Map AI: Emergency Response")
location = streamlit_geolocation()
lat, lon = location.get('latitude'), location.get('longitude')

col1, col2 = st.sidebar.columns(2)
if col1.button("▶️ START SYSTEM"): st.session_state.run_system = True
if col2.button("⏹️ STOP SYSTEM"): 
    st.session_state.run_system = False
    st.rerun()

# --- MONITORING LOOP ---
if st.session_state.run_system:
    cap = cv2.VideoCapture(0)
    frame_spot = st.empty()
    r = sr.Recognizer()
    
    while st.session_state.run_system:
        ret, frame = cap.read()
        if not ret: break
        
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        data = get_risk_metrics(img_rgb)
        
        # Audio "Help" Trigger
        help_heard = False
        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=0.1, phrase_time_limit=1)
                if "help" in r.recognize_google(audio).lower(): 
                    help_heard = True
        except: pass

        # Emergency Action Logic
        if data['threat_detected'] or help_heard:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            path = f"evidence/alert_{int(time.time())}.jpg"
            if not os.path.exists('evidence'): os.makedirs('evidence')
            
            # Save and Dispatch
            cv2.imwrite(path, cv2.cvtColor(data['image'], cv2.COLOR_RGB2BGR))
            success = send_alert_email(path, lat, lon, ts)
            
            if success: st.toast("📧 Security Email Dispatched with GPS!")
            st.error("🚨 THREAT DETECTED - ALERT SENT")

        frame_spot.image(data['image'], channels="RGB")
    cap.release()
