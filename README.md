# Facebook Comment Reply Bot

This project is a Facebook bot that automatically replies to comments on specific posts. It uses **nodriver** for browser automation and interacts with Facebook posts by logging in with cookies, selecting comments, and sending replies.

## Features

- Load cookies from a file for authentication.
- Navigate to specific Facebook posts.
- Select and sort comments by "Newest."
- Reply to comments based on a predefined reply text.
- Configurable to process multiple profiles.
- Uses Nstbrowser API to avoid Facebook tracking, including fingerprint ID and IP address.
- Implements automatic proxy pool rotation.
- AI for automatic CAPTCHA recognition.
- Bypasses popular fingerprint checkers like pixelscan, BrowserLeaks, Whoer, and creepjs.
- Compatible with Puppeteer, Playwright, and Selenium.

## Read This Docs About NstBrowser

For more information, check out the official documentation: [NstBrowser Documentation](https://docs.nstbrowser.io/)

## Technologies Used

- Python
- nodriver
- Requests
- Asyncio
- Logging

## Prerequisites

- Python 3.7 or higher
- Install the required Python packages:

```bash
pip install nodriver requests
```

## Project Structure

```
.
├── Makefile                  # Makefile to manage project commands
├── requirements.txt          # File listing required Python packages
├── fb_bot.py                 # Main bot script
├── post_links.txt            # File containing post links
└── comment.txt               # File containing reply text
```

## Getting Started

1. **Clone the repository**:

   ```bash
   git clone https://github.com/zackahr/Facebook_Bot.git
   cd Facebook_Bot
   ```

2. **Set up your cookies**:
   - Export your Facebook cookies to a text file. Ensure the format is `name=value; name2=value2; ...`.

3. **Configure your posts and replies**:
   - Add the Facebook post links to `post_links.txt`, one link per line.
   - Write your reply text in `comment.txt`.

4. **Run the bot**:
   - Make sure you have your cookies and post links ready.
   - Use the provided `Makefile` to install dependencies and run the bot:

   ```bash
   make
   ```

5. **Clean up Python cache files** (optional):

   ```bash
   make clean
   ```

## Logging

The bot uses the logging module to log activities, making it easier to debug issues and track progress.

## Notes

- Ensure you comply with Facebook's terms of service when using this bot.
- Use responsibly and avoid spamming comments.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
