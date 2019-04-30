# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
from urllib import parse
import requests
import sys

# 環境変数からトークンなどの情報を取得
notify_access_token = os.getenv('NOTIFY_ACCESS_TOKEN', None)
docomo_id = os.getenv('DOCOMO_ID', None)
docomo_pw = os.getenv('DOCOMO_PW', None)
if notify_access_token is None:
    print('Specify NOTIFY_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if docomo_id is None:
    print('Specify DOCOMO_ID as environment variable.')
    sys.exit(1)
if docomo_pw is None:
    print('Specify DOCOMO_PW as environment variable.')
    sys.exit(1)

# 通信量の取得
def getLog():

    # Selenium用オプション
    op = Options()
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=op)
    driver.get('https://www.nttdocomo.co.jp/auth/cgi/mltdomanidlogin?rl=https%3A%2F%2Fwww.nttdocomo.co.jp%2Fmydocomo%2F')

    # ID入力
    id = driver.find_element_by_id("Di_Uid")
    id.send_keys(docomo_id)

    # 「次へ」クリック
    login_button = driver.find_element_by_name("subForm")
    login_button.click()

    # PW入力
    password = driver.find_element_by_id("Di_Pass")
    password.send_keys(docomo_pw)

    # 「ログイン」クリック
    login_button = driver.find_element_by_name("subForm")
    login_button.click()

    # 通信量のページへ遷移
    driver.get("https://www.nttdocomo.co.jp/mydocomo/data/")
    dataSpan = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#mydcm_data_data-08 > div > dl > dd > p.mydcm_data_data-09-1 > span.card-t-ssnumber.t-bold.mydcm_data_data-10-1"))
    )
    return dataSpan.text

def main():
    mount = getLog()

    url = "https://notify-api.line.me/api/notify"
    token = notify_access_token #ここにアクセストークンを入力します。
    headers = {"Authorization" : "Bearer "+ token}

    message =  '今月の通信量は ' + mount + ' GBです。'
    payload = {"message" :  message}
    #files = {"imageFile": open("test.jpg", "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。

    r = requests.post(url ,headers = headers ,params=payload)

if __name__ == '__main__':
    main()