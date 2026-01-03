import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput

# ---------------- CONFIG ----------------
TOKEN = "MTQ1NzEzMzQyNjgwODE5MzE4Ng.GSR9jX.2KISmUqQKN6MAUsqxafKY65CFSivZfhjo8eqgE"
GUILD_ID = 1452612301352865896       # ID السيرفر
STAFF_ROLE_ID = 1456338910782423191  # ID رول الستاف
# ---------------------------------------

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- FORM MODAL ----------
class TicketForm(Modal):
    def __init__(self, ticket_type):
        super().__init__(title=f"{ticket_type.upper()} FORM")
        self.ticket_type = ticket_type

        self.problem = TextInput(
            label="📝 اشرح مشكلتك",
            style=discord.TextStyle.paragraph,
            required=True
        )
        self.more = TextInput(
            label="📌 معلومات إضافية (اختياري)",
            style=discord.TextStyle.paragraph,
            required=False
        )

        self.add_item(self.problem)
        self.add_item(self.more)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        staff_role = guild.get_role(STAFF_ROLE_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"{self.ticket_type}-{interaction.user.name}",
            overwrites=overwrites
        )

        embed = discord.Embed(
            title=f"🎫 {self.ticket_type.upper()} TICKET",
            color=0x2ecc71
        )
        embed.add_field(name="📝 المشكل", value=self.problem.value, inline=False)
        embed.add_field(name="📌 معلومات إضافية", value=self.more.value or "—", inline=False)
        embed.set_footer(text="Ticket System")

        await channel.send(
            content=f"{interaction.user.mention} | {staff_role.mention}",
            embed=embed,
            view=CloseTicketView()
        )

        await interaction.response.send_message("✅ Ticket تفتح بنجاح", ephemeral=True)

# ---------- CLOSE BUTTON ----------
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="❌ Close Ticket", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("⏳ Ticket بش يتسكر...", ephemeral=True)
        await interaction.channel.delete()

# ---------- PANEL BUTTONS ----------
class TicketPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💻 Probleme PC", style=discord.ButtonStyle.primary)
    async def pc(self, interaction, button):
        await interaction.response.send_modal(TicketForm("Probleme PC"))

    @discord.ui.button(label="❓ Help", style=discord.ButtonStyle.success)
    async def help(self, interaction, button):
        await interaction.response.send_modal(TicketForm("Help"))

    @discord.ui.button(label="🚨 Report", style=discord.ButtonStyle.danger)
    async def report(self, interaction, button):
        await interaction.response.send_modal(TicketForm("Report"))

    @discord.ui.button(label="🎮 Probleme Game", style=discord.ButtonStyle.secondary)
    async def game(self, interaction, button):
        await interaction.response.send_modal(TicketForm("Probleme Game"))

    @discord.ui.button(label="📝 Application Supporter", style=discord.ButtonStyle.primary)
    async def app(self, interaction, button):
        await interaction.response.send_modal(TicketForm("Application Supporter"))

# ---------- AUTO PANEL ----------
@bot.event
async def on_ready():
    print(f"✅ Bot Online : {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ GUILD_ID غلط")
        return

    channel = discord.utils.get(guild.text_channels, name="ticket-panel")
    if not channel:
        print("❌ channel ticket-panel مش موجود")
        return

    embed = discord.Embed(
        title="🎫 Ticket Support Panel",
        description="""
💻 Probleme PC  
❓ Help  
🚨 Report  
🎮 Probleme Game  
📝 Application Supporter
        """,
        color=0x3498db
    )
    embed.set_footer(text="Click a button to open a ticket")

    await channel.send(embed=embed, view=TicketPanel())

bot.run(TOKEN)
