import streamlit as st
import joblib
import numpy as np
import re

from utils.feature_extraction import extract_features

# Load trained model
model = joblib.load("model/model.pkl")

# Page config
st.set_page_config(page_title="Phishing Detection", layout="centered")

# Title
st.title("🔐 Phishing Website Detection")
st.write("Enter a URL to check whether it is **phishing or legitimate**.")

# Input
url = st.text_input("🔗 Enter URL")

# Button
if st.button("Check"):
    if url:
        try:
            url_lower = url.lower()

            # 🚨 RULE-BASED DETECTION (VERY IMPORTANT)

            # 1. IP address detection
            if re.search(r'\d+\.\d+\.\d+\.\d+', url):
                st.error("⚠️ PHISHING WEBSITE\n\nReason: Uses IP address instead of domain")
                st.stop()

            # 2. '@' symbol detection
            if "@" in url:
                st.error("⚠️ PHISHING WEBSITE\n\nReason: Contains '@' symbol")
                st.stop()

            # 3. Suspicious keywords
            suspicious_words = ["login", "verify", "secure", "account", "update", "bank"]
            if any(word in url_lower for word in suspicious_words):
                st.warning("⚠️ Suspicious URL detected (contains sensitive keywords)")

            # 4. Too many dots (subdomains)
            if url.count(".") > 4:
                st.warning("⚠️ Suspicious URL (too many subdomains)")

            # 🔍 ML PREDICTION

            features = extract_features(url)
            features = np.array(features).reshape(1, -1)

            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0]

            confidence = max(probability) * 100

            # Result
            if prediction == 1:
                st.error(f"⚠️ PHISHING WEBSITE\n\nConfidence: {confidence:.2f}%")
            else:
                st.success(f"✅ LEGITIMATE WEBSITE\n\nConfidence: {confidence:.2f}%")

            # Debug info (optional)
            with st.expander("🔍 Feature Details"):
                st.write(features.tolist())

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter a URL")