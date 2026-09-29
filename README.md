# HiteEmojiCloner

[![Release](https://img.shields.io/github/v/release/HikaruIR/HiteEmojiCloner?style=for-the-badge&color=blue)](https://github.com/HikaruIR/HiteEmojiCloner/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)](https://github.com/HikaruIR/HiteEmojiCloner/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)](LICENSE)

A streamlined, high-performance Discord utility to clone, migrate, and wipe emojis and stickers across servers with automatic rate-limit handling and dark minimalist terminal aesthetics.

---

## ⚡ Direct Download (Latest Release)

Ready-to-use standalone executable for Windows (**No Python or dependencies required**):

👉 **[Download HiteEmojiCloner.exe (Latest Release)](https://github.com/HikaruIR/HiteEmojiCloner/releases/latest)**

1. Download `HiteEmojiCloner.exe` from the latest release link above.
2. Double-click to run.

---

## 📋 Prerequisites (پیشنیازها برای اجرای سورس کد)

اگر می‌خواهید پروژه را از سورس کد اجرا کنید:

1. **Python 3.10+**: پایتون نسخه ۱۰ به بالا روی سیستم نصب باشد ([دانلود از python.org](https://www.python.org/downloads/)).
   > ⚠️ **مهم:** هنگام نصب پایتون، حتماً گزینه **`Add python.exe to PATH`** را تیک بزنید.
2. **Git**: برای کلون کردن ریپازیتوری ([دانلود Git](https://git-scm.com/)).
3. **Discord Token**:
   - **Bot Token**: از طریق [Discord Developer Portal](https://discord.com/developers/applications) با اینتنت‌های فعال و دسترسی مدیریت ایموجی (`Manage Expressions`).
   - یا **User Token**: توکن اکانت کاربر.

---

## 🚀 Setup & Run from Source (نحوه راه‌اندازی و اجرا)

### روش اول: اجرای تک‌کلیک (سریع‌ترین روش)
کافیست پروژه را دانلود کنید و روی فایل **`run.bat`** دوبار کلیک کنید.
این اسکریپت به صورت کاملاً خودکار:
- محیط مجازی (`.venv`) می‌سازد.
- پکیج‌های لازم (`requests`, `rich`) را نصب می‌کند.
- نرم‌افزار را اجرا می‌کند.

---

### روش دوم: راه‌اندازی دستی در ترمینال (CMD یا PowerShell)

```bash
# ۱. کلون کردن ریپازیتوری
git clone https://github.com/HikaruIR/HiteEmojiCloner.git
cd HiteEmojiCloner

# ۲. ساخت محیط مجازی پایتون
python -m venv .venv

# ۳. فعال‌سازی محیط مجازی
# در ویندوز (PowerShell یا CMD):
.venv\Scripts\activate

# ۴. نصب پکیج‌های مورد نیاز
pip install -r requirements.txt

# ۵. اجرای برنامه
python main.py
```

---

## 📦 Build Standalone EXE (ساخت فایل نصبی بدون نیاز به پایتون)

برای ساخت فایل `.exe` تک‌فایله برای توزیع بین کاربران:

```bash
# روی فایل build_exe.bat دوبار کلیک کنید
# یا در ترمینال اجرا کنید:
.\build_exe.bat
```

فایل نهایی در مسیر `dist\HiteEmojiCloner.exe` ساخته خواهد شد.

---

## ✨ Features (امکانات)

- **Clone Emojis**: Copy custom emojis (static PNG and animated GIF) from any server to your target server in bulk.
- **Clone Stickers**: Copy custom stickers (PNG, APNG, Lottie, GIF) with tag metadata preserved.
- **Wipe Server Assets**: Safely bulk-delete or selectively remove emojis and stickers.
- **Smart Rate-Limit Protection**: Automatic HTTP 429 backoff with live countdown display.
- **Slot Overflow Detection**: Catches Discord error `30008` (server slot limit reached) gracefully.
- **Dual Authentication**: Compatible with Bot Tokens and User Tokens.
- **Monochrome Dark Interface**: Clean, distraction-free minimalist terminal UI.

---

## 🔐 Required Permissions (دسترسی‌های مورد نیاز)

To upload emojis and stickers to the destination server, the token requires:
- `Manage Expressions` (or `Manage Emojis and Stickers`) or `Administrator`.

---

## 📄 License

**Proprietary Software — All Rights Reserved.**  
Copyright (c) 2026 HikaruIR. Unauthorized redistribution, decompilation, or publishing of source code is strictly prohibited. See [LICENSE](LICENSE) for details.
