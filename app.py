
import streamlit as st
from utils.processor import analyze_audits
import tempfile
import os
import pandas as pd
from collections import defaultdict

st.set_page_config(page_title="Audit Insights Pro", layout="wide")
st.title("📘 Audit Insights Pro")
st.markdown("Upload 2–3 audit reports in PDF format. This tool uses AI to analyze findings, compare reports, and extract key learnings.")

uploaded_files = st.file_uploader("Upload PDF audit files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) < 2 or len(uploaded_files) > 3:
        st.warning("Please upload exactly 2 or 3 audit reports.")
    else:
        with st.spinner("Analyzing files with AI..."):
            try:
                temp_paths = []
                for file in uploaded_files:
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    temp_file.write(file.read())
                    temp_paths.append(temp_file.name)

                summaries, comparison, learnings = analyze_audits(temp_paths)

                st.markdown("## 🧾 Per-Audit Summaries")
                for i, summary in enumerate(summaries):
                    with st.expander(f"Audit {i+1} Summary"):
                        st.markdown(summary)

                st.markdown("## 🟰 Comparison of Audits")
                st.markdown(comparison)

                st.markdown("## 📘 Learnings for Future Audits")
                st.markdown(learnings)

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
