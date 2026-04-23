# adixe_bot.py
import asyncio
import json
import os
import sys
import subprocess
import time
import logging
import tempfile
from datetime import datetime, timedelta
from collections import defaultdict

# ---------- AUTO INSTALL DEPENDENCIES ----------
def install_package(package):
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

required = ["python-telegram-bot", "gtts"]
for pkg in required:
    install_package(pkg)

from telegram import Update, InputFile
from telegram.ext import (
    Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
)
from gtts import gTTS

# ---------- CONFIG ----------
TOKENS = [ 
"8601525560:AAFcZjPxPzVKDOvIJ4wiX_TPpw9Q0dsOiZE",
"8756564561:AAE9UXtg5nf9vy2tccbUErB-5myxJxQMPqw",
]

OWNER_ID = 6028490642
SUDO_FILE = "sudo.json"
MUTE_FILE = "mute_data.json"
START_TIME = time.time()
COMMAND_COUNTER = 0

GCNC_TEMPLATE = [
    "🎀𓂃 ࣪˖ ִֶָ HATER 𝐑ᴀɴᴅɪᴋᴇ𓂃 ࣪˖ ִֶָ🎀",
    "🎀𓂃 ࣪˖ ִֶָ HATER 𝐊ᴀʟᴡᴇ 𝐁ɪʜᴀʀɪ ࣪˖ ִֶָ🎀",
    "🎀𓂃 ࣪˖ ִֶָ  HATER 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐊ᴀ 𝐒ᴀʀ 𝐏ʜᴏᴅ ᴅᴜɴɢᴀ ࣪˖ ִֶָ🎀",
    "🎀𓂃 ࣪˖ ִֶָ HATER 𝐋ᴇꜱʙɪᴀɴ 𝐊ɪ 𝐏ᴇᴅᴀʏɪꜱʜ ࣪˖ ִֶָ🎀",
    "🎀𓂃 ࣪˖ ִֶָ HATER 𝐑ᴀᴋʜᴀᴇʟ 𝐊ɪ 𝐀ᴜʟᴀᴅ ࣪˖ ִֶָ🎀",
    "🎀𓂃 ࣪˖ ִֶָ HATER 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐁ꜱ ADIXE 𝐂ʜᴏᴅᴇɢᴀ ࣪˖ ִֶָ🎀",
    "🎀𓂃 ࣪˖ ִֶָ HATER 𝐍ᴀɴɪ 𝐊ᴇ 𝐁ʜᴏꜱᴅᴇ ࣪˖ ִֶָ🎀",
    "🎀𓂃 ࣪˖ ִֶָ HATER 𝐔ᴛʜ 𝐏ɪʟʟᴇ 𝐊ɪᴛɴᴀ 𝐒ᴏʏᴇɢᴀ𓂃 ࣪˖ ִֶָ🎀",
    "🎀𓂃 ࣪˖ ִֶָ HATER 𝐓ᴇʀɪ 𝐍ᴀɴɪ 𝐊ɪ 𝐌ᴀᴀ 𝐑ɴᴅʏ𓂃 ࣪˖ ִֶָ🎀"
    
]

gcncemo_EMOJIS = [
    "😋","😝","😜","🤪","😑","🤫","🤭","🥱","🤗","😡","😠","😤",
    "😮‍💨","🙄","😒","🥶","🥵","🤢","😎","🥸",
    "😹","💫","😼","😽","🙀","😿","😾",
    "🙈","🙉","🙊",
    "⭐","🌟","✨","⚡","💥","💨",
    "💛","💙","💜","🤎","🤍","💘","💝"
]

GSPAM_BLOCK = """{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌸𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩❣️𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩❤️𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💛𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💜𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💞𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💔𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💙𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🩸𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩❤️‍🔥𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌺𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌺𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌷𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🩶𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌺𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💌𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌸𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🧡𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💓𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💜𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🩶𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💟𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💙𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🩷𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💛𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💙𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🤍𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💖𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💘𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌺𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩❤️‍🔥𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💙𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💘𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💔𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🥀𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💗𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🤍𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🩵𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🖤𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩❣️𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🫀𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🩵𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🎀𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💓𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💘𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌸𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💜𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💛𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌸𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🫀𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩❤️‍🔥𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💌𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💓𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🌸𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💓𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩🥀𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩💞𓆪
{ʜᴀᴛᴇʀ} 𝐀ᴘᴘᴄɪ 𝐌ᴏᴍ 𝐂ʜᴜᴅᴇ 12 𝐁ᴀᴊᴇ 𝐃ʜᴀᴋᴀ 𝐃ʜᴀᴋ !! 𓆩❤️𓆪"""

FLAGSPAM_BLOCK = """𓆩 🏴‍☠️𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩 🏴‍☠️𓆪
















𓆩 🏴‍☠️𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩 🏴‍☠️𓆪
𓆩🇮🇳𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇮🇳𓆪



















































𓆩🇮🇳𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇮🇳𓆪
𓆩🇦🇷𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇦🇷𓆪























































𓆩🇦🇷𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇦🇷𓆪
𓆩🇦🇺𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇦🇺𓆪



















































𓆩🇦🇺𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇦🇺𓆪
𓆩🇧🇭𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇧🇭𓆪





















































𓆩🇧🇭𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇧🇭𓆪
𓆩🇫🇷𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇫🇷𓆪



















































𓆩🇫🇷𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇫🇷𓆪
𓆩🇯🇵𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇯🇵𓆪





















































𓆩🇯🇵𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇯🇵𓆪
𓆩🇨🇼𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇨🇼𓆪





















































𓆩🇨🇼𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇨🇼𓆪
𓆩🇱🇰𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇱🇰𓆪






















































𓆩🇱🇰𓆪##HATER#𝗥𝗮𝗻𝗗𝗶#𝗞𝗲#𝗟𝗮𝗱𝗖𝗲##𝗧𝗺𝗞𝗰#𝗙𝗮𝗮𝗗#𝗗𝘂𝗻𝗴𝗔*####𓆩🇱🇰𓆪"""

TMKCSPAM_BLOCK = """HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️

HATER ᴛᴍᴋᴄ 🕊️"""

# Emoji lists
VEHICLE_EMOJIS = ["🚗","🚕","🚙","🚌","🚎","🏎️","🚓","🚑","🚒","🚐","🛻","🚚","🚛","🚜","🛵","🏍️","🛺","🚲","🛴","🛹","🚁","🛩️","✈️","🛫","🛬","🚀","🛸","🚤","🛶","⛵"]
FLAG_EMOJIS = ["🇮🇳","🇺🇸","🇬🇧","🇨🇦","🇦🇺","🇯🇵","🇰🇷","🇩🇪","🇫🇷","🇮🇹","🇪🇸","🇧🇷","🇷🇺","🇨🇳","🇿🇦","🇲🇽","🇦🇷","🇸🇦","🇹🇷","🇳🇬","🇵🇰","🇧🇩","🇮🇩","🇵🇭","🇻🇳","🇹🇭","🇲🇾","🇸🇬","🇪🇬","🇰🇪"]
MOON_EMOJIS = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘","🌙","🌚","🌛","🌜","🌝","🌞","⭐","🌟","🌠","☀️","☁️","⛅"]
PET_EMOJIS = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐸","🐵","🐔","🐧","🐦","🐤","🐣","🐺","🐗","🐴","🦄","🐝","🐛","🦋","🐌","🐞","🐜"]
PLANT_EMOJIS = ["🌿","🍀","🌱","🌲","🌳","🌴","🌵","🌾","🌺","🌸","🌼","🌻","🌹","🌷","🥀","🍂","🍁","🌽","🌶️","🍄","🌰","🎋","🎍","🍃","🍂"]
FOOD_EMOJIS = ["🍕","🍔","🍟","🌭","🍿","🥓","🥚","🍳","🧇","🥞","🧈","🍞","🥐","🥨","🥯","🥖","🧀","🥗","🥙","🌮","🌯","🥫","🍖","🍗","🥩","🍠","🥟","🥠","🍱"]
FLOWER_EMOJIS = ["🌸","🌺","🌻","🌹","🌷","🌼","💐","🥀","🌾","🌿","🍀","🌱","🍁","🍂","🌵","🌴","🎋","🎍","💮","🏵️"]
HEART_EMOJIS = ["❤️","🧡","💛","💚","💙","💜","🖤","🤍","🤎","💔","❤️‍🔥","❤️‍🩹","💕","💞","💓","💗","💖","💘","💝","💟"]
ANIMAL_EMOJIS = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐸","🐵","🐔","🐧","🐦","🐤","🐣","🐺","🐗","🐴","🦄","🦓","🦌","🐪","🐫","🐘","🦏","🦛","🐀","🐿️","🦔","🐉","🐲","🐍","🦎"]
SPORT_EMOJIS = ["⚽","🏀","🏈","⚾","🥎","🎾","🏐","🏉","🥏","🎱","🪀","🏓","🏸","🏒","🏑","🥍","🏏","⛳","🏹","🥊","🥋","⛸️","🛼","🛹","🛷","⛷️","🏂","🏋️","🤸","⛹️"]
WEATHER_EMOJIS = ["☀️","☁️","⛅","⛈️","🌤️","🌥️","🌦️","🌧️","🌨️","🌩️","🌪️","🌫️","🌬️","🌈","☔","⚡","❄️","💧","💨","🌊"]

# ---------- GLOBAL STATE ----------
if os.path.exists(SUDO_FILE):
    with open(SUDO_FILE, "r") as f:
        data = json.load(f)
        if isinstance(data, dict):
            SUDO_USERS = {int(k): v for k, v in data.items()}
        else:
            SUDO_USERS = {int(x): datetime.now().strftime("%Y-%m-%d %H:%M:%S") for x in data}
else:
    SUDO_USERS = {OWNER_ID: datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    with open(SUDO_FILE, "w") as f: json.dump(SUDO_USERS, f)

def save_sudo():
    with open(SUDO_FILE, "w") as f: json.dump(SUDO_USERS, f)

if os.path.exists(MUTE_FILE):
    with open(MUTE_FILE, "r") as f:
        MUTE_DATA = json.load(f)
else:
    MUTE_DATA = {}

def save_mute():
    with open(MUTE_FILE, "w") as f: json.dump(MUTE_DATA, f)

def get_mute_state(chat_id):
    chat_id = str(chat_id)
    if chat_id not in MUTE_DATA:
        MUTE_DATA[chat_id] = {"mute_all": False, "muted_users": [], "safe_users": []}
        save_mute()
    return MUTE_DATA[chat_id]

msg_counter = defaultdict(lambda: defaultdict(int))

group_tasks = {}
spam_tasks = {}
photo_tasks = {}
tts_tasks = {}
picspam_tasks = {}
swipe_names = {}
photo_cache = {}
gspam_prefixes = {}
pic_cache = {}

apps, bots = [], []
BURST = 5
DELAY = 1.0

logging.basicConfig(level=logging.INFO)

# ---------- DECORATORS ----------
def count_command(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        global COMMAND_COUNTER
        COMMAND_COUNTER += 1
        return await func(update, context)
    return wrapper

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in SUDO_USERS:
            return await update.message.reply_text("⛔ Access denied. SUDO permission required.")
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != OWNER_ID:
            return await update.message.reply_text("⛔ Access denied. Owner only.")
        return await func(update, context)
    return wrapper

def only_sudo_or_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid != OWNER_ID and uid not in SUDO_USERS:
            return await update.message.reply_text("⛔ Access denied. Owner or SUDO only.")
        return await func(update, context)
    return wrapper

# ---------- HELPER: TTS GENERATION ----------
async def generate_tts_voice(text: str) -> bytes:
    def _gen():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts = gTTS(text=text, lang="en")
            tts.save(tmp.name)
            with open(tmp.name, "rb") as f:
                return f.read()
    return await asyncio.to_thread(_gen)

# ---------- SECTION MANAGER ----------
def get_sections():
    n = len(bots)
    if n == 0:
        return [], []
    mid = (n + 1) // 2
    return bots[:mid], bots[mid:]

# ---------- ROUND-ROBIN WORKERS ----------
async def section_worker(bot, chat_id, section_bots, bot_index_in_section, base_text, mode, rounds):
    gap = DELAY / len(section_bots) if section_bots else DELAY
    idx = 0
    for r in range(rounds):
        for i, b in enumerate(section_bots):
            if b.id == bot.id:
                try:
                    if mode == "text":
                        msg = base_text
                    elif mode == "raid_list":
                        msg = GCNC_TEMPLATE[idx % len(GCNC_TEMPLATE)]
                    elif mode == "emoji_list":
                        msg = f"{base_text} {gcncemo_EMOJIS[idx % len(gcncemo_EMOJIS)]}"
                    elif mode == "swipe":
                        name = base_text.get(chat_id, "") if isinstance(base_text, dict) else base_text
                        msg = f"{name} {GCNC_TEMPLATE[idx % len(GCNC_TEMPLATE)]}"
                    elif mode == "gspam":
                        prefix = gspam_prefixes.get(chat_id, "{ʜᴀᴛᴇʀ}")
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        block = GSPAM_BLOCK.replace("{ʜᴀᴛᴇʀ}", prefix).replace("12", current_time)
                        msg = block
                    elif mode == "flagspam":
                        prefix = gspam_prefixes.get(chat_id, "HATER")
                        msg = FLAGSPAM_BLOCK.replace("HATER", prefix)
                    elif mode == "tmkcspam":
                        prefix = gspam_prefixes.get(chat_id, "HATER")
                        msg = TMKCSPAM_BLOCK.replace("HATER", prefix)
                    else:
                        msg = "Error"
                    await bot.send_message(chat_id, msg)
                    msg_counter[chat_id][bot.id] += 1
                    idx += 1
                except Exception as e:
                    logging.warning(f"Spam error: {e}")
                await asyncio.sleep(gap)

async def section_title_worker(bot, chat_id, section_bots, bot_index_in_section, base, emoji_list, rounds):
    gap = DELAY / len(section_bots) if section_bots else DELAY
    idx = 0
    for r in range(rounds):
        for i, b in enumerate(section_bots):
            if b.id == bot.id:
                try:
                    if emoji_list is GCNC_TEMPLATE:  # raid mode uses HATER placeholder
                        text = GCNC_TEMPLATE[idx % len(GCNC_TEMPLATE)].replace("HATER", base)
                    else:
                        text = f"{base} {emoji_list[idx % len(emoji_list)]}"
                    await bot.set_chat_title(chat_id, text)
                    idx += 1
                except Exception as e:
                    logging.warning(f"Title error: {e}")
                await asyncio.sleep(gap)

async def section_photo_worker(bot, chat_id, section_bots, bot_index_in_section, photo_bytes, rounds):
    gap = DELAY / len(section_bots) if section_bots else DELAY
    for r in range(rounds):
        for i, b in enumerate(section_bots):
            if b.id == bot.id:
                try:
                    await bot.set_chat_photo(chat_id, InputFile(photo_bytes))
                except Exception as e:
                    logging.warning(f"Photo error: {e}")
                await asyncio.sleep(gap)

async def section_picspam_worker(bot, chat_id, section_bots, bot_index_in_section, photo_bytes, rounds):
    gap = DELAY / len(section_bots) if section_bots else DELAY
    for r in range(rounds):
        for i, b in enumerate(section_bots):
            if b.id == bot.id:
                try:
                    await bot.send_photo(chat_id, photo_bytes)
                    msg_counter[chat_id][bot.id] += 1
                except Exception as e:
                    logging.warning(f"Picspam error: {e}")
                await asyncio.sleep(gap)

async def section_tts_worker(bot, chat_id, section_bots, bot_index_in_section, voice_bytes, rounds):
    gap = DELAY / len(section_bots) if section_bots else DELAY
    for r in range(rounds):
        for i, b in enumerate(section_bots):
            if b.id == bot.id:
                try:
                    await bot.send_voice(chat_id, voice_bytes)
                except Exception as e:
                    logging.warning(f"TTS error: {e}")
                await asyncio.sleep(gap)

async def section_orchestrator(chat_id, base_text, mode, emoji_list=None, photo_bytes=None, voice_bytes=None):
    secA, secB = get_sections()
    if not secA and not secB:
        return
    rounds = BURST
    while True:
        tasksA = []
        for i, bot in enumerate(secA):
            if mode == "tts" and voice_bytes:
                task = asyncio.create_task(section_tts_worker(bot, chat_id, secA, i, voice_bytes, rounds))
            elif mode == "picspam" and photo_bytes:
                task = asyncio.create_task(section_picspam_worker(bot, chat_id, secA, i, photo_bytes, rounds))
            elif mode in ["gcnc", "gcncemo"] or emoji_list:
                task = asyncio.create_task(section_title_worker(bot, chat_id, secA, i, base_text, emoji_list or gcncemo_EMOJIS, rounds))
            elif mode == "photo" and photo_bytes:
                task = asyncio.create_task(section_photo_worker(bot, chat_id, secA, i, photo_bytes, rounds))
            else:
                task = asyncio.create_task(section_worker(bot, chat_id, secA, i, base_text, mode, rounds))
            tasksA.append(task)
        await asyncio.gather(*tasksA)
        tasksB = []
        for i, bot in enumerate(secB):
            if mode == "tts" and voice_bytes:
                task = asyncio.create_task(section_tts_worker(bot, chat_id, secB, i, voice_bytes, rounds))
            elif mode == "picspam" and photo_bytes:
                task = asyncio.create_task(section_picspam_worker(bot, chat_id, secB, i, photo_bytes, rounds))
            elif mode in ["gcnc", "gcncemo"] or emoji_list:
                task = asyncio.create_task(section_title_worker(bot, chat_id, secB, i, base_text, emoji_list or gcncemo_EMOJIS, rounds))
            elif mode == "photo" and photo_bytes:
                task = asyncio.create_task(section_photo_worker(bot, chat_id, secB, i, photo_bytes, rounds))
            else:
                task = asyncio.create_task(section_worker(bot, chat_id, secB, i, base_text, mode, rounds))
            tasksB.append(task)
        await asyncio.gather(*tasksB)

# ---------- START FUNCTIONS ----------
async def start_spam_for_chat(chat_id, base_text, mode):
    if chat_id in spam_tasks:
        return
    task = asyncio.create_task(section_orchestrator(chat_id, base_text, mode))
    spam_tasks[chat_id] = task

async def start_title_loop(chat_id, base, mode):
    if chat_id in group_tasks:
        return
    emoji_list = GCNC_TEMPLATE if mode == "raid" else gcncemo_EMOJIS
    task = asyncio.create_task(section_orchestrator(chat_id, base, "gcnc", emoji_list=emoji_list))
    group_tasks[chat_id] = task

async def start_title_loop_with_emojis(chat_id, base, emoji_list):
    if chat_id in group_tasks:
        return
    task = asyncio.create_task(section_orchestrator(chat_id, base, "gcnc", emoji_list=emoji_list))
    group_tasks[chat_id] = task

async def start_photo_loop(chat_id, photo_bytes):
    if chat_id in photo_tasks:
        return
    task = asyncio.create_task(section_orchestrator(chat_id, None, "photo", photo_bytes=photo_bytes))
    photo_tasks[chat_id] = task

async def start_tts_loop(chat_id, voice_bytes):
    if chat_id in tts_tasks:
        return
    task = asyncio.create_task(section_orchestrator(chat_id, None, "tts", voice_bytes=voice_bytes))
    tts_tasks[chat_id] = task

async def start_picspam_loop(chat_id, photo_bytes):
    if chat_id in picspam_tasks:
        return
    task = asyncio.create_task(section_orchestrator(chat_id, None, "picspam", photo_bytes=photo_bytes))
    picspam_tasks[chat_id] = task

# ---------- MUTE HANDLER ----------
async def mute_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    chat_id = str(update.message.chat_id)
    user_id = update.message.from_user.id
    if user_id == OWNER_ID:
        return
    state = get_mute_state(chat_id)
    if user_id in state.get("safe_users", []):
        return
    if state.get("mute_all", False) or user_id in state.get("muted_users", []):
        try:
            await update.message.delete()
        except:
            pass

# ---------- COMMANDS ----------
@count_command
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ADIXE Bot is online.\nUse /menu to view available commands.")

@count_command
async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = (
        "╔══════════════════════════════════╗\n"
        "      ✦  ADIXE BOT v1  ✦\n"
        "        「 ᴘᴏᴡᴇʀ ᴍᴏᴅᴇ ᴏɴ 」\n"
        "╚══════════════════════════════════╝\n"
        "        › type /help anytime\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ 📌  G C   T I T L E   L O O P S\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /gcnc <text>      → 🔥 Raid text title loop\n"
        "• /gcncemo <text>     → 😋 Emoji title loop\n"
        "• /caremo <text>    → 🚗 Vehicle emoji loop\n"
        "• /flagemo <text>   → 🇮🇳 Flag emoji loop\n"
        "• /moonemo <text>   → 🌙 Moon emoji loop\n"
        "• /petemo <text>    → 🐶 Pet emoji loop\n"
        "• /plantemo <text>  → 🌿 Plant emoji loop\n"
        "• /foodemo <text>   → 🍕 Food emoji loop\n"
        "• /floweremo <text> → 🌸 Flower emoji loop\n"
        "• /heartemo <text>  → ❤️ Heart emoji loop\n"
        "• /animalemo <text> → 🐾 Animal emoji loop\n"
        "• /sportemo <text>  → ⚽ Sport emoji loop\n"
        "• /weatheremo <text> → ☁️ Weather emoji loop\n"
        "• /stopgcnc         → ⏹️ Stop title loop\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ 🎯  S P A M   C O M M A N D S\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /spam <text>      → 💬 Simple continuous spam\n"
        "• /targetslide      → 🎯 Raid text spam\n"
        "• /slidespam        → 📜 Slide style spam\n"
        "• /swipe <name>     → ⚡ Swipe name spam\n"
        "• /gspam [prefix]   → ⏱️ G‑Spam block (time auto)\n"
        "• /flagspam <text>  → 🏁 Flag block spam\n"
        "• /tmkcspam <text>  → 🔨 TMKC block spam\n"
        "• /picspam (reply)  → 🖼️ Continuous photo spam\n"
        "• /stopspam         → ⏹️ Stop spam in this chat\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ 💥  C O M B O   A T T A C K\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /fuck <text> (reply photo optional)\n"
        "     → 🔄 Alternates: Title → GSPAM → DP\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ 🖼  P H O T O   L O O P\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /startphoto (reply) → 🖼️ Start DP loop\n"
        "• /stopphoto          → ⏹️ Stop DP loop\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ 🔇  M U T E   S Y S T E M\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /mute (reply / id) → 🔇 Mute specific user\n"
        "• /mute (no args)    → 🔇 Mute entire group\n"
        "• /speak             → 🔊 Unmute all\n"
        "• /safe (reply)      → ✅ Exempt user from mute\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ 🛠️  C O N T R O L   P A N E L\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /delay <seconds>   → ⏳ Set request delay\n"
        "• /kill              → 💀 Stop all loops in this chat\n"
        "• /othgc             → 🌐 Remote control (start/stop elsewhere)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ 👑  S U D O   M A N A G E M E N T\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /addsudo (reply)   → ➕ Add a SUDO user\n"
        "• /delsudo (reply)   → ➖ Remove a SUDO user\n"
        "• /listsudo          → 📋 List all SUDO users\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ ℹ️  I N F O R M A T I O N\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /myid              → 🆔 Show your Telegram ID\n"
        "• /ping              → 🏓 Check bot latency\n"
        "• /status            → 📊 System status & uptime\n"
        "• /stats             → 📈 Per‑bot message count\n"
        "• /leave             → 🚪 (Owner) All bots leave chat\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✦ 🔊  T T S   C O M M A N D S\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• /tts <text>        → 🎤 Send TTS to owner\n"
        "• /ttsfuck <text>    → 🔁 Continuous TTS spam loop\n\n"
        "╔════════════════════╗\n"
        "      ✦  A D I X E  V I B E S  ✦\n"
        "╚════════════════════╝"
    )
    await update.message.reply_text(menu_text)

@count_command
async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    await msg.edit_text(f"Pong! {int((time.time()-start)*1000)} ms")

@count_command
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your Telegram ID: {update.effective_user.id}")

@only_sudo
@count_command
async def delay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global DELAY
    if not context.args:
        return await update.message.reply_text(f"⏳ Current delay: {DELAY} second(s)")
    try:
        new_delay = float(context.args[0])
        if new_delay <= 0:
            return await update.message.reply_text("⚠️ Delay must be greater than 0.")
        DELAY = new_delay
        await update.message.reply_text(f"✅ Delay set to {DELAY} second(s).")
    except ValueError:
        await update.message.reply_text("⚠️ Invalid number.")

@only_sudo
@count_command
async def gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /gcnc <text>")
    base = " ".join(context.args)
    await start_title_loop(update.message.chat_id, base, "raid")
    await update.message.reply_text("🔥 GC title loop started (raid mode).")

@only_sudo
@count_command
async def gcncemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /gcncemo <text>")
    base = " ".join(context.args)
    await start_title_loop(update.message.chat_id, base, "emoji")
    await update.message.reply_text("😋 Emoji title loop started.")

@only_sudo
@count_command
async def stopgcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        group_tasks[chat_id].cancel()
        del group_tasks[chat_id]
        await update.message.reply_text("⏹️ Title loop stopped.")
    else:
        await update.message.reply_text("⚠️ No active title loop in this chat.")

@only_owner
@count_command
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for d in [group_tasks, spam_tasks, photo_tasks, tts_tasks, picspam_tasks]:
        for cid, task in list(d.items()):
            task.cancel()
            del d[cid]
    await update.message.reply_text("⏹️ All loops stopped globally.")

@only_sudo
@count_command
async def spam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /spam <text>")
    text = " ".join(context.args)
    await start_spam_for_chat(update.message.chat_id, text, "text")
    await update.message.reply_text(f"💬 Spam started with text: {text}")

@only_sudo
@count_command
async def targetslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_spam_for_chat(update.message.chat_id, None, "raid_list")
    await update.message.reply_text("🎯 Target slide spam started.")

@only_sudo
@count_command
async def slidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_spam_for_chat(update.message.chat_id, None, "raid_list")
    await update.message.reply_text("📜 Slide spam started.")

@only_sudo
@count_command
async def swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /swipe <name>")
    name = " ".join(context.args)
    chat_id = update.message.chat_id
    swipe_names[chat_id] = name
    await start_spam_for_chat(chat_id, swipe_names, "swipe")
    await update.message.reply_text(f"⚡ Swipe spam started with name: {name}")

@only_sudo
@count_command
async def stopswipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    swipe_names.pop(chat_id, None)
    if chat_id in spam_tasks:
        spam_tasks[chat_id].cancel()
        del spam_tasks[chat_id]
    await update.message.reply_text("⏹️ Swipe spam stopped.")

@only_sudo
@count_command
async def stopspam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in spam_tasks:
        spam_tasks[chat_id].cancel()
        del spam_tasks[chat_id]
        await update.message.reply_text("⏹️ Spam stopped.")
    else:
        await update.message.reply_text("⚠️ No active spam in this chat.")

@only_sudo
@count_command
async def gspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    prefix = " ".join(context.args) if context.args else "{ʜᴀᴛᴇʀ}"
    gspam_prefixes[chat_id] = prefix
    await start_spam_for_chat(chat_id, None, "gspam")
    await update.message.reply_text(f"⏱️ GSPAM started with prefix: {prefix}")

@only_sudo
@count_command
async def flagspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /flagspam <text>")
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    gspam_prefixes[chat_id] = text
    await start_spam_for_chat(chat_id, None, "flagspam")
    await update.message.reply_text(f"🏁 Flag spam started with text: {text}")

@only_sudo
@count_command
async def tmkcspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /tmkcspam <text>")
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    gspam_prefixes[chat_id] = text
    await start_spam_for_chat(chat_id, None, "tmkcspam")
    await update.message.reply_text(f"🔨 TMKC spam started with text: {text}")

@only_sudo
@count_command
async def startphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ Reply to a photo to start DP loop.")
    chat_id = update.message.chat_id
    photo_file = await update.message.reply_to_message.photo[-1].get_file()
    photo_bytes = bytes(await photo_file.download_as_bytearray())
    photo_cache[chat_id] = photo_bytes
    await start_photo_loop(chat_id, photo_bytes)
    await update.message.reply_text("🖼️ Group DP loop started.")

@only_sudo
@count_command
async def stopphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in photo_tasks:
        photo_tasks[chat_id].cancel()
        del photo_tasks[chat_id]
        photo_cache.pop(chat_id, None)
        await update.message.reply_text("⏹️ Photo loop stopped.")
    else:
        await update.message.reply_text("⚠️ No active photo loop.")

@only_sudo
@count_command
async def picspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ Reply to a photo to start picture spam.")
    chat_id = update.message.chat_id
    photo_file = await update.message.reply_to_message.photo[-1].get_file()
    photo_bytes = bytes(await photo_file.download_as_bytearray())
    pic_cache[chat_id] = photo_bytes
    await start_picspam_loop(chat_id, photo_bytes)
    await update.message.reply_text("🖼️ Picture spam started.")

# Mute commands
@only_sudo_or_owner
@count_command
async def mute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    state = get_mute_state(chat_id)
    if context.args:
        if update.message.reply_to_message:
            target_id = update.message.reply_to_message.from_user.id
        else:
            try:
                target_id = int(context.args[0]) if not context.args[0].startswith("@") else None
                if target_id is None:
                    return await update.message.reply_text("⚠️ Reply to a user or provide numeric ID.")
            except:
                return await update.message.reply_text("⚠️ Invalid user ID.")
        if target_id == OWNER_ID:
            return await update.message.reply_text("⛔ Cannot mute the owner.")
        if target_id in SUDO_USERS:
            return await update.message.reply_text("⛔ Cannot mute a SUDO user.")
        if target_id not in state["muted_users"]:
            state["muted_users"].append(target_id)
            save_mute()
            await update.message.reply_text(f"🔇 User {target_id} muted.")
        else:
            await update.message.reply_text("⚠️ User is already muted.")
    else:
        state["mute_all"] = True
        save_mute()
        await update.message.reply_text("🔇 Group muted. Only owner and safe users can speak.")

@only_sudo_or_owner
@count_command
async def speak_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    state = get_mute_state(chat_id)
    state["mute_all"] = False
    state["muted_users"] = []
    save_mute()
    await update.message.reply_text("🔊 All mutes cleared. Everyone can speak.")

@only_sudo_or_owner
@count_command
async def safe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user to mark as safe.")
    chat_id = str(update.message.chat_id)
    target_id = update.message.reply_to_message.from_user.id
    state = get_mute_state(chat_id)
    if target_id not in state["safe_users"]:
        state["safe_users"].append(target_id)
        save_mute()
        await update.message.reply_text(f"✅ User {target_id} added to safe list.")
    else:
        await update.message.reply_text("⚠️ User is already safe.")

# SUDO Management
@only_owner
@count_command
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        SUDO_USERS[uid] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_sudo()
        await update.message.reply_text(f"➕ User {uid} added as SUDO.")
    else:
        await update.message.reply_text("⚠️ Reply to a user to add as SUDO.")

@only_owner
@count_command
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        if uid in SUDO_USERS:
            del SUDO_USERS[uid]
            save_sudo()
            await update.message.reply_text(f"➖ User {uid} removed from SUDO.")
        else:
            await update.message.reply_text("⚠️ User is not a SUDO.")
    else:
        await update.message.reply_text("⚠️ Reply to a user to remove from SUDO.")

@only_sudo
@count_command
async def listsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not SUDO_USERS:
        return await update.message.reply_text("📋 No SUDO users configured.")
    text = "📋 SUDO Users:\n\n"
    for uid, ts in SUDO_USERS.items():
        try:
            user = await context.bot.get_chat(uid)
            name = f"@{user.username}" if user.username else user.first_name
        except:
            name = str(uid)
        text += f"{name} ({uid}) - added {ts}\n"
    await update.message.reply_text(text)

@only_sudo
@count_command
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime = str(timedelta(seconds=int(time.time() - START_TIME)))
    active_groups = len(set(list(group_tasks.keys()) + list(spam_tasks.keys()) + list(photo_tasks.keys()) + list(tts_tasks.keys()) + list(picspam_tasks.keys())))
    msg = (
        f"📊 ADIXE System Status\n\n"
        f"⏱️ Uptime: {uptime}\n"
        f"🔢 Commands executed: {COMMAND_COUNTER}\n"
        f"🌐 Active groups: {active_groups}\n"
        f"⏳ Delay: {DELAY} sec\n"
        f"👑 SUDO users: {len(SUDO_USERS)}\n"
    )
    await update.message.reply_text(msg)

@only_sudo
@count_command
async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id not in msg_counter or not msg_counter[chat_id]:
        await update.message.reply_text("📈 No messages sent in this group yet.")
        return
    text = "📈 Messages sent by each bot in this group:\n\n"
    for bot_id, count in msg_counter[chat_id].items():
        text += f"Bot {bot_id}: {count} messages\n"
    await update.message.reply_text(text)

@only_sudo_or_owner
@count_command
async def kill_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    stopped = False
    for d in [group_tasks, spam_tasks, photo_tasks, tts_tasks, picspam_tasks]:
        if chat_id in d:
            d[chat_id].cancel()
            del d[chat_id]
            stopped = True
    if stopped:
        await update.message.reply_text("💀 All loops killed in this chat.")
    else:
        await update.message.reply_text("⚠️ No active loops here.")

@only_owner
@count_command
async def leave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    for d in [group_tasks, spam_tasks, photo_tasks, tts_tasks, picspam_tasks]:
        if chat_id in d:
            d[chat_id].cancel()
            del d[chat_id]
    success = 0
    for bot in bots:
        try:
            await bot.leave_chat(chat_id)
            success += 1
            await asyncio.sleep(0.5)
        except:
            pass
    await update.message.reply_text(f"🚪 {success} out of {len(bots)} bots left the chat.")

# /fuck combo
@only_owner
@count_command
async def fuck_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /fuck <text> (optionally reply to a photo)")
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in spam_tasks:
        spam_tasks[chat_id].cancel()
        del spam_tasks[chat_id]
    gspam_prefixes[chat_id] = text
    photo_bytes = None
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        photo_file = await update.message.reply_to_message.photo[-1].get_file()
        photo_bytes = bytes(await photo_file.download_as_bytearray())
        photo_cache[chat_id] = photo_bytes
    await update.message.reply_text(f"💥 FUCK mode activated with text: {text}" + (" + photo" if photo_bytes else ""))

# ---------- TTS COMMANDS ----------
@only_owner
@count_command
async def tts_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /tts <text>")
    text = " ".join(context.args)
    owner_id = update.effective_user.id
    voice_bytes = await generate_tts_voice(text)
    for bot in bots:
        try:
            await bot.send_voice(chat_id=owner_id, voice=voice_bytes)
        except Exception as e:
            logging.warning(f"TTS send error: {e}")
    await update.message.reply_text("🔊 TTS message sent to owner.")

@only_owner
@count_command
async def ttsfuck_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ttsfuck <text>")
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    voice_bytes = await generate_tts_voice(text)
    await start_tts_loop(chat_id, voice_bytes)
    await update.message.reply_text(f"🔊 TTS fuck loop started with text: {text}")

# Emoji title commands (all 13)
@only_sudo
@count_command
async def caremo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /caremo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, VEHICLE_EMOJIS)
    await update.message.reply_text("🚗 Vehicle emoji title loop started.")

@only_sudo
@count_command
async def flagemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /flagemo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, FLAG_EMOJIS)
    await update.message.reply_text("🇮🇳 Flag emoji title loop started.")

@only_sudo
@count_command
async def moonemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /moonemo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, MOON_EMOJIS)
    await update.message.reply_text("🌙 Moon emoji title loop started.")

@only_sudo
@count_command
async def petemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /petemo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, PET_EMOJIS)
    await update.message.reply_text("🐶 Pet emoji title loop started.")

@only_sudo
@count_command
async def plantemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /plantemo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, PLANT_EMOJIS)
    await update.message.reply_text("🌿 Plant emoji title loop started.")

@only_sudo
@count_command
async def foodemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /foodemo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, FOOD_EMOJIS)
    await update.message.reply_text("🍕 Food emoji title loop started.")

@only_sudo
@count_command
async def floweremo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /floweremo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, FLOWER_EMOJIS)
    await update.message.reply_text("🌸 Flower emoji title loop started.")

@only_sudo
@count_command
async def heartemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /heartemo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, HEART_EMOJIS)
    await update.message.reply_text("❤️ Heart emoji title loop started.")

@only_sudo
@count_command
async def animalemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /animalemo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, ANIMAL_EMOJIS)
    await update.message.reply_text("🐾 Animal emoji title loop started.")

@only_sudo
@count_command
async def sportemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /sportemo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, SPORT_EMOJIS)
    await update.message.reply_text("⚽ Sport emoji title loop started.")

@only_sudo
@count_command
async def weatheremo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /weatheremo <text>")
    base = " ".join(context.args)
    await start_title_loop_with_emojis(update.message.chat_id, base, WEATHER_EMOJIS)
    await update.message.reply_text("☁️ Weather emoji title loop started.")

# ---------- /othgc CONVERSATION ----------
WAIT_GROUP_ID, WAIT_ACTION, WAIT_TEXT, WAIT_COMMAND = range(4)

def is_owner_or_sudo(user_id):
    return user_id == OWNER_ID or user_id in SUDO_USERS

@count_command
async def othgc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_or_sudo(update.effective_user.id):
        await update.message.reply_text("⛔ Access denied.")
        return ConversationHandler.END
    await update.message.reply_text("📌 Send the target Group ID.\nSend /cancel to abort.")
    return WAIT_GROUP_ID

async def receive_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target = int(update.message.text.strip())
    except:
        await update.message.reply_text("⚠️ Invalid ID. Must be numeric.\n/cancel to abort.")
        return WAIT_GROUP_ID
    try:
        await bots[0].get_chat(target)
    except:
        await update.message.reply_text("⚠️ Bot is not in that group.\n/cancel to abort.")
        return WAIT_GROUP_ID
    context.user_data['target_chat'] = target
    await update.message.reply_text("✅ Bot is present. Send 'start' or 'stop'.\n/cancel to abort.")
    return WAIT_ACTION

async def receive_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = update.message.text.strip().lower()
    if action not in ('start', 'stop'):
        await update.message.reply_text("⚠️ Invalid. Send 'start' or 'stop'.\n/cancel to abort.")
        return WAIT_ACTION
    context.user_data['action'] = action
    if action == 'stop':
        target = context.user_data['target_chat']
        for d in [group_tasks, spam_tasks, photo_tasks, tts_tasks, picspam_tasks]:
            if target in d:
                d[target].cancel()
                del d[target]
        await update.message.reply_text(f"⏹️ All loops stopped in group {target}.")
        return ConversationHandler.END
    await update.message.reply_text("📝 Send the text to use.\n/cancel to abort.")
    return WAIT_TEXT

async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['text'] = update.message.text.strip()
    await update.message.reply_text(
        "🔧 Which command? Choose from:\n"
        "gcnc, gcncemo, spam, targetslide, slidespam, swipe, startphoto, gspam, flagspam, tmkcspam, picspam, "
        "caremo, flagemo, moonemo, petemo, plantemo, foodemo, floweremo, heartemo, animalemo, sportemo, weatheremo, ttsfuck\n"
        "/cancel to abort."
    )
    return WAIT_COMMAND

async def receive_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.strip().lower()
    valid = ['gcnc','gcncemo','spam','targetslide','slidespam','swipe','startphoto','gspam','flagspam','tmkcspam','picspam',
             'caremo','flagemo','moonemo','petemo','plantemo','foodemo','floweremo','heartemo','animalemo','sportemo','weatheremo','ttsfuck']
    if cmd not in valid:
        await update.message.reply_text(f"⚠️ Invalid command. Options: {', '.join(valid)}\n/cancel to abort.")
        return WAIT_COMMAND

    target = context.user_data['target_chat']
    text = context.user_data['text']

    if cmd == 'gcnc':
        await start_title_loop(target, text, "raid")
        msg = f"GC title loop started in {target}."
    elif cmd == 'gcncemo':
        await start_title_loop(target, text, "emoji")
        msg = f"Emoji title loop started in {target}."
    elif cmd == 'spam':
        await start_spam_for_chat(target, text, "text")
        msg = f"Spam started in {target}."
    elif cmd == 'targetslide':
        await start_spam_for_chat(target, None, "raid_list")
        msg = f"Target slide started in {target}."
    elif cmd == 'slidespam':
        await start_spam_for_chat(target, None, "raid_list")
        msg = f"Slide spam started in {target}."
    elif cmd == 'swipe':
        swipe_names[target] = text
        await start_spam_for_chat(target, swipe_names, "swipe")
        msg = f"Swipe spam started in {target}."
    elif cmd == 'gspam':
        gspam_prefixes[target] = text
        await start_spam_for_chat(target, None, "gspam")
        msg = f"GSPAM started in {target}."
    elif cmd == 'flagspam':
        gspam_prefixes[target] = text
        await start_spam_for_chat(target, None, "flagspam")
        msg = f"Flag spam started in {target}."
    elif cmd == 'tmkcspam':
        gspam_prefixes[target] = text
        await start_spam_for_chat(target, None, "tmkcspam")
        msg = f"TMKC spam started in {target}."
    elif cmd == 'picspam':
        if target not in pic_cache:
            await update.message.reply_text("⚠️ No photo cached for that group. Use /picspam there first.")
            return ConversationHandler.END
        await start_picspam_loop(target, pic_cache[target])
        msg = f"Picture spam started in {target}."
    elif cmd == 'startphoto':
        if target not in photo_cache:
            await update.message.reply_text("⚠️ No photo cached for that group. Use /startphoto there first.")
            return ConversationHandler.END
        await start_photo_loop(target, photo_cache[target])
        msg = f"Photo loop started in {target}."
    elif cmd == 'caremo':
        await start_title_loop_with_emojis(target, text, VEHICLE_EMOJIS)
        msg = f"Vehicle emoji loop started in {target}."
    elif cmd == 'flagemo':
        await start_title_loop_with_emojis(target, text, FLAG_EMOJIS)
        msg = f"Flag emoji loop started in {target}."
    elif cmd == 'moonemo':
        await start_title_loop_with_emojis(target, text, MOON_EMOJIS)
        msg = f"Moon emoji loop started in {target}."
    elif cmd == 'petemo':
        await start_title_loop_with_emojis(target, text, PET_EMOJIS)
        msg = f"Pet emoji loop started in {target}."
    elif cmd == 'plantemo':
        await start_title_loop_with_emojis(target, text, PLANT_EMOJIS)
        msg = f"Plant emoji loop started in {target}."
    elif cmd == 'foodemo':
        await start_title_loop_with_emojis(target, text, FOOD_EMOJIS)
        msg = f"Food emoji loop started in {target}."
    elif cmd == 'floweremo':
        await start_title_loop_with_emojis(target, text, FLOWER_EMOJIS)
        msg = f"Flower emoji loop started in {target}."
    elif cmd == 'heartemo':
        await start_title_loop_with_emojis(target, text, HEART_EMOJIS)
        msg = f"Heart emoji loop started in {target}."
    elif cmd == 'animalemo':
        await start_title_loop_with_emojis(target, text, ANIMAL_EMOJIS)
        msg = f"Animal emoji loop started in {target}."
    elif cmd == 'sportemo':
        await start_title_loop_with_emojis(target, text, SPORT_EMOJIS)
        msg = f"Sport emoji loop started in {target}."
    elif cmd == 'weatheremo':
        await start_title_loop_with_emojis(target, text, WEATHER_EMOJIS)
        msg = f"Weather emoji loop started in {target}."
    elif cmd == 'ttsfuck':
        voice_bytes = await generate_tts_voice(text)
        await start_tts_loop(target, voice_bytes)
        msg = f"TTS fuck loop started in {target}."
    else:
        msg = "Unknown command."

    await update.message.reply_text(f"✅ {msg}")
    return ConversationHandler.END

async def othgc_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Remote operation cancelled.")
    return ConversationHandler.END

# ---------- BUILD & RUN ----------
def build_app(token):
    app = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('othgc', othgc_start)],
        states={
            WAIT_GROUP_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_group_id)],
            WAIT_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_action)],
            WAIT_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text)],
            WAIT_COMMAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_command)],
        },
        fallbacks=[CommandHandler('cancel', othgc_cancel)],
    )
    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mute_handler), group=1)

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("menu", menu_cmd))
    app.add_handler(CommandHandler("help", menu_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("gcnc", gcnc))
    app.add_handler(CommandHandler("gcncemo", gcncemo))
    app.add_handler(CommandHandler("stopgcnc", stopgcnc))
    app.add_handler(CommandHandler("stopall", stopall))
    app.add_handler(CommandHandler("delay", delay_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("addsudo", addsudo))
    app.add_handler(CommandHandler("delsudo", delsudo))
    app.add_handler(CommandHandler("listsudo", listsudo))
    app.add_handler(CommandHandler("spam", spam_cmd))
    app.add_handler(CommandHandler("targetslide", targetslide))
    app.add_handler(CommandHandler("slidespam", slidespam))
    app.add_handler(CommandHandler("swipe", swipe))
    app.add_handler(CommandHandler("stopswipe", stopswipe))
    app.add_handler(CommandHandler("stopspam", stopspam))
    app.add_handler(CommandHandler("gspam", gspam_cmd))
    app.add_handler(CommandHandler("flagspam", flagspam_cmd))
    app.add_handler(CommandHandler("tmkcspam", tmkcspam_cmd))
    app.add_handler(CommandHandler("picspam", picspam_cmd))
    app.add_handler(CommandHandler("startphoto", startphoto_cmd))
    app.add_handler(CommandHandler("stopphoto", stopphoto_cmd))
    app.add_handler(CommandHandler("mute", mute_cmd))
    app.add_handler(CommandHandler("speak", speak_cmd))
    app.add_handler(CommandHandler("safe", safe_cmd))
    app.add_handler(CommandHandler("kill", kill_cmd))
    app.add_handler(CommandHandler("leave", leave_cmd))
    app.add_handler(CommandHandler("fuck", fuck_cmd))
    app.add_handler(CommandHandler("tts", tts_cmd))
    app.add_handler(CommandHandler("ttsfuck", ttsfuck_cmd))
    app.add_handler(CommandHandler("caremo", caremo))
    app.add_handler(CommandHandler("flagemo", flagemo))
    app.add_handler(CommandHandler("moonemo", moonemo))
    app.add_handler(CommandHandler("petemo", petemo))
    app.add_handler(CommandHandler("plantemo", plantemo))
    app.add_handler(CommandHandler("foodemo", foodemo))
    app.add_handler(CommandHandler("floweremo", floweremo))
    app.add_handler(CommandHandler("heartemo", heartemo))
    app.add_handler(CommandHandler("animalemo", animalemo))
    app.add_handler(CommandHandler("sportemo", sportemo))
    app.add_handler(CommandHandler("weatheremo", weatheremo))

    return app

async def run_all_bots():
    global apps, bots
    for token in TOKENS:
        if token.strip():
            try:
                app = build_app(token)
                apps.append(app)
                bots.append(app.bot)
            except Exception as e:
                print(f"Build error: {e}")
    for app in apps:
        try:
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
        except Exception as e:
            print(f"Start error: {e}")
    print("🚀 ADIXE Bot is running.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run_all_bots())