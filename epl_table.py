from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests, io, os
from datetime import datetime

API_KEY = os.getenv("API_KEY")
URL = "https://api.football-data.org/v4/competitions/PL/standings"
headers = {"X-Auth-Token": API_KEY}
data = requests.get(URL, headers=headers).json()
table = data["standings"][0]["table"]

# 배경 만들기
width, height = 500, 800
img = Image.new("RGB", (width, height), color=(15, 15, 15))
draw = ImageDraw.Draw(img)

title_font = ImageFont.truetype("arial.ttf", 28)
team_font = ImageFont.truetype("arial.ttf", 18)
small_font = ImageFont.truetype("arial.ttf", 14)

draw.text((20, 20), "🏆 Premier League Standings", fill=(255, 255, 255), font=title_font)
y = 70

for row in table[:10]:
    team = row["team"]["name"]
    pts = row["points"]
    crest = row["team"]["crest"]
    
    # 로고 불러오기
    logo = Image.open(io.BytesIO(requests.get(crest).content))
    logo = logo.convert("RGBA")
    logo = ImageOps.contain(logo, (32, 32))
    img.paste(logo, (20, y), logo)
    
    draw.text((60, y+5), f"{row['position']}. {team[:18]}", fill=(230,230,230), font=team_font)
    draw.text((400, y+5), f"{pts} pts", fill=(180,180,180), font=team_font)
    y += 45

# 업데이트 시간
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
draw.text((20, height - 40), f"Updated: {timestamp}", fill=(150,150,150), font=small_font)

img.save("epl_table.png")
