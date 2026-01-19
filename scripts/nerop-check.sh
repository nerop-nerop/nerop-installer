#!/bin/bash
echo "=== NEROP System Check ==="
echo "Date: $(date)"
echo "Project: /home/nerop/nerop-installer"
echo ""
echo "📁 Project structure:"
echo "Files in project: $(find /home/nerop/nerop-installer -type f | wc -l)"
echo ""
echo "📦 Main files:"
ls -la /home/nerop/nerop-installer/*.py /home/nerop/nerop-installer/*.md /home/nerop/nerop-installer/.gitignore 2>/dev/null
echo ""
echo "🎨 Configurations:"
ls -la /home/nerop/nerop-installer/configs/*/* 2>/dev/null
echo ""
echo "✅ To install NEROP: ./nerop-installer.py"
echo "✅ Test command: ./nerop-installer.py --help"
