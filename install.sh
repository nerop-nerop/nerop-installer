#!/bin/bash
# NEROP Quick Install - Простая установка одной командой

echo "=== NEROP Quick Install ==="

# Проверяем что не root
if [ "$EUID" -eq 0 ]; then 
    echo "Не запускайте скрипт от root!"
    exit 1
fi

# Проверяем Arch
if ! grep -q "Arch" /etc/os-release 2>/dev/null; then
    read -p "Похоже это не Arch Linux. Продолжить? (y/N): " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

echo "1. Установка yay..."
sudo pacman -S --noconfirm git base-devel
git clone https://aur.archlinux.org/yay.git /tmp/yay-tmp
cd /tmp/yay-tmp && makepkg -si --noconfirm
cd && rm -rf /tmp/yay-tmp

echo "2. Установка Hyprland и окружения..."
sudo pacman -S --noconfirm hyprland hyprpaper waybar kitty rofi

echo "3. Установка приложений..."
sudo pacman -S --noconfirm firefox telegram-desktop mpv vlc
yay -S --noconfirm yandex-music-desktop tty-clock cmatrix cava

echo "4. Копирование конфигураций..."
mkdir -p ~/.config/hypr ~/.config/waybar ~/.config/kitty
cp -f configs/hyprland/hyprland.conf ~/.config/hypr/
cp -f configs/waybar/config ~/.config/waybar/
cp -f configs/kitty/kitty.conf ~/.config/kitty/

echo ""
echo "✅ Готово! Перезагрузитесь: sudo reboot"
echo "   На экране входа выберите Hyprland"
