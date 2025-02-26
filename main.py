import random
import telebot
from telebot import types, util
from telebot.apihelper import ApiTelegramException
import time
import asyncio
import os
import json
from uuid import getnode
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters

print(hex(getnode()))

import datetime
import sqlite3
import ujson as json
import os
import matplotlib.pyplot as plt
import numpy as np
import traceback
import requests


bot_adi = "TerrorgameRobot"

if hex(getnode()) in ["0xdc7b23bb434e"]:
    print("kyb")
    bot_adi = "TerrorgameRobot"
    bot_token = "8097493050:AAHODcBgRI0F-KnhH8adKGFg6o7e-pHMZwg"
    bot = AsyncTeleBot(bot_token, parse_mode="html")
else:
    bot_adi = "TerrorgameRobot"
    bot_token =  "8097493050:AAHODcBgRI0F-KnhH8adKGFg6o7e-pHMZwg"
    bot = AsyncTeleBot(bot_token, parse_mode="html")

temp = {}

kurucu_id = 6276057244
admins = [kurucu_id]
zaman_hassasiyeti = pow(10,6)


async def telegram_yedek_al():
    await bot.send_message(kurucu_id,"Yedek alınıyor...", disable_notification=True)
    for i in os.listdir():
        if "." in i:
            await bot.send_document(kurucu_id,open(i, 'rb'), disable_notification=True)
    await bot.send_message(kurucu_id,"Yedek alındı.", disable_notification=True)

def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)


ayarDosyasi = 'vt.json'
sqlDosyasi = "db.db"
db={}


def dbGetir():
    global db
    with open(ayarDosyasi, encoding='utf-8') as json_file:
        db = json.load(json_file)

def dbYaz():
    global db
    with open(ayarDosyasi, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

if not (os.path.exists(ayarDosyasi)):
    dbYaz()
dbGetir()


hizlar = {}

async def performans_testi():
    txt = "\n".join([f"{i} → {hizlar[i]}" for i in hizlar])
    await bot.send_message(kurucu_id,txt)

def sql_execute(command):
    while True:
        try:
            connection = sqlite3.connect(sqlDosyasi)

            crsr = connection.cursor()
            sql_command = command
            crsr.execute(sql_command)
            connection.commit()

            connection.close()
            break
        except Exception as e:
            if "locked" in str(e):
                time.sleep(0.1)
            elif "UNIQUE" in str(e):
                break
            else:
                bot.send_message(kurucu_id,str(e))
                bot.send_message(kurucu_id,get_traceback(e))
                bot.send_message(kurucu_id,command)
                break


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def sql_get(command):
    connection = sqlite3.connect(sqlDosyasi)

    connection.row_factory = dict_factory
    
    crsr = connection.cursor()
    crsr.execute(command)
    ans = crsr.fetchall()

    if len(ans) == 1:
        return ans[0]
    
    return [i for i in ans]

def get_js(table,id):
    arr = sql_get(f'SELECT * FROM "{table}" WHERE id="{id}";')
    if arr == []:
        return []
    return json.loads(arr["json"])


def set_js(table,id, js):
    ret = get_js(table,id)
    if ret!=[]:
        sql_execute("UPDATE '{}' SET json='{}' WHERE id='{}';".format(table,json.dumps(js, ensure_ascii=False),id))
    else:
        sql_execute(f"INSERT INTO '{table}' (id, json) values ('{id}', '{json.dumps(js, ensure_ascii=False)}');")


headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

def anlam_getir(kelime):
    js = json.loads(requests.get("https://www.azleks.az/online-dictionary/"+kelime, headers = headers).content.decode())[0]["anlamlarListe"]
    
    ekle = []
    for i in range(len(js)):
        ekle = ekle + [js[i]["anlam"]]
    return ekle


def add_words(kelimeler, tablo = "kelimeler"):
    frst = len(sql_get("SELECT * FROM '"+tablo+"';"))
    for kelime in kelimeler:
        if kelime.strip() == "":
            continue
        kelime = kelime.replace('I', 'ı').replace('İ', 'i').replace('\'', '').lower().strip()
        try:
            sql_execute("INSERT INTO " + tablo + " (kelime) VALUES ('"+kelime+"');")
        except Exception as e:
            if not "UNIQUE" in str(e):
                print("ahhh",e,kelime)
    sec = len(sql_get("SELECT * FROM '"+tablo+"';"))
    return str(frst) + " ⟶ " + str(sec) + f" = {sec-frst}"

def read_file(where):
    with open(where, encoding="UTF8") as f:
        return [i.strip() for i in f.readlines()]

def random_from_table(tablo = "kelimeler"):
    return sql_get("SELECT * FROM " + tablo + " ORDER BY RANDOM() LIMIT 1;")


def f(path, process="$read", **kwargs):
    """veritabanı yardımcısı
a.b.c.d şeklinde yazılır ve her birisi bir daldır.
"""
    t0 = time.time()
   
    output = kwargs.get("output", "$one") #$array
    
    if path.startswith("groups") or path.startswith("privates") or path.startswith("games") or path.startswith("kelime_turetme_kelimeler"):

        tablo = ""

        for say in [i["name"] for i in sql_get("SELECT name FROM sqlite_master WHERE type='table';")]:
            if path.startswith(say):
                tablo = say
                break
        
        path = path.replace(tablo+".","")

        ayir = path.split(".")

        id = ayir[0]
        js = []

        if tablo!=path:
            js = ayir[1:]




        if process=="$del":
            if js == []:
                sql_execute(f"DELETE FROM '{tablo}' WHERE id='{id}';")
            else:
                veri_db = get_js(tablo,id)
                veri = veri_db
                if veri == []:
                    veri = {}
        
                for i in js[:-1]:
                    if not i in veri:
                        veri[i] = {}
                    elif not "dict" in str(type(veri[i])):
                        del veri[i]
                        veri[i] = {}
                    veri = veri[i]
                
                if js[-1] in veri:
                    del veri[js[-1]]

                set_js(tablo,id,veri_db)

        elif process=="$read":
            if js==[]:
                if path == tablo:
                    return sql_get(f"SELECT * FROM '{tablo}';")


                gelen = get_js(tablo,id)

                if output=="$array" and "dict" in str(type(gelen)):
                    return [get_js(tablo,id)]
                
                return get_js(tablo,id)

            elif len(js)>0:
                w = get_js(tablo,id)

                islem = f(".".join(js), db=w)

                if output=="$array" and "dict" in str(type(w)):
                    return [islem]
                    
                return islem

            # yaz
        else:
            if js == []:
                set_js(tablo,id,process)

            elif len(js)>0:
         

                veri_db = get_js(tablo,id)

                if veri_db == []:
                    veri_db = {}

                veri = veri_db


        
                for i in js[:-1]:
                    if not i in veri:
                        veri[i] = {}
                    elif not "dict" in str(type(veri[i])):
                        del veri[i]
                        veri[i] = {}
                    veri = veri[i]

                veri[js[-1]] = process
                set_js(tablo,id,veri_db)
                return process

        hizlar["f1"] = time.time() - t0
    else:    
        global db
        veri_db = kwargs.get("db", db)

        veri = veri_db
        ayrik = path.split(".")



        for i in ayrik[:-1]:
            if process!="$read" or process!="$del":
                if not i in veri:
                    if veri == []:
                        veri = {}
                        veri[i] = {}
                    else:
                        veri[i] = {}
                elif not "dict" in str(type(veri[i])):
                    del veri[i]
                    veri[i] = {}


            if i in veri:
                veri = veri[i]
            else:
                if process=="$read" or process=="$del":
                    if output == "$array":
                        return []
                    else:
                        return ""

        if process == "$del":
            if ayrik[-1] in veri:
                del veri[ayrik[-1]]
                dbYaz()
                return


        elif process=="$read":
            if len(ayrik)>0:
                if ayrik[-1] in veri:
                    getir = veri[ayrik[-1]]
                else:
                    if output == "$array":
                        return []
                    else:
                        return ""

                if output == "$array" and "dict" in str(type(getir)):
                    return [veri[ayrik[-1]]]
                return veri[ayrik[-1]]
            else:
                if output == "$array":
                    return []
                return ""

        onceki_veri = None
        if ayrik[-1] in veri:
            onceki_veri = veri[ayrik[-1]]

        veri[ayrik[-1]] = process



        dbYaz()

        if onceki_veri == None:
            onceki_veri = veri[ayrik[-1]]
        hizlar["f2"] = time.time() - t0
        return onceki_veri


    hizlar["f"] = time.time() - t0


def oyunu_iptal_et(game_id):
    """game_id"""
    konum = f(f"games.{game_id}.konum")
    
    f(f"groups.{konum}.oyun", "")
    
    
    sql_execute("DELETE FROM games WHERE id='{}';".format(game_id))


def oyun_var_mi(chat_id):
    """oyun_konum, grup_konum"""
    oyun_konum = f(f"groups.{chat_id}.oyun")
    sayisal_mi = str(oyun_konum).isnumeric()

    grup_konum = f(f"games.{oyun_konum}.konum")

    if sayisal_mi and grup_konum != "":
        return [oyun_konum, grup_konum]
    return False

def draw_graph(x,y, **kwargs):
        
    fig, ax = plt.subplots()


    fig.set_figwidth(max(5,kwargs.get("width",int(len(x)/1.1))))

    plt.tick_params(axis='x', 
                    which='major'
                    )



      

    plt.plot(x,y)

    m, b = np.polyfit(x, y, 1)

    plt.plot(x,
             m*np.array(x) + b,
             alpha=.4,
             linestyle='dashed')
             

    plt.title(kwargs.get("title", ""))


    plt.xlabel(kwargs.get("xlabel", ""))

    plt.ylabel(kwargs.get("ylabel", ""))


    plt.xticks(x, [str(i) for i in x], rotation=12)


    for i, txt in enumerate(y):
        ax.annotate(f"{round(txt,2)}", (x[i], y[i]), xytext=(15,0), textcoords='offset points')
        plt.scatter(x, y, marker='x', color='red')
    plt.savefig('base.jpg', format='jpg')

    if (kwargs.get("chat_id", "-1002432414281")!="-1002432414281"):
        #bot.send_photo(kwargs.get("chat_id", ""), photo=open('base.jpg', 'rb'))
        bot.send_document(kwargs.get("chat_id", "-1002432414281"), document=open('base.jpg', 'rb'))
        os.remove("base.jpg")

def skor_arttir(neyi,artis=1, **kwargs):
    skor_getir = f(neyi) #, db = kwargs.get("db", db)
    if skor_getir=="":
        #oyun_id = f(neyi,artis)
        f(neyi,artis)
        return artis
    else:
        skor_getir = skor_getir + artis
        f(neyi, skor_getir)
        return skor_getir

async def log_gonder(**kwargs):
    chat_id = kwargs.get("chat_id","-1002432414281")


    oyunlar = f("games")
    if type(oyunlar) is dict:
        oyunlar = [oyunlar]


    try:
        await bot.send_message(-1002432414281, f"""
<b> ~~ 📢 Log ~~</b>

💬: <code>{f(f"groups.{chat_id}.username")}</code>
🆔: <code>{kwargs.get('user_id','')}</code>
Qrup 🆔: <code>{chat_id}</code>
Fəaliyyət: <code>{kwargs.get('eylem','')}</code>

    """, disable_web_page_preview=True)
    except Exception as e:
        if "chat not found" in str(e):
            pass
        #else:
        #    bot.send_message(kurucu_id, str(e))
    try:
        await bot.set_chat_title(-1002432414281, f"Bot Log - {len(oyunlar)}")
    except Exception as e:
        if "chat not found" in str(e):
            pass

@bot.message_handler(commands=['start'])
async def start_private(message): #, **kwargs
    chat_tipi = message.chat.type

    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id #sabit    

    msg = message.text



    if chat_tipi == "private":
        ayrik = msg.split(" ")
        if len(ayrik) == 2:
            acan_id = f(f"games.{ayrik[1]}.açan_id") 
            if acan_id == "":
                await bot.send_message(user_id,'Üzr istəyirik, bu oyunun vaxtı bitib .')
                return


            if acan_id == user_id:
                konum = f(f"games.{ayrik[1]}.konum")
                sent = await bot.send_message(user_id,'🗒 Zəhmət olmasa soruşmaq istədiyiniz sözü deyə bilərsinizmi?:')
                #bot.register_next_step_handler(sent, kelime_gir, konum)

                temp[f"{user_id}.kelime"] = {}
                temp[f"{user_id}.kelime"]["konum"] = konum
            else:
                await bot.send_message(user_id,'Bu oyunu siz açmamısınız 🚫')
        else:
            f(f"privates.{user_id}.start",True)
            keyboard = types.InlineKeyboardMarkup()

            callback_button = types.InlineKeyboardButton(text="🇦🇿Qrupa Əlavə Et🇦🇿", url="https://t.me/CrocodileGame_Robot?startgroup=a")
            callback_button2 = types.InlineKeyboardButton(text="🧬Digər botlar🧬", url="https://t.me/NeonGroupResmi")
            callback_button3 = types.InlineKeyboardButton(text="🫂Tanışlıq botu", url="https://t.me/tanisliqbot?start=r815485") 
            keyboard.add(callback_button)
            keyboard.add(callback_button2)
            keyboard.add(callback_button3)
            await bot.send_message(chat_id, f'<b>✋🏻 Salam, mən Crocodile Lite oyun botuyam 🐊\n\n🎯 Müxtəlif oyunlar oynamaq və əylənmək üçün mənimlə oynaya bilərsiniz.\n\n⚙️ Məni qrupa əlavə edin və mənimlə oynamaq üçün məni qrupda Admin et.</b >',  reply_markup=keyboard)



async def sessiz_sinema_baslat(message, **kwargs): 
    t0 = time.time()
    chat_tipi = message.chat.type

    oyun_modu = kwargs.get("mod", "oto-sunucu") # oto-sunucu, sabit, normal

    if chat_tipi == "private":
        await bot.send_message(message.chat.id, "Bu əmr yalnız qrup üçün istifadə edilə bilər.")
        return

    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id #sabit
    
    #await bot.send_chat_action(chat_id, 'typing')


    first_name = None
    if message.from_user.first_name != None:
        first_name = message.from_user.first_name
        first_name = first_name.replace("'","").replace("<","").replace(">","")

    username = None
    if message.from_user.username != None:
        username = message.from_user.username
        username = username.replace("'","").replace("<","").replace(">","")
    else:
        username = first_name
        username = username.replace("'","").replace("<","").replace(">","")
    
    first_name = kwargs.get("acan_user", first_name)
    user_id = kwargs.get("acan_id", user_id)

    konumlar = oyun_var_mi(chat_id)
    if konumlar != False:
        await bot.send_message(kurucu_id, f'Bu 456456 istifadə olunur')
        await bot.send_message(chat_id, f'❌ Hörmətli <a href="tg://user?id={user_id}">{first_name}</a>,Hazırda aktiv oyunlar var. ')
        return


    text = kwargs.get("text", f'<a href="tg://user?id={user_id}">{first_name}</a> 🗣️ sözünü təqdim edir')


    try:
        dict_name = f(f"groups.{chat_id}.bilme-sayıları")
        if dict_name == "":
            dict_name = {}
        en_iyiler = sorted(dict_name, key=dict_name.__getitem__, reverse=True)
        birinci = en_iyiler[0]
        ikinci = en_iyiler[1]
        ucuncu = en_iyiler[2]
        dorduncu = en_iyiler[3]
        besinci = en_iyiler[4]

        suser_id = str(user_id)
        
        

        if birinci == suser_id:
            ayir = text.split("\n")
            for a in range(len(ayir)):
                if first_name in ayir[a]:
                    ayir[a] = "👑 " + ayir[a]
            text = "\n".join(ayir)
            #text += f'\n\n👑 Bu kişi bu grubun birincisi 👑'
        elif ikinci == suser_id:
            ayir = text.split("\n")
            for a in range(len(ayir)):
                if first_name in ayir[a]:
                    ayir[a] = "🥈 " + ayir[a]
            text = "\n".join(ayir)
            #text += f'\n\n🥈 Bu kişi bu grubun ikincisi 🥈'
        elif ucuncu == suser_id:
            ayir = text.split("\n")
            for a in range(len(ayir)):
                if first_name in ayir[a]:
                    ayir[a] = "🥉 " + ayir[a]
            text = "\n".join(ayir)
            #text += f'\n\n🥉 Bu kişi bu grubun ikincisi 🥉'
        elif dorduncu == suser_id or besinci == suser_id:
            ayir = text.split("\n")
            for a in range(len(ayir)):
                if first_name in ayir[a]:
                    ayir[a] = "👑 " + ayir[a]
            text = "\n".join(ayir)

            
    except Exception as e:
        # eğer ilk 5te kimse yoksa hata
        pass
        #bot.send_message(kurucu_id, str(e))
    
        
    if user_id in admins and user_id != 5898049921 and user_id != 5898049921:
        ayir = text.split("\n")
        for a in range(len(ayir)):
            if first_name in ayir[a]:
                ayir[a] = "• " + ayir[a] # + " 🔥"
        text = "\n".join(ayir)
    elif user_id==6276057244 or user_id==6276057244:
        ayir = text.split("\n")
        for a in range(len(ayir)):
            if first_name in ayir[a]:
                ayir[a] = "🏅 " + ayir[a] # + " 🔥"
        text = "\n".join(ayir)
    
    incele_emoji = random.choice(["🔬","🔭","👁","👀","🔍","🔎"])
    soru_yaz_emoji = random.choice(["✍️", "📝", "✏️", "🗯"])
    istemiyorum_emoji = random.choice(["✖️", "❌", "❎", "🚫", "🙅"])
    gec_emoji = random.choice(["➡️", "♻️", "👉"])
    
    oyun_id = int(time.time() * zaman_hassasiyeti)

    callback_button3 = types.InlineKeyboardButton(text="Sözə baxın 👀", callback_data="kelime_bak")
    callback_button2 = types.InlineKeyboardButton(text="Sözü keçin ♻️", callback_data="siradaki_kelime")
    #callback_button = types.InlineKeyboardButton(text="Kelime Yaz ✏️", callback_data="kelime_gir")
    callback_button = types.InlineKeyboardButton(text="Öz sözüm 📝", url=f"https://t.me/CrocodileGame_Robot?start={oyun_id}")


    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(callback_button2)
    keyboard.add(callback_button, callback_button3)
    if oyun_modu != "sabit":
        callback_button4 = types.InlineKeyboardButton(text="Aparıcı olmaq istəmirəm ⛔", callback_data="istemiyorum")
        keyboard.add(callback_button4)


    hata_msg = None
    while 1:
        try:
            if hata_msg != None:
                await bot.edit_message_text(chat_id=chat_id, text=text, reply_markup=keyboard, message_id=hata_msg)
            else:
                await bot.send_message(chat_id, text, reply_markup=keyboard)
            hizlar["sessiz_sinema"] = time.time() - t0

            rastgele_kelime = random_from_table()["kelime"].replace("'", "")
            
            f(f"groups.{chat_id}.oyun", oyun_id)
            f(f"games.{oyun_id}",{
                "açan_id":user_id,
                "açan_user":first_name,
                "kelime":rastgele_kelime,
                "konum":chat_id,
                "oyun_tipi":"sessiz_sinema",
                "oyun_modu":oyun_modu
                }
            )

            f(f"groups.{chat_id}.son_oyun_aktivitesi", time.time())
            f(f"groups.{chat_id}.group_size", await bot.get_chat_members_count(chat_id))

            now_tuple = datetime.datetime.now().timetuple()
            skor_arttir(f"istatistik.gunluk-istatistik.baslatilan-oyun.{now_tuple.tm_yday}")
            skor_arttir(f"istatistik.saatlik-istatistik.baslatilan-oyun.{now_tuple.tm_hour}")


            f(f"privates.{user_id}.son-oyun-oynama",time.time())
            f(f"privates.{user_id}.username
