"""
discord_api.py
Discord REST API wrapper — handles all HTTP calls to the Discord API.
Language: Python 3.10+  |  Runtime: No external event loop needed
"""

import base64
import time
import requests
from typing import Optional
from rich.console import Console

console = Console()
BASE_URL = "https://discord.com/api/v10"


class DiscordAPI:
    """Thin wrapper around the Discord REST API using a bot or user token."""

    def __init__(self, token: str, is_bot: bool = True):
        prefix = "Bot" if is_bot else ""
        self.headers = {
            "Authorization": f"{prefix} {token}".strip(),
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    # ─── rate-limit aware request with live countdown ────────────────────────

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{BASE_URL}{path}"
        if "timeout" not in kwargs:
            kwargs["timeout"] = 20

        while True:
            try:
                resp = self.session.request(method, url, **kwargs)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                console.print(f"[dim grey70]⚠ Network timeout/retry in 3s... ({e})[/dim grey70]")
                time.sleep(3)
                continue

            if resp.status_code == 429:
                try:
                    data = resp.json()
                    retry_after = float(data.get("retry_after", 5.0))
                except Exception:
                    retry_after = 5.0

                console.print(f"[grey78]⏳ Rate limited by Discord. Waiting {retry_after:.1f}s...[/grey78]")
                # Sleep in small increments so the user knows it's active
                end_time = time.time() + retry_after + 0.2
                while time.time() < end_time:
                    remaining = int(end_time - time.time())
                    if remaining > 0 and remaining % 10 == 0:
                        console.print(f"[dim grey50]Waiting on Discord rate limit... {remaining}s remaining[/dim grey50]")
                    time.sleep(1)
                continue

            return resp

    # ─── guilds ──────────────────────────────────────────────────────────────

    def get_my_guilds(self) -> list[dict]:
        """Return all guilds the authenticated user/bot is in."""
        resp = self._request("GET", "/users/@me/guilds")
        resp.raise_for_status()
        return resp.json()

    def get_guild(self, guild_id: str) -> dict:
        resp = self._request("GET", f"/guilds/{guild_id}")
        resp.raise_for_status()
        return resp.json()

    # ─── emojis ──────────────────────────────────────────────────────────────

    def list_emojis(self, guild_id: str) -> list[dict]:
        resp = self._request("GET", f"/guilds/{guild_id}/emojis")
        resp.raise_for_status()
        return resp.json()

    def get_emoji_image_b64(self, emoji: dict) -> str:
        """Download emoji image and return as base64 data URI."""
        ext = "gif" if emoji.get("animated") else "png"
        url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.{ext}?size=128&quality=lossless"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        mime = "image/gif" if emoji.get("animated") else "image/png"
        b64 = base64.b64encode(resp.content).decode()
        return f"data:{mime};base64,{b64}"

    def create_emoji(self, guild_id: str, name: str, image_b64: str) -> requests.Response:
        """Upload an emoji to the target guild."""
        payload = {"name": name, "image": image_b64}
        resp = self._request("POST", f"/guilds/{guild_id}/emojis", json=payload)
        return resp

    def delete_emoji(self, guild_id: str, emoji_id: str) -> requests.Response:
        return self._request("DELETE", f"/guilds/{guild_id}/emojis/{emoji_id}")

    # ─── stickers ────────────────────────────────────────────────────────────

    def list_stickers(self, guild_id: str) -> list[dict]:
        resp = self._request("GET", f"/guilds/{guild_id}/stickers")
        resp.raise_for_status()
        return resp.json()

    def get_sticker_file(self, sticker: dict) -> tuple[bytes, str, str]:
        """Download sticker file. Returns (bytes, mime_type, extension)."""
        fmt_map = {1: ("png", "image/png"), 2: ("apng", "image/png"),
                   3: ("lottie", "application/json"), 4: ("gif", "image/gif")}
        fmt_id = sticker.get("format_type", 1)
        ext, mime = fmt_map.get(fmt_id, ("png", "image/png"))
        url = f"https://media.discordapp.net/stickers/{sticker['id']}.{ext}"
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        return resp.content, mime, ext

    def create_sticker(
        self,
        guild_id: str,
        name: str,
        description: str,
        tags: str,
        file_bytes: bytes,
        mime: str,
        ext: str,
    ) -> requests.Response:
        """Upload a sticker using multipart/form-data."""
        files = {"file": (f"sticker.{ext}", file_bytes, mime)}
        data = {
            "name": name,
            "description": description or name,
            "tags": tags or name[:200],
        }
        headers_copy = {k: v for k, v in self.session.headers.items()
                        if k.lower() != "content-type"}
        resp = requests.post(
            f"{BASE_URL}/guilds/{guild_id}/stickers",
            headers=headers_copy,
            data=data,
            files=files,
            timeout=30,
        )
        return resp

    def delete_sticker(self, guild_id: str, sticker_id: str) -> requests.Response:
        return self._request("DELETE", f"/guilds/{guild_id}/stickers/{sticker_id}")
