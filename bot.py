""" : RiZoeL : """

import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, sys, time, datetime, asyncio
from pyrogram import Client, idle, filters, __version__ 
from pyrogram.types import Message
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
from database.users_db import *
from database import SESSION 
from vars import *

broadcast_mode = False

RiZoeL = Client(
    "RiZoeL-Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    )


@RiZoeL.on_message(~filters.service, group=1)
async def users_database(_, msg: Message):
    if msg.from_user:
        Check = SESSION.query(Users).get(int(msg.from_user.id))
        if not Check:
            SESSION.add(Users(msg.from_user.id))
            SESSION.commit()
        else:
            SESSION.close()
            
@RiZoeL.on_message(filters.service & filters.group & filters.channel)
async def users_database(_, msg: Message):
      Check = SESSION.query(Users).get(int(msg.chat.id))
      if not Check:
          SESSION.add(Users(msg.chat.id))
          SESSION.commit()
      else:
          SESSION.close()


@RiZoeL.on_message(filters.user(SUDO_USERS) & filters.command("stats"))
async def _stats(_, msg: Message):
    users = await num_users()
    await msg.reply(f"Total Users : {users}", quote=True)

@RiZoeL.on_message(filters.private & filters.incoming & filters.command("broadcast") & filters.user(SUDO_USERS))
async def start_broadcast(client, message):
    global broadcast_mode
    broadcast_mode = True
    await message.reply("Okay, every message of yours will be broadcasted to all users now.")

# Handler for /end command
@RiZoeL.on_message(filters.private & filters.incoming & filters.command("end") & filters.user(SUDO_USERS))
async def stop_broadcast(client, message):
    global broadcast_mode
    broadcast_mode = False
    await message.reply("Broadcast process ended.")

# Handler for all other messages
@RiZoeL.on_message(filters.private & filters.incoming)
async def handle_message(client, message):
    global broadcast_mode
    if broadcast_mode:
        # Get all users and broadcast the message to them
        users = await RiZoeL.get_users()
        for user in users:
            await client.send_message(user.id, message.text)


@RiZoeL.on_message(filters.command(["start"]))
async def start_handler(client, message):
    await client.send_message(
        message.chat.id,
        f"Hey {message.chat.first_name} Thanks for subscribing our bot!\n\nAll New updates will be broadcasted here\n\nStay Tuned!",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "- Join Channel -", url="https://t.me/livekamaoroj"
                )
            ]]
        )
    )
    await client.send_message(
        "SUDO_USERS",
        f"New user started the bot:\n\n"
        f"ID: {message.chat.id}\n"
        f"Username: {message.chat.username}\n"
        f"Full name: {message.chat.first_name} {message.chat.last_name}"
    )


@RiZoeL.on_message(filters.user(SUDO_USERS) & filters.command(["fcast", "fmsg", "forward", "forwardmessage"]))
async def forward_(_, e: Message):
    Siu = "".join(e.text.split(maxsplit=1)[1:]).split(" ", 1)
    if len(Siu) == 2:
       from_chat = str(Siu[0])
       Msg_id = int(Siu[1])      
    else:
       await e.reply_text("Wrong Usage! \n\n Syntax: /forward (from chat id) (message id) \n\nNote: Must add bot in from message Channel!")
       return

    Han = await e.reply_text("__forwarding__")
    err = 0
    dn = 0
    data = await get_all_users()
    for x in data:
       try:
          await RiZoeL.forward_messages(x.user_id, from_chat, Msg_id)
          await asyncio.sleep(0.5)
          dn += 1
       except Exception as a:
          print(a)
          err += 1
    try:
       await Han.edit_text(f"Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")

if __name__ == "__main__":
    print("Bot - [INFO]: Starting the bot")
    try:
        RiZoeL.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your TOKEN is not valid.")
    print(f"""
     --------------------------------
       YOUR BOT HAS BEEN STARTED!
       PYROGRAM VERSION: {__version__}
     --------------------------------
       """)
    idle()
    RiZoeL.stop()
    print("Bot - [INFO]: Bot stopped.")
