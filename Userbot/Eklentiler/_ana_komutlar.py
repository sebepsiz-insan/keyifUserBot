# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT, API_ID, API_HASH, STRING_SESSION, SESSION_ADI
from Userbot.Edevat._drive.yetkilendirme import CLIENT_ID, CLIENT_SECRET
from Userbot.Edevat.eklenti_listesi import eklentilerim
from Userbot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj, kullanici
from Userbot.Edevat.deldog import deldog

from pyrogram import Client, filters
from time import time

mesaj_baslangici = '`Hallediyorum..`'

@Client.on_message(filters.command(['yardim'], ['!','.','/']) & filters.me)
async def yardim_mesaji(client, message):
    await log_yolla(client, message)
    ilk_mesaj = await message.edit(mesaj_baslangici)

    basla = time()
    await ilk_mesaj.edit("__Aranıyor...__")

    mesaj = f"""Merhaba, [{message.from_user.first_name}](tg://user?id={message.from_user.id})!\n
Ben @keyiflerolsun tarafından, @KekikAkademi'de yaratıldım.\n
Kaynak kodlarım [Burada](https://github.com/keyiflerolsun/keyifUserBot)
Kullanabileceğim komutlar ise eklentilerimde gizli..\n\n"""

    mesaj += """__Eklentilerimi görebilmek için__ `.eklentilist` __komutunu kullanabilirsin..__

`.destek` «__eklenti__» **komutuyla da eklenti hakkında bilgi alabilirsin..**
"""

    bitir = time()
    sure = bitir - basla
    mesaj += f"\n**Tepki Süresi :** `{str(sure)[:4]} sn`"

    try:
        await ilk_mesaj.edit(mesaj, disable_web_page_preview=True)
    except Exception as hata:
        await hata_log(hata)
        await ilk_mesaj.edit(f'**Hata Var !**\n\n`{type(hata).__name__}`\n\n__{hata}__')

@Client.on_message(filters.command(['destek'], ['!','.','/']) & filters.me)
async def destek(client, message):
    await log_yolla(client, message)
    ilk_mesaj = await message.edit(mesaj_baslangici)

    girilen_yazi = message.text.split()

    if len(girilen_yazi) == 1:
        mesaj = "`DosyaAdı` **Girmelisin!**\n\n"

        mesaj += "__Destek alınabilecek Eklentilerim;__\n"
        mesaj += eklentilerim()

        await ilk_mesaj.edit(mesaj)
        return

    try:
        destek_json = DESTEK_KOMUT[girilen_yazi[1]]
        mesaj = f"\t📝\t `{girilen_yazi[1]}` <u>**Eklentisi;**</u>\n"

        if destek_json['aciklama']:
            mesaj += f"__{destek_json['aciklama']}__\n"

        if destek_json['kullanim'][0]:
            mesaj += "\n\t✒️ <u>**Kullanım;**</u>\n"
            for destek_parametre in destek_json['kullanim']:
                mesaj += f"\t«<i>{destek_parametre}</i>»\n"

        if destek_json['ornekler'][0]:
            mesaj += "\n\t✏️ <u>**Örneğin;**</u>\n"
            for destek_ornek in destek_json['ornekler']:
                mesaj += f"```{destek_ornek}```\n"

    except KeyError:
        mesaj = f"`{girilen_yazi[1]}`\n\t**Adında bir eklenti bulunamadı..**"

        mesaj += "\n\n__Destek alınabilecek Eklentilerim;__\n"
        mesaj += eklentilerim()

    await ilk_mesaj.edit(mesaj)

@Client.on_message(filters.command(['logsalla'], ['!','.','/']) & filters.me)
async def logsalla(client, message):
    await log_yolla(client, message)
    yanitlanacak_mesaj = yanitlanan_mesaj(message)

    raw_log = await deldog(message, open(f"@{SESSION_ADI}.log", "r").read())

    await message.reply(
        f"**Log istersin de vermez miyim..**\n\n__[@{SESSION_ADI} Logları]({raw_log})__",
        disable_web_page_preview    = True,
        reply_to_message_id         = yanitlanacak_mesaj
    )

@Client.on_message(filters.command(['envsalla'], ['!','.','/']) & filters.me)
async def envsalla(client, message):
    await log_yolla(client, message)
    ilk_mesaj = await message.edit(mesaj_baslangici)

    kullanici_adi, kullanici_id = kullanici(message)

    env_bilgileri = f"""__İşte {kullanici_adi} » {SESSION_ADI} Bilgileri;__

**API_ID :**
`{API_ID}`

**API_HASH :**
`{API_HASH}`

**STRING_SESSION :**
`{STRING_SESSION}`

**CLIENT_ID :**
`{CLIENT_ID}`

**CLIENT_SECRET :**
`{CLIENT_SECRET}`

**KİMSEYLE PAYLAŞMAYINIZ!!**

`Sağlayıcı :` **@KekikAkademi**"""

    await client.send_message(kullanici_id, env_bilgileri)

    await ilk_mesaj.edit(f"**{kullanici_adi} !**\n\n`ayar.env` **için gerekli olan bilgilerini kaydettim..**\n\n__Kayıtlı Mesajlarına Bakabilirsin..__")