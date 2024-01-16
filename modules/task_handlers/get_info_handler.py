import urllib
import os
from playwright.sync_api import sync_playwright
from config import ROOT_DIR

# the maximum time a locator can wait before timinout
TIMEOUT_TIME = 5    # in ms
SCREENSHOT_PATH = os.path.join(
    ROOT_DIR, 'modules/task_handlers/temp/search_screenshot.png')


def get_info_handler(raw_query):
    query = urllib.parse.quote_plus(raw_query)

    with sync_playwright() as p:
        result = None
        browser = p.chromium.launch()
        device = p.devices['Desktop Edge']
        context = browser.new_context(
            locale='bg-BG',
            color_scheme='dark',
            timezone_id='Europe/Sofia',
            forced_colors='active',
            **device
        )
        page = context.new_page()
        page.goto(f'https://google.com/search?q={query}&lr=lang_en')
        page.locator('#W0wltc').click()
        page.wait_for_selector('#rcnt')
        page.screenshot(path=SCREENSHOT_PATH)

        result = get_heading_text(page)
        if result is not None:
            browser.close()
            return result

        result = get_side_info(page)
        if result is not None:
            browser.close()
            return result

        browser.close()
        return result


def get_heading_text(page):
    selector = 'div.wDYxhc > div > span'
    info_locator = page.locator(selector).all()
    try:
        return info_locator[0].inner_text(timeout=TIMEOUT_TIME)
    except Exception:
        pass

    return None


def get_side_info(page):
    container = page.get_by_role('complementary')
    info_locator = container.locator('span').nth(0)

    try:
        return info_locator.inner_text(
            timeout=TIMEOUT_TIME)
    except Exception:
        return None


# print(get_info_handler('can you tell me something about bill gates'))
