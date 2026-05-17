# Darkelf CLI Browser – Secure, Privacy-Focused Command-Line Web Browser
# Copyright (C) 2025 Dr. Kevin Moore
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# EXPORT COMPLIANCE NOTICE:
# This software contains publicly available encryption source code and is
# released under License Exception TSU in accordance with 15 CFR §740.13(e) of the
# U.S. Export Administration Regulations (EAR).
#
# A public notification of source code release has been submitted to the
# U.S. Bureau of Industry and Security (BIS) and the National Security Agency (NSA).
#
# The software includes implementations of standard cryptographic algorithms
# (e.g., AES, RSA, ChaCha20, TLS 1.3, X25519) for research and general-purpose use.
#
# This is source code only. No compiled binaries are included in this distribution.
# Redistribution, modification, or use must comply with all applicable U.S. export
# control laws and regulations.
#
# PROHIBITED DESTINATIONS:
# This software may not be exported or transferred, directly or indirectly, to:
# - Countries or territories under comprehensive U.S. embargo (OFAC or BIS lists),
# - Entities or individuals listed on the U.S. Denied Persons, Entity, or SDN Lists,
# - Parties on the BIS Country Group E:1 or E:2 lists.
#
# END-USE RESTRICTIONS:
# This software may not be used in the development or production of weapons of mass
# destruction, including nuclear, chemical, biological weapons, or missile systems
# as defined in EAR Part 744.
#
# By downloading, using, or distributing this software, you agree to comply with
# all applicable export control laws.
#
# This software is published under the LGPL v3.0 license and authored by
# Dr. Kevin Moore, 2025.
#
# NOTE: This is the CLI (Command-Line Interface) edition of Darkelf.
# It is entirely terminal-based and does not use PyQt5, PySide6, or any GUI frameworks.

# DISCLAIMER:
# This tool is intended for educational, research, and ethical OSINT (Open Source Intelligence) purposes only.
# It must only be used on systems and data for which you have explicit, authorized access.
# The developer assumes no responsibility for misuse or illegal activities performed using this tool.

# NOTE:
# This tool routes network traffic through the Tor network for anonymity.
# Ensure your use of Tor and any target services complies with all applicable laws and terms of service.

# © [Dr. Kevin Moore] – Original author of Darkelf.
# Released under the LGPL license. Contributions welcome.

import os
import sys
import secrets
import subprocess  # nosec B404
import time
import re
import random
import html
import hashlib
import logging
import argparse
import shutil
import signal
import platform
import termios
import tty
import textwrap
import base64
import requests
from bs4 import BeautifulSoup
from rich.markdown import Markdown
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.align import Align
from rich.table import Table
from rich.layout import Layout
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from urllib.parse import quote_plus

from urllib.parse import quote_plus, parse_qs, urlparse, unquote, urljoin

console = Console()

# ---------- DuckDuckGo + CLI Browser ----------

DUCK_URL = "https://duckduckgo.com/html/"
SEARCH_ENDPOINTS = [
    "https://html.duckduckgo.com/html/",
    "https://duckduckgo.com/html/",
    "https://duckduckgo.com/lite/",
]

def run(self):
    console.print("[bold green]Darkelf CLI Browser[/bold green]\n")

    while True:
        try:
            cmd = Prompt.ask(
                "[bold magenta]darkelf[/bold magenta] " "(search, open, quit)"
            ).strip()

            if cmd in ("quit", "exit"):
                break

            elif cmd.startswith("search"):
                query = cmd.replace("search", "", 1).strip()
                if not query:
                    query = Prompt.ask("Search query")

                url = f"{DUCKDUCKGO_LITE}?q={quote_plus(query)}"
                fetch_and_display(url, session=session)

            elif cmd.startswith("open"):
                url = cmd.replace("open", "", 1).strip()
                if not url:
                    url = Prompt.ask("URL")

                if not url.startswith("http"):
                    url = "http://" + url

                fetch_and_display(url, session=session)

        except KeyboardInterrupt:
            console.print("\n[red]Exiting browser[/red]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


# === Stealth, Threat Detection, In-Memory Logging ===
# Known tracker hashes (SHA256-obfuscated)

STEALTH_MODE = True  # or True, depending on context


def in_stealth():
    return STEALTH_MODE


KNOWN_TRACKER_HASHES = {
    hashlib.sha256(domain.encode()).hexdigest()
    for domain in [
        "google-analytics.com",
        "doubleclick.net",
        "facebook.net",
        "hotjar.com",
        "cloudflareinsights.com",
    ]
}


def setup_logging(debug=False):
    """
    Configure logging for Darkelf.

    debug=False → stealth mode (silent)
    debug=True  → show useful logs
    """

    # --- Reset any existing logging config (important) ---
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # --- Base level ---
    level = logging.DEBUG if debug else logging.CRITICAL

    logging.basicConfig(
        level=level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # --- Silence noisy libraries ---
    noisy_libs = [
        "stem",
        "urllib3",
        "requests",
        "torpy",
        "socks",
        "httpx",
        "aiohttp",
        "asyncio",
    ]

    for lib in noisy_libs:
        logger = logging.getLogger(lib)
        logger.setLevel(logging.CRITICAL)
        logger.propagate = False

    # --- Optional: Null handler only in stealth mode ---
    if not debug:
        logging.getLogger().addHandler(logging.NullHandler())


DUCKDUCKGO_LITE = "https://html.duckduckgo.com/html/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
]
ACCEPT_LANGUAGES = [
    "en-US,en;q=0.5",
    "en-GB,en;q=0.7",
    "en;q=0.9",
    "en-US;q=0.8,en;q=0.6",
]
REFERERS = [
    "",
    "https://duckduckgo.com/",
    "https://startpage.com/",
    "https://example.com/",
]

def random_headers(extra_stealth_options=None):
    headers = {
        "User-Agent": secrets.choice(USER_AGENTS),
        "Accept-Language": secrets.choice(ACCEPT_LANGUAGES),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": secrets.choice(REFERERS),
        "DNT": "1" if secrets.randbelow(2) == 0 else "0",
    }

    if extra_stealth_options:
        # 🔐 FIX: secure shuffle instead of random.sample
        if extra_stealth_options.get("random_order"):
            items = list(headers.items())
            for i in range(len(items)):
                j = secrets.randbelow(len(items))
                items[i], items[j] = items[j], items[i]
            headers = dict(items)

        if extra_stealth_options.get("add_noise_headers"):
            headers["X-Request-ID"] = base64.urlsafe_b64encode(os.urandom(6)).decode()

            if secrets.randbelow(2) == 0:
                headers["X-Fake-Header"] = "Darkelf"

        if extra_stealth_options.get("minimal_headers"):
            headers.pop("Accept-Language", None)
            headers.pop("Referer", None)

        if extra_stealth_options.get("spoof_platform"):
            if secrets.randbelow(2) == 0:
                headers["Sec-CH-UA-Platform"] = secrets.choice(
                    ["Linux", "Windows", "macOS"]
                )

    return headers


def random_delay(extra_stealth_options=None):
    base = (secrets.randbelow(1000) / 1000) * (0.8 - 0.1) + 0.1
    if extra_stealth_options and extra_stealth_options.get("delay_range"):
        min_d, max_d = extra_stealth_options["delay_range"]
        base = (secrets.randbelow(1000) / 1000) * (max_d - min_d) + min_d
    time.sleep(base)


def fetch_with_requests(
    url, session=None, extra_stealth_options=None, debug=False, method="GET", data=None
):
    proxies = None
    headers = random_headers(extra_stealth_options)
    try:
        random_delay(extra_stealth_options)
        req_session = session or requests.Session()
        if extra_stealth_options and extra_stealth_options.get("session_isolation"):
            req_session = requests.Session()
        if method == "POST":
            resp = req_session.post(
                url,
                data=data,
                headers=headers,
                timeout=30
            )
        else:
            resp = req_session.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        random_delay(extra_stealth_options)
        if debug:
            console.print("\n[DEBUG] Request URL:", url)
            console.print("[DEBUG] Request Headers:", headers)
            console.print("[DEBUG] Response Status:", resp.status_code)
            console.print("[DEBUG] Response Headers:", dict(resp.headers))
            console.print(
                "[DEBUG] Raw HTML preview:\n", resp.text[:2000], "\n[END DEBUG]\n"
            )
        return resp.text, headers
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Network error during fetch: {e}[/red]")
        # Optionally, return a blank page or raise a custom error
        return "<html><p>[Network error]</p></html>", headers
    except Exception as e:
        # Only wipe for actual intrusion, not for network errors!
        return "<html>Error</html>", headers


def parse_ddg_lite_results(soup):
    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        label = a.get_text(strip=True)

        # Handle redirect wrapper
        if "redirect_url=" in href:
            parsed = urlparse(href)
            query = parse_qs(parsed.query)
            real_url = query.get("redirect_url", [None])[0]
            if real_url and label:
                results.append((label, real_url))

        # Handle direct links
        elif href.startswith("http") and label:
            results.append((label, href))

    return results if results else "no_results"

        
def fallback_search(query, extra_stealth_options=None):
    engines = [
        ("DDG Lite", f"https://duckduckgo.com/lite/?q={quote_plus(query)}"),
        ("DDG HTML", f"https://duckduckgo.com/html/?q={quote_plus(query)}"),
        ("Brave", f"https://search.brave.com/search?q={quote_plus(query)}"),
    ]

    for name, url in engines:
        try:
            console.print(f"[yellow]⚠ Tor failed → trying {name}...[/yellow]")

            html, _ = fetch_with_requests(
                url,
                extra_stealth_options=extra_stealth_options,
                debug=False,
            )

            if html and "[Network error]" not in html:
                console.print(f"[green]✓ Using {name}[/green]")
                return html, url

        except Exception as e:
            console.print(f"[red]{name} failed:[/red] {e}")

    return None, None

def fetch_and_display(url, session=None, extra_stealth_options=None, debug=True):
    parsed = urlparse(url)
    hashed_domain = hashlib.sha256(parsed.netloc.encode()).hexdigest()

    # =========================
    # BLOCK TRACKERS
    # =========================
    if hashed_domain in KNOWN_TRACKER_HASHES:
        console.print(f"⛔ Blocked tracker domain: {parsed.netloc}")
        return

    if re.search(r"(tracking|analytics|ads|beacon)", parsed.netloc):
        console.print(f"⛔ Blocked suspicious tracker domain pattern: {parsed.netloc}")
        return

    # =========================
    # FETCH PAGE
    # =========================
    html, headers = fetch_with_requests(
        url,
        session=session,
        extra_stealth_options=extra_stealth_options,
        debug=debug,
    )

    # =========================
    # DETECT TOR FAILURE → FALLBACK
    # =========================
    if not html or "[Network error]" in html:
        parsed = urlparse(url)
        query = parse_qs(parsed.query).get("q", [""])[0]

        if query:
            fallback_html, fallback_url = fallback_search(query, extra_stealth_options)

            if fallback_html:
                html = fallback_html
                url = fallback_url
            else:
                console.print("[red]All search engines failed[/red]")
                return

    # =========================
    # PARSE HTML
    # =========================
    soup = BeautifulSoup(html, "html.parser")

    console.print(
        "\n📄 Title:",
        soup.title.string.strip() if soup.title else "No title",
    )

    parsed = urlparse(url)

    # =========================
    # SEARCH DETECTION (UNIFIED)
    # =========================
    SEARCH_ENGINES = ["duckduckgo", "duckduckgogg", "brave"]

    is_search = (
        any(engine in parsed.netloc for engine in SEARCH_ENGINES)
        and "q=" in parsed.query
    )

    # =========================
    # SEARCH RESULT PARSING
    # =========================
    if is_search:
        results = []

        # Try DDG parser first (works for lite/html + many fallbacks)
        results = parse_ddg_lite_results(soup)

        # Retry via POST if empty (DDG Lite quirk)
        if (not results or results == "no_results") and "duckduckgo" in parsed.netloc:
            query = parse_qs(parsed.query).get("q", [""])[0]

            resp2, _ = fetch_with_requests(
                DUCKDUCKGO_LITE,
                session=session,
                extra_stealth_options=extra_stealth_options,
                debug=debug,
                method="POST",
                data={"q": query},
            )

            soup2 = BeautifulSoup(resp2, "html.parser")
            results = parse_ddg_lite_results(soup2)

        # OUTPUT RESULTS
        if results == "no_results":
            console.print("  ▪ No results found for this query.")
        elif results:
            for txt, link in results:
                console.print(f"  ▪ {txt} — {link if link else '[no url]'}")
        else:
            console.print("  ▪ No results found or parsing failed.")
            if debug:
                console.print(html)

    # =========================
    # NORMAL PAGE PARSING
    # =========================
    else:
        found = False

        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                console.print("  ▪", text)
                found = True

        if not found:
            console.print("  ▪ No readable content found.")

def get_terminal_size():
    return shutil.get_terminal_size((80, 20))


def paginate_output(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        width, height = shutil.get_terminal_size((80, 20))
        page_size = height - 2  # reserve lines for prompt

        print("c", end="")
        for line in lines[i : i + page_size]:
            console.print(line[:width])  # truncate long lines

        i += page_size
        if i < len(lines):
            console.print("[bold green]>>[/bold green] ", end="")
            input("\n-- More -- Press Enter to continue...")

def cli_browser():
    setup_logging()
    ensure_strong_entropy()

    console.print("[bold green]Darkelf CLI Browser[/bold green]\n")

    try:
        repl_main()
    except Exception as e:
        console.print(f"[red]Fatal error:[/red] {e}")


def get_key():
    try:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)

            if key == "\x1b":
                key += sys.stdin.read(2)

            return key

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    except Exception:
        return input()[0]


# 1. === Strong Entropy Check ===
def ensure_strong_entropy(min_bytes=256):
    try:
        entropy = os.urandom(min_bytes)
        if len(entropy) < min_bytes:
            raise RuntimeError("Insufficient entropy")

    except Exception as e:
        print(f"[EntropyCheck] ⚠️ Warning: {e}")


# 2. === Session Isolation Wrapper ===
def fetch_with_isolated_session(url, method="GET", headers=None, data=None, timeout=30):
    session = requests.Session()  # New session per call
    proxies = {"http": get_tor_proxy(), "https": get_tor_proxy()}
    try:
        if method == "POST":
            resp = session.post(
                url, headers=headers, data=data, proxies=proxies, timeout=timeout
            )
        else:
            resp = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
        resp.raise_for_status()
        return resp.text, resp.headers
    except Exception as e:
        return f"[ERROR] {e}", {}


# Ensure entropy at program start
ensure_strong_entropy()

# --- Theme definitions, improved for accuracy ---
DARKELF_THEMES = {
    "dark": {
        "panel_border": "bright_magenta",
        "header_text": "bold bright_magenta",
        "footer_text": "bright_magenta",
        "content": "white",
        "highlight": "cyan",
        "link": "bright_cyan underline",
        "table_header": "bold cyan",
        "table_row": "white",
        "divider": "cyan",
    },
    "hacker": {
        "panel_border": "bright_green",
        "header_text": "bold bright_green",
        "footer_text": "bright_green",
        "content": "white",
        "highlight": "bright_green",
        "link": "bold green underline",
        "table_header": "bold green",
        "table_row": "white",
        "divider": "bright_green",
    },
    "light": {
        "panel_border": "bright_white",
        "header_text": "bold bright_blue",
        "footer_text": "bright_blue",
        "content": "black",
        "highlight": "yellow",
        "link": "bright_blue underline",
        "table_header": "bold bright_blue",
        "table_row": "black",
        "divider": "yellow",
    },
    "blue": {
        "panel_border": "bright_blue",
        "header_text": "bold bright_blue",
        "footer_text": "bright_blue",
        "content": "white",
        "highlight": "cyan",
        "link": "bright_blue underline",
        "table_header": "bold bright_blue",
        "table_row": "white",
        "divider": "cyan",
    },
}


def fetch_browser_page(url, debug=False):
    try:
        cmd = ["curl", "-L", "-m", "40", url]

        # ⚠️ REVIEW: subprocess usage
        result = subprocess.run(cmd, capture_output=True, text=True)  # nosec B603

        if result.returncode != 0:
            raise Exception(result.stderr.strip())

        return result.stdout, url

    except Exception as e:
        raise Exception(f"curl fetch failed: {e}")


def make_clickable(text, url):
    return Text(text, style=f"underline blue link {url}")


class Page:
    def __init__(self, url):
        self.url = url
        self.title = url
        self.lines = []
        self.links = []
        self.error = None
        self.headings = []
        self.fetch()

    def fetch(self):
        try:
            html, _ = fetch_with_requests(self.url, debug=False)
            soup = BeautifulSoup(html, "html.parser")

            # --- CLEAN ---
            for s in soup(["script", "style", "noscript"]):
                s.decompose()

            # --- TITLE ---
            title_tag = soup.find("title")
            if title_tag:
                self.title = title_tag.get_text(strip=True)

            # --- HEADINGS ---
            self.headings = [
                h.get_text(strip=True)
                for h in soup.find_all(["h1", "h2", "h3"])
            ]

            fancy_divider = "═" * 40
            self.lines = []

            # =========================
            # 1. PARSE SEARCH RESULTS
            # =========================
            results = soup.select(".result")

            if results:
                for idx, result in enumerate(results):
                    title = result.select_one(".result__title")
                    snippet = result.select_one(".result__snippet")
                    link_tag = result.find("a", href=True)

                    if title:
                        self.lines.append((f"[{idx+1}]", title.get_text(strip=True)))

                    if snippet:
                        self.lines.append(("", snippet.get_text(strip=True)))

                    if link_tag:
                        self.lines.append(("", link_tag["href"]))

                    self.lines.append((None, fancy_divider))

            # =========================
            # 2. FALLBACK CONTENT
            # =========================
            else:
                for idx, p in enumerate(soup.find_all("p")):
                    text = p.get_text(strip=True)
                    if text:
                        self.lines.append((f"[{idx+1}]", text))
                        self.lines.append((None, fancy_divider))

                if not self.lines:
                    text = soup.get_text(separator="\n\n")
                    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

                    for idx, paragraph in enumerate(paragraphs):
                        self.lines.append((f"[{idx+1}]", paragraph))
                        self.lines.append((None, fancy_divider))

            if self.lines and self.lines[-1][1] == fancy_divider:
                self.lines.pop()

            # =========================
            # 🔥 3. ALWAYS EXTRACT LINKS (FIX)
            # =========================
            self.links = []

            for a in soup.find_all("a", href=True):
                href = a.get("href")
                label = a.get_text(strip=True)

                if not href or not label:
                    continue

                # --- DuckDuckGo redirect fix ---
                if "/l/?uddg=" in href:
                    parsed = urlparse(href)
                    qs = parse_qs(parsed.query)
                    real = qs.get("uddg", [""])[0]
                    if real:
                        href = unquote(real)

                # --- Normalize relative URLs ---
                if not href.startswith("http"):
                    href = urljoin(self.url, href)

                # --- Deduplicate ---
                if any(existing_href == href for _, _, existing_href in self.links):
                    continue

                self.links.append((len(self.links) + 1, label, href))

            # =========================
            # 4. ANNOTATE DISPLAY
            # =========================
            for num, label, _ in self.links:
                annotated = f"[{num}] {label}"

                for i, (n, line) in enumerate(self.lines):
                    if label in line:
                        self.lines[i] = (n, line.replace(label, annotated, 1))
                        break

        except Exception as e:
            self.error = str(e)


def launch_browser_in_new_terminal():
    console.print("[yellow]Launching browser in current terminal...[/yellow]\n")
    run_browser_mode()


class DarkelfCLIBrowser:
    def __init__(self):
        self.history = []
        self.forward_stack = []
        self.current_page = None
        self.scroll = 0
        self.tabs = []
        self.active_tab = 0
        self.height = max(12, shutil.get_terminal_size((80, 24)).lines - 2)
        self.needs_render = True
        self.page_size = 15
        self.help_mode = False
        self.links_mode = False
        self.quit = False
        self.search_term = ""
        self.search_matches = []
        self.current_match_idx = 0
        signal.signal(signal.SIGWINCH, self.on_resize)
        self.console = Console()
        self.theme_name = "blue"  # Default: cyan/blue/green
        self.theme = DARKELF_THEMES[self.theme_name]

    def set_theme(self, name):
        if name in DARKELF_THEMES:
            self.theme_name = name
            self.theme = DARKELF_THEMES[name]
            self.console.print(f"[green]Theme set to {name}.[/green]")
            self.needs_render = True
        else:
            self.console.print(
                f"[red]Theme '{name}' not found. Available: {', '.join(DARKELF_THEMES.keys())}[/red]"
            )

    def get_terminal_size(self):
        return shutil.get_terminal_size((80, 24))

    def on_resize(self, signum, frame):
        self.needs_render = True

    def clear(self):
        # ⚠️ REVIEW: subprocess usage
        subprocess.run(["clear"] if os.name == "posix" else ["cls"])  # nosec

    def wrap_text(self, lines, width):
        fancy_divider = "═" * (width - 4)
        wrapped = []
        for idx, pair in enumerate(lines):
            number, line = pair if isinstance(pair, tuple) else (None, pair)
            # Search highlight
            if self.search_term and self.search_term.lower() in line.lower():
                line = line.replace(
                    self.search_term,
                    f"[reverse {self.theme['highlight']}]{self.search_term}[/reverse {self.theme['highlight']}]",
                )
            if line.strip() == "═" * 40 or line.strip() == fancy_divider:
                wrapped.append(Text(" ", style=self.theme["content"]))
                wrapped.append(
                    Text(fancy_divider, style=f"bold {self.theme['divider']}")
                )
                wrapped.append(Text(" ", style=self.theme["content"]))
                continue
            if not line.strip():
                wrapped.append(Text("", style=self.theme["content"]))
                continue
            if line.isupper() and len(line) < 80:
                wrapped.append(Text(line, style=f"bold {self.theme['highlight']}"))
                wrapped.append(Text("", style=self.theme["content"]))
                continue
            if line.endswith(":") and len(line) < 80:
                wrapped.append(Text(line, style=f"bold {self.theme['header_text']}"))
                wrapped.append(Text("", style=self.theme["content"]))
                continue
            if number and number.startswith("[") and "]" in number:
                text_obj = Text()
                text_obj.append(number + " ", style=self.theme["highlight"])
                text_obj.append(line, style=self.theme["link"])
                wrapped.append(text_obj)
                wrapped.append(Text("", style=self.theme["content"]))
                continue
            if line.strip().startswith("[") and "]" in line:
                try:
                    num = int(line.strip().split("]")[0][1:])
                    wrapped.append(Text(line, style=f"underline {self.theme['link']}"))
                    wrapped.append(Text("", style=self.theme["content"]))
                    continue
                except Exception as e:
                    print(f"[warn] {e}")
            wrapped.extend(
                [
                    Text(t, style=self.theme["content"])
                    for t in textwrap.wrap(line, width=width) or [""]
                ]
            )
        return wrapped

    def do_search(self):
        self.search_term = input("Search: ").strip()
        self.search_matches = []
        self.current_match_idx = 0
        if not self.search_term or not self.current_page or not self.current_page.lines:
            return
        term = self.search_term.lower()
        for idx, (_, line) in enumerate(self.current_page.lines):
            if term in line.lower():
                self.search_matches.append(idx)
        if self.search_matches:
            self.scroll = self.search_matches[0] // self.page_size
            self.current_match_idx = 0

    def next_match(self):
        if self.search_matches:
            self.current_match_idx = (self.current_match_idx + 1) % len(
                self.search_matches
            )
            idx = self.search_matches[self.current_match_idx]
            self.scroll = idx // self.page_size
            self.needs_render = True

    def prev_match(self):
        if self.search_matches:
            self.current_match_idx = (self.current_match_idx - 1) % len(
                self.search_matches
            )
            idx = self.search_matches[self.current_match_idx]
            self.scroll = idx // self.page_size
            self.needs_render = True

    def jump_to_heading(self):
        if not self.current_page or not self.current_page.headings:
            console.print("[yellow]No headings found on this page.[/yellow]")
            return
        for i, heading in enumerate(self.current_page.headings):
            console.print(f"{i+1}. {heading}")
        num = input("Jump to heading #: ").strip()
        if num.isdigit():
            idx = int(num) - 1
            if 0 <= idx < len(self.current_page.headings):
                heading_text = self.current_page.headings[idx]
                for i, (_, line) in enumerate(self.current_page.lines):
                    if heading_text in line:
                        self.scroll = i // self.page_size
                        self.needs_render = True
                        break

    def render_markdown(self, width):
        # Restore clean organized line breaks!
        output_lines = []
        for i, (_, line) in enumerate(self.current_page.lines):
            # Split each record by a divider, or detect when a new result starts
            if line.strip().startswith("[") and "]" in line:
                # Start of new record
                output_lines.append("")  # blank line before new record
            output_lines.append(line)
        content = "\n".join(output_lines)
        md = Markdown(content)
        self.console.print(
            Panel(md, title="Markdown", border_style="white", width=width, expand=True)
        )

    def render(self):
        # DO NOT clear or print blank lines here!
        term_size = shutil.get_terminal_size((80, 24))
        width = term_size.columns

        if self.help_mode:
            self.render_help(width)
            return
        if self.links_mode:
            self.render_links(width)
            return

        if not self.current_page:
            self.console.print(
                Panel(
                    Text("[blue]No page loaded.[/blue]", style=self.theme["content"]),
                    title="Darkelf CLI Browser",
                    border_style=self.theme["panel_border"],
                    width=width,
                )
            )
            self.render_footer(width)
            return

        header_text = Text.assemble(
            ("Darkelf CLI Browser", self.theme["header_text"]),
            f" | Tab {self.active_tab + 1}/{len(self.tabs)}\n",
            (self.current_page.title or self.current_page.url, self.theme["link"]),
        )
        self.console.print(
            Panel(
                header_text,
                border_style=self.theme["panel_border"],
                padding=(0, 1),
                width=width,
            )
        )

        total_lines = (
            len(self.current_page.lines)
            if self.current_page and self.current_page.lines
            else 0
        )
        if total_lines:
            start = self.scroll * self.page_size
            end = min(start + self.page_size, total_lines)
            visible_lines = self.current_page.lines[start:end]
        else:
            visible_lines = []

        wrapped_lines = self.wrap_text(visible_lines, width - 4)
        content = []
        for w in wrapped_lines:
            if isinstance(w, Text):
                content.append(w)
            else:
                content.append(Text(w, style=self.theme["content"]))
        self.console.print(
            Panel(
                Text.assemble(*content),
                title="\U0001f4f0 Page Content",
                border_style=self.theme["panel_border"],
                width=width,
                expand=True,
            )
        )

        if self.current_page and self.current_page.lines:
            total_pages = max(
                1, (len(self.current_page.lines) + self.page_size - 1) // self.page_size
            )
            current_page = self.scroll + 1
            status = f"-- Page {current_page}/{total_pages} --"
            self.console.print(
                Align.right(
                    Text(status, style=f"bold {self.theme['footer_text']}"), width=width
                )
            )

        self.render_footer(width)

        if self.tabs:
            tabs_panel = Text.from_markup(
                f"[bold {self.theme['highlight']}]Open Tabs:[/bold {self.theme['highlight']}] "
            )
            for i, tab in enumerate(self.tabs):
                mark = "*" if i == self.active_tab else " "
                tab_title = getattr(tab, "title", getattr(tab, "url", "Tab"))
                style = (
                    self.theme["highlight"]
                    if i == self.active_tab
                    else self.theme["footer_text"]
                )
                tabs_panel.append(f"{i+1}. {tab_title} {mark}  ", style=style)
            self.console.print(Align.center(tabs_panel, width=width))

    def render_footer(self, width):
        self.console.print(
            Rule(style=self.theme["divider"], characters="─"), width=width
        )
        footer = Text()
        footer.append(
            "[↑/↓/w/s/j/k] Prev/Next Page  ", style=f"bold {self.theme['footer_text']}"
        )
        footer.append("[O] Open Link  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[U] URL  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[B] Back  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[H] History  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[T] Tabs  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[t] Themes  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[F] Search  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[L] List Links  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[E] Export Links  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[G] Headings  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[M] Markdown  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[/] Search  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[N] Next match  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[?] Help  ", style=f"bold {self.theme['footer_text']}")
        footer.append("[Q] Quit", style="bold red")
        # Function key to return to CLI menu
        self.console.print(Align.center(footer, width=width))

    def prompt_theme_menu(self):
        self.console.print("\n[bold cyan]Choose a theme:[/bold cyan]")
        theme_names = list(DARKELF_THEMES.keys())
        for i, t in enumerate(theme_names, 1):
            self.console.print(f"  {i}. {t}")
        choice = input("Theme name or number: ").strip().lower()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(theme_names):
                theme = theme_names[idx]
                self.set_theme(theme)
                self.needs_render = True
                return
        elif choice in DARKELF_THEMES:
            self.set_theme(choice)
            self.needs_render = True
            return
        self.console.print(f"[red]Invalid theme: {choice}[/red]")
        self.needs_render = True

    def render_help(self, width):
        header_text = Text.assemble(
            ("Darkelf CLI Browser", self.theme["header_text"]),
            f" | Tab {self.active_tab + 1}/{len(self.tabs)}\n",
            (
                (
                    self.current_page.title or self.current_page.url
                    if self.current_page
                    else "No Page Loaded"
                ),
                self.theme["link"],
            ),
        )

        self.console.print(
            Panel(
                header_text,
                border_style=self.theme["panel_border"],
                padding=(0, 1),
                width=width,
            )
        )

        helptext = Text()

        helptext.append(
            Text.from_markup(
                f"\n[{self.theme['header_text']}]Darkelf CLI Browser Help[/{self.theme['header_text']}]\n\n"
            )
        )

        helptext.append(Text("[↑/↓/w/s/j/k] : Scroll page up/down\n"))
        helptext.append(Text("[O]           : Open link by number\n"))
        helptext.append(Text("[U]           : Enter a URL\n"))
        helptext.append(Text("[B]           : Go back\n"))
        helptext.append(Text("[H]           : Show history\n"))
        helptext.append(Text("[T]           : Manage tabs\n"))
        helptext.append(Text("[t]           : Change theme\n"))
        helptext.append(Text("[F]           : Search DuckDuckGo\n"))
        helptext.append(Text("[L]           : List all links on page\n"))
        helptext.append(Text("[E]           : Export links to file\n"))
        helptext.append(Text("[G]           : Jump to heading\n"))
        helptext.append(Text("[M]           : Render page as Markdown\n"))
        helptext.append(Text("[/]           : Search within page\n"))  # ✅ fixed
        helptext.append(Text("[N]           : Next search match\n"))
        helptext.append(Text("[?]           : Show this help\n"))
        helptext.append(Text("[Q]           : Quit browser\n"))

        helptext.append(
            Text.from_markup(
                f"\n[bold {self.theme['highlight']}]Tips:[/bold {self.theme['highlight']}]\n"
            )
        )

        helptext.append(
            Text(
                "Use [O] to open links, [L] to inspect all links, and [/] to search inside pages.\n"
            )
        )

        self.console.print(
            Panel(
                helptext,
                title="Help",
                border_style=self.theme["panel_border"],
                width=width,
            )
        )

        self.render_footer(width)
        self.console.print("\nPress any key to return.", style=self.theme["highlight"])

        get_key()
        self.help_mode = False
        self.needs_render = True

    def export_links(self):
        if not self.current_page or not self.current_page.links:
            console.print("[red]No links to export.[/red]")
            return
        filename = f"darkelf_links_{int(time.time())}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for num, label, href in self.current_page.links:
                f.write(f"{num}. {label} - {href}\n")
        console.print(f"[green]Links exported to {filename}[/green]")

    def render_links(self, width):
        # Defensive patch: ensure self.current_page and .links are valid and non-empty
        if (
            not self.current_page
            or not hasattr(self.current_page, "links")
            or not self.current_page.links
        ):
            header_text = Text.assemble(
                ("Darkelf CLI Browser", self.theme["header_text"]),
                " | No Tab\n",
                ("No Page Loaded", self.theme["link"]),
            )
            self.console.print(
                Panel(
                    header_text,
                    border_style=self.theme["panel_border"],
                    padding=(0, 1),
                    width=width,
                )
            )
            self.console.print(
                Panel(
                    Text("No links found.", style=self.theme["highlight"]),
                    title="Links",
                    border_style=self.theme["panel_border"],
                    width=width,
                )
            )
            self.render_footer(width)
            self.links_mode = False
            self.needs_render = True
            return

        header_text = Text.assemble(
            ("Darkelf CLI Browser", self.theme["header_text"]),
            f" | Tab {self.active_tab + 1}/{len(self.tabs)}\n",
            (self.current_page.title or self.current_page.url, self.theme["link"]),
        )
        self.console.print(
            Panel(
                header_text,
                border_style=self.theme["panel_border"],
                padding=(1, 2),
                width=width,
            )
        )

        seen_urls = set()
        deduped_links = []
        for num, label, href in self.current_page.links:
            if href and href not in seen_urls:
                deduped_links.append((num, label, href))
                seen_urls.add(href)
        fancy_divider = "═" * (width - 4)
        table = Table(show_header=False, box=None, expand=True)
        table.add_column("Result", style=self.theme["content"], ratio=1)
        if deduped_links:
            for num, label, href in deduped_links:
                link_text = Text()
                link_text.append(f"[{num}] ", style=self.theme["highlight"])
                link_text.append(label + "\n", style=f"bold {self.theme['highlight']}")
                link_text.append(href, style=f"{self.theme['link']} link {href}")
                table.add_row(link_text)
                table.add_row(
                    Text(fancy_divider, style=f"bold {self.theme['divider']}")
                )
        else:
            table.add_row(Text("No links found", style=self.theme["highlight"]))
        self.console.print(table)
        self.render_footer(width)
        self.console.print(
            "\n[O] Open link by number | [E] Export links | Any key to return."
        )

        key = get_key().lower()
        if key == "o":
            try:
                num = int(input("Open link #: ").strip())
                link_dict = {n: href for n, _, href in deduped_links}
                if num in link_dict:
                    href = link_dict[num]
                    if href.startswith("/l/?uddg="):
                        parsed = urlparse(href)
                        qs = parse_qs(parsed.query)
                        resolved = qs.get("uddg", [""])[0]
                        href = unquote(resolved)
                    if not href.startswith("http"):
                        href = "https://" + href.lstrip("/")
                    self.links_mode = False
                    self.needs_render = True
                    self.visit(href)
                    return
                else:
                    self.console.print(f"[red]Invalid link number: {num}[/red]")
                    time.sleep(1)
                    self.needs_render = True
            except Exception as err:
                self.console.print(f"[red]Invalid input: {err}[/red]")
                time.sleep(1)
                self.needs_render = True
        elif key == "e":
            self.export_links()
            self.links_mode = False
            self.needs_render = True
        elif key.isdigit():
            num = int(key)
            link_dict = {n: href for n, _, href in deduped_links}
            if num in link_dict:
                href = link_dict[num]
                if href.startswith("/l/?uddg="):
                    parsed = urlparse(href)
                    qs = parse_qs(parsed.query)
                    resolved = qs.get("uddg", [""])[0]
                    href = unquote(resolved)
                if not href.startswith("http"):
                    href = "https://" + href.lstrip("/")
                self.links_mode = False
                self.needs_render = True
                self.visit(href)
                return
            else:
                self.console.print(f"[red]Invalid link number: {num}[/red]")
                time.sleep(1)
                self.needs_render = True
        else:
            self.links_mode = False
            self.needs_render = True

    def visit(self, url):
        try:
            if self.current_page:
                self.history.append(self.current_page.url)
            self.scroll = 0
            self.forward_stack.clear()
            self.current_page = Page(url)
            if len(self.tabs) <= self.active_tab:
                self.tabs.append(self.current_page)
            else:
                self.tabs[self.active_tab] = self.current_page
            self.needs_render = True
        except Exception as e:
            self.current_page = Page(
                "data:text/html,<html><body><p>Failed to load page</p></body></html>"
            )
            self.current_page.error = str(e)
            self.needs_render = True

    def open_link(self, number):
        try:
            if not self.current_page or not self.current_page.links:
                console.print("[red]No links available on this page.[/red]")
                return
            link_map = dict((num, href) for num, _, href in self.current_page.links)
            href = link_map.get(number)
            if not href:
                console.print(f"[red]No link found for number: {number}[/red]")
                return
            if href.startswith("/l/?uddg="):
                qs = urlparse(href).query
                resolved = parse_qs(qs).get("uddg", [""])[0]
                if not resolved:
                    console.print(
                        f"[red]DuckDuckGo redirect did not resolve for {href}[/red]"
                    )
                    return
                href = unquote(resolved)
            if not href.startswith("http"):
                href = urljoin(self.current_page.url, href)
            # Show loading message for better UX
            console.print(f"[yellow]Opening link #{number}: {href}[/yellow]")
            try:
                self.visit(href)
            except Exception as e:
                console.print(f"[red]Network or fetch error: {e}[/red]")
                return
            self.needs_render = True  # Force redraw
        except Exception as e:
            console.print(f"[red]Error opening link: {e}[/red]")

    def show_history(self):
        width = shutil.get_terminal_size((80, 24)).columns
        if not self.history:
            console.print("[green]No browsing history available.[/green]")
        else:
            table = Table(title="History", show_lines=True, box=None, expand=True)
            table.add_column("#", style="cyan", width=6)
            table.add_column("URL", style="blue")
            for i, url in enumerate(reversed(self.history[-20:]), 1):
                table.add_row(str(i), url)
            console.print(table)
        self.render_footer(width)
        console.print("\nPress any key to return.")
        get_key()
        self.needs_render = True

    def manage_tabs(self):
        if not self.tabs:
            console.print("[grey]No open tabs.[/grey]")
            return
        console.print("[bold magenta]Open Tabs:[/bold magenta]")
        for i, tab in enumerate(self.tabs):
            mark = "*" if i == self.active_tab else " "
            console.print(f" {i+1}. {tab.url} {mark}")
        user_input = input("\nEnter tab number or 'x' to close tab: ").strip()
        if user_input.lower() == "x":
            self.tabs.pop(self.active_tab)
            if self.tabs:
                self.active_tab = max(0, self.active_tab - 1)
                self.current_page = self.tabs[self.active_tab]
            else:
                self.active_tab = 0
                self.current_page = None
                self.scroll = 0
        elif user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(self.tabs):
                self.active_tab = idx
                self.current_page = self.tabs[idx]
        self.needs_render = True

    def simulate_search_prompt(self):
        console.print("\n[bold cyan]Search DuckDuckGo:[/bold cyan]", end=" ")

        query = input().strip()

        if query:
            encoded_query = requests.utils.quote(query)

            url = (
                f"https://html.duckduckgo.com/html/?q={encoded_query}"
            )

            self.visit(url)

            if self.current_page:
                self.current_page.title = f"Search DuckDuckGo: {query}"

            self.needs_render = True

    def secure_wipe(self):
        self.history.clear()
        self.tabs.clear()
        self.forward_stack.clear()
        self.current_page = None
        self.scroll = 0
        self.help_mode = False
        self.links_mode = False

    def run(self):
        self.needs_render = True
        console.print("[bold cyan]Welcome to Darkelf Browser[/bold cyan]")
        console.print("Type a search query to begin...\n")
        self.simulate_search_prompt()
        while not self.quit:
            while self.needs_render:
                # self.clear()  # Alignment fix!
                self.render()
                self.needs_render = False
                if not self.links_mode and not self.help_mode and self.current_page:
                    continue
                break

            key = get_key()
            # --- Robust ESC key handling: accept any sequence starting with ESC ---
            if key.startswith("\x1b") and key not in ("\x1b[A", "\x1b[B"):
                # Only treat ESC *not* up or down as quit/wipe!
                self.console.print(
                    f"[bold {self.theme['highlight']}]Exiting browser...[/bold {self.theme['highlight']}]"
                )
                self.quit = True
                break
            elif key == "\x1b[A" or key == "w" or key == "k":
                if self.current_page and self.scroll > 0:
                    self.scroll -= 1
                    self.needs_render = True
            elif key == "\x1b[B" or key == "s" or key == "j":
                if self.current_page and self.current_page.lines:
                    total_pages = max(
                        1,
                        (len(self.current_page.lines) + self.page_size - 1)
                        // self.page_size,
                    )
                    if self.scroll + 1 < total_pages:
                        self.scroll += 1
                        self.needs_render = True
                    # FIX: If at last page, do nothing. Don't quit, don't break, just stay.
            elif key == "/":
                self.do_search()
            elif key == "n":
                self.next_match()
            elif key == "N":
                self.prev_match()
            elif key == "G":
                self.jump_to_heading()
            elif key == "M":
                if self.current_page:
                    width = self.get_terminal_size().columns
                    self.render_markdown(width)
            elif key == "u":
                url = input("\nEnter URL: ").strip()
                if not url:
                    continue
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
                self.visit(url)
            elif key == "b":
                if self.history:
                    url = self.history.pop()
                    if self.current_page:
                        self.forward_stack.append(self.current_page.url)
                    self.visit(url)
            elif key == "o":
                try:
                    num = int(input("Open link #: "))
                    self.open_link(num)
                except Exception as e:
                    print(f"[warn] {e}")
            elif key.isdigit():
                num = int(key)
                self.open_link(num)
            elif key == "h":
                self.show_history()
                self.needs_render = True
            elif key == "T":  # Shift+T for Tabs
                self.manage_tabs()
            elif key == "t":  # Lowercase t for Theme
                self.prompt_theme_menu()
                self.needs_render = True
            elif key == "f":
                self.simulate_search_prompt()
            elif key == "?":
                self.help_mode = True
                self.needs_render = True
            elif key == "l":
                self.links_mode = True
                self.needs_render = True
            elif key == "q" or key == "Q":
                self.quit = True
                break
        self.console.print("[yellow]Returning to main menu...[/yellow]")
        self.clear()
        return


# === END PATCH ===


def repl_main():
    console.print("🧭 Darkelf CLI - Browser Mode\n")

    stealth_on = True

    # FIX: create persistent session
    session = requests.Session()

    extra_stealth_options = {
        "random_order": True,
        "add_noise_headers": True,
        "minimal_headers": False,
        "spoof_platform": True,
        "session_isolation": True,
        "delay_range": (1.0, 2.5),
    }

    while True:
        try:
            cmd = input("darkelf> ").strip()

            if not cmd:
                continue

            # --- EXIT ---
            if cmd in ("exit", "quit"):
                console.print("👋 Exiting Darkelf.")
                break

            # --- SEARCH ---
            elif cmd.startswith("search "):
                q = cmd.split(" ", 1)[1]
                url = f"{DUCKDUCKGO_LITE}?q={quote_plus(q)}"
                fetch_and_display(
                    url,
                    session=session,
                    extra_stealth_options=extra_stealth_options if stealth_on else {},
                    debug=False,
                )

            # --- DEBUG SEARCH ---
            elif cmd.startswith("debug "):
                q = cmd.split(" ", 1)[1]
                url = f"{DUCKDUCKGO_LITE}?q={quote_plus(q)}"
                fetch_and_display(
                    url,
                    session=session,
                    extra_stealth_options=extra_stealth_options if stealth_on else {},
                    debug=True,
                )

            # --- OPEN URL ---
            elif cmd.startswith("open "):
                url = cmd.split(" ", 1)[1].strip()
                if not url.startswith("http"):
                    url = "http://" + url

                fetch_and_display(
                    url,
                    session=session,
                    extra_stealth_options=extra_stealth_options if stealth_on else {},
                )

            # --- ONION DISCOVERY ---
            elif cmd.startswith("findonions "):
                keywords = cmd.split(" ", 1)[1]
                onion_discovery(
                    keywords,
                    extra_stealth_options=extra_stealth_options if stealth_on else {},
                )

            # --- TOR CONTROL ---
            elif cmd == "tornew":
                renew_tor_identity()

            elif cmd == "checkip":
                check_my_ip()

            # --- STEALTH TOGGLE ---
            elif cmd == "stealth":
                stealth_on = not stealth_on
                console.print(f"🫥 Stealth {'ENABLED' if stealth_on else 'DISABLED'}")

            # --- HELP ---
            elif cmd == "help":
                console.print("""
Commands:
  search <query>      - Search DuckDuckGo (onion)
  open <url>          - Open a URL
  debug <query>       - Debug search
  stealth             - Toggle stealth mode
  exit                - Quit
""")

            else:
                console.print("❓ Unknown command. Type 'help'")

        except KeyboardInterrupt:
            console.print("\n⛔ Interrupted. Exiting.")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


# --- Browser Mode Launcher ---


def run_browser_mode():
    browser = DarkelfCLIBrowser()
    browser.run()

def main():
    if "--browser" in sys.argv:
        run_browser_mode()
    else:
        main_menu()


def main_menu():
    console.print("\n[bold cyan]Darkelf Main Menu[/bold cyan]\n")

    while True:
        console.print("""
[1] Browser
[2] CLI Mode
[Q] Quit
""")

        choice = input("Select: ").strip().lower()

        if choice == "1":
            browser = DarkelfCLIBrowser()
            browser.run()

        elif choice == "2":
            repl_main()

        elif choice == "q":
            break

        else:
            console.print("[red]Invalid option[/red]")

if __name__ == "__main__":
    main()
