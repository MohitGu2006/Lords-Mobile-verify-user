
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, PeerIdInvalid

API_ID = 29585470
API_HASH = "c9c5067a8ca826bc41dfd94ea578fe28"
BOT_TOKEN = "7897128796:AAHYml5NT_yV2quFC5jQ6ltd3FeJx0TQ0qk"
GROUP_ID = -1002875359426
ADMIN_ID = 2095987863

WAITING = ChatPermissions(can_send_messages=False)
VERIFIED = ChatPermissions(can_send_messages=True)

app = Client("auto_verify_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

pending = {}

@app.on_message(filters.new_chat_members & filters.chat(GROUP_ID))
async def new_member(client, message):
    for member in message.new_chat_members:
        if member.is_bot:
            continue
        uid = member.id
        name = member.first_name or "User"
        await client.restrict_chat_member(GROUP_ID, uid, WAITING)
        try:
            await client.send_message(
                uid,
                f"""👋 **Hello {name}!**

🔒 You're in **waiting mode** for verification.

🛡 To gain access to the group:

1️⃣ Type `/verify` here  
2️⃣ Send a **screenshot** of your **Lords Mobile profile**  
3️⃣ Include this caption format:
```
IGN: YourName
Level: 60
Guild: [TAG]
```

Once verified, you'll be unmuted. Thank you!""")
        except PeerIdInvalid:
            pass

@app.on_message(filters.command("verify") & filters.private)
async def start_verify(client, message):
    uid = message.from_user.id
    try:
        await client.get_chat_member(GROUP_ID, uid)
    except UserNotParticipant:
        return await message.reply("❌ You must join the group first.")
    pending[uid] = "awaiting"
    await message.reply(
        """📸 Please send your Lords Mobile **profile screenshot** with caption:

```
IGN: YourName
Level: 60
Guild: [TAG]
```

✅ Caption required for verification!""")

@app.on_message(filters.photo & filters.private)
async def handle_photo(client, message):
    uid = message.from_user.id
    name = message.from_user.first_name
    if uid not in pending:
        return await message.reply("⚠️ Type `/verify` first.")
    if not message.caption or "ign:" not in message.caption.lower():
        return await message.reply("❌ Invalid caption. Use this format:\n```
IGN: YourName\nLevel: 60\nGuild: [ABC]\n```")
    
    pending[uid] = "pending"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{uid}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{uid}")
        ]
    ])

    await client.send_message(
        ADMIN_ID,
        f"""🔍 **Verification Request**

👤 **Name:** {name}  
🆔 **User ID:** `{uid}`  
📄 **Caption:**  
{message.caption}

⏳ Waiting for admin action...""",
        reply_markup=keyboard
    )
    await message.forward(ADMIN_ID)
    await message.reply("✅ Your request has been sent. Please wait for admin approval.")

@app.on_callback_query()
async def handle_callback(client, cb):
    data = cb.data
    action, uid = data.split(":")
    uid = int(uid)

    if cb.from_user.id != ADMIN_ID:
        return await cb.answer("❌ You are not allowed to use this.", show_alert=True)

    if action == "approve":
        await client.restrict_chat_member(GROUP_ID, uid, VERIFIED)
        await client.send_message(uid, "✅ You are verified and unmuted. Welcome to the group!")
        await cb.message.edit_text(f"✅ User `{uid}` has been approved.")
        pending.pop(uid, None)

    elif action == "reject":
        await client.send_message(uid, "❌ Your verification has been rejected. Contact admin for help.")
        await cb.message.edit_text(f"❌ User `{uid}` has been rejected.")
        pending.pop(uid, None)

@app.on_message(filters.command("status"))
async def status(client, message):
    bot = await client.get_me()
    await message.reply(
        f"""📊 **Bot Status**

🤖 Bot: @{bot.username}  
🧾 Pending Verifications: {len(pending)}  
🔒 Group ID: `{GROUP_ID}`  
✅ Working Fine
""")

app.run()
