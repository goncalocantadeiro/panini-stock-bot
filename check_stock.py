import os
import requests

DISCORD_WEBHOOK = os.environ["https://discord.com/api/webhooks/1506582743645945967/9gcnGgBhTS9ceGDe5mquMp6l6vwrAhhUl2zILNuOI9r6K6DBf_OUua2rNEsZ8W4SZ8sY"]

URLS = [
    "https://www.paniniportugal.com/shp_prt_pt/cromos-e-cards/desporto/fifa.html"
]

def send_discord(message):
    requests.post(DISCORD_WEBHOOK, json={
        "content": message
    })

for url in URLS:

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    html = r.text.lower()

    if "adicionar ao carrinho" in html or "em stock" in html:

        send_discord(
            f"🚨 @everyone STOCK PANINI DETETADO!\n{url}"
        )
