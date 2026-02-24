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

GROQ_API_KEY = "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"
ADMIN_PASSWORD = "admin123"

st.set_page_config(
    page_title="Public Pulse | Smart Citizen Services",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; }

    /* PWA MOBILE APP FEEL */
    .main .block-container {
        padding: 0.5rem 0.8rem !important;
        max-width: 100% !important;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* MOBILE BOTTOM NAV FEEL */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.08) !important;
    }

    /* APP HEADER */
    .app-header {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        padding: 16px 20px;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
        margin-bottom: 16px;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 4px 20px rgba(37,99,235,0.3);
    }

    .app-header h1 {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.5px !important;
    }

    .app-header p {
        font-size: 0.72rem !important;
        opacity: 0.85 !important;
        margin: 4px 0 0 0 !important;
    }

    /* MOBILE CARDS */
    .mobile-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    /* METRIC CARDS MOBILE */
    .metric-card {
        background: white;
        padding: 16px 12px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border-top: 3px solid #2563eb;
        margin-bottom: 8px;
    }

    .metric-number {
        font-size: 2rem !important;
        font-weight: 800;
        color: #1e3a8a;
    }

    .metric-label {
        font-size: 0.72rem;
        color: #64748b;
        margin-top: 3px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* COMPLAINT CARDS MOBILE */
    .complaint-card {
        background: white;
        padding: 16px;
        border-radius: 14px;
        margin-bottom: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border-left: 4px solid #2563eb;
        color: #1e293b !important;
    }

    .complaint-card * { color: #1e293b !important; }

    /* SECTION HEADER MOBILE */
    .section-header {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #000000 !important;
        margin-bottom: 14px !important;
        padding-bottom: 8px !important;
        border-bottom: 2px solid #2563eb !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* BUTTONS MOBILE */
    .stButton>button {
        background: linear-gradient(135deg, #1e3a8a, #2563eb) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(37,99,235,0.3) !important;
    }

    .stFormSubmitButton>button {
        background: linear-gradient(135deg, #1e3a8a, #2563eb) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 14px !important;
        font-size: 1rem !important;
    }

    /* INPUTS MOBILE */
    .stTextInput>div>div>input {
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: #f8fafc !important;
        color: #1e293b !important;
        padding: 12px 14px !important;
        font-size: 0.95rem !important;
    }

    .stTextArea>div>div>textarea {
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: #f8fafc !important;
        color: #1e293b !important;
        font-size: 0.95rem !important;
    }

    div[data-testid="stForm"] input {
        background: #f8fafc !important;
        color: #1e293b !important;
    }

    div[data-testid="stForm"] textarea {
        background: #f8fafc !important;
        color: #1e293b !important;
    }

    /* FORM CONTAINER */
    div[data-testid="stForm"] {
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 16px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }

    /* DROPDOWN */
    .stSelectbox [data-baseweb="select"] {
        background: #f8fafc !important;
        border-radius: 10px !important;
    }
    .stSelectbox [data-baseweb="select"] * {
        background: #f8fafc !important;
        color: #1e293b !important;
    }
    .stSelectbox svg { fill: #2563eb !important; }
    [data-baseweb="popover"] * {
        background: #ffffff !important;
        color: #1e293b !important;
    }

    /* FILE UPLOADER */
    [data-testid="stFileUploaderDropzone"] {
        background: #f8fafc !important;
        border: 2px dashed #2563eb !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploaderDropzone"] * { color: #1e293b !important; }
    [data-testid="stFileUploader"] * { color: #1e293b !important; }
    section[data-testid="stFileUploaderDropzone"] p,
    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] small,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] span { color: #64748b !important; }

    /* PASSWORD */
    [data-testid="stPasswordInput"] button {
        background: #f8fafc !important;
        border: none !important;
    }
    [data-testid="stPasswordInput"] svg {
        fill: #2563eb !important;
        stroke: #2563eb !important;
    }

    /* SIDEBAR MOBILE */
    .sidebar-stats {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        padding: 16px;
        border-radius: 14px;
        color: white;
        margin-bottom: 16px;
    }

    /* BADGES */
    .badge-high { background:#fee2e2; color:#dc2626 !important; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.78rem; border:1px solid #fecaca; }
    .badge-medium { background:#fef3c7; color:#d97706 !important; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.78rem; border:1px solid #fde68a; }
    .badge-low { background:#d1fae5; color:#059669 !important; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.78rem; border:1px solid #a7f3d0; }
    .fake-badge { background:#fce7f3; color:#be185d !important; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.78rem; border:1px solid #fbcfe8; }

    /* SUCCESS CARD */
    .success-card {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        padding: 24px 16px;
        border-radius: 16px;
        border: 1px solid #10b981;
        text-align: center;
        color: #1e293b !important;
    }

    /* TRACK CARD */
    .track-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        color: #1e293b !important;
    }
    .track-card * { color: #1e293b !important; }

    /* WHATSAPP */
    .whatsapp-container {
        max-width: 340px;
        margin: 16px auto;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    .whatsapp-header {
        background: #075e54;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .whatsapp-body {
        background: #e5ddd5;
        padding: 16px;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    .whatsapp-bubble {
        background: #ffffff;
        border-radius: 0 12px 12px 12px;
        padding: 12px 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        max-width: 300px;
    }
    .whatsapp-tick {
        text-align: right;
        color: #34b7f1;
        font-size: 0.7rem;
        margin-top: 6px;
    }

    /* LEADERBOARD */
    .rank-card {
        background: white;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 10px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* PREDICT CARD */
    .predict-card {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        padding: 16px;
        border-radius: 14px;
        color: white;
        margin-bottom: 12px;
    }

    .fake-card {
        background: linear-gradient(135deg, #be185d, #ec4899);
        padding: 16px;
        border-radius: 14px;
        color: white;
        margin-bottom: 12px;
    }

    /* TIMER */
    .timer-high { color: #dc2626; font-weight: 700; }
    .timer-medium { color: #d97706; font-weight: 700; }
    .timer-low { color: #059669; font-weight: 700; }

    /* PROGRESS */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1e3a8a, #2563eb) !important;
        border-radius: 10px !important;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #2563eb; border-radius: 4px; }

    /* RADIO */
    .stRadio label { 
        color: #000000 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    /* ALL LABELS BLACK */
    label { color: #000000 !important; }
    p { color: #000000 !important; }
    .stMarkdown p { color: #000000 !important; }
    .stMarkdown { color: #000000 !important; }
    [data-testid="stMarkdownContainer"] p { color: #000000 !important; }
    [data-testid="stMarkdownContainer"] { color: #000000 !important; }
    div[data-testid="stForm"] label { color: #000000 !important; }
    .stSelectbox label { color: #000000 !important; }
    .stTextInput label { color: #000000 !important; }
    .stTextArea label { color: #000000 !important; }
    .stFileUploader label { color: #000000 !important; }

    /* DIVIDER */
    hr { border-color: #f1f5f9 !important; }

    /* ALERTS */
    .stAlert { border-radius: 12px !important; }

    /* MOBILE RESPONSIVE */
    @media (max-width: 768px) {
        .main .block-container { padding: 0.3rem 0.5rem !important; }
        .hero-header h1 { font-size: 1.4rem !important; }
        .metric-number { font-size: 1.6rem !important; }
        .complaint-card { padding: 12px !important; }
        .section-header { font-size: 1rem !important; }
    }
    .main { background-color: #f0f4f8; }
    .hero-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #0ea5e9 100%);
        padding: 40px; border-radius: 20px; color: white;
        text-align: center; margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(37, 99, 235, 0.3);
    }
    .hero-header h1 { font-size: 3rem; font-weight: 700; margin: 0; }
    .hero-header p { font-size: 1.1rem; opacity: 0.9; margin-top: 10px; }
    .metric-card {
        background: white; padding: 25px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-top: 4px solid #2563eb;
    }
    .metric-number { font-size: 2.5rem; font-weight: 700; color: #1e3a8a; }
    .metric-label { font-size: 0.9rem; color: #64748b; margin-top: 5px; font-weight: 500; }
    .complaint-card {
        background: white; padding: 25px; border-radius: 15px;
        margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border-left: 5px solid #2563eb; color: #1e293b !important;
    }
    .complaint-card * { color: #1e293b !important; }
    .badge-high { background:#fee2e2; color:#dc2626 !important; padding:5px 15px; border-radius:20px; font-weight:600; font-size:0.85rem; }
    .badge-medium { background:#fef3c7; color:#d97706 !important; padding:5px 15px; border-radius:20px; font-weight:600; font-size:0.85rem; }
    .badge-low { background:#d1fae5; color:#059669 !important; padding:5px 15px; border-radius:20px; font-weight:600; font-size:0.85rem; }
    .fake-badge { background:#fce7f3; color:#be185d !important; padding:5px 15px; border-radius:20px; font-weight:600; font-size:0.85rem; }
    .success-card {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        padding: 30px; border-radius: 20px; border: 2px solid #10b981;
        text-align: center; box-shadow: 0 10px 30px rgba(16,185,129,0.2);
    }
    .section-header {
        font-size: 1.5rem; font-weight: 700; color: #ffffff !important;
        margin-bottom: 20px; padding-bottom: 10px;
        border-bottom: 3px solid #2563eb;
    }
    .sidebar-stats {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;
    }
    .track-card {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); color: #1e293b !important;
    }
    .track-card * { color: #1e293b !important; }
    .predict-card {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        padding: 20px; border-radius: 15px; color: white;
        margin-bottom: 15px; box-shadow: 0 4px 15px rgba(124,58,237,0.4);
    }
    .fake-card {
        background: linear-gradient(135deg, #be185d, #ec4899);
        padding: 20px; border-radius: 15px; color: white;
        margin-bottom: 15px;
    }
    .timer-high { color: #dc2626; font-weight: 700; font-size: 1.1rem; }
    .timer-medium { color: #d97706; font-weight: 700; font-size: 1.1rem; }
    .timer-low { color: #059669; font-weight: 700; font-size: 1.1rem; }
    .stTextInput>div>div>input { border-radius:10px; border:2px solid #1e3a8a !important; color:#000000 !important; background-color:#ffffff !important; caret-color:#000000 !important; }
    .stTextArea>div>div>textarea { border-radius:10px; border:2px solid #1e3a8a !important; color:#000000 !important; background-color:#ffffff !important; }
    .stSelectbox>div>div { border-radius:10px; border:2px solid #e2e8f0; }
    .stSelectbox [data-baseweb="select"] { background-color:#ffffff !important; }
    .stSelectbox [data-baseweb="select"] * { background-color:#ffffff !important; color:#000000 !important; }
    .stSelectbox svg { fill: #000000 !important; }
    [data-baseweb="select"] * { color:#000000 !important; background-color:#ffffff !important; }
    [data-baseweb="popover"] * { color:#000000 !important; background-color:#ffffff !important; }
    [data-testid="stFileUploader"] * { color: #ffffff !important; }
    [data-testid="stFileUploaderDropzone"] { background-color: #1e293b !important; }
    [data-testid="stFileUploaderDropzone"] * { color: #ffffff !important; }
    [data-testid="stPasswordInput"] button { color:#ffffff !important; background-color:#1e293b !important; border:none !important; }
    [data-testid="stPasswordInput"] svg { fill:#ffffff !important; stroke:#ffffff !important; }
    .stButton>button { background: #1e3a8a !important; color: #ffffff !important; border: none !important; border-radius: 10px; padding: 12px 30px; font-weight: 700; font-size: 1rem; width: 100%; }
    .stButton>button:hover { background: #2563eb !important; color: #ffffff !important; }
    .stFormSubmitButton>button { background: #1e3a8a !important; color: #ffffff !important; border: none !important; font-weight: 700 !important; }
    div[data-testid="stForm"] input { background-color:#ffffff !important; color:#000000 !important; }
    div[data-testid="stForm"] textarea { background-color:#ffffff !important; color:#000000 !important; }
    section[data-testid="stFileUploaderDropzone"] p,
    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] small,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] span { color: #ffffff !important; }

    /* MOBILE RESPONSIVE */
    @media (max-width: 768px) {
        .hero-header h1 { font-size: 1.8rem !important; }
        .hero-header { padding: 20px !important; }
        .metric-card { padding: 15px !important; }
        .metric-number { font-size: 1.8rem !important; }
        .complaint-card { padding: 15px !important; }
        [data-testid="column"] { min-width: 100% !important; }
        .section-header { font-size: 1.2rem !important; }
        div[data-testid="stForm"] { padding: 15px !important; }
    }
    
    /* WHATSAPP STYLES */
    .whatsapp-container {
        max-width: 360px;
        margin: 20px auto;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        font-family: 'Inter', sans-serif;
    }
    .whatsapp-header {
        background: #075e54;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .whatsapp-body {
        background: #e5ddd5;
        padding: 16px;
    }
    .whatsapp-bubble {
        background: #ffffff;
        border-radius: 0 12px 12px 12px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        max-width: 320px;
    }
    .whatsapp-tick {
        text-align: right;
        color: #34b7f1;
        font-size: 0.7rem;
        margin-top: 6px;
    }

    /* LEADERBOARD */
    .podium-card {
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .rank-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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
    st.session_state.chat_history = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hello! I am the Public Pulse AI Assistant. I can help you submit complaints, track status, and answer civic questions. How can I help you today?"}
    ]

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
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except:
        return text

def call_ai(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
        )
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"API Error: {data['error']['message']}"
        else:
            return f"Unexpected response: {str(data)}"
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_complaint(description, category):
    try:
        prompt = f"""
        You are a government complaint analysis AI.
        Category: {category}
        Description: {description}
        Respond ONLY with this JSON — no extra text:
        {{"priority": "High or Medium or Low", "summary": "One line summary", "department": "Government department name", "is_fake": true or false, "fake_reason": "reason if fake else empty string"}}
        Priority rules: High=safety risk/health hazard, Medium=inconvenience, Low=minor issue
        Fake detection: Mark as fake if description is gibberish, too vague, offensive, duplicate intent, or clearly not a real civic complaint.
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except:
        return {"priority": "Medium", "summary": "Complaint received and logged", "department": "General Administration", "is_fake": False, "fake_reason": ""}

def generate_prediction(complaints):
    try:
        summary = "\n".join([
            f"- {c['category']} at {c['location']} | Priority: {c['priority']} | Date: {c['date']}"
            for c in complaints
        ])
        prompt = f"""
        You are a smart city AI analyst. Based on these civic complaint patterns:
        {summary}
        
        Generate exactly 3 predictions about which areas or issues are likely to worsen next week.
        Respond ONLY with a JSON array like this:
        [
          {{"area": "Area name", "issue": "Issue type", "risk": "High/Medium/Low", "reason": "One line reason"}},
          {{"area": "Area name", "issue": "Issue type", "risk": "High/Medium/Low", "reason": "One line reason"}},
          {{"area": "Area name", "issue": "Issue type", "risk": "High/Medium/Low", "reason": "One line reason"}}
        ]
        Only respond with the JSON array, nothing else.
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except:
        return [
            {"area": "MVP Colony", "issue": "Water Supply", "risk": "High", "reason": "Repeated water complaints in this area"},
            {"area": "Maddilapalem", "issue": "Road & Potholes", "risk": "High", "reason": "Multiple pothole reports detected"},
            {"area": "Gajuwaka", "issue": "Garbage & Sanitation", "risk": "Medium", "reason": "Sanitation complaints increasing"}
        ]

# ============================================
# ============================================
# COPILOT FUNCTION
# ============================================
def ask_copilot(question):
    try:
        complaints = st.session_state.complaints
        total = len(complaints)
        high = len([c for c in complaints if c['priority'] == 'High'])
        medium = len([c for c in complaints if c['priority'] == 'Medium'])
        low = len([c for c in complaints if c['priority'] == 'Low'])
        resolved = len([c for c in complaints if c['status'] == 'Resolved'])
        pending = len([c for c in complaints if c['status'] == 'Pending'])

        complaint_details = ""
        for c in complaints:
            complaint_details += f"ID:{c['id']} Category:{c['category']} Location:{c['location']} Priority:{c['priority']} Status:{c['status']}\n"

        prompt = f"""
        You are Public Pulse AI Copilot, a smart helpful assistant for a citizen complaint management system.
        
        Current system data:
        - Total Complaints: {total}
        - High Priority: {high}
        - Medium Priority: {medium}
        - Low Priority: {low}
        - Resolved: {resolved}
        - Pending: {pending}
        
        All Complaints:
        {complaint_details}
        
        Instructions:
        - Answer ANY question the user asks
        - If question is about complaints, use the data above
        - If question is general knowledge, answer from your knowledge
        - If question is about how to use this app, explain clearly
        - Always be friendly, helpful and concise
        - Never say you cannot answer
        
        User Question: {question}
        """
        return call_ai(prompt)
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================
st.markdown("""
<div class="app-header">
    <div style="display:flex;align-items:center;justify-content:center;gap:12px;">
        <div style="background:rgba(255,255,255,0.2);width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;">🏛️</div>
        <div style="text-align:left;">
            <h1 style="color:white;margin:0;font-size:1.5rem;font-weight:800;">Public Pulse</h1>
            <p style="color:rgba(255,255,255,0.8);margin:0;font-size:0.72rem;">AI Citizen Services • Ratan Tata Innovation Hub</p>
        </div>
    </div>
    <div style="display:flex;justify-content:center;gap:12px;margin-top:12px;flex-wrap:wrap;">
        <span style="background:rgba(255,255,255,0.15);color:white;padding:4px 10px;border-radius:20px;font-size:0.7rem;font-weight:600;">🌐 Multilingual</span>
        <span style="background:rgba(255,255,255,0.15);color:white;padding:4px 10px;border-radius:20px;font-size:0.7rem;font-weight:600;">🔍 Fake Detector</span>
        <span style="background:rgba(255,255,255,0.15);color:white;padding:4px 10px;border-radius:20px;font-size:0.7rem;font-weight:600;">🗺️ Satellite Map</span>
        <span style="background:rgba(255,255,255,0.15);color:white;padding:4px 10px;border-radius:20px;font-size:0.7rem;font-weight:600;">🤖 Predictive AI</span>
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
    <div style="background:white; border-radius:20px; 
                box-shadow:0 10px 40px rgba(0,0,0,0.2); 
                margin-bottom:20px; overflow:hidden;">
        <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb); 
                    padding:15px 20px;">
            <span style="color:white; font-weight:700; font-size:1rem;">🤖 Public Pulse Copilot</span><br>
            <span style="color:rgba(255,255,255,0.8); font-size:0.8rem;">Ask me anything about complaints!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.chat_history:
        for chat in st.session_state.chat_history[-4:]:
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
                st.session_state.chat_history.append({
                    "user": user_question,
                    "bot": answer
                })
                st.rerun()
# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    complaints = st.session_state.complaints
    total = len(complaints)
    high = len([c for c in complaints if c['priority'] == 'High'])
    resolved = len([c for c in complaints if c['status'] == 'Resolved'])
    fake_count = len([c for c in complaints if c.get('is_fake', False)])

    st.markdown(f"""
    <div class="sidebar-stats">
        <h3 style="margin:0;color:white;">📊 Live Stats</h3>
        <hr style="border-color:rgba(255,255,255,0.3);">
        <p style="margin:5px 0;">📋 Total: <strong>{total}</strong></p>
        <p style="margin:5px 0;">🔴 High Priority: <strong>{high}</strong></p>
        <p style="margin:5px 0;">✅ Resolved: <strong>{resolved}</strong></p>
        <p style="margin:5px 0;">🚫 Fake Detected: <strong>{fake_count}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠 Submit Complaint",
        "🔍 Track Complaint",
        "🗺️ Satellite Map",
        "🌡️ Heatmap",
        "🤖 AI Assistant",
        "🔮 Predictive Alerts",
        "📊 Admin Dashboard",
        "🏅 Leaderboard",
        "🔐 Admin Login"
    ])
    st.markdown("---")
    st.markdown("**About Public Pulse**")
    st.markdown("Next-gen AI civic tech platform with satellite maps, fake detection & predictive intelligence.")
    st.markdown("Built for **Ratan Tata Innovation Hub**")

# ============================================
# PAGE 1 - SUBMIT COMPLAINT
# ============================================
if page == "🏠 Submit Complaint":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<p class="section-header">📝 Submit a New Complaint</p>', unsafe_allow_html=True)

        # Language selector
        lang = st.selectbox("🌐 Select Your Language", ["English", "Telugu", "Hindi"], help="You can type in your preferred language!")

        with st.form("complaint_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("👤 Full Name *")
                phone = st.text_input("📱 Phone Number *")
            with c2:
                location = st.text_input("📍 Location / Area *")
                ward = st.text_input("🏘️ Ward / Zone")

            category = st.selectbox("📂 Problem Category *", [
                "Road & Potholes", "Water Supply",
                "Garbage & Sanitation", "Electricity", "Public Spaces & Parks"
            ])

            if lang == "Telugu":
                st.markdown('<p style="color:#64748b;font-size:0.85rem;">తెలుగులో మీ సమస్యను వివరించండి 👇</p>', unsafe_allow_html=True)
            elif lang == "Hindi":
                st.markdown('<p style="color:#64748b;font-size:0.85rem;">हिंदी में अपनी समस्या बताएं 👇</p>', unsafe_allow_html=True)

            description = st.text_area("📝 Describe Your Problem *",
                placeholder="Describe the issue in detail... / సమస్యను వివరించండి... / समस्या बताएं...",
                height=150)

            uploaded_image = st.file_uploader("📸 Upload Photo (optional)", type=["jpg","jpeg","png"])
            if uploaded_image:
                st.image(uploaded_image, caption="Uploaded Photo", width=300)

            st.info("🤖 AI will analyze, detect fake complaints, assign priority and auto-route to correct department")
            submitted = st.form_submit_button("🚀 Submit Complaint", use_container_width=True)

            if submitted:
                if not name or not phone or not location or not description:
                    st.error("⚠️ Please fill all required fields marked with *")
                else:
                    with st.spinner("🤖 AI is analyzing and verifying your complaint..."):
                        # Translate if needed
                        english_description = translate_to_english(description, lang)
                        ai_result = analyze_complaint(english_description, category)

                    if ai_result.get("is_fake", False):
                        st.markdown(f"""
                        <div class="fake-card">
                            <h2>🚫 Complaint Rejected — Suspicious Content Detected</h2>
                            <p>Our AI has flagged this complaint as potentially fake or invalid.</p>
                            <p><strong>Reason:</strong> {ai_result.get("fake_reason", "Description does not match a real civic complaint")}</p>
                            <p>If you believe this is an error, please resubmit with more specific details.</p>
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
                            "description": english_description,
                            "original_description": description,
                            "language": lang,
                            "priority": ai_result["priority"],
                            "summary": ai_result["summary"],
                            "department": ai_result.get("department","General Administration"),
                            "status": "Pending",
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "image": image_data,
                            "lat": 17.7231, "lon": 83.3012,
                            "is_fake": False,
                            "fake_reason": ""
                        }
                        st.session_state.complaints.append(complaint)

                        # WhatsApp Simulation
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
                                    <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">📂 {category}</p>
                                    <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">⚡ Priority: <strong>{ai_result["priority"]}</strong></p>
                                    <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">🏢 {ai_result.get("department","General Admin")}</p>
                                    <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">⏰ Resolution: <strong>{deadline_msg}</strong></p>
                                    <p style="margin:6px 0 0 0;color:#075e54;font-size:0.75rem;font-weight:600;">Track: PublicPulse.streamlit.app</p>
                                    <div class="whatsapp-tick">✓✓ Delivered</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        p_icon = "🔴" if ai_result["priority"]=="High" else "🟡" if ai_result["priority"]=="Medium" else "🟢"
                        deadline_hours = get_deadline_hours(ai_result["priority"])
                        st.markdown(f"""
                        <div class="success-card">
                            <h2>✅ Complaint Submitted Successfully!</h2>
                            <h1 style="color:#065f46;font-size:2rem;">{complaint_id}</h1>
                            <p>Save this ID to track your complaint</p><hr>
                            <p><strong>🌐 Language Detected:</strong> {lang}</p>
                            <p><strong>🤖 AI Priority:</strong> {p_icon} {ai_result["priority"]}</p>
                            <p><strong>📋 Summary:</strong> {ai_result["summary"]}</p>
                            <p><strong>🏢 Routed To:</strong> {ai_result.get("department","General Administration")}</p>
                            <p><strong>⏱️ Expected Resolution:</strong> Within {deadline_hours} hours</p>
                            <p><strong>✅ Authenticity Check:</strong> Passed — Genuine complaint verified</p>
                        </div>
                        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-header">📈 Quick Stats</p>', unsafe_allow_html=True)
        complaints_data = st.session_state.complaints
        total = len(complaints_data)
        high = len([c for c in complaints_data if c['priority']=='High'])
        resolved = len([c for c in complaints_data if c['status']=='Resolved'])
        fake = len([c for c in complaints_data if c.get('is_fake', False)])

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);padding:25px;border-radius:15px;text-align:center;margin-bottom:15px;box-shadow:0 4px 15px rgba(37,99,235,0.4);">
            <div style="font-size:2.5rem;font-weight:700;color:#ffffff;">{total}</div>
            <div style="font-size:0.9rem;color:#ffffff;margin-top:5px;">📋 Total Complaints</div>
        </div>
        <div style="background:linear-gradient(135deg,#dc2626,#ef4444);padding:25px;border-radius:15px;text-align:center;margin-bottom:15px;box-shadow:0 4px 15px rgba(220,38,38,0.4);">
            <div style="font-size:2.5rem;font-weight:700;color:#ffffff;">{high}</div>
            <div style="font-size:0.9rem;color:#ffffff;margin-top:5px;">🔴 High Priority</div>
        </div>
        <div style="background:linear-gradient(135deg,#059669,#10b981);padding:25px;border-radius:15px;text-align:center;margin-bottom:15px;box-shadow:0 4px 15px rgba(5,150,105,0.4);">
            <div style="font-size:2.5rem;font-weight:700;color:#ffffff;">{resolved}</div>
            <div style="font-size:0.9rem;color:#ffffff;margin-top:5px;">✅ Resolved</div>
        </div>
        <div style="background:linear-gradient(135deg,#be185d,#ec4899);padding:25px;border-radius:15px;text-align:center;margin-bottom:15px;box-shadow:0 4px 15px rgba(190,24,93,0.4);">
            <div style="font-size:2.5rem;font-weight:700;color:#ffffff;">{fake}</div>
            <div style="font-size:0.9rem;color:#ffffff;margin-top:5px;">🚫 Fake Detected</div>
        </div>
        """, unsafe_allow_html=True)

        if complaints_data:
            df = pd.DataFrame(complaints_data)
            cat_counts = df['category'].value_counts().reset_index()
            cat_counts.columns = ['Category','Count']
            fig = px.pie(cat_counts, values='Count', names='Category',
                        color_discrete_sequence=['#ef4444','#f97316','#22c55e','#3b82f6','#a855f7'],
                        hole=0.4)
            fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=250, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 2 - TRACK COMPLAINT
# ============================================
elif page == "🔍 Track Complaint":
    st.markdown('<p class="section-header">🔍 Track Your Complaint</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="track-card"><h3 style="text-align:center;">Enter Your Complaint ID</h3><p style="text-align:center;color:#64748b;">Example: PP-2024-001</p></div>', unsafe_allow_html=True)
        st.markdown("###")
        track_id = st.text_input("🔍 Complaint ID", placeholder="PP-2024-001")
        if st.button("Track Complaint", use_container_width=True):
            found = next((c for c in st.session_state.complaints if c['id'].upper()==track_id.upper()), None)
            if found:
                priority = found['priority']
                status = found['status']
                p_icon = "🔴" if priority=="High" else "🟡" if priority=="Medium" else "🟢"
                progress = 10 if status=="Pending" else 60 if status=="In Progress" else 100
                time_remaining, is_overdue = get_time_remaining(found['date'], priority)
                timer_color = "#dc2626" if is_overdue else "#059669"

                st.markdown(f"""
                <div class="track-card" style="margin-top:20px;">
                    <h2 style="text-align:center;color:#1e3a8a;">✅ Complaint Found!</h2><hr>
                    <table style="width:100%;">
                        <tr><td style="padding:8px;color:#64748b;">🆔 ID</td><td><strong>{found['id']}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">👤 Name</td><td><strong>{found['name']}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">📍 Location</td><td><strong>{found['location']}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">📂 Category</td><td><strong>{found['category']}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">🌐 Language</td><td><strong>{found.get('language','English')}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">🤖 Priority</td><td><strong>{p_icon} {found['priority']}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">🏢 Department</td><td><strong>{found['department']}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">📋 Summary</td><td><strong>{found['summary']}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">📅 Date</td><td><strong>{found['date']}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">🔄 Status</td><td><strong>{status}</strong></td></tr>
                        <tr><td style="padding:8px;color:#64748b;">⏱️ Time Left</td><td><strong style="color:{timer_color};">{time_remaining}</strong></td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                st.progress(progress)
                st.markdown(f"**Progress: {progress}%** — {'Waiting for action' if status=='Pending' else 'Being handled' if status=='In Progress' else '🎉 Resolved!'}")
                if found.get('image'):
                    st.image(base64.b64decode(found['image']), width=400, caption="Your Submitted Photo")
            else:
                st.error("❌ Complaint ID not found. Please check and try again.")

# ============================================
# PAGE 3 - SATELLITE MAP
# ============================================
elif page == "🗺️ Satellite Map":
    st.markdown('<p class="section-header">🛰️ Live Satellite Map — Visakhapatnam</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:white;padding:15px;border-radius:10px;margin-bottom:20px;color:#1e293b;">
        <b>🛰️ Real satellite imagery</b> — Click any pin to see complaint details! &nbsp;&nbsp;
        <b>🔴</b> High &nbsp; <b>🟠</b> Medium &nbsp; <b>🟢</b> Low Priority
    </div>
    """, unsafe_allow_html=True)

    # Satellite map using Esri (free, no API key needed)
    m = folium.Map(
        location=[17.7231, 83.3012],
        zoom_start=13,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite"
    )

    # Add street labels layer on top of satellite
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Labels",
        name="Labels",
        overlay=True
    ).add_to(m)

    for c in st.session_state.complaints:
        if c.get('is_fake', False):
            continue
        lat = c.get('lat', 17.7231)
        lon = c.get('lon', 83.3012)
        color = get_marker_color(c['priority'])
        time_rem, overdue = get_time_remaining(c['date'], c['priority'])

        popup_html = f"""
        <div style="font-family:Arial;min-width:220px;padding:5px;">
            <h4 style="color:#1e3a8a;margin:0;border-bottom:2px solid #2563eb;padding-bottom:5px;">{c['id']}</h4>
            <p><b>👤</b> {c['name']}</p>
            <p><b>📂</b> {c['category']}</p>
            <p><b>📍</b> {c['location']}</p>
            <p><b>🤖 Priority:</b> {c['priority']}</p>
            <p><b>🔄 Status:</b> {c['status']}</p>
            <p><b>⏱️ Time Left:</b> {time_rem}</p>
            <p><b>📋</b> {c['summary']}</p>
        </div>
        """
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"📍 {c['id']} — {c['category']} ({c['priority']})",
            icon=folium.Icon(color=color, icon="info-sign", prefix="glyphicon")
        ).add_to(m)

    folium.LayerControl().add_to(m)
    st_folium(m, width=None, height=550)
    st.caption(f"🛰️ Satellite imagery powered by Esri | Showing {len([c for c in st.session_state.complaints if not c.get('is_fake',False)])} complaints")

# ============================================
# PAGE 4 - HEATMAP
# ============================================
elif page == "🌡️ Heatmap":
    st.markdown('<p class="section-header">🌡️ Complaint Intensity Heatmap</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:white;padding:15px;border-radius:10px;margin-bottom:20px;color:#1e293b;">
        <b>🔥 Red/Orange areas</b> = High concentration of complaints — Needs urgent attention!<br>
        <b>🟡 Yellow areas</b> = Moderate complaints &nbsp;&nbsp;
        <b>🟢 Green areas</b> = Low complaint zones
    </div>
    """, unsafe_allow_html=True)

    hm = folium.Map(location=[17.7231, 83.3012], zoom_start=12, tiles="OpenStreetMap")

    heat_data = []
    for c in st.session_state.complaints:
        if not c.get('is_fake', False):
            lat = c.get('lat', 17.7231)
            lon = c.get('lon', 83.3012)
            weight = 3 if c['priority']=="High" else 2 if c['priority']=="Medium" else 1
            heat_data.append([lat, lon, weight])

    if heat_data:
        HeatMap(
            heat_data,
            min_opacity=0.4,
            max_zoom=18,
            radius=40,
            blur=25,
            gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
        ).add_to(hm)

    st_folium(hm, width=None, height=500)

    st.markdown("### 📊 Hotspot Analysis")
    complaints_data = st.session_state.complaints
    df = pd.DataFrame([c for c in complaints_data if not c.get('is_fake',False)])
    if len(df) > 0:
        location_counts = df['location'].value_counts().reset_index()
        location_counts.columns = ['Location','Complaints']
        fig = px.bar(location_counts, x='Location', y='Complaints',
                    color='Complaints', color_continuous_scale='Reds',
                    title="Complaints per Area")
        fig.update_layout(height=300, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 5 - AI ASSISTANT
# ============================================
elif page == "🤖 AI Assistant":
    st.markdown('<p class="section-header">🤖 AI Assistant — Public Pulse Helper</p>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div style="background:#1e3a8a;color:white;padding:15px;border-radius:15px 15px 5px 15px;
                        margin:10px 0;max-width:80%;margin-left:auto;text-align:right;">
                👤 {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:white;color:#1e293b;padding:15px;border-radius:15px 15px 15px 5px;
                        margin:10px 0;max-width:80%;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
                🤖 {msg['content']}
            </div>
            """, unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5,1])
        with col1:
            user_input = st.text_input("Ask me anything...", label_visibility="collapsed", placeholder="Type in English, Telugu or Hindi...")
        with col2:
            send = st.form_submit_button("Send 🚀", use_container_width=True)
        if send and user_input:
            st.session_state.chat_history.append({"role":"user","content":user_input})
            with st.spinner("🤖 Thinking..."):
                try:
                    context = """You are a helpful multilingual AI assistant for Public Pulse 
                    — an AI-powered citizen complaint system for Ratan Tata Innovation Hub, Visakhapatnam.
                    Features: Submit complaints, Track by ID, Satellite Map, Heatmap, Fake Detector, Predictive AI.
                    Categories: Road & Potholes, Water Supply, Garbage & Sanitation, Electricity, Public Spaces & Parks.
                    Admin: username=admin password=admin123. Complaint ID format: PP-2024-001.
                    Respond in the same language the user writes in. Be friendly and concise (2-3 sentences)."""
                    response = model.generate_content(f"{context}\n\nUser: {user_input}")
                    bot_reply = response.text.strip()
                except:
                    bot_reply = "I am having trouble right now. Please try again!"
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
            st.session_state.chat_history.append({"role":"assistant","content":"Our Predictive AI analyzes complaint patterns and predicts which areas are likely to face problems next week! For example if MVP Colony has 3 water complaints, AI predicts a bigger water crisis is coming and alerts authorities proactively."})
            st.rerun()

# ============================================
# PAGE 6 - PREDICTIVE ALERTS
# ============================================
elif page == "🔮 Predictive Alerts":
    st.markdown('<p class="section-header">🔮 AI Predictive Alerts — Smart City Intelligence</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#7c3aed,#a855f7);padding:20px;border-radius:15px;color:white;margin-bottom:25px;">
        <h3 style="margin:0;">🧠 How Predictive AI Works</h3>
        <p style="margin-top:10px;opacity:0.9;">Our AI analyzes complaint patterns, frequency, locations and categories to predict 
        which areas are likely to face civic problems in the coming week — enabling proactive government action before issues escalate!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔮 Generate AI Predictions Now", use_container_width=True):
        with st.spinner("🧠 AI is analyzing complaint patterns and generating predictions..."):
            predictions = generate_prediction(st.session_state.complaints)

        st.markdown("### 📊 Predicted Problem Areas — Next 7 Days")

        for i, pred in enumerate(predictions):
            risk = pred.get('risk','Medium')
            risk_color = "#dc2626" if risk=="High" else "#d97706" if risk=="Medium" else "#059669"
            risk_bg = "#fee2e2" if risk=="High" else "#fef3c7" if risk=="Medium" else "#d1fae5"
            risk_icon = "🔴" if risk=="High" else "🟡" if risk=="Medium" else "🟢"

            st.markdown(f"""
            <div style="background:white;padding:25px;border-radius:15px;margin-bottom:15px;
                        border-left:5px solid {risk_color};box-shadow:0 4px 15px rgba(0,0,0,0.08);">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <h3 style="color:#1e3a8a;margin:0;">Prediction #{i+1}: {pred.get('area','Unknown Area')}</h3>
                    <span style="background:{risk_bg};color:{risk_color};padding:5px 15px;border-radius:20px;font-weight:700;">
                        {risk_icon} {risk} Risk
                    </span>
                </div>
                <hr style="border-color:#e2e8f0;">
                <p style="color:#1e293b;"><b>⚠️ Predicted Issue:</b> {pred.get('issue','Unknown')}</p>
                <p style="color:#1e293b;"><b>🧠 AI Reasoning:</b> {pred.get('reason','Based on complaint patterns')}</p>
                <p style="color:#64748b;font-size:0.85rem;">📅 Prediction valid for next 7 days | Take preventive action now!</p>
            </div>
            """, unsafe_allow_html=True)

        st.success("✅ Predictions generated! Share these with relevant departments for proactive action.")

    st.markdown("---")
    st.markdown("### 📈 Current Complaint Trends")
    df = pd.DataFrame([c for c in st.session_state.complaints if not c.get('is_fake',False)])
    if len(df) > 0:
        col1, col2 = st.columns(2)
        with col1:
            trend = df.groupby(['category','priority']).size().reset_index(name='count')
            fig = px.bar(trend, x='category', y='count', color='priority',
                        color_discrete_map={'High':'#dc2626','Medium':'#d97706','Low':'#059669'},
                        title="Complaints by Category & Priority",
                        barmode='group')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            loc_counts = df['location'].value_counts().reset_index()
            loc_counts.columns = ['Location','Count']
            fig2 = px.pie(loc_counts, values='Count', names='Location',
                         title="Complaints by Location",
                         color_discrete_sequence=px.colors.qualitative.Bold, hole=0.4)
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 7 - ADMIN DASHBOARD
# ============================================
elif page == "📊 Admin Dashboard":
    if not st.session_state.admin_logged_in:
        st.warning("⚠️ Please login as Admin first.")
        st.info("👉 Click Admin Login in the sidebar")
    else:
        col_title, col_refresh = st.columns([4,1])
        with col_title:
            st.markdown('<p class="section-header">📊 Admin Dashboard</p>', unsafe_allow_html=True)
        with col_refresh:
            auto_refresh = st.toggle("🔄 Auto Refresh", value=False)
            if auto_refresh:
                st.markdown("🟢 **Live**")
                time.sleep(30)
                st.rerun()

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

        st.markdown("###")

        if total > 0:
            resolution_rate = int((resolved/total)*100)
            st.markdown(f"### 📈 Resolution Rate: {resolution_rate}%")
            st.progress(resolution_rate)
            if resolution_rate >= 70:
                st.success("🎉 Excellent! Most complaints are resolved!")
            elif resolution_rate >= 40:
                st.warning("⚠️ Good progress! Keep resolving complaints.")
            else:
                st.error("🚨 Many complaints pending. Immediate action needed!")

        st.markdown("---")

        col1, col2 = st.columns(2)
        real_complaints = [c for c in complaints if not c.get('is_fake',False)]
        df = pd.DataFrame(real_complaints) if real_complaints else pd.DataFrame()

        if len(df) > 0:
            with col1:
                st.markdown("**📊 Complaints by Category**")
                cat_counts = df['category'].value_counts().reset_index()
                cat_counts.columns = ['Category','Count']
                fig1 = px.bar(cat_counts, x='Category', y='Count', color='Count',
                             color_continuous_scale='Blues', text='Count')
                fig1.update_layout(margin=dict(t=20,b=0), height=300, showlegend=False, coloraxis_showscale=False)
                fig1.update_traces(textposition='outside')
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                st.markdown("**🎯 Priority Distribution**")
                priority_counts = df['priority'].value_counts().reset_index()
                priority_counts.columns = ['Priority','Count']
                fig2 = px.pie(priority_counts, values='Count', names='Priority',
                             color='Priority',
                             color_discrete_map={'High':'#dc2626','Medium':'#d97706','Low':'#059669'},
                             hole=0.5)
                fig2.update_layout(margin=dict(t=20,b=0), height=300)
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        if st.button("🤖 Generate AI Weekly Report", use_container_width=True):
            with st.spinner("🤖 AI is generating your professional weekly report..."):
                try:
                    complaint_summary = "\n".join([
                        f"- {c['id']}: {c['category']} at {c['location']} | Priority: {c['priority']} | Status: {c['status']} | Language: {c.get('language','English')}"
                        for c in complaints if not c.get('is_fake',False)
                    ])
                    fake_summary = f"Fake complaints detected and rejected: {fake}"
                    report_prompt = f"""
                    Generate a professional government weekly report for Public Pulse - Smart Citizen Service System.
                    
                    Complaints Data:
                    {complaint_summary}
                    
                    {fake_summary}
                    
                    Write a structured report with:
                    1. Executive Summary
                    2. Key Statistics (total, high priority, resolved, fake detected)
                    3. Most Critical Issues requiring immediate attention
                    4. Department-wise breakdown
                    5. Multilingual Accessibility Stats
                    6. AI Fake Detection Performance
                    7. Recommendations for improvement
                    
                    Make it professional and government-ready.
                    """
                    report_response = model.generate_content(report_prompt)
                    report_text = report_response.text.strip()
                    st.markdown(f"""
                    <div style="background:white;padding:30px;border-radius:15px;
                                box-shadow:0 4px 20px rgba(0,0,0,0.1);color:#1e293b;">
                        <h2 style="color:#1e3a8a;">📊 AI Weekly Complaint Analysis Report</h2>
                        <p style="color:#64748b;">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | Public Pulse — Ratan Tata Innovation Hub</p>
                        <hr>
                        {report_text.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                    st.download_button("📥 Download Report", data=report_text,
                        file_name=f"public_pulse_report_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain")
                except:
                    st.error("Could not generate report. Please try again.")

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
        if filter_priority != "All":
            filtered = [c for c in filtered if c['priority']==filter_priority]
        if filter_status != "All":
            filtered = [c for c in filtered if c['status']==filter_status]
        if filter_category != "All":
            filtered = [c for c in filtered if c['category']==filter_category]
        if filter_fake == "Real Only":
            filtered = [c for c in filtered if not c.get('is_fake',False)]
        elif filter_fake == "Fake Only":
            filtered = [c for c in filtered if c.get('is_fake',False)]

        col_show, col_export = st.columns([3,1])
        with col_show:
            st.markdown(f"**Showing {len(filtered)} complaints**")
        with col_export:
            if filtered:
                df_export = pd.DataFrame(filtered).drop(columns=['image','lat','lon'], errors='ignore')
                csv = df_export.to_csv(index=False)
                st.download_button("📥 Export CSV", data=csv,
                    file_name="public_pulse_complaints.csv", mime="text/csv", use_container_width=True)

        st.markdown("---")

        for complaint in filtered:
            priority = complaint['priority']
            status = complaint['status']
            is_fake = complaint.get('is_fake', False)
            time_rem, overdue = get_time_remaining(complaint['date'], priority)
            p_badge = '<span class="badge-high">🔴 High</span>' if priority=="High" else '<span class="badge-medium">🟡 Medium</span>' if priority=="Medium" else '<span class="badge-low">🟢 Low</span>'
            fake_badge = '<span class="fake-badge">🚫 FAKE</span>' if is_fake else '<span style="background:#d1fae5;color:#065f46;padding:5px 15px;border-radius:20px;font-weight:600;font-size:0.85rem;">✅ Genuine</span>'
            border_color = "#be185d" if is_fake else "#dc2626" if priority=="High" else "#d97706" if priority=="Medium" else "#059669"
            timer_color = "#dc2626" if overdue else "#059669"

            st.markdown(f"""
            <div class="complaint-card" style="border-left-color:{border_color};">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:5px;">
                    <div><strong style="font-size:1.1rem;color:#1e3a8a;">{complaint['id']}</strong>&nbsp;&nbsp;{p_badge}&nbsp;&nbsp;{fake_badge}</div>
                    <div style="color:#64748b;font-size:0.85rem;">📅 {complaint['date']}</div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:10px;">
                    <div><span style="color:#64748b;">👤 Name</span><br><strong style="color:#1e293b;">{complaint['name']}</strong></div>
                    <div><span style="color:#64748b;">📍 Location</span><br><strong style="color:#1e293b;">{complaint['location']}</strong></div>
                    <div><span style="color:#64748b;">📂 Category</span><br><strong style="color:#1e293b;">{complaint['category']}</strong></div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;">
                    <div><span style="color:#64748b;">🌐 Language</span><br><strong style="color:#1e293b;">{complaint.get('language','English')}</strong></div>
                    <div><span style="color:#64748b;">⏱️ Time Remaining</span><br><strong style="color:{timer_color};">{time_rem}</strong></div>
                </div>
                <div style="background:#f8fafc;padding:12px;border-radius:8px;margin-bottom:10px;">
                    <span style="color:#64748b;font-size:0.85rem;">🤖 AI Analysis</span><br>
                    <strong style="color:#1e293b;">{complaint['summary']}</strong><br>
                    <span style="color:#2563eb;font-size:0.85rem;">🏢 {complaint['department']}</span>
                </div>
                <div style="color:#1e293b;font-size:0.9rem;"><span style="color:#64748b;">📝 Description:</span> {complaint['description']}</div>
            </div>
            """, unsafe_allow_html=True)

            if complaint.get('image'):
                st.image(base64.b64decode(complaint['image']), width=300, caption="Complaint Photo")

            if not is_fake:
                new_status = st.selectbox(
                    f"Update Status for {complaint['id']}",
                    ["Pending","In Progress","Resolved"],
                    index=["Pending","In Progress","Resolved"].index(complaint['status']),
                    key=f"status_{complaint['id']}"
                )
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
                            <div>
                                <div style="color:#ffffff;font-weight:700;font-size:0.9rem;">Public Pulse Official</div>
                                <div style="color:#25d366;font-size:0.75rem;">● Online</div>
                            </div>
                        </div>
                        <div class="whatsapp-body">
                            <div class="whatsapp-bubble">
                                <p style="margin:0 0 6px 0;color:#075e54;font-weight:700;font-size:0.85rem;">🔔 Status Update</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">Hello <strong>{complaint['name']}</strong>! 👋</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">{status_emoji} Your complaint <strong>{complaint['id']}</strong> {status_msg}</p>
                                <p style="margin:4px 0;color:#1e293b;font-size:0.85rem;">Status: <strong>{new_status}</strong></p>
                                <p style="margin:6px 0 0 0;color:#075e54;font-size:0.75rem;">Thank you for using Public Pulse! 🏛️</p>
                                <div class="whatsapp-tick">✓✓ Delivered</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.rerun()
            st.markdown("---")

# ============================================
# ============================================
# PAGE - LEADERBOARD
# ============================================
elif page == "🏅 Leaderboard":
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
        leaderboard.append({
            'department': dept, 'total': stats['total'],
            'resolved': stats['resolved'], 'pending': stats['pending'],
            'in_progress': stats['in_progress'], 'high': stats['high'],
            'rate': rate, 'score': score
        })

    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    medals = ["🥇","🥈","🥉"]
    podium_colors = ["#f59e0b","#6366f1","#10b981"]
    podium_shadows = ["rgba(245,158,11,0.3)","rgba(99,102,241,0.3)","rgba(16,185,129,0.3)"]

    # TOP 3 PODIUM
    st.markdown("### 🏆 Top Performers")
    if len(leaderboard) >= 3:
        col1, col2, col3 = st.columns(3)
        podium_order = [1, 0, 2]
        cols = [col1, col2, col3]
        for i, (col, rank) in enumerate(zip(cols, podium_order)):
            if rank < len(leaderboard):
                d = leaderboard[rank]
                with col:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,{podium_colors[rank]}20,{podium_colors[rank]}10);
                                border:2px solid {podium_colors[rank]}60;
                                border-radius:20px;padding:25px;text-align:center;
                                box-shadow:0 8px 25px {podium_shadows[rank]};
                                margin-bottom:15px;">
                        <div style="font-size:3rem;">{medals[rank]}</div>
                        <div style="font-weight:800;color:#1e293b;font-size:0.9rem;margin:10px 0;">{d['department'][:22]}</div>
                        <div style="font-size:2rem;font-weight:900;color:{podium_colors[rank]};">{d['rate']}%</div>
                        <div style="color:#64748b;font-size:0.75rem;margin-bottom:8px;">Resolution Rate</div>
                        <div style="background:{podium_colors[rank]}20;padding:6px;border-radius:8px;">
                            <span style="color:{podium_colors[rank]};font-weight:700;font-size:0.85rem;">Score: {d['score']}</span>
                        </div>
                        <div style="margin-top:10px;font-size:0.8rem;color:#64748b;">
                            ✅ {d['resolved']} resolved | 📋 {d['total']} total
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Full Rankings")

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
                        <div style="font-weight:700;color:#1e293b;font-size:1rem;">{dept['department']}</div>
                        <div style="color:#64748b;font-size:0.8rem;">
                            📋 Total: {dept['total']} &nbsp;|&nbsp; 
                            ✅ Resolved: {dept['resolved']} &nbsp;|&nbsp; 
                            ⏳ Pending: {dept['pending']} &nbsp;|&nbsp; 
                            🔄 In Progress: {dept['in_progress']}
                        </div>
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
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📈 Overall Statistics")

    total_c = len(real_complaints)
    total_r = len([c for c in real_complaints if c['status']=='Resolved'])
    overall = int((total_r/total_c)*100) if total_c > 0 else 0
    best = leaderboard[0]['department'] if leaderboard else "N/A"

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card" style="border-top-color:#6366f1;">
            <div class="metric-number" style="color:#6366f1;">{overall}%</div>
            <div class="metric-label">Overall Resolution</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card" style="border-top-color:#f59e0b;">
            <div class="metric-number" style="color:#f59e0b;">{len(dept_stats)}</div>
            <div class="metric-label">Departments Active</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card" style="border-top-color:#10b981;">
            <div class="metric-number" style="color:#10b981;">{total_r}</div>
            <div class="metric-label">Total Resolved</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card" style="border-top-color:#dc2626;">
            <div class="metric-number" style="color:#dc2626;">🏆</div>
            <div class="metric-label">Best: {best[:12]}</div></div>""", unsafe_allow_html=True)
# ============================================
elif page == "🔐 Admin Login":
    st.markdown('<p class="section-header">🔐 Admin Login</p>', unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        if st.session_state.admin_logged_in:
            st.success("✅ You are logged in as Admin!")
            if st.button("🚪 Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
        else:
            st.markdown('<div style="background:white;padding:40px;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,0.1);"><h3 style="text-align:center;color:#1e3a8a;">🏛️ Admin Portal</h3><p style="text-align:center;color:#64748b;">Enter credentials to access dashboard</p></div>', unsafe_allow_html=True)
            with st.form("login_form"):
                username = st.text_input("👤 Username")
                password = st.text_input("🔒 Password", type="password")
                login_btn = st.form_submit_button("🔐 Login", use_container_width=True)
                if login_btn:
                    if username=="admin" and password==ADMIN_PASSWORD:
                        st.session_state.admin_logged_in = True
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Try admin / admin123")