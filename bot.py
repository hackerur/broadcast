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

@RiZoeL.on_message(filters.command(["start"]))
async def start_command(client, message):
    video_file_id = "https://graph.org/file/8048e7f238b98bcf008c7.jpg"
    caption = f"Hey {message.chat.first_name} Thanks for subscribing our bot!\n\nAll New updates will be broadcasted here\n\nStay Tuned!"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("- Join Channel -", url="https://t.me/livekamaoroj")]]
    )
    await RiZoeL.send_photo(chat_id=message.chat.id, photo=video_file_id, caption=caption, reply_markup=keyboard)

@RiZoeL.on_message(filters.user(SUDO_USERS) & filters.command("gcast"))
async def gcast_(_, e: Message):
    txt = ' '.join(e.command[1:])
    if txt:
      msg = str(txt)
    elif e.reply_to_message:
        msg = e.reply_to_message.text.markdown
    else:
        await e.reply_text("Give Message for Broadcast or reply to any msg")
        return

    Han = await e.reply_text("__Processing...__")
    err = 0
    dn = 0
    data = await get_all_users()
    for x in data:
       try:
          await RiZoeL.send_message(x.user_id, msg)
          await asyncio.sleep(0.5)
          dn += 1
       except Exception as a:
          print(a)
          err += 1
    try:
       await Han.edit_text(f"Gcast Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"Gcast Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")

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

@RiZoeL.on_message(filters.private & filters.incoming & filters.user(SUDO_USERS))
async def gcast_(_, e: Message):
    global broadcast_mode
    if broadcast_mode:
        text = e.text
    else:
        await e.reply_text("broadcast is not enabled")
        return

    Han = await e.reply_text("__Broadcasting__")
    error_count = 0
    done_count = 0
    data = await get_all_users()
    for user in data:
        try:
            message_media = None
            if e.photo:
                message_media = e.photo.file_id
            elif e.video:
                message_media = e.video.file_id
            elif e.animation:
                message_media = e.animation.file_id
            elif e.document:
                message_media = e.document.file_id
            elif e.audio:
                message_media = e.audio.file_id
                
            caption = None
            if e.caption:
                caption = e.caption
            elif e.video_note:
                caption = e.video_note.caption
            elif e.voice:
                caption = e.voice.caption

            await RiZoeL.send_chat_action(user.user_id, "typing")
            await asyncio.sleep(1)
            await RiZoeL.send_message(user.user_id, message_text, reply_markup=None, disable_web_page_preview=True, reply_to_message_id=None, media=message_media, caption=caption, parse_mode="markdown")
            done_count += 1
        except Exception as e:
            print(e)
            error_count += 1
    try:
        await Han.edit_text(f"Broadcast Done ✓ \n\n Success chats: {done_count} \n Failed chats: {error_count}")
    except:
        await Han.delete()
        await e.reply_text(f"Broadcast Done ✓ \n\n Success chats: {done_count} \n Failed chats: {error_count}")



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
