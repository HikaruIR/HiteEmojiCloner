# HiteEmojiCloner

[![Release](https://img.shields.io/github/v/release/HikaruIR/HiteEmojiCloner?style=for-the-badge&color=blue)](https://github.com/HikaruIR/HiteEmojiCloner/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)](https://github.com/HikaruIR/HiteEmojiCloner/releases/latest)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)](LICENSE)

A streamlined, high-performance Discord utility to clone, migrate, and wipe emojis and stickers across servers with automatic rate-limit handling.

---

## ⚡ Direct Download (Latest Release)

Ready-to-use standalone executable for Windows (no Python required):

👉 **[Download HiteEmojiCloner.exe (Latest Release)](https://github.com/HikaruIR/HiteEmojiCloner/releases/latest)**

1. Download `HiteEmojiCloner.exe` from the latest release link above.
2. Double-click to run.

---

## Features

- **Clone Emojis**: Copy custom emojis (static PNG and animated GIF) from any server to your target server in bulk.
- **Clone Stickers**: Copy custom stickers (PNG, APNG, Lottie, GIF) with tag metadata preserved.
- **Wipe Server Assets**: Safely bulk-delete or selectively remove emojis and stickers.
- **Smart Rate-Limit Protection**: Automatic HTTP 429 backoff with live countdown display.
- **Slot Overflow Detection**: Catches Discord error `30008` (server slot limit reached) gracefully.
- **Dual Authentication**: Compatible with Bot Tokens and User Tokens.
- **Monochrome Dark Interface**: Clean, distraction-free terminal UI.

---

## Required Permissions

To upload emojis and stickers to the destination server, the token requires:
- `Manage Expressions` (or `Manage Emojis and Stickers`) or `Administrator`.

---

## License

**Proprietary Software — All Rights Reserved.**  
Copyright (c) 2026 HikaruIR. Unauthorized redistribution, decompilation, or publishing of source code is strictly prohibited. See [LICENSE](LICENSE) for details.
