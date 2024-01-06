import urllib
from playwright.sync_api import sync_playwright
# the maximum time a locator can wait before timinout
TIMEOUT_TIME = 5    # in ms


def get_info_handler(raw_query):
    query = urllib.parse.quote_plus(raw_query)

    with sync_playwright() as p:
        result = None
        browser = p.chromium.launch()
        device = p.devices['Desktop Edge']
        context = browser.new_context(
            locale='de-DE',
            color_scheme='dark',
            forced_colors='active',
            **device
        )
        page = context.new_page()
        page.goto(f'https://google.com/search?q={query}&lr=lang_en')
        page.locator('#W0wltc').click()
        page.wait_for_selector('#rcnt')
        page.screenshot(path='search_screenshot.png')

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
    selector = '#rso > div:nth-child(2) > div > block-component > div > div.dG2XIf.XzTjhb > div > div > div > div > div.ifM9O > div > div > div > div > div.wDYxhc > div > span > span'
    # selector = 'div.wDYxhc > div > span > span'
    info_locator = page.locator(selector)
    try:
        return info_locator.inner_text(timeout=TIMEOUT_TIME)
    except Exception:
        return None


def get_side_info(page):
    selector = '.xGj8Mb > .wDYxhc .kno-rdesc span'

    info_locators = page.locator(selector).all()
    try:
        return info_locators[0].inner_text(timeout=TIMEOUT_TIME)
    except Exception:
        return None


# print(get_info_handler('Tell me about quantum physics.'))
# print(get_info_handler('who is steve jobs?'))
