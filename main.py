import discord
import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mixtral-8x7b",
            "messages":[{"role":"user","content":message.content}]
        }
    )

    reply = response.json()["choices"][0]["message"]["content"]

    await message.channel.send(reply)

bot.run(DISCORD_TOKEN)
