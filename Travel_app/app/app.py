import streamlit as st
import requests
import datetime

# --- Page Configuration ---
st.set_page_config(page_title="AI Travel Assistant", layout="wide")

# =======================================================================
# !!! IMPORTANT: PASTE YOUR PINGGY URL HERE !!!
LLM_SERVER_URL = "http://fhqdc-34-125-200-76.a.free.pinggy.link/generate_itinerary" 
# =======================================================================


# --- Session State Management ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# --- 1. Simple Login Function ---
def login_form():
    st.sidebar.header("🔐 Login")
    with st.sidebar.form("login_form"):
        username = st.text_input("Username", value="user")
        password = st.text_input("Password", type="password", value="pass")
        submitted = st.form_submit_button("Login")
        
        if submitted and username == "24127546" and password == "hihihi":
            st.session_state['logged_in'] = True
            st.rerun()
        elif submitted:
            st.sidebar.error("Invalid credentials.")

# --- 2. Main Interface ---
if not st.session_state['logged_in']:
    login_form()
    st.info("Please log in to use the application.")
    st.stop()

# --- 3. Sidebar (Includes Chat History) ---
st.sidebar.header(f"Welcome, user!")
st.sidebar.header("📜 History")

if st.sidebar.button("Clear History"):
    st.session_state['chat_history'] = []

if not st.session_state['chat_history']:
    st.sidebar.caption("No itineraries generated yet.")

for item in reversed(st.session_state['chat_history'][-5:]):
    with st.sidebar.expander(f"{item['destination']} ({item['duration']} days)"):
        st.markdown(item['itinerary'])

# --- 4. Main Input Form ---
st.title("✈️ AI Travel Itinerary Generator")

with st.form("itinerary_form"):
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("Origin City", "Hanoi")
        today = datetime.date.today()
        dates = st.date_input(
            "Start and End Dates",
            (today, today + datetime.timedelta(days=5)),
        )
    with col2:
        destination = st.text_input("Destination City", "Tokyo")
        interests = st.multiselect(
            "Interests",
            ["Food", "Museums", "Nature", "Nightlife"],
            default=["Food", "Nature"]
        )

    pace = st.radio(
        "Travel Pace",
        ["Relaxed", "Normal", "Tight"], index=1, horizontal=True
    )
    generate_button = st.form_submit_button("✨ Generate Itinerary")

# --- 5. Process and Display Results ---
if generate_button:
    # Cập nhật kiểm tra này để tìm chuỗi URL mẫu
    if "YOUR_FASTAPI_PUBLIC_URL_HERE" in LLM_SERVER_URL:
        st.error("Error: Please update `LLM_SERVER_URL` in app.py with your Pinggy URL.")
    elif len(dates) != 2:
        st.error("Please select both a start and end date.")
    else:
        start_date, end_date = dates
        duration = (end_date - start_date).days + 1
        
        if duration <= 0:
            st.error("The end date must be after the start date.")
        else:
            with st.spinner(f"Generating your {duration}-day itinerary to {destination}... (This may take 1-2 minutes)"):
                payload = {
                    "origin": origin,
                    "destination": destination,
                    "duration_days": duration,
                    "interests": ", ".join(interests),
                    "pace": pace
                }
                try:
                    response = requests.post(LLM_SERVER_URL, json=payload, timeout=300)
                    response.raise_for_status()
                    result = response.json()
                    
                    if "itinerary" in result:
                        itinerary_text = result["itinerary"]
                        # ĐÃ SỬA LỖI Ở ĐÂY: Tiêu đề kết quả
                        st.header(f"🌟 Your Itinerary") 
                        st.markdown(itinerary_text)
                        st.session_state['chat_history'].append({
                            "destination": destination,
                            "duration": duration,
                            "itinerary": itinerary_text
                        })
                    else:
                        st.error(f"Error from server: {result.get('error', 'Unknown error.')}")
                
                except requests.exceptions.Timeout:
                    st.error("Request timed out. The Colab server might be busy. Please try again.")
                except requests.exceptions.RequestException as e:
                    # Cung cấp thông báo lỗi chi tiết hơn cho người dùng
                    st.error(f"Error connecting to the Backend server. Please check the Colab terminal or Pinggy URL. Details: {e}")