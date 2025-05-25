#!/bin/bash

echo "⚙️ Disabling GNOME thumbnailing..."
gsettings set org.gnome.desktop.thumbnailers disable true

echo "🧹 Clearing thumbnail cache..."
rm -rf ~/.cache/thumbnails/*

echo "✅ Done. Thumbnailing disabled and cache cleared."

echo ""
echo "🔒 Optional: If you're running a Python script that processes images,"
echo "   you can add this to the top of your script to prevent GUI access:"
echo ""
echo "   import os"
echo "   os.environ['DISPLAY'] = ''"
echo ""

