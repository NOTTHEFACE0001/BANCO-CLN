# ╔════════════════════════════════════════════════════════════════╗
# ║     🏦 BANCO ALIANZA SANTANDER — Gran Chile RP                ║
# ║                  Bot de Discord                               ║
# ║                  Archivo: main.py                             ║
# ╚════════════════════════════════════════════════════════════════╝
#
# INSTALACIÓN:
#   pip install discord.py flask
#
# CONFIGURACIÓN:
#   En Render, crea una variable de entorno llamada TOKEN con el token de tu bot.
#   Cambia GUILD_ID abajo por el ID de tu servidor.
#
# EJECUTAR:
#   python main.py

# ══════════════════════════════════════════════════════════════
# 🌐 KEEP ALIVE (Flask — para Render/Replit)
# ══════════════════════════════════════════════════════════════
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "¡Bot BANCO ALIANZA SANTANDER ONLINE!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ══════════════════════════════════════════════════════════════
# 📦 IMPORTS
# ══════════════════════════════════════════════════════════════
import discord
from discord import app_commands
from discord.ext import commands, tasks
import json, os, random
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════
# ⚙️  CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════
GUILD_ID = 1234567890  # ← Cambia esto por el ID de tu servidor

# ══════════════════════════════════════════════════════════════
# 🎨 CONSTANTES
# ══════════════════════════════════════════════════════════════
COLOR_PRINCIPAL   = 0x003087
COLOR_EXITO       = 0x00A650
COLOR_ERROR       = 0xE63946
COLOR_ADVERTENCIA = 0xFFD700
COLOR_INFO        = 0x4FC3F7
COLOR_CRIPTO      = 0xF7931A
COLOR_PREMIUM     = 0x7B2FBE

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

TRABAJOS = [
    ("🚕 Taxista",      15_000, 30_000),
    ("🚚 Repartidor",   20_000, 40_000),
    ("👷 Construcción", 25_000, 45_000),
    ("🏪 Cajero",       18_000, 35_000),
    ("💻 Programador",  35_000, 70_000),
    ("🩺 Médico",       50_000, 90_000),
    ("⚖️ Abogado",      45_000, 80_000),
    ("🚔 Policía",      30_000, 55_000),
]

DB_FILE = "database.json"

# ══════════════════════════════════════════════════════════════
# 🗄️  BASE DE DATOS (JSON)
# ══════════════════════════════════════════════════════════════
def cargar_db() -> dict:
    if not os.path.exists(DB_FILE):
        data = {"users": {}, "cripto_precios": {}, "acciones_precios": {},
                "ultima_actualizacion_cripto": 0, "ultima_actualizacion_acciones": 0}
        guardar_db(data)
        return data
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_db(db: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(user_id) -> dict:
    db = cargar_db()
    uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "efectivo":                   50_000,
            "banco":                      0,
            "usd":                        0,
            "usd_banco":                  0,
            "tarjeta_debito":             None,
            "tarjeta_credito":            None,
            "deuda_credito":              0,
            "limite_credito":             0,
            "cuentas_ahorro":             [],
            "prestamos":                  [],
            "cripto":                     {},
            "acciones":                   {},
            "historial":                  [],
            "ultimo_colectar":            None,
            "ultimo_diario":              None,
            "ultimo_crimen":              None,
            "ultimo_trabajo":             None,
            "rachas":                     0,
            "penales":                    0,
            "nombre_completo":            None,
            "ocupacion":                  None,
            "ingresos":                   0,
            "registrado":                 False,
            "nivel":                      1,
            "experiencia":                0,
            "logros":                     [],
            "transferencias_hoy":         0,
            "ultima_transferencia_fecha": None,
        }
        guardar_db(db)
    return db["users"][uid]

def save_user(user_id, data: dict):
    db = cargar_db()
    db["users"][str(user_id)] = data
    guardar_db(db)

def add_historial(user_id, tipo: str, monto: int, descripcion: str):
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

def agregar_xp(user: dict, cantidad: int) -> tuple:
    """Agrega XP y retorna (nivel_actual, subio_de_nivel)."""
    user["experiencia"] = user.get("experiencia", 0) + cantidad
    nivel_viejo = user.get("nivel", 1)
    nivel_nuevo = 1 + int(user["experiencia"] ** 0.4 / 3)
    user["nivel"] = nivel_nuevo
    return nivel_nuevo, nivel_nuevo > nivel_viejo

def get_precios_cripto(db: dict) -> dict:
    ahora = datetime.now().timestamp()
    if not db.get("cripto_precios") or ahora - db.get("ultima_actualizacion_cripto", 0) > 3600:
        db["cripto_precios"] = {
            "BTC":  random.randint(25_000_000, 35_000_000),
            "ETH":  random.randint(1_500_000,   2_000_000),
            "SOL":  random.randint(80_000,       120_000),
            "DOGE": random.randint(60,            120),
            "ADA":  random.randint(300,           600),
        }
        db["ultima_actualizacion_cripto"] = ahora
        guardar_db(db)
    return db["cripto_precios"]

def get_precios_acciones(db: dict) -> dict:
    ahora = datetime.now().timestamp()
    if not db.get("acciones_precios") or ahora - db.get("ultima_actualizacion_acciones", 0) > 3600:
        db["acciones_precios"] = {
            "COPEC":     random.randint(7_000,  10_000),
            "FALABELLA": random.randint(2_500,   4_000),
            "BCI":       random.randint(30_000, 40_000),
            "CMPC":      random.randint(1_500,   2_500),
            "ENTEL":     random.randint(900,     1_500),
            "LATAM":     random.randint(3_000,   5_000),
            "CENCOSUD":  random.randint(1_800,   3_000),
        }
        db["ultima_actualizacion_acciones"] = ahora
        guardar_db(db)
    return db["acciones_precios"]

# ══════════════════════════════════════════════════════════════
# 🤖 BOT
# ══════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
guild_obj = discord.Object(id=1486083692089704619)

@bot.event
async def on_ready():
    print(f"✅ Bot listo: {bot.user}")
    bot.tree.copy_global_to(guild=guild_obj)
    await bot.tree.sync(guild=guild_obj)
    print("✅ Slash commands sincronizados.")
    actualizar_precios.start()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="🏦 Banco Alianza Santander | Gran Chile RP"
        )
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

    identidad_val = (
        f"**{user['nombre_completo']}**\n*{user['ocupacion']}*"
        if user["registrado"] else "*No registrado como ciudadano*"
    )
    credito_val = f"{tc['emoji']} {tc['nombre']}" if tc else "❌ Sin tarjeta"

    em = discord.Embed(
        title=f"⚖️ Balanza Financiera: {interaction.user.display_name}",
        color=COLOR_PRINCIPAL
    )
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(name="👤 Identidad", value=identidad_val, inline=False)
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

    identidad_val = (
        f"**{user['nombre_completo']}**\n{user['ocupacion']}"
        if user["registrado"] else "*No registrado*"
    )
    credito_val = f"{tc['emoji']} {tc['nombre']}" if tc else "❌ Sin tarjeta"
    logros_val = "\n".join(logros[-5:]) if isinstance(logros[0], str) else "*Sin logros*"

    em = discord.Embed(title=f"👤 Perfil: {interaction.user.display_name}", color=COLOR_PRINCIPAL)
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(name="📋 Identidad",          value=identidad_val,                              inline=True)
    em.add_field(name="⭐ Nivel",               value=f"**{user.get('nivel',1)}**\nXP: {user.get('experiencia',0)}", inline=True)
    em.add_field(name="🔥 Racha",               value=f"**{user.get('rachas',0)}** días",         inline=True)
    em.add_field(name="💵 Efectivo",            value=clp(user["efectivo"]),                      inline=True)
    em.add_field(name="🏦 Banco",               value=clp(user["banco"]),                         inline=True)
    em.add_field(name="🇺🇸 USD Banco",          value=usd(user["usd_banco"]),                     inline=True)
    em.add_field(name="💳 Débito",              value="✅ Activa" if user["tarjeta_debito"] else "❌ Sin tarjeta", inline=True)
    em.add_field(name="💎 Crédito",             value=credito_val,                                inline=True)
    em.add_field(name="🚔 Penales",             value=str(user.get("penales", 0)),                inline=True)
    em.add_field(name="📋 Préstamos activos",   value=str(len(user.get("prestamos", []))),        inline=True)
    em.add_field(name="💰 Cuentas ahorro",      value=f"{len(user.get('cuentas_ahorro', []))}/3", inline=True)
    em.add_field(name="🏆 Logros",              value=logros_val,                                 inline=False)
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
    em.add_field(name="💵 Efectivo",  value=clp(user["efectivo"]),  inline=True)
    em.add_field(name="🏦 Banco",     value=clp(user["banco"]),     inline=True)
    em.add_field(name="🇺🇸 USD Banco",value=usd(user["usd_banco"]), inline=True)
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
        title="✅ Depósito Exitoso", color=COLOR_EXITO,
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
        title="🏧 Retiro Exitoso", color=COLOR_EXITO,
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
        title="➡️ Transferencia Exitosa", color=COLOR_EXITO,
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
        return await interaction.response.send_message(f