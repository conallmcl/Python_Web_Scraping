head = {"Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en,en-US;q=0.9,nl;q=0.8",
"Connection": "keep-alive",
"Cookie": "TP.uuid=8649e58e-b7e1-4f3e-aefe-3d79f355b569; _hjSessionUser_391767=eyJpZCI6IjM4Mzc5Njc0LWMzZWYtNWNiNy05NTg3LWEyNzQ1MGVhNTMxMiIsImNyZWF0ZWQiOjE2NDY5MDkwNzEzNTEsImV4aXN0aW5nIjp0cnVlfQ==; __auc=7256391d18148ccc4aa7cdeaf4b; _ga=GA1.1.870527177.1663834062; _biz_uid=25cfa1081ab84f4c8bf0aaadfe4e5aa9; _biz_flagsA=%7B%22Version%22%3A1%2C%22ViewThrough%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; _tt_enable_cookie=1; _ttp=e3aae4bb-85b5-40ee-9c74-342ac974ca12; OptanonAlertBoxClosed=2022-10-04T10:38:23.104Z; _biz_nA=13; _biz_pendingA=%5B%5D; _ga_11HBWMC274=GS1.1.1664879902.3.1.1664881178.0.0.0; _ga_MD2Z7JEPWG=GS1.1.1664879902.3.1.1664881178.0.0.0; amplitude_id_67f7b7e6c8cb1b558b0c5bda2f747b07trustpilot.com=eyJkZXZpY2VJZCI6ImFjOTQyNmI0LTNhZjUtNDNhNi05OTExLTRjMTgzMDMwODM0OFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY2NDg3OTkwMTUwOSwibGFzdEV2ZW50VGltZSI6MTY2NDg4MTE3ODA5MywiZXZlbnRJZCI6MjI5LCJpZGVudGlmeUlkIjozNSwic2VxdWVuY2VOdW1iZXIiOjI2NH0=; ajs_anonymous_id=%221db00130-98a6-4adc-92ed-6e2c8a35107d%22; amplitude_id_cfe705a69359b8a4c0049d061ee5787btrustpilot.com=eyJkZXZpY2VJZCI6IjI1NWU4ZDRiLWJmNjAtNDVhYi1iYmY2LTEzMjFkYmUxYWE3ZFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY2NTE1ODk0MjcxNCwibGFzdEV2ZW50VGltZSI6MTY2NTE1OTQyNTgxMSwiZXZlbnRJZCI6MTksImlkZW50aWZ5SWQiOjE2LCJzZXF1ZW5jZU51bWJlciI6MzV9; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+21+2023+15%3A51%3A43+GMT%2B0100+(British+Summer+Time)&version=6.28.0&isIABGlobal=false&hosts=&consentId=8c63999d-361a-4792-b5d4-e4122969fa0f&interactionCount=3&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=GB%3BENG&AwaitingReconsent=false&genVendors=",
"Host": "uk.trustpilot.com",
"Referer": "https://uk.trustpilot.com/review/www.paypal.com",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
"sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows",
"x-nextjs-data": "1"}

import requests
import json
import math
from tqdm import tqdm
from time import sleep
import pandas as pd

all_reviews = []

url = "https://uk.trustpilot.com/_next/data/businessunitprofile-consumersite-7978/review/www.paypal.com.json"

response = requests.get(url, headers = head)

data = json.loads(response.content)

total_reviews = data["pageProps"]["businessUnit"]["numberOfReviews"]

total_pages = math.ceil(total_reviews / 20)

reviews = data["pageProps"]["reviews"]

for review in reviews:

    reviewid = review["id"]

    reviewtext = review["text"]

    reviewrating = review["rating"]

    all_reviews.append({
        "reviewid": reviewid,
        "reviewtext": reviewtext,
        "reviewrating": reviewrating
    })

for page in tqdm(range(2, total_pages+1)):

    url = f"https://uk.trustpilot.com/_next/data/businessunitprofile-consumersite-7978/review/www.paypal.com.json?page={page}"

    response = requests.get(url, headers = head)

    data = json.loads(response.content)

    reviews = data["pageProps"]["reviews"]

    for review in reviews:

        reviewid = review["id"]

        reviewtext = review["text"]

        reviewrating = review["rating"]

        all_reviews.append({
            "reviewid": reviewid,
            "reviewtext": reviewtext,
            "reviewrating": reviewrating
        })

    if page >= 5: break

    sleep (3)

# with open("reviews.text", "w", encoding = "utf-8") as f:
#     for review in all_reviews:
#         f.write(str (review))

df = pd.DataFrame(all_reviews)
df.to_excel("reviews.xlsx")