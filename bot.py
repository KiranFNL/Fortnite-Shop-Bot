import requests
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


# ==========================
# EINSTELLUNGEN
# ==========================

WEBHOOK_URL = "https://discord.com/api/webhooks/1541555671483285524/_yqUuRy-UyrJSmOTY6nJwXLkcthnxyDAjWOqs0sNNlaKeV_dRvHf6TUPueqCgGcdPXhs"

ROLE_ID = "1541572897095548948"

API_URL = "https://fortnite-api.com/v2/shop"

GERMAN_TIME = ZoneInfo("Europe/Berlin")

SHOP_IMAGE = "shop.png"
SHOP_IMAGE_16 = "shop_16_9.png"



# ==========================
# SHOP DATEN HOLEN
# ==========================

def get_shop():

    try:
        r = requests.get(API_URL, timeout=10)

        if r.status_code == 200:
            return r.json()["data"]["entries"]

    except Exception as e:
        print("API Fehler:", e)

    return []



# ==========================
# SHOP BILD ERSTELLEN
# ==========================

def create_shop_image():

    items = get_shop()

    if not items:
        print("Keine Items gefunden")
        return False


    width = 1920
    height = 1080

    img = Image.new(
        "RGB",
        (width, height),
        (20, 20, 20)
    )

    draw = ImageDraw.Draw(img)


    try:
        font_big = ImageFont.truetype(
            "arial.ttf",
            80
        )

        font = ImageFont.truetype(
            "arial.ttf",
            35
        )

    except:

        font_big = None
        font = None



    draw.text(
        (60,40),
        "Fortnite Item Shop",
        font=font_big
    )


    x = 50
    y = 180

    count = 0


    for item in items[:12]:

        name = item.get(
            "items",
            [{}]
        )[0].get(
            "name",
            "Unknown"
        )


        draw.rectangle(
            (
                x,
                y,
                x+400,
                y+180
            ),
            outline=(255,255,255),
            width=3
        )


        draw.text(
            (
                x+20,
                y+60
            ),
            name[:20],
            font=font
        )


        x += 450

        count += 1


        if count == 4:

            x = 50
            y += 230
            count = 0



    img.save(SHOP_IMAGE)

    print("[SHOP BILD] erstellt")

    return True



# ==========================
# DISCORD SENDEN
# ==========================

def send_shop():

    create_shop_image()


    now = datetime.now(
        GERMAN_TIME
    )


    embed = {

        "title":
        "🛒 Fortnite Item Shop",


        "description":
        f"📅 {now.strftime('%d.%m.%Y %H:%M')}",


        "color":
        5793266,


        "image":
        {
            "url":
            "attachment://shop_16_9.png"
        },


        "footer":
        {
            "text":
            "Made by @kiranfn"
        }

    }



    payload = {

        "content":
        f"<@&{ROLE_ID}> Fortnite Shop ist live!",


        "allowed_mentions":
        {
            "roles":
            [
                ROLE_ID
            ]
        },


        "embeds":
        [
            embed
        ]

    }



    with open(SHOP_IMAGE,"rb") as f:


        files = {

            "file":
            (
                "shop_16_9.png",
                f,
                "image/png"
            )

        }


        r = requests.post(

            WEBHOOK_URL,

            data={
                "payload_json":
                json.dumps(payload)
            },

            files=files

        )


    print(
        "[DISCORD]",
        r.status_code
    )



# ==========================
# START
# ==========================

print(
    "[BOT] gestartet"
)


last_post = None


while True:


    now = datetime.now(
        GERMAN_TIME
    )


    if now.dst():

        shop_time = 2

    else:

        shop_time = 1



    if (
        now.hour == shop_time
        and now.minute == 0
    ):


        if last_post != now.date():

            send_shop()

            last_post = now.date()



    time.sleep(60)
