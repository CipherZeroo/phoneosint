#!/bin/bash
set -e

BOLD='\033[1m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${CYAN}${BOLD}"
echo "  ___ _                      ___  _____ _____ _   _ _____ "
echo " / _ \\ |__   ___  _ __ ___  / _ \\/  ___|_   _| \\ | |_   _|"
echo "/ /_)/ '_ \\ / _ \\| '_ \` _ \\/ /_\\ \\ \`--.  | | |  \\| | | |  "
echo "___/| | | | (_) | | | | |/ ___ \\ \`--. \\ | | | |\\  | | |  "
echo "\\/    |_| |_|\\___/|_| |_| |_/   \\_\\_____/ \\_/ \\_| \\_/ \\_/  "
echo -e "${NC}"
echo -e "${CYAN}PhoneOSINT Installer — by CipherZeroo${NC}"

PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
    echo -e "${RED}[!] Python not found.${NC}"; exit 1
fi
echo -e "${GREEN}[*] Using Python: $($PYTHON --version)${NC}"

if command -v apt &> /dev/null; then
    echo -e "${YELLOW}[*] Installing system dependencies...${NC}"
    sudo apt update -qq && sudo apt install -y python3-pip python3-venv
fi

echo -e "${YELLOW}[*] Installing Python dependencies...${NC}"
$PYTHON -m pip install --upgrade pip --quiet
$PYTHON -m pip install -r requirements.txt --quiet
$PYTHON -m pip install . --quiet

echo -e "${GREEN}${BOLD}[✓] PhoneOSINT installed!${NC}"
echo -e "Run: ${CYAN}phoneosint --number +1234567890${NC}"
