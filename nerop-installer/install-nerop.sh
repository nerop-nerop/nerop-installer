#!/bin/bash
echo "=== NEROP Quick Install ==="
echo "Этот скрипт установит основные компоненты:"

echo ""
echo "1. Обновление системы..."
sudo pacman -Syu --noconfirm

echo ""
echo "2. Установка базовых утилит..."
sudo pacman -S --noconfirm git wget base-devel

echo ""
echo "3. Установка yay (AUR)..."
git clone https://aur.archlinux.org/yay.git /tmp/yay-nerop
cd /tmp/yay-nerop && makepkg -si --noconfirm
cd && rm -rf /tmp/yay-nerop

echo ""
echo "4. Установка Hyprland и окружения..."
sudo pacman -S --noconfirm hyprland hyprpaper waybar kitty rofi

echo ""
echo "5. Установка приложений..."
sudo pacman -S --noconfirm firefox telegram-desktop mpv vlc
yay -S --noconfirm yandex-music-desktop tty-clock cmatrix cava

echo ""
echo "✅ Готово! Перезагрузитесь: sudo reboot"
echo "   На экране входа выберите Hyprland"
