import json
import time
import logging
from urllib.parse import quote, urlencode
import nodriver as uc
from requests.exceptions import HTTPError, Timeout

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(_name_)

def get_debugger_port(url: str):
    try:
        res = requests.get(url, timeout=10).json()
        if 'data' not in res:
            raise ValueError(f"Unexpected response structure: {res}")
        return res['data']['port']
    except (HTTPError, Timeout, ValueError) as err:
        logger.error(f"Error getting debugger port: {err}")
        raise

def load_cookies_from_file(file_path):
    cookies = []
    try:
        with open(file_path, 'r') as file:
            cookie_str = file.read().strip()
            if cookie_str:
                cookie_pairs = cookie_str.split('; ')
                for pair in cookie_pairs:
                    name, value = pair.split('=', 1)
                    cookies.append({"name": name, "value": value, "domain": ".facebook.com"})
        logger.info(f"Loaded {len(cookies)} cookies from file.")
    except Exception as e:
        logger.error(f"Error reading cookies from file: {e}")
    return cookies

def load_post(file_path):
    try:
        with open(file_path, 'r') as file:
            post_links = [line.strip() for line in file if line.strip()]
        logger.info(f"Loaded {len(post_links)} post links from file.")
        return post_links
    except Exception as e:
        logger.error(f"Error reading post links from file: {e}")
        return []

async def login_with_cookies(page, post_file):
    post_links = load_post(post_file)
    if post_links:
        post = post_links[0]
        logger.info(f"Navigating to Facebook post: {post}")
        await page.goto(post)
        await page.evaluate("document.body.style.zoom='175%'")
        await page.wait_for_timeout(10000)
        await page.evaluate("window.scrollBy(0, 400);")
    else:
        logger.warning("No post links found. Exiting function.")
        return

async def select_new_comments(page):
    try:
        logger.info("Waiting for the Sort Comments button...")
        dropdown_button = await page.wait_for_selector(".xe0p6wg > div:nth-child(1) > span:nth-child(1)", timeout=10000)
        await dropdown_button.click()
        logger.info("Waiting for the Newest option...")
        new_comments_option = await page.wait_for_selector("xpath=//span[text()='Newest']", timeout=10000)
        await new_comments_option.click()
    except Exception as e:
        logger.error(f"Error selecting 'Newest' comments: {e}")

def load_reply_text(file_path):
    try:
        with open(file_path, 'r') as file:
            reply_text = file.read().strip()  # Reading all text and removing extra spaces
        logger.info(f"Loaded reply text from {file_path}.")
        return reply_text
    except Exception as e:
        logger.error(f"Error reading reply text from file: {e}")
        return "test"  # Default reply if the file fails to load

async def reply_to_comments(page, reply_text_file):
    reply_text = load_reply_text(reply_text_file)
    logger.info(f"Reply text loaded: {reply_text}")
    await page.evaluate("window.scrollBy(0, 100);")
    
    start_index = 2
    end_index = 100
    c = 0

    for i in range(start_index, end_index + 1):
        cmt1 = f"xpath=/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[2]/div[3]/div[{i}]"
        try:
            comment_element = await page.wait_for_selector(cmt1, timeout=10000)
            comment_text = await page.evaluate("(element) => element.textContent", comment_element)
            logger.info(f"Comment {i}: {comment_text}")

            if "View" in comment_text:
                logger.info(f"Comment {i} has replies. Skipping.")
                await page.evaluate("window.scrollBy(0, 150);")
                await page.wait_for_timeout(1000)
                continue

            await page.evaluate("window.scrollBy(0, 150);")
            await page.wait_for_timeout(1000)

            reply_button_xpath = f"xpath=/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[2]/div[3]/div[{i}]/div/div[1]/div/div[2]/div[2]/ul/li[3]/div/div"
            reply_button = await page.wait_for_selector(reply_button_xpath, timeout=10000)
            await reply_button.click()

            reply_input = await page.wait_for_selector("xpath=//div[@aria-label='Write a reply…']", timeout=10000)
            await reply_input.type(reply_text)
            await reply_input.press('Enter')
            c += 1
            logger.info(f"Replied to comment {i}. Current count: {c}")

            if c == 5:
                logger.info("Reached 5 replies. Stopping.")
                break

        except Exception as e:
            logger.error(f"Error while processing comment {i}: {e}")

async def process_profiles(profile_ids):
    for profile_id in profile_ids:
        browser = None
        try:
            logger.info(f"Processing profile: {profile_id}")
            browser = await uc.start()
            page = await browser.new_page()
            await login_with_cookies(page, r"C:\Users\User 2\fb_bot\post_links.txt")
            await select_new_comments(page)
            await page.evaluate("window.scrollBy(0, 300);")
            await reply_to_comments(page, r"C:\Users\User 2\fb_bot\comment.txt")
            logger.info(f"Finished processing profile: {profile_id}")
        except Exception as e:
            logger.error(f"Error processing profile {profile_id}: {e}")
        finally:
            if browser:
                await browser.stop()

# Example usage:
profile_ids = ['21f69182-7488-468f-b0ec-11dd856ace96']  # Replace with actual profile IDs
asyncio.run(process_profiles(profile_ids))
