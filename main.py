# cat > /home/claude/main_final.py << 'PYEOF'
# ╔════════════════════════════════════════════════════════════════╗
# ║     🏦 BANCO ALIANZA SANTANDER — Gran Chile RP                ║
# ║   Cripto x15 + Autos + Bolsa + Balanza Personalizada          ║
# ║   /regalar /ruleta /banco_info /mi_nivel /buscar_usuario       ║
# ║   /convertir /auto_info /pagar_deuda                          ║
# ║                  Archivo: main.py                             ║
# ╚════════════════════════════════════════════════════════════════╝
# INSTALACIÓN:  pip install discord.py flask
# RAILWAY:      Variable de entorno TOKEN = tu token del bot
# EJECUTAR:     python main.py

# ══════════════════════════════════════════════════════════════
# 🌐 KEEP ALIVE
# ══════════════════════════════════════════════════════════════
import os
from flask import Flask
from threading import Thread

_app = Flask('')

@_app.route('/')
def home():
    return "🏦 BANCO ALIANZA SANTANDER — Gran Chile RP ONLINE!"

def _run():
    puerto = int(os.environ.get("PORT", 8080))
    _app.run(host='0.0.0.0', port=puerto)

def keep_alive():
    Thread(target=_run, daemon=True).start()

# ══════════════════════════════════════════════════════════════
# 📦 IMPORTS
# ══════════════════════════════════════════════════════════════
import discord
from discord import app_commands
from discord.ext import commands, tasks
import json, random
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════
# ⚙️  CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════
GUILD_ID = 1486083692089704619

# ══════════════════════════════════════════════════════════════
# 🎨 COLORES
# ══════════════════════════════════════════════════════════════
COLOR_PRINCIPAL   = 0x003087
COLOR_EXITO       = 0x00A650
COLOR_ERROR       = 0xE63946
COLOR_ADVERTENCIA = 0xFFD700
COLOR_INFO        = 0x4FC3F7
COLOR_CRIPTO      = 0xF7931A
COLOR_PREMIUM     = 0x7B2FBE
COLOR_AUTO        = 0x1565C0
COLOR_REGALO      = 0xFF69B4
COLOR_RULETA      = 0x8B0000

TASA_CAMBIO = 950  # 1 USD = 950 CLP

# ══════════════════════════════════════════════════════════════
# 🪙 15 CRIPTOMONEDAS
# ══════════════════════════════════════════════════════════════
CRIPTO_INFO = {
    "BTC":    {"nombre": "Bitcoin",      "emoji": "₿",  "icon": "🟠", "desc": "La primera criptomoneda del mundo"},
    "ETH":    {"nombre": "Ethereum",     "emoji": "⟠",  "icon": "🔵", "desc": "Plataforma de contratos inteligentes"},
    "SOL":    {"nombre": "Solana",       "emoji": "◎",  "icon": "🟣", "desc": "Blockchain ultrarrápida"},
    "DOGE":   {"nombre": "Dogecoin",     "emoji": "🐶", "icon": "🟡", "desc": "La moneda del meme"},
    "ADA":    {"nombre": "Cardano",      "emoji": "🔷", "icon": "🔷", "desc": "Blockchain científica de tercera gen."},
    "CLPX":   {"nombre": "ChileCoin",    "emoji": "🇨🇱", "icon": "🌟", "desc": "La moneda oficial del metaverso chileno"},
    "COND":   {"nombre": "CondorToken",  "emoji": "🦅", "icon": "🦅", "desc": "Respaldada por el Cóndor de los Andes"},
    "LATA":   {"nombre": "LataChain",    "emoji": "🍺", "icon": "🍺", "desc": "Moneda del pueblo, del barrio, de la calle"},
    "PESC":   {"nombre": "PescaoCoin",   "emoji": "🐟", "icon": "🐟", "desc": "Basada en la industria pesquera chilena"},
    "COBRE":  {"nombre": "CopperX",      "emoji": "🟤", "icon": "⛏️", "desc": "Respaldada por el cobre de Chile"},
    "FLAITE": {"nombre": "FlaiteToken",  "emoji": "😎", "icon": "😎", "desc": "La moneda del RP underground"},
    "HUASO":  {"nombre": "HuasoCoin",    "emoji": "🤠", "icon": "🤠", "desc": "Moneda del campo chileno digital"},
    "ANDIN":  {"nombre": "AndinoChain",  "emoji": "⛰️", "icon": "⛰️", "desc": "Alta montaña, alta volatilidad"},
    "CUECA":  {"nombre": "CuecaToken",   "emoji": "💃", "icon": "💃", "desc": "Respaldada por el folklore chileno"},
    "RUCAF":  {"nombre": "RucaFinance",  "emoji": "🏠", "icon": "🏠", "desc": "DeFi mapuche descentralizado"},
}

CRIPTO_BASE = {
    "BTC": 28_000_000, "ETH": 1_800_000, "SOL": 90_000,
    "DOGE": 80,        "ADA": 450,       "CLPX": 5_000,
    "COND": 15_000,    "LATA": 200,      "PESC": 1_200,
    "COBRE": 25_000,   "FLAITE": 3_500,  "HUASO": 8_000,
    "ANDIN": 45_000,   "CUECA": 12_000,  "RUCAF": 60_000,
}

# ══════════════════════════════════════════════════════════════
# 🚗 AUTOS
# ══════════════════════════════════════════════════════════════
CATEGORIAS_AUTO = {
    "normal":    {"nombre": "🚗 Normal",    "costo_registro": 150_000,  "mensualidad": 25_000},
    "deportivo": {"nombre": "🏎️ Deportivo", "costo_registro": 400_000,  "mensualidad": 60_000},
    "suv":       {"nombre": "🚙 SUV",       "costo_registro": 300_000,  "mensualidad": 45_000},
    "lujo":      {"nombre": "💎 Lujo",      "costo_registro": 800_000,  "mensualidad": 120_000},
    "moto":      {"nombre": "🏍️ Moto",      "costo_registro": 80_000,   "mensualidad": 15_000},
    "camion":    {"nombre": "🚚 Camión",    "costo_registro": 500_000,  "mensualidad": 80_000},
}

def generar_matricula() -> str:
    letras = "ABCDEFGHJKLMNPRSTUVWXYZ"
    p1 = "".join(random.choices(letras, k=2))
    p2 = str(random.randint(1000, 9999))
    p3 = "".join(random.choices(letras, k=2))
    return f"{p1}·{p2}·{p3}"

# ══════════════════════════════════════════════════════════════
# 💳 TARJETAS
# ══════════════════════════════════════════════════════════════
TIPO_TARJETA = {
    "clasica":  {"nombre": "Clásica",  "emoji": "💳", "limite": 200_000,    "color": 0x808080},
    "plata":    {"nombre": "Plata",    "emoji": "🥈", "limite": 500_000,    "color": 0xC0C0C0},
    "oro":      {"nombre": "Oro",      "emoji": "🥇", "limite": 1_500_000,  "color": 0xFFD700},
    "platinum": {"nombre": "Platinum", "emoji": "💎", "limite": 5_000_000,  "color": 0x4FC3F7},
    "diamante": {"nombre": "Diamante", "emoji": "💠", "limite": 15_000_000, "color": 0x7B2FBE},
}

CRIMENES = [
    "🏦 Robo a Banco","📦 Tráfico de artículos ilegales",
    "💻 Hackeo de sistema financiero","🏢 Asalto a empresa",
    "📱 Fraude electrónico","🚗 Robo de vehículo de lujo",
    "💰 Lavado de dinero","🔐 Falsificación de documentos",
]

TRABAJOS = [
    ("🚕 Taxista",15_000,30_000),("🚚 Repartidor",20_000,40_000),
    ("👷 Construcción",25_000,45_000),("🏪 Cajero",18_000,35_000),
    ("💻 Programador",35_000,70_000),("🩺 Médico",50_000,90_000),
    ("⚖️ Abogado",45_000,80_000),("🚔 Policía",30_000,55_000),
]

DB_FILE = "database.json"

# ══════════════════════════════════════════════════════════════
# 🗄️  BASE DE DATOS
# ══════════════════════════════════════════════════════════════
def cargar_db() -> dict:
    if not os.path.exists(DB_FILE):
        data = {"users":{},"cripto_precios":{},"acciones_precios":{},
                "ultima_actualizacion_cripto":0,"ultima_actualizacion_acciones":0}
        guardar_db(data); return data
    with open(DB_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def guardar_db(db: dict):
    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(db,f,ensure_ascii=False,indent=2)

def get_user(user_id) -> dict:
    db = cargar_db(); uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "efectivo":50_000,"banco":0,"usd":0,"usd_banco":0,
            "tarjeta_debito":None,"tarjeta_credito":None,
            "deuda_credito":0,"limite_credito":0,
            "cuentas_ahorro":[],"prestamos":[],"cripto":{},
            "acciones":{},"autos":[],"historial":[],
            "ultimo_colectar":None,"ultimo_diario":None,
            "ultimo_crimen":None,"ultimo_trabajo":None,
            "rachas":0,"penales":0,"nombre_completo":None,
            "ocupacion":None,"ingresos":0,"registrado":False,
            "nivel":1,"experiencia":0,"logros":[],
            "transferencias_hoy":0,"ultima_transferencia_fecha":None,
        }
        guardar_db(db)
    return db["users"][uid]

def save_user(uid, data):
    db = cargar_db(); db["users"][str(uid)] = data; guardar_db(db)

def add_historial(uid, tipo, monto, desc):
    db = cargar_db(); s = str(uid)
    if s not in db["users"]: return
    h = db["users"][s].setdefault("historial",[])
    h.insert(0,{"tipo":tipo,"monto":monto,"descripcion":desc,
                "fecha":datetime.now().strftime("%d/%m/%Y %H:%M")})
    db["users"][s]["historial"] = h[:50]; guardar_db(db)

def clp(m) -> str:
    return f"${int(m):,} CLP".replace(",",".")

def usd(m) -> str:
    return f"${float(m):,.2f} USD"

def generar_numero_tarjeta() -> str:
    return " ".join(str(random.randint(1000,9999)) for _ in range(4))

def agregar_xp(user, cantidad):
    user["experiencia"] = user.get("experiencia",0) + cantidad
    nv = user.get("nivel",1)
    nn = 1 + int(user["experiencia"]**0.4/3)
    user["nivel"] = nn
    return nn, nn > nv

def get_precios_cripto(db):
    ahora = datetime.now().timestamp()
    if not db.get("cripto_precios") or ahora-db.get("ultima_actualizacion_cripto",0)>3600:
        db["cripto_precios"] = {s:max(1,int(b*(1+random.uniform(-0.12,0.12)))) for s,b in CRIPTO_BASE.items()}
        db["ultima_actualizacion_cripto"] = ahora; guardar_db(db)
    return db["cripto_precios"]

def get_precios_acciones(db):
    ahora = datetime.now().timestamp()
    if not db.get("acciones_precios") or ahora-db.get("ultima_actualizacion_acciones",0)>3600:
        db["acciones_precios"] = {
            "COPEC":random.randint(7_000,10_000),"FALABELLA":random.randint(2_500,4_000),
            "BCI":random.randint(30_000,40_000),"CMPC":random.randint(1_500,2_500),
            "ENTEL":random.randint(900,1_500),"LATAM":random.randint(3_000,5_000),
            "CENCOSUD":random.randint(1_800,3_000),
        }
        db["ultima_actualizacion_acciones"] = ahora; guardar_db(db)
    return db["acciones_precios"]

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
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="🏦 Banco Alianza Santander | Gran Chile RP"))

@tasks.loop(hours=1)
async def actualizar_precios():
    db = cargar_db()
    db["ultima_actualizacion_cripto"] = 0
    db["ultima_actualizacion_acciones"] = 0
    guardar_db(db)

# ══════════════════════════════════════════════════════════════
# ⚖️  /balanza — PERSONALIZADA BANCO ALIANZA SANTANDER
# ══════════════════════════════════════════════════════════════
# REEMPLAZA el comando /balanza en tu main.py por este:

@bot.tree.command(guild=guild_obj, name="balanza",
    description="⚖️ Ver tu resumen financiero — Banco Alianza Santander")
async def balanza(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    tc   = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
    db   = cargar_db()
    precios = get_precios_cripto(db)

    valor_cripto = sum(
        int(v * precios.get(k, 0))
        for k, v in user.get("cripto", {}).items() if v > 0
    )
    patrimonio_clp = user["efectivo"] + user["banco"] + valor_cripto
    patrimonio_usd  = user["usd"] + user["usd_banco"]

    # ── Identidad ──
    if user["registrado"]:
        id_val = f"```{user['nombre_completo']}```*{user['ocupacion']}*"
    else:
        id_val = "```No registrado```Usa `/banco` → Solicitar Tarjeta de Débito"

    # ── Tarjetas ──
    deb = "✅ Activa" if user["tarjeta_debito"] else "❌ Sin tarjeta"
    cred = f"{tc['emoji']} {tc['nombre']}" if tc else "❌ Sin tarjeta"

    # ── Cripto ──
    cripto_lineas = [
        f"{CRIPTO_INFO.get(k,{}).get('icon','🪙')} {k}: **{v:.4f}**"
        for k, v in user.get("cripto", {}).items() if v > 0.000001
    ]
    cripto_val = "\n".join(cripto_lineas) if cripto_lineas else "*Vacía*"

    # ── Vehículos ──
    n_autos = len(user.get("autos", []))
    autos_val = f"**{n_autos}** registrado(s)" if n_autos else "*Sin vehículos*"

    # ── Nivel / estado ──
    nivel  = user.get("nivel", 1)
    racha  = user.get("rachas", 0)
    penal  = user.get("penales", 0)
    estado = "🟢 Limpio" if penal == 0 else ("🟡 Vigilado" if penal < 3 else "🔴 Buscado")

    em = discord.Embed(color=COLOR_PRINCIPAL)

    # Título con nombre dinámico
    em.set_author(
        name=f"🏦 Banco Alianza Santander  •  Gran Chile RP",
    )
    em.title = f"📋 Resumen Financiero de {interaction.user.display_name}"
    em.set_thumbnail(url=interaction.user.display_avatar.url)

    # Bloque 1 — Identidad
    em.add_field(name="👤  Ciudadano", value=id_val, inline=False)

    # Bloque 2 — Dinero en CLP
    em.add_field(
        name="🇨🇱  Pesos Chilenos (CLP)",
        value=(
            f"💵 Efectivo: **{clp(user['efectivo'])}**\n"
            f"🏦 Banco:    **{clp(user['banco'])}**\n"
            f"💳 Deuda:   **{clp(user['deuda_credito'])}**\n"
            f"💰 Crédito libre: **{clp(max(0, user['limite_credito'] - user['deuda_credito']))}**"
        ),
        inline=True,
    )

    # Bloque 3 — USD
    em.add_field(
        name="🇺🇸  Dólares (USD)",
        value=(
            f"💵 Efectivo: **{usd(user['usd'])}**\n"
            f"🏦 Banco:    **{usd(user['usd_banco'])}**"
        ),
        inline=True,
    )

    em.add_field(name="\u200b", value="\u200b", inline=False)  # separador

    # Bloque 4 — Tarjetas
    em.add_field(
        name="💳  Tarjetas",
        value=f"Débito:  {deb}\nCrédito: {cred}",
        inline=True,
    )

    # Bloque 5 — Cripto
    em.add_field(
        name=f"🪙  Cartera Cripto  *(+{clp(valor_cripto)})*",
        value=cripto_val,
        inline=True,
    )

    # Bloque 6 — Autos
    em.add_field(
        name="🚗  Vehículos",
        value=autos_val,
        inline=True,
    )

    # Bloque 7 — Patrimonio (resaltado)
    em.add_field(
        name="━━━━━━━━━━━━━━━━━━━━━━━━━",
        value=(
            f"**💎 PATRIMONIO TOTAL**\n"
            f"🇨🇱  `{clp(patrimonio_clp)}`  *(incluye cripto)*\n"
            f"🇺🇸  `{usd(patrimonio_usd)}`"
        ),
        inline=False,
    )

    # Bloque 8 — Stats rápidos
    em.add_field(name="⭐ Nivel",  value=f"**{nivel}** | {user.get('experiencia',0)} XP", inline=True)
    em.add_field(name="🔥 Racha",  value=f"**{racha}** días",                              inline=True)
    em.add_field(name="🚨 Estado", value=estado,                                            inline=True)

    em.set_footer(text="🏦 Banco Alianza Santander  •  Gran Chile RP  |  Información confidencial")
    em.timestamp = datetime.now()

    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 👤 /perfil
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="perfil", description="👤 Ver tu perfil económico completo")
async def perfil(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
    logros = user.get("logros",[]) or ["*Sin logros aún*"]
    identidad_val = f"**{user['nombre_completo']}**\n{user['ocupacion']}" if user["registrado"] else "*No registrado*"
    credito_val = f"{tc['emoji']} {tc['nombre']}" if tc else "❌ Sin tarjeta"
    logros_val = "\n".join(logros[-5:]) if isinstance(logros[0],str) else "*Sin logros*"
    em = discord.Embed(title=f"👤 Perfil Ciudadano — {interaction.user.display_name}", color=COLOR_PRINCIPAL)
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(name="📋 Identidad",    value=identidad_val, inline=True)
    em.add_field(name="⭐ Nivel",        value=f"**{user.get('nivel',1)}**\nXP: {user.get('experiencia',0)}", inline=True)
    em.add_field(name="🔥 Racha",        value=f"**{user.get('rachas',0)}** días", inline=True)
    em.add_field(name="💵 Efectivo",     value=clp(user["efectivo"]), inline=True)
    em.add_field(name="🏦 Banco",        value=clp(user["banco"]), inline=True)
    em.add_field(name="🇺🇸 USD Banco",   value=usd(user["usd_banco"]), inline=True)
    em.add_field(name="💳 Débito",       value="✅ Activa" if user["tarjeta_debito"] else "❌ Sin tarjeta", inline=True)
    em.add_field(name="💎 Crédito",      value=credito_val, inline=True)
    em.add_field(name="🚗 Vehículos",    value=str(len(user.get("autos",[]))), inline=True)
    em.add_field(name="🚔 Penales",      value=str(user.get("penales",0)), inline=True)
    em.add_field(name="📋 Préstamos",    value=str(len(user.get("prestamos",[]))), inline=True)
    em.add_field(name="💰 Ahorros",      value=f"{len(user.get('cuentas_ahorro',[]))}/3", inline=True)
    em.add_field(name="🏆 Logros",       value=logros_val, inline=False)
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
    em.add_field(name="💵 Efectivo",   value=clp(user["efectivo"]), inline=True)
    em.add_field(name="🏦 Banco",      value=clp(user["banco"]),    inline=True)
    em.add_field(name="🇺🇸 USD Banco", value=usd(user["usd_banco"]),inline=True)
    if user["tarjeta_debito"]:
        em.add_field(name="💳 Tarjeta",
            value=f"✅ **Activa**\n`{user['tarjeta_debito']['numero']}`\nTitular: {user.get('nombre_completo', interaction.user.display_name)}",
            inline=False)
    else:
        em.add_field(name="💳 Tarjeta", value="❌ Sin tarjeta\nUsa `/banco` para solicitar una.", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="depositar", description="Guardar efectivo en el banco (Efectivo → Banco)")
@app_commands.describe(monto="Monto en CLP a depositar")
async def debito_depositar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto <= 0: return await interaction.response.send_message("❌ El monto debe ser mayor a $0.", ephemeral=True)
    if user["efectivo"] < monto: return await interaction.response.send_message(f"❌ Efectivo insuficiente. Tienes **{clp(user['efectivo'])}**.", ephemeral=True)
    user["efectivo"] -= monto; user["banco"] += monto
    agregar_xp(user, 5); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DEPÓSITO", monto, f"Depósito de {clp(monto)}")
    em = discord.Embed(title="✅ Depósito Exitoso", color=COLOR_EXITO,
        description=f"Depositaste **{clp(monto)}** en tu banco.\n🏦 Nuevo saldo banco: **{clp(user['banco'])}**")
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="retirar", description="Sacar dinero del cajero (Banco → Efectivo)")
@app_commands.describe(monto="Monto en CLP a retirar")
async def debito_retirar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto <= 0: return await interaction.response.send_message("❌ El monto debe ser mayor a $0.", ephemeral=True)
    if user["banco"] < monto: return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    user["banco"] -= monto; user["efectivo"] += monto
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "RETIRO", monto, f"Retiro de {clp(monto)}")
    em = discord.Embed(title="🏧 Retiro Exitoso", color=COLOR_EXITO,
        description=f"Retiraste **{clp(monto)}** del banco.\n💵 Efectivo: **{clp(user['efectivo'])}**")
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_debito.command(name="transferir", description="Transferir dinero a otro usuario (Banco → Banco)")
@app_commands.describe(usuario="Usuario a quien transferir", monto="Monto en CLP")
async def debito_transferir(interaction: discord.Interaction, usuario: discord.Member, monto: int):
    if usuario.id == interaction.user.id: return await interaction.response.send_message("❌ No puedes transferirte a ti mismo.", ephemeral=True)
    if usuario.bot: return await interaction.response.send_message("❌ No puedes transferir a un bot.", ephemeral=True)
    if monto <= 0: return await interaction.response.send_message("❌ El monto debe ser mayor a $0.", ephemeral=True)
    user = get_user(interaction.user.id)
    if not user["tarjeta_debito"]: return await interaction.response.send_message("❌ Necesitas una **tarjeta de débito** para transferir.", ephemeral=True)
    if user["banco"] < monto: return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    receptor = get_user(usuario.id)
    user["banco"] -= monto; receptor["banco"] += monto
    agregar_xp(user, 10); save_user(interaction.user.id, user); save_user(usuario.id, receptor)
    add_historial(interaction.user.id, "TRANSFERENCIA", -monto, f"Transferencia a {usuario.display_name}")
    add_historial(usuario.id, "TRANSFERENCIA", monto, f"Transferencia de {interaction.user.display_name}")
    em = discord.Embed(title="➡️ Transferencia Exitosa", color=COLOR_EXITO,
        description=f"Transferiste **{clp(monto)}** a **{usuario.display_name}**\n🏦 Tu saldo: **{clp(user['banco'])}**")
    em.set_footer(text="🏦 Banco Alianza Santander")
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
    if monto < 10_000: return await interaction.response.send_message("❌ El monto mínimo es **$10.000 CLP**.", ephemeral=True)
    if user["banco"] < monto: return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    if len(user["cuentas_ahorro"]) >= 3: return await interaction.response.send_message("❌ Máximo **3 cuentas de ahorro**.", ephemeral=True)
    user["banco"] -= monto
    user["cuentas_ahorro"].append({"id":int(datetime.now().timestamp()),"saldo":monto,"apertura":datetime.now().strftime("%d/%m/%Y")})
    agregar_xp(user, 20); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_ABRIR", monto, f"Cuenta de ahorro abierta con {clp(monto)}")
    em = discord.Embed(title="✅ Cuenta de Ahorro Abierta", color=COLOR_EXITO,
        description=f"Depositaste **{clp(monto)}** en tu nueva cuenta.\n📈 Tasa: **{int(TASA_AHORRO*100)}% semanal**")
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="ver", description="Ver tus cuentas de ahorro")
async def ahorro_ver(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]: return await interaction.response.send_message("❌ No tienes cuentas de ahorro. Usa `/ahorro abrir`.", ephemeral=True)
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
    if not user["cuentas_ahorro"]: return await interaction.response.send_message("❌ No tienes cuentas de ahorro.", ephemeral=True)
    if user["banco"] < monto: return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    user["banco"] -= monto; user["cuentas_ahorro"][0]["saldo"] += monto
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_DEPÓSITO", monto, f"Depósito en ahorro {clp(monto)}")
    em = discord.Embed(title="✅ Depósito en Ahorro", color=COLOR_EXITO,
        description=f"Depositaste **{clp(monto)}**.\nNuevo saldo: **{clp(user['cuentas_ahorro'][0]['saldo'])}**")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="retirar", description="Retirar de tu cuenta de ahorro")
@app_commands.describe(monto="Monto en CLP")
async def ahorro_retirar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]: return await interaction.response.send_message("❌ No tienes cuentas de ahorro.", ephemeral=True)
    if user["cuentas_ahorro"][0]["saldo"] < monto: return await interaction.response.send_message(f"❌ Saldo insuficiente en ahorro. Tienes **{clp(user['cuentas_ahorro'][0]['saldo'])}**.", ephemeral=True)
    user["cuentas_ahorro"][0]["saldo"] -= monto; user["banco"] += monto
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_RETIRO", monto, f"Retiro de ahorro {clp(monto)}")
    em = discord.Embed(title="✅ Retiro de Ahorro", color=COLOR_EXITO,
        description=f"Retiraste **{clp(monto)}** de tu ahorro al banco.")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="cerrar", description="Cerrar tu cuenta de ahorro")
async def ahorro_cerrar(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    if not user["cuentas_ahorro"]: return await interaction.response.send_message("❌ No tienes cuentas de ahorro.", ephemeral=True)
    cuenta = user["cuentas_ahorro"].pop(0); user["banco"] += cuenta["saldo"]
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AHORRO_CERRAR", cuenta["saldo"], "Cuenta de ahorro cerrada")
    em = discord.Embed(title="⚠️ Cuenta de Ahorro Cerrada", color=COLOR_ADVERTENCIA,
        description=f"Se devolvieron **{clp(cuenta['saldo'])}** a tu banco.")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_ahorro.command(name="calcular", description="Calcular rendimiento de un ahorro")
@app_commands.describe(monto="Monto inicial en CLP", semanas="Número de semanas (1-52)")
async def ahorro_calcular(interaction: discord.Interaction, monto: int, semanas: int):
    semanas = max(1, min(52, semanas))
    acumulado = monto * ((1 + TASA_AHORRO) ** semanas)
    ganancia = acumulado - monto
    em = discord.Embed(title="📊 Calculadora de Ahorro", color=COLOR_INFO)
    em.add_field(name="💵 Monto inicial",     value=clp(monto),                 inline=True)
    em.add_field(name="📅 Semanas",           value=str(semanas),               inline=True)
    em.add_field(name="📈 Tasa semanal",      value=f"{int(TASA_AHORRO*100)}%", inline=True)
    em.add_field(name="💰 Ganancia estimada", value=clp(int(ganancia)),         inline=True)
    em.add_field(name="🏆 Total estimado",    value=clp(int(acumulado)),        inline=True)
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
    if not user["prestamos"]: return await interaction.response.send_message("✅ No tienes préstamos activos.", ephemeral=True)
    em = discord.Embed(title="📋 Mis Préstamos Activos", color=COLOR_ADVERTENCIA)
    for i, p in enumerate(user["prestamos"], 1):
        em.add_field(name=f"Préstamo #{i}",
            value=f"Total: **{clp(p['total'])}**\nCuota: **{clp(p['cuota'])}**\nSemanas: **{p['semanas_restantes']}**\nMotivo: *{p['motivo'][:40]}*",
            inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_prestamo.command(name="pagar", description="Realizar un pago a tu préstamo")
@app_commands.describe(monto="Monto en CLP a pagar")
async def prestamo_pagar(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if not user["prestamos"]: return await interaction.response.send_message("✅ No tienes préstamos activos.", ephemeral=True)
    if user["banco"] < monto: return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    user["banco"] -= monto; restante = monto; nuevos = []
    for p in user["prestamos"]:
        if restante <= 0: nuevos.append(p); continue
        pago = min(restante, p["total"]); p["total"] -= pago; restante -= pago
        if p["total"] > 0: nuevos.append(p)
    user["prestamos"] = nuevos
    agregar_xp(user, 15); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "PRÉSTAMO_PAGO", -monto, f"Pago préstamo {clp(monto)}")
    em = discord.Embed(title="✅ Pago Realizado", color=COLOR_EXITO,
        description=f"Pagaste **{clp(monto)}**.\nPréstamos restantes: **{len(user['prestamos'])}**")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_prestamo.command(name="calcular", description="Calcular cuotas de un préstamo")
@app_commands.describe(monto="Monto solicitado en CLP", semanas="1, 2 o 3 semanas")
async def prestamo_calcular(interaction: discord.Interaction, monto: int, semanas: int):
    semanas = max(1, min(3, semanas))
    interes = {1: 0.05, 2: 0.10, 3: 0.15}[semanas]
    total = int(monto * (1 + interes)); cuota = total // semanas
    em = discord.Embed(title="🧮 Calculadora de Préstamo", color=COLOR_INFO)
    em.add_field(name="💵 Monto",         value=clp(monto),             inline=True)
    em.add_field(name="📅 Plazo",         value=f"{semanas} semana(s)", inline=True)
    em.add_field(name="📈 Interés",       value=f"{int(interes*100)}%", inline=True)
    em.add_field(name="💰 Total a pagar", value=clp(total),             inline=True)
    em.add_field(name="📋 Cuota semanal", value=clp(cuota),             inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_prestamo.command(name="ayuda", description="Información sobre préstamos")
async def prestamo_ayuda(interaction: discord.Interaction):
    em = discord.Embed(title="ℹ️ Información de Préstamos", color=COLOR_INFO,
        description="Para solicitar un préstamo usa **/banco** → Solicitar Préstamo.")
    em.add_field(name="📈 Tasas", value="• 1 semana: **5%**\n• 2 semanas: **10%**\n• 3 semanas: **15%**", inline=False)
    em.add_field(name="📋 Requisitos", value="• Tarjeta de débito activa\n• Monto mínimo: **$10.000 CLP**", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

bot.tree.add_command(grupo_prestamo)

# ══════════════════════════════════════════════════════════════
# 🪙 /cripto — 15 MONEDAS — BUG COMPRAR ARREGLADO
# ══════════════════════════════════════════════════════════════
grupo_cripto = app_commands.Group(name="cripto", description="🪙 Mercado de criptomonedas", guild_ids=[GUILD_ID])

@grupo_cripto.command(name="mercado", description="Ver el precio actual de TODAS las criptomonedas")
async def cripto_mercado(interaction: discord.Interaction):
    db = cargar_db(); precios = get_precios_cripto(db)
    em = discord.Embed(title="🪙 Mercado Cripto — Gran Chile RP",
        description="**15 criptomonedas disponibles** • Precios en CLP 🇨🇱 • Se actualizan cada hora",
        color=COLOR_CRIPTO)
    em.add_field(name="━━━ 🌍 MONEDAS REALES ━━━", value="\u200b", inline=False)
    for k in ["BTC","ETH","SOL","DOGE","ADA"]:
        info = CRIPTO_INFO[k]
        em.add_field(name=f"{info['icon']} {info['emoji']} {k}", value=f"**{clp(precios.get(k,0))}**", inline=True)
    em.add_field(name="━━━ 🇨🇱 MONEDAS GRAN CHILE RP ━━━", value="\u200b", inline=False)
    for k in ["CLPX","COND","LATA","PESC","COBRE","FLAITE","HUASO","ANDIN","CUECA","RUCAF"]:
        info = CRIPTO_INFO[k]
        em.add_field(name=f"{info['icon']} {info['emoji']} {k}", value=f"**{clp(precios.get(k,0))}**", inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • /cripto info <moneda> para detalles • /cripto comprar para invertir")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

@grupo_cripto.command(name="info", description="Ver información detallada de una criptomoneda")
@app_commands.describe(moneda="Símbolo: BTC, ETH, SOL, DOGE, ADA, CLPX, COND, LATA, PESC, COBRE, FLAITE, HUASO, ANDIN, CUECA, RUCAF")
async def cripto_info(interaction: discord.Interaction, moneda: str):
    moneda = moneda.upper().strip()
    if moneda not in CRIPTO_INFO:
        return await interaction.response.send_message(
            f"❌ Moneda no encontrada.\nDisponibles: **{', '.join(CRIPTO_INFO.keys())}**", ephemeral=True)
    db = cargar_db(); precios = get_precios_cripto(db)
    info = CRIPTO_INFO[moneda]; precio = precios.get(moneda, 0); base = CRIPTO_BASE.get(moneda, 1)
    variacion = ((precio - base) / base) * 100
    tendencia = "📈" if variacion >= 0 else "📉"
    em = discord.Embed(title=f"{info['icon']} {info['nombre']} ({moneda})", description=info["desc"], color=COLOR_CRIPTO)
    em.add_field(name="💰 Precio actual",       value=clp(precio),             inline=True)
    em.add_field(name=f"{tendencia} Variación", value=f"{variacion:+.2f}%",    inline=True)
    em.add_field(name="📊 Precio base",         value=clp(base),               inline=True)
    em.add_field(name="🔤 Símbolo",             value=f"`{moneda}`",            inline=True)
    em.add_field(name="⛓️ Tipo",
        value="🌍 Moneda Real" if moneda in ["BTC","ETH","SOL","DOGE","ADA"] else "🇨🇱 Exclusiva Gran Chile RP",
        inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • /cripto comprar para invertir")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

@grupo_cripto.command(name="comprar", description="Comprar criptomonedas con pesos chilenos")
@app_commands.describe(
    moneda="Símbolo (BTC, ETH, SOL, DOGE, ADA, CLPX, COND, LATA, PESC, COBRE, FLAITE, HUASO, ANDIN, CUECA, RUCAF)",
    monto="Monto en CLP a invertir (mínimo $1.000)")
async def cripto_comprar(interaction: discord.Interaction, moneda: str, monto: int):
    await interaction.response.defer(ephemeral=True)
    moneda = moneda.upper().strip()
    if moneda not in CRIPTO_INFO:
        return await interaction.followup.send(
            f"❌ Moneda no disponible.\nDisponibles: **{', '.join(CRIPTO_INFO.keys())}**", ephemeral=True)
    if monto < 1_000:
        return await interaction.followup.send("❌ Monto mínimo de compra: **$1.000 CLP**", ephemeral=True)
    user = get_user(interaction.user.id)
    if user["banco"] < monto:
        return await interaction.followup.send(f"❌ Saldo insuficiente.\nTienes: **{clp(user['banco'])}** en banco.\nNecesitas: **{clp(monto)}**", ephemeral=True)
    db = cargar_db(); precios = get_precios_cripto(db)
    info = CRIPTO_INFO[moneda]; precio_unitario = precios[moneda]
    cantidad = monto / precio_unitario
    user["banco"] -= monto
    if "cripto" not in user: user["cripto"] = {}
    user["cripto"][moneda] = user["cripto"].get(moneda, 0) + cantidad
    agregar_xp(user, 10); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "CRIPTO_COMPRA", monto, f"Compra {cantidad:.6f} {moneda}")
    em = discord.Embed(title=f"✅ Compra de {info['nombre']} Exitosa", color=COLOR_EXITO)
    em.add_field(name=f"{info['icon']} Moneda",    value=f"{info['emoji']} **{moneda}**",  inline=True)
    em.add_field(name="💰 Invertido",              value=clp(monto),                        inline=True)
    em.add_field(name="📦 Cantidad obtenida",      value=f"{cantidad:.8f} {moneda}",        inline=True)
    em.add_field(name="💹 Precio unitario",        value=clp(precio_unitario),              inline=True)
    em.add_field(name="🏦 Saldo banco restante",   value=clp(user["banco"]),               inline=True)
    em.add_field(name=f"🪙 Total {moneda} en cartera", value=f"{user['cripto'][moneda]:.8f}", inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • /cripto portafolio para ver tus inversiones")
    await interaction.followup.send(embed=em, ephemeral=True)

@grupo_cripto.command(name="vender", description="Vender criptomonedas por pesos chilenos")
@app_commands.describe(
    moneda="Símbolo de la moneda a vender",
    cantidad="Cantidad a vender (Ej: 0.001 para BTC)")
async def cripto_vender(interaction: discord.Interaction, moneda: str, cantidad: float):
    await interaction.response.defer(ephemeral=True)
    moneda = moneda.upper().strip()
    if moneda not in CRIPTO_INFO:
        return await interaction.followup.send("❌ Moneda no encontrada.", ephemeral=True)
    user = get_user(interaction.user.id)
    saldo_actual = user.get("cripto", {}).get(moneda, 0)
    if saldo_actual < cantidad:
        return await interaction.followup.send(
            f"❌ No tienes suficiente **{moneda}**.\nTienes: **{saldo_actual:.8f} {moneda}**\nQuieres vender: **{cantidad:.8f} {moneda}**",
            ephemeral=True)
    db = cargar_db(); precios = get_precios_cripto(db)
    info = CRIPTO_INFO[moneda]; ganancia = int(cantidad * precios[moneda])
    if "cripto" not in user: user["cripto"] = {}
    user["cripto"][moneda] = saldo_actual - cantidad
    user["banco"] += ganancia
    agregar_xp(user, 10); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "CRIPTO_VENTA", ganancia, f"Venta {cantidad:.6f} {moneda}")
    em = discord.Embed(title=f"✅ Venta de {info['nombre']} Exitosa", color=COLOR_EXITO)
    em.add_field(name=f"{info['icon']} Moneda",    value=f"{info['emoji']} **{moneda}**",  inline=True)
    em.add_field(name="📦 Cantidad vendida",        value=f"{cantidad:.8f} {moneda}",       inline=True)
    em.add_field(name="💰 CLP recibidos",           value=clp(ganancia),                    inline=True)
    em.add_field(name="💹 Precio unitario",         value=clp(precios[moneda]),             inline=True)
    em.add_field(name="🏦 Nuevo saldo banco",       value=clp(user["banco"]),              inline=True)
    em.add_field(name=f"🪙 {moneda} restante",      value=f"{user['cripto'][moneda]:.8f}", inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.followup.send(embed=em, ephemeral=True)

@grupo_cripto.command(name="portafolio", description="Ver todas tus criptomonedas y su valor actual")
async def cripto_portafolio(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    db = cargar_db(); precios = get_precios_cripto(db)
    entradas = [(k,v) for k,v in user.get("cripto",{}).items() if v > 0.000001]
    em = discord.Embed(title="💼 Mi Portafolio Cripto — Banco Alianza Santander", color=COLOR_CRIPTO)
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    if not entradas:
        em.description = "*Sin criptomonedas.*\nUsa `/cripto mercado` para ver las 15 disponibles\ny `/cripto comprar` para invertir."
    else:
        total = 0
        for k, v in entradas:
            val = int(v * precios.get(k, 0)); total += val
            info = CRIPTO_INFO.get(k, {"icon":"🪙","emoji":"🪙"})
            em.add_field(name=f"{info['icon']} {info['emoji']} {k}",
                value=f"Cant: **{v:.6f}**\nValor: **{clp(val)}**", inline=True)
        em.add_field(name="\u200b", value="\u200b", inline=False)
        em.add_field(name="📊 Valor Total en Cripto", value=f"**{clp(total)}**", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_cripto.command(name="grafica", description="Ver gráfico histórico de precio de una criptomoneda")
@app_commands.describe(moneda="Símbolo de la moneda")
async def cripto_grafica(interaction: discord.Interaction, moneda: str):
    moneda = moneda.upper().strip()
    if moneda not in CRIPTO_INFO:
        return await interaction.response.send_message("❌ Moneda no encontrada.", ephemeral=True)
    db = cargar_db(); precios = get_precios_cripto(db)
    info = CRIPTO_INFO[moneda]; base = precios.get(moneda, CRIPTO_BASE.get(moneda, 1000))
    dias = ["Lun","Mar","Mié","Jue","Vie","Sáb","Hoy"]
    puntos = [int(base*(1+random.uniform(-0.10,0.10))) for _ in range(7)]
    grafica = "\n".join(f"`{dias[i]}` → **{clp(p)}**" for i,p in enumerate(puntos))
    tendencia = "📈" if puntos[-1] >= puntos[0] else "📉"
    variacion = ((puntos[-1]-puntos[0])/puntos[0])*100
    em = discord.Embed(title=f"📊 {tendencia} {info['nombre']} ({moneda}) — Últimos 7 días",
        color=COLOR_CRIPTO, description=grafica)
    em.add_field(name="📈 Variación semanal", value=f"{variacion:+.2f}%",    inline=True)
    em.add_field(name="💰 Precio actual",     value=clp(precios[moneda]),    inline=True)
    em.add_field(name="🔺 Máximo semana",     value=clp(max(puntos)),        inline=True)
    em.add_field(name="🔻 Mínimo semana",     value=clp(min(puntos)),        inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Datos simulados para Gran Chile RP")
    await interaction.response.send_message(embed=em, ephemeral=True)

bot.tree.add_command(grupo_cripto)

# ══════════════════════════════════════════════════════════════
# 📈 /bolsa
# ══════════════════════════════════════════════════════════════
grupo_bolsa = app_commands.Group(name="bolsa", description="📈 Mercado de valores", guild_ids=[GUILD_ID])

@grupo_bolsa.command(name="ver", description="Ver el mercado de valores actual")
async def bolsa_ver(interaction: discord.Interaction):
    db = cargar_db(); precios = get_precios_acciones(db)
    em = discord.Embed(title="📈 Bolsa de Valores — Gran Chile RP", color=0x00A650,
        description="Acciones chilenas disponibles (precio por acción en CLP)")
    for k, v in precios.items():
        em.add_field(name=f"🏢 {k}", value=clp(v), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Precios actualizados cada hora")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

@grupo_bolsa.command(name="comprar", description="Comprar acciones")
@app_commands.describe(empresa="COPEC, FALABELLA, BCI, CMPC, ENTEL, LATAM, CENCOSUD", cantidad="Número de acciones")
async def bolsa_comprar(interaction: discord.Interaction, empresa: str, cantidad: int):
    empresa = empresa.upper(); db = cargar_db(); precios = get_precios_acciones(db)
    if empresa not in precios:
        return await interaction.response.send_message(f"❌ Empresa no encontrada. Opciones: **{', '.join(precios.keys())}**", ephemeral=True)
    user = get_user(interaction.user.id); costo = precios[empresa] * cantidad
    if user["banco"] < costo:
        return await interaction.response.send_message(f"❌ Necesitas **{clp(costo)}**. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    user["banco"] -= costo
    user["acciones"][empresa] = user["acciones"].get(empresa, 0) + cantidad
    agregar_xp(user, 15); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "BOLSA_COMPRA", costo, f"Compra {cantidad} acciones {empresa}")
    em = discord.Embed(title="✅ Acciones Compradas", color=COLOR_EXITO)
    em.add_field(name="🏢 Empresa",  value=empresa,               inline=True)
    em.add_field(name="📦 Cantidad", value=f"{cantidad} acciones", inline=True)
    em.add_field(name="💰 Pagado",   value=clp(costo),            inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_bolsa.command(name="vender", description="Vender acciones")
@app_commands.describe(empresa="Empresa", cantidad="Número de acciones a vender")
async def bolsa_vender(interaction: discord.Interaction, empresa: str, cantidad: int):
    empresa = empresa.upper(); db = cargar_db(); precios = get_precios_acciones(db)
    user = get_user(interaction.user.id)
    if user["acciones"].get(empresa, 0) < cantidad:
        return await interaction.response.send_message(f"❌ No tienes suficientes acciones de **{empresa}**.", ephemeral=True)
    precio_venta = int(precios.get(empresa, 0) * cantidad * random.uniform(0.95, 1.05))
    user["acciones"][empresa] -= cantidad; user["banco"] += precio_venta
    agregar_xp(user, 15); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "BOLSA_VENTA", precio_venta, f"Venta {cantidad} acciones {empresa}")
    em = discord.Embed(title="✅ Acciones Vendidas", color=COLOR_EXITO)
    em.add_field(name="🏢 Empresa",  value=empresa,               inline=True)
    em.add_field(name="📦 Cantidad", value=f"{cantidad} acciones", inline=True)
    em.add_field(name="💰 Recibido", value=clp(precio_venta),     inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_bolsa.command(name="portafolio", description="Ver tus inversiones en bolsa")
async def bolsa_portafolio(interaction: discord.Interaction):
    user = get_user(interaction.user.id); db = cargar_db(); precios = get_precios_acciones(db)
    entradas = [(k,v) for k,v in user.get("acciones",{}).items() if v > 0]
    em = discord.Embed(title="💼 Mi Portafolio Bolsa", color=0x00A650)
    if not entradas:
        em.description = "*Sin inversiones. Usa `/bolsa comprar` para invertir.*"
    else:
        total = 0
        for k, v in entradas:
            val = int(v * precios.get(k, 0)); total += val
            em.add_field(name=f"🏢 {k}", value=f"Acciones: **{v}**\nValor: **{clp(val)}**", inline=True)
        em.add_field(name="📊 Valor Total", value=f"**{clp(total)}**", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

bot.tree.add_command(grupo_bolsa)

# ══════════════════════════════════════════════════════════════
# 🚗 /auto — ARREGLADO: Modal directo sin followup
# ══════════════════════════════════════════════════════════════
grupo_auto = app_commands.Group(name="auto", description="🚗 Sistema de registro de vehículos", guild_ids=[GUILD_ID])

class ModalRegistrarAuto(discord.ui.Modal, title="🚗 Registrar Vehículo — Gran Chile RP"):
    marca     = discord.ui.TextInput(label="Marca del vehículo",        placeholder="Ej: Toyota, BMW, Ford, Chevrolet...")
    modelo    = discord.ui.TextInput(label="Modelo",                    placeholder="Ej: Corolla, M3, Mustang, Spark...")
    anio      = discord.ui.TextInput(label="Año (1980-2025)",           placeholder="Ej: 2022", max_length=4)
    color_v   = discord.ui.TextInput(label="Color",                     placeholder="Ej: Rojo Metálico, Negro, Blanco...")
    categoria = discord.ui.TextInput(label="Categoría",                 placeholder="normal / deportivo / suv / lujo / moto / camion")

    async def on_submit(self, interaction: discord.Interaction):
        cat = str(self.categoria).lower().strip()
        if cat not in CATEGORIAS_AUTO:
            return await interaction.response.send_message(
                f"❌ Categoría inválida.\nOpciones disponibles: **{', '.join(CATEGORIAS_AUTO.keys())}**",
                ephemeral=True)
        try:
            anio_int = int(str(self.anio).strip())
            if anio_int < 1980 or anio_int > 2025: raise ValueError
        except ValueError:
            return await interaction.response.send_message(
                "❌ Año inválido. Debe estar entre **1980** y **2025**.", ephemeral=True)

        user = get_user(interaction.user.id)
        info_cat = CATEGORIAS_AUTO[cat]

        if user["banco"] < info_cat["costo_registro"]:
            return await interaction.response.send_message(
                f"❌ Saldo insuficiente en banco.\n"
                f"Costo de registro: **{clp(info_cat['costo_registro'])}**\n"
                f"Tu banco: **{clp(user['banco'])}**",
                ephemeral=True)

        # Generar matrícula única
        matricula = generar_matricula()
        db = cargar_db()
        todas = [a["matricula"] for u in db["users"].values() for a in u.get("autos", [])]
        intentos = 0
        while matricula in todas and intentos < 100:
            matricula = generar_matricula(); intentos += 1

        auto = {
            "id":             random.randint(100000, 999999),
            "marca":          str(self.marca).strip().title(),
            "modelo":         str(self.modelo).strip().title(),
            "anio":           anio_int,
            "color":          str(self.color_v).strip().title(),
            "categoria":      cat,
            "matricula":      matricula,
            "mensualidad":    info_cat["mensualidad"],
            "ultimo_pago":    datetime.now().strftime("%d/%m/%Y"),
            "fecha_registro": datetime.now().strftime("%d/%m/%Y"),
        }

        user["banco"] -= info_cat["costo_registro"]
        if "autos" not in user: user["autos"] = []
        user["autos"].append(auto)
        agregar_xp(user, 50)
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "AUTO_REGISTRO", info_cat["costo_registro"],
            f"Registro {auto['marca']} {auto['modelo']} — {matricula}")

        em = discord.Embed(
            title="🚗 ¡Vehículo Registrado Exitosamente!",
            description="Tu vehículo ha sido registrado en el **Registro Civil de Vehículos** de Gran Chile RP.",
            color=COLOR_AUTO)
        em.add_field(name="🚘 Vehículo",         value=f"**{auto['marca']} {auto['modelo']}**", inline=True)
        em.add_field(name="📅 Año",              value=str(auto["anio"]),                       inline=True)
        em.add_field(name="🎨 Color",            value=auto["color"],                           inline=True)
        em.add_field(name="🏷️ Categoría",        value=info_cat["nombre"],                      inline=True)
        em.add_field(name="💰 Costo Registro",   value=clp(info_cat["costo_registro"]),         inline=True)
        em.add_field(name="📆 Mensualidad",       value=clp(info_cat["mensualidad"]),            inline=True)
        em.add_field(
            name="🪪 ══ MATRÍCULA OFICIAL ══",
            value=f"```\n{matricula}\n```\n📌 *Anota esta matrícula para usarla en Liberty Point RP*",
            inline=False)
        em.add_field(name="🏦 Saldo banco restante", value=clp(user["banco"]), inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander • Registro Civil de Vehículos | Gran Chile RP")
        em.timestamp = datetime.now()
        await interaction.response.send_message(embed=em)

@grupo_auto.command(name="registrar", description="🚗 Registrar un nuevo vehículo y obtener matrícula oficial")
async def auto_registrar(interaction: discord.Interaction):
    # Mostrar precios DENTRO del modal — se abre directo
    em = discord.Embed(
        title="🚗 Tarifas de Registro — Gran Chile RP",
        description="Revisa los costos y luego usa el botón para abrir el formulario.",
        color=COLOR_AUTO)
    for clave, info in CATEGORIAS_AUTO.items():
        em.add_field(
            name=info["nombre"],
            value=f"Registro: **{clp(info['costo_registro'])}**\nMensualidad: **{clp(info['mensualidad'])}**",
            inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • El costo de registro se descuenta de tu banco")

    class BtnAuto(discord.ui.View):
        def __init__(self): super().__init__(timeout=120)
        @discord.ui.button(label="📋 Abrir Formulario de Registro", style=discord.ButtonStyle.primary, emoji="🚗")
        async def abrir(self, intr: discord.Interaction, button: discord.ui.Button):
            await intr.response.send_modal(ModalRegistrarAuto())

    await interaction.response.send_message(embed=em, view=BtnAuto(), ephemeral=True)

@grupo_auto.command(name="mis_autos", description="🚗 Ver todos tus vehículos registrados")
async def auto_mis_autos(interaction: discord.Interaction):
    user = get_user(interaction.user.id); autos = user.get("autos", [])
    if not autos:
        return await interaction.response.send_message(
            "❌ No tienes vehículos registrados.\nUsa `/auto registrar` para agregar uno.", ephemeral=True)
    em = discord.Embed(title="🚗 Mis Vehículos Registrados — Gran Chile RP", color=COLOR_AUTO)
    for a in autos:
        cat = CATEGORIAS_AUTO.get(a["categoria"], {})
        em.add_field(
            name=f"{cat.get('nombre','🚗')} {a['marca']} {a['modelo']} ({a['anio']})",
            value=(f"🎨 Color: **{a['color']}**\n"
                   f"🪪 Matrícula: `{a['matricula']}`\n"
                   f"📆 Mensualidad: **{clp(a['mensualidad'])}**\n"
                   f"💳 Último pago: {a['ultimo_pago']}\n"
                   f"📅 Registrado: {a['fecha_registro']}"),
            inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander • Registro Civil de Vehículos | Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_auto.command(name="pagar_mensualidad", description="💳 Pagar la mensualidad de tu vehículo")
@app_commands.describe(matricula="Matrícula del vehículo (Ej: AB·1234·CD)")
async def auto_pagar_mensualidad(interaction: discord.Interaction, matricula: str):
    user = get_user(interaction.user.id); matricula = matricula.upper().strip()
    auto = next((a for a in user.get("autos",[]) if a["matricula"] == matricula), None)
    if not auto:
        return await interaction.response.send_message(f"❌ No se encontró el vehículo con matrícula `{matricula}`.\nUsa `/auto mis_autos` para ver tus vehículos.", ephemeral=True)
    mensualidad = auto["mensualidad"]
    if user["banco"] < mensualidad:
        return await interaction.response.send_message(
            f"❌ Saldo insuficiente.\nMensualidad: **{clp(mensualidad)}**\nTienes en banco: **{clp(user['banco'])}**", ephemeral=True)
    user["banco"] -= mensualidad; auto["ultimo_pago"] = datetime.now().strftime("%d/%m/%Y")
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AUTO_MENSUALIDAD", mensualidad, f"Mensualidad {auto['marca']} {auto['modelo']} ({matricula})")
    em = discord.Embed(title="✅ Mensualidad Pagada", color=COLOR_EXITO,
        description=f"Pagaste la mensualidad de tu **{auto['marca']} {auto['modelo']}**.")
    em.add_field(name="🪪 Matrícula",    value=f"`{matricula}`",    inline=True)
    em.add_field(name="💰 Monto pagado", value=clp(mensualidad),   inline=True)
    em.add_field(name="🏦 Saldo banco",  value=clp(user["banco"]), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

@grupo_auto.command(name="info", description="🔍 Ver detalles de un vehículo por matrícula")
@app_commands.describe(matricula="Matrícula del vehículo (Ej: AB·1234·CD)")
async def auto_info(interaction: discord.Interaction, matricula: str):
    matricula = matricula.upper().strip(); db = cargar_db()
    # Buscar en todos los usuarios
    encontrado = None; propietario_id = None
    for uid, data in db["users"].items():
        for a in data.get("autos", []):
            if a["matricula"] == matricula:
                encontrado = a; propietario_id = uid; break
        if encontrado: break
    if not encontrado:
        return await interaction.response.send_message(f"❌ No se encontró ningún vehículo con matrícula `{matricula}`.", ephemeral=True)
    cat = CATEGORIAS_AUTO.get(encontrado["categoria"], {})
    em = discord.Embed(title=f"🔍 Información del Vehículo — `{matricula}`", color=COLOR_AUTO)
    em.add_field(name="🚘 Vehículo",     value=f"**{encontrado['marca']} {encontrado['modelo']}**", inline=True)
    em.add_field(name="📅 Año",          value=str(encontrado["anio"]),                              inline=True)
    em.add_field(name="🎨 Color",        value=encontrado["color"],                                  inline=True)
    em.add_field(name="🏷️ Categoría",   value=cat.get("nombre","Desconocido"),                      inline=True)
    em.add_field(name="📆 Registrado",   value=encontrado["fecha_registro"],                         inline=True)
    em.add_field(name="💳 Último pago",  value=encontrado["ultimo_pago"],                            inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Registro Civil de Vehículos")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_auto.command(name="vender", description="💸 Vender un vehículo registrado")
@app_commands.describe(matricula="Matrícula del vehículo a vender")
async def auto_vender(interaction: discord.Interaction, matricula: str):
    user = get_user(interaction.user.id); matricula = matricula.upper().strip()
    auto = next((a for a in user.get("autos",[]) if a["matricula"] == matricula), None)
    if not auto:
        return await interaction.response.send_message(f"❌ No se encontró el vehículo con matrícula `{matricula}`.", ephemeral=True)
    cat = CATEGORIAS_AUTO.get(auto["categoria"], {})
    valor_venta = int(cat.get("costo_registro", 0) * random.uniform(0.55, 0.75))
    user["autos"] = [a for a in user.get("autos",[]) if a["matricula"] != matricula]
    user["banco"] += valor_venta
    agregar_xp(user, 20); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "AUTO_VENTA", valor_venta, f"Venta {auto['marca']} {auto['modelo']} ({matricula})")
    em = discord.Embed(title="💸 Vehículo Vendido", color=COLOR_ADVERTENCIA,
        description=f"Vendiste tu **{auto['marca']} {auto['modelo']}** y recibiste **{clp(valor_venta)}**.")
    em.add_field(name="🪪 Matrícula", value=f"`{matricula}`",  inline=True)
    em.add_field(name="💰 Recibido",  value=clp(valor_venta), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

bot.tree.add_command(grupo_auto)

# ══════════════════════════════════════════════════════════════
# ₿ /bitcoin precio
# ══════════════════════════════════════════════════════════════
grupo_bitcoin = app_commands.Group(name="bitcoin", description="₿ Bitcoin", guild_ids=[GUILD_ID])

@grupo_bitcoin.command(name="precio", description="Ver el precio actual de Bitcoin y estado de la red")
async def bitcoin_precio(interaction: discord.Interaction):
    db = cargar_db(); precios = get_precios_cripto(db)
    variacion = random.uniform(-8, 8)
    em = discord.Embed(title="₿ Bitcoin — Precio Actual", color=COLOR_CRIPTO)
    em.add_field(name="💰 Precio CLP",    value=clp(precios["BTC"]),                  inline=True)
    em.add_field(name="📈 Variación 24h", value=f"{variacion:+.2f}%",                 inline=True)
    em.add_field(name="🌐 Estado de Red", value="🟢 Operacional",                     inline=True)
    em.add_field(name="⛏️ Dificultad",    value="Alta",                               inline=True)
    em.add_field(name="📦 Bloque actual", value=f"#{random.randint(800000,850000):,}", inline=True)
    em.add_field(name="⚡ Hashrate",      value=f"{random.randint(400,600)} EH/s",    inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Usa /cripto mercado para ver las 15 monedas disponibles")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

bot.tree.add_command(grupo_bitcoin)

# ══════════════════════════════════════════════════════════════
# 💼 /colectar
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="colectar", description="💼 Colectar tu salario (cada 72 horas)")
async def colectar(interaction: discord.Interaction):
    user = get_user(interaction.user.id); ahora = datetime.now(); espera = timedelta(hours=72)
    if user["ultimo_colectar"]:
        ultimo = datetime.fromisoformat(user["ultimo_colectar"])
        if ahora - ultimo < espera:
            restante = espera - (ahora - ultimo)
            h, rem = divmod(int(restante.total_seconds()), 3600); m = rem // 60
            return await interaction.response.send_message(
                embed=discord.Embed(title="⏳ Aún no puedes colectar", color=COLOR_ERROR,
                    description=f"Podrás colectar en **{h}h {m}m**\n🔥 Racha actual: **{user.get('rachas',0)} días**"),
                ephemeral=True)
    salario = random.randint(75_000, 100_000)
    user["efectivo"] += salario; user["ultimo_colectar"] = ahora.isoformat()
    user["rachas"] = user.get("rachas", 0) + 1
    nivel, subio = agregar_xp(user, 25); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "SALARIO", salario, f"Salario cobrado {clp(salario)}")
    desc = f"Recibiste **{clp(salario)}** en efectivo.\n🔥 Racha: **{user['rachas']} días**"
    if subio: desc += f"\n⭐ **¡Subiste al nivel {nivel}!**"
    em = discord.Embed(title="💼 ¡Salario Cobrado! — Banco Alianza Santander", color=COLOR_EXITO, description=desc)
    em.set_footer(text="🏦 Banco Alianza Santander | Próxima colecta en 72 horas")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 🎁 /diario
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="diario", description="🎁 Reclamar tu recompensa diaria")
async def diario(interaction: discord.Interaction):
    user = get_user(interaction.user.id); ahora = datetime.now(); espera = timedelta(hours=24)
    if user["ultimo_diario"]:
        ultimo = datetime.fromisoformat(user["ultimo_diario"])
        if ahora - ultimo < espera:
            restante = espera - (ahora - ultimo)
            h, rem = divmod(int(restante.total_seconds()), 3600); m = rem // 60
            return await interaction.response.send_message(
                embed=discord.Embed(title="⏳ Ya reclamaste hoy", color=COLOR_ERROR,
                    description=f"Vuelve en **{h}h {m}m**"), ephemeral=True)
    recompensa = random.randint(20_000, 50_000)
    user["efectivo"] += recompensa; user["ultimo_diario"] = ahora.isoformat()
    agregar_xp(user, 10); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DIARIO", recompensa, f"Recompensa diaria {clp(recompensa)}")
    em = discord.Embed(title="🎁 ¡Recompensa Diaria! — Banco Alianza Santander", color=COLOR_EXITO,
        description=f"Recibiste **{clp(recompensa)}** en efectivo.\n💵 Efectivo actual: **{clp(user['efectivo'])}**")
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 💼 /trabajo
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="trabajo", description="💼 Trabajar para ganar dinero (cada 4 horas)")
async def trabajo(interaction: discord.Interaction):
    user = get_user(interaction.user.id); ahora = datetime.now(); espera = timedelta(hours=4)
    if user.get("ultimo_trabajo"):
        ultimo = datetime.fromisoformat(user["ultimo_trabajo"])
        if ahora - ultimo < espera:
            restante = espera - (ahora - ultimo)
            h, rem = divmod(int(restante.total_seconds()), 3600); m = rem // 60
            return await interaction.response.send_message(
                embed=discord.Embed(title="⏳ Aún estás descansando", color=COLOR_ERROR,
                    description=f"Podrás trabajar en **{h}h {m}m**"), ephemeral=True)
    nombre, minimo, maximo = random.choice(TRABAJOS)
    ganancia = random.randint(minimo, maximo)
    user["efectivo"] += ganancia; user["ultimo_trabajo"] = ahora.isoformat()
    agregar_xp(user, 20); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "TRABAJO", ganancia, f"{nombre} → {clp(ganancia)}")
    em = discord.Embed(title="💼 ¡Turno Completado! — Gran Chile RP", color=COLOR_EXITO,
        description=f"Trabajaste como **{nombre}** y ganaste **{clp(ganancia)}**.\n💵 Efectivo actual: **{clp(user['efectivo'])}**")
    em.set_footer(text="🏦 Banco Alianza Santander | Próximo trabajo en 4 horas")
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 🔫 /crimen
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="crimen", description="🔫 Cometer un crimen de alto riesgo (60% éxito)")
async def crimen(interaction: discord.Interaction):
    user = get_user(interaction.user.id); ahora = datetime.now(); espera = timedelta(hours=6)
    if user["ultimo_crimen"]:
        ultimo = datetime.fromisoformat(user["ultimo_crimen"])
        if ahora - ultimo < espera:
            restante = espera - (ahora - ultimo)
            h, rem = divmod(int(restante.total_seconds()), 3600); m = rem // 60
            return await interaction.response.send_message(
                embed=discord.Embed(title="🚔 La Policía te vigila", color=COLOR_ERROR,
                    description=f"Espera **{h}h {m}m** antes de otro crimen."), ephemeral=True)
    user["ultimo_crimen"] = ahora.isoformat()
    crimen_elegido = random.choice(CRIMENES)
    if random.random() < 0.60:
        ganancia = random.randint(50_000, 200_000); user["efectivo"] += ganancia
        agregar_xp(user, 30); save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "CRIMEN", ganancia, f"Crimen: {crimen_elegido}")
        em = discord.Embed(title="🔫 ¡Crimen Exitoso!", color=0x2ECC71,
            description=f"**{crimen_elegido}**\n\nEscapaste con **{clp(ganancia)}** en efectivo.\n⚠️ *La Policía te busca...*")
    else:
        multa = random.randint(30_000, 80_000)
        user["efectivo"] = max(0, user["efectivo"] - multa)
        user["penales"] = user.get("penales", 0) + 1
        save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "CRIMEN_FALLO", -multa, f"Arrestado: {crimen_elegido}")
        em = discord.Embed(title="🚔 ¡Arrestado por Carabineros!", color=COLOR_ERROR,
            description=f"**{crimen_elegido}**\n\nFuiste multado con **{clp(multa)}**.\n📋 Penales acumulados: **{user['penales']}**")
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 💱 /divisa
# ══════════════════════════════════════════════════════════════
grupo_divisa = app_commands.Group(name="divisa", description="💱 Cambio de divisas", guild_ids=[GUILD_ID])

@grupo_divisa.command(name="clp_a_usd", description="Convertir CLP → USD")
@app_commands.describe(monto="Monto en CLP a convertir")
async def divisa_clp_usd(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    resultado = round(monto / TASA_CAMBIO, 2)
    user["banco"] -= monto; user["usd_banco"] += resultado
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DIVISA", monto, f"Cambio {clp(monto)} → {usd(resultado)}")
    em = discord.Embed(title="💱 Cambio de Divisa Exitoso", color=COLOR_EXITO)
    em.add_field(name="🇨🇱 Entregaste",   value=clp(monto),              inline=True)
    em.add_field(name="🇺🇸 Recibiste",    value=usd(resultado),          inline=True)
    em.add_field(name="📈 Tasa aplicada", value=f"1 USD = {clp(TASA_CAMBIO)}", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_divisa.command(name="usd_a_clp", description="Convertir USD → CLP")
@app_commands.describe(monto="Monto en USD a convertir")
async def divisa_usd_clp(interaction: discord.Interaction, monto: float):
    user = get_user(interaction.user.id)
    if user["usd_banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo USD insuficiente. Tienes **{usd(user['usd_banco'])}**.", ephemeral=True)
    resultado = int(monto * TASA_CAMBIO)
    user["usd_banco"] -= monto; user["banco"] += resultado
    save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "DIVISA", resultado, f"Cambio {usd(monto)} → {clp(resultado)}")
    em = discord.Embed(title="💱 Cambio de Divisa Exitoso", color=COLOR_EXITO)
    em.add_field(name="🇺🇸 Entregaste",   value=usd(monto),              inline=True)
    em.add_field(name="🇨🇱 Recibiste",    value=clp(resultado),          inline=True)
    em.add_field(name="📈 Tasa aplicada", value=f"1 USD = {clp(TASA_CAMBIO)}", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    await interaction.response.send_message(embed=em, ephemeral=True)

@grupo_divisa.command(name="tasa", description="Ver la tasa de cambio actual")
async def divisa_tasa(interaction: discord.Interaction):
    variacion = random.uniform(-2, 2)
    em = discord.Embed(title="💱 Tasa de Cambio — Banco Alianza Santander", color=COLOR_INFO)
    em.add_field(name="🇨🇱 CLP → USD",       value=f"$1.000 CLP = {usd(1000/TASA_CAMBIO)}", inline=True)
    em.add_field(name="🇺🇸 USD → CLP",       value=f"$1 USD = {clp(TASA_CAMBIO)}",           inline=True)
    em.add_field(name="📊 Variación del día", value=f"{variacion:+.2f}%",                     inline=False)
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
    movs = user.get("historial", [])[:10]
    em = discord.Embed(title="📊 Historial de Movimientos — Banco Alianza Santander", color=COLOR_PRINCIPAL)
    em.description = (
        "\n".join(f"`{m['fecha']}` **{m['tipo']}** — {m['descripcion']}" for m in movs)
        if movs else "*Sin movimientos registrados aún.*"
    )
    em.set_footer(text="🏦 Banco Alianza Santander | Últimos 10 movimientos")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🔥 /rachas
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="rachas", description="🔥 Ver tu racha de días consecutivos")
async def rachas(interaction: discord.Interaction):
    user = get_user(interaction.user.id); racha = user.get("rachas", 0)
    if racha >= 30:   titulo = "🏆 ¡Leyenda del Banco Alianza!"
    elif racha >= 14: titulo = "🔥 ¡Racha Épica!"
    elif racha >= 7:  titulo = "⭐ ¡Racha Semanal!"
    else:             titulo = "💪 ¡Sigue así, ciudadano!"
    em = discord.Embed(title=f"🔥 {titulo}", color=COLOR_ADVERTENCIA,
        description=f"Llevas **{racha}** días consecutivos colectando tu salario.")
    em.add_field(name="⭐ Nivel",    value=str(user.get("nivel", 1)),       inline=True)
    em.add_field(name="🎯 XP Total", value=str(user.get("experiencia", 0)), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🚔 /penales
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="penales", description="🚔 Ver tus penales acumulados")
async def penales(interaction: discord.Interaction):
    user = get_user(interaction.user.id); p = user.get("penales", 0)
    tanda = int(p * 1.5)
    nivel_peligro = "🟢 Ciudadano Limpio" if p == 0 else "🟡 Bajo Vigilancia" if p < 3 else "🔴 Buscado por Carabineros"
    em = discord.Embed(title="🚔 Mis Penales — Gran Chile RP", color=COLOR_ERROR)
    em.add_field(name="📋 Penales acumulados", value=str(p),        inline=True)
    em.add_field(name="⚖️ Tanda (x1.5)",       value=str(tanda),    inline=True)
    em.add_field(name="🚨 Estado legal",        value=nivel_peligro, inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🏧 /cajero
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="cajero", description="🏧 Abrir el Cajero Automático (ATM)")
async def cajero(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    em = discord.Embed(title="🏧 Cajero Automático — Banco Alianza Santander",
        color=COLOR_PRINCIPAL, description="Bienvenido al ATM de **Banco Alianza Santander**.\nUsa los comandos de débito para operar:")
    em.add_field(name="💵 Efectivo disponible", value=clp(user["efectivo"]), inline=True)
    em.add_field(name="🏦 Saldo en banco",      value=clp(user["banco"]),    inline=True)
    em.add_field(name="🇺🇸 USD en banco",       value=usd(user["usd_banco"]),inline=True)
    em.add_field(name="📋 Operaciones disponibles",
        value=("• `/debito depositar` — Depositar efectivo al banco\n"
               "• `/debito retirar` — Retirar dinero al efectivo\n"
               "• `/debito transferir` — Transferir a otro ciudadano\n"
               "• `/debito estado` — Ver estado completo de cuenta"), inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP | Servicio 24/7")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🏆 /top
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="top", description="🏆 Ver el ranking de los más ricos de Gran Chile RP")
async def top(interaction: discord.Interaction):
    db = cargar_db()
    usuarios = sorted(
        [(uid, d.get("efectivo",0)+d.get("banco",0), d.get("nombre_completo", f"Ciudadano {uid[:4]}"))
         for uid, d in db["users"].items()],
        key=lambda x: x[1], reverse=True)[:10]
    medallas = ["🥇","🥈","🥉"] + ["🏅"]*7
    em = discord.Embed(title="🏆 Los Más Ricos de Gran Chile RP", color=COLOR_ADVERTENCIA,
        description="*Ranking basado en efectivo + saldo bancario*")
    em.description += "\n\n" + "\n".join(
        f"{medallas[i]} **#{i+1}** {nombre or 'Desconocido'} — **{clp(total)}**"
        for i, (_, total, nombre) in enumerate(usuarios)
    ) if usuarios else "*Sin datos aún*"
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 🎰 /invertir
# ══════════════════════════════════════════════════════════════
@bot.tree.command(guild=guild_obj, name="invertir", description="🎰 Hacer una inversión de riesgo en el mercado")
@app_commands.describe(monto="Monto en CLP a arriesgar (mínimo $5.000)")
async def invertir(interaction: discord.Interaction, monto: int):
    user = get_user(interaction.user.id)
    if monto < 5_000: return await interaction.response.send_message("❌ Monto mínimo: **$5.000 CLP**", ephemeral=True)
    if user["banco"] < monto: return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}**.", ephemeral=True)
    r = random.random()
    if r < 0.10:
        ganancia = int(monto*3.0); msg = f"💎 **¡JACKPOT!** Triplicaste tu inversión.\nGanaste **{clp(ganancia)}** extra."; color = COLOR_PREMIUM
    elif r < 0.40:
        ganancia = int(monto*1.5); msg = f"📈 ¡Buena inversión! Ganaste **{clp(ganancia-monto)}** extra."; color = COLOR_EXITO
    elif r < 0.65:
        ganancia = int(monto*0.8); msg = f"📉 Mala racha. Perdiste **{clp(monto-ganancia)}**."; color = COLOR_ERROR
    else:
        ganancia = 0; msg = "💥 **¡Perdiste todo!** La inversión fracasó completamente."; color = COLOR_ERROR
    user["banco"] = user["banco"] - monto + ganancia
    agregar_xp(user, 5); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "INVERSIÓN", ganancia-monto, f"{clp(monto)} → {clp(ganancia)}")
    em = discord.Embed(title="🎰 Resultado de Inversión — Banco Alianza Santander", color=color, description=msg)
    em.add_field(name="💵 Invertido",         value=clp(monto),        inline=True)
    em.add_field(name="💰 Resultado",         value=clp(ganancia),     inline=True)
    em.add_field(name="🏦 Nuevo saldo banco", value=clp(user["banco"]),inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ══════════════════════════════════════════════════════════════
# 🆕 NUEVOS COMANDOS EXCLUSIVOS GRAN CHILE RP
# ══════════════════════════════════════════════════════════════

# 🎁 /regalar — Regalar efectivo a otro ciudadano
@bot.tree.command(guild=guild_obj, name="regalar", description="🎁 Regalar efectivo a otro ciudadano de Gran Chile RP")
@app_commands.describe(usuario="Ciudadano a quien regalar", monto="Monto en CLP a regalar")
async def regalar(interaction: discord.Interaction, usuario: discord.Member, monto: int):
    if usuario.id == interaction.user.id:
        return await interaction.response.send_message("❌ No puedes regalarte dinero a ti mismo.", ephemeral=True)
    if usuario.bot:
        return await interaction.response.send_message("❌ No puedes regalarle a un bot.", ephemeral=True)
    if monto < 1_000:
        return await interaction.response.send_message("❌ El monto mínimo para regalar es **$1.000 CLP**.", ephemeral=True)
    user = get_user(interaction.user.id)
    if user["efectivo"] < monto:
        return await interaction.response.send_message(
            f"❌ Efectivo insuficiente.\nTienes: **{clp(user['efectivo'])}**\nNecesitas: **{clp(monto)}**", ephemeral=True)
    receptor = get_user(usuario.id)
    user["efectivo"] -= monto; receptor["efectivo"] += monto
    agregar_xp(user, 5); save_user(interaction.user.id, user); save_user(usuario.id, receptor)
    add_historial(interaction.user.id, "REGALO_ENVIADO", -monto, f"Regalo a {usuario.display_name}")
    add_historial(usuario.id, "REGALO_RECIBIDO", monto, f"Regalo de {interaction.user.display_name}")
    em = discord.Embed(
        title="🎁 ¡Regalo Enviado! — Gran Chile RP",
        description=f"**{interaction.user.display_name}** le regaló **{clp(monto)}** a **{usuario.display_name}** 💝",
        color=COLOR_REGALO)
    em.add_field(name="💵 Monto regalado",  value=clp(monto),              inline=True)
    em.add_field(name="👤 Receptor",        value=usuario.mention,         inline=True)
    em.add_field(name="💰 Tu efectivo restante", value=clp(user["efectivo"]), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP | ¡La generosidad es virtud!")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# 🎲 /ruleta — Apostar en ruleta
@bot.tree.command(guild=guild_obj, name="ruleta", description="🎲 Apostar en la ruleta del Banco Alianza (rojo/negro/número)")
@app_commands.describe(
    monto="Monto en CLP a apostar",
    apuesta="Escribe: rojo, negro, par, impar, o un número del 0-36")
async def ruleta(interaction: discord.Interaction, monto: int, apuesta: str):
    user = get_user(interaction.user.id)
    if monto < 5_000:
        return await interaction.response.send_message("❌ Apuesta mínima: **$5.000 CLP**", ephemeral=True)
    if user["banco"] < monto:
        return await interaction.response.send_message(f"❌ Saldo insuficiente. Tienes **{clp(user['banco'])}** en banco.", ephemeral=True)

    numero_salido = random.randint(0, 36)
    rojos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    es_rojo = numero_salido in rojos
    es_negro = numero_salido != 0 and not es_rojo
    es_par = numero_salido != 0 and numero_salido % 2 == 0
    color_salido = "🔴 Rojo" if es_rojo else ("⚫ Negro" if es_negro else "🟢 Zero")

    apuesta_lower = apuesta.lower().strip()
    ganador = False; multiplicador = 0

    if apuesta_lower == "rojo":
        ganador = es_rojo; multiplicador = 2
    elif apuesta_lower == "negro":
        ganador = es_negro; multiplicador = 2
    elif apuesta_lower == "par":
        ganador = es_par; multiplicador = 2
    elif apuesta_lower == "impar":
        ganador = not es_par and numero_salido != 0; multiplicador = 2
    elif apuesta_lower.isdigit():
        num = int(apuesta_lower)
        if 0 <= num <= 36:
            ganador = num == numero_salido; multiplicador = 36
        else:
            return await interaction.response.send_message("❌ Número inválido. Usa un número entre 0 y 36.", ephemeral=True)
    else:
        return await interaction.response.send_message(
            "❌ Apuesta inválida.\nOpciones: **rojo**, **negro**, **par**, **impar**, o un **número del 0 al 36**", ephemeral=True)

    if ganador:
        ganancia = int(monto * multiplicador) - monto
        user["banco"] += ganancia
        agregar_xp(user, 15)
        desc = f"🎉 **¡Ganaste!**\nEl número fue **{numero_salido}** {color_salido}\nGanaste **{clp(ganancia)}** extra!"
        color = COLOR_EXITO
        add_historial(interaction.user.id, "RULETA_GANÓ", ganancia, f"Ruleta: aposte {apuesta} — salió {numero_salido}")
    else:
        user["banco"] -= monto
        desc = f"💸 **¡Perdiste!**\nEl número fue **{numero_salido}** {color_salido}\nPerdiste **{clp(monto)}**."
        color = COLOR_ERROR
        add_historial(interaction.user.id, "RULETA_PERDIÓ", -monto, f"Ruleta: aposte {apuesta} — salió {numero_salido}")

    save_user(interaction.user.id, user)
    em = discord.Embed(title="🎲 Ruleta — Banco Alianza Santander", color=color, description=desc)
    em.add_field(name="🎯 Tu apuesta",   value=apuesta.title(),        inline=True)
    em.add_field(name="💰 Monto",        value=clp(monto),             inline=True)
    em.add_field(name="🔢 Número salido",value=f"**{numero_salido}** {color_salido}", inline=True)
    em.add_field(name="🏦 Saldo banco",  value=clp(user["banco"]),    inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP | Juega con responsabilidad")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ℹ️ /banco_info — Información del banco
@bot.tree.command(guild=guild_obj, name="banco_info", description="ℹ️ Ver información completa del Banco Alianza Santander")
async def banco_info(interaction: discord.Interaction):
    em = discord.Embed(
        title="🏦 Banco Alianza Santander — Información Oficial",
        description="El banco oficial de **Gran Chile RP**.\nBrindamos servicios financieros a todos los ciudadanos del servidor.",
        color=COLOR_PRINCIPAL)
    em.add_field(name="💳 Tarjetas de Crédito", value=(
        "• 💳 Clásica — Límite: **$200.000**\n"
        "• 🥈 Plata — Límite: **$500.000**\n"
        "• 🥇 Oro — Límite: **$1.500.000**\n"
        "• 💎 Platinum — Límite: **$5.000.000**\n"
        "• 💠 Diamante — Límite: **$15.000.000**"), inline=False)
    em.add_field(name="💰 Préstamos", value=(
        "• 1 semana: **5% interés**\n"
        "• 2 semanas: **10% interés**\n"
        "• 3 semanas: **15% interés**"), inline=True)
    em.add_field(name="🏦 Ahorro", value=(
        "• Tasa: **3% semanal**\n"
        "• Máximo: **3 cuentas**\n"
        "• Mínimo: **$10.000 CLP**"), inline=True)
    em.add_field(name="🚗 Registro Autos", value=(
        "• 🚗 Normal: **$150.000**\n"
        "• 🏎️ Deportivo: **$400.000**\n"
        "• 🚙 SUV: **$300.000**\n"
        "• 💎 Lujo: **$800.000**"), inline=True)
    em.add_field(name="💱 Divisas", value=f"• 1 USD = **{clp(TASA_CAMBIO)}**\n• Cambio disponible 24/7", inline=True)
    em.add_field(name="🪙 Criptomonedas", value="• **15 monedas** disponibles\n• 5 reales + 10 exclusivas Chile RP\n• `/cripto mercado` para ver precios", inline=True)
    em.add_field(name="⏰ Horario de servicios", value="🕐 **24/7** — Servicio Automático\nTodos los comandos disponibles siempre", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP | Sirviendo a la comunidad")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# ⭐ /mi_nivel — Ver nivel y XP
@bot.tree.command(guild=guild_obj, name="mi_nivel", description="⭐ Ver tu nivel, XP y recompensas de Gran Chile RP")
async def mi_nivel(interaction: discord.Interaction):
    user = get_user(interaction.user.id)
    nivel = user.get("nivel", 1); xp = user.get("experiencia", 0)
    xp_sig_nivel = int(((nivel) * 3) ** (1/0.4))
    progreso = min(100, int((xp / max(xp_sig_nivel, 1)) * 100))
    barra = "█" * (progreso // 10) + "░" * (10 - progreso // 10)

    recompensas = {
        1: "💵 Saldo inicial $50.000", 5: "💳 Acceso a tarjeta Plata",
        10: "🥇 Acceso a tarjeta Oro", 20: "💎 Acceso a tarjeta Platinum",
        30: "💠 Acceso a tarjeta Diamante", 50: "🏆 Leyenda del Banco Alianza",
    }
    prox = [(l, r) for l, r in recompensas.items() if l > nivel]
    prox_txt = f"**Nivel {prox[0][0]}:** {prox[0][1]}" if prox else "🏆 ¡Nivel máximo alcanzado!"

    em = discord.Embed(title=f"⭐ Mi Nivel — {interaction.user.display_name}", color=COLOR_ADVERTENCIA)
    em.set_thumbnail(url=interaction.user.display_avatar.url)
    em.add_field(name="⭐ Nivel actual",     value=f"**{nivel}**",                 inline=True)
    em.add_field(name="🎯 XP Total",         value=f"**{xp:,}**",                 inline=True)
    em.add_field(name="🔥 Racha",            value=f"**{user.get('rachas',0)}** días", inline=True)
    em.add_field(name="📊 Progreso al siguiente nivel",
        value=f"`{barra}` {progreso}%\n{xp:,} / {xp_sig_nivel:,} XP", inline=False)
    em.add_field(name="🎁 Próxima recompensa", value=prox_txt, inline=False)
    em.add_field(name="💡 Cómo ganar XP",
        value=("• `/colectar` → +25 XP\n• `/trabajo` → +20 XP\n"
               "• `/crimen` exitoso → +30 XP\n• Comprar cripto/bolsa → +10-15 XP\n"
               "• Registrar auto → +50 XP\n• Obtener tarjeta crédito → +100 XP"),
        inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# 🔍 /buscar_usuario — Ver perfil financiero de otro ciudadano
@bot.tree.command(guild=guild_obj, name="buscar_usuario", description="🔍 Ver el perfil financiero público de otro ciudadano")
@app_commands.describe(usuario="Ciudadano a consultar")
async def buscar_usuario(interaction: discord.Interaction, usuario: discord.Member):
    if usuario.bot:
        return await interaction.response.send_message("❌ Los bots no tienen perfil financiero.", ephemeral=True)
    user = get_user(usuario.id)
    tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
    fichas_cripto = len([v for v in user.get("cripto",{}).values() if v > 0.000001])
    em = discord.Embed(
        title=f"🔍 Perfil Público — {usuario.display_name}",
        description="*Información financiera pública del ciudadano*",
        color=COLOR_INFO)
    em.set_thumbnail(url=usuario.display_avatar.url)
    em.add_field(name="📋 Nombre RP",
        value=user.get("nombre_completo") or "*No registrado*", inline=True)
    em.add_field(name="💼 Ocupación",
        value=user.get("ocupacion") or "*Sin ocupación*", inline=True)
    em.add_field(name="⭐ Nivel",
        value=f"**{user.get('nivel',1)}**", inline=True)
    em.add_field(name="💳 Tarjeta Crédito",
        value=f"{tc['emoji']} {tc['nombre']}" if tc else "❌ Sin tarjeta", inline=True)
    em.add_field(name="🚗 Vehículos",
        value=str(len(user.get("autos",[]))), inline=True)
    em.add_field(name="🪙 Monedas cripto",
        value=f"{fichas_cripto} tipo(s)", inline=True)
    em.add_field(name="🔥 Racha",
        value=f"**{user.get('rachas',0)}** días", inline=True)
    em.add_field(name="🚔 Penales",
        value=str(user.get("penales",0)), inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP | Solo información pública")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em)

# 💱 /convertir — Convertir cripto a CLP directamente
@bot.tree.command(guild=guild_obj, name="convertir", description="💱 Convertir entre cripto y CLP instantáneamente")
@app_commands.describe(
    moneda="Símbolo de la criptomoneda",
    cantidad="Cantidad de cripto a convertir a CLP")
async def convertir(interaction: discord.Interaction, moneda: str, cantidad: float):
    moneda = moneda.upper().strip()
    if moneda not in CRIPTO_INFO:
        return await interaction.response.send_message(
            f"❌ Moneda no encontrada.\nDisponibles: **{', '.join(CRIPTO_INFO.keys())}**", ephemeral=True)
    user = get_user(interaction.user.id)
    saldo = user.get("cripto", {}).get(moneda, 0)
    if saldo < cantidad:
        return await interaction.response.send_message(
            f"❌ No tienes suficiente **{moneda}**.\nTienes: **{saldo:.8f}**\nNecesitas: **{cantidad:.8f}**", ephemeral=True)
    db = cargar_db(); precios = get_precios_cripto(db)
    info = CRIPTO_INFO[moneda]; valor_clp = int(cantidad * precios[moneda])
    user["cripto"][moneda] = saldo - cantidad; user["banco"] += valor_clp
    agregar_xp(user, 5); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "CONVERSIÓN", valor_clp, f"Convirtió {cantidad:.6f} {moneda} → {clp(valor_clp)}")
    em = discord.Embed(title=f"💱 Conversión Exitosa — {info['nombre']} → CLP", color=COLOR_EXITO)
    em.add_field(name=f"{info['icon']} Entregaste",   value=f"{cantidad:.8f} {moneda}", inline=True)
    em.add_field(name="🇨🇱 Recibiste",                value=clp(valor_clp),             inline=True)
    em.add_field(name="💹 Precio unitario",            value=clp(precios[moneda]),       inline=True)
    em.add_field(name="🏦 Nuevo saldo banco",          value=clp(user["banco"]),        inline=True)
    em.add_field(name=f"🪙 {moneda} restante",         value=f"{user['cripto'][moneda]:.8f}", inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# 💳 /pagar_deuda — Pagar deuda de tarjeta de crédito
@bot.tree.command(guild=guild_obj, name="pagar_deuda", description="💳 Pagar deuda de tu tarjeta de crédito")
@app_commands.describe(monto="Monto en CLP a pagar (0 para ver deuda actual)")
async def pagar_deuda(interaction: discord.Interaction, monto: int = 0):
    user = get_user(interaction.user.id)
    if not user["tarjeta_credito"]:
        return await interaction.response.send_message("❌ No tienes tarjeta de crédito activa.", ephemeral=True)
    tc = TIPO_TARJETA[user["tarjeta_credito"]]
    deuda = user["deuda_credito"]

    if monto == 0:
        # Solo mostrar estado de deuda
        disponible = max(0, user["limite_credito"] - deuda)
        em = discord.Embed(title=f"💳 Estado Tarjeta {tc['emoji']} {tc['nombre']}", color=tc["color"])
        em.add_field(name="💰 Límite total",      value=clp(user["limite_credito"]), inline=True)
        em.add_field(name="🔴 Deuda actual",      value=clp(deuda),                 inline=True)
        em.add_field(name="✅ Crédito disponible",value=clp(disponible),            inline=True)
        if deuda > 0:
            em.add_field(name="💡 Para pagar",
                value=f"Usa `/pagar_deuda <monto>` con hasta **{clp(deuda)}**", inline=False)
        else:
            em.add_field(name="🎉 Estado", value="¡Sin deudas! Tu tarjeta está limpia.", inline=False)
        em.set_footer(text="🏦 Banco Alianza Santander")
        return await interaction.response.send_message(embed=em, ephemeral=True)

    if deuda <= 0:
        return await interaction.response.send_message("✅ No tienes deuda en tu tarjeta de crédito.", ephemeral=True)
    if monto <= 0:
        return await interaction.response.send_message("❌ El monto debe ser mayor a $0.", ephemeral=True)
    pago_real = min(monto, deuda)
    if user["banco"] < pago_real:
        return await interaction.response.send_message(
            f"❌ Saldo insuficiente.\nDeuda: **{clp(deuda)}**\nTu banco: **{clp(user['banco'])}**", ephemeral=True)

    user["banco"] -= pago_real; user["deuda_credito"] -= pago_real
    agregar_xp(user, 10); save_user(interaction.user.id, user)
    add_historial(interaction.user.id, "PAGO_DEUDA", -pago_real, f"Pago deuda crédito {clp(pago_real)}")
    em = discord.Embed(title=f"✅ Pago de Deuda Realizado — Tarjeta {tc['emoji']} {tc['nombre']}", color=COLOR_EXITO)
    em.add_field(name="💰 Monto pagado",         value=clp(pago_real),                     inline=True)
    em.add_field(name="🔴 Deuda restante",        value=clp(user["deuda_credito"]),         inline=True)
    em.add_field(name="✅ Crédito disponible",    value=clp(max(0,user["limite_credito"]-user["deuda_credito"])), inline=True)
    em.add_field(name="🏦 Saldo banco restante",  value=clp(user["banco"]),                inline=True)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, ephemeral=True)

# ══════════════════════════════════════════════════════════════
# 🏦 /banco — MENÚ PRINCIPAL CON BOTONES
# ══════════════════════════════════════════════════════════════
class ModalDebitoView(discord.ui.Modal, title="💳 Solicitar Tarjeta de Débito"):
    nombre    = discord.ui.TextInput(label="Nombre Completo (RP)", placeholder="Ej: Juan Patricio González Soto")
    ocupacion = discord.ui.TextInput(label="Ocupación",            placeholder="Ej: Policía, Mecánico, Comerciante...")

    async def on_submit(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)
        if user["tarjeta_debito"]:
            return await interaction.response.send_message("❌ Ya tienes una tarjeta de débito activa.", ephemeral=True)
        user["nombre_completo"] = str(self.nombre); user["ocupacion"] = str(self.ocupacion)
        user["registrado"] = True
        user["tarjeta_debito"] = {"numero": generar_numero_tarjeta(),
            "fecha_emision": datetime.now().strftime("%d/%m/%Y"), "activa": True}
        agregar_xp(user, 50); save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "TARJETA_DÉBITO", 0, "Tarjeta de débito emitida")
        em = discord.Embed(title="✅ ¡Tarjeta de Débito Emitida! — Banco Alianza Santander", color=COLOR_EXITO)
        em.add_field(name="👤 Titular",   value=str(self.nombre),                        inline=True)
        em.add_field(name="💼 Ocupación", value=str(self.ocupacion),                     inline=True)
        em.add_field(name="💳 Número",    value=f"`{user['tarjeta_debito']['numero']}`", inline=False)
        em.add_field(name="📅 Emisión",   value=user["tarjeta_debito"]["fecha_emision"], inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
        await interaction.response.send_message(embed=em, ephemeral=True)

class ModalCreditoView(discord.ui.Modal, title="💎 Solicitar Tarjeta de Crédito"):
    ingresos = discord.ui.TextInput(label="Ingresos Mensuales (CLP)", placeholder="Ej: 500000")
    motivo   = discord.ui.TextInput(label="Motivo de la Solicitud", style=discord.TextStyle.paragraph,
                                    placeholder="¿Para qué usarás la tarjeta de crédito?")

    async def on_submit(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)
        if not user["tarjeta_debito"]:
            return await interaction.response.send_message("❌ Primero necesitas una **tarjeta de débito**.", ephemeral=True)
        if user["tarjeta_credito"]:
            tc = TIPO_TARJETA[user["tarjeta_credito"]]
            return await interaction.response.send_message(f"❌ Ya tienes tarjeta **{tc['emoji']} {tc['nombre']}**.", ephemeral=True)
        try:
            ing = int(str(self.ingresos).replace(".","").replace(",","").replace("$","").replace(" ",""))
        except Exception:
            return await interaction.response.send_message("❌ Ingresa un monto válido sin letras.", ephemeral=True)
        if   ing >= 5_000_000: nivel = "diamante"
        elif ing >= 2_000_000: nivel = "platinum"
        elif ing >= 1_000_000: nivel = "oro"
        elif ing >= 500_000:   nivel = "plata"
        else:                  nivel = "clasica"
        tc = TIPO_TARJETA[nivel]
        user["tarjeta_credito"] = nivel; user["limite_credito"] = tc["limite"]; user["ingresos"] = ing
        agregar_xp(user, 100); save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "TARJETA_CRÉDITO", 0, f"Tarjeta {tc['nombre']} emitida")
        em = discord.Embed(title=f"{tc['emoji']} ¡Tarjeta de Crédito {tc['nombre']} Aprobada!", color=tc["color"])
        em.add_field(name="💳 Tipo",                value=f"{tc['emoji']} {tc['nombre']}", inline=True)
        em.add_field(name="💰 Límite de crédito",   value=clp(tc["limite"]),               inline=True)
        em.add_field(name="💵 Ingresos declarados", value=clp(ing),                        inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
        await interaction.response.send_message(embed=em, ephemeral=True)

class ModalPrestamoView(discord.ui.Modal, title="💰 Solicitar Préstamo — Banco Alianza"):
    monto_input  = discord.ui.TextInput(label="Monto Solicitado (CLP)",           placeholder="Ej: 1000000")
    plazo_input  = discord.ui.TextInput(label="Plazo de pago (1, 2 o 3 semanas)", placeholder="Ej: 2", max_length=1)
    motivo_input = discord.ui.TextInput(label="Motivo del Préstamo", style=discord.TextStyle.paragraph,
                                        placeholder="¿Para qué necesitas el préstamo?")

    async def on_submit(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)
        try:
            monto   = int(str(self.monto_input).replace(".","").replace(",","").replace("$","").replace(" ",""))
            semanas = max(1, min(3, int(str(self.plazo_input).strip())))
        except Exception:
            return await interaction.response.send_message("❌ Datos inválidos. Revisa el monto y el plazo.", ephemeral=True)
        if monto < 10_000:
            return await interaction.response.send_message("❌ Monto mínimo: **$10.000 CLP**.", ephemeral=True)
        interes = {1:0.05,2:0.10,3:0.15}[semanas]
        total = int(monto*(1+interes)); cuota = total//semanas
        user["prestamos"].append({"id":int(datetime.now().timestamp()),"monto":monto,
            "total":total,"cuota":cuota,"semanas":semanas,"semanas_restantes":semanas,
            "motivo":str(self.motivo_input)})
        user["banco"] += monto
        agregar_xp(user, 20); save_user(interaction.user.id, user)
        add_historial(interaction.user.id, "PRÉSTAMO", monto, f"Préstamo {clp(monto)} a {semanas} semana(s)")
        em = discord.Embed(title="✅ ¡Préstamo Aprobado! — Banco Alianza Santander", color=COLOR_EXITO,
            description="El monto ha sido depositado en tu cuenta bancaria.")
        em.add_field(name="💵 Monto recibido", value=clp(monto),             inline=True)
        em.add_field(name="📅 Plazo",          value=f"{semanas} semana(s)", inline=True)
        em.add_field(name="📈 Interés",        value=f"{int(interes*100)}%", inline=True)
        em.add_field(name="💰 Total a pagar",  value=clp(total),             inline=True)
        em.add_field(name="📋 Cuota semanal",  value=clp(cuota),             inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander | Usa /prestamo ver para gestionar tu préstamo")
        await interaction.response.send_message(embed=em, ephemeral=True)

class BancoMenuView(discord.ui.View):
    def __init__(self): super().__init__(timeout=180)

    @discord.ui.select(placeholder="🏦 Selecciona un servicio bancario...", options=[
        discord.SelectOption(label="Solicitar Tarjeta de Débito",  value="debito",   emoji="💳", description="Tarjeta de débito en CLP"),
        discord.SelectOption(label="Solicitar Tarjeta de Crédito", value="credito",  emoji="💎", description="Tarjeta con línea de crédito"),
        discord.SelectOption(label="Solicitar Préstamo",           value="prestamo", emoji="💰", description="Créditos personales"),
        discord.SelectOption(label="Estado de Cuenta",             value="estado",   emoji="📊", description="Ver saldos y movimientos"),
        discord.SelectOption(label="Cambio de Divisa CLP→USD",     value="divisa",   emoji="💱", description="Convertir pesos a dólares"),
        discord.SelectOption(label="Mis Tarjetas",                 value="tarjetas", emoji="🗂️", description="Ver mis tarjetas activas"),
        discord.SelectOption(label="Registrar Vehículo",           value="auto",     emoji="🚗", description="Registro con matrícula oficial"),
    ])
    async def menu_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        val = select.values[0]
        if val == "debito":   return await interaction.response.send_modal(ModalDebitoView())
        if val == "credito":  return await interaction.response.send_modal(ModalCreditoView())
        if val == "prestamo": return await interaction.response.send_modal(ModalPrestamoView())
        if val == "auto":     return await interaction.response.send_modal(ModalRegistrarAuto())
        if val == "estado":
            user = get_user(interaction.user.id)
            tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
            h = user.get("historial", [])[:5]
            tarjetas_val = (
                f"**Débito:** {'✅ Activa' if user['tarjeta_debito'] else '❌ Sin tarjeta'}\n"
                f"**Crédito:** {tc['emoji']} {tc['nombre']}\n"
                f"**Límite:** {clp(user['limite_credito'])}\n"
                f"**Deuda:** {clp(user['deuda_credito'])}\n"
                f"**Disponible:** {clp(user['limite_credito']-user['deuda_credito'])}"
                if tc else
                f"**Débito:** {'✅ Activa' if user['tarjeta_debito'] else '❌ Sin tarjeta'}\n**Crédito:** ❌ Sin tarjeta"
            )
            em = discord.Embed(title="📊 Estado de Cuenta — Banco Alianza Santander", color=COLOR_PRINCIPAL)
            em.set_thumbnail(url=interaction.user.display_avatar.url)
            em.add_field(name="🇨🇱 Saldos CLP", value=f"💵 Efectivo: **{clp(user['efectivo'])}**\n🏦 Banco: **{clp(user['banco'])}**", inline=True)
            em.add_field(name="🇺🇸 Saldos USD", value=f"💵 Efectivo: **{usd(user['usd'])}**\n🏦 Banco: **{usd(user['usd_banco'])}**", inline=True)
            em.add_field(name="💳 Tarjetas",    value=tarjetas_val, inline=False)
            em.add_field(name="🚗 Vehículos",   value=f"{len(user.get('autos',[]))} registrado(s)", inline=True)
            em.add_field(name="📋 Préstamos",   value=f"{len(user.get('prestamos',[]))} activo(s)", inline=True)
            em.add_field(name="🕐 Últimos movimientos",
                value="\n".join(f"`{m['fecha']}` {m['descripcion']}" for m in h) if h else "*Sin movimientos aún*",
                inline=False)
            em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
            em.timestamp = datetime.now()
            return await interaction.response.send_message(embed=em, ephemeral=True)
        if val == "divisa":
            em = discord.Embed(title="💱 Cambio de Divisa — Banco Alianza Santander", color=COLOR_INFO,
                description=f"**Tasa actual: 1 USD = {clp(TASA_CAMBIO)}**\n\nUsa los comandos de divisa:\n• `/divisa clp_a_usd` — Convertir CLP a USD\n• `/divisa usd_a_clp` — Convertir USD a CLP\n• `/divisa tasa` — Ver tasa actual")
            em.set_footer(text="🏦 Banco Alianza Santander")
            return await interaction.response.send_message(embed=em, ephemeral=True)
        if val == "tarjetas":
            user = get_user(interaction.user.id)
            tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
            em = discord.Embed(title="🗂️ Mis Tarjetas — Banco Alianza Santander", color=COLOR_PRINCIPAL)
            debito_val = (
                f"✅ **Activa**\nNúmero: `{user['tarjeta_debito']['numero']}`\n"
                f"Titular: **{user.get('nombre_completo','No registrado')}**\n"
                f"Emisión: {user['tarjeta_debito']['fecha_emision']}"
                if user["tarjeta_debito"] else "❌ Sin tarjeta\nSolicítala en el menú de arriba."
            )
            credito_val = (
                f"✅ **{tc['nombre']}** Activa\n"
                f"Límite: **{clp(user['limite_credito'])}**\n"
                f"Deuda: **{clp(user['deuda_credito'])}**\n"
                f"Disponible: **{clp(user['limite_credito']-user['deuda_credito'])}**"
                if tc else "❌ Sin tarjeta de crédito\nSolicítala en el menú de arriba."
            )
            em.add_field(name="💳 Tarjeta de Débito", value=debito_val, inline=False)
            em.add_field(name=f"{tc['emoji'] if tc else '💎'} Tarjeta de Crédito", value=credito_val, inline=False)
            em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP")
            return await interaction.response.send_message(embed=em, ephemeral=True)

    @discord.ui.button(label="⚡ Crédito Express", style=discord.ButtonStyle.green, emoji="💎")
    async def btn_credito(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ModalCreditoView())

    @discord.ui.button(label="📊 Estado Rápido", style=discord.ButtonStyle.blurple, emoji="📊")
    async def btn_estado(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = get_user(interaction.user.id)
        em = discord.Embed(title="📊 Estado Rápido — Banco Alianza Santander", color=COLOR_PRINCIPAL)
        em.add_field(name="💵 Efectivo", value=clp(user["efectivo"]),  inline=True)
        em.add_field(name="🏦 Banco",    value=clp(user["banco"]),     inline=True)
        em.add_field(name="🇺🇸 USD",     value=usd(user["usd_banco"]), inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander")
        await interaction.response.send_message(embed=em, ephemeral=True)

    @discord.ui.button(label="💳 Mis Tarjetas", style=discord.ButtonStyle.gray, emoji="💳")
    async def btn_tarjetas(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = get_user(interaction.user.id)
        tc = TIPO_TARJETA.get(user["tarjeta_credito"]) if user["tarjeta_credito"] else None
        em = discord.Embed(title="🗂️ Mis Tarjetas", color=COLOR_PRINCIPAL)
        em.add_field(name="💳 Débito", value="✅ Activa" if user["tarjeta_debito"] else "❌ Sin tarjeta", inline=True)
        em.add_field(name="💎 Crédito", value=f"{tc['emoji']} {tc['nombre']}" if tc else "❌ Sin tarjeta", inline=True)
        em.set_footer(text="🏦 Banco Alianza Santander")
        await interaction.response.send_message(embed=em, ephemeral=True)

    @discord.ui.button(label="🚗 Registrar Auto", style=discord.ButtonStyle.gray, emoji="🚗")
    async def btn_auto(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ModalRegistrarAuto())

@bot.tree.command(guild=guild_obj, name="banco", description="🏦 Acceder al Banco Alianza Santander — Gran Chile RP")
async def banco(interaction: discord.Interaction):
    em = discord.Embed(
        title="🏦 BANCO ALIANZA SANTANDER",
        description=(
            "**Bienvenido al Banco Alianza Santander — Gran Chile RP**\n\n"
            "El banco oficial de tu servidor. Selecciona el servicio que necesitas."
        ),
        color=COLOR_PRINCIPAL)
    em.add_field(name="📋 Servicios Disponibles", value=(
        "💳 **Tarjetas** — Débito y crédito con límites\n"
        "💰 **Préstamos** — Créditos personales hasta 3 semanas\n"
        "📊 **Consultas** — Estado de cuenta y movimientos\n"
        "💱 **Divisas** — CLP ⇌ USD al instante\n"
        "🗂️ **Mis Tarjetas** — Ver estado de tus tarjetas\n"
        "🚗 **Registro de Autos** — Matrícula oficial Gran Chile RP"
    ), inline=False)
    em.add_field(name="🪙 Criptomonedas",
        value="**15 monedas** disponibles — 5 reales + 10 exclusivas Gran Chile RP\nUsa `/cripto mercado` para ver precios",
        inline=True)
    em.add_field(name="🆕 Nuevos Comandos",
        value="`/regalar` • `/ruleta` • `/banco_info`\n`/mi_nivel` • `/buscar_usuario`\n`/convertir` • `/pagar_deuda` • `/auto info`",
        inline=True)
    em.add_field(name="⏰ Horario", value="🕐 **24/7** Servicio Automático", inline=False)
    em.set_footer(text="🏦 Banco Alianza Santander • Gran Chile RP | Sirviendo a la comunidad")
    em.timestamp = datetime.now()
    await interaction.response.send_message(embed=em, view=BancoMenuView())

# ══════════════════════════════════════════════════════════════
# 🚀 INICIAR BOT
# ══════════════════════════════════════════════════════════════
keep_alive()
TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
PYEOF
# echo "✅ Archivo creado: $(wc -l < /home/claude/main_final.py) líneas"
Salida
