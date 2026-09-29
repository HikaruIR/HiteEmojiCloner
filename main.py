"""
main.py — Discord Emoji & Sticker Cloner CLI
Theme: Minimalist Dark Slate / Monochrome Gray
Language: Python 3.10+ | Dependencies: rich, requests
Run: python main.py
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn
from rich import box
from discord_api import DiscordAPI

console = Console()

# ─── DARK MINIMALIST BANNER ──────────────────────────────────────────────────

BANNER = """
[bold white]
  ███████╗███╗   ███╗ ██████╗      ██╗██╗
  ██╔════╝████╗ ████║██╔═══██╗     ██║██║
  █████╗  ██╔████╔██║██║   ██║     ██║██║
  ██╔══╝  ██║╚██╔╝██║██║   ██║██   ██║██║
  ███████╗██║ ╚═╝ ██║╚██████╔╝╚█████╔╝██║
  ╚══════╝╚═╝     ╚═╝ ╚═════╝  ╚════╝ ╚═╝
[/bold white]
[bold grey85]           Discord Emoji & Sticker Cloner[/bold grey85]
[dim grey62]        Minimalist Dark Edition  •  v1.2[/dim grey62]
"""

# ─── LOGGING HELPERS ─────────────────────────────────────────────────────────

def show_banner():
    console.print(Panel(BANNER, border_style="grey42", padding=(0, 2)))


def error(msg: str):
    console.print(f"[bold red]✕[/bold red] [grey85]{msg}[/grey85]")


def success(msg: str):
    console.print(f"[bold green]✓[/bold green] [grey85]{msg}[/grey85]")


def info(msg: str):
    console.print(f"[bold grey70]ℹ[/bold grey70] [grey85]{msg}[/grey85]")


def warn(msg: str):
    console.print(f"[bold yellow]⚠[/bold yellow] [grey78]{msg}[/grey78]")


def pick_guild(api: DiscordAPI, prompt_text: str = "Select a server") -> dict | None:
    """Show numbered list of guilds and let user pick one."""
    with console.status("[dim grey70]Fetching server list...[/dim grey70]"):
        try:
            guilds = api.get_my_guilds()
        except Exception as ex:
            error(f"Failed to fetch servers: {ex}")
            return None

    if not guilds:
        error("No servers found.")
        return None

    table = Table(title="Available Discord Servers", box=box.ROUNDED, border_style="grey42", title_style="bold grey85")
    table.add_column("#", style="bold grey70", width=4)
    table.add_column("Server Name", style="bold white")
    table.add_column("Server ID", style="dim grey50")

    for i, g in enumerate(guilds, 1):
        table.add_row(str(i), g["name"], g["id"])

    console.print(table)

    choice = Prompt.ask(f"[bold grey85]{prompt_text}[/bold grey85] [dim](enter number)[/dim]")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(guilds):
            return guilds[idx]
    except ValueError:
        pass
    error("Invalid selection.")
    return None


def pick_emojis(emojis: list[dict]) -> list[dict]:
    """Let user pick specific emojis from a list."""
    table = Table(title="Available Emojis", box=box.ROUNDED, border_style="grey42", title_style="bold grey85")
    table.add_column("#", style="bold grey70", width=4)
    table.add_column("Name", style="bold white")
    table.add_column("Type", style="grey62", width=8)
    table.add_column("ID", style="dim grey50")

    for i, e in enumerate(emojis, 1):
        anim = "Animated" if e.get("animated") else "Static"
        table.add_row(str(i), e["name"], anim, e["id"])

    console.print(table)
    console.print("[dim grey50]Separate numbers with commas (e.g. 1,3,5) or type 'ALL' for everything:[/dim grey50]")
    raw = Prompt.ask("[bold grey85]Select emojis[/bold grey85]").strip()

    if raw.upper() == "ALL":
        return emojis

    selected = []
    for part in raw.split(","):
        part = part.strip()
        try:
            idx = int(part) - 1
            if 0 <= idx < len(emojis):
                selected.append(emojis[idx])
        except ValueError:
            pass

    return selected


def pick_stickers(stickers: list[dict]) -> list[dict]:
    """Let user pick specific stickers from a list."""
    table = Table(title="Available Stickers", box=box.ROUNDED, border_style="grey42", title_style="bold grey85")
    table.add_column("#", style="bold grey70", width=4)
    table.add_column("Name", style="bold white")
    table.add_column("Format", style="grey62")
    table.add_column("ID", style="dim grey50")

    fmt_names = {1: "PNG", 2: "APNG", 3: "Lottie", 4: "GIF"}
    for i, s in enumerate(stickers, 1):
        fmt = fmt_names.get(s.get("format_type", 1), "Unknown")
        table.add_row(str(i), s["name"], fmt, s["id"])

    console.print(table)
    console.print("[dim grey50]Separate numbers with commas (e.g. 1,3,5) or type 'ALL' for everything:[/dim grey50]")
    raw = Prompt.ask("[bold grey85]Select stickers[/bold grey85]").strip()

    if raw.upper() == "ALL":
        return stickers

    selected = []
    for part in raw.split(","):
        part = part.strip()
        try:
            idx = int(part) - 1
            if 0 <= idx < len(stickers):
                selected.append(stickers[idx])
        except ValueError:
            pass
    return selected


# ─── CORE OPERATIONS ─────────────────────────────────────────────────────────

def op_copy_emojis(api: DiscordAPI):
    """Copy emojis (single or bulk) from a source server to a target server."""
    console.rule("[bold grey70]Copy Emojis[/bold grey70]", style="grey42")

    info("Select the SOURCE server:")
    src = pick_guild(api, "Source Server")
    if not src:
        return

    with console.status("[dim grey70]Fetching emojis...[/dim grey70]"):
        try:
            emojis = api.list_emojis(src["id"])
        except Exception as ex:
            error(f"Failed to fetch emojis: {ex}")
            return

    if not emojis:
        warn("This server has no custom emojis.")
        return

    info(f"Found [bold white]{len(emojis)}[/bold white] emojis.")
    selected = pick_emojis(emojis)

    if not selected:
        warn("No emojis selected.")
        return

    console.print()
    info("Select the DESTINATION server:")
    dst = pick_guild(api, "Destination Server")
    if not dst:
        return

    ok, fail = 0, 0
    with Progress(
        SpinnerColumn(style="grey70"),
        TextColumn("[grey85]{task.description}[/grey85]"),
        BarColumn(style="grey30", complete_style="grey85"),
        TaskProgressColumn(style="dim grey70"),
        console=console,
    ) as progress:
        task = progress.add_task("Uploading emojis...", total=len(selected))
        for emoji in selected:
            progress.update(task, description=f"Uploading: [bold white]{emoji['name']}[/bold white]")
            try:
                b64 = api.get_emoji_image_b64(emoji)
                resp = api.create_emoji(dst["id"], emoji["name"], b64)
                if resp.status_code in (200, 201):
                    ok += 1
                elif resp.status_code == 400 and "30008" in resp.text:
                    error("Server emoji slots are FULL! (Maximum 50 emojis reached for non-boosted server).")
                    fail += 1
                    break
                else:
                    fail += 1
                    warn(f"Error on {emoji['name']}: {resp.status_code} — {resp.text[:120]}")
            except Exception as ex:
                fail += 1
                warn(f"Error on {emoji['name']}: {ex}")
            time.sleep(0.5)
            progress.advance(task)

    console.print()
    success(f"[bold white]{ok}[/bold white] emojis copied successfully  |  [dim]{fail} failed[/dim]")


def op_copy_stickers(api: DiscordAPI):
    """Copy stickers (single or bulk) from a source server to a target server."""
    console.rule("[bold grey70]Copy Stickers[/bold grey70]", style="grey42")

    info("Select the SOURCE server:")
    src = pick_guild(api, "Source Server")
    if not src:
        return

    with console.status("[dim grey70]Fetching stickers...[/dim grey70]"):
        try:
            stickers = api.list_stickers(src["id"])
        except Exception as ex:
            error(f"Failed to fetch stickers: {ex}")
            return

    if not stickers:
        warn("This server has no stickers.")
        return

    info(f"Found [bold white]{len(stickers)}[/bold white] stickers.")
    selected = pick_stickers(stickers)

    if not selected:
        warn("No stickers selected.")
        return

    console.print()
    info("Select the DESTINATION server:")
    dst = pick_guild(api, "Destination Server")
    if not dst:
        return

    ok, fail = 0, 0
    with Progress(
        SpinnerColumn(style="grey70"),
        TextColumn("[grey85]{task.description}[/grey85]"),
        BarColumn(style="grey30", complete_style="grey85"),
        TaskProgressColumn(style="dim grey70"),
        console=console,
    ) as progress:
        task = progress.add_task("Uploading stickers...", total=len(selected))
        for sticker in selected:
            progress.update(task, description=f"Uploading: [bold white]{sticker['name']}[/bold white]")
            try:
                file_bytes, mime, ext = api.get_sticker_file(sticker)
                resp = api.create_sticker(
                    dst["id"],
                    sticker["name"],
                    sticker.get("description", sticker["name"]),
                    sticker.get("tags", sticker["name"][:200]),
                    file_bytes,
                    mime,
                    ext,
                )
                if resp.status_code in (200, 201):
                    ok += 1
                elif resp.status_code == 400 and "30008" in resp.text:
                    error("Server sticker slots are FULL!")
                    fail += 1
                    break
                else:
                    fail += 1
                    warn(f"Error on {sticker['name']}: {resp.status_code} — {resp.text[:120]}")
            except Exception as ex:
                fail += 1
                warn(f"Error on {sticker['name']}: {ex}")
            time.sleep(0.6)
            progress.advance(task)

    console.print()
    success(f"[bold white]{ok}[/bold white] stickers copied successfully  |  [dim]{fail} failed[/dim]")


def op_delete_emojis(api: DiscordAPI):
    """Delete all or selected emojis from the user's own server."""
    console.rule("[bold red]Delete Emojis[/bold red]", style="grey42")
    warn("Warning: This operation permanently removes emojis from your server!")

    info("Select your server:")
    guild = pick_guild(api, "Target Server")
    if not guild:
        return

    with console.status("[dim grey70]Fetching emojis...[/dim grey70]"):
        try:
            emojis = api.list_emojis(guild["id"])
        except Exception as ex:
            error(f"Failed to fetch emojis: {ex}")
            return

    if not emojis:
        warn("This server has no emojis.")
        return

    info(f"Found [bold white]{len(emojis)}[/bold white] emojis.")

    mode = Prompt.ask(
        "[bold grey85]Which emojis should be deleted?[/bold grey85]",
        choices=["all", "select"],
        default="select",
    )

    if mode == "select":
        target = pick_emojis(emojis)
    else:
        if not Confirm.ask(f"[bold red]Are you sure? All {len(emojis)} emojis will be deleted![/bold red]"):
            info("Operation cancelled.")
            return
        target = emojis

    if not target:
        warn("No emojis selected.")
        return

    ok, fail = 0, 0
    with Progress(
        SpinnerColumn(style="grey70"),
        TextColumn("[grey85]{task.description}[/grey85]"),
        BarColumn(style="grey30", complete_style="red"),
        TaskProgressColumn(style="dim grey70"),
        console=console,
    ) as progress:
        task = progress.add_task("Deleting emojis...", total=len(target))
        for emoji in target:
            progress.update(task, description=f"Deleting: [bold white]{emoji['name']}[/bold white]")
            try:
                resp = api.delete_emoji(guild["id"], emoji["id"])
                if resp.status_code == 204:
                    ok += 1
                else:
                    fail += 1
                    warn(f"Failed to delete {emoji['name']}: {resp.status_code}")
            except Exception as ex:
                fail += 1
                warn(f"Failed to delete {emoji['name']}: {ex}")
            time.sleep(0.3)
            progress.advance(task)

    console.print()
    success(f"[bold white]{ok}[/bold white] emojis deleted  |  [dim]{fail} failed[/dim]")


def op_delete_stickers(api: DiscordAPI):
    """Delete all or selected stickers from the user's own server."""
    console.rule("[bold red]Delete Stickers[/bold red]", style="grey42")
    warn("Warning: This operation permanently removes stickers from your server!")

    info("Select your server:")
    guild = pick_guild(api, "Target Server")
    if not guild:
        return

    with console.status("[dim grey70]Fetching stickers...[/dim grey70]"):
        try:
            stickers = api.list_stickers(guild["id"])
        except Exception as ex:
            error(f"Failed to fetch stickers: {ex}")
            return

    if not stickers:
        warn("This server has no stickers.")
        return

    info(f"Found [bold white]{len(stickers)}[/bold white] stickers.")

    mode = Prompt.ask(
        "[bold grey85]Which stickers should be deleted?[/bold grey85]",
        choices=["all", "select"],
        default="select",
    )

    if mode == "select":
        target = pick_stickers(stickers)
    else:
        if not Confirm.ask(f"[bold red]Are you sure? All {len(stickers)} stickers will be deleted![/bold red]"):
            info("Operation cancelled.")
            return
        target = stickers

    if not target:
        warn("No stickers selected.")
        return

    ok, fail = 0, 0
    with Progress(
        SpinnerColumn(style="grey70"),
        TextColumn("[grey85]{task.description}[/grey85]"),
        BarColumn(style="grey30", complete_style="red"),
        TaskProgressColumn(style="dim grey70"),
        console=console,
    ) as progress:
        task = progress.add_task("Deleting stickers...", total=len(target))
        for sticker in target:
            progress.update(task, description=f"Deleting: [bold white]{sticker['name']}[/bold white]")
            try:
                resp = api.delete_sticker(guild["id"], sticker["id"])
                if resp.status_code == 204:
                    ok += 1
                else:
                    fail += 1
                    warn(f"Failed to delete {sticker['name']}: {resp.status_code}")
            except Exception as ex:
                fail += 1
                warn(f"Failed to delete {sticker['name']}: {ex}")
            time.sleep(0.3)
            progress.advance(task)

    console.print()
    success(f"[bold white]{ok}[/bold white] stickers deleted  |  [dim]{fail} failed[/dim]")


# ─── MAIN MENU ───────────────────────────────────────────────────────────────

MENU_ITEMS = {
    "1": ("Clone Emojis from Server (Single or Bulk)", op_copy_emojis),
    "2": ("Clone Stickers from Server (Single or Bulk)", op_copy_stickers),
    "3": ("Delete Emojis from My Server (Single or All)", op_delete_emojis),
    "4": ("Delete Stickers from My Server (Single or All)", op_delete_stickers),
    "0": ("Exit", None),
}


def show_menu():
    table = Table(box=box.ROUNDED, border_style="grey42", show_header=False, padding=(0, 2))
    table.add_column("Key", style="bold grey70", width=4)
    table.add_column("Action", style="white")
    for key, (label, _) in MENU_ITEMS.items():
        table.add_row(key, label)
    console.print(table)


def main():
    show_banner()

    # ── Token input ──────────────────────────────────────────────────────────
    console.print(Panel(
        "[grey85]Enter your Discord Token:[/grey85]\n"
        "[dim grey62]- Bot Token: Discord Bot Token\n"
        "- User Token: Discord User Account Token (Self-bot)[/dim grey62]",
        title="[bold grey85]Authentication[/bold grey85]",
        border_style="grey42",
    ))

    token_type = Prompt.ask(
        "[bold grey85]Token Type[/bold grey85]",
        choices=["bot", "user"],
        default="bot",
    )
    token = Prompt.ask("[bold grey85]Token[/bold grey85]", password=True)

    is_bot = token_type == "bot"
    api = DiscordAPI(token.strip(), is_bot=is_bot)

    # ── Verify token ─────────────────────────────────────────────────────────
    with console.status("[dim grey70]Verifying token...[/dim grey70]"):
        try:
            guilds = api.get_my_guilds()
            success(f"Token verified. Found [bold white]{len(guilds)}[/bold white] accessible servers.")
        except Exception as ex:
            error(f"Invalid token or network error: {ex}")
            sys.exit(1)

    # ── Main loop ────────────────────────────────────────────────────────────
    while True:
        console.print()
        console.rule("[bold grey70]Main Menu[/bold grey70]", style="grey42")
        show_menu()
        console.print()

        choice = Prompt.ask("[bold grey85]Select an option[/bold grey85]", default="0").strip()

        if choice == "0":
            console.print("[dim grey62]\nGoodbye.\n[/dim grey62]")
            break

        if choice in MENU_ITEMS and MENU_ITEMS[choice][1]:
            console.print()
            try:
                MENU_ITEMS[choice][1](api)
            except KeyboardInterrupt:
                warn("\nOperation cancelled by user.")
            except Exception as ex:
                error(f"Unexpected error: {ex}")
        else:
            warn("Invalid selection, please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[dim grey62]\nGoodbye.\n[/dim grey62]")
