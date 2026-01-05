# WireGuard Tray

![Python](https://img.shields.io/badge/Made_with-Python-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Linux-ready-brightgreen?logo=linux)
![Status](https://img.shields.io/badge/Status-Active-blue)

> A minimalist tray-based GUI to manage WireGuard connections on Linux.

---

## ✅ Features

- One-click connect/disconnect WireGuard interfaces
- Auto-selection of the last used interface
- Browse and select any `.conf` file from `/etc/wireguard`
- Desktop notifications using `notify-send`
- Lightweight and efficient

---

## 📦 Dependencies

```bash
# Arch-based
sudo pacman -S wireguard-tools

# Debian/Ubuntu
sudo apt install wireguard 
```

---

## 🚀 Installation

```bash
git clone https://github.com/artemventvent/wireguardGuiV2.git
cd wireguardGuiV2
chmod +x tray.py
./tray.py
```

---

## 🔐 Passwordless Sudo Configuration

To avoid being prompted for a password on every operation:

### 1. Grant access to the configuration directory:

```bash
sudo chmod 775 /etc/wireguard
sudo chown $USER:root /etc/wireguard
```

### 2. Add rules to sudoers (run `sudo visudo`):

```bash
username ALL=(ALL) NOPASSWD: /usr/bin/wg-quick, /usr/bin/wg
username ALL=(ALL) NOPASSWD: /usr/bin/wg*, /usr/bin/wireguard*
```

Replace `username` with your actual Linux username.

---

## 🖼️ Icons

Icons should be placed in `~/wireguardGuiV2/`:

- `iconWireguard.png` — inactive state
- `iconWireguardON.png` — active state

You can change the icon path directly in `tray.py` if needed.

---

> Simple and effective WireGuard control from your system tray.
