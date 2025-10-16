import streamlit as st
import pandas as pd
from openai import OpenAI
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Auditor (GAAP Compliance Checker)", page_icon="🧾", layout="wide")
st.title("🧾 AI Auditor — GAAP Compliance Checker")
st.markdown("Upload financial statements and detect potential GAAP compliance issues using AI.")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload an Excel file with financial statements:", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📊 Uploaded Financial Data Preview")
    st.dataframe(df.head())

    # Convert dataframe to a string for analysis
    data_str = df.to_string(index=False)

    # --- AI ANALYSIS ---
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    with st.spinner("Analyzing for GAAP compliance issues..."):
        prompt = f"""
        You are an expert financial auditor trained in current US GAAP standards.
        Review the following financial statement data and identify potential errors, inconsistencies,
        or compliance issues with GAAP. Suggest specific adjustments if applicable.

        Data:
        {data_str}

        Provide:
        - Specific issues detected
        - Relevant GAAP principles affected
        - Suggested correction or adjustment
        - Confidence level (Low / Medium / High)
        """

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}]
        )

        st.subheader("🧠 AI Findings")
        st.write(response.choices[0].message.content)

        st.success("Analysis complete!")
else:
    st.info("Please upload an Excel file to begin.")
