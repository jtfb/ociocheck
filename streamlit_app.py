import streamlit as st
import subprocess
import smtplib
from email.mime.text import MIMEText
import os
import datetime

# Configuration
UPLOAD_FOLDER = 'uploads'
LOG_FILE = 'logs.txt'
EMAIL = 'your-email@example.com'

# Create necessary folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# UI for file upload
st.title("OCIOCheck Remote Runner")
st.header("Upload your ocio.config file")
uploaded_file = st.file_uploader("Choose a file", type="config")

if uploaded_file:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Run ociocheck
    try:
        result = subprocess.run(
            ['ociocheck', '-iconfig', file_path], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Log the result
        with open(LOG_FILE, "a") as log:
            log.write(f"{datetime.datetime.now()} - {uploaded_file.name}\n")
        
        # Display results
        if result.returncode == 0:
            st.success("OCIOCheck passed!")
            st.text(result.stdout)
        else:
            st.error("OCIOCheck failed!")
            st.text(result.stderr)

            # Send email notification
            msg = MIMEText(result.stderr)
            msg['Subject'] = 'OCIOCheck Failure Notification'
            msg['From'] = EMAIL
            msg['To'] = EMAIL

            # Note: Configure your SMTP server settings here
            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.login('user', 'password')
                server.sendmail(EMAIL, [EMAIL], msg.as_string())
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Tabs for future expansion
st.sidebar.title("Features")
st.sidebar.write("Future features will be added here.")
