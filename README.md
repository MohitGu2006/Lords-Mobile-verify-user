# 🚀 Lords Mobile Auto Verification Bot

A smart and secure Telegram bot that automatically verifies new members who join your Lords Mobile Telegram group. It ensures only real players get access by requiring a screenshot and manual/admin approval.

---

## 🔍 Features

- ✅ Auto-detect when user joins via invite link  
- 🔒 Instantly mute the user (waiting mode)  
- 📩 Send instructions in private chat for verification  
- 📸 Accept screenshot of Lords Mobile profile with IGN & Level  
- 🧾 Admin gets Approve / Reject buttons  
- 🔓 Upon approval, user gets full chat access  
- ❌ Rejected users remain muted and are notified  
- 📊 `/status` command to check bot status  

---

## 📦 Installation

### Step 1: Clone this repository

```bash
git clone https://github.com/MohitGu2006/Lords-Mobile-verify-user.git
cd Lords-Mobile-verify-user
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Update your credentials in `main.py`

Replace the following:

```python
API_ID = your_api_id
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
GROUP_ID = -100xxxxxxxxxx  # your group id
ADMIN_ID = 123456789       # your Telegram user id
```

Get your API credentials from [my.telegram.org](https://my.telegram.org)

---

## ▶️ Run the Bot

```bash
python main.py
```

---

## 🧪 Usage Flow

1. User joins group via invite link  
2. Bot auto mutes and sends DM with instructions  
3. User types `/verify` and sends screenshot + caption  
4. Admin receives verification request with Approve/Reject buttons  
5. Approved users are unmuted and notified  
6. Rejected users stay muted  

---

## 🛡 Security Tip

Enable this in your Telegram group settings:

- **"New members can't see message history"**  
- **Only admins can post** *(optional)*  

---

## 🧑‍💻 Author

Made by [Mohit Gupta](https://github.com/MohitGu2006)

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).
