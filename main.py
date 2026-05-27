python3 << 'PYEOF'
code = r'''
# BANCO ALIANZA SANTANDER — Gran Chile RP
# Bot de Discord — main.py
#
# INSTALACION:
#   pip install "discord.py>=2.3.2" flask
#
# EN RENDER:
#   - Tipo de servicio: Web Service
#   - Build Command:  pip install "discord.py>=2.3.2" flask
#   - Start Command:  python main.py
#   - Variable de entorno TOKEN = tu_token_de_discord
#   - Variable de entorno GUILD_ID = id_de_tu_servidor

# ══ KEEP ALIVE — Flask para Render ══
from flask import Flask
from threading import Thread

_flask_app = Flask(__name__)

@_flask_app.route("/")
def _home():
    return "Banco Alianza Santander — ONLINE"

Thread(target=lambda: _flask_app.run(host="0.0.0.0", port=10000), daemon=True).start()

# ══ IMPORTS ══
import discord
from discord import app_commands
from discord.ext import commands, tasks
import json, os, random
from datetime import datetime, timedelta

# ══ CONFIGURACION ══
TOKEN    = os.environ.get("TOKEN", "TU_TOKEN_AQUI")
GUILD_ID = int(os.environ.get("GUILD_ID", "1234567890"))

# ══ COLORES ══
COLOR_PRINCIPAL   = 0x003087
COLOR_EXITO       = 0x00A650
COLOR_ERROR       = 0xE63946
COLOR_ADVERTENCIA = 0xFFD700
COLOR_INFO        = 0x4FC3F7
COLOR_CRIPTO      = 0xF7931A
COLOR_PREMIUM     = 0x7B2FBE
COLOR_AUTO        = 0xFF4500

TASA_CAMBIO = 950

# ══ DATOS ESTATICOS ══
TIPO_TARJETA = {
    "clasica":  {"nombre": "Clasica",  "emoji": "C", "limite": 200_000,    "color": 0x808080},
    "plata":    {"nombre": "Plata",    "emoji": "P", "limite": 500_000,    "color": 0xC0C0C0},
    "oro":      {"nombre": "Oro",      "emoji": "O", "limite": 1_500_000,  "color": 0xFFD700},
    "platinum": {"nombre": "Platinum", "emoji": "L", "limite": 5_000_000,  "color": 0x4FC3F7},
    "diamante": {"nombre": "Diamante", "emoji": "D", "limite": 15_000_000, "color": 0x7B2FBE},
}

CRIMENES = [
    "Robo a Banco",
    "Trafico de articulos ilegales",
    "Hackeo de sistema financiero",
    "Asalto a empresa",
    "Fraude electronico",
    "Robo de vehiculo de lujo",
    "Lavado de dinero",
    "Falsificacion de documentos",
]

TRABAJOS = [
    ("Taxista",      15_000,  30_000),
    ("Repartidor",   20_000,  40_000),
    ("Construccion", 25_000,  45_000),
    ("Cajero",       18_000,  35_000),
    ("Programador",  35_000,  70_000),
    ("Medico",       50_000,  90_000),
    ("Abogado",      45_000,  80_000),
    ("Policia",      30_000,  55_000),
]

# Catalogo de autos de la concesionaria
CATALOGO_AUTOS = {
    "toyota_corolla":   {"nombre": "Toyota Corolla",    "año": 2022, "precio": 8_500_000,   "categoria": "Sedan"},
    "hyundai_tucson":   {"nombre": "Hyundai Tucson",    "año": 2023, "precio": 14_000_000,  "categoria": "SUV"},
    "chevrolet_spark":  {"nombre": "Chevrolet Spark",   "año": 2021, "precio": 5_200_000,   "categoria": "Hatchback"},
    "ford_ranger":      {"nombre": "Ford Ranger",       "año": 2023, "precio": 18_500_000,  "categoria": "Pickup"},
    "bmw_320i":         {"nombre": "BMW 320i",          "año": 2022, "precio": 32_000_000,  "categoria": "Lujo"},
    "mercedes_clase_c": {"nombre": "Mercedes Clase C",  "año": 2023, "precio": 38_000_000,  "categoria": "Lujo"},
    "lamborghini":      {"nombre": "Lamborghini Huracan","año": 2023, "precio": 180_000_000, "categoria": "Superdeportivo"},
    "volkswagen_golf":  {"nombre": "Volkswagen Golf",   "año": 2022, "precio": 11_000_000,  "categoria": "Hatchback"},
    "kia_sportage":     {"nombre": "Kia Sportage",      "año": 2023, "precio": 13_500_000,  "categoria": "SUV"},
    "jeep_wrangler":    {"nombre": "Jeep Wrangler",     "año": 2022, "precio": 25_000_000,  "categoria": "Todoterreno"},
}

# Criptos oficiales del servidor Gran Chile RP
CRIPTO_SERVIDOR = {
    "PSD": {"nombre": "Peso Digital",   "supply": 10_000_000},
    "CLC": {"nombre": "ChileCoin",      "supply":  5_000_000},
    "ADC": {"nombre": "AndesCoin",      "supply":  2_000_000},
    "PAT": {"nombre": "PatagoniaCoin",  "supply":  1_000_000},
    "CPR": {"nombre": "CopperToken",    "supply":  8_000_000},
}

DB_FILE = "database.json"

# ══ BASE DE DATOS ══
def cargar_db():
    if not os.path.exists(DB_FILE):
        data = {
            "users": {},
            "cripto_precios": {},
            "acciones_precios": {},
            "cripto_servidor_precios": {},
            "criptos_creadas": {},
            "ultima_actualizacion_cripto": 0,
            "ultima_actualizacion_acciones": 0,
            "ultima_actualizacion_cripto_servidor": 0,
        }
        guardar_db(data)
        return data
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(user_id):
    db = cargar_db()
    uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "efectivo": 50_000, "banco": 0, "usd": 0, "usd_banco": 0,
            "tarjeta_debito": None, "tarjeta_credito": None,
            "deuda_credito": 0, "limite_credito": 0,
            "cuentas_ahorro": [], "prestamos": [],
            "cripto": {}, "cripto_servidor": {}, "acciones": {}, "autos": [],
            "historial": [],
            "ultimo_colectar": None, "ultimo_diario": None,
            "ultimo_crimen": None, "ultimo_trabajo": None,
            "rachas": 0, "penales": 0,
            "nombre_completo": None, "ocupacion": None,
            "ingresos": 0, "registrado": False,
            "nivel": 1, "experiencia": 0, "logros": [],
            "transferencias_hoy": 0, "ultima_transferencia_fecha": None,
        }
        guardar_db(db)
    return db["users"][uid]

def save_user(user_id, data):
    db = cargar_db()
    db["users"][str(user_id)] = data
    guardar_db(db)

def add_historial(user_id, tipo, monto, descripcion):
    db = cargar_db()
    uid = str(user_id)
    if uid not in db["users"]:
        return
    h = db["users"][uid].setdefault("historial", [])
    h.insert(0, {"tipo": tipo, "monto": monto, "descripcion": descripcion,
                 "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")})
    db["users"][uid]["historial"] = h[:50]
    guardar_db(db)

# ══ UTILIDADES ══
def clp(monto):
    return "$" + "{:,}".format(int(monto)).replace(",", ".") + " CLP"

def usd_fmt(monto):
    return "${:.2f} USD".format(float(monto))

def generar_numero_tarjeta():
    return " ".join(str(random.randint(1000, 9999)) for _ in range(4))

def generar_placa():
    letras = "ABCDEFGHJKLMNPRSTUVWXYZ"
    return (random.choice(letras) + random.choice(letras) +
            str(random.randint(10, 99)) +
            random.choice(letras) + random.choice(letras))

def agregar_xp(user, cantidad):
    user["experiencia"] = user.get("experiencia", 0) + cantidad
    nivel_viejo = user.get("nivel", 1)
    nivel_nuevo = 1 + int(user["experiencia"] ** 0.4 / 3)
    user["nivel"] = nivel_nuevo
    return nivel_nuevo, nivel_nuevo > nivel_viejo

def get_precios_cripto(db):
    ahora = datetime.now().timestamp()
    if not db.get("cripto_precios") or ahora - db.get("ultima_actualizacion_cripto", 0) > 3600:
        db["cripto_precios"] = {
            "BTC": random.randint(25_000_000, 35_000_000),
            "ETH": random.randint(1_500_000, 2_000_000),
            "SOL": random.randint(80_000, 120_000),
            "DOGE": random.randint(60, 120),
            "ADA": random.randint(300, 600),
        }
        db["ultima_actualizacion_cripto"] = ahora
        guardar_db(db)
    return db["cripto_precios"]

def get_precios_acciones(db):
    ahora = datetime.now().timestamp()
    if not db.get("acciones_precios") or ahora - db.get("ultima_actualizacion_acciones", 0) > 3600:
        db["acciones_precios"] = {
            "COPEC": random.randint(7_000, 10_000),
            "FALABELLA": random.randint(2_500, 4_000),
            "BCI": random.randint(30_000, 40_000),
            "CMPC": random.randint(1_500, 2_500),
            "ENTEL": random.randint(900, 1_500),
            "LATAM": random.randint(3_000, 5_000),
            "CENCOSUD": random.randint(1_800, 3_000),
        }
        db["ultima_actualizacion_acciones"] = ahora
        guardar_db(db)
    return db["acciones_precios"]

def get_precios_cripto_servidor(db):
    ahora = datetime.now().timestamp()
    if not db.get("cripto_servidor_precios") or ahora - db.get("ultima_actualizacion_cripto_servidor", 0) > 3600:
        precios = {}
        for s in CRIPTO_SERVIDOR:
            precios[s] = random.randint(500, 50_000)
        for s, info in db.get("criptos_creadas", {}).items():
            precio_base = info.get("precio_inicial", 1000)
            precios[s] = max(100, int(precio_base * random.uniform(0.5, 2.0)))
        db["cripto_servidor_precios"] = precios
        db["ultima_actualizacion_cripto_servidor"] = ahora
        guardar_db(db)
    return db["cripto_servidor_precios"]

# ══ BOT ══
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
guild_obj = discord.Object(id=GUILD_ID)

@bot.event
async def on_ready():
    print("Bot listo:", bot.user)
    bot.tree.copy_global_to(guild=guild_obj)
    await bot.tree.sync(guild=guild_obj)
    print("Slash commands sincronizados.")
    if not actualizar_precios.is_running():
        actualizar_precios.start()
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="Banco Alianza Santander | Gran Chile RP"
    ))

@tasks.loop(hours=1)
async def actualizar_precios():
    db = cargar_db()
    db["ultima_actualizacion_cripto"] = 0
    db["ultima_actualizacion_acciones"] = 0
    db["ultima_actualizacion_cripto_servidor"] = 0
    guardar_db(db)

# ══ /balanza ══
@bot.tree.command(guild=guild_obj, name="balanza", description="Ver tu balance financiero completo")
async def balanza(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    tc = TIPO_TARJETA.get(user.get("tarjeta_credito")) if user.get("tarjeta_credito") else None
    cripto_txt = "\n".join(k + ": " + "{:.6f}".format(v) for k, v in user.get("cripto", {}).items() if v > 0) or "Sin saldo"
    patrimonio_clp = user["efectivo"] + user["banco"]
    patrimonio_usd = user.get("usd", 0) + user.get("usd_banco", 0)
    if user.get("registrado"):
        identidad_val = str(user.get("nombre_completo", "")) + " | " + str(user.get("ocupacion", ""))
    else:
        identidad_val = "No registrado como ciudadano"
    credito_val = (tc["nombre"]) if tc else "Sin tarjeta"
    num_autos = len(user.get("autos", []))
    em = discord.Embed(title="Balanza Financiera: " + interaction.user.display_name, color=COLOR_PRINCIPAL)
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(name="Identidad", value=identidad_val, inline=False)
    em.add_field(name="CLP", value="Efectivo: " + clp(user["efectivo"]) + "\nBanco: " + clp(user["banco"]), inline=True)
    em.add_field(name="USD", value="Banco: " + usd_fmt(user.get("usd_banco", 0)), inline=True)
    em.add_field(name="Tarjetas", value="Debito: " + ("Activa" if user.get("tarjeta_debito") else "Sin tarjeta") + "\nCredito: " + credito_val, inline=True)
    em.add_field(name="Cripto Global", value=cripto_txt, inline=True)
    em.add_field(name="Autos", value=str(num_autos) + " vehiculo(s)", inline=True)
    em.add_field(name="Patrimonio Total", value=clp(patrimonio_clp) + "\n" + usd_fmt(patrimonio_usd), inline=False)
    em.add_field(name="Nivel", value=str(user.get("nivel", 1)) + " | XP: " + str(user.get("experiencia", 0)), inline=True)
    em.add_field(name="Racha", value=str(user.get("rachas", 0)) + " dias", inline=True)
    em.set_footer(text="Banco Alianza Santander - Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══ /perfil ══
@bot.tree.command(guild=guild_obj, name="perfil", description="Ver tu perfil economico completo")
async def perfil(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    tc = TIPO_TARJETA.get(user.get("tarjeta_credito")) if user.get("tarjeta_credito") else None
    logros = user.get("logros", []) or ["Sin logros aun"]
    identidad_val = (str(user.get("nombre_completo", "")) + " | " + str(user.get("ocupacion", ""))) if user.get("registrado") else "No registrado"
    credito_val = tc["nombre"] if tc else "Sin tarjeta"
    logros_val = "\n".join(logros[-5:]) if logros and isinstance(logros[0], str) else "Sin logros"
    em = discord.Embed(title="Perfil: " + interaction.user.display_name, color=COLOR_PRINCIPAL)
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(name="Identidad", value=identidad_val, inline=True)
    em.add_field(name="Nivel", value=str(user.get("nivel", 1)) + "\nXP: " + str(user.get("experiencia", 0)), inline=True)
    em.add_field(name="Racha", value=str(user.get("rachas", 0)) + " dias", inline=True)
    em.add_field(name="Efectivo", value=clp(user["efectivo"]), inline=True)
    em.add_field(name="Banco", value=clp(user["banco"]), inline=True)
    em.add_field(name="USD Banco", value=usd_fmt(user.get("usd_banco", 0)), inline=True)
    em.add_field(name="Debito", value="Activa" if user.get("tarjeta_debito") else "Sin tarjeta", inline=True)
    em.add_field(name="Credito", value=credito_val, inline=True)
    em.add_field(name="Penales", value=str(user.get("penales", 0)), inline=True)
    em.add_field(name="Prestamos", value=str(len(user.get("prestamos", []))), inline=True)
    em.add_field(name="Autos", value=str(len(user.get("autos", []))), inline=True)
    em.add_field(name="Ahorro", value=str(len(user.get("cuentas_ahorro", []))) + "/3", inline=True)
    em.add_field(name="Logros", value=logros_val, inline=False)
    em.set_footer(text="Banco Alianza Santander - Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══ /debito ══
grupo_debito = app_commands.Group(name="debito", description="Gestionar tu cuenta de debito", guild_ids=[GUILD_ID])

@grupo_debito.command(name="estado", description="Ver tu saldo bancario y tarjeta")
async def debito_estado(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    em = discord.Embed(title="Estado de Cuenta Debito", color=COLOR_PRINCIPAL)
    em.add_field(name="Efectivo", value=clp(user["efectivo"]), inline=True)
    em.add_field(name="Banco", value=clp(user["banco"]), inline=True)
    em.add_field(name="USD Banco", value=usd_fmt(user.get("usd_banco", 0)), inline=True)
    if user.get("tarjeta_debito"):
        titular = user.get("nombre_completo", interaction.user.display_name)
        em.add_field(name="Tarjeta", value="Activa\n" + user["tarjeta_debito"]["numero"] + "\nTitular: " + titular, inline=False)
    else:
        em.add_field(name="Tarjeta", value="Sin tarjeta. Usa /banco para solicitar una.", inline=False)
    em.set_footer(text="Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="depositar", description="Guardar efectivo en el banco")
@app_commands.describe(monto="Monto en CLP")
async def debito_depositar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto <= 0:
        return await interaction.response.send_message("El monto debe ser mayor a 0.", ephemeral=True)
    if user["efectivo"] < monto:
        return await interaction.response.send_message("Efectivo insuficiente. Tienes " + clp(user["efectivo"]), ephemeral=True)
    user["efectivo"] -= monto
    user["banco"] += monto
    agregar_xp(user, 5)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DEPOSITO", monto, "Deposito de " + clp(monto))
    em = discord.Embed(title="Deposito Exitoso", color=COLOR_EXITO,
        description="Depositaste " + clp(monto) + "\nNuevo saldo: " + clp(user["banco"]))
    em.set_footer(text="Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="retirar", description="Retirar dinero del banco")
@app_commands.describe(monto="Monto en CLP")
async def debito_retirar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto <= 0:
        return await interaction.response.send_message("El monto debe ser mayor a 0.", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message("Saldo insuficiente. Tienes " + clp(user["banco"]), ephemeral=True)
    user["banco"] -= monto
    user["efectivo"] += monto
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "RETIRO", monto, "Retiro de " + clp(monto))
    em = discord.Embed(title="Retiro Exitoso", color=COLOR_EXITO,
        description="Retiraste " + clp(monto) + "\nEfectivo: " + clp(user["efectivo"]))
    em.set_footer(text="Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="transferir", description="Transferir dinero a otro usuario")
@app_commands.describe(usuario="Usuario a quien transferir", monto="Monto en CLP")
async def debito_transferir(interaction: discord.Interaction, usuario: discord.Member, monto: int):
    if usuario.id == interaction.user.id:
        return await interaction.response.send_message("No puedes transferirte a ti mismo.", ephemeral=True)
    if usuario.bot:
        return await interaction.response.send_message("No puedes transferir a un bot.", ephemeral=True)
    if monto <= 0:
        return await interaction.response.send_message("El monto debe ser mayor a 0.", ephemeral=True)
    user = get_user(interaction.user.id)
    if not user.get("tarjeta_debito"):
        return await interaction.response.send_message("Necesitas una tarjeta de debito para transferir.", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message("Saldo insuficiente. Tienes " + clp(user["banco"]), ephemeral=True)
    receptor = get_user(usuario.id)
    user["banco"] -= monto
    receptor["banco"] += monto
    agregar_xp(user, 10)
    save_user(interaction.user.id, user)
    save_user(usuario.id, receptor)
    add_historial(interaction.user.id, "TRANSFERENCIA", -monto, "Transferencia a " + usuario.display_name)
    add_historial(usuario.id, "TRANSFERENCIA", monto, "Transferencia de " + interaction.user.display_name)
    em = discord.Embed(title="Transferencia Exitosa", color=COLOR_EXITO,
        description="Transferiste " + clp(monto) + " a " + usuario.display_name + "\nTu saldo: " + clp(user["banco"]))
    em.set_footer(text="Banco Alianza Santander")
    await interaction.response.send_message(embed=em)

bot.tree.add_command(grupo_debito)

# ══ /ahorro ══
grupo_ahorro = app_commands.Group(name="ahorro", description="Gestionar cuentas de ahorro", guild_ids=[GUILD_ID])
TASA_AHORRO = 0.03

@grupo_ahorro.command(name="abrir", description="Abrir una cuenta de ahorro (minimo 10.000)")
@app_commands.describe(monto="Monto inicial en CLP")
async def ahorro_abrir(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto < 10_000:
        return await interaction.response.send_message("Minimo 10.000 CLP.", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message("Saldo insuficiente. Tienes " + clp(user["banco"]), ephemeral=True)
    if len(user.get("cuentas_ahorro", [])) >= 3:
        return await interaction.response.send_message("Maximo 3 cuentas de ahorro.", ephemeral=True)
    user["banco"] -= monto
    user.setdefault("cuentas_ahorro", []).append({
        "id": int(datetime.now().timestamp()), "saldo": monto,
        "apertura": datetime.now().strftime("%d/%m/%Y")
    })
    agregar_xp(user, 20)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_ABRIR", monto, "Ahorro abierto con " + cl