#!/bin/bash
echo "=== NEROP Simple Install ==="
echo "Скрипт устанавливает только самое необходимое:"
echo ""

echo "1. Обновление системы..."
sudo pacman -Syu --noconfirm

echo ""
echo "2. Установка Hyprland и окружения..."
sudo pacman -S --needed --noconfirm hyprland hyprpaper waybar kitty rofi

echo ""
echo "3. Установка приложений..."
sudo pacman -S --needed --noconfirm firefox telegram-desktop mpv vlc

echo ""
echo "4. Установка утилит..."
sudo pacman -S --needed --noconfirm cava cmatrix

echo ""
echo "5. Копирование конфигураций..."
mkdir -p ~/.config/hypr ~/.config/waybar ~/.config/kitty
cp -f configs/hyprland/hyprland.conf ~/.config/hypr/
cp -f configs/waybar/config ~/.config/waybar/
cp -f configs/kitty/kitty.conf ~/.config/kitty/

echo ""
echo "✅ Готово!"
echo "Перезагрузитесь: sudo reboot"
echo "На экране входа выберите Hyprland"
