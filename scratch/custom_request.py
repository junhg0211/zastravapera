import requests

url = "https://discord.com/api/v8/applications/879294810492665857/guilds/561880172542820353/commands"

# This is an example USER command, with a type of 2
json = {
    "name": "zasok",
    "type": 1,
    "description": "자소크어 단어를 검색합니다.",
    "options": [
        {
            "name": "query",
            "description": "검색할 단어",
            "type": 3,
            "required": True
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot Dc5Mjk0ODEwNDkyNjY1ODU3.YSNpGw.82s1JGoUDShGoPRWS8CZCzrpa7w"
}

r = requests.post(url, headers=headers, json=json)
