# 🧠 Darkelf CLI Post-Quantum OSINT & Secure Tor Terminal

Darkelf CLI is a post-quantum hardened OSINT Tool Kit and messaging platform for adversarial or censorship-heavy environments. Designed for operatives, researchers, and red teamers, it provides powerful reconnaissance and secure communication with memory-safe features and zero-API intelligence gathering.

---

## ⚙️ Features Overview

| Category                         | Description                                                                                                 |
|----------------------------------|-------------------------------------------------------------------------------------------------------------|
| 🔐 **Post-Quantum Messaging**    | ML-KEM-768 + Fernet hybrid encryption for encrypted CLI messaging, including async-prekey (X3DH) PQChat     |
| 💬 **DarkelfPQChat**             | Post-quantum secure chat with Ed25519 identity, Kyber768 session, async prekey (X3DH), replay protection, CLI exit |
| 🌐 **Tor-Based Browser**         | Full-text HTML browser routed over Tor (SOCKS5h proxy with obfs4, bridge fallback, multi-tab, themed)        |
| 🔎 **Darkelf OSINT Engine**      | Phone, email & username recon with zero APIs — DDG Onion, DNS, RDAP, leaks, dorking, and search link export |
| 🪪 **License Plate Search**      | Multi-dork and direct lookup of license plates (EU/US/CA) via OSINT, digitpol, findbyplate, and more        |
| 🎓 **Govscan Legal Search**      | Multi-jurisdiction court/case search: US (CourtListener), UK (BAILII), Australia (AustLII), worldwide LII   |
| 🧠 **Phishing Detection**        | Spoofed domain, lookalike, open dir, typosquatting, PQ-encrypted memory logs, no disk writes                |
| 💀 **Panic Mode**                | Erases memory, logs, local state, and triggers decoy traffic, plus secure file/vault wipe                   |
| 🔐 **Secure Vault**              | Kyber768 + Fernet/AES-GCM encrypted storage for recon results and CLI session logs, with secure wipe         |
| 🎭 **Stealth Enhancements**      | Memory locking, decoy background threads, header spoofing, sandbox/kernel/swap check, entropy check         |
| 🧪 **Log Encryption**            | AES-GCM encrypted logs in volatile memory, wiped on exit, with PQ log manager per category                  |
| 🧩 **Tool Launcher**             | CLI runner for OSINT tools: `nmap`, `shodan`, `amass`, `theharvester`, `sherlock`, `httpx`, etc.           |
| 🕵️ **.onion Search Engine**      | Onion discovery via Ahmia and DuckDuckGo Onion mirror, export results, link navigation                      |
| 📱 **Phone OSINT**               | Validity, region, VoIP & carrier check, disposable detection, with no PhoneInfoga API needed                |
| ✉️ **Email Intelligence**        | MX/DNS/TXT records, RDAP, breach checks, Gravatar, threat scoring, disposable detection                     |
| 📬 **EmailHunt Engine**          | Profile discovery from email/usernames on GitHub, Reddit, StackOverflow, and many more                      |
| 🕷️ **Async Web Spider**          | Fast, keyword-filtering, parallel crawling with email/hash/name extraction, spaCy NER summary               |
| ⚖️ **Legal/Court OSINT**         | Aggregates court/case info from multiple global legal databases and summarizes with spaCy NER                |
| 📦 **Vault Export/Import**       | Export any browser page to KyberVault, view/decrypt Vault files in CLI                                      |
| 🧑‍💻 **Memory & Kernel Monitor**  | Swap/dynamic_pager/entropy monitoring, triggers cleanup on forensic risk                                    |
| 📊 **IP/Network Tools**          | IP, ASN, ISP, and region lookup over Tor; DNS leak test; beacon check for .onion reachability               |
| 🛡️ **PegasusMonitor**            | Device scan for Pegasus/spyware indicators, hostfile poison, suspicious process/network scan                 |
| 🛠️ **Secure Cleanup**            | Secure delete (multi-pass) for logs, key files, RAM disk, and vaults                                        |
| 📜 **Markdown/History Export**   | Render current browser session as markdown, export session links, and view history                          |
| 🎨 **Theming/UI**                | Multiple terminal color themes, font obfuscation, rich panels, and responsive layout                        |
| 🧠 **spaCy NLP Summaries**       | All major OSINT modules provide optional spaCy-powered name/entity/party extraction and summaries           |
| 🕸️ **Decoy & Cover Traffic**     | Background threads for decoy onion traffic, Tor circuit auto-renew, cover-traffic in PQChat/NetworkProtector|
| 🚨 **SIGTERM/INT Secure Exit**   | Secure shutdown handler wipes sensitive state on Ctrl+C, kill, or exit                                      |
| 🧠 **Entropy/Anti-forensics**    | Ensures hardware entropy at boot, disables bash history, wipes memory logs                                  |
| 🔎 **CLI Help & Toolinfo**       | In-CLI help menus, tool descriptions, categorized tool listing, numbered shortcut launcher                   |

---

**All features above are present in this version of Darkelf CLI TL OSINT Tool Kit v3.0 as found in your code.**

---

## 🧰 Modules Included

- **Encrypted Messenger:** CLI-based secure communication with hybrid PQ+Symmetric encryption.
- **OSINT Engine:** Performs recon using only public Tor and DuckDuckGo onion-lite searches.
- **Phone Analyzer:** Validity, region, carrier detection, and potential disposable number checks.
- **Email Scanner:** Domain checks, breach results, and DNS intelligence—without using APIs.
- **Memory-Hardened Browser:** Fetch and parse web content securely from `.onion` and clearnet.
- **Tool Hub:** Launches external OSINT tools from a unified REPL interface.
- **Tor Beacon & Onion Validation:** Pings `.onion` services for uptime and status checks.
- **Fake Traffic Generator:** Background activity simulation to confuse behavioral forensics.
- **Secure Vault:** Stores sensitive session artifacts encrypted, supports purge/export.

---

## 🗄️ Secure Vault

Darkelf includes a memory-safe **Secure Vault** system that:
- 💾 Stores session logs, email/phone recon data, and Onion scans
- 🔐 Uses AES-GCM with optional hybrid PQ key-wrapping (`ML-KEM-768`)
- 🧼 Supports zeroization on exit or `panic` command
- 🔍 Vault entries can be listed, exported, or searched inside the REPL
- 🛡️ Optionally syncs across encrypted temp volumes if used in air-gapped systems

Use the REPL to manage your Vault:

## 🔧 Installation

### 1. Dependencies

Install Tor & Python 3.11:

```bash
# Debian/Ubuntu
sudo apt install tor python3.11

# macOS (using brew)
brew install tor python@3.11
```

### 2. Python Modules

```bash
pip install -r requirements.txt
```

---

## 🚀 Getting Started

```bash
python3.11 Darkelf_CLI_TL_Edition_Patched_FINAL_FIXED_WORKING.py
```

Use the REPL prompt for commands like:

- `search <query>` — DuckDuckGo .onion search
- `osintscan <phone|username>` — OSINT scan on target
- `message send` — Start encrypted messaging
- `vault show/export/clear` — Manage secure Vault entries
- `wipe` — Trigger panic mode
- `launch <tool>` — Run an integrated OSINT utility
- `beacon <onion>` — Check onion site status
- `exit` — Quit securely

---

## ✅ Supported Platforms

- ✅ macOS (Apple Silicon M1–M4)
- ✅ Linux (Debian, Arch, Fedora)
- ✅ Windows (WSL2 Recommended)
- ✅ Android (via Termux)

---

## 🔐 Security Model

- Encrypted logs are stored only in memory (`AES-GCM`) and purged on exit.
- All metadata stays local; no 3rd-party OSINT APIs like Numverify or PhoneInfoga are used.
- All search is routed through `DuckDuckGo Onion Lite` to bypass tracking & geofiltering.
- Carrier and location data is inferred offline using `phonenumbers`, `geocoder`, and `timezone`.

---

## 📝 Licenses & Attributions

This project includes:

- `psutil` — BSD 3-Clause
- `rich` — MIT
- `beautifulsoup4` — MIT
- `requests` — Apache 2.0
- `cryptography` — Apache 2.0
- `phonenumbers` — Apache 2.0
- `liboqs` & `pyoqs` — BSD & MIT (Post-Quantum Crypto)
- `stem` — Tor control interface

---

## 📫 Feedback & Contributions

Feel free to submit issues, patches, or modules. All tooling is designed with privacy, auditability, and operational flexibility in mind.
