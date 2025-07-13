import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from twilio.rest import Client
import tweepy
import facebook
import instagrapi
import pywhatkit as kit
import linkedin_api
from datetime import datetime
import os
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Communication Hub",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5em;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 20px;
    }
    .success-msg {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 10px 0;
    }
    .error-msg {
        background: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 10px 0;
    }
    .info-box {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Multi-Platform Communication Hub</h1>
    <p style="color: white; font-size: 1.2em;">Send emails, SMS, make calls, and post on social media - all in one place!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("🎯 Select Feature")
feature = st.sidebar.selectbox(
    "Choose a communication method:",
    ["📧 Email", "📱 SMS", "☎️ Phone Call", "💼 LinkedIn", "🐦 Twitter/X", "📘 Facebook", "📸 Instagram", "💬 WhatsApp", "🔧 All Features Demo"]
)

# Helper functions
def display_success(message):
    st.markdown(f'<div class="success-msg">✅ {message}</div>', unsafe_allow_html=True)

def display_error(message):
    st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)

def display_info(message):
    st.markdown(f'<div class="info-box">ℹ️ {message}</div>', unsafe_allow_html=True)

# 1. EMAIL FUNCTIONALITY
if feature == "📧 Email":
    st.header("📧 Email Sender")
    
    with st.form("email_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            sender_email = st.text_input("Your Email Address", placeholder="your.email@gmail.com")
            sender_password = st.text_input("App Password", type="password", help="Use app-specific password for Gmail")
            recipient_email = st.text_input("Recipient Email", placeholder="recipient@email.com")
        
        with col2:
            subject = st.text_input("Subject", placeholder="Enter email subject")
            smtp_server = st.selectbox("SMTP Server", ["smtp.gmail.com", "smtp.outlook.com", "smtp.yahoo.com"])
            smtp_port = st.selectbox("Port", [587, 465, 25])
        
        message = st.text_area("Message", height=150, placeholder="Enter your message here...")
        
        submit_email = st.form_submit_button("📤 Send Email", use_container_width=True)
        
        if submit_email:
            try:
                # Create message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(message, 'plain'))
                
                # Send email
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                
                display_success(f"Email sent successfully to {recipient_email}!")
                
            except Exception as e:
                display_error(f"Failed to send email: {str(e)}")
    
    # Instructions
    st.markdown("### 📋 Setup Instructions:")
    st.markdown("""
    1. **Gmail**: Enable 2-factor authentication and generate an app password
    2. **Outlook**: Use your regular password or app password
    3. **Yahoo**: Generate an app password in security settings
    """)

# 2. SMS FUNCTIONALITY
elif feature == "📱 SMS":
    st.header("📱 SMS Sender")
    
    with st.form("sms_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            account_sid = st.text_input("Twilio Account SID", type="password")
            auth_token = st.text_input("Twilio Auth Token", type="password")
            from_number = st.text_input("From Number", placeholder="+1234567890")
        
        with col2:
            to_number = st.text_input("To Number", placeholder="+1234567890")
            sms_message = st.text_area("Message", height=100, placeholder="Enter your SMS message...")
        
        submit_sms = st.form_submit_button("📤 Send SMS", use_container_width=True)
        
        if submit_sms:
            try:
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=sms_message,
                    from_=from_number,
                    to=to_number
                )
                display_success(f"SMS sent successfully! Message SID: {message.sid}")
                
            except Exception as e:
                display_error(f"Failed to send SMS: {str(e)}")
    
    display_info("💡 You need a Twilio account to send SMS. Sign up at twilio.com for free credits.")

# 3. PHONE CALL FUNCTIONALITY
elif feature == "☎️ Phone Call":
    st.header("☎️ Phone Call Maker")
    
    with st.form("call_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            twilio_sid = st.text_input("Twilio Account SID", type="password")
            twilio_token = st.text_input("Twilio Auth Token", type="password")
            from_phone = st.text_input("From Number", placeholder="+1234567890")
        
        with col2:
            to_phone = st.text_input("To Number", placeholder="+1234567890")
            twiml_url = st.text_input("TwiML URL", placeholder="http://demo.twilio.com/docs/voice.xml")
        
        submit_call = st.form_submit_button("📞 Make Call", use_container_width=True)
        
        if submit_call:
            try:
                client = Client(twilio_sid, twilio_token)
                call = client.calls.create(
                    url=twiml_url,
                    to=to_phone,
                    from_=from_phone
                )
                display_success(f"Call initiated successfully! Call SID: {call.sid}")
                
            except Exception as e:
                display_error(f"Failed to make call: {str(e)}")
    
    # TwiML example
    st.markdown("### 🎵 Sample TwiML Response:")
    st.code("""
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>Hello! This is a call from your Python application.</Say>
        <Play>https://api.twilio.com/cowbell.mp3</Play>
    </Response>
    """, language="xml")

# 4. LINKEDIN FUNCTIONALITY
elif feature == "💼 LinkedIn":
    st.header("💼 LinkedIn Poster")
    
    with st.form("linkedin_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            linkedin_email = st.text_input("LinkedIn Email")
            linkedin_password = st.text_input("LinkedIn Password", type="password")
        
        with col2:
            post_content = st.text_area("Post Content", height=150, placeholder="What's on your mind?")
        
        submit_linkedin = st.form_submit_button("📤 Post to LinkedIn", use_container_width=True)
        
        if submit_linkedin:
            try:
                # Note: This is a simplified example. LinkedIn API requires OAuth 2.0
                display_info("LinkedIn posting requires OAuth 2.0 authentication. This is a demonstration of the structure.")
                
                # Simulated success (in real implementation, use LinkedIn API)
                display_success("Post would be published to LinkedIn!")
                
            except Exception as e:
                display_error(f"Failed to post to LinkedIn: {str(e)}")
    
    st.markdown("### 🔐 LinkedIn API Setup:")
    st.markdown("""
    1. Create a LinkedIn App at [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
    2. Get your Client ID and Client Secret
    3. Implement OAuth 2.0 flow
    4. Use the LinkedIn API to post content
    """)

# 5. TWITTER/X FUNCTIONALITY
elif feature == "🐦 Twitter/X":
    st.header("🐦 Twitter/X Poster")
    
    with st.form("twitter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            consumer_key = st.text_input("Consumer Key", type="password")
            consumer_secret = st.text_input("Consumer Secret", type="password")
            access_token = st.text_input("Access Token", type="password")
        
        with col2:
            access_token_secret = st.text_input("Access Token Secret", type="password")
            tweet_content = st.text_area("Tweet Content", height=100, max_chars=280, placeholder="What's happening?")
        
        submit_tweet = st.form_submit_button("🐦 Send Tweet", use_container_width=True)
        
        if submit_tweet:
            try:
                # Twitter API v2 implementation
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)
                
                # Post tweet
                api.update_status(tweet_content)
                display_success("Tweet posted successfully!")
                
            except Exception as e:
                display_error(f"Failed to post tweet: {str(e)}")
    
    st.markdown("### 🔑 Twitter API Setup:")
    st.markdown("""
    1. Apply for Twitter Developer Account
    2. Create a new App in Twitter Developer Portal
    3. Generate API keys and access tokens
    4. Use Twitter API v2 for posting
    """)

# 6. FACEBOOK FUNCTIONALITY
elif feature == "📘 Facebook":
    st.header("📘 Facebook Poster")
    
    with st.form("facebook_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            access_token = st.text_input("Facebook Access Token", type="password")
            page_id = st.text_input("Page ID (optional)", placeholder="For page posting")
        
        with col2:
            fb_message = st.text_area("Post Message", height=150, placeholder="Share your thoughts...")
        
        submit_facebook = st.form_submit_button("📤 Post to Facebook", use_container_width=True)
        
        if submit_facebook:
            try:
                # Facebook Graph API implementation
                graph = facebook.GraphAPI(access_token)
                
                if page_id:
                    graph.put_object(page_id, "feed", message=fb_message)
                else:
                    graph.put_object("me", "feed", message=fb_message)
                
                display_success("Posted to Facebook successfully!")
                
            except Exception as e:
                display_error(f"Failed to post to Facebook: {str(e)}")
    
    st.markdown("### 📱 Facebook API Setup:")
    st.markdown("""
    1. Create a Facebook App at [Facebook Developers](https://developers.facebook.com/)
    2. Get your App ID and App Secret
    3. Generate User Access Token
    4. Use Facebook Graph API for posting
    """)

# 7. INSTAGRAM FUNCTIONALITY
elif feature == "📸 Instagram":
    st.header("📸 Instagram Poster")
    
    with st.form("instagram_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            instagram_username = st.text_input("Instagram Username")
            instagram_password = st.text_input("Instagram Password", type="password")
        
        with col2:
            caption = st.text_area("Caption", height=100, placeholder="Write a caption...")
            image_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        
        submit_instagram = st.form_submit_button("📤 Post to Instagram", use_container_width=True)
        
        if submit_instagram:
            try:
                # Instagram posting simulation
                display_info("Instagram posting requires careful handling of their API policies.")
                display_success("Image would be posted to Instagram!")
                
            except Exception as e:
                display_error(f"Failed to post to Instagram: {str(e)}")
    
    st.markdown("### 📷 Instagram API Notes:")
    st.markdown("""
    1. Instagram Basic Display API for reading data
    2. Instagram Graph API for business accounts
    3. Third-party libraries like instagrapi for automation
    4. Be mindful of Instagram's terms of service
    """)

# 8. WHATSAPP FUNCTIONALITY
elif feature == "💬 WhatsApp":
    st.header("💬 WhatsApp Sender")
    
    with st.form("whatsapp_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            phone_number = st.text_input("Phone Number", placeholder="+1234567890")
            send_time_hour = st.selectbox("Hour", list(range(24)))
            send_time_minute = st.selectbox("Minute", list(range(60)))
        
        with col2:
            whatsapp_message = st.text_area("Message", height=100, placeholder="Enter your WhatsApp message...")
        
        submit_whatsapp = st.form_submit_button("💬 Send WhatsApp", use_container_width=True)
        
        if submit_whatsapp:
            try:
                # Using pywhatkit for WhatsApp automation
                kit.sendwhatmsg(phone_number, whatsapp_message, send_time_hour, send_time_minute)
                display_success(f"WhatsApp message scheduled for {send_time_hour:02d}:{send_time_minute:02d}")
                
            except Exception as e:
                display_error(f"Failed to send WhatsApp message: {str(e)}")
    
    st.markdown("### 💡 WhatsApp Automation Notes:")
    st.markdown("""
    1. **pywhatkit**: Automates WhatsApp Web
    2. **Selenium**: For more complex automation
    3. **WhatsApp Business API**: For business use cases
    4. Requires WhatsApp Web to be logged in
    """)

# 9. ALL FEATURES DEMO
elif feature == "🔧 All Features Demo":
    st.header("🔧 Complete Communication Hub Demo")
    
    # Overview
    st.markdown("### 🎯 Feature Overview")
    
    features = [
        ("📧 Email", "Send emails using SMTP", "✅ Implemented"),
        ("📱 SMS", "Send SMS using Twilio", "✅ Implemented"),
        ("☎️ Phone Call", "Make calls using Twilio", "✅ Implemented"),
        ("💼 LinkedIn", "Post to LinkedIn", "🔧 API Integration Required"),
        ("🐦 Twitter/X", "Post tweets", "🔧 API Keys Required"),
        ("📘 Facebook", "Post to Facebook", "🔧 API Integration Required"),
        ("📸 Instagram", "Post to Instagram", "🔧 Special Handling Required"),
        ("💬 WhatsApp", "Send WhatsApp messages", "✅ Implemented"),
    ]
    
    for emoji, name, status in features:
        st.markdown(f"**{emoji} {name}**: {status}")
    
    st.markdown("---")
    
    # Quick Test Form
    st.markdown("### 🚀 Quick Test")
    
    with st.form("quick_test"):
        test_type = st.selectbox("Select test type:", ["Email Test", "SMS Test", "Call Test"])
        
        if test_type == "Email Test":
            email = st.text_input("Test Email")
            if st.form_submit_button("Test Email"):
                display_info(f"Email test would be sent to: {email}")
        
        elif test_type == "SMS Test":
            phone = st.text_input("Test Phone Number")
            if st.form_submit_button("Test SMS"):
                display_info(f"SMS test would be sent to: {phone}")
        
        elif test_type == "Call Test":
            phone = st.text_input("Test Phone Number")
            if st.form_submit_button("Test Call"):
                display_info(f"Test call would be made to: {phone}")
    
    # Installation Requirements
    st.markdown("### 📦 Installation Requirements")
    st.code("""
pip install streamlit
pip install twilio
pip install tweepy
pip install python-facebook-api
pip install instagrapi
pip install pywhatkit
pip install linkedin-api
pip install requests
pip install pillow
    """)
    
    # Configuration Template
    st.markdown("### ⚙️ Configuration Template")
    st.code("""
# config.py
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'your_email@gmail.com',
    'password': 'your_app_password'
}

TWILIO_CONFIG = {
    'account_sid': 'your_twilio_sid',
    'auth_token': 'your_twilio_token',
    'phone_number': '+1234567890'
}

SOCIAL_MEDIA_CONFIG = {
    'twitter': {
        'consumer_key': 'your_key',
        'consumer_secret': 'your_secret',
        'access_token': 'your_token',
        'access_token_secret': 'your_token_secret'
    },
    'facebook': {
        'access_token': 'your_facebook_token'
    },
    'linkedin': {
        'client_id': 'your_linkedin_client_id',
        'client_secret': 'your_linkedin_client_secret'
    }
}
    """, language="python")

# Footer
st.markdown("---")
st.markdown("### 📚 Documentation & Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📧 Email APIs**")
    st.markdown("- Python smtplib")
    st.markdown("- Gmail API")
    st.markdown("- SendGrid API")

with col2:
    st.markdown("**📱 SMS/Voice APIs**")
    st.markdown("- Twilio")
    st.markdown("- Vonage (Nexmo)")
    st.markdown("- AWS SNS")

with col3:
    st.markdown("**🌐 Social Media APIs**")
    st.markdown("- Twitter API v2")
    st.markdown("- Facebook Graph API")
    st.markdown("- LinkedIn API")

st.markdown("---")
st.markdown("### 🎯 LinkedIn Post Template")
st.code("""
🚀 Just built an amazing Multi-Platform Communication Hub using Python & Streamlit! 

✨ Features:
📧 Email automation with SMTP
📱 SMS sending via Twilio
☎️ Phone calls integration
💼 LinkedIn posting
🐦 Twitter/X automation
📘 Facebook posting
📸 Instagram integration
💬 WhatsApp messaging

Perfect for automating your communication workflow! 

#Python #Streamlit #Automation #API #CommunicationHub #TechInnovation

GitHub: [Your Repository Link]
Live Demo: [Your Streamlit App Link]
""")

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;">
    <h3>🎉 Communication Hub Ready!</h3>
    <p>Your all-in-one solution for emails, SMS, calls, and social media posting.</p>
    <p><strong>Next Steps:</strong> Add your API credentials and start communicating!</p>
</div>
""", unsafe_allow_html=True)
