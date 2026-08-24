import requests
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image


# ==========================
# EINSTELLUNGEN
# ==========================

WEBHOOK_URL = "https://discord.com/api/webhooks/1541555671483285524/_yqUuRy-UyrJSmOTY6nJwXLkcthnxyDAjWOqs0sNNlaKeV_dRvHf6TUPueqCgGcdPXhs"

ROLE_ID = "1541572897095548948"

API_URL = "https://fortnite-api.com/v2/shop"

ORIGINAL_IMAGE = "shop.png"

CROP_IMAGE = "shop_16_9.png"

GERMAN_TIME = ZoneInfo("Europe/Berlin")



# ==========================
# BILD AUF 16:9 SCHNEIDEN
# ==========================

def make_16_9():

    try:

        img = Image.open(ORIGINAL_IMAGE)

        width, height = img.size


        target_ratio = 16 / 9

        current_ratio = width / height


        if current_ratio > target_ratio:

            # zu breit -> Seiten abschneiden

            new_width = int(height * target_ratio)

            left = (width - new_width) // 2

            img = img.crop(
                (
                    left,
                    0,
                    left + new_width,
                    height
                )
            )


        elif current_ratio < target_ratio:

            # zu hoch -> oben/unten abschneiden

            new_height = int(width / target_ratio)

            top = (height - new_height) // 2

            img = img.crop(
                (
                    0,
                    top,
                    width,
                    top + new_height
                )
            )


        img.save(
            CROP_IMAGE,
            "PNG"
        )


        print("[BILD] 16:9 erstellt")


    except Exception as e:

        print("Bild Fehler:", e)



# ==========================
# FORTNITE API
# ==========================

def get_shop():

    try:

        r = requests.get(
            API_URL,
            timeout=10
        )

        if r.status_code == 200:

            data = r.json()

            return data["data"]["date"]


    except Exception as e:

        print("API Fehler:", e)


    return None



# ==========================
# DISCORD SENDEN
# ==========================

def send_shop(test=False):


    make_16_9()


    now = datetime.now(GERMAN_TIME)


    title = (
        "🛒 Fortnite Item Shop (TEST)"
        if test
        else
        "🛒 Fortnite Item Shop"
    )



    embed = {

        "title": title,

        "description":
        f"📅 Shop Update: {now.strftime('%d.%m.%Y %H:%M:%S')}",


        "color": 5793266,


        "image": {

            "url":
            "attachment://shop_16_9.png"

        },


        "footer": {

            "text":
            "Made by @kiranfn"

        },


        "timestamp":
        now.isoformat()

    }



    payload = {


        "content":
        f"<@&{ROLE_ID}> **Fortnite Item Shop ist live!**",


        "allowed_mentions": {

            "roles": [
                ROLE_ID
            ]

        },


        "embeds": [

            embed

        ]

    }



    try:


        with open(CROP_IMAGE, "rb") as img:


            files = {

                "file":

                (

                    "shop_16_9.png",

                    img,

                    "image/png"

                )

            }



            response = requests.post(

                WEBHOOK_URL,

                data={

                    "payload_json":
                    json.dumps(payload)

                },

                files=files

            )



        if response.status_code == 204:

            print("[WEBHOOK] Gesendet")


        else:

            print(response.text)



    except Exception as e:

        print("Webhook Fehler:", e)



# ==========================
# START
# ==========================

print("[BOT] Fortnite Shop Bot gestartet")


send_shop(test=True)


last_shop = get_shop()

last_post = None



# ==========================
# AUTO SYSTEM
# ==========================

while True:


    now = datetime.now(GERMAN_TIME)


    if now.dst():

        shop_hour = 2

    else:

        shop_hour = 1



    if now.hour == shop_hour and now.minute == 0:


        if last_post != now.date():


            current_shop = get_shop()


            if current_shop != last_shop:


                print("[SHOP] Neuer Shop")


                send_shop()


                last_shop = current_shop



            last_post = now.date()



    time.sleep(60)