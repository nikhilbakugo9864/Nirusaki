import os, logging, asyncio
from logging.handlers import RotatingFileHandler
from pyrogram import Client
from dotenv import load_dotenv
from pyromod import listen
import pymongo
from pymongo import MongoClient


if os.path.exists('config.env'):
  load_dotenv('config.env')
try:
  os.makedirs('encodes/')
  os.makedirs('temp/')
  os.makedirs('downloads/')
except:
   pass


class Config(object):
  API_ID = int(os.environ.get("API_ID", "14874438"))
  API_HASH = str(os.environ.get("API_HASH", "9d75f325568b6297204ef261040595f7"))
  BOT_TOKEN = str(os.environ.get("BOT_TOKEN", "5387861278:AAF3CtbOu298iG522AY615UqtvxrDMT_XsU"))
  DATABASE_URL = str(os.environ.get("DATABASE_URL", "mongodb+srv://Venkat3823:Venkat3823@cluster0.ig0oc9y.mongodb.net/?retryWrites=true&w=majority"))
  USERNAME = str(os.environ.get("BOT_USERNAME", "5387861278"))
  LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001774034291"))
  AUTH_USERS = list(set(int(x) for x in os.environ.get("AUTH_USERS", "5178332815").split()))
  ADMIN = list(set(int(x) for x in os.environ.get("ADMIN", "5629750139").split()))
  OWNER = list(set(int(x) for x in os.environ.get("OWNER", "5178332815").split()))
  TEMP = 'temp/'
  DOWNLOAD_DIR = str(os.environ.get("DOWNLOAD_DIR"))


LOG_FILE_NAME = "Logs.txt"


if os.path.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, "r+") as f_d:
        f_d.truncate(0)


cluster = MongoClient(Config.DATABASE_URL)
db = cluster[Config.USERNAME]
collection = db["data"]
queue = db["queue"]
words = db["words"]


data = []
list_handler = []


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=2097152000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
LOGS = logging.getLogger(__name__)


bot = Client("Encoder", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, workers=2)


if not Config.DOWNLOAD_DIR.endswith("/"):
  Config.DOWNLOAD_DIR = str() + "/"
if not os.path.isdir(Config.DOWNLOAD_DIR):
  os.makedirs(Config.DOWNLOAD_DIR)
