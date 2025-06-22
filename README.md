<h1 align="center">🤖 SchwarzBot - Hybrid Discord Bot</h1>
<p align="center">
  A feature-rich moderation & fun Discord bot supporting both <strong>prefix</strong> and <strong>slash</strong> commands!
</p>

---

## ⚠️ IMPORTANT NOTE

📁 **Updated Script:** `bot user (slash cmd).py`  
✅ Now supports **Hybrid Commands**: Works with both `?prefix` and `/slash` style commands.  
📥 **Download this version** if you want the enhanced hybrid functionality.

---

## 📚 BOT SETUP GUIDE

### 🔧 Basic Configuration

```python
# Add your bot token here
TOKEN = "YOUR_BOT_TOKEN"

# Set your moderation logs channel ID
LOG_CHANNEL_ID = 123456789012345678
```

### 🔍 Log Testing
Use the command below to test log output:
```
?testlog
```

---

## 🎭 Custom Responses

Make your bot reply to specific messages:

```python
if content == "PLACE YOUR MESSAGE HERE":
    await message.reply("PLACE YOUR RESPONSE HERE", mention_author=False)
```

### 🎤 Jokes & Punchlines
- Add jokes in the `setup` list or section.
- Add punchlines in the `punchline` list or section.

---

## 🛠️ MODERATION COMMANDS

| 🧾 Action        | 🔤 Prefix Command           | 💬 Slash Command        |
|------------------|-----------------------------|--------------------------|
| Ban User         | `?ban [reason]`             | `/ban [reason]`          |
| Kick User        | `?kick [reason]`            | `/kick [reason]`         |
| Mute User        | `?mute [unit] [reason]`     | `/mute [reason]`         |
| Unmute User      | `?unmute`                   | `/unmute`                |
| Warn User        | `?warn [reason]`            | `/warn [reason]`         |
| Clear Messages   | `?clear [amount]`           | `/clear [amount]`        |
| Check Latency    | `?ping`                     | `/ping`                  |

🕒 **Supported Mute Units:** `minutes`, `hours`, `days`, `weeks`, `months`

---

## 🌐 Need Help?

For bug reports or help, visit our support page:  
🔗 [**SchwarzBot Website**](https://rhwongit.github.io/Schwarzapp.website/)  
Scroll to the bottom of the page and leave us a message!

---

> 💡 *Want to contribute or customize? Fork this repo and build your own bot easily!*
