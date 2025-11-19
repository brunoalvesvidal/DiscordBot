import discord
from discord import app_commands
from discord.ext import commands

from database.mongo import (
    insert_suporte,
    get_suporte_by_id,
    close_suporte,
    count_suportes,
)


class SuporteN2Modal(discord.ui.Modal, title="Novo Suporte Avancado"):
    titulo = discord.ui.TextInput(
        label="Titulo do Suporte",
        placeholder="idclinic - Resumo do problema",
        max_length=50,
    )
    descricao = discord.ui.TextInput(
        label="Descreva o problema ou duvida",
        style=discord.TextStyle.paragraph,
        placeholder=(
            "Descreva com detalhes, prints e informacoes da clinica/customer se possivel"
        ),
        max_length=1000,
    )

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        titulo_canal = self.titulo.value.replace(" ", "-").lower()[:30]
        user = interaction.user

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True
            ),
        }

        canal = await interaction.guild.create_text_channel(
            name=titulo_canal,
            overwrites=overwrites,
            topic=f"Suporte aberto por {user.display_name}",
        )

        suporte_data = {
            "suporte_id": interaction.id,
            "user_id": user.id,
            "status": "open",
            "titulo": self.titulo.value,
            "descricao": self.descricao.value,
            "channel_id": canal.id,
        }

        await insert_suporte(suporte_data)

        await canal.send(
            f"Ola {user.mention}, seu suporte foi criado com sucesso!\n"
            f"**Titulo:** {self.titulo.value}\n"
            f"**Descricao:** {self.descricao.value}"
        )

        await interaction.followup.send(
            f"Seu suporte foi criado em {canal.mention}.",
            ephemeral=True,
        )


class SuporteCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="criar_suporte", description="Abrir um suporte N2")
    async def criar_suporte(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SuporteN2Modal(self.bot))

    @app_commands.command(
        name="status_suporte", description="Verificar status de um suporte N2"
    )
    @app_commands.describe(suporte_id="ID do suporte")
    async def status_suporte(
        self, interaction: discord.Interaction, suporte_id: int
    ):
        suporte = await get_suporte_by_id(suporte_id)
        if suporte:
            await interaction.response.send_message(
                f"Suporte {suporte_id} status: {suporte['status']}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"Suporte {suporte_id} nao encontrado!",
                ephemeral=True,
            )

    @app_commands.command(name="fechar_suporte", description="Fechar suporte N2")
    @app_commands.describe(
        suporte_id="ID do suporte", responsavel="Quem esta fechando o suporte"
    )
    async def fechar_suporte(
        self,
        interaction: discord.Interaction,
        suporte_id: int,
        responsavel: str,
    ):
        resultado = await close_suporte(suporte_id, responsavel)
        if resultado:
            await interaction.response.send_message(
                f"Suporte {suporte_id} foi fechado por {responsavel}.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"Suporte {suporte_id} nao encontrado ou ja finalizado.",
                ephemeral=True,
            )

    @app_commands.command(
        name="debug_suportes",
        description="Mostra quantos suportes existem no MongoDB",
    )
    async def debug_suportes(self, interaction: discord.Interaction):
        try:
            total = await count_suportes()
        except Exception as e:
            # Loga o erro completo no terminal para debug
            import traceback

            print("ERRO AO CONTAR SUPORTES NO MONGO:", repr(e))
            traceback.print_exc()

            await interaction.response.send_message(
                "Erro ao consultar o MongoDB. Veja o terminal para detalhes.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Total de suportes no MongoDB (suporteN2.Suporte): {total}",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(SuporteCommands(bot))
