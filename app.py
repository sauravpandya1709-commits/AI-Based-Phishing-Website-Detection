
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(
    page_title="AI Phishing Detector",
    page_icon="🛡️",
    layout="centered"
)

# Sample training data from your project
data = {
    "url_length": [20,75,65,18,80,22,60,25,70,19],
    "has_at": [0,1,0,0,1,0,0,0,1,0],
    "num_dots": [1,5,4,2,6,1,4,2,5,1],
    "has_https": [1,0,0,1,0,1,0,1,0,1],
    "num_hyphens": [0,4,3,0,5,0,2,0,3,0],
    "label": [0,1,1,0,1,0,1,0,1,0]
}

df = pd.DataFrame(data)
X = df.drop("label", axis=1)
y = df["label"]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Website design
st.title("🛡️ AI Phishing Website Detector")
st.write(
    "Enter a website URL to analyze its features "
    "and estimate its phishing risk."
)

url = st.text_input(
    "Website URL",
    placeholder="https://example.com"
)

if st.button("Analyze Website", type="primary"):

    if not url.strip():
        st.warning("Please enter a website URL.")

    elif " " in url.strip() or "." not in url:
        st.error("Please enter a valid-looking URL.")

    else:
        url = url.strip()

        features = [[
            len(url),
            int("@" in url),
            url.count("."),
            int(url.lower().startswith("https://")),
            url.count("-")
        ]]

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1] * 100
        risk_score = round(probability / 20, 1)

        st.subheader("Analysis Report")

        st.write("**URL:**", url)
        st.write("**URL Length:**", len(url))
        st.write("**Contains @:**", "Yes" if "@" in url else "No")
        st.write("**Number of Dots:**", url.count("."))
        st.write(
            "**HTTPS Enabled:**",
            "Yes" if url.lower().startswith("https://") else "No"
        )
        st.write("**Number of Hyphens:**", url.count("-"))

        st.metric("Model Phishing Probability", f"{probability:.2f}%")
        st.metric("Risk Score", f"{risk_score}/5")

        if prediction == 1:
            st.error("⚠️ RESULT: PHISHING WEBSITE")
            st.write(
                "Recommendation: Avoid entering passwords, "
                "OTPs, or banking details."
            )
        else:
            st.success("RESULT: Classified as legitimate")
            st.write(
                "Recommendation: Check the domain and other "
                "security indicators before trusting the website."
            )

        st.caption(
            "Educational prototype. Results are not a guarantee "
            "that a website is safe or malicious."
      )
