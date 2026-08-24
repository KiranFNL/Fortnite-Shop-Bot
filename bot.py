import requests
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw

# ==========================
# EINSTELLUNGEN
# ==========================

WEBHOOK_URL = "https://discord.com/api/webhooks/1541555671483285524/_yqUuRy-UyrJSmOTY6nJwXLkcthnxyDAjWOqs0sNNlaKeV_dRvHf6TUPueqCgGcdPXhs"
ROLE_ID = "1541572897095548948"

GERMAN_TIME = ZoneInfo("Europe/Berlin")

IMAGE_NAME = "shop_16_9.png"


# ==========================
# SHOP BILD ERSTELLEN
# ==========================

def create_shop_image():

    try:
        img = Image.new(
            "RGB",
            (1280, 720),
            (25, 25, 35)
        )

        draw = ImageDraw.Draw(img)

        text = (
            "FORTNITE ITEM SHOP\n\n"
            "Shop ist live!"
        )

        draw.text(
            (100, 250),
            text,
            fill=(255, 255, 255)
        )

        img.save(IMAGE_NAME)

        print("[BILD] Shop Bild erstellt")

    except Exception as e:
        print("Bild Fehler:", e)



# ==========================
# DISCORD SENDEN
# ==========================

def send_shop(test=False):

    create_shop_image()

    now = datetime.now(GERMAN_TIME)

    if test:
        title = "🛒 Fortnite Item Shop TEST"
    else:
        title = "🛒 Fortnite Item Shop"


    embed = {
        "title": title,

        "description": " Fortnite Item Shop ist live!",

        "color": 5793266,

        "image": {
            "url": "attachment://shop_16_9.png"
        },

      "footer": {
    "text": f"made by @kiranfn • heute um {now.strftime('%H:%M Uhr')}"
}

}

    payload = {

        "content": f"<@&{ROLE_ID}> **Fortnite Item Shop ist live!**",

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

        with open(IMAGE_NAME, "rb") as file:

            files = {
                "file": (
                    IMAGE_NAME,
                    file,
                    "image/png"
                )
            }


            response = requests.post(
                WEBHOOK_URL,

                data={
                    "payload_json": json.dumps(payload)
                },

                files=files
            )


        if response.status_code == 204:
            print("[DISCORD] Gesendet")

        else:
            print("Discord Fehler:", response.text)


    except Exception as e:
        print("Webhook Fehler:", e)



# ==========================
# START
# ==========================

print("[BOT] Fortnite Shop Bot gestartet")


# Test Nachricht beim Start
send_shop(test=True)



# ==========================
# AUTO POST 2 UHR
# ==========================

last_post = None


while True:

    now = datetime.now(GERMAN_TIME)


    if now.hour == 2 and now.minute == 0:

        if last_post != now.date():

            print("[SHOP] Automatischer Post")

            send_shop()

            last_post = now.date()


    time.sleep(30)
