#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, AppIndicator3

APP_NAME = "wireguard-tray"

ICON_DIR = "/usr/share/wireguard-tray/icons"
ICON_OFF = os.path.join(ICON_DIR, "icon-off.png")
ICON_ON = os.path.join(ICON_DIR, "icon-on.png")

CONFIG_DIR = os.path.join(os.path.expanduser("~/.config"), APP_NAME)
STATE_FILE = os.path.join(CONFIG_DIR, "state")

WG_QUICK = "/usr/bin/wg-quick"

DEFAULT_INTERFACE = "wg0"

indicator = None
current_interface = DEFAULT_INTERFACE

def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def notify(title, message, icon=ICON_OFF):
    subprocess.Popen(
        ["notify-send", "-i", icon, title, message],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def run_wg(action, iface=None):
    cmd = ["sudo", WG_QUICK, action]
    if iface:
        cmd.append(iface)

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        stderr = result.stderr.lower()
        if action == "up" and "already exists" in stderr:
            print(f"wg-{iface} already up")
            return
        if action == "down" and "not found" in stderr:
            print(f"wg-{iface} already down")
            return
        print(result.stderr.strip())
        sys.exit(result.returncode)

def load_state():
    global current_interface
    ensure_config_dir()
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            current_interface = f.read().strip() or DEFAULT_INTERFACE

def save_state():
    ensure_config_dir()
    with open(STATE_FILE, "w") as f:
        f.write(current_interface)

def connect():
    try:
        run_wg("up", current_interface)
        indicator.set_icon(ICON_ON)
        indicator.set_label("VPN включён", "")
        notify("WireGuard", f"Подключён: {current_interface}", ICON_ON)
        return True
    except subprocess.CalledProcessError:
        indicator.set_icon(ICON_OFF)
        notify("WireGuard", "Ошибка подключения")
        return False

def disconnect():
    try:
        run_wg("down", current_interface)
        indicator.set_icon(ICON_OFF)
        indicator.set_label("VPN выключен", "")
        notify("WireGuard", f"Отключён: {current_interface}")
        return True
    except subprocess.CalledProcessError:
        notify("WireGuard", "Ошибка отключения")
        return False

def on_toggle(item):
    if item.get_active():
        if not connect():
            item.set_active(False)
    else:
        if not disconnect():
            item.set_active(True)

def on_interface_selected(_, iface):
    global current_interface
    current_interface = iface
    save_state()
    notify("WireGuard", f"Выбран интерфейс: {iface}")

def build_interface_menu():
    menu = Gtk.Menu()
    try:
        for f in os.listdir("/etc/wireguard"):
            if f.endswith(".conf"):
                iface = f[:-5]
                item = Gtk.MenuItem(label=iface)
                item.connect("activate", on_interface_selected, iface)
                menu.append(item)
    except PermissionError:
        menu.append(Gtk.MenuItem(label="Нет доступа к /etc/wireguard"))
    menu.show_all()
    return menu

def create_tray():
    global indicator
    indicator = AppIndicator3.Indicator.new(
        APP_NAME,
        ICON_OFF,
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_label("VPN", "")
    menu = Gtk.Menu()
    toggle = Gtk.CheckMenuItem(label="VPN")
    toggle.connect("toggled", on_toggle)
    menu.append(toggle)
    iface_item = Gtk.MenuItem(label="Интерфейс")
    iface_item.set_submenu(build_interface_menu())
    menu.append(iface_item)
    menu.append(Gtk.SeparatorMenuItem())
    quit_item = Gtk.MenuItem(label="Выход")
    quit_item.connect("activate", Gtk.main_quit)
    menu.append(quit_item)
    menu.show_all()
    indicator.set_menu(menu)

def handle_cli():
    parser = argparse.ArgumentParser(prog=APP_NAME)
    parser.add_argument("-a", "--autostart", action="store_true", help="Enable autostart")
    parser.add_argument("-d", "--disable-autostart", action="store_true", help="Disable autostart")
    parser.add_argument("-u", "--up", metavar="IFACE", help="Bring interface up and exit")
    parser.add_argument("-D", "--down", action="store_true", help="Bring interface down and exit")
    parser.add_argument("-s", "--sudo-setup", action="store_true", help="Setup sudoers for WireGuard")
    parser.add_argument("-S", "--set", metavar="IFACE", help="Set default interface")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        print("wireguard-tray 1.0.0")
        sys.exit(0)

    if args.autostart:
        subprocess.run(["systemctl", "--user", "enable", "--now", "wireguard-tray"])
        print("Autostart enabled")
        sys.exit(0)

    if args.disable_autostart:
        subprocess.run(["systemctl", "--user", "disable", "--now", "wireguard-tray"])
        print("Autostart disabled")
        sys.exit(0)

    if args.set:
        global current_interface
        current_interface = args.set
        save_state()
        print(f"Default interface set to {args.set}")
        sys.exit(0)

    if args.up:
        run_wg("up", args.up)
        sys.exit(0)

    if args.down:
        run_wg("down", current_interface)
        sys.exit(0)

    if args.sudo_setup:
        if os.geteuid() != 0:
            print("Запустите этот флаг с sudo!")
            sys.exit(1)
        user = os.getenv("SUDO_USER") or os.getenv("USER")
        sudoers_file = "/etc/sudoers.d/wireguard-tray"
        rules = [
            f"{user} ALL=(root) NOPASSWD: /usr/bin/wg-quick",
            f"{user} ALL=(root) NOPASSWD: /usr/bin/wg",
            f"{user} ALL=(root) NOPASSWD: /usr/bin/ip",
            f"{user} ALL=(root) NOPASSWD: /usr/bin/resolvectl",
            f"{user} ALL=(root) NOPASSWD: /usr/bin/resolvconf",
        ]
        with open(sudoers_file, "w") as f:
            f.write("\n".join(rules) + "\n")
        os.chmod(sudoers_file, 0o440)
        # права на /etc/wireguard
        subprocess.run(["sudo", "chmod", "750", "/etc/wireguard"])
        print(f"Sudoers и права на /etc/wireguard настроены для {user}")
        sys.exit(0)

def main():
    handle_cli()
    load_state()
    create_tray()
    Gtk.main()

if __name__ == "__main__":
    main()
