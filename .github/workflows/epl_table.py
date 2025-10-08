import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

API_KEY = "API_KEY"  # GitHub Secrets로 대체 예정
URL = "https://api.football-data.org/v4/competitions/PL/standings"

headers = {"X-Auth-Token": API_KEY}
response = requests.get(URL, headers=headers)
data = response.json()

table = data["standings"][0]["table"]

width, height = 420, 650
img = Image.new("RGB", (width, height), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()

draw.text((20, 10), "Premier League Standings", fill=(255, 255, 255), font=font)

y = 50
for row in table[:10]:
    text = f"{row['position']:>2}. {row['team']['name'][:18]:<18} {row['points']:>3} pts"
    draw.text((20, y), text, fill=(255, 255, 255), font=font)
    y += 25

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
draw.text((20, height - 30), f"Updated: {timestamp}", fill=(180, 180, 180), font=font)

img.save("epl_table.png")
