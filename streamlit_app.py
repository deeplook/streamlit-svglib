#!/usr/bin/env python

"""
A demo for using svglib inside a small Streamlit application.

This app is running in a webbrowser and allows to open and edit a SVG source file,
convert it to PDF and display that all on the same page. The PDF rendering happens
via some browser plugin preinstalled in the browser or installed by the user or
Streamlit.

Install Streamlit:

    $ pip install streamlit

Run the app:

    $ streamlit run streamlit_app.py
"""

import base64
import io

import requests
import streamlit as st
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg


# config

st.set_page_config(
    page_title="SVG to PDF Converter",
    layout="wide",
    initial_sidebar_state="auto",
)

# sidebar

st.sidebar.header("Settings")
url = "https://upload.wikimedia.org/wikipedia/commons/d/d3/Flag_of_Kiribati.svg"
svg_url = st.sidebar.text_input("SVG URL", value=url)
if st.sidebar.button("Load"):
    pass

# main 

st.title('Streamlit for Svglib')

st.markdown(
    "An interactive [Streamlit](https://streamlit.io) UI for illustrating "
    "examples of [Svg2pdf](https://github.com/deeplook/svglib) (based on "
    "[Reportlab](https://reportlab.com)) in the spirit of the "
    "[Streamlit Geospatial](https://streamlit.gishub.org) collection of "
    "demos. Contributions are welcome on "
    "[GitHub](https://github.com/deeplook/streamlit-svglib/)."
)

pdf_content = b""
col1, col2 = st.columns(2)
with col1:
    with st.expander("SVG"):
        svg_code = ""
        if svg_url:
            svg_code = requests.get(svg_url).content
        svg = st.text_area("Code", value=svg_code.decode("utf-8"), height=400)
        st.markdown(
            "Paste SVG code above or edit it and click below "
            "to convert it!"
        )
        if st.button("Convert", key=2):
            if svg:
                drawing = svg2rlg(io.BytesIO(svg.encode("utf-8")))
                pdf_content = renderPDF.drawToString(drawing)
with col2:
    with st.expander("PDF"):
        if pdf_content:
            base64_pdf = base64.b64encode(pdf_content).decode("utf-8")
            pdf_display = (
                f'<embed src="data:application/pdf;base64,{base64_pdf}" '
                'width="500" height="400" type="application/pdf">'
            )
            st.markdown(pdf_display, unsafe_allow_html=True)
