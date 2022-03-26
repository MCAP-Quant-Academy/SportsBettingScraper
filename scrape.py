from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def americanToDecimal(a):
    if not a: return None
    sign = a[0]
    if sign == "+":
        return 1 + int(a[1:]) / 100 
    elif sign == "-":
        return 1 + 100 / int(a[1:])
    else:
        return None

def scrapeBet365(d):
    d.get("https://www.bet365.com/#/AC/B17/C20798172/D48/E972/F10/")
    time.sleep(1)
    element = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'gl-MarketGroupContainer')))
    teams = element.find_elements(by=By.XPATH, value='//div[@class="sci-ParticipantFixtureDetailsHigherIceHockey_Team "]')
    money_line = element.find_elements(by=By.XPATH, value='//span[@class="sac-ParticipantOddsOnly50OTB_Odds"]')
    bet365 = {}
    i = 0
    while i < len(teams):
        vig = {}
        vig["away"] = americanToDecimal(money_line[i].text)
        vig["home"] = americanToDecimal(money_line[i + 1].text)
        vig["payout"] = 1 / ((1 / vig["away"]) + (1 / vig["home"]))
        bet365[teams[i].text + " - " + teams[i + 1].text] = vig
        i += 2
    return bet365

def scrapeBetway(d):    
    d.get("https://betway.com/en/sports/grp/ice-hockey/north-america/nhl")
    time.sleep(1)
    element = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'eventItemCollection')))
    events = element.find_elements(by=By.XPATH, value='//div[@class="oneLineEventItem"]')
    betway = {}
    for i in range(len(events)):
        text = events[i].text.split("\n")
        if len(text) > 4:
            text = text[2:]
        try: 
            away = float(text[-2])
            home = float(text[-1])
            teams = text[1].split(" @ ")
            game = teams[0].split(" ")[-1] + "-" + teams[1].split(" ")[-1]
        except:
            pass
    return betway

# chromedriver setup 
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


print(scrapeBet365(driver))
# print(scrapeBetway(driver))





