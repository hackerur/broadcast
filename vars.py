import os, sys
from dotenv import load_dotenv

def makelist_(str_input):
    str_list = str_input.split(" ")
    int_list = []
    for x in str_list:
        int_list.append(int(x))
    return int_list

if os.path.exists(".env"):
    load_dotenv(".env")

print("Bot - [INFO]: Cheking Variables....")
API_ID = int(os.getenv("API_ID", ""))
if not API_ID:
    print("Bot - [INFO]: Fill API_ID!")
    sys.exit()

API_HASH = os.getenv("API_HASH", "")
if not API_HASH:
    print("Bot - [INFO]: Fill API_HASH!")
    sys.exit()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    print("Bot - [INFO]: Fill BOT_TOKEN!")
    sys.exit()

SUDO_USERS = makelist_(os.getenv("SUDO_USERS", ""))
if not SUDO_USERS:
    print("Bot - [INFO]: Fill SUDO_USERS!")
    sys.exit()

DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    print("Bot - [INFO]: Fill DATABASE_URL!")
    sys.exit()

if 'postgres' in DATABASE_URL and 'postgresql' not in DATABASE_URL:
      DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")

print("Bot - [INFO]: Got all variables ✓")
