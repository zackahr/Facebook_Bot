# Makefile for Facebook Comment Reply Bot

# Variables
PYTHON = python
PIP = pip

# Default target
all: install run

# Install required packages
install:
	$(PIP) install -r requirements.txt

# Run the bot
run:
	$(PYTHON) fb_bot.py

# Clean up (optional)
clean:
	find . -type f -name '*.pyc' -delete

