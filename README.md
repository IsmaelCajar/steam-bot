# 🎮 Steam Bot — Bot de Discord

Bot de Discord que consulta información de juegos en tiempo real usando la API pública de Steam.

## ¿Qué hace?

Permite a los usuarios de un servidor de Discord consultar datos de Steam directamente desde el chat, sin salir de Discord.

## Comandos

| Comando | Descripción |
|---|---|
| `!populares` | Muestra los 5 juegos con más jugadores en Steam en este momento |
| `!juego <nombre>` | Muestra precio, género y descripción de un juego específico |
| `!buscar <nombre>` | Lista los primeros 5 resultados de Steam para un término de búsqueda (variantes de un juego)|
| `!ayuda` | Muestra la lista de comandos disponibles |

## Tecnologías usadas

- **Python 3.14**
- **discord.py** — conexión con la API de Discord
- **aiohttp** — peticiones HTTP asíncronas a la API de Steam

## Instalación

1. Clona o descarga el proyecto
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```
3. Coloca tu token en el archivo `steam-bot.py`:
```python
TOKEN = "TU_TOKEN_AQUI"
```
4. Ejecuta el bot:
```bash
python steam-bot.py
```

## Configuración en Discord

En el portal de desarrolladores (discord.com/developers) activa los siguientes intents para tu bot:
- **Message Content Intent**

Permisos del bot:
- Enviar mensajes
- Gestionar mensajes

## API utilizada

Este bot usa la API pública de Steam, que es gratuita y no requiere registro ni API key.

- Juegos más jugados: `api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/`
- Búsqueda de juegos: `store.steampowered.com/api/storesearch`
- Detalles de un juego: `store.steampowered.com/api/appdetails`
