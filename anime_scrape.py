import requests
import time
import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# Function takes two inputs from sys.arg to scrape raw data from MAL:
# 1. Number of anime descriptions to scrape
# 2. How the anime should be ranked (1. By User Score, 2. By Popularity, 3. By Most Favorited)
def anime_scrape():
    anime_num = int(sys.argv[1])
    ranking_by = int(sys.argv[2])

    choice = {1:"", 2:"?type=bypopularity", 3:"?type=favorite"}

    url = "https://myanimelist.net/topanime.php" + choice[ranking_by]
    anime_count = 0

    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    #options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(service = service, options = options)
    driver.set_window_size(1120, 1000)

    driver.get(url)

    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    anime_list, anime_summary = [], {}
    while anime_count < int(anime_num):
        time.sleep(3)
        scroll_down(driver)
        body = driver.find_elements("xpath", "//*[@id='content']/div[4]/table/tbody/tr[position()>=2 and position()<=51]/td[2]/a")
        for i in body:
            anime_list.append(i.get_attribute("href"))
            anime_count += 1
            if anime_count >= anime_num:
                break

        try:
            driver.find_element("link text", "Next 50").click()
            time.sleep(2)
        except NoSuchElementException:
            print(f"[ERROR] Scraping terminated before reaching desired number of anime. Needed {anime_num}, got {anime_count}.")
            break

    anime_count = 1
    for link in anime_list:
        time.sleep(2)
        driver.get(link)

        title = driver.find_element("xpath", "/html/head/meta[9]").get_attribute("content")
        if title in anime_summary:
            continue

        print(f"[INFO] Scraping {title} for summary :: Got {anime_count}/{anime_num}")
        body = driver.find_element("xpath", "/html/head/meta[14]").get_attribute("content")
        anime_summary[title] = body
        anime_count += 1

    return anime_summary

# Extracts summary from raw text 
def get_summary(anime_summary, lower=0):
    summary_list = list(anime_summary.values())

    for i in range(len(summary_list)):
        text = summary_list[i]
        if "(Source" in text:
            text, __, __ = text.partition("(Source")
        if "[Written " in text:
            text, __, __ = text.partition("[Written")
        text = re.sub("([^\x00-\x7F])+"," ",text)
        #text = re.sub(r"[^\w\d\s\-]+", "", text) # remove all punctuations
        summary_list[i] = text

    def push_to_txt(summary_list):
        summary_text = " ".join(summary_list)
        summary_file = open("summary.txt","w")
        summary_file.write(summary_text)
        summary_file.close()

    for i in range(len(summary_list)):
        if len(summary_list[i]) <= 30:
            summary_list.pop(i)
        if lower:
            summary_list[i] = summary_list[i].lower()
        # summary_list[i] = summary_list[i] + "<|endoftext|>" #lower caps all text + add endoftext
    push_to_txt(summary_list)
    return

get_summary(anime_scrape(), 1)
