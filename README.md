# 🛡️ Silent Risk Map AI
**A Multimodal Real-Time Security Engine** *Official Submission for AMD Slingshot 2026*

## 🌟 Project Overview
Silent Risk AI is a proactive safety solution that transforms standard surveillance into an intelligent emergency responder. By integrating **Computer Vision**, **Audio NLP**, and **Live Geolocation**, the system autonomously identifies threats and dispatches verified evidence to authorities in under 2 seconds.

## 🚀 AMD Optimization & Tech Stack
This system is engineered to leverage the high-performance capabilities of the **AMD ROCm™** software stack, ensuring low-latency processing for life-saving applications.

* **Visual Intelligence:** YOLOv8 (Nano) for real-time weapon and isolation detection.
* **Acoustic Intelligence:** Speech-to-Text engine monitoring for "Help" distress triggers.
* **Geospatial Tracking:** Live GPS coordinate injection for precise emergency dispatch.
* **Infrastructure:** Optimized for **AMD Ryzen™** and **EPYC™** processors to handle parallel AI workloads.



---

## ✨ Key Features
* **Multimodal Threat Detection:** Simultaneously identifies physical threats (weapons) and verbal distress calls.
* **Environmental Risk Scoring:** Calculates safety levels based on darkness (luminosity) and isolation (pedestrian count).
* **Autonomous Evidence Chain:** Automatically captures a timestamped photo and dispatches an SMTP email with a Google Maps link to security.
* **Evidence Gallery:** In-app archive for immediate forensic review of all triggered alerts.

---

## 🛠️ Installation & Setup

### 1. System Requirements
Ensure you have the **PortAudio** development headers installed on your machine to support microphone input.
* **Mac:** `brew install portaudio`
* **Linux:** `sudo apt-get install portaudio19-dev`

### 2. Clone and Install
```bash
git clone [https://github.com/your-username/Silent-Risk-AI.git](https://github.com/your-username/Silent-Risk-AI.git)
cd Silent-Risk-AI
pip install -r requirements.txt
