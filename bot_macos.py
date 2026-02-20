from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from fake_useragent import UserAgent
import re
import random
import shutil
import subprocess


def str_to_bool(value, default=True):
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def interceptor(request):
    del request.headers["user-agent"]
    del request.headers["sec-ch-ua"]
    del request.headers["sec-ch-ua-platform"]
    request.headers["user-agent"] = uagent
    request.headers["sec-ch-ua"] = sec
    request.headers["sec-ch-ua-platform"] = platform_name
    request.headers["sec-fetch-mode"] = "navigate"
    request.headers["sec-fetch-user"] = "?1"
    request.headers["sec-ch-ua-mobile"] = "?0"
    request.headers["accept-Language"] = language
    request.headers["accept-Encoding"] = encoding
    request.headers["accept"] = accept
    request.headers["upgrade-insecure-requests"] = "1"


def get_browser(agent):
    if "Chrome/" in agent and "Edg/" not in agent:
        browser = "Chrome"
    elif "Safari/" in agent and "Chrome/" not in agent:
        browser = "Safari"
    elif "Firefox/" in agent:
        browser = "Firefox"
    elif "Edg/" in agent:
        browser = "Edge"
    else:
        browser = "Chrome"
    return browser


def get_sec(browser, user):
    if browser == "Chrome":
        ver = get_ver(user)
        sec = f'"Google Chrome";v={ver}, "Not;A=Brand";v="8", "Chromium";v={ver}'
    elif browser == "Edge":
        ver = get_ver(user)
        sec = f'"Microsoft Edge";v={ver}, "Not;A=Brand";v="8", "Chromium";v={ver}'
    else:
        sec = '"Not;A=Brand";v="8", "Chromium";v="120"'
    return sec


def get_ver(user):
    pattern = r"(?:Chrome|Edg)/(\d+\.\d+\.\d+\.\d+)"
    match = re.search(pattern, user)
    if match:
        v = match.group(1)
        return v.split(".")[0]
    return "120"


def get_platform(agent):
    if "Windows" in agent:
        return "Windows"
    if "Mac" in agent:
        return "macOS"
    if "Linux" in agent:
        return "Linux"
    return "macOS"


def find_windscribe_cli():
    for candidate in [
        shutil.which("windscribe"),
        shutil.which("windscribe-cli"),
        "/Applications/Windscribe.app/Contents/MacOS/WindscribeCLI",
        "/usr/local/bin/windscribe",
        "/opt/homebrew/bin/windscribe",
    ]:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def vpn(action, location=None):
    windscribe_cli = find_windscribe_cli()
    if not windscribe_cli:
        print("Windscribe CLI not found, skip VPN action.")
        return

    command = [windscribe_cli, action]
    if location:
        command.append(location)

    subprocess.run(command, check=False)


def b_1():
    return driver.find_element(By.XPATH, '//*[@id="app"]/div[4]/div[2]/div[2]/div[2]/button')


def b_2():
    return driver.find_element(By.XPATH, '//*[@id="app"]/div[4]/div[2]/div[2]/div[2]/button[2]')


def get_dates():
    b1 = b_1()
    while True:
        t_group = driver.find_element(By.XPATH, '//*[@class="tls-time-group"]')
        dates = t_group.find_elements(By.XPATH, './/*[@class="tls-time-group--slot"]')
        for date in dates:
            dt = date.find_element(By.XPATH, './/*[@class="tls-time-group--header-title"]').text
            try:
                date.find_element(By.XPATH, ".//*[@class='tls-time-unit  -available']")
                available_dates.append(dt)
            except Exception:
                try:
                    date.find_element(By.XPATH, ".//*[@class='tls-time-unit  -available -prime']")
                    available_dates.append(dt)
                except Exception:
                    continue
            time.sleep(2)
        try:
            b_2().click()
        except Exception:
            try:
                b1.click()
                b1 = False
            except Exception:
                break


while True:
    connect_list = [
        "Atlanta Mountain",
        "Dallas Ranch",
        "Chicago Cub",
        "Miami Snow",
        "Miami Vice",
        "New York Empire",
        "New York Grand Central",
        "Washington DC Precedent",
        "Los Angeles Dogg",
        "seattle Cobain",
        "Montreal Expo 67",
        "Toronto Comfort Zone",
        " Toronto The 6",
        "Vancouver Granville",
        "Vancouver Vansterdam",
        "Paris Seine",
        "Paris Jardin",
        "Amsterdam Canal",
        "Amsterdam Red Light",
        "Amsterdam Tulip",
        "Oslo Fjord",
        "Zurich Alphorn",
        "Zurich Lindenhof",
        "London Crumpets",
        "London Custard",
        "Istanbul Lygos",
        "Hong Kong Phooey",
        "Hong Kong Victoria",
    ]
    use_vpn = str_to_bool(os.getenv("USE_VPN"), default=False)
    vpn_connected = False
    if use_vpn:
        location = random.choice(connect_list)
        vpn("connect", location)
        vpn_connected = True
    else:
        print("USE_VPN is disabled. Running without Windscribe.")

    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    encoding = "gzip, deflate, br"
    language = "en-GB,en-US;q=0.9,en;q=0.8"

    uagent = UserAgent().random

    username = os.getenv("TLS_USERNAME")
    password = os.getenv("TLS_PASSWORD")
    if not username or not password:
        raise RuntimeError("Please set TLS_USERNAME and TLS_PASSWORD environment variables before running bot_macos.py")

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=chrome_options, use_subprocess=True)

    browser = get_browser(uagent)
    sec = get_sec(browser, uagent)
    platform_name = get_platform(uagent)

    driver.request_interceptor = interceptor
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.maximize_window()
    wait = WebDriverWait(driver, 200)

    try:
        driver.get("https://visas-fr.tlscontact.com/visa/gb/gbLON2fr/home")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Login"]')))
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[text()="Login"]').click()
        element = driver.find_element(By.XPATH, '//input[@name="username"]')
        time.sleep(3)
        element.send_keys(username)
        element = driver.find_element(By.XPATH, "//input[@name='password']")
        element.send_keys(password)
        element.send_keys(Keys.RETURN)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()="My Application"]'))).click()
        time.sleep(5)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="tls-button-primary button-neo-inside"]'))).click()

        js_code = "arguments[0].scrollIntoView();"
        scroll = driver.find_element(By.XPATH, '//*[@class="button-neo-inside -primary"]')
        driver.execute_script(js_code, scroll)
        js_scroll = "window.scrollBy(0, 1200);"
        driver.execute_script(js_scroll)
        time.sleep(2)

        available_dates = []
        get_dates()

        if len(available_dates) == 0:
            print("No dates available!!!")
        else:
            print(available_dates)
    except Exception as err:
        print(f"Run failed: {err}")
    finally:
        driver.quit()
        if vpn_connected:
            vpn("disconnect")

    time.sleep(300)