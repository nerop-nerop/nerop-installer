#!/bin/bash
echo "=== NEROP Simple Install ==="
echo ""

echo "1. Обновление системы..."
sudo pacman -Syu --noconfirm

echo ""
echo "2. Установка yay если нет..."
if ! command -v yay &> /dev/null; then
    sudo pacman -S --needed --noconfirm git base-devel
    git clone https://aur.archlinux.org/yay.git /tmp/yay-install
    cd /tmp/yay-install
    makepkg -si --noconfirm
    cd ~
    rm -rf /tmp/yay-install
fi

echo ""
echo "3. Установка Hyprland и окружения..."
sudo pacman -S --needed --noconfirm hyprland hyprpaper waybar kitty rofi

echo ""
echo "4. Установка приложений..."
sudo pacman -S --needed --noconfirm firefox telegram-desktop mpv vlc cava cmatrix

echo ""
echo "5. Установка AUR пакетов..."
yay -S --noconfirm tty-clock swaylock-effects

echo ""
echo "✅ Готово!"
echo "Перезагрузитесь: sudo reboot"
echo "На экране входа выберите Hyprland"
