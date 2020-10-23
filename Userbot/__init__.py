# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, __version__
from konsolTaban._evrensel.tanimlar import bellenim_surumu
import os, sys
from dotenv import load_dotenv
from rich.console import Console

konsol = Console(log_path=False)

def hata(yazi):
   konsol.print(yazi, style="bold red")
def bilgi(yazi):
   konsol.print(yazi, style="blue")
def basarili(yazi):
   konsol.print(yazi, style="bold green")
def onemli(yazi):
   konsol.print(yazi, style="bold cyan")
def soru(soru):
   return konsol.input(f"[bold yellow]{soru}[/]")
def log_ver(bisi):
    konsol.log(bisi)

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    hata("""En az python 3.6 sürümüne sahip olmanız gerekir.
              Birden fazla özellik buna bağlıdır. Bot kapatılıyor.""")
    quit(1)

if (bellenim_surumu.split('-')[-1] != 'aws') and (not os.path.exists("ayar.env")): # Heroku Geçmek için aws
   hata("\n\tLütfen ayar.env dosyanızı oluşturun..\n")
   quit(1)

load_dotenv("ayar.env")

# Yapılandırmanın önceden kullanılan değişkeni kullanarak düzenlenip düzenlenmediğini kontrol edin.
# Temel olarak, yapılandırma dosyası için kontrol.
AYAR_KONTROL = os.environ.get("___________LUTFEN_______BU_____SATIRI_____SILIN__________", None)

if AYAR_KONTROL:
    hata("\n\tLütfen ayar.env dosyanızı düzenlediğinize emin olun /veya\n\tilk hashtag'de belirtilen satırı kaldırın..\n")
    quit(1)

API_ID          = os.environ.get("API_ID", None)
API_HASH        = os.environ.get("API_HASH", None)
STRING_SESSION  = os.environ.get("STRING_SESSION", None)
SESSION_ADI     = os.environ.get("SESSION_ADI", "kekikUserbot")
INDIRME_ALANI   = os.environ.get("INDIRME_ALANI", "downloads/")
if not os.path.isdir(INDIRME_ALANI): os.makedirs(INDIRME_ALANI)

if STRING_SESSION.startswith('-') or len(STRING_SESSION) < 351:
    hata("\n\tMuhtemelen String Session Hatalı..!\n")
    quit(1)

try:
    kekikUserbot        = Client(
        STRING_SESSION,
        api_id          = int(API_ID),
        api_hash        = API_HASH,
        plugins         = dict(root="Userbot/Eklentiler")
    )
except ValueError:
    hata("\n\tLütfen ayar.env dosyanızı DÜZGÜNCE! oluşturun..\n")
    quit(1)

DESTEK_KOMUT = {}

tum_eklentiler = []
for dosya in os.listdir("./Userbot/Eklentiler/"):
    if not dosya.endswith(".py") or dosya.startswith("_"):
        continue
    tum_eklentiler.append(f"📂 {dosya.replace('.py','')}")

def baslangic():
    kekikUserbot.start()

    surum = f"{str(sys.version_info[0])}.{str(sys.version_info[1])}"
    konsol.print(f"\t\t[gold1]@{SESSION_ADI}[/] [yellow]:bird:[/] [bold red]Python: [/][i]{surum}[/]")
    basarili(f"  {SESSION_ADI} [magenta]v[/] [blue]{__version__}[/] [red]Pyrogram[/] tabanında [magenta]{len(tum_eklentiler)} eklentiyle[/] çalışıyor...\n")

    kekikUserbot.stop()