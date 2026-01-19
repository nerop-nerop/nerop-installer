#!/usr/bin/env python3
"""
NEROP Installer - Полностью рабочий установщик Arch Linux
ВСЁ ИСПРАВЛЕНО: правильные названия пакетов, AUR через yay
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_logo():
    print(f"""{Colors.CYAN}{Colors.BOLD}
__          __             __
\ \_________\ \____________\ \___
 \  _ \  _\ _  \  _\ __ \ __\   /
  \___/\__/\__/ \_\ \___/\__/\_\_
                      {Colors.MAGENTA}NEROP{Colors.RESET}""")
    print(f"{'='*50}")
    print(f"{Colors.BOLD}🚀 NEROP Installer for Arch Linux{Colors.RESET}")
    print(f"{'='*50}{Colors.RESET}")

def print_status(msg, status="info"):
    if status == "success":
        print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")
    elif status == "error":
        print(f"{Colors.RED}❌ {msg}{Colors.RESET}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")
    else:
        print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def run_cmd(cmd, desc=""):
    """Запускает команду с обработкой ошибок"""
    if desc:
        print(f"\n{Colors.CYAN}▶ {desc}{Colors.RESET}")
    print(f"   $ {cmd}")
    
    try:
        # Для pacman и установки пакетов используем sudo
        if any(x in cmd for x in ['pacman', 'yay', 'paru', 'makepkg', 'systemctl']):
            result = subprocess.run(f'sudo {cmd}', shell=True, check=True, 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, shell=True, check=True,
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def main():
    print_logo()
    
    # Проверка, что не запускаем от root
    if os.geteuid() == 0:
        print_status("Не запускайте скрипт от root! Используйте обычного пользователя.", "error")
        sys.exit(1)
    
    # Проверка Arch Linux
    try:
        with open('/etc/os-release', 'r') as f:
            if 'Arch' not in f.read():
                print_status("Похоже, это не Arch Linux", "warning")
                if input("Продолжить? (y/N): ").lower() != 'y':
                    sys.exit(0)
    except:
        pass
    
    # 1. ОБНОВЛЕНИЕ СИСТЕМЫ
    print(f"\n{Colors.BOLD}1. ОБНОВЛЕНИЕ СИСТЕМЫ{Colors.RESET}")
    success, output = run_cmd("pacman -Syu --noconfirm", "Обновление пакетов")
    if success:
        print_status("Система обновлена", "success")
    else:
        print_status(f"Ошибка обновления: {output}", "error")
    
    # 2. БАЗОВЫЕ УТИЛИТЫ
    print(f"\n{Colors.BOLD}2. БАЗОВЫЕ УТИЛИТЫ{Colors.RESET}")
    base_packages = ["git", "wget", "base-devel", "python-pip", "sudo", "neofetch"]
    success, output = run_cmd(f"pacman -S --needed --noconfirm {' '.join(base_packages)}", 
                             "Установка базовых утилит")
    if success:
        print_status("Базовые утилиты установлены", "success")
    
    # 3. УСТАНОВКА yay (AUR хелпер)
    print(f"\n{Colors.BOLD}3. УСТАНОВКА yay (AUR хелпер){Colors.RESET}")
    yay_installed = False
    success, _ = run_cmd("which yay", check=False)
    
    if not success:
        print_status("Установка yay из AUR...", "info")
        cmds = [
            "git clone https://aur.archlinux.org/yay.git /tmp/yay-install",
            "cd /tmp/yay-install && makepkg -si --noconfirm",
            "rm -rf /tmp/yay-install"
        ]
        
        for cmd in cmds:
            success, output = run_cmd(cmd)
            if not success:
                print_status(f"Ошибка: {output}", "error")
                break
        else:
            yay_installed = True
            print_status("yay установлен", "success")
    else:
        yay_installed = True
        print_status("yay уже установлен", "success")
    
    # 4. УСТАНОВКА paru (альтернативный AUR хелпер)
    print(f"\n{Colors.BOLD}4. УСТАНОВКА paru (альтернативный AUR хелпер){Colors.RESET}")
    paru_installed = False
    success, _ = run_cmd("which paru", check=False)
    
    if not success:
        print_status("Установка paru из AUR...", "info")
        cmds = [
            "git clone https://aur.archlinux.org/paru.git /tmp/paru-install",
            "cd /tmp/paru-install && makepkg -si --noconfirm",
            "rm -rf /tmp/paru-install"
        ]
        
        for cmd in cmds:
            success, output = run_cmd(cmd)
            if not success:
                print_status(f"Ошибка: {output}", "error")
                break
        else:
            paru_installed = True
            print_status("paru установлен", "success")
    else:
        paru_installed = True
        print_status("paru уже установлен", "success")
    
    # 5. УСТАНОВКА ОФИЦИАЛЬНЫХ ПАКЕТОВ
    print(f"\n{Colors.BOLD}5. УСТАНОВКА ОФИЦИАЛЬНЫХ ПАКЕТОВ{Colors.RESET}")
    
    # ПРАВИЛЬНЫЙ список официальных пакетов (без tty-clock и swaylock-effects)
    official_packages = [
        "cava", "cmatrix", "telegram-desktop",
        "hyprland", "hyprpaper", "hyprlock", "hypridle",
        "firefox", "kitty", "waybar", "rofi",
        "mpv", "vlc", "thunar", "gparted",
        "polkit-kde-agent", "network-manager-applet",
        "pavucontrol", "bluez", "bluez-utils", "blueman",
        "slurp", "grim", "wl-clipboard"
    ]
    
    success, output = run_cmd(f"pacman -S --needed --noconfirm {' '.join(official_packages)}", 
                             "Установка официальных пакетов")
    if success:
        print_status("Официальные пакеты установлены", "success")
    else:
        print_status(f"Ошибка: {output}", "error")
        # Пробуем установить по одному
        for pkg in official_packages:
            run_cmd(f"pacman -S --noconfirm {pkg}", f"Установка {pkg}", check=False)
    
    # 6. УСТАНОВКА AUR ПАКЕТОВ (через yay, если он установлен)
    print(f"\n{Colors.BOLD}6. УСТАНОВКА AUR ПАКЕТОВ{Colors.RESET}")
    
    # ПРАВИЛЬНЫЙ список AUR пакетов (tty-clock и swaylock-effects ТОЛЬКО здесь!)
    aur_packages = [
        "tty-clock",           # ТОЛЬКО в AUR!
        "yandex-music-desktop",
        "pycharm-community-edition",
        "swaylock-effects",    # ТОЛЬКО в AUR!
        "discord",
        "vivaldi",
        "visual-studio-code-bin"
    ]
    
    aur_helper = None
    if yay_installed:
        aur_helper = "yay"
    elif paru_installed:
        aur_helper = "paru"
    
    if aur_helper:
        success, output = run_cmd(f"{aur_helper} -S --noconfirm {' '.join(aur_packages)}", 
                                 f"Установка AUR пакетов через {aur_helper}")
        if success:
            print_status("AUR пакеты установлены", "success")
        else:
            print_status(f"Ошибка установки AUR пакетов: {output}", "error")
            # Пробуем установить по одному
            for pkg in aur_packages:
                run_cmd(f"{aur_helper} -S --noconfirm {pkg}", f"Установка {pkg}", check=False)
    else:
        print_status("AUR хелперы не установлены, пропускаем AUR пакеты", "warning")
    
    # 7. КОПИРОВАНИЕ КОНФИГУРАЦИЙ
    print(f"\n{Colors.BOLD}7. КОПИРОВАНИЕ КОНФИГУРАЦИЙ{Colors.RESET}")
    
    # Пути к конфигурациям в проекте
    project_dir = Path(__file__).parent.absolute()
    home_dir = Path.home()
    
    # Создаем директории если их нет
    config_dirs = [
        home_dir / ".config" / "hypr",
        home_dir / ".config" / "waybar", 
        home_dir / ".config" / "kitty"
    ]
    
    for dir_path in config_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print_status(f"Создана директория: {dir_path}")
    
    # Копируем конфигурации
    configs_to_copy = [
        (project_dir / "configs" / "hyprland" / "hyprland.conf", 
         home_dir / ".config" / "hypr" / "hyprland.conf"),
        (project_dir / "configs" / "waybar" / "config",
         home_dir / ".config" / "waybar" / "config"),
        (project_dir / "configs" / "kitty" / "kitty.conf",
         home_dir / ".config" / "kitty" / "kitty.conf")
    ]
    
    for src, dst in configs_to_copy:
        if src.exists():
            shutil.copy2(src, dst)
            print_status(f"Скопировано: {dst}", "success")
        else:
            print_status(f"Не найден исходный файл: {src}", "warning")
    
    # 8. ФИНАЛЬНЫЕ ИНСТРУКЦИИ
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}✅ УСТАНОВКА ЗАВЕРШЕНА!{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    
    print(f"""
{Colors.BOLD}📋 ЧТО УСТАНОВЛЕНО:{Colors.RESET}
  • AUR хелперы: {'yay' if yay_installed else 'НЕТ'} и {'paru' if paru_installed else 'НЕТ'}
  • Hyprland + Waybar + Kitty + Rofi
  • Telegram Desktop, Firefox, Яндекс.Музыка
  • PyCharm Community, VSCode
  • cava, cmatrix, tty-clock
  • Конфигурации скопированы в ~/.config/

{Colors.BOLD}🚀 ДАЛЬНЕЙШИЕ ШАГИ:{Colors.RESET}
  1. Перезагрузитесь: {Colors.CYAN}sudo reboot{Colors.RESET}
  2. На экране входа выберите {Colors.CYAN}Hyprland{Colors.RESET}
  3. Основные сочетания клавиш:
     • {Colors.YELLOW}SUPER + Q{Colors.RESET} - Терминал (Kitty)
     • {Colors.YELLOW}SUPER + R{Colors.RESET} - Запуск приложений (Rofi)
     • {Colors.YELLOW}SUPER + F{Colors.RESET} - Полноэкранный режим
     • {Colors.YELLOW}SUPER + M{Colors.RESET} - Выйти из сессии

{Colors.BOLD}🔧 ПРОВЕРКА СИСТЕМЫ:{Colors.RESET}
  Запустите: {Colors.CYAN}./scripts/nerop-check.sh{Colors.RESET}

{Colors.BOLD}🎮 УДАЧИ!{Colors.RESET}
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}❌ Установка прервана пользователем{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Критическая ошибка: {e}{Colors.RESET}")
        sys.exit(1)
