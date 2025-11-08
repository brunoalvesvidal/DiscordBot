import discord
from discord import app_commands
from discord.ext import commands

class TicketCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command simples: /ping
    @app_commands.command(name="ping", description="Verifica se o bot está online.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong! O bot está online.", ephemeral=True)

    # Exemplo: /ticket abrir
    @app_commands.command(name="ticket", description="Abre um novo ticket de suporte.")
    async def ticket(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        # Cria canal privado
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            overwrites=overwrites,
            reason="Abertura de ticket de suporte"
        )

        await interaction.response.send_message(
            f"🎟️ Ticket criado: {channel.mention}", ephemeral=True
        )
        await channel.send(f"👋 Olá {user.mention}! Explique seu problema para nossa equipe.")

async def setup(bot):
    await bot.add_cog(TicketCommands(bot))
