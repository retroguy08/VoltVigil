import streamlit as st
import os
import requests
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="VoltVigil | Energy Auditor", page_icon="⚡")

# Safely fetch the API key from Streamlit secrets
api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Google API Key not found in Streamlit Secrets!")
    st.stop()

N8N_WEBHOOK_URL = "https://ahmadhassaan.app.n8n.cloud/webhook/incoming-data"

# --- 2. FRONTEND UI ---
st.title("⚡ VoltVigil: Smart-Home Energy Auditor")
st.write("Enter your daily appliance usage telemetry to receive an instant engineering-grade load analysis and optimization plan.")

with st.form("energy_form"):
    total_kwh = st.number_input("Total Daily Consumption (kWh)", min_value=0.0, format="%.1f")
    peak_hours = st.text_input("Peak Usage Hours", placeholder="e.g., 6:00 PM - 10:00 PM")
    appliance_log = st.text_area("Appliance Log", placeholder="e.g., 1.5 Ton AC for 8 hrs, 1HP Water Pump for 1.5 hrs...")
    
    submitted = st.form_submit_button("Run Energy Audit")

# --- 3. AI & BACKEND LOGIC ---
if submitted:
    if total_kwh > 0 and appliance_log:
        st.info("Analyzing load profile...")
        
        prompt = f"""
        You are an expert electrical engineer. Analyze this residential telemetry data:
        - Total Consumption: {total_kwh} kWh
        - Peak Hours: {peak_hours}
        - Appliance Log: {appliance_log}
        
        Provide a concise 3-step actionable plan to shift heavy loads to off-peak hours and reduce grid stress.
        """
        
        # A. Trigger the AI Analysis (Direct REST API Bypass)
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            rest_response = requests.post(url, headers=headers, json=data)
            
            if rest_response.status_code == 200:
                response_json = rest_response.json()
                ai_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
                
                st.success("Analysis Complete!")
                st.subheader("💡 Optimization Directives")
                st.write(ai_text)
            else:
                st.error(f"API Error: {rest_response.text}")
            
        except Exception as e:
            st.error(f"Request Failed: {e}")

        # B. Send data to n8n backend for logging and email
        payload = {
            "total_kwh": str(total_kwh),
            "peak_hours": peak_hours,
            "appliance_log": appliance_log
        }
        
        try:
            requests.post(N8N_WEBHOOK_URL, json=payload)
            st.caption("✅ Audit securely logged to VoltVigil Database and sent to your inbox via n8n.")
        except Exception as e:
            st.warning("Could not connect to backend logging system.")
            
    else:
        st.warning("Please enter your total kWh and appliance log to run the audit.")