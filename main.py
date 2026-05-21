# Asegúrate de que no haya ni un solo espacio antes de cada palabra
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "¡Bot de Gran Chile RP Online!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ╔════════════════════════════════════════════════════════════════╗
# ║ 🏦BANCO ALIANZA SANTANDER-Gran Chile rol                       ║
# ║                      Bot Delaware Discordia                    ║
# ║                      Archivo:principal.py                      ║
# ╚════════════════════════════════════════════════════════════════╝

INSTALACIÓN:
  pip install discord.py

CONFIGURACIÓN:
  Cambia TOKEN, CLIENT_ID y GUILD_ID abajo antes de ejecutar.

EJECUTAR:
  python main.py
"""
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "¡Bot BANCO ALIANZA CORDILLERA ONLINE!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
import discord
from discord import app_commands
from discord.ext import commands, tasks
import json, os, random, math
from datetime import datetime, timedelta
from typing import Optional

# ══════════════════════════════════════════════════════════════
# ⚙️  CONFIGURACIÓN — CAMBIA ESTOS VALORES
# ══════════════════════════════════════════════════════════════
TOKEN    = "TU_TOKEN_AQUI"
GUILD_ID = 1234567890  # ID de tu servidor (número, sin comillas)

# ══════════════════════════════════════════════════════════════
# 🎨 CONSTANTES
# ══════════════════════════════════════════════════════════════
COLOR_PRINCIPAL  = 0x003087
COLOR_EXITO      = 0x00A650
COLOR_ERROR      = 0xE63946
COLOR_ADVERTENCIA= 0xFFD700
COLOR_INFO       = 0x4FC3F7
COLOR_CRIPTO     = 0xF7931A
COLOR_PREMIUM    = 0x7B2FBE

TASA_CAMBIO = 950  # 1 USD = 950 CLP

TIPO_TARJETA = {
    "clasica":  {"nombre": "Clásica",  "emoji": "💳", "limite": 200_000,    "color": 0x808080},
    "plata":    {"nombre": "Plata",    "emoji": "🥈", "limite": 500_000,    "color": 0xC0C0C0},
    "oro":      {"nombre": "Oro",      "emoji": "🥇", "limite": 1_500_000,  "color": 0xFFD700},
    "platinum": {"nombre": "Platinum", "emoji": "💎", "limite": 5_000_000,  "color": 0x4FC3F7},
    "diamante": {"nombre": "Diamante", "emoji": "💠", "limite": 15_000_000, "color": 0x7B2FBE},
}

CRIMENES = [
    "🏦 Robo a Banco",
    "📦 Tráfico de artículos ilegales",
    "💻 Hackeo de sistema financiero",
    "🏢 Asalto a empresa",
    "📱 Fraude electrónico",
    "🚗 Robo de vehículo de lujo",
    "💰 Lavado de dinero",
    "🔐 Falsificación de documentos",
]

DB_FILE = "database.json"

# ══════════════════════════════════════════════════════════════
# 🗄️  BASE DE DATOS (JSON)
# ══════════════════════════════════════════════════════════════
def cargar_db() -> dict:
    if not os.path.exists(DB_FILE):
        data = {"users": {}, "cripto_precios": {}, "acciones_precios": {}, "ultima_actualizacion": 0}
        guardar_db(data)
        return data
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_db(db: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(user_id: str) -> dict:
    db = cargar_db()
    uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "efectivo":          50_000,
            "banco":             0,
            "usd":               0,
            "usd_banco":         0,
            "tarjeta_debito":    None,
            "tarjeta_credito":   None,
            "deuda_credito":     0,
            "limite_credito":    0,
            "cuentas_ahorro":    [],
            "prestamos":         [],
            "cripto":            {},
            "acciones":          {},
            "historial":         [],
            "ultimo_colectar":   None,
            "ultimo_diario":     None,
            "ultimo_crimen":     None,
            "ultimo_trabajo":    None,
            "rachas":            0,
            "penales":           0,
            "nombre_completo":   None,
            "ocupacion":         None,
            "ingresos":          0,
            "registrado":        False,
            "nivel":             1,
            "experiencia":       0,
            "logros":            [],
            "transferencias_hoy": 0,
            "ultima_transferencia_fecha": None,
        }
        guardar_db(db)
    return db["users"][uid]

def save_user(user_id: str, data: dict):
    db = cargar_db()
    db["users"][str(user_id)] = data
    guardar_db(db)

def add_historial(user_id: str, tipo: str, monto: int, descripcion: str):
    db = cargar_db()
    uid = str(user_id)
    if uid not in db["users"]:
        return
    h = db["users"][uid].setdefault("historial", [])
    h.insert(0, {
        "tipo": tipo,
        "monto": monto,
        "descripcion": descripcion,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
    })
    db["users"][uid]["historial"] = h[:50]
    guardar_db(db)

def clp(monto) -> str:
    return f"${int(monto):,} CLP".replace(",", ".")

def usd(monto) -> str:
    return f"${float(monto):,.2f} USD"

def generar_numero_tarjeta() -> str:
    return " ".join(str(random.randint(1000, 9999)) for _ in range(4))

def get_precios_cripto(db: dict) -> dict:
    ahora = datetime.now().timestamp()
    if not db.get("cripto_precios") or ahora - db.get("ultima_actualizacion_cripto", 0) > 3600:
        db["cripto_precios"] = {
            "BTC":  random.randint(25_000_000, 35_000_000),
            "ETH":  random.randint(1_500_000,  2_000_000),
            "SOL":  random.randint(80_000,     120_000),
            "DOGE": random.randint(60,          120),
            "ADA":  random.randint(300,         600),
        }
        db["ultima_actualizacion_cripto"] = ahora
        guardar_db(db)
    return db["cripto_precios"]

def get_precios_acciones(db: dict) -> dict:
    ahora = datetime.now().timestamp()
    if not db.get("acciones_precios") or ahora - db.get("ultima_actualizacion_acciones", 0) > 3600:
        db["acciones_precios"] = {
            "COPEC":     random.randint(7_000,   10_000),
            "FALABELLA": random.randint(2_500,    4_000),
            "BCI":       random.randint(30_000,  40_000),
            "CMPC":      random.randint(1_500,    2_500),
            "ENTEL":     random.randint(900,      1_500),
            "LATAM":     random.randint(3_000,    5_000),
            "CENCOSUD":  random.randint(1_800,    3_000),
        }
        db["ultima_actualizacion_acciones"] = ahora
        guardar_db(db)
    return db["acciones_precios"]

def agregar_xp(user, monto): # O como se llame tu función
    """
    Agrega XP y retorna (nivel_actual, subio_de_nivel)
    """
    # Aquí sigue tu código normal...
    user["experiencia"] = user.get("experiencia", 0) + cantidad
    nivel_viejo = user.get("nivel", 1)
    nivel_nuevo = 1 + int(user["experiencia"] ** 0.4 / 3)
    user["nivel"] = nivel_nuevo
    return nivel_nuevo, nivel_nuevo > nivel_viejo

# ══════════════════════════════════════════════════════════════
# 🤖 BOT
# ══════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
guild_obj = discord.Object(id=GUILD_ID)

@bot.event
async def on_ready():
    print(f"✅ Bot listo: {bot.user}")
    bot.tree.copy_global_to(guild=guild_obj)
    await bot.tree.sync(guild=guild_obj)
    print("✅ Slash commands sincronizados.")
    actualizar_precios.start()
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="🏦 Banco Alianza Santander | Gran Chile RP")
    )

@tasks.loop(hours=1)
async def actualizar_precios():
    db = cargar_db()
    db["ultima_actualizacion_cripto"] = 0
    db["ultima_actualizacion_acciones"] = 0
    guardar_db(db)

# ══════════════════════════════════════════════════════════════
# ⚖️  /balanza
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="balanza", description="⚖️ Ver tu balance financiero personal completo")
async def balanza(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None

    cripto_txt = "\n".join(
        f"**{k}:** {v:.6f}" for k, v in user.get("cripto", {}).items() if v > 0
    ) or "*Sin saldo*"

    patrimonio_clp = user["efectivo"] + user["banco"]
    patrimonio_usd = user["usd"] + user["usd_banco"]

    if user["registrado"]:
        identidad_val = f"**{user['nombre_completo']}**\n*{user['ocupacion']}*"
    else:
        identidad_val = "*No registrado como ciudadano*"

    if tc:
        credito_val = f"{tc['emoji']} {tc['nombre']}"
    else:
        credito_val = "❌ Sin tarjeta"

    em = discord.Embed(
        title=f"⚖️ Balanza Financiera: {interaction.user.display_name}",
        color=COLOR_PRINCIPAL
    )
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(
        name="👤 Identidad",
        value=identidad_val,
        inline=False
    )
    em.add_field(
        name="🇨🇱 CLP — Pesos Chilenos",
        value=(
            f"💵 **Efectivo:** {clp(user['efectivo'])}\n"
            f"🏦 **Banco:** {clp(user['banco'])}\n"
            f"💳 **Deuda Crédito:** {clp(user['deuda_credito'])}\n"
            f"💰 **Crédito Disponible:** {clp(max(0, user['limite_credito'] - user['deuda_credito']))}"
        ),
        inline=True
    )
    em.add_field(
        name="🇺🇸 USD — Dólares",
        value=f"💵 **Efectivo:** {usd(user['usd'])}\n🏦 **Banco:** {usd(user['usd_banco'])}",
        inline=True
    )
    em.add_field(name="\u200b", value="\u200b", inline=False)
    em.add_field(
        name="💳 Tarjetas",
        value=f"**Débito:** {'✅ Activa' if user['tarjeta_debito'] else '❌ Sin tarjeta'}\n**Crédito:** {credito_val}",
        inline=True
    )
    em.add_field(name="🪙 Billetera Cripto", value=cripto_txt, inline=True)
    em.add_field(
        name="📊 Patrimonio Total",
        value=f"🇨🇱 **{clp(patrimonio_clp)}**\n🇺🇸 **{usd(patrimonio_usd)}**",
        inline=False
    )
    em.add_field(name="⭐ Nivel", value=f"**{user.get('nivel', 1)}** | XP: {user.get('experiencia', 0)}", inline=True)
    em.add_field(name="🔥 Racha", value=f"**{user.get('rachas', 0)}** días", inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP | Información financiera personal")
    em.timestamp = datetime.now()

    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 👤 /perfil
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="perfil", description="👤 Ver tu perfil económico completo")
async def perfil(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
    logros = user.get("logros", []) or ["*Sin logros aún*"]

    if user["registrado"]:
        identidad_val = f"**{user['nombre_completo']}**\n{user['ocupacion']}"
    else:
        identidad_val = "*No registrado*"

    if tc:
        credito_val = f"{tc['emoji']} {tc['nombre']}"
    else:
        credito_val = "❌ Sin tarjeta"

    em = discord.Embed(title=f"👤 Perfil: {interaction.user.display_name}", color=COLOR_PRINCIPAL)
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(name="📋 Identidad", value=identidad_val, inline=True)
    em.add_field(name="⭐ Nivel", value=f"**{user.get('nivel', 1)}**\nXP: {user.get('experiencia', 0)}", inline=True)
    em.add_field(name="🔥 Racha", value=f"**{user.get('rachas', 0)}** días", inline=True)
    em.add_field(name="💵 Efectivo", value=clp(user["efectivo"]), inline=True)
    em.add_field(name="🏦 Banco", value=clp(user["banco"]), inline=True)
    em.add_field(name="🇺🇸 USD Banco", value=usd(user["usd_banco"]), inline=True)
    em.add_field(name="💳 Débito", value="✅ Activa" if user["tarjeta_debito"] else "❌ Sin tarjeta", inline=True)
    em.add_field(name="💎 Crédito", value=credito_val, inline=True)
    em.add_field(name="🚔 Penales", value=str(user.get("penales", 0)), inline=True)
    em.add_field(name="📋 Préstamos activos", value=str(len(user.get("prestamos", []))), inline=True)
    em.add_field(name="💰 Cuentas ahorro", value=f"{len(user.get('cuentas_ahorro', []))}/3", inline=True)
    if isinstance(logros[0], str):
        logros_val = "\n".join(logros[-5:])
    else:
        logros_val = "*Sin logros*"
    em.add_field(name="🏆 Logros", value=logros_val, inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 💳 /debito
# ══════════════════════════════════════════════════════════════
grupo_debito = app_commands.Group(name="debito", description="💳 Gestionar tu cuenta de débito", guild_ids=[GUILD_ID])

@grupo_debito.command(name="estado", description="Ver tu saldo bancario y tarjeta")
async def debito_estado(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    em = discord.Embed(title="💳 Estado de Cuenta Débito", color=COLOR_PRINCIPAL)
    em.add_field(name="💵 Efectivo", value=clp(user["efectivo"]), inline=True)
    em.add_field(name="🏦 Banco", value=clp(user["banco"]), inline=True)
    em.add_field(name="🇺🇸 USD Banco", value=usd(user["usd_banco"]), inline=True)
    if user["tarjeta_debito"]:
        titular = user.get("nombre_completo", interaction.user.display_name)
        em.add_field(
            name="💳 Tarjeta",
            value=f"✅ **Activa**\n`{user['tarjeta_debito']['numero']}`\nTitular: {titular}",
            inline=False
        )
    else:
        em.add_field(name="💳 Tarjeta", value="❌ Sin tarjeta\nUsa `/banco` para solicitar una.", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="depositar", description="Guardar efectivo en el banco (Efectivo → Banco)")
@app_commands.describe(monto="Monto en CLP a depositar")
async def debito_depositar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto <= 0:
        return await interaction.response.send_message("❌ El monto debe ser mayor a $0.", ephemeral=True)
    if user["efectivo"] < monto:
        return await interaction.response.send_message(f"❌ Efectivo insuficiente. Tienes **{clp(user['efectivo'])}**.", ephemeral=True)
    user["efectivo"] -= monto
    user["banco"] += monto
    agregar_xp(user, 5)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DEPÓSITO", monto, f"Depósito de {clp(monto)}")
    em = discord.Embed(
        title="✅ Depósito Exitoso",
        color=COLOR_EXITO,
        description=f"Depositaste **{clp(monto)}** en tu banco.\n🏦 Nuevo saldo banco: **{clp(user['banco'])}**"
    )
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="retirar", description="Sacar dinero del cajero (Banco → Efectivo)")
@app_commands.describe(monto="Monto en CLP a retirar")
async def debito_retirar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto <= 0:
        return await interaction.response.send_message("❌ El monto debe ser mayor a $0.", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente en banco. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    user["banco"] -= monto
    user["efectivo"] += monto
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "RETIRO", monto, f"Retiro de {clp(monto)}")
    em = discord.Embed(
        title="🏧 Retiro Exitoso",
        color=COLOR_EXITO,
        description=f"Retiraste **{clp(monto)}** del banco.\n💵 Efectivo: **{clp(user['efectivo'])}**"
    )
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="transferir", description="Transferir dinero a otro usuario (Banco → Banco)")
@app_commands.describe(usuario="Usuario a quien transferir", monto="Monto en CLP")
async def debito_transferir(interaction: discord.Interaction, usuario: discord.Member, monto: int):
    if usuario.id == interaction.user.id:
        return await interaction.response.send_message("❌ No puedes transferirte a ti mismo.", ephemeral=True)
    if usuario.bot:
        return await interaction.response.send_message("❌ No puedes transferir a un bot.", ephemeral=True)
    if monto <= 0:
        return await interaction.response.send_message("❌ El monto debe ser mayor a $0.", ephemeral=True)
    user = get_user(interaction.user.id)
    if not user["tarjeta_debito"]:
        return await interaction.response.send_message("❌ Necesitas una **tarjeta de débito** para transferir.", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    receptor = get_user(usuario.id)
    user["banco"] -= monto
    receptor["banco"] += monto
    agregar_xp(user, 10)
    save_user(interaction.user.id, user)
    save_user(usuario.id, receptor)
    add_historial(interaction.user.id, "TRANSFERENCIA", -monto, f"Transferencia a {usuario.display_name}")
    add_historial(usuario.id, "TRANSFERENCIA", monto, f"Transferencia de {interaction.user.display_name}")
    em = discord.Embed(
        title="➡️ Transferencia Exitosa",
        color=COLOR_EXITO,
        description=f"Transferiste **{clp(monto)}** a **{usuario.display_name}**\n🏦 Tu saldo: **{clp(user['banco'])}**"
    )
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

bot.tree.add_command(grupo_debito)

# ══════════════════════════════════════════════════════════════
# 💰 /ahorro
# ══════════════════════════════════════════════════════════════
grupo_ahorro = app_commands.Group(name="ahorro", description="💰 Gestionar tus cuentas de ahorro", guild_ids=[GUILD_ID])
TASA_AHORRO = 0.03

@grupo_ahorro.command(name="abrir", description="Abrir una cuenta de ahorro")
@app_commands.describe(monto="Monto inicial en CLP (mínimo $10.000)")
async def ahorro_abrir(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto < 10_000:
        return await interaction.response.send_message("❌ El monto mínimo es **$10.000 CLP**.", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}** en banco.", ephemeral=True)
    if len(user["cuentas_ahorro"]) >= 3:
        return await interaction.response.send_message("❌ Máximo **3 cuentas de ahorro** permitidas.", ephemeral=True)
    user["banco"] -= monto
    user["cuentas_ahorro"].append({
        "id": int(datetime.now().timestamp()),
        "saldo": monto,
        "apertura": datetime.now().strftime("%d/%m/%Y")
    })
    agregar_xp(user, 20)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_ABRIR", monto, f"Cuenta de ahorro abierta con {clp(monto)}")
    em = discord.Embed(
        title="✅ Cuenta de Ahorro Abierta",
        color=COLOR_EXITO,
        description=f"Depositaste **{clp(monto)}** en tu nueva cuenta de ahorro.\n📈 Tasa: **{int(TASA_AHORRO*100)}% semanal**"
    )
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="ver", description="Ver tus cuentas de ahorro")
async def ahorro_ver(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]:
        return await interaction.response.send_message("❌ No tienes cuentas de ahorro. Usa `/ahorro abrir`.", ephemeral=True)
    em = discord.Embed(title="💰 Mis Cuentas de Ahorro", color=COLOR_PRINCIPAL)
    total = 0
    for i, c in enumerate(user["cuentas_ahorro"], 1):
        em.add_field(name=f"💰 Cuenta #{i}", value=f"Saldo: **{clp(c['saldo'])}**\nAbierta: {c['apertura']}", inline=True)
        total += c["saldo"]
    em.add_field(name="📊 Total en ahorro", value=f"**{clp(total)}**", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="depositar", description="Depositar en tu cuenta de ahorro")
@app_commands.describe(monto="Monto en CLP")
async def ahorro_depositar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]:
        return await interaction.response.send_message("❌ No tienes cuentas de ahorro.", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    user["banco"] -= monto
    user["cuentas_ahorro"][0]["saldo"] += monto
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_DEPÓSITO", monto, f"Depósito en ahorro {clp(monto)}")
    em = discord.Embed(
        title="✅ Depósito en Ahorro",
        color=COLOR_EXITO,
        description=f"Depositaste **{clp(monto)}**.\nNuevo saldo: **{clp(user['cuentas_ahorro'][0]['saldo'])}**"
    )
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="retirar", description="Retirar de tu cuenta de ahorro")
@app_commands.describe(monto="Monto en CLP")
async def ahorro_retirar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]:
        return await interaction.response.send_message("❌ No tienes cuentas de ahorro.", ephemeral=True)
    if user["cuentas_ahorro"][0]["saldo"] < monto:
        return await interaction.response.send_message(
            f"❌ Saldo insuficiente en ahorro. Tienes **{clp(user['cuentas_ahorro'][0]['saldo'])}**.", ephemeral=True
        )
    user["cuentas_ahorro"][0]["saldo"] -= monto
    user["banco"] += monto
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_RETIRO", monto, f"Retiro de ahorro {clp(monto)}")
    em = discord.Embed(
        title="✅ Retiro de Ahorro",
        color=COLOR_EXITO,
        description=f"Retiraste **{clp(monto)}** de tu ahorro al banco."
    )
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="cerrar", description="Cerrar tu cuenta de ahorro (retira todo el saldo)")
async def ahorro_cerrar(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]:
        return await interaction.response.send_message("❌ No tienes cuentas de ahorro.", ephemeral=True)
    cuenta = user["cuentas_ahorro"].pop(0)
    user["banco"] += cuenta["saldo"]
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_CERRAR", cuenta["saldo"], "Cuenta de ahorro cerrada")
    em = discord.Embed(
        title="⚠️ Cuenta de Ahorro Cerrada",
        color=COLOR_ADVERTENCIA,
        description=f"Se devolvieron **{clp(cuenta['saldo'])}** a tu banco."
    )
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="calcular", description="Calcular rendimiento de un ahorro")
@app_commands.describe(monto="Monto inicial en CLP", semanas="Número de semanas (1-52)")
async def ahorro_calcular(interaction: discord.Interaction, monto: int, semanas: int):
    semanas = max(1, min(52, semanas))
    acumulado = monto * ((1 + TASA_AHORRO) ** semanas)
    ganancia = acumulado - monto
    em = discord.Embed(title="📊 Calculadora de Ahorro", color=COLOR_INFO)
    em.add_field(name="💵 Monto inicial", value=clp(monto), inline=True)
    em.add_field(name="📅 Semanas", value=str(semanas), inline=True)
    em.add_field(name="📈 Tasa semanal", value=f"{int(TASA_AHORRO*100)}%", inline=True)
    em.add_field(name="💰 Ganancia estimada", value=clp(int(ganancia)), inline=True)
    em.add_field(name="🏆 Total estimado", value=clp(int(acumulado)), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

bot.tree.add_command(grupo_ahorro)

# ══════════════════════════════════════════════════════════════
# 📋 /prestamo
# ══════════════════════════════════════════════════════════════
grupo_prestamo = app_commands.Group(name="prestamo", description="📋 Gestionar préstamos", guild_ids=[GUILD_ID])

@grupo_prestamo.command(name="ver", description="Ver tus préstamos activos")
async def prestamo_ver(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    if not user["prestamos"]:
        return await interaction.response.send_message("✅ No tienes préstamos activos.", ephemeral=True)
    em = discord.Embed(title="📋 Mis Préstamos Activos", color=COLOR_ADVERTENCIA)
    for i, p in enumerate(user["prestamos"], 1):
        motivo_corto = p['motivo'][:40]
        em.add_field(
            name=f"Préstamo #{i}",
            value=(
                f"Total: **{clp(p['total'])}**\n"
                f"Cuota: **{clp(p['cuota'])}**\n"
                f"Semanas restantes: **{p['semanas_restantes']}**\n"
                f"Motivo: *{motivo_corto}*"
            ),
            inline=True
        )
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_prestamo.command(name="pagar", description="Realizar un pago a tu préstamo")
@app_commands.describe(monto="Monto en CLP a pagar")
async def prestamo_pagar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if not user["prestamos"]:
        return await interaction.response.send_message("✅ No tienes préstamos activos.", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    user["banco"] -= monto
    restante = monto
    nuevos = []
    for p in user["prestamos"]:
        if restante <= 0:
            nuevos.append(p)
            continue
        pago = min(restante, p["total"])
        p["total"] -= pago
        restante -= pago
        if p["total"] > 0:
            nuevos.append(p)
    user["prestamos"] = nuevos
    agregar_xp(user, 15)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "PRÉSTAMO_PAGO", -monto, f"Pago préstamo {clp(monto)}")
    em = discord.Embed(
        title="✅ Pago Realizado",
        color=COLOR_EXITO,
        description=f"Pagaste **{clp(monto)}** de tu préstamo.\nPréstamos restantes: **{len(user['prestamos'])}**"
    )
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_prestamo.command(name="calcular", description="Calcular cuotas de un préstamo")
@app_commands.describe(monto="Monto solicitado en CLP", semanas="1, 2 o 3 semanas")
async def prestamo_calcular(interaction: discord.Interaction, monto: int, semanas: int):
    semanas = max(1, min(3, semanas))
    tasas = {1: 0.05, 2: 0.10, 3: 0.15}
    interes = tasas[semanas]
    total = int(monto * (1 + interes))
    cuota = total // semanas
    em = discord.Embed(title="🧮 Calculadora de Préstamo", color=COLOR_INFO)
    em.add_field(name="💵 Monto", value=clp(monto), inline=True)
    em.add_field(name="📅 Plazo", value=f"{semanas} semana(s)", inline=True)
    em.add_field(name="📈 Interés", value=f"{int(interes*100)}%", inline=True)
    em.add_field(name="💰 Total a pagar", value=clp(total), inline=True)
    em.add_field(name="📋 Cuota semanal", value=clp(cuota), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_prestamo.command(name="ayuda", description="Información sobre cómo solicitar un préstamo")
async def prestamo_ayuda(interaction: discord.Interaction):
    em = discord.Embed(
        title="ℹ️ Información de Préstamos",
        color=COLOR_INFO,
        description="Para solicitar un préstamo usa **/banco** y selecciona **Solicitar Préstamo**."
    )
    em.add_field(name="📈 Tasas de interés", value="• 1 semana: **5%**\n• 2 semanas: **10%**\n• 3 semanas: **15%**", inline=False)
    em.add_field(name="📋 Requisitos", value="• Tener tarjeta de débito activa\n• Monto mínimo: **$10.000 CLP**", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

bot.tree.add_command(grupo_prestamo)

# ══════════════════════════════════════════════════════════════
# 🪙 /cripto
# ══════════════════════════════════════════════════════════════
grupo_cripto = app_commands.Group(name="cripto", description="🪙 Mercado de criptomonedas", guild_ids=[GUILD_ID])

@grupo_cripto.command(name="mercado", description="Ver el precio actual de las criptomonedas")
async def cripto_mercado(interaction: discord.Interaction):
    db = cargar_db()
    precios = get_precios_cripto(db)
    em = discord.Embed(
        title="🪙 Mercado Cripto — Gran Chile RP",
        color=COLOR_CRIPTO,
        description="Precios actuales en **CLP 🇨🇱**"
    )
    iconos = {"BTC": "₿", "ETH": "⟠", "SOL": "◎", "DOGE": "🐶", "ADA": "🔵"}
    for k, v in precios.items():
        em.add_field(name=f"{iconos.get(k, '🪙')} {k}", value=clp(v), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Precios actualizados cada hora")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

@grupo_cripto.command(name="comprar", description="Comprar criptomonedas (precio al momento de la compra)")
@app_commands.describe(moneda="BTC, ETH, SOL, DOGE o ADA", monto="Monto en CLP a invertir")
async def cripto_comprar(interaction: discord.Interaction, moneda: str, monto: int):
    moneda = moneda.upper()
    db = cargar_db()
    precios = get_precios_cripto(db)
    if moneda not in precios:
        opciones = ", ".join(precios.keys())
        return await interaction.response.send_message(f"❌ Moneda no disponible. Opciones: **{opciones}**", ephemeral=True)
    user = get_user(interaction.user.id)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    cantidad = monto / precios[moneda]
    user["banco"] -= monto
    user["cripto"][moneda] = user["cripto"].get(moneda, 0) + cantidad
    agregar_xp(user, 10)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "CRIPTO_COMPRA", monto, f"Compra {cantidad:.6f} {moneda}")
    em = discord.Embed(title="✅ Compra Cripto Exitosa", color=COLOR_EXITO)
    em.add_field(name="🪙 Moneda", value=moneda, inline=True)
    em.add_field(name="💰 Invertido", value=clp(monto), inline=True)
    em.add_field(name="📦 Cantidad", value=f"{cantidad:.6f} {moneda}", inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_cripto.command(name="vender", description="Vender criptomonedas (precio al momento de la venta)")
@app_commands.describe(moneda="BTC, ETH, SOL, DOGE o ADA", cantidad="Cantidad a vender")
async def cripto_vender(interaction: discord.Interaction, moneda: str, cantidad: float):
    moneda = moneda.upper()
    db = cargar_db()
    precios = get_precios_cripto(db)
    user = get_user(interaction.user.id)
    if moneda not in precios:
        return await interaction.response.send_message("❌ Moneda no encontrada.", ephemeral=True)
    if user["cripto"].get(moneda, 0) < cantidad:
        return await interaction.response.send_message(f"❌ No tienes suficiente **{moneda}**.", ephemeral=True)
    ganancia = int(cantidad * precios[moneda])
    user["cripto"][moneda] -= cantidad
    user["banco"] += ganancia
    agregar_xp(user, 10)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "CRIPTO_VENTA", ganancia, f"Venta {cantidad:.6f} {moneda}")
    em = discord.Embed(title="✅ Venta Cripto Exitosa", color=COLOR_EXITO)
    em.add_field(name="🪙 Moneda", value=moneda, inline=True)
    em.add_field(name="📦 Vendido", value=f"{cantidad:.6f} {moneda}", inline=True)
    em.add_field(name="💰 Recibido", value=clp(ganancia), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_cripto.command(name="portafolio", description="Ver tus billeteras cripto")
async def cripto_portafolio(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    db = cargar_db()
    precios = get_precios_cripto(db)
    entradas = [(k, v) for k, v in user.get("cripto", {}).items() if v > 0]
    em = discord.Embed(title="💼 Mi Portafolio Cripto", color=COLOR_CRIPTO)
    if not entradas:
        em.description = "*Sin criptomonedas. Usa `/cripto comprar` para invertir.*"
    else:
        total = 0
        for k, v in entradas:
            val = int(v * precios.get(k, 0))
            total += val
            em.add_field(name=f"🪙 {k}", value=f"Cant: **{v:.6f}**\nValor: **{clp(val)}**", inline=True)
        em.add_field(name="📊 Valor Total", value=f"**{clp(total)}**", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_cripto.command(name="grafica", description="Generar el gráfico de precio histórico")
@app_commands.describe(moneda="BTC, ETH, SOL, DOGE o ADA")
async def cripto_grafica(interaction: discord.Interaction, moneda: str):
    moneda = moneda.upper()
    db = cargar_db()
    precios = get_precios_cripto(db)
    if moneda not in precios:
        return await interaction.response.send_message("❌ Moneda no encontrada.", ephemeral=True)
    base = precios[moneda]
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Hoy"]
    puntos = [int(base * (1 + random.uniform(-0.08, 0.08))) for _ in range(7)]
    grafica = "\n".join(f"`{dias[i]}` → **{clp(p)}**" for i, p in enumerate(puntos))
    tendencia = "📈" if puntos[-1] >= puntos[0] else "📉"
    variacion = ((puntos[-1] - puntos[0]) / puntos[0]) * 100
    em = discord.Embed(
        title=f"📊 {tendencia} {moneda} — Últimos 7 días",
        color=COLOR_CRIPTO,
        description=grafica
    )
    em.add_field(name="Variación semanal", value=f"{variacion:+.2f}%", inline=True)
    em.add_field(name="Precio actual", value=clp(precios[moneda]), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Datos simulados")
    await interaction.response.send_message(embed=em, ephemeral=True)

bot.tree.add_command(grupo_cripto)

# ══════════════════════════════════════════════════════════════
# 📈 /bolsa
# ══════════════════════════════════════════════════════════════
grupo_bolsa = app_commands.Group(name="bolsa", description="📈 Mercado de valores", guild_ids=[GUILD_ID])

@grupo_bolsa.command(name="ver", description="Ver el mercado de valores actual")
async def bolsa_ver(interaction: discord.Interaction):
    db = cargar_db()
    precios = get_precios_acciones(db)
    em = discord.Embed(
        title="📈 Bolsa de Valores — Gran Chile RP",
        color=0x00A650,
        description="Acciones chilenas disponibles (precio por acción en CLP)"
    )
    for k, v in precios.items():
        em.add_field(name=f"🏢 {k}", value=clp(v), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Precios actualizados cada hora")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

@grupo_bolsa.command(name="comprar", description="Comprar acciones")
@app_commands.describe(empresa="COPEC, FALABELLA, BCI, CMPC, ENTEL, LATAM, CENCOSUD", cantidad="Número de acciones")
async def bolsa_comprar(interaction: discord.Interaction, empresa: str, cantidad: int):
    empresa = empresa.upper()
    db = cargar_db()
    precios = get_precios_acciones(db)
    if empresa not in precios:
        opciones = ", ".join(precios.keys())
        return await interaction.response.send_message(f"❌ Empresa no encontrada. Opciones: **{opciones}**", ephemeral=True)
    user = get_user(interaction.user.id)
    costo = precios[empresa] * cantidad
    if user["banco"] < costo:
        return await interaction.response.send_message(
            f"❌ Necesitas **{clp(costo)}**. Tienes **{clp(user['banco'])}**.", ephemeral=True
        )
    user["banco"] -= costo
    user["acciones"][empresa] = user["acciones"].get(empresa, 0) + cantidad
    agregar_xp(user, 15)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "BOLSA_COMPRA", costo, f"Compra {cantidad} acciones {empresa}")
    em = discord.Embed(title="✅ Acciones Compradas", color=COLOR_EXITO)
    em.add_field(name="🏢 Empresa", value=empresa, inline=True)
    em.add_field(name="📦 Cantidad", value=f"{cantidad} acciones", inline=True)
    em.add_field(name="💰 Pagado", value=clp(costo), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_bolsa.command(name="vender", description="Vender acciones")
@app_commands.describe(empresa="Empresa", cantidad="Número de acciones a vender")
async def bolsa_vender(interaction: discord.Interaction, empresa: str, cantidad: int):
    empresa = empresa.upper()
    db = cargar_db()
    precios = get_precios_acciones(db)
    user = get_user(interaction.user.id)
    if user["acciones"].get(empresa, 0) < cantidad:
        return await interaction.response.send_message(
            f"❌ No tienes suficientes acciones de **{empresa}**.", ephemeral=True
        )
    precio_venta = int(precios.get(empresa, 0) * cantidad * random.uniform(0.95, 1.05))
    user["acciones"][empresa] -= cantidad
    user["banco"] += precio_venta
    agregar_xp(user, 15)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "BOLSA_VENTA", precio_venta, f"Venta {cantidad} acciones {empresa}")
    em = discord.Embed(title="✅ Acciones Vendidas", color=COLOR_EXITO)
    em.add_field(name="🏢 Empresa", value=empresa, inline=True)
    em.add_field(name="📦 Cantidad", value=f"{cantidad} acciones", inline=True)
    em.add_field(name="💰 Recibido", value=clp(precio_venta), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_bolsa.command(name="portafolio", description="Ver tus inversiones en bolsa")
async def bolsa_portafolio(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    db = cargar_db()
    precios = get_precios_acciones(db)
    entradas = [(k, v) for k, v in user.get("acciones", {}).items() if v > 0]
    em = discord.Embed(title="💼 Mi Portafolio Bolsa", color=0x00A650)
    if not entradas:
        em.description = "*Sin inversiones. Usa `/bolsa comprar` para invertir.*"
    else:
        total = 0
        for k, v in entradas:
            val = int(v * precios.get(k, 0))
            total += val
            em.add_field(name=f"🏢 {k}", value=f"Acciones: **{v}**\nValor: **{clp(val)}**", inline=True)
        em.add_field(name="📊 Valor Total", value=f"**{clp(total)}**", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

bot.tree.add_command(grupo_bolsa)

# ══════════════════════════════════════════════════════════════
# ₿ /bitcoin precio
# ══════════════════════════════════════════════════════════════
grupo_bitcoin = app_commands.Group(name="bitcoin", description="₿ Bitcoin", guild_ids=[GUILD_ID])

@grupo_bitcoin.command(name="precio", description="Ver el precio actual de Bitcoin y el estado de la red")
async def bitcoin_precio(interaction: discord.Interaction):
    db = cargar_db()
    precios = get_precios_cripto(db)
    variacion = random.uniform(-8, 8)
    em = discord.Embed(title="₿ Bitcoin — Precio Actual", color=COLOR_CRIPTO)
    em.add_field(name="💰 Precio CLP", value=clp(precios["BTC"]), inline=True)
    em.add_field(name="📈 Variación 24h", value=f"{variacion:+.2f}%", inline=True)
    em.add_field(name="🌐 Estado de Red", value="🟢 Operacional", inline=True)
    em.add_field(name="⛏️ Dificultad", value="Alta", inline=True)
    em.add_field(name="📦 Bloque actual", value=f"#{random.randint(800000, 850000):,}", inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

bot.tree.add_command(grupo_bitcoin)

# ══════════════════════════════════════════════════════════════
# 💼 /colectar
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="colectar", description="💼 Colectar tu salario (cada 72 horas)")
async def colectar(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    ahora = datetime.now()
    espera = timedelta(hours=72)
    if user["ultimo_colectar"]:
        ultimo = datetime.fromisoformat(user["ultimo_colectar"])
        if ahora - ultimo < espera:
            restante = espera - (ahora - ultimo)
            h, rem = divmod(int(restante.total_seconds()), 3600)
            m = rem // 60
            em = discord.Embed(
                title="⏳ Aún no puedes colectar",
                color=COLOR_ERROR,
                description=f"Podrás colectar en **{h}h {m}m**"
            )
            return await interaction.response.send_message(embed=em, ephemeral=True)
    salario = random.randint(75_000, 100_000)
    user["efectivo"] += salario
    user["ultimo_colectar"] = ahora.isoformat()
    user["rachas"] = user.get("rachas", 0) + 1
    nivel, subio = agregar_xp(user, 25)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "SALARIO", salario, f"Salario cobrado {clp(salario)}")
    desc = f"Recibiste **{clp(salario)}** en efectivo.\n🔥 Racha: **{user['rachas']} días**"
    if subio:
        desc += f"\n⭐ **¡Subiste al nivel {nivel}!**"
    em = discord.Embed(title="💼 ¡Salario Cobrado!", color=COLOR_EXITO, description=desc)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 🎁 /diario
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="diario", description="🎁 Reclamar tu recompensa diaria")
async def diario(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    ahora = datetime.now()
    espera = timedelta(hours=24)
    if user["ultimo_diario"]:
        ultimo = datetime.fromisoformat(user["ultimo_diario"])
        if ahora - ultimo < espera:
            restante = espera - (ahora - ultimo)
            h, rem = divmod(int(restante.total_seconds()), 3600)
            m = rem // 60
            em = discord.Embed(
                title="⏳ Ya reclamaste hoy",
                color=COLOR_ERROR,
                description=f"Vuelve en **{h}h {m}m**"
            )
            return await interaction.response.send_message(embed=em, ephemeral=True)
    recompensa = random.randint(20_000, 50_000)
    user["efectivo"] += recompensa
    user["ultimo_diario"] = ahora.isoformat()
    agregar_xp(user, 10)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DIARIO", recompensa, f"Recompensa diaria {clp(recompensa)}")
    em = discord.Embed(
        title="🎁 ¡Recompensa Diaria!",
        color=COLOR_EXITO,
        description=f"Recibiste **{clp(recompensa)}** en efectivo."
    )
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 💼 /trabajo
# ══════════════════════════════════════════════════════════════
TRABAJOS = [
    ("🚕 Taxista",        15_000, 30_000),
    ("🚚 Repartidor",     20_000, 40_000),
    ("👷 Construcción",   25_000, 45_000),
    ("🏪 Cajero",         18_000, 35_000),
    ("💻 Programador",    35_000, 70_000),
    ("🩺 Médico",         50_000, 90_000),
    ("⚖️ Abogado",        45_000, 80_000),
    ("🚔 Policía",        30_000, 55_000),
]

@bot.tree.command(guild=guild_obj, name="trabajo", description="💼 Trabajar para ganar dinero (cada 4 horas)")
async def trabajo(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    ahora = datetime.now()
    espera = timedelta(hours=4)
    if user.get("ultimo_trabajo"):
        ultimo = datetime.fromisoformat(user["ultimo_trabajo"])
        if ahora - ultimo < espera:
            restante = espera - (ahora - ultimo)
            h, rem = divmod(int(restante.total_seconds()), 3600)
            m = rem // 60
            em = discord.Embed(
                title="⏳ Aún estás descansando",
                color=COLOR_ERROR,
                description=f"Podrás trabajar en **{h}h {m}m**"
            )
            return await interaction.response.send_message(embed=em, ephemeral=True)
    trabajo_elegido = random.choice(TRABAJOS)
    nombre, minimo, maximo = trabajo_elegido
    ganancia = random.randint(minimo, maximo)
    user["efectivo"] += ganancia
    user["ultimo_trabajo"] = ahora.isoformat()
    agregar_xp(user, 20)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "TRABAJO", ganancia, f"Trabajo: {nombre} → {clp(ganancia)}")
    em = discord.Embed(
        title="💼 ¡Turno Completado!",
        color=COLOR_EXITO,
        description=f"Trabajaste como **{nombre}** y ganaste **{clp(ganancia)}**."
    )
    em.set_footer(text="🏦 Banco Alianza Santander | Próximo trabajo en 4 horas")
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 🔫 /crimen
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="crimen", description="🔫 Cometer un crimen de alto riesgo para ganar dinero sucio")
async def crimen(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    ahora = datetime.now()
    espera = timedelta(hours=6)
    if user["ultimo_crimen"]:
        ultimo = datetime.fromisoformat(user["ultimo_crimen"])
        if ahora - ultimo < espera:
            restante = espera - (ahora - ultimo)
            h, rem = divmod(int(restante.total_seconds()), 3600)
            m = rem // 60
            em = discord.Embed(
                title="🚔 La Policía te vigila",
                color=COLOR_ERROR,
                description=f"Espera **{h}h {m}m** antes de intentar otro crimen."
            )
            return await interaction.response.send_message(embed=em, ephemeral=True)
    user["ultimo_crimen"] = ahora.isoformat()
    crimen_elegido = random.choice(CRIMENES)
    exito = random.random() < 0.60
    if exito:
        ganancia = random.randint(50_000, 200_000)
        user["efectivo"] += ganancia
        agregar_xp(user, 30)
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "CRIMEN", ganancia, f"Crimen exitoso: {crimen_elegido}")
        em = discord.Embed(
            title="🔫 ¡Crimen Exitoso!",
            color=0x2ECC71,
            description=f"**{crimen_elegido}**\n\nLograste escapar con **{clp(ganancia)}** en efectivo.\n⚠️ *Cuidado, la Policía te busca...*"
        )
    else:
        multa = random.randint(30_000, 80_000)
        user["efectivo"] = max(0, user["efectivo"] - multa)
        user["penales"] = user.get("penales", 0) + 1
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "CRIMEN_FALLO", -multa, f"Arrestado: {crimen_elegido}")
        em = discord.Embed(
            title="🚔 ¡Arrestado!",
            color=COLOR_ERROR,
            description=f"**{crimen_elegido}**\n\nFuiste capturado y multado con **{clp(multa)}**.\n📋 Penales acumulados: **{user['penales']}**"
        )
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 💱 /divisa
# ══════════════════════════════════════════════════════════════
grupo_divisa = app_commands.Group(name="divisa", description="💱 Cambio de divisas", guild_ids=[GUILD_ID])

@grupo_divisa.command(name="clp_a_usd", description="Convertir Pesos Chilenos a Dólares (CLP → USD)")
@app_commands.describe(monto="Monto en CLP a convertir")
async def divisa_clp_usd(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    resultado = round(monto / TASA_CAMBIO, 2)
    user["banco"] -= monto
    user["usd_banco"] += resultado
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DIVISA", monto, f"Cambio {clp(monto)} → {usd(resultado)}")
    em = discord.Embed(title="💱 Cambio de Divisa Exitoso", color=COLOR_EXITO)
    em.add_field(name="🇨🇱 Entregaste", value=clp(monto), inline=True)
    em.add_field(name="🇺🇸 Recibiste", value=usd(resultado), inline=True)
    em.add_field(name="📈 Tasa aplicada", value=f"1 USD = {clp(TASA_CAMBIO)}", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_divisa.command(name="usd_a_clp", description="Convertir Dólares a Pesos Chilenos (USD → CLP)")
@app_commands.describe(monto="Monto en USD a convertir")
async def divisa_usd_clp(interaction: discord.Interaction, monto: float):
    user = get_user(interaction.user.id)
    if user["usd_banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo USD insuficiente. Tienes **{usd(user['usd_banco'])}**.", ephemeral=True)
    resultado = int(monto * TASA_CAMBIO)
    user["usd_banco"] -= monto
    user["banco"] += resultado
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DIVISA", resultado, f"Cambio {usd(monto)} → {clp(resultado)}")
    em = discord.Embed(title="💱 Cambio de Divisa Exitoso", color=COLOR_EXITO)
    em.add_field(name="🇺🇸 Entregaste", value=usd(monto), inline=True)
    em.add_field(name="🇨🇱 Recibiste", value=clp(resultado), inline=True)
    em.add_field(name="📈 Tasa aplicada", value=f"1 USD = {clp(TASA_CAMBIO)}", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_divisa.command(name="tasa", description="Ver la tasa de cambio actual")
async def divisa_tasa(interaction: discord.Interaction):
    variacion = random.uniform(-2, 2)
    em = discord.Embed(title="💱 Tasa de Cambio — Banco Alianza Santander", color=COLOR_INFO)
    em.add_field(name="🇨🇱 CLP → USD", value=f"$1.000 CLP = {usd(1000/TASA_CAMBIO)}", inline=True)
    em.add_field(name="🇺🇸 USD → CLP", value=f"$1 USD = {clp(TASA_CAMBIO)}", inline=True)
    em.add_field(name="📊 Variación del día", value=f"{variacion:+.2f}%", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

bot.tree.add_command(grupo_divisa)

# ══════════════════════════════════════════════════════════════
# 📊 /historial
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="historial", description="📊 Ver tus últimos movimientos financieros")
async def historial(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    movimientos = user.get("historial", [])[:10]
    em = discord.Embed(title="📊 Historial de Movimientos", color=COLOR_PRINCIPAL)
    if not movimientos:
        em.description = "*Sin movimientos registrados.*"
    else:
        texto = "\n".join(
            f"`{m['fecha']}` **{m['tipo']}** — {m['descripcion']}"
            for m in movimientos
        )
        em.description = texto
    em.set_footer(text="🏦 Banco Alianza Santander | Últimos 10 movimientos")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🔥 /rachas
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="rachas", description="🔥 Ver tu racha de días consecutivos")
async def rachas(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    racha = user.get("rachas", 0)
    if racha >= 30:
        titulo = "🏆 ¡Leyenda del Banco!"
    elif racha >= 14:
        titulo = "🔥 ¡Racha Épica!"
    elif racha >= 7:
        titulo = "⭐ ¡Racha de Semana!"
    else:
        titulo = "💪 ¡Sigue así!"
    em = discord.Embed(
        title=f"🔥 {titulo}",
        color=COLOR_ADVERTENCIA,
        description=f"Llevas **{racha}** días consecutivos colectando."
    )
    em.add_field(name="⭐ Nivel", value=str(user.get("nivel", 1)), inline=True)
    em.add_field(name="🎯 XP Total", value=str(user.get("experiencia", 0)), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🚔 /penales
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="penales", description="🚔 Ver tus penales acumulados (x1.5)")
async def penales(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    p = user.get("penales", 0)
    tanda = int(p * 1.5)
    nivel_peligro = "🟢 Limpio" if p == 0 else "🟡 Vigilado" if p < 3 else "🔴 Buscado"
    em = discord.Embed(title="🚔 Mis Penales", color=COLOR_ERROR)
    em.add_field(name="📋 Penales acumulados", value=str(p), inline=True)
    em.add_field(name="⚖️ Tanda (x1.5)", value=str(tanda), inline=True)
    em.add_field(name="🚨 Estado", value=nivel_peligro, inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🏧 /cajero
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="cajero", description="🏧 Abrir el Cajero Automático (ATM)")
async def cajero(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    em = discord.Embed(
        title="🏧 Cajero Automático — Banco Alianza Santander",
        color=COLOR_PRINCIPAL,
        description="Usa los comandos de débito para operar:"
    )
    em.add_field(name="💵 Efectivo disponible", value=clp(user["efectivo"]), inline=True)
    em.add_field(name="🏦 Saldo en banco", value=clp(user["banco"]), inline=True)
    em.add_field(
        name="📋 Operaciones",
        value=(
            "• `/debito depositar` — Depositar efectivo\n"
            "• `/debito retirar` — Retirar al efectivo\n"
            "• `/debito transferir` — Transferir a otro usuario\n"
            "• `/debito estado` — Ver estado completo"
        ),
        inline=False
    )
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🏆 /top — Ranking del servidor
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="top", description="🏆 Ver el ranking de los más ricos del servidor")
async def top(interaction: discord.Interaction):
    db = cargar_db()
    usuarios = []
    for uid, data in db["users"].items():
        total = data.get("efectivo", 0) + data.get("banco", 0)
        nombre = data.get("nombre_completo", f"Usuario {uid[:4]}")
        usuarios.append((uid, total, nombre))
    usuarios.sort(key=lambda x: x[1], reverse=True)
    top10 = usuarios[:10]
    medallas = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    em = discord.Embed(title="🏆 Ranking — Los más ricos de Gran Chile RP", color=COLOR_ADVERTENCIA)
    desc = ""
    for i, (uid, total, nombre) in enumerate(top10):
        desc += f"{medallas[i]} **#{i+1}** {nombre or 'Desconocido'} — **{clp(total)}**\n"
    em.description = desc or "*Sin datos*"
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 🎰 /invertir — Inversión de riesgo rápida
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="invertir", description="🎰 Hacer una inversión de riesgo (puedes ganar o perder)")
@app_commands.describe(monto="Monto en CLP a arriesgar")
async def invertir(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto < 5_000:
        return await interaction.response.send_message("❌ Monto mínimo para invertir: **$5.000 CLP**", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    resultado = random.random()
    if resultado < 0.10:
        ganancia = int(monto * 3.0)
        msg = f"💎 **¡JACKPOT!** Triplicaste tu inversión.\nGanaste **{clp(ganancia)}**"
        color = COLOR_PREMIUM
    elif resultado < 0.40:
        ganancia = int(monto * 1.5)
        msg = f"📈 ¡Buena inversión! Ganaste **{clp(ganancia - monto)}** extra."
        color = COLOR_EXITO
    elif resultado < 0.65:
        ganancia = int(monto * 0.8)
        msg = f"📉 Mala racha. Perdiste **{clp(monto - ganancia)}**."
        color = COLOR_ERROR
    else:
        ganancia = 0
        msg = "💥 **¡Perdiste todo!** La inversión fracasó completamente."
        color = COLOR_ERROR
    user["banco"] = user["banco"] - monto + ganancia
    agregar_xp(user, 5)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "INVERSIÓN", ganancia - monto, f"Inversión {clp(monto)} → {clp(ganancia)}")
    em = discord.Embed(title="🎰 Resultado de Inversión", color=color, description=msg)
    em.add_field(name="💵 Invertido", value=clp(monto), inline=True)
    em.add_field(name="💰 Resultado", value=clp(ganancia), inline=True)
    em.add_field(name="🏦 Nuevo saldo banco", value=clp(user["banco"]), inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 🏦 /banco — Menú principal con botones (ModalView)
# ══════════════════════════════════════════════════════════════

class ModalDebitoView(discord.ui.Modal, title="💳 Solicitar Tarjeta de Débito"):
    nombre = discord.ui.TextInput(label="Nombre Completo", placeholder="Ej: Juan Patricio González Soto")
    ocupacion = discord.ui.TextInput(label="Ocupación", placeholder="Ej: Policía, Mecánico, Comerciante...")

    async def on_submit(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)
        if user["tarjeta_debito"]:
            return await interaction.response.send_message("❌ Ya tienes una tarjeta de débito activa.", ephemeral=True)
        user["nombre_completo"] = str(self.nombre)
        user["ocupacion"] = str(self.ocupacion)
        user["registrado"] = True
        user["tarjeta_debito"] = {
            "numero": generar_numero_tarjeta(),
            "fecha_emision": datetime.now().strftime("%d/%m/%Y"),
            "activa": True
        }
        agregar_xp(user, 50)
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "TARJETA_DÉBITO", 0, "Tarjeta de débito emitida")
        em = discord.Embed(title="✅ ¡Tarjeta de Débito Emitida!", color=COLOR_EXITO)
        em.add_field(name="👤 Titular", value=str(self.nombre), inline=True)
        em.add_field(name="💼 Ocupación", value=str(self.ocupacion), inline=True)
        em.add_field(name="💳 Número", value=f"`{user['tarjeta_debito']['numero']}`", inline=False)
        em.add_field(name="📅 Emisión", value=user["tarjeta_debito"]["fecha_emision"], inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander")
        await interaction.response.send_message(embed=em, ephemeral=True)

class ModalCreditoView(discord.ui.Modal, title="💎 Solicitar Tarjeta de Crédito"):
    ingresos = discord.ui.TextInput(label="Ingresos Mensuales (CLP)", placeholder="Ej: 500000")
    motivo = discord.ui.TextInput(
        label="Motivo de la Solicitud",
        style=discord.TextStyle.paragraph,
        placeholder="¿Para qué usarás la tarjeta de crédito?"
    )

    async def on_submit(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)
        if not user["tarjeta_debito"]:
            return await interaction.response.send_message("❌ Primero necesitas una **tarjeta de débito**.", ephemeral=True)
        if user["tarjeta_credito"]:
            tc = TIPO_TARJETA[user["tarjeta_credito"]]
            return await interaction.response.send_message(
                f"❌ Ya tienes tarjeta **{tc['emoji']} {tc['nombre']}**.", ephemeral=True
            )
        try:
            ing = int(
                str(self.ingresos)
                .replace(".", "")
                .replace(",", "")
                .replace("$", "")
                .replace(" ", "")
            )
        except Exception:
            return await interaction.response.send_message("❌ Ingresa un monto válido.", ephemeral=True)
        if ing >= 5_000_000:
            nivel = "diamante"
        elif ing >= 2_000_000:
            nivel = "platinum"
        elif ing >= 1_000_000:
            nivel = "oro"
        elif ing >= 500_000:
            nivel = "plata"
        else:
            nivel = "clasica"
        tc = TIPO_TARJETA[nivel]
        user["tarjeta_credito"] = nivel
        user["limite_credito"] = tc["limite"]
        user["ingresos"] = ing
        agregar_xp(user, 100)
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "TARJETA_CRÉDITO", 0, f"Tarjeta {tc['nombre']} emitida")
        em = discord.Embed(
            title=f"{tc['emoji']} ¡Tarjeta de Crédito {tc['nombre']} Aprobada!",
            color=tc["color"]
        )
        em.add_field(name="💳 Tipo", value=f"{tc['emoji']} {tc['nombre']}", inline=True)
        em.add_field(name="💰 Límite", value=clp(tc["limite"]), inline=True)
        em.add_field(name="💵 Ingresos declarados", value=clp(ing), inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander")
        await interaction.response.send_message(embed=em, ephemeral=True)

class ModalPrestamoView(discord.ui.Modal, title="💰 Solicitar Préstamo"):
    monto_input = discord.ui.TextInput(label="Monto Solicitado (CLP)", placeholder="Ej: 1000000")
    plazo_input = discord.ui.TextInput(label="Plazo de pago (1, 2 o 3 semanas)", placeholder="Ej: 2")
    motivo_input = discord.ui.TextInput(
        label="Motivo del Préstamo",
       style=discord.TextStyle.paragraph,
        placeholder="¿Para qué necesitas el préstamo?"
    )

    async def on_submit(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)
        try:
            monto = int(
                str(self.monto_input)
                .replace(".", "")
                .replace(",", "")
                .replace("$", "")
                .replace(" ", "")
            )
            semanas = max(1, min(3, int(str(self.plazo_input).strip())))
        except Exception:
            return await interaction.response.send_message("❌ Datos inválidos.", ephemeral=True)
        if monto < 10_000:
            return await interaction.response.send_message("❌ Monto mínimo: **$10.000 CLP**.", ephemeral=True)
        tasas = {1: 0.05, 2: 0.10, 3: 0.15}
        interes = tasas[semanas]
        total = int(monto * (1 + interes))
        cuota = total // semanas
        user["prestamos"].append({
            "id": int(datetime.now().timestamp()),
            "monto": monto,
            "total": total,
            "cuota": cuota,
            "semanas": semanas,
            "semanas_restantes": semanas,
            "motivo": str(self.motivo_input)
        })
        user["banco"] += monto
        agregar_xp(user, 20)
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "PRÉSTAMO", monto, f"Préstamo {clp(monto)} a {semanas} semana(s)")
        em = discord.Embed(
            title="✅ ¡Préstamo Aprobado!",
            color=COLOR_EXITO,
            description="El monto ha sido depositado en tu cuenta bancaria."
        )
        em.add_field(name="💵 Monto recibido", value=clp(monto), inline=True)
        em.add_field(name="📅 Plazo", value=f"{semanas} semana(s)", inline=True)
        em.add_field(name="📈 Interés", value=f"{int(interes*100)}%", inline=True)
        em.add_field(name="💰 Total a pagar", value=clp(total), inline=True)
        em.add_field(name="📋 Cuota semanal", value=clp(cuota), inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander | Usa /prestamo ver para gestionar")
        await interaction.response.send_message(embed=em, ephemeral=True)

class BancoMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.select(placeholder="🏦 Selecciona un servicio bancario", options=[
        discord.SelectOption(label="Solicitar Tarjeta de Débito",  value="debito",   emoji="💳", description="Tarjeta de débito en CLP"),
        discord.SelectOption(label="Solicitar Tarjeta de Crédito", value="credito",  emoji="💎", description="Tarjeta con línea de crédito"),
        discord.SelectOption(label="Solicitar Préstamo",           value="prestamo", emoji="💰", description="Créditos personales"),
        discord.SelectOption(label="Estado de Cuenta",             value="estado",   emoji="📊", description="Ver saldos y movimientos"),
        discord.SelectOption(label="Cambio de Divisa",             value="divisa",   emoji="💱", description="CLP ⇌ USD"),
        discord.SelectOption(label="Mis Tarjetas",                 value="tarjetas", emoji="🗂️", description="Ver mis tarjetas activas"),
    ])
    async def menu_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        val = select.values[0]
        if val == "debito":
            await interaction.response.send_modal(ModalDebitoView())
        elif val == "credito":
            await interaction.response.send_modal(ModalCreditoView())
        elif val == "prestamo":
            await interaction.response.send_modal(ModalPrestamoView())
        elif val == "estado":
            user = get_user(interaction.user.id)
            tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
            h = user.get("historial", [])[:5]
            if tc:
                tarjetas_val = (
                    f"**Débito:** {'✅ Activa' if user['tarjeta_debito'] else '❌ Sin tarjeta'}\n"
                    f"**Crédito:** {tc['emoji']} {tc['nombre']}\n"
                    f"**Límite:** {clp(user['limite_credito'])}\n"
                    f"**Deuda:** {clp(user['deuda_credito'])}\n"
                    f"**Disponible:** {clp(user['limite_credito'] - user['deuda_credito'])}"
                )
            else:
                debito_estado_txt = "✅ Activa" if user["tarjeta_debito"] else "❌ Sin tarjeta"
                tarjetas_val = f"**Débito:** {debito_estado_txt}\n**Crédito:** ❌ Sin tarjeta"
            em = discord.Embed(title="📊 Estado de Cuenta", color=COLOR_PRINCIPAL)
            em.set_thumbnail(url=interaction.user.display_avatar.url)
            em.add_field(
                name="🇨🇱 Saldos CLP",
                value=f"💵 Efectivo: **{clp(user['efectivo'])}**\n🏦 Banco: **{clp(user['banco'])}**",
                inline=True
            )
            em.add_field(
                name="🇺🇸 Saldos USD",
                value=f"💵 Efectivo: **{usd(user['usd'])}**\n🏦 Banco: **{usd(user['usd_banco'])}**",
                inline=True
            )
            em.add_field(name="💳 Tarjetas", value=tarjetas_val, inline=False)
            em.add_field(name="📋 Préstamos activos", value=f"{len(user.get('prestamos', []))} préstamo(s)", inline=True)
            if h:
                movs = "\n".join(f"`{m['fecha']}` {m['descripcion']}" for m in h)
            else:
                movs = "*Sin movimientos*"
            em.add_field(name="🕐 Últimos movimientos", value=movs, inline=False)
            em.set_footer(text="🏦 Banco Alianza Santander")
            em.timestamp = datetime.now()
            await interaction.response.send_message(embed=em, ephemeral=True)
        elif val == "divisa":
            em = discord.Embed(
                title="💱 Cambio de Divisa",
                color=COLOR_INFO,
                description=f"Tasa actual: **1 USD = {clp(TASA_CAMBIO)}**\n\nUsa los comandos:\n• `/divisa clp_a_usd`\n• `/divisa usd_a_clp`\n• `/divisa tasa`"
            )
            em.set_footer(text="🏦 Banco Alianza Santander")
            await interaction.response.send_message(embed=em, ephemeral=True)
        elif val == "tarjetas":
            user = get_user(interaction.user.id)
            tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
            em = discord.Embed(title="🗂️ Mis Tarjetas", color=COLOR_PRINCIPAL)
            if user["tarjeta_debito"]:
                debito_val = (
                    f"✅ **Activa**\n"
                    f"Número: `{user['tarjeta_debito']['numero']}`\n"
                    f"Titular: {user.get('nombre_completo', '?')}\n"
                    f"Emisión: {user['tarjeta_debito']['fecha_emision']}"
                )
            else:
                debito_val = "❌ Sin tarjeta\nUsa el menú para solicitar una."
            em.add_field(name="💳 Tarjeta de Débito", value=debito_val, inline=False)
            if tc:
                credito_val = (
                    f"✅ **{tc['nombre']}** Activa\n"
                    f"Límite: **{clp(user['limite_credito'])}**\n"
                    f"Deuda: **{clp(user['deuda_credito'])}**\n"
                    f"Disponible: **{clp(user['limite_credito'] - user['deuda_credito'])}**"
                )
                credito_emoji = tc["emoji"]
            else:
                credito_val = "❌ Sin tarjeta\nUsa el menú para solicitar una."
                credito_emoji = "💎"
            em.add_field(name=f"{credito_emoji} Tarjeta de Crédito", value=credito_val, inline=False)
            em.set_footer(text="🏦 Banco Alianza Santander")
            await interaction.response.send_message(embed=em, ephemeral=True)

    @discord.ui.button(label="⚡ Crédito Express", style=discord.ButtonStyle.green)
    async def btn_credito(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ModalCreditoView())

    @discord.ui.button(label="📊 Estado de Cuenta", style=discord.ButtonStyle.blurple)
    async def btn_estado(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = get_user(interaction.user.id)
        em = discord.Embed(title="📊 Estado de Cuenta Rápido", color=COLOR_PRINCIPAL)
        em.add_field(name="💵 Efectivo", value=clp(user["efectivo"]), inline=True)
        em.add_field(name="🏦 Banco", value=clp(user["banco"]), inline=True)
        em.add_field(name="🇺🇸 USD", value=usd(user["usd_banco"]), inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander")
        await interaction.response.send_message(embed=em, ephemeral=True)

    @discord.ui.button(label="💳 Mis Tarjetas", style=discord.ButtonStyle.gray)
    async def btn_tarjetas(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = get_user(interaction.user.id)
        tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
        em = discord.Embed(title="🗂️ Mis Tarjetas", color=COLOR_PRINCIPAL)
        em.add_field(name="💳 Débito", value="✅ Activa" if user["tarjeta_debito"] else "❌ Sin tarjeta", inline=True)
        if tc:
            credito_val = f"{tc['emoji']} {tc['nombre']}"
        else:
            credito_val = "❌ Sin tarjeta"
        em.add_field(name="💎 Crédito", value=credito_val, inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander")
        await interaction.response.send_message(embed=em, ephemeral=True)

@bot.tree.command(guild=guild_obj, name="banco", description="🏦 Acceder al Banco Alianza Santander")
async def banco(interaction: discord.Interaction):
    em = discord.Embed(
        title="🏦 BANCO ALIANZA SANTANDER",
        description="**Bienvenido al Banco Alianza Santander — Gran Chile RP**\n\nSelecciona el servicio que necesitas del menú o usa los botones rápidos.",
        color=COLOR_PRINCIPAL
    )
    em.add_field(name="📋 Servicios Disponibles", value=(
        "💳 **Tarjetas** — Crédito y débito\n"
        "💰 **Créditos** — Préstamos personales\n"
        "📊 **Consultas** — Estado de cuenta y movimientos\n"
        "💱 **Cambio de Divisa** — CLP ⇌ USD\n"
        "🗂️ **Mis Tarjetas** — Ver tarjetas activas"
    ), inline=False)
    em.add_field(name="⏰ Horario", value="🕐 24/7 (Servicio Automático)", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, view=BancoMenuView())

# ══════════════════════════════════════════════════════════════
# 🚀 INICIAR BOT
keep_alive()

TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
