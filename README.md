# HiteEmojiCloner

A streamlined, minimalist Discord CLI utility to clone, migrate, and wipe emojis and stickers across servers with rate-limit handling.

---

## Features

- **Clone Emojis**: Copy custom emojis (static PNG and animated GIF) from any joined server to your target server, individually or in bulk.
- **Clone Stickers**: Copy custom stickers (PNG, APNG, Lottie, GIF) with tag metadata preserved.
- **Wipe Server Assets**: Safely bulk-delete or selectively remove emojis and stickers from your own servers.
- **Smart Rate-Limit Protection**: Automatic HTTP 429 backoff with live countdown display to prevent Discord bucket penalties.
- **Slot Overflow Detection**: Catches Discord error `30008` (server emoji slot limit reached) gracefully.
- **Dual Authentication**: Works with both Bot Tokens and User Tokens (Selfbot).
- **Minimalist Dark Aesthetic**: Clean, distraction-free monochrome slate terminal UI powered by `rich`.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:HikaruIR/HiteEmojiCloner.git
   cd HiteEmojiCloner
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the launcher or script directly:

```bash
# Windows one-click:
run.bat

# Or directly via Python:
python main.py
```

### Required Permissions
To upload emojis and stickers to the destination server, the token needs:
- `Manage Expressions` (or `Manage Emojis and Stickers`) or `Administrator`.

---

## License
MIT License.
