"""
╔══════════════════════════════════════════════════════════════╗
║      🏦 BANCO CENTRAL DE CHILE — Gran Chile RP             ║
║                    Bot de Discord                            ║
║                 Archivo: main.py                             ║
╚══════════════════════════════════════════════════════════════╝

INSTALACIÓN:
  pip install discord.py

CONFIGURACIÓN:
  Cambia TOKEN y GUILD_ID abajo antes de ejecutar.

EJECUTAR:
  python main.py
"""

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
COLOR_PRINCIPAL   = 0x003087
COLOR_EXITO       = 0x00A650
COLOR_ERROR       = 0xE63946
COLOR_ADVERTENCIA = 0xFFD700
COLOR_INFO        = 0x4FC3F7
COLOR_CRIPTO       = 0xF7931A
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

def agregar_xp(user: dict, cantidad: int) -> tuple[int, bool]:
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
        activity=discord.Activity(type=discord.ActivityType.watching, name="🏦 Banco Central de Chile | Gran Chile RP")
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

    em = discord.Embed(
        title=f"⚖️ Balanza Financiera: {interaction.user.display_name}",
        color=COLOR_PRINCIPAL
    )
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(
        name="👤 Identidad",
        value=f"**{user['nombre_completo']}**\n*{user['ocupacion']}*" if user["registrado"] else "*No registrado como ciudadano*",
        inline=False
    )
    em.add_field(
        name="🇨🇱 CLP — Pesos Chilenos",
        value=f"💵 **Efectivo:** {clp(user['efectivo'])}\n🏦 **Banco:** {clp(user['banco'])}\n💳 **Deuda Crédito:** {clp(user['deuda_credito'])}\n💰 **Crédito Disponible:** {clp(max(0, user['limite_credito'] - user['deuda_credito']))}",
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
        value=f"**Débito:** {'✅ Activa' if user['tarjeta_debito'] else '❌ Sin tarjeta'}\n**Crédito:** {f\"{tc['emoji']} {tc['nombre']}\" if tc else '❌ Sin tarjeta'}",
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
    em.set_footer(text="🏦 Banco Central de Chile • Gran Chile RP | Información financiera personal")
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

    em = discord.Embed(title=f"👤 Perfil: {interaction.user.display_name}", color=COLOR_PRINCIPAL)
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(name="📋 Identidad", value=f"**{user['nombre_completo']}**\n{user['ocupacion']}" if user["registrado"] else "*No registrado*", inline=True)
    em.add_field(name="⭐ Nivel", value=f"**{user.get('nivel', 1)}**\nXP: {user.get('experiencia', 0)}", inline=True)
    em.add_field(name="🔥 Racha", value=f"**{user.get('rachas', 0)}** días", inline=True)
    em.add_field(name="💵 Efectivo", value=clp(user["efectivo"]), inline=True)
    em.add_field(name="🏦 Banco", value=clp(user["banco"]), inline=True)
    em.add_field(name="🇺🇸 USD Banco", value=usd(user["usd_banco"]), inline=True)
    em.add_field(name="💳 Débito", value="✅ Activa" if user["tarjeta_debito"] else "❌ Sin tarjeta", inline=True)
    em.add_field(name="💎 Crédito", value=f"{tc['emoji']} {tc['nombre']}" if tc else "❌ Sin tarjeta", inline=True)
    em.add_field(name="🚔 Penales", value=str(user.get("penales", 0)), inline=True)
    em.add_field(name="📋 Préstamos activos", value=str(len(user.get("prestamos", []))), inline=True)
    em.add_field(name="💰 Cuentas ahorro", value=f"{len(user.get('cuentas_ahorro', []))}/3", inline=True)
    em.add_field(name="🏆 Logros", value="\n".join(logros[-5:]) if isinstance(logros[0], str) else "*Sin logros*", inline=False)
    em.set_footer(text="🏦 Banco Central de Chile • Gran Chile RP")
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
        em.add_field(name="💳 Tarjeta", value=f"✅ **Activa**\n`{user['tarjeta_debito']['numero']}`\nTitular: {user.get('nombre_completo', interaction.user.display_name)}", inline=False)
    else:
        em.add_field(name="💳 Tarjeta", value="❌ Sin tarjeta\nUsa `/banco` para solicitar una.", inline=False)
    em.set_footer(text="🏦 Banco Central de Chile")
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
    em = discord.Embed(title="✅ Depósito Exitoso", color=COLOR_EXITO,
                       description=f"Depositaste **{clp(monto)}** en tu banco.\n🏦 Nuevo saldo banco: **{clp(user['banco'])}**")
    em.set_footer(text="🏦 Banco Central de Chile")
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
    em = discord.Embed(title="🏧 Retiro Exitoso", color=COLOR_EXITO,
                       description=f"Retiraste **{clp(monto)}** del banco.\n💵 Efectivo: **{clp(user['efectivo'])}**")
    em.set_footer(text="🏦 Banco Central de Chile")
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
    em = discord.Embed(title="➡️ Transferencia Exitosa", color=COLOR_EXITO,
                       description=f"Transferiste **{clp(monto)}** a **{usuario.display_name}**\n🏦 Tu saldo: **{clp(user['banco'])}**")
    em.set_footer(text="🏦 Banco Central de Chile")
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
    user["cuentas_ahorro"].append({"id": int(datetime.now().timestamp()), "saldo": monto, "apertura": datetime.now().strftime("%d/%m/%Y")})
    agregar_xp(user, 20)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_ABRIR", monto, f"Cuenta de ahorro abierta con {clp(monto)}")
    em = discord.Embed(title="✅ Cuenta de Ahorro Abierta", color=COLOR_EXITO,
                       description=f"Depositaste **{clp(monto)}** en tu nueva cuenta de ahorro.\n📈 Tasa: **{int(TASA_AHORRO*100)}% semanal**")
    em.set_footer(text="🏦 Banco Central de Chile")
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
    em.set_footer(text="🏦 Banco Central de Chile")
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
    await interaction.response.send_message(embed=discord.Embed(title="✅ Depósito en Ahorro", color=COLOR_EXITO,
        description=f"Depositaste **{clp(monto)}**.\nNuevo saldo: **{clp(user['cuentas_ahorro'][0]['saldo'])}**"), ephemeral=True)

@grupo_ahorro.command(name="retirar", description="Retirar de tu cuenta de ahorro")
@app_commands.describe(monto="Monto en CLP")
async def ahorro_retirar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]:
        return await interaction.response.send_message("❌ No tienes cuentas de ahorro.", ephemeral=True)
    if user["cuentas_ahorro"][0]["saldo"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente en ahorro. Tienes **{clp(user['cuentas_ahorro'][0]['saldo'])}**.", ephemeral=True)
    user["cuentas_ahorro"][0]["saldo"] -= monto
    user["banco"] += monto
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_RETIRO", monto, f"Retiro de ahorro {clp(monto)}")
    await interaction.response.send_message(embed=discord.Embed(title="✅ Retiro de Ahorro", color=COLOR_EXITO,
        description=f"Retiraste **{clp(monto)}** de tu ahorro al banco."), ephemeral=True)

@grupo_ahorro.command(name="cerrar", description="Cerrar tu cuenta de ahorro (retira todo el saldo)")
async def ahorro_cerrar(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]:
        return await interaction.response.send_message("❌ No tienes cuentas de ahorro.", ephemeral=True)
    cuenta = user["cuentas_ahorro"].pop(0)
    user["banco"] += cuenta["saldo"]
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_CERRAR", cuenta["saldo"], f"Cuenta de ahorro cerrada")
    await interaction.response.send_message(embed=discord.Embed(title="⚠️ Cuenta de Ahorro Cerrada", color=COLOR_ADVERTENCIA,
        description=f"Se devolvieron **{clp(cuenta['saldo'])}** a tu banco."), ephemeral=True)

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
    em.set_footer(text="🏦 Banco Central de Chile")
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
        em.add_field(name=f"Préstamo #{i}", value=f"Total: **{clp(p['total'])}**\nCuota: **{clp(p['cuota'])}**\nSemanas restantes: **{p['semanas_restantes']}**\nMotivo: *{p['motivo'][:40]}*", inline=True)
    em.set_footer(text="🏦 Banco Central de Chile")
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
    await interaction.response.send_message(embed=discord.Embed(title="✅ Pago Realizado", color=COLOR_EXITO,
        description=f"Pagaste **{clp(monto)}** de tu préstamo.\nPréstamos restantes: **{len(user['prestamos'])}**"), ephemeral=True)

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
    em.set_footer(text="🏦 Banco Central de Chile")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_prestamo.command(name="ayuda", description="Información sobre cómo solicitar un préstamo")
async def prestamo_ayuda(interaction: discord.Interaction):
    em = discord.Embed(title="ℹ️ Información de Préstamos", color=COLOR_INFO,
        description="Para solicitar un préstamo usa **/banco** y selecciona **Solicitar Préstamo**.")
    em.add_field(name="📈 Tasas de interés", value="• 1 semana: **5%**\n• 2 semanas: **10%**\n• 3 semanas: **15%**", inline=False)
    em.add_field(name="📋 Requisitos", value="• Tener tarjeta de débito activa\n• Monto mínimo: **$10.000 CLP**", inline=False)
    em.set_footer(text="🏦 Banco Central de Chile")
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
    em = discord.Embed(title="🪙 Mercado Cripto — Gran Chile RP", color=COLOR_CRIPTO,
        description="Precios actuales en **CLP 🇨🇱**")
    iconos = {"BTC": "₿", "ETH": "⟠", "SOL": "◎", "DOGE": "🐶", "ADA": "🔵"}
    for k, v in precios.items():
        em.add_field(name=f"{iconos.get(k,'🪙')} {k}", value=clp(v), inline=True)
    em.set_footer(text="🏦 Banco Central de Chile • Precios actualizados cada hora")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

@grupo_cripto.command(name="comprar", description="Comprar criptomonedas (precio al momento de la compra)")
@app_commands.describe(moneda="BTC, ETH, SOL, DOGE o ADA", monto="Monto en CLP a invertir")
async def cripto_comprar(interaction: discord.Interaction, moneda: str, monto: int):
    moneda = moneda.upper()
    db = cargar_db()
    precios = get_precios_cripto(db)
    if moneda not in precios:
        return await interaction.response.send_message(f"❌ Moneda no disponible. Opciones: **{', '.join(precios.keys())}**", ephemeral=True)
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
    em.set_footer(text="🏦 Banco Central de Chile")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_cripto.command(name="vender", description="Vender criptomonedas (precio al momento de la venta)")
@app_commands.describe(moneda="BTC, ETH, SOL, DOGE o ADA", cantidad="Cantidad a vender")
async def cripto_vender(interaction: discord.Interaction, moneda: str, cantidad: float):
    moneda = moneda.upper()
    db = cargar_db()
    precios = get_precios_cripto(db)
    user = get_user(interaction.user.id)
    if moneda not in precios:
        return await interaction.response.send_message(f"❌ Moneda no encontrada.", ephemeral=True)
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
    em.set_footer(text="🏦 Banco Central de Chile")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_cripto.command(name="portafolio", description="Ver tus billeteras cripto")
async def cripto_portafolio(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    db = cargar_db()
    precios = get_precios_cripto(db)
    entradas = [(k, v) for k, v in user.get("cripto", {}).items() if v > 0]
    
    if not entradas:
        return await interaction.response.send_message("❌ No tienes ninguna criptomoneda en tu portafolio.", ephemeral=True)
        
    em = discord.Embed(title=f"💼 Mi Portafolio Cripto — {interaction.user.display_name}", color=COLOR_CRIPTO)
    total_clp = 0
    for k, v in entradas:
        valor_actual = int(v * precios.get(k, 0))
        total_clp += valor_actual
        em.add_field(name=f"🪙 {k}", value=f"Monto: `{v:.6f}`\nValor: **{clp(valor_actual)}**", inline=True)
        
    em.add_field(name="📊 Valor Total de Activos", value=f"**{clp(total_clp)}**", inline=False)
    em.set_footer(text="🏦 Banco Central de Chile")
    await interaction.response.send_message(embed=em, ephemeral=True)

bot.tree.add_command(grupo_cripto)

# ══════════════════════════════════════════════════════════════
# 📊 /acciones
# ══════════════════════════════════════════════════════════════
grupo_acciones = app_commands.Group(name="acciones", description="📊 Mercado de acciones de empresas chilenas", guild_ids=[GUILD_ID])

@grupo_acciones.command(name="mercado", description="Ver precios de acciones")
async def acciones_mercado(interaction: discord.Interaction):
    db = cargar_db()
    precios = get_precios_acciones(db)
    em = discord.Embed(title="📊 Bolsa de Comercio (Chile RP)", color=COLOR_INFO, description="Precios de acciones por unidad")
    for k, v in precios.items():
        em.add_field(name=f"📈 {k}", value=clp(v), inline=True)
    em.set_footer(text="🏦 Actualizado automáticamente cada hora")
    await interaction.response.send_message(embed=em)

@grupo_acciones.command(name="comprar", description="Comprar acciones comerciales")
@app_commands.describe(empresa="COPEC, FALABELLA, BCI, CMPC, ENTEL, LATAM, CENCOSUD", cantidad="Cantidad a comprar")
async def acciones_comprar(interaction: discord.Interaction, empresa: str, cantidad: int):
    empresa = empresa.upper()
    db = cargar_db()
    precios = get_precios_acciones(db)
    if empresa not in precios:
        return await interaction.response.send_message("❌ Empresa no válida.", ephemeral=True)
    if cantidad <= 0:
        return await interaction.response.send_message("❌ La cantidad debe ser mayor a 0.", ephemeral=True)
        
    costo = precios[empresa] * cantidad
    user = get_user(interaction.user.id)
    if user["banco"] < costo:
        return await interaction.response.send_message(f"❌ Saldo bancario insuficiente. Necesitas **{clp(costo)}**.", ephemeral=True)
        
    user["banco"] -= costo
    user["acciones"][empresa] = user["acciones"].get(empresa, 0) + cantidad
    agregar_xp(user, 10)
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "ACCIONES_COMPRA", costo, f"Compra de {cantidad} acciones de {empresa}")
    
    await interaction.response.send_message(embed=discord.Embed(
        title="✅ Compra de Acciones Exitosa", color=COLOR_EXITO,
        description=f"Adquiriste **{cantidad}** acciones de **{empresa}** por **{clp(costo)}**."
    ), ephemeral=True)

@grupo_acciones.command(name="vender", description="Vender acciones comerciales")
@app_commands.describe(empresa="COPEC, FALABELLA, BCI, CMPC, ENTEL, LATAM, CENCOSUD", cantidad="Cantidad a vender")
async def acciones_vender(interaction: discord.Interaction, empresa: str, cantidad: int):
    empresa = empresa.upper()
    db = cargar_db()
    precios = get_precios_acciones(db)
    user = get_user(interaction.user.id)
    
    if user["acciones"].get(empresa, 0) < cantidad or cantidad <= 0:
        return await interaction.response.send_message("❌ No posees suficientes acciones de esta empresa.", ephemeral=True)
        
    ganancia = precios[empresa] * cantidad
    user["acciones"][empresa] -= cantidad
    user["banco"] += ganancia
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "ACCIONES_VENTA", ganancia, f"Venta de {cantidad} acciones de {empresa}")
    
    await interaction.response.send_message(embed=discord.Embed(
        title="✅ Venta de Acciones Exitosa", color=COLOR_EXITO,
        description=f"Vendiste **{cantidad}** acciones de **{empresa}** y recibiste **{clp(ganancia)}** en tu banco."
    ), ephemeral=True)

bot.tree.add_command(grupo_acciones)

# ══════════════════════════════════════════════════════════════
# 📇 SISTEMA DE INTERFACES INTERACTIVAS
# ══════════════════════════════════════════════════════════════
class BancoMenuSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Registrar Identidad Civil", description="Crea tu carnet de identidad chileno en el servidor", emoji="👤"),
            discord.SelectOption(label="Obtener Tarjeta de Débito", description="Tramita tu tarjeta para transferencias bancarias", emoji="💳"),
            discord.SelectOption(label="Tramitar Tarjeta de Crédito", description="Obtén financiamiento con una línea de crédito base", emoji="💎"),
            discord.SelectOption(label="Solicitar Préstamo Rápido", description="Pide un préstamo express de $50.000 CLP", emoji="📋"),
            discord.SelectOption(label="Saldar Tarjeta de Crédito", description="Paga los saldos y deudas pendientes", emoji="💰")
        ]
        super().__init__(placeholder="🏦 Elige un trámite o servicio financiero...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)
        
        if self.values[0] == "Registrar Identidad Civil":
            if user["registrado"]:
                return await interaction.response.send_message("❌ Ya estás registrado formalmente en el Registro Civil.", ephemeral=True)
            user["nombre_completo"] = f"Ciudadano {interaction.user.display_name}"
            user["ocupacion"] = "Empleado Común"
            user["registrado"] = True
            save_user(interaction.user.id, user)
            return await interaction.response.send_message(f"🇨🇱 **Registro Exitoso:** Bienvenido al sistema, **{user['nombre_completo']}**.", ephemeral=True)

        if self.values[0] == "Obtener Tarjeta de Débito":
            if user["tarjeta_debito"]:
                return await interaction.response.send_message("❌ Tu tarjeta de débito ya se encuentra activa.", ephemeral=True)
            user["tarjeta_debito"] = {"numero": generar_numero_tarjeta(), "creacion": datetime.now().strftime("%d/%m/%Y")}
            save_user(interaction.user.id, user)
            return await interaction.response.send_message(f"💳 **Tarjeta de Débito Creada:** Número asignado: `{user['tarjeta_debito']['numero']}`", ephemeral=True)

        if self.values[0] == "Tramitar Tarjeta de Crédito":
            if user["tarjeta_credito"]:
                return await interaction.response.send_message("❌ Ya eres titular de una tarjeta de crédito comercial.", ephemeral=True)
            user["tarjeta_credito"] = "clasica"
            user["limite_credito"] = TIPO_TARJETA["clasica"]["limite"]
            save_user(interaction.user.id, user)
            return await interaction.response.send_message("🥈 **Aprobada:** Has obtenido una Tarjeta de Crédito **Clásica** con cupo inicial de $200.000 CLP.", ephemeral=True)

        if self.values[0] == "Solicitar Préstamo Rápido":
            if not user["tarjeta_debito"]:
                return await interaction.response.send_message("❌ Requiere una tarjeta de débito activa para depositar el dinero.", ephemeral=True)
            if len(user["prestamos"]) >= 2:
                return await interaction.response.send_message("❌ Límite de préstamos activos alcanzado (Máximo 2).", ephemeral=True)
            
            monto, semanas = 50000, 2
            total = int(monto * 1.10)
            user["banco"] += monto
            user["prestamos"].append({
                "total": total, "cuota": total // semanas, "semanas_restantes": semanas, "motivo": "Préstamo Directo Express"
            })
            save_user(interaction.user.id, user)
            add_historial(interaction.user.id, "PRESTAMO_OTORGADO", monto, "Préstamo Express aprobado via menú")
            return await interaction.response.send_message(f"✅ **Aprobado:** Se agregaron {clp(monto)} a tu banco. Debes pagar {clp(total)} en {semanas} semanas.", ephemeral=True)

        if self.values[0] == "Saldar Tarjeta de Crédito":
            if user["deuda_credito"] <= 0:
                return await interaction.response.send_message("✅ No registras deudas pendientes en tu línea crediticia.", ephemeral=True)
            if user["banco"] < user["deuda_credito"]:
                return await interaction.response.send_message("❌ Saldo bancario insuficiente para pagar tu deuda.", ephemeral=True)
                
            deuda = user["deuda_credito"]
            user["banco"] -= deuda
            user["deuda_credito"] = 0
            save_user(interaction.user.id, user)
            add_historial(interaction.user.id, "PAGO_TARJETA", -deuda, "Saldó deuda de crédito")
            return await interaction.response.send_message("💳 **Línea de Crédito Liberada:** Tu deuda ha sido liquidada por completo.", ephemeral=True)

class BancoMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BancoMenuSelect())

@bot.tree.command(guild=guild_obj, name="banco", description="🏦 Abrir el panel interactivo del Banco Central")
async def banco(interaction: discord.Interaction):
    em = discord.Embed(
        title="🏦 Banco Central de la República de Chile",
        description="Bienvenido a la sucursal automatizada. Usa el menú de selección de abajo para procesar tus trámites directamente sin comandos.",
        color=COLOR_PRINCIPAL
    )
    em.set_footer(text="Gran Chile RP • Estabilidad y Crecimiento Económico")
    await interaction.response.send_message(embed=em, view=BancoMenuView(), ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 💼 COMANDOS DE TRABAJO, CRIMEN Y RECOMPENSAS
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="diario", description="📆 Recibir tu sueldo de asistencia diario")
async def diario(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    ahora = datetime.now()
    
    if user["ultimo_diario"]:
        ud = datetime.strptime(user["ultimo_diario"], "%Y-%m-%d %H:%M:%S")
        if ahora - ud < timedelta(days=1):
            restante = timedelta(days=1) - (ahora - ud)
            horas, rem = divmod(restante.seconds, 3600)
            minutos, _ = divmod(rem, 60)
            return await interaction.response.send_message(f"⏳ Ya retiraste tu bono diario. Vuelve en **{horas}h {minutos}m**.", ephemeral=True)

    bono = 25000
    user["efectivo"] += bono
    user["ultimo_diario"] = ahora.strftime("%Y-%m-%d %H:%M:%S")
    user["rachas"] = user.get("rachas", 0) + 1
    agregar_xp(user, 30)
    save_user(interaction.user.id, user)
    
    await interaction.response.send_message(embed=discord.Embed(
        title="📆 Bono Diario Recogido", color=COLOR_EXITO,
        description=f"Has cobrado tu subsidio de **{clp(bono)}** en efectivo.\n🔥 Racha actual: **{user['rachas']} días**"
    ))

@bot.tree.command(guild=guild_obj, name="trabajar", description="🛠️ Hacer jornadas de trabajo lícitas")
async def trabajar(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    ahora = datetime.now()
    
    if user["ultimo_trabajo"]:
        ut = datetime.strptime(user["ultimo_trabajo"], "%Y-%m-%d %H:%M:%S")
        if ahora - ut < timedelta(minutes=30):
            restante = timedelta(minutes=30) - (ahora - ut)
            mins = restante.seconds // 60
            return await interaction.response.send_message(f"❌ Estás cansado. Puedes volver a trabajar en **{mins} minutos**.", ephemeral=True)

    empleos = [
        ("Conductor de buses en Red Metropolitana 🚌", 15000),
        ("Operador en minería de Cobre en Calama ⛏️", 28000),
        ("Cajero en un local de Falabella 🛍️", 16500),
        ("Desarrollador de software para Corfo 💻", 35000),
        ("Guardia de seguridad de Prosegur 🛡️", 18000)
    ]
    
    empleo, sueldo = random.choice(empleos)
    user["efectivo"] += sueldo
    user["ultimo_trabajo"] = ahora.strftime("%Y-%m-%d %H:%M:%S")
    subio_lvl = agregar_xp(user, 25)[1]
    save_user(interaction.user.id, user)
    
    desc = f"Cumpliste con tu turno como: **{empleo}**.\n💰 **Sueldo recibido:** {clp(sueldo)}"
    if subio_lvl: 
        desc += f"\n\n⭐ ¡Subiste de nivel! Nivel actual: **{user['nivel']}**"
        
    await interaction.response.send_message(embed=discord.Embed(title="🛠️ Jornada Laboral Completada", color=COLOR_INFO, description=desc))

@bot.tree.command(guild=guild_obj, name="crimen", description="🥷 Planificar y ejecutar un acto delictivo")
async def crimen(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    ahora = datetime.now()
    
    if user["ultimo_crimen"]:
        uc = datetime.strptime(user["ultimo_crimen"], "%Y-%m-%d %H:%M:%S")
        if ahora - uc < timedelta(hours=1):
            restante = timedelta(hours=1) - (ahora - uc)
            mins = restante.seconds // 60
            return await interaction.response.send_message(f"🚨 La policía te sigue el rastro. Espera **{mins} minutos**.", ephemeral=True)

    user["ultimo_crimen"] = ahora.strftime("%Y-%m-%d %H:%M:%S")
    exito = random.choices([True, False], weights=[45, 55])[0] # 45% probabilidad de éxito
    delito = random.choice(CRIMENES)
    
    if exito:
        botin = random.randint(50000, 200000)
        user["efectivo"] += botin
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "CRIMEN_EXITO", botin, f"Participó en {delito}")
        await interaction.response.send_message(embed=discord.Embed(
            title="🥷 Plan Maestro Exitoso", color=COLOR_EXITO,
            description=f"Lograste el cometido en: **{delito}**.\n💰 **Botín obtenido:** {clp(botin)}"
        ))
    else:
        multa = random.randint(25000, 75000)
        user["efectivo"] = max(0, user["efectivo"] - multa)
        user["penales"] = user.get("penales", 0) + 1
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "CRIMEN_FALLIDO", -multa, f"Multado por {delito}")
        await interaction.response.send_message(embed=discord.Embed(
            title="🚨 Arresto Policial", color=COLOR_ERROR,
            description=f"Fuiste interceptado ejecutando: **{delito}**.\n⚖️ **Sanción:** Perdiste **{clp(multa)}** por fianza y se sumó a tu récord criminal."
        ))

# ══════════════════════════════════════════════════════════════
# 📜 /historial
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="historial", description="📜 Ver tus últimas transacciones y movimientos")
async def historial(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    movimientos = user.get("historial", [])
    
    if not movimientos:
        return await interaction.response.send_message("📋 No tienes registros de movimientos recientes.", ephemeral=True)
        
    em = discord.Embed(title=f"📜 Movimientos Recientes — {interaction.user.display_name}", color=COLOR_PRINCIPAL)
    texto_lineas = []
    
    for m in movimientos[:10]: # Muestra los últimos 10 movimientos
        signo = "+" if m["monto"] >= 0 else ""
        texto_lineas.append(f"⏱️ `[{m['fecha']}]` **{m['tipo']}** ({signo}{clp(m['monto'])})\n└ *{m['descripcion']}*")
        
    em.description = "\n".join(texto_lineas)
    em.set_footer(text="🏦 Registro de auditoría del Banco Central")
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🚀 EJECUCIÓN FINAL
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if TOKEN == "TU_TOKEN_AQUI":
        print("❌ ERROR: Recuerda cambiar 'TU_TOKEN_AQUI' por tu token real en el código.")
    else:
        bot.run(TOKEN)
