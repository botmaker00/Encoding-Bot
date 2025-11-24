from os import getenv, makedirs
import logging
import os
import time
from io import BytesIO, StringIO
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pyrogram import Client

# Load env file if exists
if os.path.exists('config.env'):
    load_dotenv('config.env')

# Bot Start Time
botStartTime = time.time()

# ==================== CONFIG VARIABLES ====================

# Telegram API Credentials
API_ID = int(getenv("API_ID", "0"))                    # Must be int
API_HASH = getenv("API_HASH", "").strip()
BOT_TOKEN = getenv("BOT_TOKEN", "").strip()

# Database & Session
MONGO_URI = getenv("MONGO_URI")
SESSION_NAME = getenv("SESSION_NAME", "VideoEncoderBot")

# Folders
DOWNLOAD_DIR = getenv("DOWNLOAD_DIR", "VideoEncoder/downloads/").rstrip("/")
ENCODE_DIR = getenv("ENCODE_DIR", "VideoEncoder/encodes/").rstrip("/")
DRIVE_DIR = getenv("DRIVE_DIR", "").strip()
INDEX_URL = getenv("INDEX_URL", "").strip()

OWNER_ID = getenv("OWNER_ID")                     # Example: 123456789

SUDO_USERS = getenv("SUDO_USERS")                 # Space separated IDs
EVERYONE_CHATS = getenv("EVERYONE_CHATS")         # Chats where everyone can use bot

# Log Channel (Optional, can be user/channel/group ID)
LOG_CHANNEL_RAW = getenv("LOG_CHANNEL", "").strip()
if LOG_CHANNEL_RAW and LOG_CHANNEL_RAW.lstrip("-").isdigit():
    LOG_CHANNEL = int(LOG_CHANNEL_RAW)
else:
    LOG_CHANNEL = None  # Will send logs to OWNER if not set

# Progress Format
PROGRESS = """
• {0} of {1}
• Speed: {2}/s
• ETA: {3}
"""

# Supported Video Mimetypes
video_mimetype = [
    "video/x-flv", "video/mp4", "application/x-mpegURL", "video/MP2T",
    "video/3gpp", "video/quicktime", "video/x-msvideo", "video/x-ms-wmv",
    "video/x-matroska", "video/webm", "video/x-m4v", "video/mpeg"
]

# Utility: In-memory file (for thumbnails, etc.)
def memory_file(name=None, contents=None, *, bytes=True):
    if isinstance(contents, str) and bytes:
        contents = contents.encode("utf-8")
    file = BytesIO() if bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file

# ==================== CREATE DIRECTORIES ====================
for directory in [DOWNLOAD_DIR, ENCODE_DIR, "VideoEncoder/utils/extras"]:
    if not os.path.isdir(directory):
        makedirs(directory, exist_ok=True)

# ==================== LOGGING SETUP ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "VideoEncoder/utils/extras/logs.txt",
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=20,
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

# Reduce noise from libraries
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("pymongo").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

# ==================== PYROGRAM CLIENT ====================
app = Client(
    name=SESSION_NAME,
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins"),
    workdir=".",                     # Session file yahin save hoga
    sleep_threshold=30,
    max_concurrent_transmissions=16,
    workers=32,
    ipv6=False
)

# Optional: Startup message
LOGGER.info("Video Encoder Bot Configuration Loaded Successfully!")
if LOG_CHANNEL:
    LOGGER.info(f"Log Channel Set: {LOG_CHANNEL}")
else:
    LOGGER.info(f"Log Channel Not Set – Logs will be sent to OWNER ({OWNER_ID[0]})")
