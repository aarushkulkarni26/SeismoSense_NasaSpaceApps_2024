import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from obspy import read
from datetime import datetime, timedelta
from scipy import signal
from matplotlib import cm

# Set up page configuration
st.set_page_config(
    page_title="Seismic Moonquake Detection",
    page_icon="🌕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and Introduction
st.title("🌕 Seismic Moonquake Detection App")
st.write("Welcome to the Seismic Moonquake Detection platform! This tool analyzes Apollo 12 seismic data and detects moonquakes in real time.")

# Sidebar: File upload for seismic data
st.sidebar.header("Upload Seismic Data")
uploaded_file = st.sidebar.file_uploader("Choose a seismic data file (CSV or MSEED format)", type=["csv", "mseed"])

# Sidebar: Detection parameters
st.sidebar.header("Detection Parameters")
threshold = st.sidebar.slider("Moonquake Detection Threshold", min_value=0.0, max_value=10.0, value=3.0, step=0.1)
sensitivity = st.sidebar.slider("Sensitivity", min_value=0.1, max_value=1.0, value=0.5)

# Sidebar: Filter options
st.sidebar.header("Filter Options")
min_freq = st.sidebar.slider("Minimum Frequency (Hz)", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
max_freq = st.sidebar.slider("Maximum Frequency (Hz)", min_value=0.5, max_value=2.0, value=0.5, step=0.1)

# Main area: If file is uploaded, show data preview and process data
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
        st.subheader("📊 Seismic Data Overview")
        st.write("Here’s a preview of the seismic data you uploaded:")
        st.dataframe(data.head())

        # Extract time and amplitude columns
        csv_times = np.array(data['time_rel(sec)'])
        csv_data = np.array(data['velocity(m/s)'])
        
        # Plot seismic data
        st.subheader("🌍 Seismic Wave Data Visualization")
        fig, ax = plt.subplots()
        ax.plot(csv_times, csv_data, label="Seismic Wave")
        ax.set_title("Seismic Waveform Over Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Velocity (m/s)")
        plt.axhline(y=threshold, color='r', linestyle='--', label=f"Threshold = {threshold}")
        ax.legend()
        st.pyplot(fig)

        # Moonquake Detection Logic
        st.subheader("🌑 Moonquake Detection")
        st.write("Detecting moonquakes based on the selected threshold and sensitivity.")
        moonquakes = data[data["velocity(m/s)"] > threshold]
        
        if len(moonquakes) > 0:
            st.success(f"Detected {len(moonquakes)} potential moonquakes!")
            st.dataframe(moonquakes)
        else:
            st.warning("No moonquakes detected based on the current threshold.")

        # Save results to CSV option
        if st.button("Download Detected Moonquakes"):
            moonquakes.to_csv("detected_moonquakes.csv", index=False)
            st.write("Results saved as `detected_moonquakes.csv`.")
    
    elif uploaded_file.name.endswith('.mseed'):
        st.subheader("📊 Miniseed File Analysis")
        # Read Miniseed file
        st_miniseed = read(uploaded_file)
        tr = st_miniseed[0]  # Assuming single trace
        tr_times = tr.times()
        tr_data = tr.data

        # Plot original seismic data from Miniseed
        fig, ax = plt.subplots()
        ax.plot(tr_times, tr_data)
        ax.set_title("Seismic Waveform from Miniseed")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Velocity (m/s)")
        st.pyplot(fig)

        # Filter data using a bandpass filter
        st.subheader("📉 Filtered Seismic Wave Data")
        st.write(f"Filtering the data between {min_freq} Hz and {max_freq} Hz.")
        tr_filtered = tr.copy()
        tr_filtered.filter('bandpass', freqmin=min_freq, freqmax=max_freq)
        tr_times_filtered = tr_filtered.times()
        tr_data_filtered = tr_filtered.data

        # Plot filtered seismic data
        fig, ax = plt.subplots()
        ax.plot(tr_times_filtered, tr_data_filtered)
        ax.set_title(f"Filtered Seismic Data ({min_freq}-{max_freq} Hz)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Filtered Velocity (m/s)")
        st.pyplot(fig)

        # Moonquake Detection in filtered data
        st.subheader("🌑 Moonquake Detection in Filtered Data")
        moonquakes_filtered = tr_filtered.data > threshold
        
        if any(moonquakes_filtered):
            st.success(f"Detected potential moonquakes in filtered data!")
        else:
            st.warning("No moonquakes detected in the filtered data.")

# Footer
st.write("---")
st.write("🌕 This app is part of a lunar seismic project aimed at improving the detection and analysis of moonquakes using advanced seismic data processing techniques.")

# Style: CSS for customizations
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)
