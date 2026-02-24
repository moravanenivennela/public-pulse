import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import base64
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "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")
ADMIN_PASSWORD = "admin123"

# ============================================
# TRANSLATIONS
# ============================================
TRANSLATIONS = {
    "English": {
        "submit_title": "📝 Submit a New Complaint",
        "select_language": "🌐 Select Your Language",
        "full_name": "👤 Full Name *",
        "phone": "📱 Phone Number *",
        "location": "📍 Location / Area *",
        "ward": "🏘️ Ward / Zone",
        "category": "📂 Problem Category *",
        "describe": "📝 Describe Your Problem *",
        "describe_placeholder": "Describe the issue in detail...",
        "upload_photo": "📸 Upload Photo (optional)",
        "ai_info": "🤖 AI will analyze, detect fake complaints, assign priority and auto-route to correct department",
        "submit_btn": "🚀 Submit Complaint",
        "fill_fields": "⚠️ Please fill all required fields marked with *",
        "track_title": "🔍 Track Your Complaint",
        "track_enter": "Enter Your Complaint ID",
        "track_example": "Example: PP-2024-001",
        "track_input": "🔍 Complaint ID",
        "track_btn": "Track Complaint",
        "track_found": "✅ Complaint Found!",
        "track_not_found": "❌ Complaint ID not found! Please check and try again.",
        "feedback_title": "💬 Share Your Feedback",
        "feedback_rate": "⭐ Rate Your Experience",
        "feedback_complaint_id": "🆔 Your Complaint ID",
        "feedback_service": "🏢 Department Service Quality",
        "feedback_comments": "📝 Your Comments",
        "feedback_recommend": "👥 Would you recommend Public Pulse?",
        "feedback_submit": "📤 Submit Feedback",
        "feedback_thanks": "🙏 Thank You for Your Feedback!",
        "admin_title": "🔐 Admin Login",
        "admin_portal": "🏛️ Admin Portal",
        "admin_subtitle": "Enter credentials to access dashboard",
        "admin_username": "👤 Username",
        "admin_password": "🔒 Password",
        "admin_login_btn": "🔐 Login",
        "admin_invalid": "❌ Invalid credentials. Try admin / admin123",
        "admin_success": "✅ Login successful! Welcome Admin!",
        "admin_logout": "🚪 Logout",
        "admin_logged_in": "✅ You are logged in as Admin!",
        "categories": ["Road & Potholes", "Water Supply", "Garbage & Sanitation", "Electricity", "Public Spaces & Parks"],
        "ratings": ["⭐⭐⭐⭐⭐ Excellent", "⭐⭐⭐⭐ Good", "⭐⭐⭐ Average", "⭐⭐ Poor", "⭐ Very Poor"],
        "service_ratings": ["Very Fast Response", "Fast Response", "Normal Response", "Slow Response", "No Response Yet"],
        "recommend_options": ["Yes, definitely!", "Yes, probably", "Not sure", "Probably not", "No"],
        "nav_submit": "🏠 Submit Complaint",
        "nav_track": "🔍 Track Complaint",
        "nav_ai": "🤖 AI Assistant",
        "nav_feedback": "💬 Feedback",
        "nav_qr": "📱 QR Code",
        "nav_admin": "🔐 Admin Login",
        "nav_satellite": "🗺️ Satellite Map",
        "nav_heatmap": "🌡️ Heatmap",
        "nav_predict": "🔮 Predictive Alerts",
        "nav_dashboard": "📊 Admin Dashboard",
        "nav_leaderboard": "🏅 Leaderboard",
        "sidebar_title": "🏛️ Public Pulse",
        "sidebar_sub": "AI-Powered Citizen Services",
        "sidebar_available": "Available 24/7 for you!",
        "sidebar_live": "📊 Live Stats",
        "about_title": "About Public Pulse",
        "about_desc": "Next-gen AI civic tech platform with satellite maps, fake detection & predictive intelligence.",
        "built_for": "Smart City AI Platform",
        "scan_title": "📱 Scan to Open App",
        "navigation": "Navigation",
        "header_sub": "AI-Powered Smart Citizen Services",
        "header_tags": ["🌐 Multilingual", "🔍 Fake Detector", "🗺️ Satellite Map", "🤖 Predictive AI"],
    },
    "Telugu": {
        "submit_title": "📝 కొత్త ఫిర్యాదు సమర్పించండి",
        "select_language": "🌐 మీ భాషను ఎంచుకోండి",
        "full_name": "👤 పూర్తి పేరు *",
        "phone": "📱 ఫోన్ నంబర్ *",
        "location": "📍 స్థానం / ప్రాంతం *",
        "ward": "🏘️ వార్డు / జోన్",
        "category": "📂 సమస్య వర్గం *",
        "describe": "📝 మీ సమస్యను వివరించండి *",
        "describe_placeholder": "సమస్యను వివరంగా వివరించండి...",
        "upload_photo": "📸 ఫోటో అప్లోడ్ చేయండి (ఐచ్ఛికం)",
        "ai_info": "🤖 AI మీ ఫిర్యాదును విశ్లేషిస్తుంది మరియు సంబంధిత విభాగానికి పంపిస్తుంది",
        "submit_btn": "🚀 ఫిర్యాదు సమర్పించండి",
        "fill_fields": "⚠️ * తో గుర్తించిన అన్ని అవసరమైన ఫీల్డ్‌లను పూరించండి",
        "track_title": "🔍 మీ ఫిర్యాదును ట్రాక్ చేయండి",
        "track_enter": "మీ ఫిర్యాదు ID నమోదు చేయండి",
        "track_example": "ఉదాహరణ: PP-2024-001",
        "track_input": "🔍 ఫిర్యాదు ID",
        "track_btn": "ఫిర్యాదు ట్రాక్ చేయండి",
        "track_found": "✅ ఫిర్యాదు కనుగొనబడింది!",
        "track_not_found": "❌ ఫిర్యాదు ID కనుగొనబడలేదు! దయచేసి మళ్ళీ ప్రయత్నించండి.",
        "feedback_title": "💬 మీ అభిప్రాయం తెలపండి",
        "feedback_rate": "⭐ మీ అనుభవాన్ని రేట్ చేయండి",
        "feedback_complaint_id": "🆔 మీ ఫిర్యాదు ID",
        "feedback_service": "🏢 విభాగ సేవా నాణ్యత",
        "feedback_comments": "📝 మీ వ్యాఖ్యలు",
        "feedback_recommend": "👥 మీరు Public Pulse ని సిఫారసు చేస్తారా?",
        "feedback_submit": "📤 అభిప్రాయం సమర్పించండి",
        "feedback_thanks": "🙏 మీ అభిప్రాయానికి ధన్యవాదాలు!",
        "admin_title": "🔐 అడ్మిన్ లాగిన్",
        "admin_portal": "🏛️ అడ్మిన్ పోర్టల్",
        "admin_subtitle": "డాష్‌బోర్డ్ యాక్సెస్ కోసం క్రెడెన్షియల్స్ నమోదు చేయండి",
        "admin_username": "👤 వినియోగదారు పేరు",
        "admin_password": "🔒 పాస్వర్డ్",
        "admin_login_btn": "🔐 లాగిన్",
        "admin_invalid": "❌ చెల్లని క్రెడెన్షియల్స్. admin / admin123 ప్రయత్నించండి",
        "admin_success": "✅ లాగిన్ విజయవంతమైంది! స్వాగతం అడ్మిన్!",
        "admin_logout": "🚪 లాగ్అవుట్",
        "admin_logged_in": "✅ మీరు అడ్మిన్‌గా లాగిన్ అయ్యారు!",
        "categories": ["రోడ్లు & గుంతలు", "నీటి సరఫరా", "చెత్త & పారిశుద్ధ్యం", "విద్యుత్", "పార్కులు & బహిరంగ స్థలాలు"],
        "ratings": ["⭐⭐⭐⭐⭐ అద్భుతం", "⭐⭐⭐⭐ మంచిది", "⭐⭐⭐ సాధారణం", "⭐⭐ పేద", "⭐ చాలా పేద"],
        "service_ratings": ["చాలా వేగంగా స్పందించారు", "వేగంగా స్పందించారు", "సాధారణ స్పందన", "నెమ్మదిగా స్పందించారు", "ఇంకా స్పందన లేదు"],
        "recommend_options": ["అవును, తప్పకుండా!", "అవును, బహుశా", "ఖచ్చితంగా తెలియదు", "బహుశా కాదు", "కాదు"],
        "nav_submit": "🏠 ఫిర్యాదు సమర్పించండి",
        "nav_track": "🔍 ఫిర్యాదు ట్రాక్ చేయండి",
        "nav_ai": "🤖 AI సహాయకుడు",
        "nav_feedback": "💬 అభిప్రాయం",
        "nav_qr": "📱 QR కోడ్",
        "nav_admin": "🔐 అడ్మిన్ లాగిన్",
        "nav_satellite": "🗺️ శాటిలైట్ మ్యాప్",
        "nav_heatmap": "🌡️ హీట్‌మ్యాప్",
        "nav_predict": "🔮 అంచనా హెచ్చరికలు",
        "nav_dashboard": "📊 అడ్మిన్ డాష్‌బోర్డ్",
        "nav_leaderboard": "🏅 లీడర్‌బోర్డ్",
        "sidebar_title": "🏛️ పబ్లిక్ పల్స్",
        "sidebar_sub": "AI పౌర సేవలు",
        "sidebar_available": "24/7 అందుబాటులో!",
        "sidebar_live": "📊 లైవ్ స్టాట్స్",
        "about_title": "పబ్లిక్ పల్స్ గురించి",
        "about_desc": "శాటిలైట్ మ్యాప్‌లు, నకిలీ గుర్తింపు & అంచనా మేధస్సుతో AI సివిక్ టెక్ ప్లాట్‌ఫారమ్.",
        "built_for": "స్మార్ట్ సిటీ AI ప్లాట్‌ఫారమ్",
        "scan_title": "📱 యాప్ తెరవడానికి స్కాన్ చేయండి",
        "navigation": "నావిగేషన్",
        "header_sub": "AI పౌర సేవలు",
        "header_tags": ["🌐 బహుభాషా", "🔍 నకిలీ గుర్తింపు", "🗺️ శాటిలైట్ మ్యాప్", "🤖 అంచనా AI"],
    },
    "Hindi": {
        "submit_title": "📝 नई शिकायत दर्ज करें",
        "select_language": "🌐 अपनी भाषा चुनें",
        "full_name": "👤 पूरा नाम *",
        "phone": "📱 फोन नंबर *",
        "location": "📍 स्थान / क्षेत्र *",
        "ward": "🏘️ वार्ड / ज़ोन",
        "category": "📂 समस्या की श्रेणी *",
        "describe": "📝 अपनी समस्या बताएं *",
        "describe_placeholder": "समस्या को विस्तार से बताएं...",
        "upload_photo": "📸 फोटो अपलोड करें (वैकल्पिक)",
        "ai_info": "🤖 AI आपकी शिकायत का विश्लेषण करेगा और सही विभाग को भेजेगा",
        "submit_btn": "🚀 शिकायत दर्ज करें",
        "fill_fields": "⚠️ कृपया * से चिह्नित सभी आवश्यक फ़ील्ड भरें",
        "track_title": "🔍 अपनी शिकायत ट्रैक करें",
        "track_enter": "अपनी शिकायत ID दर्ज करें",
        "track_example": "उदाहरण: PP-2024-001",
        "track_input": "🔍 शिकायत ID",
        "track_btn": "शिकायत ट्रैक करें",
        "track_found": "✅ शिकायत मिली!",
        "track_not_found": "❌ शिकायत ID नहीं मिली! कृपया दोबारा जांचें।",
        "feedback_title": "💬 अपनी प्रतिक्रिया दें",
        "feedback_rate": "⭐ अपना अनुभव रेट करें",
        "feedback_complaint_id": "🆔 आपकी शिकायत ID",
        "feedback_service": "🏢 विभाग सेवा गुणवत्ता",
        "feedback_comments": "📝 आपकी टिप्पणियां",
        "feedback_recommend": "👥 क्या आप Public Pulse की सिफारिश करेंगे?",
        "feedback_submit": "📤 प्रतिक्रिया सबमिट करें",
        "feedback_thanks": "🙏 आपकी प्रतिक्रिया के लिए धन्यवाद!",
        "admin_title": "🔐 एडमिन लॉगिन",
        "admin_portal": "🏛️ एडमिन पोर्टल",
        "admin_subtitle": "डैशबोर्ड एक्सेस के लिए क्रेडेंशियल दर्ज करें",
        "admin_username": "👤 उपयोगकर्ता नाम",
        "admin_password": "🔒 पासवर्ड",
        "admin_login_btn": "🔐 लॉगिन",
        "admin_invalid": "❌ अमान्य क्रेडेंशियल। admin / admin123 आज़माएं",
        "admin_success": "✅ लॉगिन सफल! स्वागत है एडमिन!",
        "admin_logout": "🚪 लॉगआउट",
        "admin_logged_in": "✅ आप एडमिन के रूप में लॉगिन हैं!",
        "categories": ["सड़क और गड्ढे", "जल आपूर्ति", "कचरा और स्वच्छता", "बिजली", "पार्क और सार्वजनिक स्थान"],
        "ratings": ["⭐⭐⭐⭐⭐ उत्कृष्ट", "⭐⭐⭐⭐ अच्छा", "⭐⭐⭐ औसत", "⭐⭐ खराब", "⭐ बहुत खराब"],
        "service_ratings": ["बहुत तेज़ प्रतिक्रिया", "तेज़ प्रतिक्रिया", "सामान्य प्रतिक्रिया", "धीमी प्रतिक्रिया", "अभी तक कोई प्रतिक्रिया नहीं"],
        "recommend_options": ["हां, बिल्कुल!", "हां, शायद", "निश्चित नहीं", "शायद नहीं", "नहीं"],
        "nav_submit": "🏠 शिकायत दर्ज करें",
        "nav_track": "🔍 शिकायत ट्रैक करें",
        "nav_ai": "🤖 AI सहायक",
        "nav_feedback": "💬 प्रतिक्रिया",
        "nav_qr": "📱 QR कोड",
        "nav_admin": "🔐 एडमिन लॉगिन",
        "nav_satellite": "🗺️ सैटेलाइट मैप",
        "nav_heatmap": "🌡️ हीटमैप",
        "nav_predict": "🔮 भविष्यवाणी अलर्ट",
        "nav_dashboard": "📊 एडमिन डैशबोर्ड",
        "nav_leaderboard": "🏅 लीडरबोर्ड",
        "sidebar_title": "🏛️ पब्लिक पल्स",
        "sidebar_sub": "AI नागरिक सेवाएं",
        "sidebar_available": "24/7 उपलब्ध!",
        "sidebar_live": "📊 लाइव स्टैट्स",
        "about_title": "पब्लिक पल्स के बारे में",
        "about_desc": "सैटेलाइट मैप्स, नकली पहचान और भविष्यवाणी के साथ AI सिविक प्लेटफॉर्म।",
        "built_for": "स्मार्ट सिटी AI प्लेटफॉर्म",
        "scan_title": "📱 ऐप खोलने के लिए स्कैन करें",
        "navigation": "नेविगेशन",
        "header_sub": "AI नागरिक सेवाएं",
        "header_tags": ["🌐 बहुभाषी", "🔍 नकली पहचान", "🗺️ सैटेलाइट मैप", "🤖 भविष्यवाणी AI"],
    }
}

st.set_page_config(
    page_title="Public Pulse | Smart Citizen Services",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
    .main .block-container { padding: 0.5rem 0.8rem !important; max-width: 100% !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    section[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e5e7eb !important; box-shadow: 2px 0 10px rgba(0,0,0,0.08) !important; }
    .app-header { background: linear-gradient(135deg, #1e3a8a, #2563eb); padding: 16px 20px; border-radius: 0 0 20px 20px; color: white; text-align: center; margin-bottom: 16px; box-shadow: 0 4px 20px rgba(37,99,235,0.3); }
    .metric-card { background: white; padding: 16px 12px; border-radius: 14px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.06); border-top: 3px solid #2563eb; margin-bottom: 8px; }
    .metric-number { font-size: 2rem !important; font-weight: 800; color: #1e3a8a; }
    .metric-label { font-size: 0.72rem; color: #64748b; margin-top: 3px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .complaint-card { background: white; padding: 16px; border-radius: 14px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); border-left: 4px solid #2563eb; color: #1e293b !important; }
    .complaint-card * { color: #1e293b !important; }
    .section-header { font-size: 1.1rem !important; font-weight: 700 !important; color: #000000 !important; margin-bottom: 14px !important; padding-bottom: 8px !important; border-bottom: 2px solid #2563eb !important; -webkit-text-fill-color: #000000 !important; }
    .stButton>button { background: linear-gradient(135deg, #1e3a8a, #2563eb) !important; color: #ffffff !important; border: none !important; border-radius: 12px !important; padding: 14px 20px !important; font-weight: 700 !important; font-size: 0.95rem !important; width: 100% !important; box-shadow: 0 4px 15px rgba(37,99,235,0.3) !important; }
    .stFormSubmitButton>button { background: linear-gradient(135deg, #1e3a8a, #2563eb) !important; color: white !important; border-radius: 12px !important; font-weight: 700 !important; padding: 14px !important; font-size: 1rem !important; }
    .stTextInput>div>div>input { border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important; background: #ffffff !important; color: #000000 !important; padding: 12px 14px !important; font-size: 0.95rem !important; caret-color: #000000 !important; }
    .stTextArea>div>div>textarea { border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important; background: #ffffff !important; color: #000000 !important; font-size: 0.95rem !important; }
    div[data-testid="stForm"] input { background: #ffffff !important; color: #000000 !important; }
    div[data-testid="stForm"] textarea { background: #ffffff !important; color: #000000 !important; }
    div[data-testid="stForm"] { background: #ffffff !important; padding: 20px !important; border-radius: 16px !important; border: 1px solid #f1f5f9 !important; box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important; }
    .stSelectbox [data-baseweb="select"] { background: #ffffff !important; border-radius: 10px !important; }
    .stSelectbox [data-baseweb="select"] * { background: #ffffff !important; color: #000000 !important; }
    .stSelectbox svg { fill: #2563eb !important; }
    [data-baseweb="popover"] * { background: #ffffff !important; color: #000000 !important; }
    [data-testid="stFileUploaderDropzone"] { background: #f8fafc !important; border: 2px dashed #2563eb !important; border-radius: 12px !important; }
    [data-testid="stFileUploaderDropzone"] * { color: #000000 !important; }
    [data-testid="stFileUploader"] * { color: #000000 !important; }
    [data-testid="stPasswordInput"] button { background: #ffffff !important; border: none !important; }
    [data-testid="stPasswordInput"] svg { fill: #2563eb !important; stroke: #2563eb !important; }
    .sidebar-stats { background: linear-gradient(135deg, #1e3a8a, #2563eb); padding: 16px; border-radius: 14px; color: white; margin-bottom: 16px; }
    .badge-high { background:#fee2e2; color:#dc2626 !important; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.78rem; border:1px solid #fecaca; }
    .badge-medium { background:#fef3c7; color:#d97706 !important; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.78rem; border:1px solid #fde68a; }
    .badge-low { background:#d1fae5; color:#059669 !important; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.78rem; border:1px solid #a7f3d0; }
    .fake-badge { background:#fce7f3; color:#be185d !important; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.78rem; border:1px solid #fbcfe8; }
    .success-card { background: linear-gradient(135deg, #d1fae5, #a7f3d0); padding: 24px 16px; border-radius: 16px; border: 1px solid #10b981; text-align: center; color: #1e293b !important; }
    .track-card { background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); color: #1e293b !important; }
    .track-card * { color: #1e293b !important; }
    .whatsapp-container { max-width: 340px; margin: 16px auto; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 30px rgba(0,0,0,0.15); }
    .whatsapp-header { background: #075e54; padding: 12px 16px; display: flex; align-items: center; gap: 10px; }
    .whatsapp-body { background: #e5ddd5; padding: 16px; }
    .whatsapp-bubble { background: #ffffff; border-radius: 0 12px 12px 12px; padding: 12px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); max-width: 300px; }
    .whatsapp-tick { text-align: right; color: #34b7f1; font-size: 0.7rem; margin-top: 6px; }
    .rank-card { background: white; border-radius: 14px; padding: 16px; margin-bottom: 10px; border: 1px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .predict-card { background: linear-gradient(135deg, #7c3aed, #a855f7); padding: 16px; border-radius: 14px; color: white; margin-bottom: 12px; }
    .fake-card { background: linear-gradient(135deg, #be185d, #ec4899); padding: 16px; border-radius: 14px; color: white; margin-bottom: 12px; }
    .stProgress > div > div { background: linear-gradient(90deg, #1e3a8a, #2563eb) !important; border-radius: 10px !important; }
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #2563eb; border-radius: 4px; }
    .stRadio label { color: #000000 !important; font-size: 0.9rem !important; font-weight: 500 !important; }
    label { color: #000000 !important; }
    p { color: #000000 !important; }
    .stMarkdown p { color: #000000 !important; }
    [data-testid="stMarkdownContainer"] p { color: #000000 !important; }
    [data-testid="stMarkdownContainer"] { color: #000000 !important; }
    div[data-testid="stForm"] label { color: #000000 !important; }
    .stSelectbox label { color: #000000 !important; }
    .stTextInput label { color: #000000 !important; }
    .stTextArea label { color: #000000 !important; }
    hr { border-color: #f1f5f9 !important; }
    .stAlert { border-radius: 12px !important; }
    @media (max-width: 768px) {
        .main .block-container { padding: 0.3rem 0.5rem !important; }
        .metric-number { font-size: 1.6rem !important; }
        .complaint-card { padding: 12px !important; }
        .section-header { font-size: 1rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if 'complaints' not in st.session_state:
    st.session_state.complaints = [
        {"id":"PP-2024-001","name":"Ravi Kumar","phone":"9876543210","location":"Maddilapalem, Visakhapatnam","ward":"Ward 5","category":"Road & Potholes","description":"Large pothole near school zone causing accidents daily","priority":"High","summary":"Dangerous pothole near school requiring urgent repair","department":"Roads & Infrastructure","status":"In Progress","date":"2024-02-20 09:15","image":None,"lat":17.7384,"lon":83.2184,"is_fake":False,"language":"English"},
        {"id":"PP-2024-002","name":"Priya Sharma","phone":"8765432109","location":"MVP Colony, Visakhapatnam","ward":"Ward 12","category":"Water Supply","description":"No water supply for 3 days in our area","priority":"High","summary":"Critical water supply disruption affecting entire colony","department":"Water & Sanitation Board","status":"Pending","date":"2024-02-20 11:30","image":None,"lat":17.7230,"lon":83.3012,"is_fake":False,"language":"English"},
        {"id":"PP-2024-003","name":"Suresh Babu","phone":"7654321098","location":"Gajuwaka, Visakhapatnam","ward":"Ward 8","category":"Garbage & Sanitation","description":"Garbage not collected for a week causing smell","priority":"Medium","summary":"Weekly garbage collection missed causing sanitation issues","department":"Sanitation Department","status":"Resolved","date":"2024-02-19 14:00","image":None,"lat":17.6868,"lon":83.2185,"is_fake":False,"language":"English"},
        {"id":"PP-2024-004","name":"Lakshmi Devi","phone":"6543210987","location":"Dwaraka Nagar, Visakhapatnam","ward":"Ward 3","category":"Electricity","description":"Street lights not working for 2 weeks","priority":"Medium","summary":"Street light outage creating safety concerns at night","department":"APEPDCL","status":"Pending","date":"2024-02-19 16:45","image":None,"lat":17.7340,"lon":83.3200,"is_fake":False,"language":"English"},
        {"id":"PP-2024-005","name":"Venkat Rao","phone":"5432109876","location":"Rushikonda, Visakhapatnam","ward":"Ward 15","category":"Public Spaces & Parks","description":"Park benches broken children getting hurt","priority":"Low","summary":"Broken park infrastructure needs maintenance","department":"Parks & Recreation","status":"Pending","date":"2024-02-18 10:00","image":None,"lat":17.7828,"lon":83.3677,"is_fake":False,"language":"English"},
        {"id":"PP-2024-006","name":"Anjali Reddy","phone":"9988776655","location":"MVP Colony, Visakhapatnam","ward":"Ward 12","category":"Water Supply","description":"Water is contaminated and smells bad. People are falling sick","priority":"High","summary":"Contaminated water supply causing health issues","department":"Water & Sanitation Board","status":"Pending","date":"2024-02-21 08:00","image":None,"lat":17.7250,"lon":83.3050,"is_fake":False,"language":"English"},
        {"id":"PP-2024-007","name":"Krishna Murthy","phone":"8877665544","location":"Maddilapalem, Visakhapatnam","ward":"Ward 5","category":"Road & Potholes","description":"Another pothole on the same road causing accidents","priority":"High","summary":"Multiple potholes in Maddilapalem area creating danger","department":"Roads & Infrastructure","status":"Pending","date":"2024-02-21 10:00","image":None,"lat":17.7390,"lon":83.2190,"is_fake":False,"language":"English"},
    ]

if 'complaint_counter' not in st.session_state:
    st.session_state.complaint_counter = 8
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'copilot_open' not in st.session_state:
    st.session_state.copilot_open = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role":"assistant","content":"👋 Hello! I am the Public Pulse AI Assistant. How can I help you today?"}]
if 'citizen_lang' not in st.session_state:
    st.session_state.citizen_lang = "English"
if 'admin_lang' not in st.session_state:
    st.session_state.admin_lang = "English"

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_marker_color(priority):
    return "red" if priority=="High" else "orange" if priority=="Medium" else "green"

def get_deadline_hours(priority):
    return 24 if priority=="High" else 72 if priority=="Medium" else 168

def get_time_remaining(date_str, priority):
    try:
        submitted = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        deadline = submitted + timedelta(hours=get_deadline_hours(priority))
        remaining = deadline - datetime.now()
        if remaining.total_seconds() <= 0:
            return "⚠️ OVERDUE", True
        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        return f"{hours}h {minutes}m remaining", False
    except:
        return "N/A", False

def translate_to_english(text, source_lang):
    try:
        if source_lang == "English":
            return text
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

def call_ai(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": 500}
        )
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"API Error: {data['error']['message']}"
        return f"Unexpected response: {str(data)}"
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_complaint(description, category):
    try:
        prompt = f"""You are a government complaint analysis AI.
        Category: {category}
        Description: {description}
        Respond ONLY with this JSON:
        {{"priority": "High or Medium or Low", "summary": "One line summary", "department": "Government department name", "is_fake": true or false, "fake_reason": "reason if fake else empty string"}}
        Priority: High=safety/health risk, Medium=inconvenience, Low=minor issue
        Fake: Mark fake if gibberish, vague, offensive, or not a real civic complaint."""
        result_text = call_ai(prompt)
        if "```" in result_text:
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
        return json.loads(result_text.strip())
    except:
        return {"priority": "Medium", "summary": "Complaint received and logged", "department": "General Administration", "is_fake": False, "fake_reason": ""}

def generate_prediction(complaints):
    try:
        summary = "\n".join([f"- {c['category']} at {c['location']} | Priority: {c['priority']} | Date: {c['date']}" for c in complaints])
        prompt = f"""You are a smart city AI analyst. Based on these civic complaint patterns:
        {summary}
        Generate exactly 3 predictions about which areas or issues are likely to worsen next week.
        Respond ONLY with a JSON array:
        [{{"area": "Area name", "issue": "Issue type", "risk": "High/Medium/Low", "reason": "One line reason"}}]"""
        result_text = call_ai(prompt)
        if "```" in result_text:
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
        return json.loads(result_text.strip())
    except:
        return [
            {"area": "MVP Colony", "issue": "Water Supply", "risk": "High", "reason": "Repeated water complaints in this area"},
            {"area": "Maddilapalem", "issue": "Road & Potholes", "risk": "High", "reason": "Multiple pothole reports detected"},
            {"area": "Gajuwaka", "issue": "Garbage & Sanitation", "risk": "Medium", "reason": "Sanitation complaints increasing"}
        ]

def ask_copilot(question):
    try:
        complaints = st.session_state.complaints
        total = len(complaints)
        high = len([c for c in complaints if c['priority'] == 'High'])
        resolved = len([c for c in complaints if c['status'] == 'Resolved'])
        pending = len([c for c in complaints if c['status'] == 'Pending'])
        complaint_details = "\n".join([f"ID:{c['id']} Category:{c['category']} Location:{c['location']} Priority:{c['priority']} Status:{c['status']}" for c in complaints])
        prompt = f"""You are Public Pulse AI Copilot for a citizen complaint management system.
        Stats: Total={total}, High={high}, Resolved={resolved}, Pending={pending}
        Complaints:\n{complaint_details}
        Answer ANY question. Be friendly and concise.
        User Question: {question}"""
        return call_ai(prompt)
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================
# GET CURRENT LANGUAGE
# ============================================
def get_lang():
    if st.session_state.admin_logged_in:
        return TRANSLATIONS[st.session_state.admin_lang]
    return TRANSLATIONS[st.session_state.citizen_lang]

# ============================================
# HEADER — rendered only once using placeholder
# ============================================
header_placeholder = st.empty()
SL = get_lang()
tags_html = "".join([f'<span style="background:rgba(255,255,255,0.15);color:white;padding:4px 10px;border-radius:20px;font-size:0.7rem;font-weight:600;">{t}</span>' for t in SL["header_tags"]])
header_placeholder.markdown(f"""
<div class="app-header">
    <div style="display:flex;align-items:center;justify-content:center;gap:12px;">
        <div style="background:rgba(255,255,255,0.2);width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;">🏛️</div>
        <div style="text-align:left;">
            <h1 style="color:white;margin:0;font-size:1.5rem;font-weight:800;">Public Pulse</h1>
            <p style="color:rgba(255,255,255,0.8);margin:0;font-size:0.72rem;">{SL["header_sub"]}</p>
        </div>
    </div>
    <div style="display:flex;justify-content:center;gap:8px;margin-top:12px;flex-wrap:wrap;">
        {tags_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# COPILOT BUTTON
# ============================================
col_space, col_btn = st.columns([6,1])
with col_btn:
    if st.button("🤖", help="Ask AI Copilot"):
        st.session_state.copilot_open = not st.session_state.copilot_open

if st.session_state.copilot_open:
    st.markdown("""
    <div style="background:white;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,0.2);margin-bottom:20px;overflow:hidden;">
        <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);padding:15px 20px;">
            <span style="color:white;font-weight:700;font-size:1rem;">🤖 Public Pulse Copilot</span><br>
            <span style="color:rgba(255,255,255,0.8);font-size:0.8rem;">Ask me anything!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    for chat in st.session_state.chat_history[-4:]:
        if 'user' in chat:
            st.markdown(f"**🧑 You:** {chat['user']}")
            st.markdown(f"**🤖 Copilot:** {chat['bot']}")
            st.markdown("---")
    user_question = st.text_input("💬 Ask Copilot...", placeholder="How many complaints are pending?", key="copilot_input")
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("Send ➤", key="copilot_send"):
            if user_question:
                with st.spinner("🤖 Thinking..."):
                    answer = ask_copilot(user_question)
                st.session_state.chat_history.append({"user": user_question, "bot": answer})
                st.rerun()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    complaints_all = st.session_state.complaints
    total_s = len(complaints_all)
    high_s = len([c for c in complaints_all if c['priority'] == 'High'])
    resolved_s = len([c for c in complaints_all if c['status'] == 'Resolved'])
    fake_s = len([c for c in complaints_all if c.get('is_fake', False)])

    # Get language for sidebar
    SL = get_lang()

    if st.session_state.admin_logged_in:
        st.markdown(f"""
        <div class="sidebar-stats">
            <h3 style="margin:0;color:white;">{SL["sidebar_live"]}</h3>
            <hr style="border-color:rgba(255,255,255,0.3);">
            <p style="margin:5px 0;color:white;">📋 Total: <strong>{total_s}</strong></p>
            <p style="margin:5px 0;color:white;">🔴 High: <strong>{high_s}</strong></p>
            <p style="margin:5px 0;color:white;">✅ Resolved: <strong>{resolved_s}</strong></p>
            <p style="margin:5px 0;color:white;">🚫 Fake: <strong>{fake_s}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="sidebar-stats">
            <h3 style="margin:0;color:white;">{SL["sidebar_title"]}</h3>
            <hr style="border-color:rgba(255,255,255,0.3);">
            <p style="margin:5px 0;color:white;opacity:0.9;">{SL["sidebar_sub"]}</p>
            <p style="margin:5px 0;color:white;opacity:0.9;">{SL["sidebar_available"]}</p>
        </div>
        """, unsafe_allow_html=True)

    # NAVIGATION based on login status and language
    if st.session_state.admin_logged_in:
        nav_options = [
            SL["nav_track"],
            SL["nav_ai"],
            SL["nav_qr"],
            SL["nav_satellite"],
            SL["nav_heatmap"],
            SL["nav_predict"],
            SL["nav_dashboard"],
            SL["nav_leaderboard"],
            SL["nav_admin"],
        ]
    else:
        nav_options = [
            SL["nav_submit"],
            SL["nav_track"],
            SL["nav_ai"],
            SL["nav_feedback"],
            SL["nav_qr"],
            SL["nav_admin"],
        ]

    page = st.radio(SL["navigation"], nav_options)

    st.markdown("---")
    st.markdown(f"**{SL['about_title']}**")
    st.markdown(SL["about_desc"])
    st.markdown(f"**{SL['built_for']}**")
    st.markdown("---")
    st.markdown(f"**{SL['scan_title']}**")
    try:
        st.image("public_pulse_qr.png", width=200)
    except:
        st.markdown("QR Code loading...")

# ============================================
# PAGE ROUTING - uses nav key values
# ============================================
def is_page(page, key):
    return page == TRANSLATIONS["English"][key] or page == TRANSLATIONS["Telugu"][key] or page == TRANSLATIONS["Hindi"][key]

# ============================================
# PAGE 1 - SUBMIT COMPLAINT
# ============================================
if is_page(page, "nav_submit"):
    lang = st.selectbox(
        "🌐 Select Your Language / మీ భాషను ఎంచుకోండి / अपनी भाषा चुनें",
        ["English", "Telugu", "Hindi"],
        index=["English", "Telugu", "Hindi"].index(st.session_state.citizen_lang)
    )
    if lang != st.session_state.citizen_lang:
        st.session_state.citizen_lang = lang
        st.rerun()

    T = TRANSLATIONS[lang]
    st.markdown(f'<p class="section-header">{T["submit_title"]}</p>', unsafe_allow_html=True)

    with st.form("complaint_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input(T["full_name"])
            phone = st.text_input(T["phone"])
        with c2:
            location = st.text_input(T["location"])
            ward = st.text_input(T["ward"])

        category = st.selectbox(T["category"], T["categories"])
        description = st.text_area(T["describe"], placeholder=T["describe_placeholder"], height=150)
        uploaded_image = st.file_uploader(T["upload_photo"], type=["jpg","jpeg","png"])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Photo", width=300)
        st.info(T["ai_info"])
        submitted = st.form_submit_button(T["submit_btn"], use_container_width=True)

        if submitted:
            if not name or not phone or not location or not description:
                st.error(T["fill_fields"])
            else:
                with st.spinner("🤖 AI is analyzing your complaint..."):
                    english_description = translate_to_english(description, lang)
                    ai_result = analyze_complaint(english_description, category)

                if ai_result.get("is_fake", False):
                    st.markdown(f"""
                    <div class="fake-card">
                        <h2>🚫 Complaint Rejected</h2>
                        <p>Our AI has flagged this complaint as potentially fake or invalid.</p>
                        <p><strong>Reason:</strong> {ai_result.get("fake_reason","Description does not match a real civic complaint")}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    complaint_id = f"PP-2024-{str(st.session_state.complaint_counter).zfill(3)}"
                    st.session_state.complaint_counter += 1
                    image_data = None
                    if uploaded_image:
                        image_data = base64.b64encode(uploaded_image.read()).decode()

                    complaint = {
                        "id": complaint_id, "name": name, "phone": phone,
                        "location": location, "ward": ward, "category": category,
                        "description": english_description, "original_description": description,
                        "language": lang, "priority": ai_result["priority"],
                        "summary": ai_result["summary"],
                        "department": ai_result.get("department","General Administration"),
                        "status": "Pending",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "image": image_data, "lat": 17.7231, "lon": 83.3012,
                        "is_fake": False, "fake_reason": ""
                    }
                    st.session_state.complaints.append(complaint)

                    deadline_msg = "24 hours" if ai_result["priority"]=="High" else "48 hours" if ai_result["priority"]=="Medium" else "72 hours"
                    st.markdown(f"""
                    <div class="whatsapp-container">
                        <div class="whatsapp-header">
                            <div style="background:#25d366;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;">🏛️</div>
                            <div>
                                <div style="color:#ffffff;font-weight:700;font-size:0.9rem;">Public Pulse Official</div>
                                <div style="color:#25d366;font-size:0.75rem;">● Online</div>
                            </div>
                        </div>
                        <div class="whatsapp-body">
                            <div class="whatsapp-bubble">
                                <p style="margin:0 0 6px 0;color:#075e54;font-weight:700;font-size:0.85rem;">🏛️ Public Pulse Alert</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">Hello <strong>{name}</strong>! 👋</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">✅ Complaint registered successfully!</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">📋 ID: <strong>{complaint_id}</strong></p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">⚡ Priority: <strong>{ai_result["priority"]}</strong></p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">🏢 {ai_result.get("department","General Admin")}</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">⏰ Resolution: <strong>{deadline_msg}</strong></p>
                                <div class="whatsapp-tick">✓✓ Delivered</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    p_icon = "🔴" if ai_result["priority"]=="High" else "🟡" if ai_result["priority"]=="Medium" else "🟢"
                    st.markdown(f"""
                    <div class="success-card">
                        <h2>✅ Complaint Submitted Successfully!</h2>
                        <h1 style="color:#065f46;font-size:2rem;">{complaint_id}</h1>
                        <p>Save this ID to track your complaint</p><hr>
                        <p><strong>🤖 AI Priority:</strong> {p_icon} {ai_result["priority"]}</p>
                        <p><strong>📋 Summary:</strong> {ai_result["summary"]}</p>
                        <p><strong>🏢 Routed To:</strong> {ai_result.get("department","General Administration")}</p>
                        <p><strong>⏱️ Expected Resolution:</strong> Within {deadline_msg}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ============================================
# PAGE 2 - TRACK COMPLAINT
# ============================================
elif is_page(page, "nav_track"):
    TL = get_lang()
    st.markdown(f'<p class="section-header">{TL["track_title"]}</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f'<div class="track-card"><h3 style="text-align:center;color:#1e3a8a;">{TL["track_enter"]}</h3><p style="text-align:center;color:#64748b;">{TL["track_example"]}</p></div>', unsafe_allow_html=True)
        st.markdown("###")
        track_id = st.text_input(TL["track_input"], placeholder="PP-2024-001")
        if st.button(TL["track_btn"], use_container_width=True):
            found = next((c for c in st.session_state.complaints if c['id'].upper()==track_id.upper().strip()), None)
            if found:
                priority = found['priority']
                status = found['status']
                p_icon = "🔴" if priority=="High" else "🟡" if priority=="Medium" else "🟢"
                progress = 10 if status=="Pending" else 60 if status=="In Progress" else 100
                progress_msg = "⏳ Waiting for action" if status=="Pending" else "🔄 Being actively handled" if status=="In Progress" else "🎉 Issue resolved!"
                status_color = "#7c3aed" if status=="Pending" else "#d97706" if status=="In Progress" else "#059669"
                time_remaining, is_overdue = get_time_remaining(found['date'], priority)
                timer_color = "#dc2626" if is_overdue else "#059669"

                st.markdown(f"""
                <div style="background:white;padding:25px;border-radius:20px;box-shadow:0 4px 20px rgba(0,0,0,0.08);margin-top:20px;">
                    <h2 style="text-align:center;color:#1e3a8a;">{TL["track_found"]}</h2>
                    <hr style="border-color:#e2e8f0;">
                    <div style="background:#f8fafc;padding:16px;border-radius:12px;margin-bottom:16px;border-left:4px solid {status_color};">
                        <p style="margin:0;color:#64748b;font-size:0.8rem;font-weight:600;">Current Status</p>
                        <p style="margin:4px 0;color:{status_color};font-size:1.3rem;font-weight:800;">{status}</p>
                        <p style="margin:0;color:#64748b;font-size:0.85rem;">{progress_msg}</p>
                    </div>
                    <table style="width:100%;border-collapse:separate;border-spacing:0 4px;">
                        <tr style="background:#f8fafc;"><td style="padding:10px;color:#64748b;font-weight:600;width:40%;">🆔 ID</td><td style="padding:10px;color:#1e293b;font-weight:700;">{found['id']}</td></tr>
                        <tr><td style="padding:10px;color:#64748b;font-weight:600;">👤 Name</td><td style="padding:10px;color:#1e293b;font-weight:600;">{found['name']}</td></tr>
                        <tr style="background:#f8fafc;"><td style="padding:10px;color:#64748b;font-weight:600;">📍 Location</td><td style="padding:10px;color:#1e293b;font-weight:600;">{found['location']}</td></tr>
                        <tr><td style="padding:10px;color:#64748b;font-weight:600;">📂 Category</td><td style="padding:10px;color:#1e293b;font-weight:600;">{found['category']}</td></tr>
                        <tr style="background:#f8fafc;"><td style="padding:10px;color:#64748b;font-weight:600;">🤖 Priority</td><td style="padding:10px;font-weight:700;">{p_icon} {found['priority']}</td></tr>
                        <tr><td style="padding:10px;color:#64748b;font-weight:600;">🏢 Department</td><td style="padding:10px;color:#2563eb;font-weight:600;">{found['department']}</td></tr>
                        <tr style="background:#f8fafc;"><td style="padding:10px;color:#64748b;font-weight:600;">📋 Summary</td><td style="padding:10px;color:#1e293b;">{found['summary']}</td></tr>
                        <tr><td style="padding:10px;color:#64748b;font-weight:600;">📅 Submitted</td><td style="padding:10px;color:#1e293b;">{found['date']}</td></tr>
                        <tr style="background:#f8fafc;"><td style="padding:10px;color:#64748b;font-weight:600;">⏱️ Time Left</td><td style="padding:10px;font-weight:700;color:{timer_color};">{time_remaining}</td></tr>
                    </table>
                    <p style="color:#64748b;font-size:0.85rem;margin:12px 0 4px;font-weight:600;">Progress: {progress}%</p>
                </div>
                """, unsafe_allow_html=True)

                st.progress(progress)

                st.markdown(f"""
                <div style="background:white;padding:20px;border-radius:16px;box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-top:16px;">
                    <p style="color:#1e293b;font-weight:700;margin-bottom:12px;">📍 Status Timeline</p>
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                        <div style="width:28px;height:28px;border-radius:50%;background:{'#059669' if progress>=10 else '#e2e8f0'};display:flex;align-items:center;justify-content:center;color:white;font-size:0.8rem;font-weight:700;">✓</div>
                        <div><p style="margin:0;color:#1e293b;font-weight:600;font-size:0.9rem;">Complaint Submitted</p><p style="margin:0;color:#64748b;font-size:0.75rem;">{found['date']}</p></div>
                    </div>
                    <div style="width:2px;height:20px;background:#e2e8f0;margin-left:13px;"></div>
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                        <div style="width:28px;height:28px;border-radius:50%;background:{'#d97706' if progress>=60 else '#e2e8f0'};display:flex;align-items:center;justify-content:center;color:white;font-size:0.8rem;font-weight:700;">{'✓' if progress>=60 else '○'}</div>
                        <div><p style="margin:0;color:{'#1e293b' if progress>=60 else '#94a3b8'};font-weight:600;font-size:0.9rem;">In Progress</p><p style="margin:0;color:#64748b;font-size:0.75rem;">Department working on it</p></div>
                    </div>
                    <div style="width:2px;height:20px;background:#e2e8f0;margin-left:13px;"></div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <div style="width:28px;height:28px;border-radius:50%;background:{'#059669' if progress==100 else '#e2e8f0'};display:flex;align-items:center;justify-content:center;color:white;font-size:0.8rem;font-weight:700;">{'✓' if progress==100 else '○'}</div>
                        <div><p style="margin:0;color:{'#1e293b' if progress==100 else '#94a3b8'};font-weight:600;font-size:0.9rem;">Resolved</p><p style="margin:0;color:#64748b;font-size:0.75rem;">Issue fixed successfully</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if found.get('image'):
                    st.image(base64.b64decode(found['image']), width=400, caption="Submitted Photo")
            else:
                st.error(TL["track_not_found"])
                st.info("💡 Complaint IDs look like PP-2024-001")

# ============================================
# PAGE 3 - SATELLITE MAP
# ============================================
elif is_page(page, "nav_satellite"):
    st.markdown('<p class="section-header">🛰️ Live Satellite Map — Visakhapatnam</p>', unsafe_allow_html=True)
    m = folium.Map(location=[17.7231, 83.3012], zoom_start=13,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite")
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Labels", name="Labels", overlay=True).add_to(m)
    for c in st.session_state.complaints:
        if c.get('is_fake', False): continue
        lat = c.get('lat', 17.7231)
        lon = c.get('lon', 83.3012)
        color = get_marker_color(c['priority'])
        time_rem, overdue = get_time_remaining(c['date'], c['priority'])
        popup_html = f"""<div style="font-family:Arial;min-width:220px;padding:5px;">
            <h4 style="color:#1e3a8a;margin:0;">{c['id']}</h4>
            <p><b>👤</b> {c['name']}</p><p><b>📂</b> {c['category']}</p>
            <p><b>📍</b> {c['location']}</p><p><b>Priority:</b> {c['priority']}</p>
            <p><b>Status:</b> {c['status']}</p></div>"""
        folium.Marker(location=[lat, lon], popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"📍 {c['id']} — {c['category']}",
            icon=folium.Icon(color=color, icon="info-sign", prefix="glyphicon")).add_to(m)
    folium.LayerControl().add_to(m)
    st_folium(m, width=None, height=550)

# ============================================
# PAGE 4 - HEATMAP
# ============================================
elif is_page(page, "nav_heatmap"):
    st.markdown('<p class="section-header">🌡️ Complaint Intensity Heatmap</p>', unsafe_allow_html=True)
    hm = folium.Map(location=[17.7231, 83.3012], zoom_start=12, tiles="OpenStreetMap")
    heat_data = []
    for c in st.session_state.complaints:
        if not c.get('is_fake', False):
            weight = 3 if c['priority']=="High" else 2 if c['priority']=="Medium" else 1
            heat_data.append([c.get('lat',17.7231), c.get('lon',83.3012), weight])
    if heat_data:
        HeatMap(heat_data, min_opacity=0.4, max_zoom=18, radius=40, blur=25,
            gradient={0.2:'blue',0.4:'lime',0.6:'yellow',0.8:'orange',1.0:'red'}).add_to(hm)
    st_folium(hm, width=None, height=500)
    df = pd.DataFrame([c for c in st.session_state.complaints if not c.get('is_fake',False)])
    if len(df) > 0:
        loc_counts = df['location'].value_counts().reset_index()
        loc_counts.columns = ['Location','Complaints']
        fig = px.bar(loc_counts, x='Location', y='Complaints', color='Complaints', color_continuous_scale='Reds')
        fig.update_layout(height=300, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 5 - AI ASSISTANT
# ============================================
elif is_page(page, "nav_ai"):
    st.markdown('<p class="section-header">🤖 AI Assistant</p>', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg.get('role') == 'user':
            st.markdown(f'<div style="background:#1e3a8a;color:white;padding:15px;border-radius:15px 15px 5px 15px;margin:10px 0;max-width:80%;margin-left:auto;text-align:right;">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:white;color:#1e293b;padding:15px;border-radius:15px 15px 15px 5px;margin:10px 0;max-width:80%;box-shadow:0 2px 10px rgba(0,0,0,0.1);">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5,1])
        with col1:
            user_input = st.text_input("Ask me anything...", label_visibility="collapsed", placeholder="Type in English, Telugu or Hindi...")
        with col2:
            send = st.form_submit_button("Send 🚀", use_container_width=True)
        if send and user_input:
            st.session_state.chat_history.append({"role":"user","content":user_input})
            with st.spinner("🤖 Thinking..."):
                context = """You are a helpful multilingual AI assistant for Public Pulse — an AI-powered citizen complaint system.
                Features: Submit complaints, Track by ID, Satellite Map, Heatmap, Fake Detector, Predictive AI.
                Respond in the same language the user writes in. Be friendly and concise."""
                bot_reply = call_ai(f"{context}\n\nUser: {user_input}")
            st.session_state.chat_history.append({"role":"assistant","content":bot_reply})
            st.rerun()

    st.markdown("**Quick Questions:**")
    q1,q2,q3 = st.columns(3)
    with q1:
        if st.button("How to submit?"):
            st.session_state.chat_history.append({"role":"user","content":"How to submit?"})
            st.session_state.chat_history.append({"role":"assistant","content":"Go to Submit Complaint, fill your name, phone, location, category and description. You can type in Telugu, Hindi or English! After submission you get a unique ID like PP-2024-001 to track your complaint."})
            st.rerun()
    with q2:
        if st.button("What is fake detector?"):
            st.session_state.chat_history.append({"role":"user","content":"What is fake detector?"})
            st.session_state.chat_history.append({"role":"assistant","content":"Our AI automatically checks every complaint for authenticity. If a complaint is gibberish, offensive or clearly fake, it gets rejected with a reason. This ensures only genuine civic issues reach government departments!"})
            st.rerun()
    with q3:
        if st.button("What is predictive AI?"):
            st.session_state.chat_history.append({"role":"user","content":"What is predictive AI?"})
            st.session_state.chat_history.append({"role":"assistant","content":"Our Predictive AI analyzes complaint patterns and predicts which areas are likely to face problems next week! This enables proactive government action before issues escalate."})
            st.rerun()

# ============================================
# PAGE 6 - PREDICTIVE ALERTS
# ============================================
elif is_page(page, "nav_predict"):
    st.markdown('<p class="section-header">🔮 AI Predictive Alerts</p>', unsafe_allow_html=True)
    st.markdown("""<div style="background:linear-gradient(135deg,#7c3aed,#a855f7);padding:20px;border-radius:15px;color:white;margin-bottom:25px;">
        <h3 style="margin:0;">🧠 How Predictive AI Works</h3>
        <p style="margin-top:10px;opacity:0.9;">Our AI analyzes complaint patterns to predict which areas are likely to face civic problems in the coming week!</p>
    </div>""", unsafe_allow_html=True)

    if st.button("🔮 Generate AI Predictions Now", use_container_width=True):
        with st.spinner("🧠 AI is analyzing complaint patterns..."):
            predictions = generate_prediction(st.session_state.complaints)
        for i, pred in enumerate(predictions):
            risk = pred.get('risk','Medium')
            risk_color = "#dc2626" if risk=="High" else "#d97706" if risk=="Medium" else "#059669"
            risk_bg = "#fee2e2" if risk=="High" else "#fef3c7" if risk=="Medium" else "#d1fae5"
            risk_icon = "🔴" if risk=="High" else "🟡" if risk=="Medium" else "🟢"
            st.markdown(f"""<div style="background:white;padding:25px;border-radius:15px;margin-bottom:15px;border-left:5px solid {risk_color};box-shadow:0 4px 15px rgba(0,0,0,0.08);">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <h3 style="color:#1e3a8a;margin:0;">Prediction #{i+1}: {pred.get('area','')}</h3>
                    <span style="background:{risk_bg};color:{risk_color};padding:5px 15px;border-radius:20px;font-weight:700;">{risk_icon} {risk} Risk</span>
                </div>
                <hr style="border-color:#e2e8f0;">
                <p style="color:#1e293b;"><b>⚠️ Predicted Issue:</b> {pred.get('issue','')}</p>
                <p style="color:#1e293b;"><b>🧠 AI Reasoning:</b> {pred.get('reason','')}</p>
            </div>""", unsafe_allow_html=True)
        st.success("✅ Predictions generated!")

    df = pd.DataFrame([c for c in st.session_state.complaints if not c.get('is_fake',False)])
    if len(df) > 0:
        col1, col2 = st.columns(2)
        with col1:
            trend = df.groupby(['category','priority']).size().reset_index(name='count')
            fig = px.bar(trend, x='category', y='count', color='priority',
                color_discrete_map={'High':'#dc2626','Medium':'#d97706','Low':'#059669'},
                title="Complaints by Category & Priority", barmode='group')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            loc_counts = df['location'].value_counts().reset_index()
            loc_counts.columns = ['Location','Count']
            fig2 = px.pie(loc_counts, values='Count', names='Location', title="Complaints by Location", hole=0.4)
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 7 - ADMIN DASHBOARD
# ============================================
elif is_page(page, "nav_dashboard"):
    if not st.session_state.admin_logged_in:
        st.warning("⚠️ Please login as Admin first.")
    else:
        st.markdown('<p class="section-header">📊 Admin Dashboard</p>', unsafe_allow_html=True)
        complaints = st.session_state.complaints
        total = len(complaints)
        high = len([c for c in complaints if c['priority']=='High'])
        medium = len([c for c in complaints if c['priority']=='Medium'])
        low = len([c for c in complaints if c['priority']=='Low'])
        resolved = len([c for c in complaints if c['status']=='Resolved'])
        pending = len([c for c in complaints if c['status']=='Pending'])
        fake = len([c for c in complaints if c.get('is_fake',False)])

        c1,c2,c3,c4,c5,c6 = st.columns(6)
        with c1: st.markdown(f'<div class="metric-card"><div class="metric-number">{total}</div><div class="metric-label">Total</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card" style="border-top-color:#dc2626"><div class="metric-number" style="color:#dc2626">{high}</div><div class="metric-label">🔴 High</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card" style="border-top-color:#d97706"><div class="metric-number" style="color:#d97706">{medium}</div><div class="metric-label">🟡 Medium</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric-card" style="border-top-color:#059669"><div class="metric-number" style="color:#059669">{resolved}</div><div class="metric-label">✅ Resolved</div></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="metric-card" style="border-top-color:#7c3aed"><div class="metric-number" style="color:#7c3aed">{pending}</div><div class="metric-label">⏳ Pending</div></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="metric-card" style="border-top-color:#be185d"><div class="metric-number" style="color:#be185d">{fake}</div><div class="metric-label">🚫 Fake</div></div>', unsafe_allow_html=True)

        if total > 0:
            resolution_rate = int((resolved/total)*100)
            st.markdown(f"### 📈 Resolution Rate: {resolution_rate}%")
            st.progress(resolution_rate)

        col1, col2 = st.columns(2)
        real_complaints = [c for c in complaints if not c.get('is_fake',False)]
        df = pd.DataFrame(real_complaints) if real_complaints else pd.DataFrame()
        if len(df) > 0:
            with col1:
                cat_counts = df['category'].value_counts().reset_index()
                cat_counts.columns = ['Category','Count']
                fig1 = px.bar(cat_counts, x='Category', y='Count', color='Count', color_continuous_scale='Blues', text='Count')
                fig1.update_layout(margin=dict(t=20,b=0), height=300, showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                priority_counts = df['priority'].value_counts().reset_index()
                priority_counts.columns = ['Priority','Count']
                fig2 = px.pie(priority_counts, values='Count', names='Priority',
                    color='Priority', color_discrete_map={'High':'#dc2626','Medium':'#d97706','Low':'#059669'}, hole=0.5)
                fig2.update_layout(margin=dict(t=20,b=0), height=300)
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.markdown("**🔍 Search & Filter**")
        search = st.text_input("🔎 Search by name, location or ID")
        f1,f2,f3,f4 = st.columns(4)
        with f1: filter_priority = st.selectbox("Priority", ["All","High","Medium","Low"])
        with f2: filter_status = st.selectbox("Status", ["All","Pending","In Progress","Resolved"])
        with f3: filter_category = st.selectbox("Category", ["All","Road & Potholes","Water Supply","Garbage & Sanitation","Electricity","Public Spaces & Parks"])
        with f4: filter_fake = st.selectbox("Authenticity", ["Real Only","All","Fake Only"])

        filtered = complaints.copy()
        if search:
            filtered = [c for c in filtered if search.lower() in c['name'].lower() or search.lower() in c['location'].lower() or search.lower() in c['id'].lower()]
        if filter_priority != "All": filtered = [c for c in filtered if c['priority']==filter_priority]
        if filter_status != "All": filtered = [c for c in filtered if c['status']==filter_status]
        if filter_category != "All": filtered = [c for c in filtered if c['category']==filter_category]
        if filter_fake == "Real Only": filtered = [c for c in filtered if not c.get('is_fake',False)]
        elif filter_fake == "Fake Only": filtered = [c for c in filtered if c.get('is_fake',False)]

        col_show, col_export = st.columns([3,1])
        with col_show: st.markdown(f"**Showing {len(filtered)} complaints**")
        with col_export:
            if filtered:
                df_export = pd.DataFrame(filtered).drop(columns=['image','lat','lon'], errors='ignore')
                st.download_button("📥 Export CSV", data=df_export.to_csv(index=False),
                    file_name="complaints.csv", mime="text/csv", use_container_width=True)

        st.markdown("---")
        for complaint in filtered:
            priority = complaint['priority']
            status = complaint['status']
            is_fake = complaint.get('is_fake', False)
            time_rem, overdue = get_time_remaining(complaint['date'], priority)
            p_badge = '<span class="badge-high">🔴 High</span>' if priority=="High" else '<span class="badge-medium">🟡 Medium</span>' if priority=="Medium" else '<span class="badge-low">🟢 Low</span>'
            fake_badge = '<span class="fake-badge">🚫 FAKE</span>' if is_fake else '<span style="background:#d1fae5;color:#065f46;padding:4px 12px;border-radius:20px;font-weight:600;font-size:0.78rem;">✅ Genuine</span>'
            border_color = "#be185d" if is_fake else "#dc2626" if priority=="High" else "#d97706" if priority=="Medium" else "#059669"
            timer_color = "#dc2626" if overdue else "#059669"

            st.markdown(f"""
            <div class="complaint-card" style="border-left-color:{border_color};">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <div><strong style="color:#1e3a8a;">{complaint['id']}</strong>&nbsp;{p_badge}&nbsp;{fake_badge}</div>
                    <div style="color:#64748b;font-size:0.85rem;">📅 {complaint['date']}</div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:10px;">
                    <div><span style="color:#64748b;">👤</span><br><strong>{complaint['name']}</strong></div>
                    <div><span style="color:#64748b;">📍</span><br><strong>{complaint['location']}</strong></div>
                    <div><span style="color:#64748b;">📂</span><br><strong>{complaint['category']}</strong></div>
                </div>
                <div style="background:#f8fafc;padding:12px;border-radius:8px;margin-bottom:10px;">
                    <strong style="color:#1e293b;">{complaint['summary']}</strong><br>
                    <span style="color:#2563eb;font-size:0.85rem;">🏢 {complaint['department']}</span>
                </div>
                <div style="color:#1e293b;font-size:0.9rem;">{complaint['description']}</div>
            </div>
            """, unsafe_allow_html=True)

            if complaint.get('image'):
                st.image(base64.b64decode(complaint['image']), width=300, caption="Complaint Photo")

            if not is_fake:
                new_status = st.selectbox(f"Update Status for {complaint['id']}",
                    ["Pending","In Progress","Resolved"],
                    index=["Pending","In Progress","Resolved"].index(complaint['status']),
                    key=f"status_{complaint['id']}")
                if new_status != complaint['status']:
                    for c in st.session_state.complaints:
                        if c['id'] == complaint['id']:
                            c['status'] = new_status
                    st.success(f"✅ Status updated to {new_status}!")
                    status_emoji = "🔄" if new_status=="In Progress" else "✅" if new_status=="Resolved" else "⏳"
                    status_msg = "is being actively worked on!" if new_status=="In Progress" else "has been RESOLVED! 🎉" if new_status=="Resolved" else "is pending assignment."
                    st.markdown(f"""
                    <div class="whatsapp-container">
                        <div class="whatsapp-header">
                            <div style="background:#25d366;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;">🏛️</div>
                            <div><div style="color:#ffffff;font-weight:700;font-size:0.9rem;">Public Pulse Official</div><div style="color:#25d366;font-size:0.75rem;">● Online</div></div>
                        </div>
                        <div class="whatsapp-body">
                            <div class="whatsapp-bubble">
                                <p style="margin:0 0 6px 0;color:#075e54;font-weight:700;font-size:0.85rem;">🔔 Status Update</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">Hello <strong>{complaint['name']}</strong>! 👋</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">{status_emoji} Complaint <strong>{complaint['id']}</strong> {status_msg}</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">Status: <strong>{new_status}</strong></p>
                                <div class="whatsapp-tick">✓✓ Delivered</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.rerun()
            st.markdown("---")

# ============================================
# PAGE - FEEDBACK
# ============================================
elif is_page(page, "nav_feedback"):
    TF = TRANSLATIONS[st.session_state.citizen_lang]
    st.markdown(f'<p class="section-header">{TF["feedback_title"]}</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("feedback_form"):
            complaint_id = st.text_input(TF["feedback_complaint_id"], placeholder="PP-2024-001")
            rating = st.selectbox(TF["feedback_rate"], TF["ratings"])
            service_rating = st.selectbox(TF["feedback_service"], TF["service_ratings"])
            feedback_text = st.text_area(TF["feedback_comments"], placeholder="Tell us about your experience...", height=120)
            recommend = st.selectbox(TF["feedback_recommend"], TF["recommend_options"])
            submitted = st.form_submit_button(TF["feedback_submit"], use_container_width=True)
            if submitted:
                if not complaint_id:
                    st.error("Please enter your Complaint ID!")
                else:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#d1fae5,#a7f3d0);padding:25px;border-radius:16px;border:1px solid #10b981;text-align:center;">
                        <h2 style="color:#065f46;">{TF["feedback_thanks"]}</h2>
                        <p style="color:#1e293b;"><strong>ID:</strong> {complaint_id} | <strong>Rating:</strong> {rating}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="whatsapp-container" style="margin-top:16px;">
                        <div class="whatsapp-header">
                            <div style="background:#25d366;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;">🏛️</div>
                            <div><div style="color:#ffffff;font-weight:700;font-size:0.9rem;">Public Pulse Official</div><div style="color:#25d366;font-size:0.75rem;">● Online</div></div>
                        </div>
                        <div class="whatsapp-body">
                            <div class="whatsapp-bubble">
                                <p style="margin:0 0 6px 0;color:#075e54;font-weight:700;">🙏 Feedback Received!</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">Thank you for rating us {rating}</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">Complaint: <strong>{complaint_id}</strong></p>
                                <div class="whatsapp-tick">✓✓ Delivered</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ============================================
# PAGE - QR CODE
# ============================================
elif is_page(page, "nav_qr"):
    TQ = get_lang()
    st.markdown(f'<p class="section-header">{TQ["scan_title"]}</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        try:
            st.image("public_pulse_qr.png", width=280, caption="Scan to open Public Pulse")
        except:
            st.markdown("""<div style="background:#f8fafc;border:2px dashed #2563eb;border-radius:16px;padding:40px;text-align:center;">
                <p style="font-size:4rem;">📱</p>
                <p style="color:#1e3a8a;font-weight:700;">QR Code</p>
                <p style="color:#64748b;">publicpulse.streamlit.app</p>
            </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;padding:20px;border-radius:16px;box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-top:16px;">
            <h3 style="color:#1e3a8a;text-align:center;">📲 How to Install</h3>
            <div style="background:#f8fafc;padding:12px;border-radius:10px;margin:8px 0;">
                <p style="margin:4px 0;color:#1e293b;"><strong>Android:</strong></p>
                <p style="margin:4px 0;color:#64748b;">1. Scan QR → 2. Tap ⋮ menu → 3. Add to Home Screen</p>
            </div>
            <div style="background:#f8fafc;padding:12px;border-radius:10px;margin:8px 0;">
                <p style="margin:4px 0;color:#1e293b;"><strong>iPhone:</strong></p>
                <p style="margin:4px 0;color:#64748b;">1. Scan QR → 2. Tap Share → 3. Add to Home Screen</p>
            </div>
        </div>
        <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);padding:16px;border-radius:14px;text-align:center;margin-top:16px;">
            <p style="color:white;font-weight:700;margin:0;">🌐 Live URL</p>
            <p style="color:#93c5fd;margin:4px 0;font-size:0.9rem;">publicpulse.streamlit.app</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# PAGE - LEADERBOARD
# ============================================
elif is_page(page, "nav_leaderboard"):
    st.markdown('<p class="section-header">🏅 Department Performance Leaderboard</p>', unsafe_allow_html=True)
    complaints = st.session_state.complaints
    real_complaints = [c for c in complaints if not c.get('is_fake', False)]
    dept_stats = {}
    for c in real_complaints:
        dept = c.get('department', 'General Administration')
        if dept not in dept_stats:
            dept_stats[dept] = {'total':0,'resolved':0,'pending':0,'high':0,'in_progress':0}
        dept_stats[dept]['total'] += 1
        if c['status'] == 'Resolved': dept_stats[dept]['resolved'] += 1
        if c['status'] == 'Pending': dept_stats[dept]['pending'] += 1
        if c['status'] == 'In Progress': dept_stats[dept]['in_progress'] += 1
        if c['priority'] == 'High': dept_stats[dept]['high'] += 1

    leaderboard = []
    for dept, stats in dept_stats.items():
        rate = int((stats['resolved']/stats['total'])*100) if stats['total'] > 0 else 0
        score = round((rate * 0.6) + ((stats['total']/max(1,len(real_complaints)))*40), 1)
        leaderboard.append({'department':dept,'total':stats['total'],'resolved':stats['resolved'],
            'pending':stats['pending'],'in_progress':stats['in_progress'],'high':stats['high'],'rate':rate,'score':score})
    leaderboard.sort(key=lambda x: x['score'], reverse=True)

    medals = ["🥇","🥈","🥉"]
    podium_colors = ["#f59e0b","#6366f1","#10b981"]
    podium_shadows = ["rgba(245,158,11,0.3)","rgba(99,102,241,0.3)","rgba(16,185,129,0.3)"]

    if len(leaderboard) >= 3:
        col1, col2, col3 = st.columns(3)
        for i, (col, rank) in enumerate(zip([col1,col2,col3],[1,0,2])):
            if rank < len(leaderboard):
                d = leaderboard[rank]
                with col:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,{podium_colors[rank]}20,{podium_colors[rank]}10);
                                border:2px solid {podium_colors[rank]}60;border-radius:20px;padding:25px;text-align:center;
                                box-shadow:0 8px 25px {podium_shadows[rank]};margin-bottom:15px;">
                        <div style="font-size:3rem;">{medals[rank]}</div>
                        <div style="font-weight:800;color:#1e293b;font-size:0.9rem;margin:10px 0;">{d['department'][:22]}</div>
                        <div style="font-size:2rem;font-weight:900;color:{podium_colors[rank]};">{d['rate']}%</div>
                        <div style="color:#64748b;font-size:0.75rem;">Resolution Rate</div>
                        <div style="margin-top:10px;font-size:0.8rem;color:#64748b;">✅ {d['resolved']} resolved | 📋 {d['total']} total</div>
                    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    for i, dept in enumerate(leaderboard):
        medal = medals[i] if i < 3 else f"#{i+1}"
        rate = dept['rate']
        bar_color = "#16a34a" if rate >= 70 else "#f59e0b" if rate >= 40 else "#ef4444"
        rate_color = "#16a34a" if rate >= 70 else "#d97706" if rate >= 40 else "#dc2626"
        grade = "⭐ Excellent" if rate >= 70 else "👍 Good" if rate >= 40 else "⚠️ Needs Work"
        st.markdown(f"""
        <div class="rank-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <span style="font-size:2rem;">{medal}</span>
                    <div>
                        <div style="font-weight:700;color:#1e293b;">{dept['department']}</div>
                        <div style="color:#64748b;font-size:0.8rem;">📋 {dept['total']} | ✅ {dept['resolved']} | ⏳ {dept['pending']}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.8rem;font-weight:800;color:{rate_color};">{rate}%</div>
                    <div style="color:#64748b;font-size:0.75rem;">{grade}</div>
                </div>
            </div>
            <div style="background:#f3f4f6;border-radius:10px;height:8px;overflow:hidden;">
                <div style="background:{bar_color};width:{rate}%;height:100%;border-radius:10px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)

# ============================================
# PAGE - ADMIN LOGIN
# ============================================
elif is_page(page, "nav_admin"):
    admin_lang = st.selectbox(
        "🌐 Select Language / భాష ఎంచుకోండి / भाषा चुनें",
        ["English", "Telugu", "Hindi"],
        index=["English", "Telugu", "Hindi"].index(st.session_state.admin_lang)
    )
    if admin_lang != st.session_state.admin_lang:
        st.session_state.admin_lang = admin_lang
        st.rerun()

    TA = TRANSLATIONS[admin_lang]
    st.markdown(f'<p class="section-header">{TA["admin_title"]}</p>', unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        if st.session_state.admin_logged_in:
            st.success(TA["admin_logged_in"])
            if st.button(TA["admin_logout"]):
                st.session_state.admin_logged_in = False
                st.rerun()
        else:
            st.markdown(f"""
            <div style="background:white;padding:40px;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,0.1);">
                <h3 style="text-align:center;color:#1e3a8a;">{TA["admin_portal"]}</h3>
                <p style="text-align:center;color:#64748b;">{TA["admin_subtitle"]}</p>
            </div>""", unsafe_allow_html=True)
            with st.form("login_form"):
                username = st.text_input(TA["admin_username"])
                password = st.text_input(TA["admin_password"], type="password")
                login_btn = st.form_submit_button(TA["admin_login_btn"], use_container_width=True)
                if login_btn:
                    if username=="admin" and password==ADMIN_PASSWORD:
                        st.session_state.admin_logged_in = True
                        st.success(TA["admin_success"])
                        st.rerun()
                    else:
                        st.error(TA["admin_invalid"])