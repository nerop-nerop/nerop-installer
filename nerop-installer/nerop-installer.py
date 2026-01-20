#!/usr/bin/env python3
"""
NEROP Installer - Полная версия
"""

import subprocess
import sys
import os
import shutil
import requests
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

def run_cmd(cmd, desc="", use_sudo=False, show_output=True):
    """Выполняет команду"""
    if desc:
        print(f"\n▶ {desc}")
    print(f"   $ {cmd}")
    
    try:
        if use_sudo:
            full_cmd = f'sudo {cmd}'
        else:
            full_cmd = cmd
        
        if show_output:
            result = subprocess.run(full_cmd, shell=True, check=False, 
                                  stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        else:
            result = subprocess.run(full_cmd, shell=True, check=False)
        
        if result.returncode == 0:
            if show_output and result.stdout:
                print(f"   ✅ Успешно")
            return True
        else:
            if show_output and result.stderr:
                print(f"   ⚠️  Ошибка: {result.stderr.decode('utf-8')[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def install_yay():
    """Устанавливает yay"""
    print("   Установка yay из AUR...")
    
    commands = [
        "git clone https://aur.archlinux.org/yay.git /tmp/yay_install",
        "cd /tmp/yay_install && makepkg -si --noconfirm",
        "rm -rf /tmp/yay_install"
    ]
    
    for cmd in commands:
        if not run_cmd(cmd, use_sudo=False):
            return False
    return True

def install_paru():
    """Устанавливает paru"""
    print("   Установка paru из AUR...")
    
    commands = [
        "git clone https://aur.archlinux.org/paru.git /tmp/paru_install",
        "cd /tmp/paru_install && makepkg -si --noconfirm",
        "rm -rf /tmp/paru_install"
    ]
    
    for cmd in commands:
        if not run_cmd(cmd, use_sudo=False):
            return False
    return True

def install_pycharm():
    """Устанавливает PyCharm из AUR"""
    print("\n   Установка PyCharm...")
    
    # Попробуем разные варианты пакетов PyCharm из AUR
    pycharm_versions = [
        "pycharm-community-edition",  # Бесплатная версия
        "pycharm-professional",       # Профессиональная версия
        "pycharm-community-bin"       # Бинарная версия
    ]
    
    for pkg in pycharm_versions:
        print(f"   Пробуем установить {pkg}...")
        if run_cmd(f"yay -S --noconfirm {pkg}", use_sudo=False, show_output=False):
            print(f"   ✅ {pkg} установлен")
            return True
    
    print("   ⚠️  Не удалось установить PyCharm через AUR")
    print("   💡 Попробуйте установить вручную: yay -S pycharm-community-edition")
    return False

def install_steam():
    """Устанавливает Steam"""
    print("\n   Установка Steam...")
    
    # Включим multilib репозиторий если не включен
    if not os.path.exists("/etc/pacman.conf.bak"):
        run_cmd("cp /etc/pacman.conf /etc/pacman.conf.bak", use_sudo=True)
    
    # Проверяем, включен ли multilib
    with open("/etc/pacman.conf", 'r') as f:
        pacman_conf = f.read()
    
    if "[multilib]" not in pacman_conf:
        print("   Включаем multilib репозиторий...")
        # Добавляем multilib в конец файла
        run_cmd('echo -e "\n[multilib]\nInclude = /etc/pacman.d/mirrorlist" >> /etc/pacman.conf', 
                use_sudo=True)
        # Обновляем базу данных
        run_cmd("pacman -Sy", use_sudo=True)
    
    # Устанавливаем Steam
    if run_cmd("pacman -S --needed --noconfirm steam steam-native-runtime", 
               "Установка Steam", use_sudo=True):
        print("   ✅ Steam установлен")
        return True
    else:
        print("   ⚠️  Пробуем установить Steam через AUR...")
        if run_cmd("yay -S --noconfirm steam-manjaro", use_sudo=False):
            print("   ✅ Steam установлен через AUR")
            return True
    
    print("   ❌ Не удалось установить Steam")
    return False

def install_yandex_music():
    """Устанавливает Яндекс.Музыку"""
    print("\n   Установка Яндекс.Музыки...")
    
    # Попробуем разные варианты из AUR
    yandex_packages = [
        "yandex-music-desktop-bin",
        "yandex-music-desktop-appimage",
        "yandex-music-desktop"
    ]
    
    for pkg in yandex_packages:
        print(f"   Пробуем {pkg}...")
        if run_cmd(f"yay -S --noconfirm {pkg}", use_sudo=False, show_output=False):
            print(f"   ✅ Яндекс.Музыка установлена ({pkg})")
            return True
    
    # Если AUR не сработал, установим напрямую из GitHub
    print("   Установка из GitHub...")
    
    # Создаем директорию для AppImage
    appimage_dir = Path.home() / "Applications"
    appimage_dir.mkdir(exist_ok=True)
    
    # URL для Яндекс.Музыки (последняя версия)
    yandex_url = "https://github.com/AppImage/appimage.github.io/raw/master/database/yandex-music-desktop"
    
    try:
        print("   Скачивание Яндекс.Музыки...")
        response = requests.get(yandex_url, stream=True)
        if response.status_code == 200:
            appimage_path = appimage_dir / "yandex-music.AppImage"
            with open(appimage_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Делаем исполняемым
            run_cmd(f"chmod +x {appimage_path}", use_sudo=False)
            
            # Создаем десктоп файл
            desktop_dir = Path.home() / ".local/share/applications"
            desktop_dir.mkdir(parents=True, exist_ok=True)
            
            desktop_content = f"""[Desktop Entry]
Name=Яндекс.Музыка
Exec={appimage_path}
Icon=music
Type=Application
Categories=Audio;Music;
"""
            
            desktop_file = desktop_dir / "yandex-music.desktop"
            with open(desktop_file, 'w') as f:
                f.write(desktop_content)
            
            print("   ✅ Яндекс.Музыка установлена из GitHub")
            return True
    except Exception as e:
        print(f"   ❌ Ошибка при установке из GitHub: {e}")
    
    print("   ⚠️  Не удалось установить Яндекс.Музыку")
    return False

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
    base_packages = ["git", "wget", "curl", "base-devel", "sudo", "neofetch"]
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
    
    # 5. Установка официальных пакетов
    print("\n5. УСТАНОВКА ОФИЦИАЛЬНЫХ ПАКЕТОВ")
    official_packages = [
        "cava", "cmatrix", "telegram-desktop",
        "hyprland", "hyprpaper", "hyprlock", "hypridle",
        "firefox", "kitty", "waybar", "rofi",
        "mpv", "vlc", "thunar",
        "polkit-kde-agent", "network-manager-applet",
        "pavucontrol", "bluez", "bluez-utils", "blueman",
        "slurp", "grim", "wl-clipboard",
        "discord", "obs-studio", "gimp", "inkscape"
    ]
    
    run_cmd(f"pacman -S --needed --noconfirm {' '.join(official_packages)}", 
            "Установка официальных пакетов", use_sudo=True)
    
    # 6. Установка Steam
    install_steam()
    
    # 7. Установка PyCharm
    install_pycharm()
    
    # 8. Установка AUR пакетов
    print("\n8. УСТАНОВКА AUR ПАКЕТОВ")
    aur_packages = [
        "tty-clock",
        "swaylock-effects",
        "visual-studio-code-bin",
        "spotify",
        "google-chrome",
        "vivaldi"
    ]
    
    for pkg in aur_packages:
        run_cmd(f"yay -S --noconfirm {pkg}", f"Установка {pkg}", use_sudo=False)
    
    # 9. Установка Яндекс.Музыки
    install_yandex_music()
    
    # 10. Копирование конфигураций
    print("\n9. КОПИРОВАНИЕ КОНФИГУРАЦИЙ")
    
    home = Path.home()
    project_dir = Path(__file__).parent.absolute()
    
    # Создаем директории
    config_dirs = [
        home/".config/hypr",
        home/".config/waybar", 
        home/".config/kitty",
        home/".config/rofi",
        home/".local/bin"
    ]
    
    for dir_path in config_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Создана директория: {dir_path}")
    
    # Копируем файлы если они существуют
    configs = [
        (project_dir/"configs/hyprland/hyprland.conf", home/".config/hypr/hyprland.conf"),
        (project_dir/"configs/waybar/config", home/".config/waybar/config"),
        (project_dir/"configs/kitty/kitty.conf", home/".config/kitty/kitty.conf"),
        (project_dir/"configs/rofi/config.rasi", home/".config/rofi/config.rasi")
    ]
    
    for src, dst in configs:
        if src.exists():
            shutil.copy2(src, dst)
            print(f"   ✅ {dst.name} скопирован")
        else:
            print(f"   📝 Создаем базовый конфиг для {dst.name}")
            # Создаем базовые конфиги если их нет
            if "hyprland" in str(dst):
                with open(dst, 'w') as f:
                    f.write("# Basic Hyprland config\n")
            elif "kitty" in str(dst):
                with open(dst, 'w') as f:
                    f.write("# Basic Kitty config\n")
    
    # 11. Финальное сообщение
    print("\n" + "="*60)
    print("✅ NEROP УСТАНОВКА ЗАВЕРШЕНА!")
    print("="*60)
    
    print("\n🎯 ЧТО УСТАНОВЛЕНО:")
    print("  • Hyprland, Waybar, Kitty, Rofi")
    print("  • Steam, PyCharm, VSCode, Firefox, Chrome")
    print("  • Telegram, Discord, Яндекс.Музыка, Spotify")
    print("  • OBS Studio, GIMP, Inkscape")
    print("  • cava, cmatrix, tty-clock, neofetch")
    
    print("\n🚀 ЗАПУСК:")
    print("  Steam:          steam")
    print("  PyCharm:        pycharm")
    print("  Яндекс.Музыка:  yandex-music")
    print("  Discord:        discord")
    
    print("\n💡 СОВЕТЫ:")
    print("  1. После перезагрузки выберите Hyprland в меню входа")
    print("  2. Для Steam может потребоваться установка proton: proton-ge-custom")
    print("  3. Обновляйте систему регулярно: sudo pacman -Syu")
    
    print("\n🔧 ПРОВЕРКА:")
    print("  Запустите: neofetch")
    print("  или: ./scripts/nerop-check.sh")
    
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Установка прервана")
        sys.exit(1)
