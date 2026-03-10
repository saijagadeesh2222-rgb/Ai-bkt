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
            "messages": [
                {"role": "system", "content": "You are an AI assistant that answers freely and directly."},
                {"role": "user", "content": message.content}
            ]
        }
    )

    data = response.json()

    if "choices" in data:
        reply = data["choices"][0]["message"]["content"]
    else:
        print(data)
        reply = "API error. Check logs."

    await message.channel.send(reply)

bot.run(DISCORD_TOKEN)
