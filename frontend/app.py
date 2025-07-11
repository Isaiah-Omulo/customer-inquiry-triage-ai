# frontend/app.py

import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Customer Inquiry Triage",
    page_icon="",
    layout="centered"
)

# --- Constants ---
API_URL = "http://127.0.0.1:8000/triage"

# --- UI Components & Styling ---
st.title(" Customer Inquiry Triage")
st.markdown(
    """
    Enter a customer message below to automatically classify it into the correct department.
    This demo uses a **FastAPI backend powered by Google Gemini** for classification.
    """
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTextArea textarea { min-height: 150px; }
    .stButton button { width: 100%; }
    .response-card {
        background-color: #f0f2f6;
        border-left: 5px solid #1a73e8; /* Google Blue */
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .response-card-error { border-left: 5px solid #f44336; }
    .response-header { font-size: 1.2rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- Application Logic ---
if 'response_data' not in st.session_state:
    st.session_state.response_data = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

with st.form(key='triage_form'):
    message_input = st.text_area(
        "Customer Message",
        placeholder="e.g., 'Hello, I was double-charged for my subscription this month. Can you help me with a refund?'",
        key='message_input'
    )
    submit_button = st.form_submit_button(label="Triage with Gemini")

if submit_button:
    if message_input and len(message_input.strip()) >= 10:
        with st.spinner('Asking Gemini for analysis...'):
            try:
                payload = {"message": message_input}
                response = requests.post(API_URL, json=payload, timeout=30)
                response.raise_for_status()
                st.session_state.response_data = response.json()
                st.session_state.error_message = None
            except requests.exceptions.RequestException as e:
                st.session_state.response_data = None
                if e.response is not None:
                    try:
                        detail = e.response.json().get('detail', 'No details provided.')
                        st.session_state.error_message = f"API Error (Status {e.response.status_code}): {detail}"
                    except json.JSONDecodeError:
                         st.session_state.error_message = f"API Error (Status {e.response.status_code}): Could not decode error response."
                else:
                    st.session_state.error_message = "Could not connect to the backend API. Is it running?"
    else:
        st.session_state.error_message = "Please enter a message with at least 10 characters."

# --- Display Results ---
if st.session_state.error_message:
    st.markdown(
        f'<div class="response-card response-card-error"><p class="response-header">Error</p><p>{st.session_state.error_message}</p></div>',
        unsafe_allow_html=True
    )

if st.session_state.response_data:
    res = st.session_state.response_data
    category = res.get('category', 'N/A').replace('_', ' ').title()
    reasoning = res.get('reasoning', 'No reasoning provided.')
    score = res.get('score', 0)

    st.markdown('<div class="response-card">', unsafe_allow_html=True)
    st.markdown(f'<p class="response-header">Triage Result</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="**Category**", value=category)
    with col2:
        st.metric(label="**Confidence Score**", value=f"{score:.2%}")

    st.markdown("**Reasoning**")
    st.info(reasoning)
    st.markdown('</div>', unsafe_allow_html=True)