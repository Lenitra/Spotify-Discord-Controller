import interactions
from interactions import Permissions, slash_option, Embed, events
from APISpotify import get_track_info, recherche_chanson
import yaml
import requests


bot = interactions.Client()


with open("config.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    token = data["discord_token"]
    acces_to = data["discord_users"]


def has_access(ctx):
    try:
        if ctx.author.id in acces_to["users"]:
            return True
    except:
        pass
    try:
        for role in ctx.author.roles:
            if role.id in acces_to["roles"]:
                return True
    except:
        pass
    return False


@interactions.listen()
async def on_startup():
    print("Bot OK !")


@interactions.slash_command(
    description="Ajouter une musique à la fille d'attente, elle passera juste après"
)
@slash_option(
    name="musique",
    description="Le nom de la musique à ajouter",
    required=True,
    opt_type=3,
)
async def add(ctx, musique):
    if not has_access(ctx):
        await ctx.send("Erreur : vous n'avez pas les permissions pour utiliser cette commande", ephemeral=True)
        return
    idmusique = recherche_chanson(musique)

    if idmusique is None:
        await ctx.send("Erreur : la musique n'a pas été trouvée")
        return

    infos = get_track_info(idmusique)
    string = ""
    string += ctx.author.mention + " propose :\n"
    string += "     Titre : " + infos[0] + "\n"
    string += "     Artiste : " + infos[1] + "\n"
    string += infos[2] + "\n"

    msg = await ctx.send(string)

    # add reation to message
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")


# print all reactions
@interactions.listen()
async def MessageReactionAdd(event):
    if event.author.id == bot.user.id:
        return

    if event.emoji.name == "✅":
        toadd = ""
        toadd += event.message.content.split("\n")[1].split("Titre : ")[1] + " "
        toadd += event.message.content.split("\n")[2].split("Artiste : ")[1]

        await event.message.delete()

        print(
            requests.post(
                f"http://localhost:8888/addqueue?uri={recherche_chanson(toadd)}"
            ).text
        )
        await event.message.channel.send(f"{toadd} ajoutée à la file d'attente !")

    if event.emoji.name == "❌":
        await event.message.delete()


bot.start(token)
