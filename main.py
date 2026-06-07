import time
import csv
import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
ITEM="Adjustable-dumbbell-upgraded-Kettlebells-Exercise"
URL = f"https://www.amazon.com/{ITEM}/dp/B0DB1FDJ9C"
load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")

DESIRED_PRICE = 20000

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_page(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=20)

        if "captcha" in response.text.lower():
            print("Blocked by Amazon")
            return None

        return response.text

    except Exception as e:
        print("Request failed:", e)
        return None


html = None

for i in range(3):
    html = fetch_page(URL, headers)
    if html:
        break
    time.sleep(2)

if not html:
    print("Failed to fetch page")
    exit()

soup = BeautifulSoup(html, "html.parser")

def get_price(soup):
    price_tag = soup.select_one(".a-price .a-offscreen")
    if not price_tag:
        return None
    return price_tag.get_text()

price = get_price(soup)

if not price:
    print("Price not found")
    exit()

# clean price (Amazon format: $199.99)
floated_value = float(price.replace("$", "").replace(",", ""))

with open("data.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        datetime.now().strftime("%Y-%m-%d"),
        ITEM,
        floated_value
    ])

if floated_value<=DESIRED_PRICE:
    with smtplib.SMTP("smtp.gmail.com",587,timeout=30) as connection:
        connection.starttls()
        connection.login(MY_EMAIL,PASSWORD)
    
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="2024n03358@gmail.com",
        msg=f"Subject:PRICE TRACKER\n\nThe {ITEM} have gone down to desired price of PKR {DESIRED_PRICE}\n Buy them at the link: {URL}")

        connection.close()
