# NEROP Installer 🚀

Автоматический установщик Arch Linux с окружением Hyprland

## Особенности
- Устанавливает **yay** и **paru** (оба AUR-хелпера)
- Настраивает окружение **Hyprland + Waybar + Kitty**
- Устанавливает основные приложения (Telegram, Firefox, Яндекс.Музыка, PyCharm)
- Включает готовые конфигурации для Hyprland, Waybar и Kitty
- Устанавливает терминальные утилиты (cava, cmatrix, tty-clock)

## Быстрая установка
```bash
# Скачать и запустить
curl -sL https://raw.githubusercontent.com/nerop_nerop/nerop-installer/main/nerop-installer.py | python3

# Или клонировать репозиторий
git clone https://github.com/ВАШ_НИК/nerop-installer.git
cd nerop-installer
./nerop-installer.py
./nerop-installer.py
./nerop-installer.py
ls -la nerop-installer.py

# Если нет прав на выполнение, дадим их
chmod +x nerop-installer.py

# Проверим шебанг (первая строка)
head -1 nerop-installer.py

# Должно быть: #!/usr/bin/env python3
# Если нет, исправим:
sed -i '1s/.*/#!\/usr\/bin\/env python3/' nerop-installer.py

ls -la nerop-installer.py

# Если нет прав на выполнение, дадим их
chmod +x nerop-installer.py

# Проверим шебанг (первая строка)
head -1 nerop-installer.py

# Должно быть: #!/usr/bin/env python3
# Если нет, исправим:
sed -i '1s/.*/#!\/usr\/bin\/env python3/' nerop-installer.py
python3 -m py_compile nerop-installer.py

# Если есть ошибки, покажем их
python3 -c "import ast; ast.parse(open('nerop-installer.py').read())"
python3 nerop-installer.py --help

python3 nerop-installer.py


cd /home/nerop/nerop-installer

# Сделаем backup старого скрипта
mv nerop-installer.py nerop-installer.py.old

# Создадим новый рабочий скрипт
cat > nerop-installer.py << 'EOF'
#!/usr/bin/env python3
"""
NEROP Installer - Простой установщик для Arch Linux
"""

import os
import sys
from pathlib import Path

def print_logo():
    print(r"""
__          __             __
\ \_________\ \____________\ \___
 \  _ \  _\ _  \  _\ __ \ __\   /
  \___/\__/\__/ \_\ \___/\__/\_\_
                      NEROP
    """)
    print("="*50)
    print("🚀 NEROP Installer for Arch Linux")
    print("="*50)

def main():
    print_logo()
    
    print("\n📦 Этот скрипт установит:")
    print("  1. AUR хелперы: yay и paru")
    print("  2. Hyprland, Waybar, Kitty, Rofi")
    print("  3. Telegram, Firefox, Яндекс.Музыка")
    print("  4. cava, cmatrix, tty-clock")
    print("  5. PyCharm и другие приложения")
    
    print("\n⚠️  ВНИМАНИЕ: Для работы скрипта нужны:")
    print("  - Arch Linux")
    print("  - Работающий интернет")
    print("  - Права sudo")
    
    response = input("\nПродолжить установку? (y/N): ").strip().lower()
    
    if response != 'y':
        print("❌ Установка отменена")
        sys.exit(0)
    
    print("\n✅ Готово! Для реальной установки нужно добавить команды pacman/yay.")
    print("   Сейчас это демо-версия.")
    
    print("\n📋 Дальнейшие действия:")
    print("  1. Запустите полную версию скрипта")
    print("  2. Или установите пакеты вручную:")
    print("     sudo pacman -S hyprland waybar kitty rofi")
    print("     sudo pacman -S telegram-desktop firefox")
    print("     git clone https://aur.archlinux.org/yay.git")
    print("     cd yay && makepkg -si")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Установка прервана")
        sys.exit(1)
