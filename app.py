import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# CONFIGURATION
# ============================================
GEMINI_API_KEY = "AIzaSyBoE86E-3zhGrYXd-s6RKCkJSYuK_-74sE"
ADMIN_PASSWORD = "admin123"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Public Pulse | Smart Citizen Services",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROFESSIONAL CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    [data-testid="stFileUploader"] * { color: #ffffff !important; }
    [data-testid="stFileUploaderDropzone"] * { color: #ffffff !important; }
    [data-testid="stFileUploaderDropzone"] { background-color: #1e293b !important; }
    
    .stSelectbox div[data-baseweb="select"] div { color: #ffffff !important; background-color: #1e293b !important; }
    .stSelectbox div[data-baseweb="select"] span { color: #ffffff !important; }
    .stSelectbox svg { fill: #000000 !important; }

    
    [data-baseweb="select"] li {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    [data-baseweb="option"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    .main { background-color: #f0f4f8; }
    
    .hero-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #0ea5e9 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(37, 99, 235, 0.3);
    }
    
    .hero-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .hero-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 10px;
    }

    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-top: 4px solid #2563eb;
        transition: transform 0.2s;
    }
    
    .metric-card:hover { transform: translateY(-5px); }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #ffffff !important;
        margin-top: 5px;
        font-weight: 500;
    }

    .complaint-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border-left: 5px solid #2563eb;
        transition: transform 0.2s;
        color: #1e293b !important;
    }
    
    .complaint-card:hover { transform: translateX(5px); }
.complaint-card * { color: #000000 !important; }
.login-card * { color: #000000 !important; }
div[data-testid="stForm"] * { color: #000000 !important; }

    .badge-high {
        background: #fee2e2;
        color: #dc2626;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .badge-medium {
        background: #fef3c7;
        color: #d97706;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .badge-low {
        background: #d1fae5;
        color: #059669;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .badge-pending {
        background: #e0e7ff;
        color: #4338ca;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .badge-progress {
        background: #fef3c7;
        color: #92400e;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .badge-resolved {
        background: #d1fae5;
        color: #065f46;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .success-card {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #10b981;
        text-align: center;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.2);
    }

    .login-card {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: auto;
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 3px solid #2563eb;
    }

    .stButton>button {
        background: #1e3a8a !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #2563eb !important;
        color: #ffffff !important;
    }
    
    .stFormSubmitButton>button {
        background: #1e3a8a !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb, #0ea5e9);
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(37, 99, 235, 0.4);
    }

    .sidebar-stats {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }

    div[data-testid="stForm"] {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }

    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    .stSelectbox>div>div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    
    .stSelectbox>div>div>div {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    
    .stSelectbox span {
        color: #ffffff !important;
    }
    
    [data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    
    [data-baseweb="popover"] * {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    [data-testid="stFileUploader"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
    }
    
    [data-testid="stFileUploaderDropzone"] {
        background-color: #1e293b !important;
        border-color: #475569 !important;
    }
    .stTextInput>div>div>input {
        border-radius: 10px !important;
        border: 2px solid #1e3a8a !important;
        color: #000000 !important;
        background-color: #ffffff !important;
        caret-color: #000000 !important;
    }
    
    div[data-testid="stForm"] input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    div[data-testid="stForm"] textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #1e3a8a !important;
        color: #000000 !important;
        background-color: #ffffff !important;
    }
input, textarea, [data-baseweb="select"] *, [data-testid="stFileUploader"] * {
        color: #ffffff !important;
    }
    
    [data-baseweb="select"] * { color: #ffffff !important; background-color: #1e293b !important; }
    [data-testid="stFileUploaderDropzone"] { background-color: #1e293b !important; }
    [data-testid="stFileUploaderDropzone"] p { color: #ffffff !important; }
    [data-testid="stFileUploaderDropzone"] span { color: #ffffff !important; }
    [data-testid="stFileUploaderDropzone"] small { color: #ffffff !important; }
    [data-testid="stFileUploaderDropzone"] button { color: #ffffff !important; }

    [data-testid="stFileUploaderDropzone"] * { color: #ffffff !important; }
section[data-testid="stFileUploaderDropzone"] p,
    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] small,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] span {
        color: #ffffff !important;
    }
[data-testid="stPasswordInput"] button {
        color: #ffffff !important;
        background-color: #1e293b !important;
        border: none !important;
        border-radius: 5px !important;
    }
    
    [data-testid="stPasswordInput"] button svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }
    
    [data-testid="stPasswordInput"] svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
        color: #ffffff !important;
    }

""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if 'complaints' not in st.session_state:
    st.session_state.complaints = [
        {
            "id": "PP-2024-001",
            "name": "Ravi Kumar",
            "phone": "9876543210",
            "location": "Maddilapalem, Visakhapatnam",
            "ward": "Ward 5",
            "category": "Road & Potholes",
            "description": "Large pothole near school zone causing accidents daily",
            "priority": "High",
            "summary": "Dangerous pothole near school requiring urgent repair",
            "department": "Roads & Infrastructure",
            "status": "In Progress",
            "date": "2024-02-20 09:15"
        },
        {
            "id": "PP-2024-002",
            "name": "Priya Sharma",
            "phone": "8765432109",
            "location": "MVP Colony, Visakhapatnam",
            "ward": "Ward 12",
            "category": "Water Supply",
            "description": "No water supply for 3 days in our area",
            "priority": "High",
            "summary": "Critical water supply disruption affecting entire colony",
            "department": "Water & Sanitation Board",
            "status": "Pending",
            "date": "2024-02-20 11:30"
        },
        {
            "id": "PP-2024-003",
            "name": "Suresh Babu",
            "phone": "7654321098",
            "location": "Gajuwaka, Visakhapatnam",
            "ward": "Ward 8",
            "category": "Garbage & Sanitation",
            "description": "Garbage not collected for a week, causing smell",
            "priority": "Medium",
            "summary": "Weekly garbage collection missed causing sanitation issues",
            "department": "Sanitation Department",
            "status": "Resolved",
            "date": "2024-02-19 14:00"
        },
        {
            "id": "PP-2024-004",
            "name": "Lakshmi Devi",
            "phone": "6543210987",
            "location": "Dwaraka Nagar, Visakhapatnam",
            "ward": "Ward 3",
            "category": "Electricity",
            "description": "Street lights not working for 2 weeks",
            "priority": "Medium",
            "summary": "Street light outage creating safety concerns at night",
            "department": "APEPDCL",
            "status": "Pending",
            "date": "2024-02-19 16:45"
        },
        {
            "id": "PP-2024-005",
            "name": "Venkat Rao",
            "phone": "5432109876",
            "location": "Rushikonda, Visakhapatnam",
            "ward": "Ward 15",
            "category": "Public Spaces & Parks",
            "description": "Park benches broken, children getting hurt",
            "priority": "Low",
            "summary": "Broken park infrastructure needs maintenance",
            "department": "Parks & Recreation",
            "status": "Pending",
            "date": "2024-02-18 10:00"
        }
    ]

if 'complaint_counter' not in st.session_state:
    st.session_state.complaint_counter = 6

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# ============================================
# GEMINI AI FUNCTION
# ============================================
def analyze_complaint(description, category):
    try:
        prompt = f"""
        You are a government complaint analysis AI.
        Analyze this citizen complaint and respond ONLY with a JSON object.
        
        Category: {category}
        Description: {description}
        
        Respond with exactly this JSON format:
        {{
            "priority": "High or Medium or Low",
            "summary": "One line summary of the complaint",
            "department": "Which government department should handle this"
        }}
        
        Priority rules:
        - High: Safety risk, health hazard, urgent public issue
        - Medium: Causing inconvenience, needs attention soon  
        - Low: Minor issue, can be addressed later
        
        Respond with ONLY the JSON, no extra text.
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text.strip())
        return result
    except Exception as e:
        return {
            "priority": "Medium",
            "summary": "Complaint received and logged successfully",
            "department": "General Administration"
        }

# ============================================
# HERO HEADER
# ============================================
st.markdown("""
<div class="hero-header">
    <h1>🏛️ Public Pulse</h1>
    <p>AI-Powered Smart Citizen Service Oversight System | Ratan Tata Innovation Hub</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    complaints = st.session_state.complaints
    total = len(complaints)
    high = len([c for c in complaints if c['priority'] == 'High'])
    resolved = len([c for c in complaints if c['status'] == 'Resolved'])

    st.markdown(f"""
    <div class="sidebar-stats">
        <h3 style="margin:0; color:white;">📊 Live Stats</h3>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <p style="margin:5px 0;">📋 Total Complaints: <strong>{total}</strong></p>
        <p style="margin:5px 0;">🔴 High Priority: <strong>{high}</strong></p>
        <p style="margin:5px 0;">✅ Resolved: <strong>{resolved}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠 Submit Complaint", "🔍 Track Complaint", "📊 Admin Dashboard", "🔐 Admin Login"]
    )

    st.markdown("---")
    st.markdown("**About Public Pulse**")
    st.markdown("An AI-powered civic tech platform that connects citizens with government services.")
    st.markdown("Built for **Ratan Tata Innovation Hub**")

# ============================================
# PAGE 1 - SUBMIT COMPLAINT
# ============================================
if page == "🏠 Submit Complaint":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<p class="section-header">📝 Submit a New Complaint</p>', unsafe_allow_html=True)

        with st.form("complaint_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("👤 Full Name *")
                phone = st.text_input("📱 Phone Number *")
            with c2:
                location = st.text_input("📍 Location / Area *")
                ward = st.text_input("🏘️ Ward / Zone")

            category = st.selectbox("📂 Problem Category *", [
                "Road & Potholes",
                "Water Supply",
                "Garbage & Sanitation",
                "Electricity",
                "Public Spaces & Parks"
            ])

            description = st.text_area(
                "📝 Describe Your Problem in Detail *",
                placeholder="Example: There is a large pothole near the bus stop on Main Road. It has caused 3 accidents this week and is very dangerous at night...",
                height=150
            )

            
            st.markdown('<p style="color:#ffffff; font-weight:600;">📸 Upload Photo (optional)</p>', unsafe_allow_html=True)
            uploaded_image = st.file_uploader(
                "",
                type=["jpg", "jpeg", "png"],
                help="Upload a photo of the problem to help authorities understand better",
                label_visibility="collapsed"
            )

            if uploaded_image:
             st.image(uploaded_image, caption="Uploaded Photo", width=300)

            st.info("🤖 Our AI will automatically analyze your complaint, assign priority, and route it to the correct department.")

            submitted = st.form_submit_button("🚀 Submit Complaint", use_container_width=True)

            if submitted:
                if not name or not phone or not location or not description:
                    st.error("⚠️ Please fill all required fields marked with *")
                else:
                    with st.spinner("🤖 AI is analyzing your complaint..."):
                        ai_result = analyze_complaint(description, category)

                    complaint_id = f"PP-2024-{str(st.session_state.complaint_counter).zfill(3)}"
                    st.session_state.complaint_counter += 1

                    image_data = None
                    if uploaded_image:
                        import base64
                        image_data = base64.b64encode(uploaded_image.read()).decode()

                    complaint = {
                        "id": complaint_id,
                        "name": name,
                        "phone": phone,
                        "location": location,
                        "ward": ward,
                        "category": category,
                        "description": description,
                        "priority": ai_result["priority"],
                        "summary": ai_result["summary"],
                        "department": ai_result.get("department", "General Administration"),
                        "status": "Pending",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "image": image_data
                    }

                    st.session_state.complaints.append(complaint)

                    priority_color = "🔴" if ai_result["priority"] == "High" else "🟡" if ai_result["priority"] == "Medium" else "🟢"

                    st.markdown(f"""
                    <div class="success-card">
                        <h2>✅ Complaint Submitted Successfully!</h2>
                        <h1 style="color:#065f46; font-size:2rem;">{complaint_id}</h1>
                        <p style="color:#374151;">Save this ID to track your complaint</p>
                        <hr>
                        <p><strong>🤖 AI Priority:</strong> {priority_color} {ai_result["priority"]}</p>
                        <p><strong>📋 AI Summary:</strong> {ai_result["summary"]}</p>
                        <p><strong>🏢 Routed To:</strong> {ai_result.get("department", "General Administration")}</p>
                        <p style="color:#6b7280; font-size:0.85rem;">Expected response within 24-72 hours based on priority</p>
                    </div>
                    """, unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-header">📈 Quick Stats</p>', unsafe_allow_html=True)

        complaints = st.session_state.complaints
        total = len(complaints)
        high = len([c for c in complaints if c['priority'] == 'High'])
        medium = len([c for c in complaints if c['priority'] == 'Medium'])
        low = len([c for c in complaints if c['priority'] == 'Low'])
        resolved = len([c for c in complaints if c['status'] == 'Resolved'])

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e3a8a, #2563eb); padding:25px; 
                    border-radius:15px; text-align:center; margin-bottom:15px;
                    box-shadow: 0 4px 15px rgba(37,99,235,0.4);">
            <div style="font-size:2.5rem; font-weight:700; color:#ffffff;">{total}</div>
            <div style="font-size:0.9rem; color:#ffffff; margin-top:5px; font-weight:500;">📋 Total Complaints</div>
        </div>
        <div style="background: linear-gradient(135deg, #dc2626, #ef4444); padding:25px; 
                    border-radius:15px; text-align:center; margin-bottom:15px;
                    box-shadow: 0 4px 15px rgba(220,38,38,0.4);">
            <div style="font-size:2.5rem; font-weight:700; color:#ffffff;">{high}</div>
            <div style="font-size:0.9rem; color:#ffffff; margin-top:5px; font-weight:500;">🔴 High Priority</div>
        </div>
        <div style="background: linear-gradient(135deg, #059669, #10b981); padding:25px; 
                    border-radius:15px; text-align:center; margin-bottom:15px;
                    box-shadow: 0 4px 15px rgba(5,150,105,0.4);">
            <div style="font-size:2.5rem; font-weight:700; color:#ffffff;">{resolved}</div>
            <div style="font-size:0.9rem; color:#ffffff; margin-top:5px; font-weight:500;">✅ Resolved</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">📂 By Category</p>', unsafe_allow_html=True)
        if complaints:
            df = pd.DataFrame(complaints)
            cat_counts = df['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig = px.pie(cat_counts, values='Count', names='Category',
                        color_discrete_sequence=['#ef4444','#f97316','#22c55e','#3b82f6','#a855f7'],
                        hole=0.4)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250,
                            showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# ============================================
# PAGE - TRACK COMPLAINT
# ============================================
elif page == "🔍 Track Complaint":
    st.markdown('<p class="section-header">🔍 Track Your Complaint</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        track_id = st.text_input("🔍 Complaint ID", placeholder="PP-2024-001")

        if st.button("Track Complaint", use_container_width=True):
            found = None
            for c in st.session_state.complaints:
                if c['id'].upper() == track_id.upper():
                    found = c
                    break

            if found:
                priority = found['priority']
                status = found['status']
                p_icon = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
                progress = 10 if status == "Pending" else 60 if status == "In Progress" else 100

                st.markdown(f"""
                <div style="background:white; padding:30px; border-radius:20px;
                            box-shadow:0 10px 30px rgba(0,0,0,0.1); margin-top:20px; color:#1e293b;">
                    <h2 style="color:#1e3a8a; text-align:center;">✅ Complaint Found!</h2>
                    <hr>
                    <table style="width:100%; color:#1e293b;">
                        <tr><td style="padding:8px; color:#64748b;">🆔 Complaint ID</td><td><strong>{found['id']}</strong></td></tr>
                        <tr><td style="padding:8px; color:#64748b;">👤 Name</td><td><strong>{found['name']}</strong></td></tr>
                        <tr><td style="padding:8px; color:#64748b;">📍 Location</td><td><strong>{found['location']}</strong></td></tr>
                        <tr><td style="padding:8px; color:#64748b;">📂 Category</td><td><strong>{found['category']}</strong></td></tr>
                        <tr><td style="padding:8px; color:#64748b;">🤖 AI Priority</td><td><strong>{p_icon} {found['priority']}</strong></td></tr>
                        <tr><td style="padding:8px; color:#64748b;">🏢 Department</td><td><strong>{found['department']}</strong></td></tr>
                        <tr><td style="padding:8px; color:#64748b;">📋 Summary</td><td><strong>{found['summary']}</strong></td></tr>
                        <tr><td style="padding:8px; color:#64748b;">📅 Submitted</td><td><strong>{found['date']}</strong></td></tr>
                    </table>
                    <hr>
                    <h3 style="text-align:center;">Current Status: {status}</h3>
                </div>
                """, unsafe_allow_html=True)

                st.progress(progress)
                st.markdown(f"**Progress: {progress}%**")
            else:
                st.error("❌ Complaint ID not found. Please check and try again.")

elif page == "📊 Admin Dashboard":
    if not st.session_state.admin_logged_in:
        st.warning("⚠️ Please login as Admin to access the dashboard.")
        st.info("👉 Click **Admin Login** in the sidebar to login.")
    else:
        st.markdown('<p class="section-header">📊 Admin Dashboard</p>', unsafe_allow_html=True)

        complaints = st.session_state.complaints
        total = len(complaints)
        high = len([c for c in complaints if c['priority'] == 'High'])
        medium = len([c for c in complaints if c['priority'] == 'Medium'])
        low = len([c for c in complaints if c['priority'] == 'Low'])
        resolved = len([c for c in complaints if c['status'] == 'Resolved'])
        pending = len([c for c in complaints if c['status'] == 'Pending'])

        # Metric Cards
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-number">{total}</div><div class="metric-label">Total</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card" style="border-top-color:#dc2626"><div class="metric-number" style="color:#dc2626">{high}</div><div class="metric-label">🔴 High</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card" style="border-top-color:#d97706"><div class="metric-number" style="color:#d97706">{medium}</div><div class="metric-label">🟡 Medium</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card" style="border-top-color:#059669"><div class="metric-number" style="color:#059669">{resolved}</div><div class="metric-label">✅ Resolved</div></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="metric-card" style="border-top-color:#7c3aed"><div class="metric-number" style="color:#7c3aed">{pending}</div><div class="metric-label">⏳ Pending</div></div>', unsafe_allow_html=True)

        st.markdown("###")

        # Charts Row
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📊 Complaints by Category**")
            df = pd.DataFrame(complaints)
            cat_counts = df['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig1 = px.bar(cat_counts, x='Category', y='Count',
                         color='Count',
                         color_continuous_scale='Blues',
                         text='Count')
            fig1.update_layout(margin=dict(t=20, b=0), height=300,
                              showlegend=False, coloraxis_showscale=False)
            fig1.update_traces(textposition='outside')
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("**🎯 Priority Distribution**")
            priority_counts = df['priority'].value_counts().reset_index()
            priority_counts.columns = ['Priority', 'Count']
            colors = {'High': '#dc2626', 'Medium': '#d97706', 'Low': '#059669'}
            fig2 = px.pie(priority_counts, values='Count', names='Priority',
                         color='Priority',
                         color_discrete_map=colors,
                         hole=0.5)
            fig2.update_layout(margin=dict(t=20, b=0), height=300)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # Filters
        st.markdown("**🔍 Filter Complaints**")
        f1, f2, f3 = st.columns(3)
        with f1:
            filter_priority = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
        with f2:
            filter_status = st.selectbox("Status", ["All", "Pending", "In Progress", "Resolved"])
        with f3:
            filter_category = st.selectbox("Category", ["All", "Road & Potholes", "Water Supply", "Garbage & Sanitation", "Electricity", "Public Spaces & Parks"])

        filtered = complaints.copy()
        if filter_priority != "All":
            filtered = [c for c in filtered if c['priority'] == filter_priority]
        if filter_status != "All":
            filtered = [c for c in filtered if c['status'] == filter_status]
        if filter_category != "All":
            filtered = [c for c in filtered if c['category'] == filter_category]

        st.markdown(f"**Showing {len(filtered)} complaints**")
        st.markdown("---")

        # Complaints List
        for complaint in filtered:
            priority = complaint['priority']
            status = complaint['status']

            p_badge = f'<span class="badge-high">🔴 High</span>' if priority == "High" else f'<span class="badge-medium">🟡 Medium</span>' if priority == "Medium" else f'<span class="badge-low">🟢 Low</span>'
            s_badge = f'<span class="badge-pending">⏳ Pending</span>' if status == "Pending" else f'<span class="badge-progress">🔄 In Progress</span>' if status == "In Progress" else f'<span class="badge-resolved">✅ Resolved</span>'

            border_color = "#dc2626" if priority == "High" else "#d97706" if priority == "Medium" else "#059669"

            st.markdown(f"""
            <div class="complaint-card" style="border-left-color: {border_color};">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <strong style="font-size:1.1rem; color:#1e3a8a;">{complaint['id']}</strong>
                        &nbsp;&nbsp;{p_badge}&nbsp;&nbsp;{s_badge}
                    </div>
                    <div style="color:#64748b; font-size:0.85rem;">📅 {complaint['date']}</div>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; margin-bottom:10px; color:#1e293b;">
                    <div><span style="color:#64748b;">👤 Name</span><br><strong>{complaint.get('name','N/A')}</strong></div>
                    <div><span style="color:#64748b;">📍 Location</span><br><strong>{complaint.get('location','N/A')}</strong></div>
                    <div><span style="color:#64748b;">📂 Category</span><br><strong>{complaint.get('category','N/A')}</strong></div>
                </div>
                <div style="background:#f8fafc; padding:12px; border-radius:8px; margin-bottom:10px;">
                    <span style="color:#64748b; font-size:0.85rem;">🤖 AI Analysis</span><br>
                    <strong>{complaint['summary']}</strong><br>
                    <span style="color:#2563eb; font-size:0.85rem;">🏢 {complaint['department']}</span>
                </div>
                <div style="color:#1e293b; font-size:0.9rem;">
                    <span style="color:#64748b;">📝 Description:</span> {complaint['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            new_status = st.selectbox(
                f"Update Status for {complaint['id']}",
                ["Pending", "In Progress", "Resolved"],
                index=["Pending", "In Progress", "Resolved"].index(complaint['status']),
                key=f"status_{complaint['id']}"
            )
            if new_status != complaint['status']:
                for c in st.session_state.complaints:
                    if c['id'] == complaint['id']:
                        c['status'] = new_status
                st.success(f"✅ Status updated to {new_status}!")
                st.rerun()

            st.markdown("---")

# ============================================
# PAGE 3 - ADMIN LOGIN
# ============================================
elif page == "🔐 Admin Login":
    st.markdown('<p class="section-header">🔐 Admin Login</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.admin_logged_in:
            st.success("✅ You are logged in as Admin!")
            if st.button("🚪 Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
        else:
            st.markdown("""
            <div style="background:white; padding:40px; border-radius:20px; 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                <h3 style="text-align:center; color:#1e3a8a;">🏛️ Admin Portal</h3>
                <p style="text-align:center; color:#64748b;">Enter credentials to access dashboard</p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("login_form"):
                username = st.text_input("👤 Username")
                password = st.text_input("🔒 Password", type="password")
                login_btn = st.form_submit_button("🔐 Login", use_container_width=True)

                if login_btn:
                    if username == "admin" and password == ADMIN_PASSWORD:
                        st.session_state.admin_logged_in = True
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Try admin / admin123")