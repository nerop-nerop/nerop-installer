#!/usr/bin/env python3
"""
NEROP Installer - Исправленная версия
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def print_logo():
    print(r"""

   ____  ___  _________  ____
  / __ \/ _ \/ ___/ __ \/ __ \
 / / / /  __/ /  / /_/ / /_/ /
/_/ /_/\___/_/   \____/ .___/
                     /_/
                      NEROP(by @windagovnoitohka)
    """)
    print("="*50)
    print("🚀 NEROP Installer for Arch Linux")
    print("="*50)

def run_cmd(cmd, desc="", use_sudo=False):
    """Выполняет команду"""
    if desc:
        print(f"\n▶ {desc}")
    print(f"   $ {cmd}")
    
    try:
        if use_sudo:
            result = subprocess.run(f'sudo {cmd}', shell=True, check=False)
        else:
            result = subprocess.run(cmd, shell=True, check=False)
        
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def install_yay():
    """Устанавливает yay"""
    print("   Установка yay из AUR...")
    
    # Удаляем старую папку если есть
    run_cmd("rm -rf /tmp/yay_install", "", use_sudo=False)
    
    commands = [
        "git clone https://aur.archlinux.org/yay.git /tmp/yay_install",
        "cd /tmp/yay_install && makepkg -si --noconfirm",
        "rm -rf /tmp/yay_install"
    ]
    
    original_dir = os.getcwd()
    os.chdir("/tmp")
    
    for cmd in commands:
        if not run_cmd(cmd, use_sudo=False):
            os.chdir(original_dir)
            return False
    
    os.chdir(original_dir)
    return True

def install_paru():
    """Устанавливает paru"""
    print("   Установка paru из AUR...")
    
    # Удаляем старую папку если есть
    run_cmd("rm -rf /tmp/paru_install", "", use_sudo=False)
    
    commands = [
        "git clone https://aur.archlinux.org/paru.git /tmp/paru_install",
        "cd /tmp/paru_install && makepkg -si --noconfirm",
        "rm -rf /tmp/paru_install"
    ]
    
    original_dir = os.getcwd()
    os.chdir("/tmp")
    
    for cmd in commands:
        if not run_cmd(cmd, use_sudo=False):
            os.chdir(original_dir)
            return False
    
    os.chdir(original_dir)
    return True

def main():
    print_logo()
    
    # Проверка что не запускаем от root
    if os.geteuid() == 0:
        print("❌ Не запускайте скрипт от root! Используйте обычного пользователя.")
        sys.exit(1)
    
    print("\nЭтот скрипт установит/обновит NEROP окружение.")
    print("Уже установленные пакеты будут пропущены.\n")
    
    input("Нажмите Enter для продолжения или Ctrl+C для отмены...")
    
    # 1. Обновление системы
    print("\n1. ОБНОВЛЕНИЕ СИСТЕМЫ")
    run_cmd("pacman -Syu --noconfirm", "Обновление системы", use_sudo=True)
    
    # 2. Базовые утилиты
    print("\n2. БАЗОВЫЕ УТИЛИТЫ")
    base_packages = ["git", "wget", "base-devel", "sudo", "neofetch"]
    run_cmd(f"pacman -S --needed --noconfirm {' '.join(base_packages)}", 
            "Установка базовых утилит", use_sudo=True)
    
    # 3. Установка yay если нет
    print("\n3. УСТАНОВКА yay (AUR)")
    if run_cmd("which yay", "Проверка yay", use_sudo=False):
        print("   ✅ yay уже установлен")
    else:
        install_yay()
    
    # 4. Установка paru если нет
    print("\n4. УСТАНОВКА paru (альтернатива)")
    if run_cmd("which paru", "Проверка paru", use_sudo=False):
        print("   ✅ paru уже установлен")
    else:
        install_paru()
    
    # 5. Установка официальных пакетов (без python-pip и neofetch)
    print("\n5. УСТАНОВКА ОФИЦИАЛЬНЫХ ПАКЕТОВ")
    official_packages = [
        "cava", "cmatrix", "telegram-desktop",
        "hyprland", "hyprpaper", "hyprlock", "hypridle",
        "firefox", "kitty", "waybar", "rofi",
        "mpv", "vlc", "thunar",
        "polkit-kde-agent", "network-manager-applet",
        "pavucontrol", "bluez", "bluez-utils", "blueman",
        "slurp", "grim", "wl-clipboard"
    ]
    
    run_cmd(f"pacman -S --needed --noconfirm {' '.join(official_packages)}", 
            "Установка официальных пакетов", use_sudo=True)
    
    # 6. Установка AUR пакетов через yay (БЕЗ sudo!)
    print("\n6. УСТАНОВКА AUR ПАКЕТОВ")
    aur_packages = [
        "tty-clock",
        "swaylock-effects"
    ]
    
    # Пробуем установить Яндекс.Музыку
    print("   Установка tty-clock и swaylock-effects...")
    run_cmd(f"yay -S --noconfirm {' '.join(aur_packages)}", 
            "Установка AUR пакетов", use_sudo=False)
    
    print("   Попытка установки Яндекс.Музыки...")
    run_cmd("yay -S --noconfirm yandex-music-desktop", 
            "Установка Яндекс.Музыки", use_sudo=False)
    
    # 7. Копирование конфигураций
    print("\n7. КОПИРОВАНИЕ КОНФИГУРАЦИЙ")
    
    home = Path.home()
    project_dir = Path(__file__).parent.absolute()
    
    # Создаем директории
    for dir_path in [home/".config/hypr", home/".config/waybar", home/".config/kitty"]:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Создана директория: {dir_path}")
    
    # Копируем файлы
    configs = [
        (project_dir/"configs/hyprland/hyprland.conf", home/".config/hypr/hyprland.conf"),
        (project_dir/"configs/waybar/config", home/".config/waybar/config"),
        (project_dir/"configs/kitty/kitty.conf", home/".config/kitty/kitty.conf")
    ]
    
    for src, dst in configs:
        if src.exists():
            shutil.copy2(src, dst)
            print(f"   ✅ {dst.name} скопирован")
        else:
            print(f"   ⚠️  Не найден: {src}")
    
    # 8. Финальное сообщение
    print("\n" + "="*60)
    print("✅ NEROP УСТАНОВКА ЗАВЕРШЕНА!")
    print("="*60)
    print("\n🎯 ЧТО УСТАНОВЛЕНО:")
    print("  • Hyprland, Waybar, Kitty, Rofi")
    print("  • Telegram, Firefox, Медиаплееры")
    print("  • cava, cmatrix, tty-clock")
    print("  • Конфигурации для Hyprland, Waybar, Kitty")
    
    print("\n🚀 ДАЛЬНЕЙШИЕ ШАГИ:")
    print("  1. Перезагрузитесь: sudo reboot")
    print("  2. На экране входа выберите Hyprland")
    print("  3. Основные сочетания клавиш:")
    print("     • SUPER + Q - Терминал (Kitty)")
    print("     • SUPER + R - Запуск приложений (Rofi)")
    print("     • SUPER + F - Полноэкранный режим")
    
    print("\n🔧 ПРОВЕРКА:")
    print("  Запустите: ./scripts/nerop-check.sh")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Установка прервана")
        sys.exit(1)
