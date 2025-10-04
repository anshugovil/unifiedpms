"""
Utility functions for the Streamlit Trade Processing App
Handles environment detection, directory management, and session state
"""

import os
import streamlit as st
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def is_streamlit_cloud():
    """Check if running on Streamlit Cloud"""
    return os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud" or \
           os.environ.get("IS_STREAMLIT_CLOUD") == "true" or \
           not os.path.exists(os.path.expanduser("~/.streamlit"))


def ensure_directories():
    """Ensure required directories exist - skip on Streamlit Cloud"""
    if is_streamlit_cloud():
        return  # Skip directory creation on cloud

    dirs = ["output", "output/stage1", "output/stage2", "output/expiry_deliveries", "temp"]
    for dir_path in dirs:
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create directory {dir_path}: {e}")


def get_temp_dir():
    """Get temporary directory that works on both desktop and Streamlit Cloud"""
    import tempfile
    temp_system = tempfile.gettempdir()
    if os.access(temp_system, os.W_OK):
        return Path(temp_system)

    # Fallback to /tmp on Unix-like systems
    if Path("/tmp").exists() and os.access("/tmp", os.W_OK):
        return Path("/tmp")

    # Last resort - create local temp directory
    try:
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        return temp_dir
    except:
        # If all else fails, use current directory
        return Path(".")


def get_output_path(filename: str, subfolder: str = "") -> str:
    """
    Get output file path that works on both desktop and Streamlit Cloud
    On cloud, use temporary directory; on desktop, use output folder
    """
    if is_streamlit_cloud():
        # On cloud, use temp directory
        temp_dir = get_temp_dir()
        if subfolder:
            output_dir = temp_dir / subfolder.replace("output/", "")
        else:
            output_dir = temp_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir / filename)
    else:
        # On desktop, use regular output folder
        if subfolder:
            output_dir = Path(subfolder)
        else:
            output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir / filename)


def initialize_session_state():
    """Initialize all session state variables"""
    # Stage completion flags
    if 'stage1_complete' not in st.session_state:
        st.session_state.stage1_complete = False
    if 'stage2_complete' not in st.session_state:
        st.session_state.stage2_complete = False
    if 'deliverables_complete' not in st.session_state:
        st.session_state.deliverables_complete = False
    if 'recon_complete' not in st.session_state:
        st.session_state.recon_complete = False
    if 'expiry_deliveries_complete' not in st.session_state:
        st.session_state.expiry_deliveries_complete = False
    if 'broker_recon_complete' not in st.session_state:
        st.session_state.broker_recon_complete = False

    # Output storage
    if 'stage1_outputs' not in st.session_state:
        st.session_state.stage1_outputs = {}
    if 'stage2_outputs' not in st.session_state:
        st.session_state.stage2_outputs = {}
    if 'dataframes' not in st.session_state:
        st.session_state.dataframes = {}
    if 'deliverables_data' not in st.session_state:
        st.session_state.deliverables_data = {}
    if 'recon_data' not in st.session_state:
        st.session_state.recon_data = {}
    if 'expiry_delivery_files' not in st.session_state:
        st.session_state.expiry_delivery_files = {}
    if 'expiry_delivery_results' not in st.session_state:
        st.session_state.expiry_delivery_results = {}

    # ACM mapper
    if 'acm_mapper' not in st.session_state:
        st.session_state.acm_mapper = None

    # File caching
    if 'cached_position_file' not in st.session_state:
        st.session_state.cached_position_file = None
    if 'cached_mapping_file' not in st.session_state:
        st.session_state.cached_mapping_file = None
    if 'cached_position_password' not in st.session_state:
        st.session_state.cached_position_password = None

    # Account validation
    if 'account_validator' not in st.session_state:
        try:
            from account_validator import AccountValidator
            st.session_state.account_validator = AccountValidator()
        except ImportError:
            st.session_state.account_validator = None
    if 'detected_account' not in st.session_state:
        st.session_state.detected_account = None
    if 'account_validated' not in st.session_state:
        st.session_state.account_validated = False

    # Processing mode
    if 'processing_mode' not in st.session_state:
        st.session_state.processing_mode = 'EOD'

    # Broker reconciliation
    if 'enhanced_clearing_file' not in st.session_state:
        st.session_state.enhanced_clearing_file = None
    if 'final_enhanced_clearing_file' not in st.session_state:
        st.session_state.final_enhanced_clearing_file = None
    if 'broker_recon_result' not in st.session_state:
        st.session_state.broker_recon_result = None


def apply_custom_css():
    """Apply custom CSS styling to the app"""
    st.markdown("""
        <style>
        .main { padding: 0rem 1rem; }
        h1 { color: #1f77b4; }
        .stDownloadButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
        }
        .stage-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
        }
        .info-box {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
        }
        .expiry-card {
            background-color: #f8f9fa;
            border: 2px solid #007bff;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        .deliverable-header {
            background-color: #007bff;
            color: white;
            padding: 8px;
            border-radius: 4px;
            margin: 5px 0;
        }
        </style>
        """, unsafe_allow_html=True)
