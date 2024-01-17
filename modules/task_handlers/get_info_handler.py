import urllib
import os
import re
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
        if result is not None and not '':
            browser.close()
            return result

        result = get_side_info(page)
        if result is not None and not '':
            browser.close()
            return result

        browser.close()
        return result


def get_heading_text(page):
    try:
        info_container = page.get_by_role('heading').all()
        info_container = list(filter(
            lambda el: el.get_attribute('aria-level') == '2',
            info_container
        ))[1]

        result = info_container.inner_text(timeout=TIMEOUT_TIME)

        if re.search('[a-zA-Z]', result) is None:
            return None

        return result
    except Exception:
        pass

    return None


def get_side_info(page):
    try:
        container = page.locator('[aria-label=\'Информация\']')

        span = container.locator('span').nth(0)
        return span.inner_text(timeout=TIMEOUT_TIME)
    except Exception:
        pass

    return None
