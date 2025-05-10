import streamlit as st
import os
from downloader import YouTubeDownloader
from utils import validate_url, create_output_dir, get_human_readable_size

# Page config
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎥",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            background-color: #FF0000;
            color: white;
        }
        .stButton>button:hover {
            background-color: #CC0000;
            color: white;
        }
        .download-header {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .success-message {
            padding: 1rem;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .error-message {
            padding: 1rem;
            background-color: #f44336;
            color: white;
            border-radius: 5px;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Create downloads directory
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
create_output_dir(DOWNLOAD_DIR)

# Header
st.markdown('<div class="download-header"><h1>📥 YouTube Downloader</h1></div>', unsafe_allow_html=True)

# Initialize session state for download history
if 'download_history' not in st.session_state:
    st.session_state.download_history = []

# Main form
with st.form("download_form"):
    url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        format_type = st.selectbox(
            "Format",
            options=["MP4", "MP3"],
            index=0
        )
    
    with col2:
        quality = st.selectbox(
            "Quality",
            options=["Best", "High", "Medium", "Low"],
            index=1
        )
    
    submit_button = st.form_submit_button("Download")

if submit_button:
    if not url:
        st.error("Please enter a YouTube URL")
    elif not validate_url(url):
        st.error("Please enter a valid YouTube URL")
    else:
        try:
            with st.spinner("Downloading..."):
                downloader = YouTubeDownloader(
                    url=url,
                    format_type=format_type.lower(),
                    output_dir=DOWNLOAD_DIR,
                    quality=quality.lower()
                )
                
                success = downloader.download()
                
                if success:
                    # Add to download history
                    st.session_state.download_history.insert(0, {
                        'url': url,
                        'format': format_type,
                        'quality': quality
                    })
                    st.markdown('<div class="success-message">✅ Download completed successfully!</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Download failed!</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.markdown(f'<div class="error-message">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

# Download History
if st.session_state.download_history:
    st.markdown("### 📋 Download History")
    for item in st.session_state.download_history:
        with st.expander(f"📥 {item['url'][:50]}..."):
            st.write(f"Format: {item['format']}")
            st.write(f"Quality: {item['quality']}")

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. Paste a YouTube video URL in the input field
    2. Select your preferred format (MP4 for video, MP3 for audio)
    3. Choose the quality level
    4. Click the Download button
    5. Wait for the download to complete
    
    **Note:** Downloads are saved in the 'downloads' folder
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Python")