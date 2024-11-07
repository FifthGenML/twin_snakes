#!/bin/bash

echo -e "\033[1;32m"
echo "======================================="
echo "          TWIN SNAKES            "
echo "======================================="
echo -e "\033[0m"

# Create venv
if [ ! -d "venv" ]; then
    echo -e "\033[1;34m[1/5] Creating virtual environment...\033[0m"
    python3 -m venv venv
    echo -e "\033[1;32m✔ Virtual environment created.\033[0m"
else
    echo -e "\033[1;33m[1/5] Virtual environment already exists. Skipping...\033[0m"
fi

# activate
echo -e "\033[1;34m[2/5] Activating virtual environment...\033[0m"
source "$(pwd)/venv/bin/activate"
echo -e "\033[1;32m✔ Virtual environment activated.\033[0m"

# Install deps
echo -e "\033[1;34m[3/5] Installing dependencies...\033[0m"
pip install --upgrade pip
pip install -e .
pip freeze > requirements.txt
echo -e "\033[1;32m✔ Dependencies installed and requirements.txt updated.\033[0m"

# Alias
echo -e "\033[1;34m[4/5] Setting up alias...\033[0m"
if ! grep -q "alias twin_snakes=" ~/.bashrc; then
    echo "alias twin_snakes='source $(pwd)/venv/bin/activate && python -m src.attack'" >> ~/.bashrc
    echo -e "\033[1;32m✔ Alias added to .bashrc.\033[0m"
else
    echo -e "\033[1;33mAlias already exists in .bashrc. Skipping...\033[0m"
fi

# reload bashrc
echo -e "\033[1;34m[5/5] Reloading .bashrc...\033[0m"
source ~/.bashrc
echo -e "\033[1;32m✔ .bashrc reloaded.\033[0m"

#complete
echo -e "\033[1;32m======================================="
echo "   SETUP COMPLETE! "
echo "   Run the script with: twin_snakes [optional_image_path]"
echo "=======================================\033[0m"