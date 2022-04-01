from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from operator import getitem

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
    # Scraping hockey (NHL)
    d.get("https://www.bet365.com/#/AC/B17/C20798172/D48/E972/F10/")
    time.sleep(3)
    element = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'gl-MarketGroupContainer')))
    teams = element.find_elements(by=By.XPATH,
                                  value='//div[@class="sci-ParticipantFixtureDetailsHigherIceHockey_Team "]')
    money_line = element.find_elements(by=By.XPATH, value='//span[@class="sac-ParticipantOddsOnly50OTB_Odds"]')
    bet365 = {}
    i = 0
    while i < len(teams):
        vig = {}
        vig["away"] = americanToDecimal(money_line[i].text)
        vig["home"] = americanToDecimal(money_line[i + 1].text)
        if vig["away"] and vig["home"]:
            vig["payout"] = 1 / ((1 / vig["away"]) + (1 / vig["home"]))
            game = teams[i].text.split(" ")[-1] + "-" + teams[i + 1].text.split(" ")[-1]
            bet365[game] = vig
        i += 2
    bet365 = dict(sorted(bet365.items(), key=lambda x: getitem(x[1], "payout"), reverse=True))
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
            vig = {}
            vig["away"] = float(text[-2])
            vig["home"] = float(text[-1])
            if vig["away"] and vig["home"]:
                vig["payout"] = 1 / ((1 / vig["away"]) + (1 / vig["home"]))
                teams = text[1].split(" @ ")
                game = teams[0].split(" ")[-1] + "-" + teams[1].split(" ")[-1]
            betway[game] = vig
        except:
            pass
    betway = dict(sorted(betway.items(), key=lambda x: getitem(x[1], "payout"), reverse=True))
    return betway

# chromedriver setup 
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

bet365Dict = scrapeBet365(driver)
betwayDict = scrapeBetway(driver)

for key in bet365Dict:
    if key in betwayDict:
        print(key)
        homeAway = 1 / ((1 / bet365Dict[key]["home"]) + (1 / betwayDict[key]["away"]))
        awayHome = 1 / ((1 / bet365Dict[key]["away"]) + (1 / betwayDict[key]["home"]))

        bet365 = 1 / ((1 / bet365Dict[key]["home"]) + (1 / bet365Dict[key]["away"]))
        betway = 1 / ((1 / betwayDict[key]["home"]) + (1 / betwayDict[key]["away"]))

        maxVig = max(homeAway, awayHome, bet365, betway)

        if maxVig == homeAway:
            print("Bet365 home, Betway away: " + str(homeAway))
        elif maxVig == awayHome:
            print("Betway away, Bet365 home: " + str(awayHome))
        elif maxVig == bet365:
            print("Bet365 away, Bet365 home: " + str(bet365))
        elif maxVig == betway:
            print("Betway away, Betway home: " + str(betway))
