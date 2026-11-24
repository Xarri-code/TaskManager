"""Gére le bot TaskManager"""

import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv
from github import Github, GithubException, Auth

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
gh = Github(auth=Auth.Token(os.getenv("GITHUB_TOKEN")))
repo = gh.get_repo(os.getenv("GITHUB_REPO"))


class Bot(discord.Client):
    """Class bot"""
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


bot = Bot()


def assigner_issue(numero: int, utilisateur: str) -> str:
    """Assigne une issues"""
    issue = repo.get_issue(numero)
    issue.add_to_assignees(utilisateur)
    return issue.title


@bot.tree.command(name="assigner", description="Assigner une issue GitHub à quelqu'un")
@app_commands.describe(issue="Numéro de l'issue", utilisateur="Login GitHub de la personne")
async def assigner(interaction: discord.Interaction, issue: int, utilisateur: str):
    """Affiche la commande /assigner"""
    await interaction.response.defer()
    try:
        # PyGithub est bloquant, donc on l'exécute dans un thread
        titre = await asyncio.to_thread(assigner_issue, issue, utilisateur)
        await interaction.followup.send(f"✅ Issue #{issue} (« {titre} ») assignée à **{utilisateur}**.")
    except GithubException as e:
        await interaction.followup.send(f"❌ Erreur GitHub : {e.data.get('message', 'inconnue')}")


@bot.event
async def on_ready():
    """Voir si connecté"""
    print(f"Connecté en tant que {bot.user}")


bot.run(DISCORD_TOKEN)
