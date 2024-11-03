from selenium import webdriver
from selenium.webdriver.common.by import By
import time

timeout = time.time() + 5  # 5 secs
five_min = time.time() + 60 * 5

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")


cookie = driver.find_element(By.ID, value="cookie")
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]


powerups = driver.find_elements(By.CSS_SELECTOR, "#store b")
storePrices = []
for power in powerups:
    element_text = power.text
    if element_text != "":
        cost = int(element_text.split("-")[1].strip().replace(",", ""))
        storePrices.append(cost)


cookie_upgrades = {}

for n in range(len(storePrices)):
    cookie_upgrades[storePrices[n]] = item_ids[n]

while True:
    cookie.click()

    if time.time() > timeout:

        money_element = driver.find_element(by=By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        affordable_upgrades = {}

        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        max_affordable = max(affordable_upgrades)

        to_click = affordable_upgrades[max_affordable]
        driver.find_element(By.ID, to_click).click()
        timeout = time.time() + 5
    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_s)
        break
