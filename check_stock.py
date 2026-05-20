import os
import json
import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

PRODUCTS = {
    "Caderneta": "https://www.paniniportugal.com/shp_prt_pt/fifa-world-cup-2026-official-sticker-collection-caderneta-cole-o-oficial-panini-005460aptw-es01.html",

    "Caixa 50 Saquetas": "https://www.paniniportugal.com/shp_prt_pt/fifa-world-cup-2026-official-sticker-collection-caixa-de-50-saquetas-cole-o-oficial-panini-005460box50ew-es01.html",

    "Big Collector Box": "https://www.paniniportugal.com/shp_prt_pt/fifa-world-cup-2026-big-collector-s-box-cole-o-oficial-de-cromos-005460box144oe-es01.html",

    "Tin Box": "https://www.paniniportugal.com/shp_prt_pt/fifa-world-cup-2026-official-sticker-collection-tin-box-cole-o-oficial-panini-005460tinew-es01.html"
}

STATE_FILE = "stock_state.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def load_previous_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_stock_status(url):

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)

        html = r.text.lower()

        unavailable_words = [
            "sem stock",
            "esgotado",
            "indisponível",
            "out of stock"
        ]

        available_words = [
            "adicionar ao carrinho",
            "comprar",
            "em stock"
        ]

        if any(word in html for word in unavailable_words):
            return "❌ ESGOTADO"

        if any(word in html for word in available_words):
            return "✅ DISPONÍVEL"

        return "❓ DESCONHECIDO"

    except Exception as e:
        return f"⚠️ ERRO"

def send_discord(message):

    requests.post(
        DISCORD_WEBHOOK,
        json={
            "content": message
        }
    )

previous_state = load_previous_state()

current_state = {}

message = "📦 **STOCK PANINI FIFA 2026**\n\n"

mention = False

for product_name, url in PRODUCTS.items():

    status = get_stock_status(url)

    current_state[product_name] = status

    message += f"**{product_name}**\n"
    message += f"{status}\n"
    message += f"{url}\n\n"

    old_status = previous_state.get(product_name)

    if old_status == "❌ ESGOTADO" and status == "✅ DISPONÍVEL":
        mention = True

if mention:
    message = "@everyone\n\n" + message

send_discord(message)

save_state(current_state)

print("Bot executado com sucesso")
