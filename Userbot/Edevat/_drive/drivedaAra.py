# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Userbot.Edevat._drive.yetkilendirme import g_yetki

async def drive_aramasi(arama_kelimesi, parent_id=None):
    if parent_id:
        sorgu = f"'{parent_id}' in parents and name contains '{arama_kelimesi}'"
    else:
        sorgu = f"name contains '{arama_kelimesi}'"

    try:
        drive_service = await g_yetki()
    except AttributeError:
        return

    page_token    = None
    cevap         = ""
    while True:
        try:
            response = drive_service.files().list(
                supportsAllDrives=True,
                q=sorgu,
                spaces="drive",
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token
                ).execute()
            # print(parent_id)
            # print(response)
            for file in response.get("files", []):
                dosya_adi   = file.get("name")
                dosya_id    = file.get("id")
                if file.get("mimeType") == "application/vnd.google-apps.folder":
                    cevap += f"📁 __[{dosya_adi}](https://drive.google.com/drive/folders/{dosya_id})__\n\n"
                else:
                    cevap += f"📄 __[{dosya_adi}](https://drive.google.com/uc?id={dosya_id}&export=download\)__\n\n"
            page_token = response.get("nextPageToken", None)
            if not page_token:
                # daha fazla dosya yoksa
                break

        except Exception as hata:
            cevap += str(hata)
            break
    return f"🔍**Google Drive Araması**: `{arama_kelimesi}`\n\n{cevap}"