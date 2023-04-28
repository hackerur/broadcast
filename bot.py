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
    video_file_id = "https://graph.org/file/eb3fcee6b5238a027957c.jpg"
    caption = f"ʜᴇʏ {message.chat.first_name} ᴛʜᴀɴᴋs ғᴏʀ sᴛᴀʀᴛɪɴɢ ʙᴏᴛ!\n\nᴀʟʟ ɴᴇᴡ ᴜᴘᴅᴀᴛᴇs ᴡɪʟʟ ʙᴇ sʜᴀʀᴇᴅ ᴛʜᴇʀᴇ\n\nsᴛᴀʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴡɪᴛʜ ᴏᴜʀ ɴᴇᴛᴡᴏʀᴋ - [ɴᴏᴏʙᴄʀᴇᴀᴛᴏʀ](t.me/noobcreator)! \n\nғᴀᴄɪɴɢ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴄᴏɴᴛᴀᴄᴛ - [ᴘɪʀᴏᴋɪᴅ](t.me/pirokid) \n\nᴏᴡɴᴇʀ ᴏғ ᴛʜɪs ᴄᴏᴅᴇ ɪs - [ᴠɪᴠᴇᴋᴇᴠɪʟ](t.me/vivekevil)"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⁂ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ⁂", url="https://t.me/NOOBXCREATOR")]]
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
        await e.reply_text("ɢɪᴠᴇ ᴍᴇ ᴍᴇssᴇɢᴇ ғᴏʀ ʙʀᴏᴀᴅᴄᴀsᴛ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇssᴇɢᴇ")
        return

    Han = await e.reply_text("__ᴘʀᴏᴄᴇssɪɴɢ...__")
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
       await Han.edit_text(f"ɢᴄᴀꜱᴛ ᴅᴏɴᴇ ✓ \n\n ꜱᴜᴄᴄᴇꜱꜱ ᴄʜᴀᴛꜱ: {dn} \n ꜰᴀɪʟᴇᴅ ᴄʜᴀᴛꜱ: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"ɢᴄᴀꜱᴛ ᴅᴏɴᴇ ✓ \n\n ꜱᴜᴄᴄᴇꜱꜱ ᴄʜᴀᴛꜱ: {dn} \n ꜰᴀɪʟᴇᴅ ᴄʜᴀᴛꜱ: {err}")

@RiZoeL.on_message(filters.private & filters.incoming & filters.command("broadcast") & filters.user(SUDO_USERS))
async def start_broadcast(client, message):
    global broadcast_mode
    broadcast_mode = True
    await message.reply("ᴏᴋᴀʏ, ᴇᴠᴇʀʏ ᴍᴇꜱꜱᴀɢᴇ ᴏꜰ ʏᴏᴜʀꜱ ᴡɪʟʟ ʙᴇ ʙʀᴏᴀᴅᴄᴀꜱᴛᴇᴅ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ ɴᴏᴡ.")

# Handler for /end command
@RiZoeL.on_message(filters.private & filters.incoming & filters.command("end") & filters.user(SUDO_USERS))
async def stop_broadcast(client, message):
    global broadcast_mode
    broadcast_mode = False
    await message.reply("ʙʀᴏᴀᴅᴄᴀsᴛ ᴘʀᴏᴄᴇss ᴇɴᴅᴇᴅ.")

# Handler for all other messages
@RiZoeL.on_message(filters.private & filters.incoming & filters.user(SUDO_USERS))
async def gcast_(_, e: Message):
    global broadcast_mode
    if broadcast_mode:
     txt = e.text
    if txt:
      msg = str(txt)
    elif e.reply_to_message:
        msg = e.reply_to_message.text.markdown
    else:
        await e.reply_text("ɢɪᴠᴇ ᴍᴇꜱꜱᴀɢᴇ ꜰᴏʀ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍꜱɢ")
        return

    Han = await e.reply_text("__ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ__")
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
       await Han.edit_text(f"ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴅᴏɴᴇ ✓ \n\n ꜱᴜᴄᴄᴇꜱꜱ ᴄʜᴀᴛꜱ: {dn} \n ꜰᴀɪʟᴇᴅ ᴄʜᴀᴛꜱ: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴅᴏɴᴇ ✓ \n\n ꜱᴜᴄᴄᴇꜱꜱ ᴄʜᴀᴛꜱ: {dn} \n ꜰᴀɪʟᴇᴅ ᴄʜᴀᴛꜱ: {err}")


@RiZoeL.on_message(filters.user(SUDO_USERS) & filters.command(["fcast", "fmsg", "forward", "forwardmessage"]))
async def forward_(_, e: Message):
    Siu = "".join(e.text.split(maxsplit=1)[1:]).split(" ", 1)
    if len(Siu) == 2:
       from_chat = str(Siu[0])
       Msg_id = int(Siu[1])      
    else:
       await e.reply_text("ᴡʀᴏɴɢ ᴜsᴇᴀɢᴇ! \n\n sʏɴᴛᴀx: /forward (from chat id) (message id) \n\nɴᴏᴛᴇ: ᴍᴜsᴛ ᴀᴅᴅ ʙᴏᴛ ɪɴ ғʀᴏᴍ ᴍᴇssᴇɢᴇ ᴄʜᴀɴɴᴇʟ! \n\nғᴀᴄɪɴɢ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴄᴏɴᴛᴀᴄᴛ - [ᴘɪʀᴏᴋɪᴅ](t.me/pirokid)")
       return

    Han = await e.reply_text("__ғᴏʀᴡᴀʀᴅɪɴɢ__")
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
       await Han.edit_text(f"ᴅᴏɴᴇ ✓ \n\n ꜱᴜᴄᴄᴇꜱꜱ ᴄʜᴀᴛꜱ: {dn} \n ꜰᴀɪʟᴇᴅ ᴄʜᴀᴛꜱ: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"ᴅᴏɴᴇ ✓ \n\n ꜱᴜᴄᴄᴇꜱꜱ ᴄʜᴀᴛꜱ: {dn} \n ꜰᴀɪʟᴇᴅ ᴄʜᴀᴛꜱ: {err}")

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
