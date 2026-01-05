# WireGuard Tray

[![English](https://img.shields.io/badge/lang-English-blue)](README.md)
[![Russian](https://img.shields.io/badge/lang-Русский-red)](README.ru.md)

A lightweight system tray application for managing WireGuard VPN connections on Linux.

## Features

- 📌 **System tray integration** - Easy access from your desktop panel
- 🔄 **One-click connect/disconnect** - Toggle VPN with a single click
- 🎯 **Multiple interface support** - Switch between different WireGuard configurations
- 🔔 **Desktop notifications** - Get notified about connection status changes
- ⚡ **Quick CLI access** - Command-line interface for automation
- 🔧 **Sudoers auto-setup** - Easy configuration for passwordless VPN management
- 🚀 **Systemd autostart** - Launch at system startup

## Screenshots

![Tray Icon](icon-on.png) *Active connection*
![Tray Icon](icon-off.png) *Inactive connection*

## Installation

### From AUR (Arch Linux)

```bash
# Using yay
yay -S wireguard-tray

# Using paru
paru -S wireguard-tray
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/artemventvent/wireguard-tray.git
   cd wireguard-tray
   ```

2. Build and install:
   ```bash
   makepkg -si
   ```

## Configuration

### 1. Sudoers Setup

To run WireGuard without entering password each time:

```bash
sudo wireguard-tray --sudo-setup
```

This will create `/etc/sudoers.d/wireguard-tray` with appropriate permissions.

### 2. WireGuard Configuration

Place your WireGuard configuration files in `/etc/wireguard/`:
```bash
sudo nano /etc/wireguard/wg0.conf
```

Example configuration:
```ini
[Interface]
PrivateKey = YOUR_PRIVATE_KEY
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY
AllowedIPs = 0.0.0.0/0
Endpoint = vpn.server.com:51820
```

### 3. Autostart (Optional)

Enable automatic startup with systemd:
```bash
wireguard-tray --autostart
```

Disable autostart:
```bash
wireguard-tray --disable-autostart
```

## Usage

### Graphical Interface

1. Launch the application:
   ```bash
   wireguard-tray
   ```

2. Click the tray icon to see the menu:
   - **VPN** checkbox - Toggle connection on/off
   - **Interface** - Select WireGuard configuration
   - **Exit** - Quit the application

### Command Line Interface

```bash
# Show help
wireguard-tray --help

# Connect to specific interface
wireguard-tray --up wg0

# Disconnect current interface
wireguard-tray --down

# Set default interface
wireguard-tray --set wg1

# Enable autostart
wireguard-tray --autostart

# Disable autostart
wireguard-tray --disable-autostart

# Setup sudoers (run with sudo)
sudo wireguard-tray --sudo-setup

# Show version
wireguard-tray --version
```

## Project Structure

```
wireguard-tray/
├── tray.py                    # Main application script
├── icon-on.png               # Active connection icon
├── icon-off.png              # Inactive connection icon
├── wireguard-tray.desktop   # Desktop entry
├── wireguard-tray.service   # Systemd service file
├── wireguard-tray.install   # Post-installation script
├── PKGBUILD                 # Arch Linux package build file
└── README.md                # This file
```

## Dependencies

- **Python 3.x**
- **GTK 3** and Python bindings
- **libappindicator** for system tray integration
- **WireGuard Tools** (`wg-quick`)
- **libnotify** for desktop notifications

Install dependencies on Arch Linux:
```bash
sudo pacman -S python python-gobject gtk3 libappindicator-gtk3 wireguard-tools libnotify
```

## Troubleshooting

### Common Issues

1. **"Permission denied" when connecting**
   ```bash
   sudo wireguard-tray --sudo-setup
   ```

2. **No interfaces found in menu**
   Ensure WireGuard configs are in `/etc/wireguard/` with `.conf` extension:
   ```bash
   sudo chmod 755 /etc/wireguard/
   ls -la /etc/wireguard/*.conf
   ```

3. **Tray icon not showing**
   Check if your desktop environment supports AppIndicator:
   ```bash
   # For KDE Plasma
   sudo pacman -S plasma5-applets-appindicator
   
   # For GNOME
   sudo pacman -S gnome-shell-extension-appindicator
   ```

4. **Notifications not working**
   Ensure notification daemon is running:
   ```bash
   systemctl --user status dunst  # or whatever notification daemon you use
   ```

### Debug Mode

Run with verbose output:
```bash
python3 tray.py
```

Check systemd logs:
```bash
journalctl --user -u wireguard-tray -f
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Note**: This application is not officially affiliated with the WireGuard project.