# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat.zenginLog import log_yolla, hata_log
from Userbot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama" : "Çeşitli GoogleDrive İşlemleri",
        "kullanim" : [
            "`.gyetki` Komutuyla Yetkilendirme Linki Alın!",
            "`.gtoken kod` Komutuyla Token'inizi tanıtın..",
            "`.gortaklar` Komutuyla ortak drive listenizi alın..",
            "`.gdrive ortak_id` Komutuyla ortak drive dizini belirlenir..",
            "`.gara bişiy` Komutuyla disk'inizde arama yapın.."
            ],
        "ornekler" : [
            ".gyetki",
            ".gtoken kod",
            ".gortaklar",
            ".gdrive ortak_id",
            ".gara winrar"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.errors import MessageTooLong
from Userbot.Edevat._drive.yetkilendirme import kod_al, token_olustur, G_DRIVE_TOKEN_DOSYASI
from Userbot.Edevat._drive.drivedaAra import ara_drive
from Userbot.Edevat._drive.ortakDrivelar import ortak_drive_listesi, ortak_drive_s
from oauth2client.client import FlowExchangeError
import os

ORTAK_DRIVE_LAR  = None
ORTAK_DRIVE_ADI  = None
ORTAK_DRIVE_ID   = None

@Client.on_message(filters.command(['gyetki'],['!','.','/']) & filters.me)
async def gyetki(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >

    await kod_al(ilk_mesaj)

@Client.on_message(filters.command(['gtoken'],['!','.','/']) & filters.me)
async def gtoken(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >

    try:
        await token_olustur(ilk_mesaj, message.command[1])
    except IndexError as hata:
        await hata_log(hata)
        await ilk_mesaj.edit('`Kod Girmedin..`')
        return
    except FlowExchangeError as hata:
        await hata_log(hata)
        await ilk_mesaj.edit('`Vermiş olduğun kod geçersiz..`')
        return

    await ilk_mesaj.edit('**Drive Yetkilendirme Başarılı!**')

@Client.on_message(filters.command(['gortaklar'],['!','.','/']) & filters.me)
async def gortaklar(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >
    if not os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await kod_al(ilk_mesaj)
        await message.reply('**Önce Yetkilendirme Yapmalısın..**')
        return

    await ilk_mesaj.edit(await ortak_drive_listesi())

@Client.on_message(filters.command(['gdrive'],['!','.','/']) & filters.me)
async def gdrive(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >
    try:
        message.command[1]
    except IndexError:
        await ilk_mesaj.edit('__Lütfen ID Giriniz..__')
        return

    if not os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await kod_al(ilk_mesaj)
        await message.reply('**Önce Yetkilendirme Yapmalısın..**')
        return

    global ORTAK_DRIVE_LAR
    global ORTAK_DRIVE_ID
    global ORTAK_DRIVE_ADI

    if not ORTAK_DRIVE_LAR:
        ORTAK_DRIVE_LAR = await ortak_drive_s()

    drive_adi = [drive['adi'] for drive in ORTAK_DRIVE_LAR]
    drive_id  = [drive['id'] for drive in ORTAK_DRIVE_LAR]

    if message.command[1] in drive_id:
        ORTAK_DRIVE_ID  = os.environ.get("ORTAK_DRIVE_ID", message.command[1])
        ORTAK_DRIVE_ADI = os.environ.get("ORTAK_DRIVE_ID", drive_adi[drive_id.index(ORTAK_DRIVE_ID)])
    else:
        await message.edit('**Ortak Drive ID Bulunamadı!**')
        return

    await ilk_mesaj.edit(f"`{ORTAK_DRIVE_ADI}` __varsayılan olarak ayarlandı..__")

@Client.on_message(filters.command(['gara'],['!','.','/']) & filters.me)
async def gara(client, message):
    # < Başlangıç
    await log_yolla(client, message)
    ilk_mesaj = await message.edit("__Bekleyin..__",
        disable_web_page_preview    = True,
        parse_mode                  = "Markdown"
    )
    #------------------------------------------------------------- Başlangıç >
    if not os.path.exists(G_DRIVE_TOKEN_DOSYASI):
        await kod_al(ilk_mesaj)
        await message.reply('**Önce Yetkilendirme Yapmalısın..**')
        return

    try:
        await ilk_mesaj.edit(await ara_drive(drive_id=ORTAK_DRIVE_ID, drive_adi=ORTAK_DRIVE_ADI, arama_kelimesi=message.command[1]),
            disable_web_page_preview = True
        )
    except (MessageTooLong, OSError) as hata:
        await hata_log(hata)
        await ilk_mesaj.edit('__Çıktı çok uzun kanka daha spesifik şekilde aramalısın..__')
        return