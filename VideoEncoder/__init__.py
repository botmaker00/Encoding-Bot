
from os import getenv
import logging
import os
import time
from io import BytesIO, StringIO
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from pyrogram import Client

botStartTime = time.time()

if os.path.exists('config.env'):
    load_dotenv('config.env')

# Variables

api_id = int(getenv("API_ID"))
api_hash = getenv("API_HASH")
bot_token = getenv("BOT_TOKEN")

database = getenv("MONGO_URI")
session = getenv("SESSION_NAME")

drive_dir = getenv("DRIVE_DIR")
index = getenv("INDEX_URL")

download_dir = getenv("DOWNLOAD_DIR")
encode_dir = getenv("ENCODE_DIR")

owner = list(set(int(x) for x in getenv("OWNER_ID").split()))
sudo_users = list(set(int(x) for x in getenv("SUDO_USERS").split()))
everyone = list(set(int(x) for x in getenv("EVERYONE_CHATS").split()))
all = everyone + sudo_users + owner

try:
    log = int(getenv("LOG_CHANNEL"))
except:
    log = owner
    print('Fill log or give user/channel/group id atleast!')


data = []

PROGRESS = """
• {0} of {1}
• Speed: {2}
• ETA: {3}
"""

video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "application/x-mpegURL",
    "video/MP2T",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg"
]

def memory_file(name=None, contents=None, *, bytes=True):
    if isinstance(contents, str) and bytes:
        contents = contents.encode()
    file = BytesIO() if bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file

# Check Folder
if not os.path.isdir(download_dir):
    os.makedirs(download_dir)
if not os.path.isdir(encode_dir):
    os.makedirs(encode_dir)

if not os.path.isdir('VideoEncoder/utils/extras'):
    os.makedirs('VideoEncoder/utils/extras')

# Download multilingual fonts for Devanagari/Hindi and English to prevent "tofu" boxes
def download_multilingual_fonts():
    import urllib.request
    fonts_dir = os.path.expanduser('~/.fonts')
    if not os.path.isdir(fonts_dir):
        os.makedirs(fonts_dir)

    font_urls = {
        "NotoSansDevanagari-Regular.ttf": "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf",
        "NotoSansDevanagari-Bold.ttf": "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Bold.ttf",
        "NotoSans-Regular.ttf": "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf",
        "NotoSans-Bold.ttf": "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Bold.ttf"
    }

    for filename, url in font_urls.items():
        filepath = os.path.join(fonts_dir, filename)
        if not os.path.exists(filepath):
            try:
                print(f"Downloading font: {filename}...")
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                print(f"Failed to download font {filename}: {e}")

    # Run fc-cache to register the newly added fonts
    try:
        os.system("fc-cache -f")
    except Exception as e:
        print(f"fc-cache failed: {e}")

try:
    download_multilingual_fonts()
except Exception as e:
    print(f"Failed to setup fonts: {e}")

# the logging things
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            'VideoEncoder/utils/extras/logs.txt',
            backupCount=20,
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("pymongo").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

# Client
app = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
    plugins={'root': os.path.join(__package__, 'plugins')},
    sleep_threshold=30,
    max_concurrent_transmissions=16,
    workers=32,
    ipv6=False)
