import streamlit as st
import requests
import google.generativeai as genai
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="VoltVigil | Energy Auditor", page_icon="⚡")

# We will securely load the API key from Streamlit's secrets later. 
# For local testing, you can temporarily paste your Gemini API key here.
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_TEMP_GEMINI_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

# Replace this with the actual Test or Production URL from your n8n Webhook node
N8N_WEBHOOK_URL = "YOUR_N8N_WEBHOOK_URL_HERE"

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
        
        # A. Trigger the UI AI Analysis (Gemini)
        prompt = f"""
        You are an expert electrical engineer. Analyze this residential telemetry data:
        - Total Consumption: {total_kwh} kWh
        - Peak Hours: {peak_hours}
        - Appliance Log: {appliance_log}
        
        Provide a concise 3-step actionable plan to shift heavy loads to off-peak hours and reduce grid stress.
        """
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            st.success("Analysis Complete!")
            st.subheader("💡 Optimization Directives")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"AI Analysis Error: {e}")

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