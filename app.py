import streamlit as st
import pandas as pd
from openai import OpenAI
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Auditor (GAAP Compliance Checker)", page_icon="🧾", layout="wide")
st.title("🧾 AI Auditor — GAAP Compliance Checker")
st.markdown("Upload financial statements and detect potential GAAP compliance issues using AI.")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload an Excel file with financial statements:", type=["xlsx"])

def generate_pdf(report_text):
    """Generate a PDF report from AI findings."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Auditor — GAAP Compliance Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("This report summarizes AI-identified potential GAAP compliance issues based on the uploaded financial statement.", styles["Normal"]))
    story.append(Spacer(1, 12))

    for paragraph in report_text.split("\n"):
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip(), styles["Normal"]))
            story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    return buffer


if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📊 Uploaded Financial Data Preview")
    st.dataframe(df.head())

    # Convert dataframe to string for AI prompt
    data_str = df.to_string(index=False)

    # --- AI ANALYSIS ---
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    with st.spinner("Analyzing for GAAP compliance issues..."):
        prompt = f"""
        You are a certified financial auditor trained in up-to-date US GAAP standards.
        Review the following financial statement data and identify potential errors,
        inconsistencies, or compliance issues with GAAP. Suggest specific adjustments if applicable.

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

        findings = response.choices[0].message.content

        st.subheader("🧠 AI Findings")
        st.write(findings)
        st.success("Analysis complete!")

        # --- PDF DOWNLOAD BUTTON ---
        pdf_buffer = generate_pdf(findings)
        st.download_button(
            label="📄 Download GAAP Audit Report (PDF)",
            data=pdf_buffer,
            file_name="GAAP_Audit_Report.pdf",
            mime="application/pdf"
        )
else:
    st.info("Please upload an Excel file to begin.")

