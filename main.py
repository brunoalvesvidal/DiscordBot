import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Ativar intents
intents = discord.Intents.default()
intents.message_content = True

# Criar bot (com árvore de comandos de aplicação — slash commands)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 {len(synced)} comandos sincronizados com o Discord.")
    except Exception as e:
        print(f"⚠️ Erro ao sincronizar comandos: {e}")

async def main():
    async with bot:
        # Carregar módulo de comandos (Cog)
        await bot.load_extension("bot.commands_ticket")
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
