import time
import csv
import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
ITEM="Adjustable-dumbbell-upgraded-Kettlebells-Exercise"
URL=f"https://www.amazon.com/{ITEM}/dp/B0DB1FDJ9C/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.3fdbc1ee-e2a3-48ef-a93a-bce40e980706&dib=eyJ2IjoiMSJ9.fEGVKcaXmraOtZYMfsQWHw8AVxneK6NyXagVMbB3exsi537M900-QPsC0xDl4VXx9A8nL-Y-DKsH-vVhVfLVlIl8mCcHJy3OCvXg4XPa2TZBjDkGrl_nJZ3IWZyz6voO54nkt4wbRsLQV3FNODMdBYJZSOZxozsfS4M4zMyHv22NK5YVSC8XonDJ-01oKDd5ARq8lOcTFNjBhm8EW0uki6nc1yY4aKJNcmurVxZwCp8imQN8_SwgDXGVFF3-glufALF43Cso862rbhKpCpART6CTqZe3BRZfgn9WyjVlRjI.UakLDVDBJ3FBwB86WdbWXvnT96wcCCTMdb9fekACt1E&dib_tag=se&keywords=fitness%2Bequipment&pd_rd_r=f2299a4b-9179-459f-b8d7-8f34ae5c2841&pd_rd_w=pDiAh&pd_rd_wg=gPSTW&qid=1780827483&sr=8-1&th=1"
load_dotenv()
MY_EMAIL=os.getenv("MY_EMAIL")
PASSWORD=os.getenv("PASSWORD")
DESIRED_PRICE=20000
header = header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
for i in range(3):
    response = requests.get(URL, headers=header)
    if "captcha" not in response.text.lower():
        break
    time.sleep(5)
print("Status Code:", response.status_code)
print("Final URL:", response.url)
print(response.text[:1000])
soup=BeautifulSoup(response.text,"html.parser")
price_tag = soup.find(class_="a-offscreen")

if price_tag is None:
    print("Price element not found.")
    print(response.url)
    exit(1)

price = price_tag.get_text()
without_currency=(price.split("PKR")[1]).replace(",","")
floated_value=float(without_currency)
with open("data.csv","a",newline="") as csvfile:
    csvfilewriter=csv.writer(csvfile)
    csvfilewriter.writerow([datetime.now().strftime("%Y-%m-%d"),ITEM,floated_value])
if floated_value<=DESIRED_PRICE:
    with smtplib.SMTP("smtp.gmail.com",587,timeout=30) as connection:
        connection.starttls()
        connection.login(MY_EMAIL,PASSWORD)

        connection.sendmail(from_addr=MY_EMAIL, to_addrs="2024n03358@gmail.com",
        msg=f"Subject:PRICE TRACKER\n\nThe {ITEM} have gone down to desired price of PKR {DESIRED_PRICE}\n Buy them at the link: {URL}")

        connection.close()
