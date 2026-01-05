pkgname=wireguard-tray
pkgver=1.0.0
pkgrel=1
pkgdesc="Minimal tray GUI to manage WireGuard connections on Linux"
arch=('any')
url="https://github.com/artemventvent/wireguardGuiV2"
license=('MIT')
depends=('python' 'python-gobject' 'gtk3' 'libappindicator-gtk3' 'wireguard-tools' 'libnotify')
source=(
    "tray.py"
    "icon-off.png"
    "icon-on.png"
    "wireguard-tray.desktop"
    "wireguard-tray.service"
)
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')
install="wireguard-tray.install"

package() {
    install -Dm755 "$srcdir/tray.py" "$pkgdir/usr/bin/wireguard-tray"
    install -dm755 "$pkgdir/usr/share/wireguard-tray/icons"
    install -Dm644 "$srcdir/icon-off.png" "$pkgdir/usr/share/wireguard-tray/icons/icon-off.png"
    install -Dm644 "$srcdir/icon-on.png" "$pkgdir/usr/share/wireguard-tray/icons/icon-on.png"
    install -Dm644 "$srcdir/wireguard-tray.service" "$pkgdir/usr/lib/systemd/user/wireguard-tray.service"
    install -Dm644 "$srcdir/wireguard-tray.desktop" "$pkgdir/usr/share/applications/wireguard-tray.desktop"
}