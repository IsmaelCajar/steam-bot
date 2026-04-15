import discord
from discord.ext import commands
import aiohttp

TOKEN = "COLOCAR TOKEN AQUI"

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

@client.event
async def on_message(message):
    print(f"Mensaje de {message.author}: {message.content}")

    if message.author == client.user:
        return

    await client.process_commands(message)

@client.command()
async def populares(ctx):
    url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as respuesta:
            datos = await respuesta.json()

        juegos = datos["response"]["ranks"][:5]

        embed = discord.Embed(
            title="Top 5 juegos más jugados en Steam",
            color=discord.Color.blue()
        )

        for juego in juegos:
            appid = juego["appid"]
            url_nombre = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            
            async with session.get(url_nombre) as r:
                info = await r.json()
            
            nombre = info[str(appid)]["data"]["name"]
            jugadores = f"{juego['peak_in_game']:,} jugadores en su pico"
            embed.add_field(name=f"#{juego['rank']} — {nombre}", value=jugadores, inline=False)

        embed.set_footer(text="Datos obtenidos de la API de Steam")

    await ctx.send(embed=embed)

@client.command()
async def juego(ctx, *, nombre):
    async with aiohttp.ClientSession() as session:

        
        url_busqueda = f"https://store.steampowered.com/api/storesearch?term={nombre}&l=english&cc=US"
        async with session.get(url_busqueda) as r:
            busqueda = await r.json()

        if busqueda["total"] == 0:
            await ctx.send(f"No encontré ningún juego llamado **{nombre}**.")
            return

        appid = busqueda["items"][0]["id"]

        async with session.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=spanish&cc=CO") as r:
            info = await r.json()

        data = info[str(appid)]["data"]

        embed = discord.Embed(
            title=data["name"],
            description=data.get("short_description", "Sin descripción."),
            color=discord.Color.green()
        )

        precio = data.get("price_overview", {}).get("final_formatted", "Gratis")
        embed.add_field(name="Precio", value=precio, inline=True)
        embed.add_field(name="Géneros", value=", ".join(g["description"] for g in data.get("genres", [])), inline=True)
        embed.set_thumbnail(url=data.get("header_image", ""))
        embed.set_footer(text="Datos obtenidos de la API de Steam")

    await ctx.send(embed=embed)

@client.command()
async def buscar(ctx, *, nombre):
    url = f"https://store.steampowered.com/api/storesearch?term={nombre}&l=spanish&cc=CO"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            datos = await r.json()

    if datos["total"] == 0:
        await ctx.send(f"No encontré resultados para **{nombre}**.")
        return

    resultados = datos["items"][:5]

    print(resultados)

    embed = discord.Embed(
        title=f"Resultados para: {nombre}",
        color=discord.Color.orange()
    )

    for item in resultados:
        plataformas = []
        if item["platforms"]["windows"]:
            plataformas.append("Windows")
        if item["platforms"]["mac"]:
            plataformas.append("Mac")
        if item["platforms"]["linux"]:
            plataformas.append("Linux")

        embed.add_field(
            name=item["name"],
            value=f"{', '.join(plataformas)}",
            inline=False
        )


    embed.set_footer(text=f"{datos['total']} resultados totales en Steam")

    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Ese comando no existe. Usa `!ayuda` para ver los disponibles.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Te faltó un argumento. Uso correcto: `!{ctx.command.name} <nombre>`")
    else:
        await ctx.send(" Ocurrió un error inesperado.")
        print(f"Error: {error}")

@client.command()
async def ayuda(ctx):
    embed = discord.Embed(
        title="Comandos disponibles:",
        color=discord.Color.red()
    )
    embed.add_field(name="`!populares`", value="Muestra los 5 juegos con más jugadores en Steam en este momento.", inline=False)
    embed.add_field(name="`!juego <nombre>`", value="Muestra precio, género y descripción de un juego específico.", inline=False)
    embed.add_field(name="`!buscar <nombre>`", value="Lista los primeros 5 resultados de Steam para un término de búsqueda. (variantes de un juego)", inline=False)

    await ctx.send(embed=embed)

client.run(TOKEN)
