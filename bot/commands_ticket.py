import discord 
from discord import app_commands
from discord.ext import commands
from database.mongo import insert_suporte, get_suporte_by_id, close_suporte


class SuporteN2Modal(discord.ui.Modal, title= "Novo Suporte Avançado"):
    titulo = discord.ui.TextInput(
        label="Título do Suporte",
        placeholder="idclinic - Resumo do problema",
        max_length=50
    )
    descricao = discord.ui.TextInput(
        label="Descreva o problema ou Duvida",
        style=discord.TextSyle.paragraph,
        placeholder="Descreva com detalhes, prints e informações da clínica/customer se possível",
        max_length=1000
    )

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot


    async def on_submit(self, interaction: discord.Interaction):
        titulo = self.titulo.value.replace(" ","-").lowe()[:30]
        user = interaction.user

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        canal = await interaction.guild.create_text_channel(
            name=f"{titulo}"
            overwrites=overwrites,
            topic=f"Suporte aberto por {user.display_name}",
        )

        suporte_data = {
            "suporte_id": interaction.id,
            "user_id": user.id,
            "status": "open",
            "titulo": self.titulo.value,
            "descricao": self.descricao.value,
            "channel_id": canal.id
        }
        await insert_suporte(suporte_data)

        await interaction.response.send_message(
            f"Suporte Avançado : {canal.mention}", ephemeral=True
        )

        await canal.send(
            f"Olá {user.mention}, seu suporte foi criado com sucesso!\n"
            f"**Título:** {self.titulo.value}\n"
            f"**Descição** {self.descricao.value}"
        )