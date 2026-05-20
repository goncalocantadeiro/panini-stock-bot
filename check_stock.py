import os
import requests

DISCORD_WEBHOOK = os.environ["https://discord.com/api/webhooks/1506584948604407919/JZGgvHUQXbPYA4tZnDdxYpgQFDKuMeQYFr6NRbL-6D3fMg6J22s0PexBlYni3jhLFU_n"]

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
