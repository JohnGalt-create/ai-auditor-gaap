# 🧾 AI Auditor — GAAP Compliance Checker

An AI-powered auditing assistant that reviews uploaded financial statements for potential GAAP compliance issues and suggests adjustments.

## 🚀 How it Works
1. Upload an Excel file containing financial statement data.
2. The app sends the data to an AI model trained on GAAP knowledge.
3. The model flags potential errors, notes which principles are affected, and suggests corrections.

## 🛠️ Tech Stack
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- Python (pandas)

## 💡 Deployment
This app is ready to deploy directly to [Streamlit Cloud](https://share.streamlit.io/).

**Steps:**
1. Fork or clone this repository.
2. Add your OpenAI API key to Streamlit Secrets (`Settings → Secrets`).
3. Click “Deploy” on Streamlit Cloud.

## 📂 Example File
See `sample_data/sample_financials.xlsx` for an example upload format.
