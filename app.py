"""
Streamlit Frontend for Astrology Booklet User Management
Connects to FastAPI backend for user management and PDF generation.
"""
import streamlit as st
import requests
import json
from datetime import datetime
import os

st.set_option('client.showErrorDetails', False)

# -----------
# Page setup
# ------------
st.set_page_config(
    page_title="Astrology Booklet Portal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌙 Astrology Booklet User Management")
st.write("Frontend UI for managing users and generating astrology booklets")

# -------------
# Configuration
# -------------
st.sidebar.header("⚙️ Configuration")
BASE_URL = st.sidebar.text_input(
    "API Base URL", 
    value=os.getenv("API_BASE_URL", "http://localhost:8010"),
    help="Enter your FastAPI backend URL"
)
token_input = st.sidebar.text_input(
    "Bearer Token (Optional)", 
    type="password", 
    help="Enter API token if required"
)

# ----------------------
# Helpers
# ----------------------
def pretty(obj):
    """Format JSON object for display."""
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except Exception:
        return str(obj)

def get_headers(require_auth: bool = False):
    """Get HTTP headers with optional authentication."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if require_auth and token_input:
        headers["Authorization"] = f"Bearer {token_input}"
    return headers

def show_response(resp, success_message: str = None):
    """Display API response."""
    if resp.status_code < 400:
        if success_message:
            st.success(success_message)
        try:
            data = resp.json()
            st.json(data)
            return data
        except Exception:
            st.text_area("Raw response (text)", str(resp.text), height=200)
            return None
    else:
        try:
            error_data = resp.json()
            st.error(f"Error {resp.status_code}: {error_data.get('detail', 'Unknown error')}")
        except Exception:
            st.error(f"Error {resp.status_code}: {resp.text}")
        return None

def make_request(method: str, url: str, **kwargs):
    """Make HTTP request with error handling."""
    try:
        if method.upper() == "GET":
            resp = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            resp = requests.post(url, **kwargs)
        elif method.upper() == "PUT":
            resp = requests.put(url, **kwargs)
        elif method.upper() == "DELETE":
            resp = requests.delete(url, **kwargs)
        else:
            st.error(f"Unsupported method: {method}")
            return None
        return resp
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Connection failed. Is the backend running at {BASE_URL}?")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out")
        return None
    except requests.RequestException as e:
        st.error(f"❌ Request failed: {e}")
        return None

# ----------------------
# Main UI
# ----------------------
action = st.selectbox(
    "Select Action",
    [
        "View All Users",
        "Get User by ID",
        "Create/Update User",
        "Get Astrology Placements",
        "Get Big Three (Sun, Moon, Asc)",
        "Generate Booklet PDF",
        "Generate Calendar PDF"
    ]
)

st.markdown("---")

# ----------------------
# View All Users
# ----------------------
if action == "View All Users":
    st.subheader("📋 All Users")
    if st.button("Fetch All Users"):
        resp = make_request("GET", f"{BASE_URL}/users", headers=get_headers(), timeout=10)
        if resp:
            data = show_response(resp)
            if data:
                st.info(f"Found {len(data)} user(s)")

# ----------------------
# Get User by ID
# ----------------------
elif action == "Get User by ID":
    st.subheader("🔍 Get User by ID")
    user_id = st.number_input("User ID", min_value=1, value=1, step=1)
    if st.button("Fetch User"):
        resp = make_request("GET", f"{BASE_URL}/users/{user_id}", headers=get_headers(), timeout=10)
        if resp:
            show_response(resp)

# ----------------------
# Create/Update User
# ----------------------
elif action == "Create/Update User":
    st.subheader("➕ Create/Update User")
    st.write("Fill in the form below. Leave fields empty if you don't want to update them.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name *", value="")
        last_name = st.text_input("Last Name", value="")
        birthdate = st.date_input("Birthdate", value=None)
        birthtime = st.time_input("Birth Time (24h)", value=None)
    
    with col2:
        city = st.text_input("City", value="")
        country = st.text_input("Country", value="")
        login = st.text_input("Login/Email", value="")
        timezone = st.text_input("Timezone (IANA)", value="", help="e.g., Europe/Brussels")
    
    if st.button("Save User"):
        if not first_name:
            st.error("First name is required!")
        else:
            payload = {
                "first_name": first_name,
            }
            
            if last_name:
                payload["last_name"] = last_name
            if birthdate:
                payload["birthdate"] = birthdate.strftime('%Y-%m-%d')
            if birthtime:
                payload["birthtime"] = birthtime.strftime('%H:%M')
            if city:
                payload["city"] = city
            if country:
                payload["country"] = country
            if login:
                payload["login"] = login
            if timezone:
                payload["timezone"] = timezone
            
            resp = make_request(
                "POST", 
                f"{BASE_URL}/users", 
                json=payload, 
                headers=get_headers(require_auth=True), 
                timeout=10
            )
            if resp:
                show_response(resp, "✅ User saved successfully!")

# ----------------------
# Get Astrology Placements
# ----------------------
elif action == "Get Astrology Placements":
    st.subheader("⭐ Astrology Placements")
    user_id = st.number_input("User ID", min_value=1, value=1, step=1)
    if st.button("Get Placements"):
        resp = make_request("GET", f"{BASE_URL}/users/{user_id}/placements", headers=get_headers(), timeout=30)
        if resp:
            show_response(resp)

# ----------------------
# Get Big Three
# ----------------------
elif action == "Get Big Three (Sun, Moon, Asc)":
    st.subheader("🌟 Big Three (Sun, Moon, Ascendant)")
    user_id = st.number_input("User ID", min_value=1, value=1, step=1)
    if st.button("Get Big Three"):
        resp = make_request("GET", f"{BASE_URL}/users/{user_id}/big-three", headers=get_headers(), timeout=30)
        if resp:
            data = show_response(resp)
            if data:
                st.markdown("### Astrology Summary")
                if data.get("Sun"):
                    st.write(f"☀️ **Sun**: {data['Sun'].get('sign', 'N/A')} {data['Sun'].get('degree', '')}°")
                if data.get("Moon"):
                    st.write(f"🌙 **Moon**: {data['Moon'].get('sign', 'N/A')} {data['Moon'].get('degree', '')}°")
                if data.get("Asc"):
                    st.write(f"⬆️ **Ascendant**: {data['Asc'].get('sign', 'N/A')} {data['Asc'].get('degree', '')}°")

# ----------------------
# Generate Booklet PDF
# ----------------------
elif action == "Generate Booklet PDF":
    st.subheader("📖 Generate Booklet PDF")
    user_id = st.number_input("User ID", min_value=1, value=1, step=1)
    if st.button("Generate Booklet"):
        with st.spinner("Generating booklet PDF... This may take a moment."):
            resp = make_request("GET", f"{BASE_URL}/users/{user_id}/booklet", headers=get_headers(), timeout=120)
            if resp and resp.status_code == 200:
                st.success("✅ Booklet generated successfully!")
                st.info("The PDF has been saved to your Downloads folder.")
                # Note: In Streamlit Cloud, you might want to return the file for download
                # For now, we just confirm generation
            elif resp:
                show_response(resp)

# ----------------------
# Generate Calendar PDF
# ----------------------
elif action == "Generate Calendar PDF":
    st.subheader("📅 Generate Calendar PDF")
    user_id = st.number_input("User ID", min_value=1, value=1, step=1)
    year = st.number_input("Year", min_value=2020, max_value=2100, value=2026, step=1)
    if st.button("Generate Calendar"):
        with st.spinner("Generating calendar PDF... This may take a moment."):
            resp = make_request(
                "GET", 
                f"{BASE_URL}/users/{user_id}/calendar?year={year}", 
                headers=get_headers(), 
                timeout=120
            )
            if resp and resp.status_code == 200:
                st.success("✅ Calendar generated successfully!")
                st.info("The PDF has been saved to your Downloads folder.")
            elif resp:
                show_response(resp)

# ----------------------
# Footer
# ----------------------
st.markdown("---")
st.caption("💡 Note: This UI connects to the FastAPI backend for user management and astrology booklet generation.")

# Health check button in sidebar
if st.sidebar.button("🔍 Check Backend Health"):
    resp = make_request("GET", f"{BASE_URL}/health", headers=get_headers(), timeout=5)
    if resp:
        if resp.status_code == 200:
            st.sidebar.success("✅ Backend is healthy!")
            try:
                health_data = resp.json()
                st.sidebar.json(health_data)
            except:
                pass
        else:
            st.sidebar.error("❌ Backend health check failed")

