import requests
import time
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

def anime_scrape():
    anime_num = input("Input the number of anime descriptions you want to scrape: ")
    ranking_by = input("Choose how the anime should be ranked (1.Ranked by User Score 2.Ranked by Popularity 3.Rank by Most Favorited):")
    if ranking_by == 1:
        url = "https://myanimelist.net/topanime.php"
    elif ranking_by == 2:
        url = "https://myanimelist.net/topanime.php?type=bypopularity"
    elif ranking_by == 3:
        url = "https://myanimelist.net/topanime.php?type=favorite"
    anime_count = 0

    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    driver.set_window_size(1120, 1000)

    driver.get(url)

    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    anime_list, anime_summary = [], {}
    while anime_count < anime_num:
        time.sleep(3)
        scroll_down(driver)
        body = driver.find_elements_by_xpath("//*[@id='content']/div[4]/table/tbody/tr[position()>=2 and position()<=51]/td[2]/a")
        for i in body:
            anime_list.append(i.get_attribute("href"))
            anime_count += 1
            if anime_count >= anime_num:
                break

        try:
            driver.find_element_by_link_text('Next 50').click()
            time.sleep(2)
        except NoSuchElementException:
            print(f"[ERROR] Scraping terminated before reaching desired number of anime. Needed {anime_num}, got {anime_count}.")
            break

    anime_count = 0
    for link in anime_list:
        time.sleep(2)
        driver.get(link)

        title = driver.find_element_by_xpath("/html/head/meta[8]").get_attribute("content")
        if title in anime_summary:
            continue

        print(f"[INFO] Scraping {title} for summary :: Got {anime_count}/{anime_num}")
        body = driver.find_element_by_xpath("/html/head/meta[13]").get_attribute("content")
        anime_summary[title] = body
        anime_count += 1
    return anime_summary

def get_summary(anime_summary, LSTM_or_GPT2):
    summary_list = list(anime_summary.values())

    for i in range(len(summary_list)):
        text = summary_list[i]
        if "(Source" in text:
            text, __, __ = text.partition("(Source")
        if "[Written " in text:
            text, __, __ = text.partition("[Written")
        text = re.sub("([^\x00-\x7F])+"," ",text)
        text = re.sub(r"[^\w\d\s\-]+", "", text)
        summary_list[i] = text

    summary_list = [x.lower() for x in summary_list]
    if LSTM_or_GPT2 == 0:
        summary_text = " ".join(summary_list)
        summary_file = open("summary.txt","w")
        summary_file.write(summary_text)
        summary_file.close()
        return
    else:
        for summ in summary_list:
            if len(summ) > 300 or len(summ) <= 30:
                print(summ) ##CHECK IF THIS WORKS
                summary_list.remove(summ)

        summary_list = [i + "<|endoftext|>" for i in summary_list] ## REFACTOR THIS PLS
        return
