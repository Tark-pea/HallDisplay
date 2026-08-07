#!/usr/bin/env bash
set -e
cd /home/braydon/HallDisplay
git pull --rebase

export DISPLAY=:0.0
xtrlock
python3 hall_display_ui.py
