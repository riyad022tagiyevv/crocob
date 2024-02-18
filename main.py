#!/usr/bin/python
# -*- coding: utf-8 -*-

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
#import requests
#from bs4 import BeautifulSoup

import sqlite3
import ujson as json
#import json
import os


import matplotlib.pyplot as plt
import numpy as np

import traceback
#import tdk.gts #pip install tdk-py
#import warnings

import requests

#warnings.filterwarnings( "ignore", module = "matplotlib\..*" ) #warnings.filterwarnings("ignore") → all warnings
#warnings.filterwarnings("ignore")


bot_adi = "crocodileneonbot"

if hex(getnode()) in ["0xdc7b23bb434e"]: #windows masaüstü pc ise veya laptop
    #kaç yaşındasın bot
    print("kyb")
    bot_adi = "crocodileneonbot"
    bot_token = "6729459089:AAFevOsdlD5u77FWJIPxyeSZNtI_gkPTnOg"
    bot = AsyncTeleBot(bot_token, parse_mode="html")
else:
    #sıl octopus bot
    bot_adi = "crocodileneonbot"
    bot_token =  "6729459089:AAFevOsdlD5u77FWJIPxyeSZNtI_gkPTnOg"
    bot = AsyncTeleBot(bot_token, parse_mode="html")

temp = {}


kurucu_id = 5045429385

admins = [kurucu_id, 5045429385]

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


#if hex(getnode()) != "0xe03f494508ec":
#    telegram_yedek_al()



#ayarDosyasi = os.path.dirname(sys.argv[0])+'//db.json'
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
        #sql_execute(f"UPDATE '{table}' SET json='{json.dumps(js, ensure_ascii=False)}' WHERE id='{id}';")
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







#sql_execute('ALTER TABLE "chats.privates" RENAME TO "privates"')
#sql_execute('ALTER TABLE "chats.groups" RENAME TO "groups"')




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
    #process read, $del, 
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
                #v = f(".".join(js), process ,db=get_js(tablo,id))

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
    
    #bot.send_message(kurucu_id,f'Oyun iptal edilmiş\nGames: {f(f"games.{game_id}")}\nGrup: {f(f"groups.{konum}.oyun")}')
    sql_execute("DELETE FROM games WHERE id='{}';".format(game_id))
    #f(f"games.{game_id}", "$del")

#if konumlar != False and (konumlar[0] =="" or konumlar[1] ==""):
#    konumlar = False
def oyun_var_mi(chat_id):
    """oyun_konum, grup_konum"""
    ## gerçekten bu kadar kontrole gerek var mı?
    oyun_konum = f(f"groups.{chat_id}.oyun")
    sayisal_mi = str(oyun_konum).isnumeric()

    grup_konum = f(f"games.{oyun_konum}.konum")

    if sayisal_mi and grup_konum != "":
        return [oyun_konum, grup_konum]
    return False

def draw_graph(x,y, **kwargs):
    #plt.figure(figsize=(12,6))
    #title = kwargs.get("key", "default")
        
    fig, ax = plt.subplots()


    fig.set_figwidth(max(5,kwargs.get("width",int(len(x)/1.1))))

    plt.tick_params(axis='x', 
                    which='major', 
                    #labelsize=kwargs.get(
                    #    "labelsize",
                    #    max(7,int(len(x)/1.1))
                    #    )
                    )



      

    plt.plot(x,y) #biz belirlemediğimiz sürece rengi otomatik kendisi verir.

    m, b = np.polyfit(x, y, 1)

    plt.plot(x,
             m*np.array(x) + b,
             alpha=.4,
             linestyle='dashed')
             

    plt.title(kwargs.get("title", ""))


    plt.xlabel(kwargs.get("xlabel", ""))

    plt.ylabel(kwargs.get("ylabel", ""))

    #print(f"{m}x+{b}")

    #plt.yticks(range(0,max(y) + max(y)%5,5))
    plt.xticks(x, [str(i) for i in x], rotation=12)


    for i, txt in enumerate(y):
        ax.annotate(f"{round(txt,2)}", (x[i], y[i]), xytext=(15,0), textcoords='offset points')
        plt.scatter(x, y, marker='x', color='red')
    plt.savefig('base.jpg', format='jpg')

    if (kwargs.get("chat_id", "-1002124835720")!="-1002124835720"):
        #bot.send_photo(kwargs.get("chat_id", ""), photo=open('base.jpg', 'rb'))
        bot.send_document(kwargs.get("chat_id", "-1002124835720"), document=open('base.jpg', 'rb'))
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
    chat_id = kwargs.get("chat_id","-1002124835720")

    #grup_link = ""
    #try:    
    #    grup_link = bot.export_chat_invite_link(chat_id)
    #except:
    #    pass
    oyunlar = f("games")
    if type(oyunlar) is dict:
        oyunlar = [oyunlar]


    try:
        await bot.send_message(-1002124835720, f"""
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
        await bot.set_chat_title(-1002124835720, f"Bot Log - {len(oyunlar)}")
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

            callback_button = types.InlineKeyboardButton(text="🇦🇿Qrupa Əlavə Et🇦🇿", url="https://t.me/crocodileneonbot?startgroup=a")
            callback_button2 = types.InlineKeyboardButton(text="🧬Digər botlar🧬", url="https://t.me/NeonfedResmi")
            keyboard.add(callback_button)
            keyboard.add(callback_button2)
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

    

    




    #if konumlar != False and (konumlar[0] =="" or konumlar[1] ==""):
    #    konumlar = False

    # Oyun var.

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
            #text += f'\n\n👑 Bu kişi bu grubun ilk beşinde 👑'
        #elif kurucu_id == user_id:
        #    ayir = text.split("\n")
        #    for a in range(len(ayir)):
        #        if first_name in ayir[a]:
        #            ayir[a] = "🔥 " + ayir[a] # + " 🔥"
        #    text = "\n".join(ayir)
            
    except Exception as e:
        # eğer ilk 5te kimse yoksa hata
        pass
        #bot.send_message(kurucu_id, str(e))
    
        
    if user_id in admins and user_id != 5469476479 and user_id != 5469476479:
        ayir = text.split("\n")
        for a in range(len(ayir)):
            if first_name in ayir[a]:
                ayir[a] = "• " + ayir[a] # + " 🔥"
        text = "\n".join(ayir)
    elif user_id==5898049921 or user_id==5469476479:
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
    callback_button = types.InlineKeyboardButton(text="Öz sözüm 📝", url=f"https://t.me/Crogame_bot?start={oyun_id}")


    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(callback_button2)
    keyboard.add(callback_button, callback_button3)
    if oyun_modu != "sabit":
        callback_button4 = types.InlineKeyboardButton(text="Aparıcı olmaq istəmirəm ⛔", callback_data="istemiyorum")
        keyboard.add(callback_button4)
    #bot.send_message(chat_id, text, reply_markup=keyboard)

    #konumlar = oyun_var_mi(chat_id)
    #if konumlar != False:
    #    bot.send_message(kurucu_id, f'burası kullanılıyo 456456')
    #    b¨ot.send_message(chat_id, f'❌ Sayın <a href="tg://user?id={user_id}">{first_name}</a>, şu anda aktif oyun var.')
    #    return

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
            f(f"privates.{user_id}.username",username)
            f(f"privates.{user_id}.first_name",first_name)
            skor_arttir(f"privates.{user_id}.sunucu-sayısı")

            skor_arttir(f"groups.{chat_id}.toplam-sunucu-sayısı") 
            skor_arttir(f"groups.{chat_id}.sunucu-sayıları.{user_id}")

            #try:
            #    f(f"games.{oyun_id}.sozluk", random.sample(anlam_getir(rastgele_kelime),1)[0].replace("'",""))
            #except:
            #    pass

            

            await log_gonder(user_id=user_id, chat_id=chat_id, eylem="sessiz sinema başlattı", game_id=oyun_id)

            return rastgele_kelime
        except Exception as e:
            if "Too Many" in str(e):
                #bot.send_message(chat_id, "❌ Siz çok hızlı oynuyorsunuz değerli oyuncular! Bu da bir hataya yol açtı.")
                #pass
                if hata_msg == None:                        
                    hata_msg = bot.send_message(chat_id, "⌛️ Əziz oyunçular, sizi çox az gözlətəcəyəm.").id
                time.sleep(1)
            else:
                await bot.send_message(chat_id, "❌ Xəta baş verdi. Zəhmət olmasa bir daha cəhd edin.")
                await bot.send_message(kurucu_id, str(e))
                await bot.send_message(kurucu_id, get_traceback(e))
                break

    #t = threading.Thread(target=oyun_ac)
    #t.daemon = True
    #t.start()
    #yap()

def ireplace(old, new, text):
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old):]
        idx = index_l + len(new) 
    return text

async def kelime_turet_baslat(message, **kwargs):
    t0 = time.time()

    chat_id = message.chat.id
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
    

    konumlar = oyun_var_mi(chat_id)
    if konumlar != False:
        bot.send_message(kurucu_id, f'bu asdasd istifadə olunur')
        bot.send_message(chat_id, f'❌ Hörmətli <a href="tg://user?id={user_id}">{first_name}</a>, Hal-hazırda aktiv oyun var')
        return

    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Növbətiyə keç 🧩", callback_data="pas_gec")
    callback_button2 = types.InlineKeyboardButton(text="İpucu 🔎", callback_data="ipucu_kelime")
    #callback_button3 = types.InlineKeyboardButton(text="Harf istiyorum 🌟", callback_data="kelimeturet_harf")

    
    keyboard.add(callback_button1, callback_button2) #, callback_button3


    # Oyun var.

    zorluk = kwargs.get("zorluk", "kolay")

    rastgele_kelime = ""
    #anlam_getir = ""
    if zorluk == "kolay":
        rastgele_sec = random_from_table(tablo = "kelime_turetme_kelimeler")
        rastgele_kelime = rastgele_sec["kelime"]

        #js = rastgele_sec["json"]
        #if "{" in js:
        #    js = json.loads(js)
        #    anlam_getir = js["anlam"]

    elif zorluk == "zor":
        connection = sqlite3.connect("tdk_kelimeler.db")

        connection.row_factory = dict_factory

        crsr = connection.cursor()
        crsr.execute("SELECT * FROM kelimeler ORDER BY RANDOM() LIMIT 1;")
        ans = crsr.fetchall()

        rastgele_kelime = ans[0]["kelime"]

        #js = ans[0]["json"]
        #if "{" in js:
        #    js = json.loads(js)
        #    anlam_getir = js["anlam"]

    #while " " in rastgele_kelime or len(rastgele_kelime)>10:
    #    rastgele_kelime = random_word()

    shuffled = list(rastgele_kelime)

    tum_harfler = shuffled.copy()

    harf_sayisi = len(shuffled)
    #ipucu_sayisi = int(harf_sayisi/5) #4

    ipucu_sayisi = max(round(0.321429 * harf_sayisi - 0.535714) - 1, 0)

    ipuclari = random.sample(shuffled, ipucu_sayisi)


    for i in range(len(shuffled)):  
        if i == 0:
            continue
        elif shuffled[i] in ipuclari:
            ipuclari.remove(shuffled[i])
        elif shuffled[i] == " ":
            shuffled[i] = " "
        else:            
            shuffled[i] = "_"

    #tum_harfler = list(rastgele_kelime)

    # tum_harfler - shuffled
    #  ['d', 'o', 'm', 'a', 't', 'e', 's'] - ['d', '_', '_', 'a', '_', '_', '_']



    while ''.join(tum_harfler) == rastgele_kelime:
        random.shuffle(tum_harfler)

    harfler = ' '.join(tum_harfler)

    shuffled = ' '.join(shuffled)


    #soru_suresi = f(f"soru_suresi")  
    #soru_suresi = str(round(soru_suresi/60,1)).replace(".0","")

    #anlamlar = "Maalesef ki yok."

    js = {}
    
    #anlamlar = ""
    ##if anlam_getir != "":
##
    ##else:
    #try:
    #    anlam = anlam_getir(rastgele_kelime)
    #    anlamlar = "\n".join([f"✍️ <b>Tanım {say+1}: </b> {i}" for say, i in enumerate(random.sample(anlam,min(2,len(anlam))))])
    #    #tdk_getir = tdk.gts.search(rastgele_kelime)[0]
    #    #for say in range(2):
    #    #    try:
    #    #        anlamlar = anlamlar + f"✍️ <b>Tanım {say+1}: </b>" + tdk_getir.meanings[say].meaning + "\n"     
    #    #    except:
    #    #        break
    #except:
    #    pass
    #if anlamlar == "":
    #    anlamlar = "❌ Maalesef ki yok."
    #elif anlam_getir == "": 
    #    if zorluk == "zor":
    #        connection = sqlite3.connect("tdk_kelimeler.db")
#
    #        crsr = connection.cursor()
    #        sql_command = f"UPDATE kelimeler SET json =  {rastgele_kelime}"
    #        crsr.execute(sql_command)
    #        connection.commit()
#
    #        connection.close()


        
    #anlamlar = ireplace(rastgele_kelime, '<span class="tg-spoiler">' + shuffled + ' </span>', anlamlar).strip()

    katsayi = 0.1
    if zorluk == "zor":
        katsayi = 0.4
    puan = harf_sayisi * katsayi

    round_sayisi = kwargs.get("round",1)
    toplam_round = kwargs.get("toplam_round",30)
#🧩 İpucu sayısı: <code>{ipucu_sayisi}</code>
#⌛️ Oyun Süresi: <code>{soru_suresi} dk</code>
#💯 Harf sayısı: <code>{harf_sayisi}</code>
#
#📖 TDK Tanımları:
#{anlamlar}

    text = kwargs.get("text",f"""
💰 Veriləcək xal: <b>{puan:.1f}</b>
🎯 Raund: <b>{round_sayisi}/{toplam_round}</b>
🧩 {harf_sayisi} hərf: <code>{harfler}</code>
🎲 İpucu: <code>{shuffled}</code>
""")

    text = kwargs.get("header","") + text



    
    
    #konumlar = oyun_var_mi(chat_id)
    #if konumlar != False:
    #    bot.send_message(kurucu_id,"burası kullanılıyormuş 778899")
    #    bot.send_message(chat_id, f'❌ Değerli <a href="tg://user?id={user_id}">{first_name}</a>, şu anda zaten aktif bir oyun var.')
    #    return
        

    hata_msg = None

    msg_durum = True
    while msg_durum:
        try:
            if hata_msg != None:
                await bot.edit_message_text(chat_id=chat_id, text=text, reply_markup=keyboard, message_id=hata_msg)
            else:
                await bot.send_message(chat_id, text, reply_markup=keyboard)
            hizlar["kelimeoyunu"] = time.time() - t0



            f(f"groups.{chat_id}.son_oyun_aktivitesi", time.time())
            f(f"groups.{chat_id}.group_size", await bot.get_chat_members_count(chat_id))
            msg_durum = False

            f(f"privates.{user_id}.son-oyun-oynama",time.time())
            f(f"privates.{user_id}.username",username)
            f(f"privates.{user_id}.first_name",first_name)
            
            

            oyun_id = int(time.time() * zaman_hassasiyeti)
            f(f"groups.{chat_id}.oyun", oyun_id)
            f(f"games.{oyun_id}",{
                "round":round_sayisi,
                "toplam_round":toplam_round,
                "skorlar":kwargs.get("skorlar",{}),
                "puan":puan,
                "shuffled": shuffled,

                "kelime":rastgele_kelime,
                "konum":chat_id,
                "oyun_tipi":"kelimeoyunu",
                "zorluk":zorluk
                }
            )
            await log_gonder(user_id=user_id, chat_id=chat_id, eylem="söz törəməsi başladı", game_id = oyun_id)

            return rastgele_kelime
        except Exception as e:
            if "Too Many" in str(e):
                #bot.send_message(chat_id, "❌ Siz çok hızlı oynuyorsunuz değerli oyuncular! Bu da bir hataya yol açtı.")
                #bot.send_message(chat_id, str(e))
                #pass
                if hata_msg == None:
                    hata_msg = bot.send_message(chat_id, "⌛️ Əziz oyunçular, sizi çox az gözlətəcəyəm.").id
                time.sleep(1)
            else:
                bot.send_message(chat_id, "❌ Xəta baş verdi. Zəhmət olmasa bir daha cəhd edin.")
                bot.send_message(kurucu_id, str(e))
                bot.send_message(kurucu_id, get_traceback(e))
                break
    #yap()
    

@bot.message_handler(commands=['oban'])
def oban(message):
    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id

    if not user_id in admins:
        return
    

    msg = message.text

    ayrik = msg.split()
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
    keyboard.add(callback_button1)

    if len(ayrik) == 1:
        try:
            alintilanan_user_id = message.reply_to_message.from_user.id
            
            banli_mi = sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{alintilanan_user_id}'") != []

            if banli_mi:            
                sql_execute(f'DELETE FROM ban_listesi WHERE id="{alintilanan_user_id}"') 
                bot.send_message(chat_id, f"✅ {message.reply_to_message.from_user.first_name} ({alintilanan_user_id}) artık yasaksız", reply_markup=keyboard, reply_to_message_id=message.id)
            else:
                sql_execute(f"INSERT INTO ban_listesi (id) VALUES ('{alintilanan_user_id}')") 
                bot.send_message(chat_id, f"🗡 {message.reply_to_message.from_user.first_name} ({alintilanan_user_id}) artık yasaklı", reply_markup=keyboard, reply_to_message_id=message.id)
                try:
                    if alintilanan_user_id == chat_id:
                        bot.send_message(chat_id, "⚠️ Grup bot tarafından engellenmiştir.")
                        bot.leave_chat(chat_id)
                except Exception as e:
                    print("sadsadsad",e,chat_id)
        except:
            bot.send_message(chat_id,f"""
Heç bir adam sitat gətirməyib!
            """, reply_to_message_id=message.id, reply_markup=keyboard)

    elif len(ayrik) == 2:
        banli_mi = sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{ayrik[1]}'") != []

        if banli_mi:            
            sql_execute(f'DELETE FROM ban_listesi WHERE id="{ayrik[1]}"') 
            bot.send_message(chat_id, f"✅ {ayrik[1]} artıq qadağan deyil", reply_markup=keyboard, reply_to_message_id=message.id)
        else:
            sql_execute(f"INSERT INTO ban_listesi (id) VALUES ('{ayrik[1]}')") 
            bot.send_message(chat_id, f"🗡 {ayrik[1]} indi qadağandır", reply_markup=keyboard, reply_to_message_id=message.id)
            try:
                if alintilanan_user_id == chat_id:
                    bot.send_message(chat_id, "⚠️ Qrup bot tərəfindən bloklanıb.")
                    bot.leave_chat(chat_id)
            except Exception as e:
                print("sadsadsad",e,chat_id)
                pass
    elif len(ayrik) == 3:
        bot.send_message(chat_id, f"Zəhmət olmasa əmri belə daxil edin: /oban {ayrik[2]}", reply_markup=keyboard, reply_to_message_id=message.id)



@bot.message_handler(commands=['games'])
async def games(message):
    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id

    if not user_id in admins:
        return
    msg = message.text


    txt = ""
    oyunlar = f("games")

    if type(oyunlar) is dict:
        oyunlar = [oyunlar]


    if msg == "/games detailed":
        for n,i in enumerate(oyunlar):
            id = i["id"]
            js = json.loads(i["json"])
            txt += f"<b>{n + 1}.</b> {id}\n"
            for j in js:
                txt += f"   <b>{j}:</b> {js[j]}\n"
            txt += "\n"
    else:
        for n,i in enumerate(oyunlar):
            i = i["id"]
            konum = f(f"games.{i}.konum")
            txt += f"""{n+1}. {f(f"groups.{konum}.username")}
            = {i}
            {konum} \t- {f(f"games.{i}.oyun_tipi")}
            {f(f"games.{i}.kelime")} - {f(f"games.{i}.açan_user")}

        """


    if txt == "":
        txt = "Heç bir oyun yoxdur"

        
    # Split the text each 3000 characters.
    # split_string returns a list with the splitted text.
    splitted_text = util.smart_split(txt, chars_per_string=3000)

    for text in splitted_text:
        await bot.send_message(chat_id,text)



async def send_msgimg(chat_id, msg, reply_to_message_id=None, reply_markup=None):
    if "http" in msg:
        ayir = msg.split("\n")

        resim_url = ""
        for n, i in enumerate(ayir):
            if "http" in i:
                resim_url = i
                del ayir[n]
                break
        yazi = "\n".join(ayir)
        try:
            await bot.send_photo(chat_id, resim_url, caption=yazi, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
        except:
            pass
    else:
        try:
            await bot.send_message(chat_id, msg, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
        except:
            pass


@bot.message_handler(commands=['c'])
async def cesaret(message):
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

    #chat_tipi = message.chat.type

    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id #sabit    
    
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="🎯 Doğruluq", callback_data="dogrulukcesaret_d")
    callback_button2 = types.InlineKeyboardButton(text="🌟 Cəsarət", callback_data="dogrulukcesaret_c")
    keyboard.add(callback_button1, callback_button2)
    
    yazi = f"<a href='tg://user?id={user_id}'>{first_name}</a> <b>cəsarəti</b> seçdi\n\n"

    getir = sql_get(f"SELECT * FROM dogruluk_cesaret WHERE tur LIKE 'c' ORDER BY RANDOM() LIMIT 1;")
    yazi = yazi + getir["yazi"]
    await send_msgimg(chat_id,yazi)


@bot.message_handler(commands=['d'])
async def dogruluk(message):
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

    #chat_tipi = message.chat.type

    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id #sabit    
    
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="🙂 Doğruluq", callback_data="dogrulukcesaret_d")
    callback_button2 = types.InlineKeyboardButton(text="🥳 Cəsarət ", callback_data="dogrulukcesaret_c")
    keyboard.add(callback_button1, callback_button2)
    
    yazi = f"<a href='tg://user?id={user_id}'>{first_name}</a> <b>doğruluğu</b> seçdi\n\n"

    getir = sql_get(f"SELECT * FROM dogruluk_cesaret WHERE tur LIKE 'd' ORDER BY RANDOM() LIMIT 1;")
    yazi = yazi + getir["yazi"]
    await send_msgimg(chat_id,yazi)







@bot.message_handler(commands=['reytinq'])
async def skorlar_komut(message):    #chat_tipi = message.chat.type
    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id


    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="✍️ Söz oyunu", callback_data="skor_sessizsinema")
    callback_button2 = types.InlineKeyboardButton(text="🧩 Boş xana", callback_data="skor_kelimeoyunu")
    keyboard.add(callback_button1)
    keyboard.add(callback_button2)
    yazi = f"📜 Hansı oyunun xallarənə görmək istərdiniz?"
    try:
        id = message.id
        await bot.edit_message_text(chat_id=chat_id, message_id=id, text=yazi, reply_markup=keyboard)
    except:
        await bot.send_message(chat_id, yazi, reply_to_message_id=message.id, reply_markup=keyboard)

@bot.message_handler(commands=['game'])
async def baslat(message):
    chat_tipi = message.chat.type

    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id #sabit    


    if sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{chat_id}'") != []:
        await bot.send_message(chat_id, "⚠️ Qrup bot tərəfindən bloklanıb.")
        await bot.leave_chat(chat_id)
        return
    elif sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{user_id}'") != []:
        return


    
    konumlar = oyun_var_mi(chat_id) #oyun_konum grup_konum
    if chat_tipi == "private":
        await bot.send_message(message.chat.id, "Bu əmr yalnız qrup üçün istifadə edilə bilər.")
        return
    if konumlar != False:
        await bot.send_message(message.chat.id, "🎯 Oyun artıq başlayıb.\nDayandırmaq üçün /stop")
        return

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


    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="🐊 Söz oyunu", callback_data="sessiz_sinema")
    callback_button2 = types.InlineKeyboardButton(text="🧩 Boş xana", callback_data="kelimeoyunu")
    callback_button3 = types.InlineKeyboardButton(text="🔞 Doğruluq yoxsa Cəsarət", callback_data="dogrulukcesaret")
    keyboard.add(callback_button1)
    keyboard.add(callback_button2)
    keyboard.add(callback_button3)
    await bot.send_message(chat_id, f"📜 Zəhmət olmasa oyun növü seçin.", reply_markup=keyboard)

#@bot.message_handler(state=MyStates.kelime)
async def kelime_gir(message, grup_id): #grup_id    
    user_id = message.from_user.id #sabit
    chat_id = grup_id

    oyun_id = f(f"groups.{chat_id}.oyun")

    if f(f"games.{oyun_id}.açan_id") == user_id:
        yeni_kelime = message.text[:500]
        #keyboard = types.InlineKeyboardMarkup()
        #callback_button1 = types.InlineKeyboardButton(text="Oyuna geri dön .", url=f"tg://user?id={grup_id}")
        #keyboard.add(callback_button1)
        await bot.send_message(user_id,"👍 İndi yeni sual: "+yeni_kelime) #, reply_markup=keyboard
        f(f"games.{oyun_id}.kelime", yeni_kelime)

        with open('girilen_kelimeler.txt', 'a') as myfile:
            myfile.write(yeni_kelime+"\n")

        #keyboard = types.InlineKeyboardMarkup()
        #callback_button = types.InlineKeyboardButton(text="Sunucuya geri dön", url="tg://user?id="+grup_id)
        #keyboard.add(callback_button)

async def is_subscribed(chat_id, user_id):
    try:
        get = await bot.get_chat_member(chat_id, user_id) #gruba hiç girmemişse

        if get.status == "left": #gruptan çıkmışsa
            return False
        return True
    except ApiTelegramException as e:
        if e.result_json['description'] == 'Səhv sorğu: istifadəçi tapılmadı':
            return False


async def skor_master(cagri):    
    max_skor = 20

    sorgu = cagri.data
    chat_id = str(cagri.message.json["chat"]["id"]) #değişken
    user_id = cagri.from_user.id #sabit        


    # chat_tipi = cagri.message.chat.type

    keyboard = types.InlineKeyboardMarkup()
    # if chat_tipi == "private":
    #     callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
    #     callback_button3 = types.InlineKeyboardButton(text="🔙 Geri dön", callback_data=f'skor_')
    #     keyboard.add(callback_button1, callback_button3)
    #     bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="• Bu komut sadece gruplarda çalışır.", reply_markup=keyboard)
    #     return
    
    first_name = None
    if cagri.from_user.first_name != None:
        first_name = cagri.from_user.first_name
        first_name = first_name.replace("'","").replace("<","").replace(">","")

    username = None
    if cagri.from_user.username != None:
        username = cagri.from_user.username
        username = username.replace("'","").replace("<","").replace(">","")
    else:
        username = first_name
        username = username.replace("'","").replace("<","").replace(">","")
    
    ayir = sorgu.split("_")

    ne_skoru = ayir[1]
    
    if len(ayir) == 2:
        if ne_skoru == "sessizsinema":
            callback_button1 = types.InlineKeyboardButton(text="Qlobal puan 🌐", callback_data="skor_sessizsinema_kureselskor")
            callback_button2 = types.InlineKeyboardButton(text="Mənim puam 📊", callback_data="skor_sessizsinema_skorum")
            callback_button3 = types.InlineKeyboardButton(text="Qrup puan 💬", callback_data="skor_sessizsinema_skor")           
            geri_don_btn = types.InlineKeyboardButton(text="🔙 Geri", callback_data='skor_')
            keyboard.add(callback_button2, callback_button1)
            keyboard.add(callback_button3)
            keyboard.add(geri_don_btn)

            await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="🔸 Hansı puanları görmək istərdiniz?", reply_markup=keyboard)
        elif ne_skoru == "kelimeoyunu":
            callback_button1 = types.InlineKeyboardButton(text="Qlobal puan 🌐", callback_data="skor_kelimeoyunu_kureselskor")
            callback_button3 = types.InlineKeyboardButton(text="Qrup puan 💬", callback_data="skor_kelimeoyunu_skor")
            geri_don_btn = types.InlineKeyboardButton(text="🔙 Geri", callback_data='skor_')
            keyboard.add(callback_button1, callback_button3)
            keyboard.add(geri_don_btn)

            await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="🔸 Hansı puanları görmək istərdiniz?", reply_markup=keyboard)
        else:
            await bot.answer_callback_query(cagri.id, text="😞")
    else:
        tip = ayir[2]

        if ne_skoru == "sessizsinema":
            if tip == "skor":
                skorlar = f(f"groups.{chat_id}.bilme-sayıları")

                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)

                if skorlar!=[] and "dict" in str(type(skorlar)):
                    txt = f"Bu qrupda ən yaxşı {max_skor} oyunçu 📜\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))
                    skorlar_list = list(skorlar)[::-1][:max_skor]


                    #txt += "\n".join([f"<b>{n+1}</b>. {f('privates.{i}.first_name')} - {skorlar[i]} cevap" for n,i in enumerate(skorlar_list)])
                    for n,i in enumerate(skorlar_list):
                        if n+1 < 4:
                            txt += "👑 "
                        else:
                            txt += "▫️ "
                            #if n+1 == 1:
                            #    txt += " 👑"
                            #elif n+1 == 2:
                            #    txt += " 👑"
                            #elif n+1 == 3:
                            #    txt += " 👑"
                        first_name = f(f'privates.{i}.first_name')
                        username = f(f'privates.{i}.username')
                        if first_name != "":
                            txt += f"<b>{n+1}</b>. {first_name} - <code>{skorlar[i]}</code> cavab"
                        elif username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{skorlar[i]}</code> cavab"

                        txt += "\n"


                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                #elif not "list" in str(type(skorlar)):
                #    bot.send_message(chat_id,"Skorlarınızda bir hata vardı, düzelttim!")
                #    f(f"groups.{chat_id}.bilme-sayıları", "$del")
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="Hələ heç bir xal yoxdur.", reply_markup=keyboard)
            elif tip == "skorum":                  
                sunucu_sayisi = f(f"groups.{chat_id}.sunucu-sayıları.{user_id}")
                if sunucu_sayisi == "":
                    sunucu_sayisi = 0

                anlatmis = f(f"groups.{chat_id}.anlatma-sayıları.{user_id}")
                if anlatmis == "":
                    anlatmis = 0

                bilme = f(f"groups.{chat_id}.bilme-sayıları.{user_id}")
                if bilme == "":
                    bilme = 0

                txt = f'''👤 {first_name} oyunçunun puanları

🔹 Bu qrupda
Aparıcı olub: \t{sunucu_sayisi}
Uğurla təqdim edildi: \t{anlatmis}
Tapdığı cavablar: \t{bilme}

🔸 Bütün qruplarda
Aparıcı olub: \t{f(f"privates.{user_id}.sunucu-sayısı")}
Uğurla təqdim edildi: \t{f(f"privates.{user_id}.anlatma-sayısı")}
Tapdığı cavablar: \t{f(f"privates.{user_id}.bilme-sayısı")}
            '''

                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
            elif tip == "kureselskor":
                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                
                kullanicilar = f(f"privates", output="$array")

                if "dict" in str(type(kullanicilar)):
                    kullanicilar = [kullanicilar]


                liste = []

                for kullanici in kullanicilar:   
                    id = kullanici["id"]
                    bilme_sayisi = json.loads(kullanici["json"])
                    #bilme_sayisi = f(f"privates.{kullanici}.bilme-sayısı")

                    if "bilme-sayısı" in bilme_sayisi:
                        kullanici = id
                        bilme_sayisi = bilme_sayisi["bilme-sayısı"]

                        liste.append([kullanici,int(bilme_sayisi)])

                liste.sort(key=lambda x:x[1])
                skorlar_list = list(liste)[::-1]

                sira = "∞"
                for n, i in enumerate(skorlar_list):
                    if i[0] == str(user_id):
                        sira = n+1
                        break
                
                skorlar_list = skorlar_list[:max_skor]


                #txt = "En iyi max_skor Grup 📜\n\n" + "\n".join([f"<b>{n+1}</b>. {f(f'groups.{i[0]}.username')} - {i[1]} cevap" for n,i in enumerate(skorlar_list)])
                txt = f"Bütün zamanların ən yaxşı {max_skor} oyunçusu 📜\n\n"
                
                for n,i in enumerate(skorlar_list):
                    if n+1 < 6:
                        if n+1 == 1:
                            txt += "🥇 "
                        elif n+1 == 2:
                            txt += "🥈 "
                        elif n+1 == 3:
                            txt += "🥉 "
                        else:
                            txt += "👑 "
                    else:
                        txt += "▫️ "

                    firstname = f(f'privates.{i[0]}.first_name')
                    username = f(f'privates.{i[0]}.username')
                    if firstname != "":
                        txt += f"<b>{n+1}</b>. {firstname} - <code>{i[1]}</code> cavab"
                        
                    elif username != "":
                        txt += f"<b>{n+1}</b>. {username} - <code>{i[1]}</code> cavab"


                    txt += "\n"

                txt += f"\n💎 Sən {sira} sıradasan {first_name}"
                #bot.send_message(chat_id, txt, reply_markup=keyboard)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
            elif tip == "haftalikgrup":
                skorlar = f(f"groups.{chat_id}.haftalık-bilme-sayıları")

                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)

                if skorlar!=[] and skorlar != "":
                    txt = "Qrupda həftənin ən yaxşı oyunçuları 📜\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))

                    sira = "∞"
                    
                    skorlar_list = list(skorlar)[::-1]
                    for n, i in enumerate(skorlar_list):
                        if i[0] == str(user_id):
                            sira = n+1
                            break
                    
                    skorlar_list = list(skorlar)[::-1][:max_skor]

                    for n,i in enumerate(skorlar_list):
                        first_name = f(f'privates.{i}.first_name')
                        username = f(f'privates.{i}.username')

                        if first_name != "":
                            txt += f"<b>{n+1}</b>. {first_name} - <code>{skorlar[i]}</code> cavab\n"
                            
                        elif username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{skorlar[i]}</code> cavab\n"


                        #txt += "\n".join([f"<b>{n+1}</b>. {f('privates.{i}.first_name')} - {skorlar[i]} cevap" for n,i in enumerate(skorlar_list)])
                        
                    txt += "\n"

                    txt += f"\n💎 Sən {sira} sıradasan {first_name}"
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="Hələ heç bir xal yoxdur.", reply_markup=keyboard)
            elif tip == "haftalikskorprivate":
                #chat_tipi = message.chat.type

                #chat_id = message.chat.id #değişken, private veya group
                #user_id = message.from_user.id #sabit


                ww = f(f"haftalık-bilme-sayıları")        
                skorlar = ww

                for i in ww.copy():
                    try:
                        _ = int(ww[i])
                    except:
                        del ww[i]

                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                if skorlar!=[]:
                    txt = "Qlobal həftənin ən yaxşı oyunçuları 📜\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1])[::-1])


                    for n, i in enumerate(skorlar):
                        if n+1>max_skor:
                            break
                        first_name = f(f'privates.{i}.first_name')
                        username = f(f'privates.{i}.username')

                        cevap_sayisi = skorlar[i]


                        if n+1 < 4:
                            if n+1 == 1:
                                txt += "🥇 "
                            elif n+1 == 2:
                                txt += "🥈 "
                            elif n+1 == 3:
                                txt += "🥉 "
                        else:
                            txt += "▫️ "

                        if first_name != "":
                            txt += f"<b>{n+1}</b>. {first_name} - <code>{cevap_sayisi}</code> cavab"
                            
                        elif username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{cevap_sayisi}</code> cavab"

                        txt += "\n"

                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="Hələ xal yoxdur.", reply_markup=keyboard)
            elif tip == "haftalikskorgroup":
                #chat_tipi = message.chat.type

                #chat_id = message.chat.id #değişken, private veya group
                #user_id = message.from_user.id #sabit


                ww = f(f"grup-haftalık-bilme-sayıları")        
                skorlar = ww

                for i in ww.copy():
                    try:
                        _ = int(ww[i])
                    except:
                        del ww[i]

                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                if skorlar!=[]:
                    txt = "Qlobal həftənin ən yaxşı qrupları 📜\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1])[::-1])


                    for n, i in enumerate(skorlar):
                        if n+1>max_skor:
                            break
                        username = f(f'groups.{i}.username')

                        cevap_sayisi = skorlar[i]


                        if n+1 < 4:
                            if n+1 == 1:
                                txt += "🥇 "
                            elif n+1 == 2:
                                txt += "🥈 "
                            elif n+1 == 3:
                                txt += "🥉 "
                        else:
                            txt += "▫️ "
                            
                        if username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{cevap_sayisi}</code> cavab"
                        else:
                            txt += f"<b>{n+1}</b>. ? - <code>{cevap_sayisi}</code> cavab"


                        txt += "\n"

                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="Hələ xal yoxdur", reply_markup=keyboard)
            elif tip == "kureselgrup":
                groups = f(f"groups", output="$array")


                liste = []
                for group in groups:
                    bilme_sayisi = json.loads(group["json"])
                    #bilme_sayisi = f(f"privates.{kullanici}.bilme-sayısı")

                    if "toplam-bilme-sayısı" in bilme_sayisi:
                        group = group["id"]
                        bilme_sayisi = bilme_sayisi["toplam-bilme-sayısı"]
                        #liste.append([[kullanici,int(bilme_sayisi)]])

                        liste.append([group,int(bilme_sayisi)])
                        
                        

                liste.sort(key=lambda x:x[1])
                skorlar_list = list(liste)[::-1]

                
                sira = "∞"
                for n, i in enumerate(skorlar_list):
                    if i[0] == chat_id:
                        sira = n+1
                        break

                skorlar_list = skorlar_list[:max_skor]

                #txt = "En iyi max_skor Grup 📜\n\n" + "\n".join([f"<b>{n+1}</b>. {f(f'groups.{i[0]}.username')} - {i[1]} cevap" for n,i in enumerate(skorlar_list)])
                txt = f"Ən yaxşı {max_skor} Qrup 📜\n\n"
                
                for n,i in enumerate(skorlar_list):
                    first_name = f(f'groups.{i[0]}.first_name')
                    username = f(f'groups.{i[0]}.username')
                    if n+1 < 4:
                        if n+1 == 1:
                            txt += "💎🥇 "
                        elif n+1 == 2:
                            txt += "🥈 "
                        elif n+1 == 3:
                            txt += "🥉 "
                    else:
                        txt += "▫️ "

                    if first_name != "":
                        txt += f"<b>{n+1}</b>. {first_name} - <code>{i[1]}</code> cavab"
                        
                    elif username != "":
                        txt += f"<b>{n+1}</b>. {username} - <code>{i[1]}</code> cavab"

                    txt += "\n"
                txt += f"\n💎 Bu qrup {sira} sıradadır."

                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
        
        elif ne_skoru == "kelimeoyunu":          
            if tip == "kureselskor":
                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                
                kullanicilar = f(f"privates", output="$array")

                if "dict" in str(type(kullanicilar)):
                    kullanicilar = [kullanicilar]


                liste = []

                for kullanici in kullanicilar:   
                    id = kullanici["id"]
                    bilme_sayisi = json.loads(kullanici["json"])
                    #bilme_sayisi = f(f"privates.{kullanici}.bilme-sayısı")

                    if "kelime-turet-bilme" in bilme_sayisi:
                        kullanici = id
                        bilme_sayisi = bilme_sayisi["kelime-turet-bilme"]

                        liste.append([kullanici,bilme_sayisi])

                liste.sort(key=lambda x:x[1])
                skorlar_list = list(liste)[::-1]

                sira = "∞"
                for n, i in enumerate(skorlar_list):
                    if i[0] == str(user_id):
                        sira = n+1
                        break
                
                skorlar_list = skorlar_list[:max_skor]


                #txt = "En iyi max_skor Grup 📜\n\n" + "\n".join([f"<b>{n+1}</b>. {f(f'groups.{i[0]}.username')} - {i[1]} cevap" for n,i in enumerate(skorlar_list)])
                txt = f"Bütün zamanların ən yaxşı {max_skor} oyunçusu 📜\n\n"
                
                for n,i in enumerate(skorlar_list):
                    if n+1 < 6:
                        if n+1 == 1:
                            txt += "🥇 "
                        elif n+1 == 2:
                            txt += "🥈 "
                        elif n+1 == 3:
                            txt += "🥉 "
                        else:
                            txt += "👑 "
                    else:
                        txt += "▫️ "

                    firstname = f(f'privates.{i[0]}.first_name')
                    username = f(f'privates.{i[0]}.username')
                    
                    if firstname != "":
                        txt += f"<b>{n+1}</b>. {firstname} - <code>{i[1]:.0f}</code> xal" #:.2f
                        
                    elif username != "":
                        txt += f"<b>{n+1}</b>. {username} - <code>{i[1]:.0f}</code> xal"


                    txt += "\n"

                txt += f"\n💎 Sən {sira} sıradasan {first_name}"
                #bot.send_message(chat_id, txt, reply_markup=keyboard)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
            elif tip == "skor":
                skorlar = f(f"groups.{chat_id}.kelime-turet-bilme")

                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)

                if skorlar!=[] and "dict" in str(type(skorlar)):
                    txt = f"Bu qrupda ən yaxşı {max_skor} oyunçu 📜\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))                   

                    skorlar_list = list(skorlar)[::-1][:max_skor]

                    #txt += "\n".join([f"<b>{n+1}</b>. {f('privates.{i}.first_name')} - {skorlar[i]} cevap" for n,i in enumerate(skorlar_list)])
                    for n,i in enumerate(skorlar_list):
                        if n+1 < 4:
                            txt += "👑 "
                        else:
                            txt += "▫️ "
                            #if n+1 == 1:
                            #    txt += " 👑"
                            #elif n+1 == 2:
                            #    txt += " 👑"
                            #elif n+1 == 3:
                            #    txt += " 👑"
                        first_name = f(f'privates.{i}.first_name')
                        username = f(f'privates.{i}.username')

                        if first_name != "":
                            txt += f"<b>{n+1}</b>. {first_name} - <code>{skorlar[i]:.0f}</code> xal"
                        elif username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{skorlar[i]:.0f}</code> xal"

                        txt += "\n"

                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                #elif not "list" in str(type(skorlar)):
                #    bot.send_message(chat_id,"Skorlarınızda bir hata vardı, düzelttim!")
                #    f(f"groups.{chat_id}.bilme-sayıları", "$del")
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="Hələ heç bir xal yoxdur.", reply_markup=keyboard)
            elif tip == "kureselgrup":
                groups = f(f"groups", output="$array")


                liste = []
                for group in groups:
                    bilme_sayisi = json.loads(group["json"])
                    #bilme_sayisi = f(f"privates.{kullanici}.bilme-sayısı")

                    if "toplam-kelime-turet-bilme" in bilme_sayisi:
                        group = group["id"]
                        bilme_sayisi = bilme_sayisi["toplam-kelime-turet-bilme"]
                        #liste.append([[kullanici,int(bilme_sayisi)]])

                        liste.append([group,bilme_sayisi])
                        
                        
                liste.sort(key=lambda x:x[1])
                skorlar_list = list(liste)[::-1]
                
                sira = "∞"
                for n, i in enumerate(skorlar_list):
                    if i[0] == chat_id:
                        sira = n+1
                        break
                
                skorlar_list = skorlar_list[:max_skor]

                #txt = "En iyi max_skor Grup 📜\n\n" + "\n".join([f"<b>{n+1}</b>. {f(f'groups.{i[0]}.username')} - {i[1]} cevap" for n,i in enumerate(skorlar_list)])
                txt = f"Ən yaxşı {max_skor} Qrup 📜\n\n"
                
                for n,i in enumerate(skorlar_list):
                    first_name = f(f'groups.{i[0]}.first_name')
                    username = f(f'groups.{i[0]}.username')
                    if n+1 < 4:
                        if n+1 == 1:
                            txt += "💎🥇 "
                        elif n+1 == 2:
                            txt += "🥈 "
                        elif n+1 == 3:
                            txt += "🥉 "
                    else:
                        txt += "▫️ "

                    if first_name != "":
                        txt += f"<b>{n+1}</b>. {first_name} - <code>{i[1]:.0f}</code> xal"
                        
                    elif username != "":
                        txt += f"<b>{n+1}</b>. {username} - <code>{i[1]:.0f}</code> xal"

                    txt += "\n"
                
                txt += f"\n💎 Bu qrup isə {sira} sıradadır."

                callback_button1 = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="🔙 Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)

        else:
            await bot.answer_callback_query(cagri.id, text="😞")

    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    #try:
    #    return loop.run_until_complete(yap())
    #finally:
    #    loop.close()
    #    asyncio.set_event_loop(None)

@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(cagri): #çağrıcı cagrici
    #grup veya kullanıcı id
    t0 = time.time()

    chat_id = str(cagri.message.json["chat"]["id"]) #değişken
    user_id = cagri.from_user.id #sabit

    

    if sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{chat_id}'") != []:
        await bot.send_message(chat_id, "⚠️ Qrup bot tərəfindən bloklanıb.")
        await bot.leave_chat(chat_id)
        return
    elif sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{user_id}'") != []:
        await bot.answer_callback_query(cagri.id, '⚠️ Siz botdan bloklanmısınız.', show_alert=True)
        return

    sorgu = cagri.data


    if not await is_subscribed(chat_id, user_id):
        # user is not subscribed. send message to the user
        await bot.answer_callback_query(cagri.id, '⛱ Zəhmət olmasa qrupa daxil olun.')
        #bot.send_message(kurucu_id, "Gereksiz değil. 11223344")
        return

    first_name = None
    if cagri.from_user.first_name != None:
        first_name = cagri.from_user.first_name
        first_name = first_name.replace("'","").replace("<","").replace(">","")

    username = None
    if cagri.from_user.username != None:
        username = cagri.from_user.username
        username = username.replace("'","").replace("<","").replace(">","")

    cagri.message.from_user = cagri.from_user #eğer bunu yapmazsak bot sunar


    #private or group
    msg_type = cagri.message.json["chat"]["type"]


    if "group" in msg_type:
        grup_username = cagri.message.json["chat"]["title"]
        grup_username = grup_username.replace("'","")

        if f(f"groups.{chat_id}.username") == "":
            await bot.send_message(-1001897431491, f"📜 {grup_username} ⟶ {len(f('groups')) + 1}")
            
        f(f"groups.{chat_id}.username", grup_username) 
        f(f"groups.{chat_id}.son_oyun_aktivitesi", time.time())

    #f(f"privates.{user_id}.first_name", first_name)
    #f(f"privates.{user_id}.username", username)        
    #f(f"privates.{user_id}.son-oyun-oynama",time.time())
    if sorgu == "kelimeturet_harf":
        await bot.answer_callback_query(cagri.id, f'Yaxında... ☺️', show_alert=False)
        return
    elif sorgu.startswith("sessiz_sinema"):               
        if oyun_var_mi(chat_id) != False:
            await bot.answer_callback_query(cagri.id, f'❌ Hörmətli {first_name}, hazırda aktiv oyunlar var.', show_alert=False)
            return
        
        if sorgu == "sessiz_sinema":
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text="👥 Sıralı aparıcı", callback_data="sessiz_sinema_oto-sunucu")
            callback_button2 = types.InlineKeyboardButton(text="📌 Sabit aparıcı", callback_data="sessiz_sinema_sabit")
            callback_button3 = types.InlineKeyboardButton(text="🔈 Normal aparıcı", callback_data="sessiz_sinema_normal")
            keyboard.add(callback_button1, callback_button2)
            keyboard.add(callback_button3)
            await bot.edit_message_text(f'🎯 Oyun modu nə olsun?', chat_id, cagri.message.id, reply_markup=keyboard)
        else:
            mod = sorgu.split("_")[-1]    
        
            await bot.delete_message(chat_id, cagri.message.id)

            await sessiz_sinema_baslat(cagri.message, mod = mod)
        
        #t = threading.Thread(target = sessiz_sinema_baslat, kwargs = {"message" : cagri.message})
        #t.daemon = True
        #t.start()
        return
    elif sorgu.startswith("kelimeoyunu"):       
        if oyun_var_mi(chat_id) != False:
            await bot.answer_callback_query(cagri.id, f'❌ Hörmətli {first_name}, hazırda aktiv oyunlar var.', show_alert=False)
            return

        #bot.delete_message(chat_id, cagri.message.id)

        if sorgu.startswith("kelimeoyunu_"):   
            ayir = sorgu.split("_")
            if len(ayir) == 2:
                birlestir = "_".join(ayir[:2])
                kolay_callback = birlestir + "_kolay"
                zor_callback = birlestir + "_zor"

                keyboard = types.InlineKeyboardMarkup()
                callback_button1 = types.InlineKeyboardButton(text="🧠 Asan (x1 puan)", callback_data=kolay_callback)
                callback_button2 = types.InlineKeyboardButton(text="💣 Çətin (x4 puan)", callback_data=zor_callback)
                keyboard.add(callback_button1, callback_button2)
                #bot.send_message(chat_id, f'🎯 <a href="tg://user?id={user_id}">{first_name}</a>, {ayir[1]} round oyunun zorluğu ne olsun?', reply_markup=keyboard)                
                await bot.edit_message_text(f'<a href="tg://user?id={user_id}">{first_name}</a> {ayir[1]} raund seçdi.\n🤔 Oyunun çətinliyi nə olsun?', chat_id, cagri.message.id, reply_markup=keyboard)
                return
            elif len(ayir) == 3:
                if ayir[1] == "inf":
                    ayir[1] = 999999
                await kelime_turet_baslat(cagri.message, toplam_round = int(ayir[1]), zorluk = ayir[2])                
                await bot.delete_message(chat_id, cagri.message.id)
                #t = threading.Thread(target = kelime_turet_baslat, kwargs = {
                #        "message" : cagri.message, 
                #        "toplam_round" : int(ayir[1]),
                #        "zorluk" : ayir[2]
                #    })
                #t.daemon = True
                #t.start()
            else:
                await bot.send_message(chat_id, f'🤷')
        else:
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text="15", callback_data="kelimeoyunu_15")
            callback_button2 = types.InlineKeyboardButton(text="30", callback_data="kelimeoyunu_30")
            callback_button3 = types.InlineKeyboardButton(text="45", callback_data="kelimeoyunu_45")
            callback_button4 = types.InlineKeyboardButton(text="60", callback_data="kelimeoyunu_60")
            callback_button5 = types.InlineKeyboardButton(text="75", callback_data="kelimeoyunu_75")
            callback_button6 = types.InlineKeyboardButton(text="90", callback_data="kelimeoyunu_90")
            callback_button7 = types.InlineKeyboardButton(text="Sonsuz ♾", callback_data="kelimeoyunu_inf")
            
            keyboard.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6)
            keyboard.add(callback_button7)
            await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{first_name}</a> oyun neçə raund olsun?', reply_markup=keyboard)
            
            if not "skor" in cagri.message.text.lower():
                await bot.delete_message(chat_id, cagri.message.id)
            return      
    elif sorgu.startswith("ipucu"):
        #ipucu_kelime
        oyun = oyun_var_mi(chat_id)
        if oyun_var_mi(chat_id) == False:
            await bot.answer_callback_query(cagri.id, f'Hörmətli {first_name} hazırda aktiv oyun yoxdur.', show_alert=False)
            return

        oyun_id = oyun[0]

        if sorgu == "ipucu_kelime":
            kelime = f(f"games.{oyun_id}.kelime")
            anlamlar = ""
            try:
                anlam = anlam_getir(kelime)
                anlamlar = "\n".join([f"✍️ Tərif {say+1}: {i}" for say, i in enumerate(random.sample(anlam,min(2,len(anlam))))])
                #tdk_getir = tdk.gts.search(rastgele_kelime)[0]
                #for say in range(2):
                #    try:
                #        anlamlar = anlamlar + f"✍️ <b>Tanım {say+1}: </b>" + tdk_getir.meanings[say].meaning + "\n"     
                #    except:
                #        break
            except:
                pass
            if anlamlar == "":
                anlamlar = "❌ Təssüf ki, yox."
            else:                
                anlamlar = ireplace(kelime, '❓', anlamlar).strip()

            try:
                await bot.answer_callback_query(cagri.id, f'🔎 Məsləhətlər:\n{anlamlar}', show_alert=True)
            except:
                await bot.answer_callback_query(cagri.id, f'🔎 Məsləhətlər:\n{anlamlar[:100]}', show_alert=True)

    elif sorgu.startswith("istiyorum"):
        #bot.answer_callback_query(cagri.id, "Sen — sunucusun, senin kelimen kagawa", show_alert=True)
        #sunucu_olma_sureleri[chat_id] = [user_id,time.time()]

        oyun = oyun_var_mi(chat_id)
        if oyun != False:
            await bot.answer_callback_query(cagri.id, "📜 Oyun onsuzda başladı.", show_alert=False)
            return

        #bot.delete_message(chat_id, cagri.message.id)

        if "sinema_" in sorgu:
            ayir = sorgu.split("_")
            mod = ayir[3]
            # istiyorum_sessiz_sinema_mod_userid
            if len(ayir) == 4: #istiyorum_mod
                await sessiz_sinema_baslat(cagri.message, mod = mod)
            elif len(ayir) == 5: # istiyorum_mod_userid
                userid = ayir[4]
                if time.time() - cagri.message.date < 7:
                    if userid == str(user_id):
                        await sessiz_sinema_baslat(cagri.message,  mod = mod)
                    else:
                        bekle = int(time.time() - cagri.message.date)
                        await bot.answer_callback_query(cagri.id, f"📜 {7-bekle} saniyə gözləyin.", show_alert=False)
                        #print(f"{first_name} ⟹ {userid} ({type(userid)}) | {user_id} ({type(user_id)})")
                else:
                    await sessiz_sinema_baslat(cagri.message, mod = mod)
        else:
            await sessiz_sinema_baslat(cagri.message)

        #t = threading.Thread(target = sessiz_sinema_baslat, kwargs = {"message" : cagri.message})
        #t.daemon = True
        #t.start()
        return    
    elif sorgu == "pas_gec":
        konumlar = oyun_var_mi(chat_id) #oyun_konum grup_konum
        if konumlar != False:
            oyun_id = konumlar[0]

            gecen = int(time.time() - oyun_id/zaman_hassasiyeti)
            if gecen < 6:
                await bot.answer_callback_query(cagri.id, f"📜 Keçmək üçün 6 saniyə keçməlidir, hazırda keçir: {gecen}", show_alert=True)
                return

            if f(f"games.{oyun_id}.oyun_tipi") == "kelimeoyunu":
                kelime = f(f"games.{oyun_id}.kelime")

                skorlar = f(f"games.{oyun_id}.skorlar")
                round = f(f"games.{oyun_id}.round")
                toplam_round = f(f"games.{oyun_id}.toplam_round")
                zorluk = f(f"games.{oyun_id}.zorluk")

                oyunu_iptal_et(oyun_id)
                #bot.send_message(chat_id,f'❌ <a href="tg://user?id={user_id}">{first_name}</a> kelimeyi pas geçti! Doğru cevap → <b>{kelime}</b> idi.')
                await kelime_turet_baslat(cagri.message, toplam_round = toplam_round, round = round, skorlar = skorlar, zorluk = zorluk, header = f'❌ <a href="tg://user?id={user_id}">{first_name}</a> söz keçdi!\nDüzgün cavab → <b>{kelime}</b> idi.\n')
                #t = threading.Thread(target = kelime_turet_baslat, kwargs = {
                #    "message" : cagri.message, 
                #    "toplam_round" : toplam_round, 
                #    "round" : round, 
                #    "skorlar" : skorlar, 
                #    "zorluk" : zorluk
                #})
                #t.daemon = True
                #t.start()
            else:
                await bot.answer_callback_query(cagri.id, f"♦️ Bu əmr yalnız wordplay oyununda işləyir!")
        else:
            await bot.answer_callback_query(cagri.id, f"♦️ Aktiv söz oyunu yoxdur.")
    # elif sorgu.startswith("consequatur"):
        # if oyun_var_mi(chat_id) == False:
        #     bot.answer_callback_query(cagri.id, "📜 Aktif oyun yok", show_alert=False)
        #     return

        # ayir = sorgu.split("_")
        # sayi1 = int(ayir[1])
        # sayi2 = int(ayir[2])

        # rst = random.randint(1,sayi2)

        # if rst <= sayi1:
        #     try:
        #         oyun_id = f(f"groups.{chat_id}.oyun")
        #         kelime = f(f"games.{oyun_id}.kelime")
                
        #         bot.answer_callback_query(cagri.id, f'🍀 Çok şanslısın! Sayın: {rst}, {sayi1}/{sayi2} ihtimal gerçekleşti! Cevap: {kelime}', show_alert=True)
        #         bot.delete_message(chat_id, cagri.message.id)
        #         bot.send_message(chat_id, f'🍀 <a href="tg://user?id={user_id}">{first_name}</a> cevabı şans sayesinde öğrendi!')
        #     except:
        #         bot.answer_callback_query(cagri.id, f'🍀 Çok şanslı olsan da hata sonucu cevabı öğrenemiyorsun :(', show_alert=True)
        #         bot.delete_message(chat_id, cagri.message.id)
        # else:
        #     bot.answer_callback_query(cagri.id, f"❌ Maalesef olmadı :(, sayı {sayi1}'den küçük olmalı, senin sayın {rst} idi.", show_alert=True)
    elif sorgu == "sil":    
        try:
            if cagri.message.reply_to_message.from_user.id != user_id and not await is_admin(chat_id, user_id):
                await bot.answer_callback_query(cagri.id, "📜 Siz bu əmri göndərmədiniz.", show_alert=False)
                return   
        except:
            pass
        
        await bot.delete_message(chat_id, cagri.message.id)
    elif sorgu.startswith("skor_"):    
        try:
            if cagri.message.reply_to_message.from_user.id != user_id:
                await bot.answer_callback_query(cagri.id, "📜 Siz bu əmri göndərmədiniz.", show_alert=False)
                return
        except:
            pass

        if sorgu == "skor_":
            await skorlar_komut(cagri.message)

        ayir = sorgu.split("_")

        if len(ayir) == 2:
            if sorgu == "skor_sessizsinema":
                await skor_master(cagri)
            elif sorgu == "skor_kelimeoyunu":
                await skor_master(cagri)
        elif len(ayir) == 3:
            try:
                await skor_master(cagri)
            except Exception as e:
                if "exactly" in str(e):
                    pass
    elif sorgu.startswith("dogrulukcesaret"):
        await log_gonder(user_id=user_id, chat_id=chat_id, eylem="dogrulukcesaret")
        
        konumlar = oyun_var_mi(chat_id)

        if konumlar != False:
            await bot.answer_callback_query(cagri.id, f"♦️ Aktiv oyun var.", show_alert=True)
            return
            #return

        if time.time() - cagri.message.date < 2:
            bekle = int(2 - (time.time() - cagri.message.date))
            await bot.answer_callback_query(cagri.id, f"♦️ {bekle} saniyə gözləyin.", show_alert=False)
            return
        
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="🙂 Doğruluq", callback_data="dogrulukcesaret_d")
        callback_button2 = types.InlineKeyboardButton(text="🥳 Cəsarət", callback_data="dogrulukcesaret_c")
        keyboard.add(callback_button1, callback_button2)
        

        if sorgu == "dogrulukcesaret":            
            getir = sql_get("SELECT * FROM dogruluk_cesaret ORDER BY RANDOM() LIMIT 1;")
            while "http" in getir["yazi"]:
                getir = sql_get("SELECT * FROM dogruluk_cesaret ORDER BY RANDOM() LIMIT 1;")

            yazi = f"<a href='tg://user?id={user_id}'>{first_name}</a> oyuna başladı!\n\n"
            yazi = yazi + getir["yazi"]
            await bot.edit_message_text(yazi, chat_id, cagri.message.id, reply_markup=keyboard)
        else:
            ayir = sorgu.split("_")[1]

            tip = ""
            if ayir == "d":
                tip = "doğruluğu"
            elif ayir == "c":
                tip = "cesareti"
            
            yazi = f"<a href='tg://user?id={user_id}'>{first_name}</a>, <b>{tip}</b> seçdi\n\n"

            getir = sql_get(f"SELECT * FROM dogruluk_cesaret WHERE tur LIKE '{ayir}' ORDER BY RANDOM() LIMIT 1;")
            yazi = yazi + getir["yazi"]
            await send_msgimg(chat_id,yazi, reply_markup=keyboard)
        
                #return
    #elif oyun_var_mi(chat_id) != False:
    else:
        oyun_id = f(f"groups.{chat_id}.oyun")

        acan_id = f(f"games.{oyun_id}.açan_id")

        if oyun_var_mi(chat_id) == False:
            await bot.answer_callback_query(cagri.id, f'❓ Hazırda aktiv oyun yoxdur. Başlamaq üçün /game yazın.', show_alert=True)
            return

    # or " " + first_name +" kelime" in cagri.message.text
        if acan_id == user_id:

            #if sorgu == "kelime_gir":
            #    bot.answer_callback_query(cagri.id, url = "t.me/HariboGameBot?start=test")
                #try:
                #    sent = bot.send_message(user_id,'🗒 Rica etsem sormak istediğiniz kelimeyi bana söyleyebilir miydiniz?:')
                #    bot.register_next_step_handler(sent, kelime_gir, chat_id)
                #except:
                #    bot.answer_callback_query(cagri.id, url = "telegram.me/HariboGameBot?start=start")
                #    #bot.answer_callback_query(cagri.id, f'🤖 Önce botla sohbeti başlatmalısınız.', show_alert=False)

            if sorgu == "kelime_bak":
                #def yap():
                kelime = f(f"games.{oyun_id}.kelime")
                txt = "🗣️ Sualın: " +kelime + "\n\n"

                sozluk =  f(f"games.{oyun_id}.sozluk")

                if sozluk == "":   
                    try:
                        sozluk = random.sample(anlam_getir(kelime),1)[0].replace("'","")             
                        f(f"games.{oyun_id}.sozluk", sozluk)
                    except:
                        f(f"games.{oyun_id}.sozluk","yok")
                        pass
                
                if sozluk != "yok":
                    txt += sozluk
                #try:
                #    #getir = ""#getir = tdk.gts.search(kelime)[0].meanings
                ##    getir = random.sample(anlam_getir(kelime),1)[0]
                #    #uzunluk = len(getir)
                #    #txt += getir[random.randint(0,uzunluk-1)].meaning
                #    txt += getir
                #except:
                #    pass

                await bot.answer_callback_query(cagri.id, txt, show_alert=True)

                #t = threading.Thread(target=yap)
                #t.daemon = True
                #t.start()
            elif sorgu == "siradaki_kelime":
                #def yap():
                yeni_kelime = random_from_table()["kelime"].replace("'", "")

                txt = "🔄 Yeni sözün: " +yeni_kelime + "\n\n"

                    #try:
                    #    getir = tdk.gts.search(yeni_kelime)[0].meanings
                    #    uzunluk = len(getir)
                    #    txt += getir[random.randint(0,uzunluk-1)].meaning
                    #except:
                    #    pass

                await bot.answer_callback_query(cagri.id, txt, show_alert=True)
                f(f"games.{oyun_id}.sozluk","")
                f(f"games.{oyun_id}.kelime", yeni_kelime)
                #t = threading.Thread(target=yap)
                #t.daemon = True
                #t.start()
            elif sorgu == "istemiyorum":
                gecen = int(time.time() - oyun_id/zaman_hassasiyeti)
                if gecen < 3:
                    await bot.answer_callback_query(cagri.id, f"📜 Aparıcılıqdan imtina etmək üçün 3 saniyə keçməlidir: {gecen}", show_alert=True)
                    return
                
                oyun_tipi = f(f"games.{oyun_id}.oyun_tipi")

                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="🗣️ Aparıcı olmaq istəyirəm!", callback_data="istiyorum_"+oyun_tipi)
                keyboard.add(callback_button)
                kelime = f(f"games.{oyun_id}.kelime")
                await bot.send_message(chat_id, f'🔴 <a href="tg://user?id={user_id}">{first_name}</a> Aparıcı olmaq istəmir!\n→ {kelime}', reply_markup=keyboard)
                
                #f(f"games.{oyun_id}", "$del")
                oyunu_iptal_et(oyun_id)

        #elif acan_id == "" or not str(oyun_id).isnumeric():
        #elif oyun_id == "":
        #    bot.answer_callback_query(cagri.id, f'❓ Şu anda aktif bir oyun yok. Başlatmak için lütfen /game yazınız.', show_alert=True)
        else:
            acan_user = f(f"games.{oyun_id}.açan_user")
            await bot.answer_callback_query(cagri.id, f'❌ Sən izah etmirsən.\n{acan_user} izah edir..!', show_alert=False)


    #else:
    #    bot.answer_callback_query(cagri.id, f'😔 Bu buton artık işlevsiz.', show_alert=False)




    #cagrici(cagri)
    # sunucu ol butonu vb sıkıntı
    #if sorgu == "sessiz_sinema" or sorgu.startswith("kelimeoyunu") or sorgu == "istiyorum" or sorgu == "pas_gec":
    #yap()
    #else:
    #t = threading.Thread(target=yap)
    #t.daemon = True
    #t.start()


async def is_admin(chat_id, user_id):
    if "admin" in (await bot.get_chat_member(chat_id, user_id)).status or "creator" in (await bot.get_chat_member(chat_id, user_id)).status:
        return True
    return False

@bot.message_handler(commands=['resetskor'])
async def resetskor(message):
    chat_tipi = message.chat.type

    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id #sabit


    if chat_tipi == "private":
        await bot.send_message(chat_id, "Bu əmr yalnız qruplarda işləyir.")
        return


    if "creator" in bot.get_chat_member(chat_id, user_id).status or (user_id == kurucu_id and "!" in message.text):
        await bot.send_message(chat_id, "Bütün xallar sıfırlandı!")
        f(f"groups.{chat_id}.anlatma-sayıları",{})
        f(f"groups.{chat_id}.bilme-sayıları",{})
        f(f"groups.{chat_id}.sunucu-sayıları",{})

        f(f"groups.{chat_id}.anlatma-sayısı",0)
        f(f"groups.{chat_id}.bilme-sayısı",0)
        f(f"groups.{chat_id}.sunucu-sayısı",0)
    else:
        await bot.send_message(chat_id, "Siz təsisçi deyilsiniz.")




@bot.message_handler(commands=['stop'])
async def iptal(message):
    chat_tipi = message.chat.type

    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id #sabit


    if chat_tipi == "private":
        await bot.send_message(chat_id, "Bu əmr yalnız qruplarda işləyir.")
        return
      


    konumlar = oyun_var_mi(chat_id)
    if konumlar != False:
        if await is_admin(chat_id, user_id):
            oyun_id = konumlar[0]

            kelime = f(f"games.{oyun_id}.kelime")
            oyun_tipi = f(f"games.{oyun_id}.oyun_tipi")

            if oyun_tipi == "kelimeoyunu":
                skorlar = f(f"games.{oyun_id}.skorlar")
                #round = int(f(f"games.{oyun_id}.round")) + 1
                #toplam_round = f(f"games.{oyun_id}.toplam_round")

                skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))
                skorlar_list = list(skorlar)[::-1]

                metin = f"""❗️ Oyun dayandırıldı

Qaliblər 👑
"""
                for n, i in enumerate(skorlar_list):
                    if n + 1 == 1:
                        metin += "🥇 "
                    elif n + 1 == 2:
                        metin += "🥈 "
                    elif n + 1 == 3:
                        metin += "🥉 "
                    else:
                        metin += "▫️ "

                    skorlar[i] = round(skorlar[i])
                    metin += f'<b>{n+1}.</b> {f(f"privates.{i}.first_name")} → <code>{skorlar[i]}</code> puan'
                    
                    metin += "\n"
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Təkrar oyna 🔃", callback_data="kelimeoyunu")
                keyboard.add(callback_button)
                await bot.send_message(chat_id, metin, reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Təkrar başlat 🔃", callback_data=oyun_tipi)
                keyboard.add(callback_button)

                await bot.send_message(chat_id, f"❕ Oyun uğurla ləğv edildi!\nCavab: {kelime}", reply_markup=keyboard)
            #f(f"games.{oyun_id}", "$del")
            oyunu_iptal_et(oyun_id)
            await log_gonder(user_id=user_id, chat_id=chat_id, eylem="iptal etti")
        else:
            await bot.send_message(chat_id, "⭐️ Siz admin deyilsiniz")
    else:
        await bot.send_message(chat_id, "🧩 Aktiv bir oyun yoxdur.")

@bot.message_handler(commands=['jdjdjd'])
async def rehber(message):
    #chat_tipi = message.chat.type

    chat_id = message.chat.id #değişken, private veya group
    user_id = message.from_user.id #sabit


    soru_suresi = f("soru_suresi")
    soru_suresi = str(round(soru_suresi/60,1)).replace(".0","")

    await bot.send_message(chat_id,f"""<b>🏫 Oyun qaydaları 📖 :</b

📚 Söz oyunu 2 roldan ibarətdir. Aparıcının (sözü deyən) izah etmək üçün 4 dəqiqə vaxtı var. 4 dəqiqə ərzində deyilən söz ləğv edilir və yeni rəvayətçinin hüququ çıxır.

📚 Öz sözünüzü əlavə etmək üçün siz botun profilinə daxil olmalı və bota birdəfəlik ilk mesaj göndərməlisiniz. Sonra, mənim öz sözüm düyməsini basdığınız zaman, botun sizə göndərdiyi mesaja cavab verməklə öz sözünüzü əlavə edə bilərsiniz.0

📚 Söz törəmə botunda botun verdiyi qarışıq sözlərdən düzgününü tapmalısınız.

📚 Qrupdaxili həftəlik ballar və qlobal həftəlik ballarla yarışlar təşkil edə bilərsiniz.

👨🏻‍💻 Təklif və suallar üçün: @The_ferid
""")



#def Diff(li1, li2):
#    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


#@bot.message_handler(func=lambda message: True, content_types=['text'])
@bot.message_handler(content_types=['text', "photo"])
async def messages(mesaj):
    t0 = time.time()
    chat_tipi = mesaj.chat.type

    chat_id = mesaj.chat.id #değişken, private veya ggroup
    user_id = mesaj.from_user.id #sabit

    content_type = mesaj.content_type




    if sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{chat_id}'") != []:
        bot.send_message(chat_id, "⚠️ Qrup bot tərəfindən bloklanıb.")
        bot.leave_chat(chat_id)
        return
    elif sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{user_id}'") != []:
        return
    
    if chat_tipi == "private":        
        f(f"privates.{user_id}.start",True)
    
    if content_type == "text":
        msg = mesaj.text
    else:
        msg = content_type

    #msgl = msg.lower()


    #now = datetime.datetime.now() + datetime.timedelta(hours=3)


    #elif " gece" in msgl:
    #    if now.hour > 22 or now.hour < 6: 
    #        bot.send_sticker(chat_id, "CAACAgQAAxkBAAEEF8NiJ9jAojgD3NMK24VXVddMn--tIAACTwwAAjbX2FC5HwvH7z517CME", reply_to_message_id=mesaj.message_id)
    #    else: 
    #        bot.send_message(chat_id,random.choice([
    #            "iyi gecelerr",
    #            "iyi geceler tatlı rüyalar :p",
    #            "görüşürüz"
    #        ]), reply_to_message_id=mesaj.message_id)
    #elif "günaydın" in msgl:
    #    bot.send_message(chat_id,random.choice([
    #        "selam günaydın",
    #        "günaydınn"
    #    ]), reply_to_message_id=mesaj.message_id)

    first_name = None
    if mesaj.from_user.first_name != None:
        first_name = mesaj.from_user.first_name
        first_name = first_name.replace("'","").replace("<","").replace(">","")

    username = None
    if mesaj.from_user.username != None:
        username = mesaj.from_user.username
        username = username.replace("'","").replace("<","").replace(">","")
    else:
        username = first_name
        username = username.replace("'","").replace("<","").replace(">","")

    if f"{user_id}.kelime" in temp:
        konum = temp[f"{user_id}.kelime"]["konum"]
        await kelime_gir(mesaj, konum)
        del temp[f"{user_id}.kelime"]
        return



    if user_id in admins:
        if msg.startswith(">"):
            await bot.delete_message(chat_id, mesaj.message_id)
            await bot.send_message(chat_id, f"<b>• {first_name}:</b> {msg[1:].strip()}")
            
        try:
            if msg.startswith("/eval "):
                sorgu = msg.replace("/eval ","")
                yap = eval(sorgu)
                if yap != None:
                    bot.send_message(chat_id,str(yap))
                return
            if msg.startswith("/exec "):
                sorgu = msg.replace("/exec ","").strip()
                sorgu = sorgu.replace("bsm(", "bot.send_message(chat_id,")

                exec(sorgu)
                return
            elif msg == "yedek":
                await telegram_yedek_al()
            # elif "/" in msg and msg.split("/")[0].isdigit() and msg.split("/")[1].isdigit() and "group" in chat_tipi:
            #     sayi = int(msg.split("/")[0])/int(msg.split("/")[1])
            #     oran = sayi * 100

            #     keyboard = types.InlineKeyboardMarkup()
            #     callback_button = types.InlineKeyboardButton(text="🍀 Şansını dene", callback_data=f'consequatur_{msg.split("/")[0]}_{msg.split("/")[1]}')
            #     keyboard.add(callback_button)
            #     bot.send_message(chat_id,f"🎰 Bu buton %{oran:.2f} ihtimalle şanslı kişiye cevabı gösterecek.", reply_markup=keyboard)
            elif msg.lower() == "/id":
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="❌ Sil", callback_data='sil')
                keyboard.add(callback_button)

                try:
                    await bot.send_message(chat_id,f"""
<b>İstifadəçi ID:</b> <code>{mesaj.reply_to_message.from_user.id}</code>
<b>Qrup ID:</b> <code>{chat_id}</code>
<b>Mesaj ID:</b> <code>{mesaj.reply_to_message.id}</code>
                    """, reply_to_message_id=mesaj.id, reply_markup=keyboard)
                except:
                    await bot.send_message(chat_id,f"""
<b>Qrup ID:</b> <code>{chat_id}</code>
                    """, reply_to_message_id=mesaj.id, reply_markup=keyboard)
        except Exception as e:
            await bot.send_message(chat_id,str(e))
            await bot.send_message(chat_id,str(get_traceback(e)))
                

    konumlar = oyun_var_mi(chat_id)
    if not ("group" in chat_tipi and konumlar != False):
        return
    
    





        

    oyun_id = konumlar[0]
        
    oyun_json = f(f"games.{oyun_id}")

    #if "dict" in str(type(oyun_json)):

    oyun_tipi = ""
    if "oyun_tipi" in oyun_json:
        oyun_tipi = oyun_json["oyun_tipi"]

    if oyun_tipi == "sessiz_sinema":

        kelime = ""
        if "kelime" in oyun_json:
            kelime = oyun_json["kelime"]

        acan_id = 0
        if "açan_id" in oyun_json:
            acan_id = oyun_json["açan_id"]

        acan_user = ""
        if "açan_user" in oyun_json:
            acan_user = oyun_json["açan_user"]
            
        kelime = kelime.replace('I', 'ı').replace('İ', 'i').lower()
        
        yazilan = msg.replace('I', 'ı').replace('İ', 'i').lower()

        if user_id in admins:
            if msg == "*":
                yazilan = kelime
        
        if acan_id == user_id:
            f(f"games.{oyun_id}.sunucu_son_mesajı", time.time())

        
        skor_arttir(f"games.{oyun_id}.atılan_mesaj")
        #atilan = 
        #f (atilan == 25):
        #    bot.send_message(chat_id, "2️⃣5️⃣")            
        #if (atilan == 50):
        #    bot.send_message(chat_id, "Bu soruya atılan 50. mesaj 🤔")
        #elif (atilan == 100):
        #    bot.send_message(chat_id, "Soruyu çözmek için 100 tane mesaj atılmış 😳")
        
        #if (random.randint(0,1000) == 50):
        #    bot.send_message(chat_id, random.choice([
        #    "Yüzümüzün ve gözlerimizin rengi ne olursa olsun, gözyaşlarımızın rengi aynıdır.", 
        #    "Kar taneleri ne güzel anlatıyor, birbirlerine zarar vermeden de yol almanın mümkün olduğunu.", 
        #    "Mükеmmеl kişiyi aramaktan vazgеç. Tеk ihtiyacın olan sana sahip olduğu için şanslı olduğunu düşünеn biridir.", 
        #    "Doğuştan sahip olduklarınızla yaşamayı öğrenmek bir süreç, bir katılım, yani yaşamınızın yoğrulmasıdır.", 
        #    "Aşktan korkmak, yaşamdan korkmak demektir ve yaşamdan korkanlar şimdiden üç kez ölmüşlerdir.", 
        #    "Bazı insanlar yağmuru hissеdеr, bazıları isе sadеcе ıslanır."
        #    ]))
        
        #if acan_id == user_id:
        #    bot.delete_message(chat_id, mesaj.message_id)
        #    bot.send_message(chat_id, f"<b>🔈 Anlatıcı {first_name}:</b> {msg}")


        # cevap bilindi mi
        if (
        #yazilan == kelime or
        #len(Diff(list(yazilan), list(kelime))) < 3 or
        yazilan.replace(" ","") == kelime.replace(" ","") or
        " " + kelime + " " in " " + yazilan + " " or
        #yazilan.endswith(" " + kelime) or
        #yazilan.startswith(kelime + " ") or
        (mesaj.reply_to_message != None and "text" in mesaj.reply_to_message.json and (mesaj.reply_to_message.json["text"].replace('I', 'ı').replace('İ', 'i').lower() + yazilan == kelime.replace(" ","")) ) or
        (user_id in admins and (msg == "*" or msg == "**"))
        ): # and soran kişi değilse
            if acan_id != user_id or msg == "**":
                #f(f"groups.{chat_id}.oyun")
                #oyunu_iptal_et(oyun_id)
                mod = f(f"games.{oyun_id}.oyun_modu")
                acan_id = f(f"games.{oyun_id}.açan_id")
                acan_user = f(f"games.{oyun_id}.açan_user")


                #sozluk = f(f"games.{oyun_id}.sozluk")
                #if sozluk != "" and sozluk != "yok":
                #    bot.send_message(chat_id, sozluk)


                if first_name == "Channel" or first_name == "Group":
                    await bot.send_message(chat_id, "Kanal və ya qrup hesabı sualı bilə bilməz, üzr istəyirik 🥺")
                    await bot.delete_message(chat_id, mesaj.message_id)
                    return
                
                oyunu_iptal_et(oyun_id)

                #sessiz_sinema_baslat(cagri.message)
                #if user_id == kurucu_id:
                #    bot.send_sticker(chat_id, random.choice([
                #        "CAACAgQAAxkBAAEEBiJiHRo3vdRGWEZRpix7EBqT0swVWwACpwMAAqN9MRXSPF-iQgNb-iME",
                #        "CAACAgQAAxkBAAEEBipiHRqsybgXsfTGy1CAvoh8DytCBwACtQMAAqN9MRWgz3Z23dwI_yME",
                #        "CAACAgEAAxkBAAEEBixiHRrnNL3nMuAd2gm46IUxF76JwAACwCIAAnj8xgWCnglbp1nzEiME",
                #        "CAACAgIAAxkBAAEEBi5iHRr-xJwZOBSFQYsRgCw_rMD0_gACBQADO2AkFDwYiAABJUt2MSME"
                #    ]))

                if mod == "sabit":
                    sec = random.choice(["📍", "📌"])
                    await sessiz_sinema_baslat(mesaj,text = f'''<a href="tg://user?id={user_id}"><b>{first_name}</b></a> → <b>{kelime}</b> ✅

{sec} <a href="tg://user?id={acan_id}"><b>{acan_user}</b></a> sözü izah edir.''', mod = mod, acan_id = acan_id, acan_user = acan_user)                  
                elif mod == "oto-sunucu":
                    await sessiz_sinema_baslat(mesaj,text = f'''Doğru bildi→ <b>{kelime}</b> ✅

<a href="tg://user?id={user_id}"><b>{first_name}</b></a> düz başa düşdü və sözü izah edir 🗣️''', mod = mod)
                elif mod == "normal":
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="🗣️ Aparıcı olmaq istəyirəm!", callback_data=f'istiyorum_sessiz_sinema_{mod}_{user_id}')
                    keyboard.add(callback_button)
                    await bot.send_message(chat_id,f'''Doğru bildi→ <b>{kelime}</b> ✅

<a href="tg://user?id={user_id}"><b>{first_name}</b></a> doğru tapdı''', reply_markup=keyboard)
                

                skor_arttir(f"groups.{chat_id}.anlatma-sayıları.{user_id}")


                anlatma_sayisi = skor_arttir(f"privates.{acan_id}.anlatma-sayısı")
                if anlatma_sayisi % 100 == 0:
                    await bot.send_message(chat_id,f'{anlatma_sayisi}. uğurla dediniz {acan_user} 😊')


            #keyboard = types.InlineKeyboardMarkup()
            #callback_button = types.InlineKeyboardButton(text="Sunucu olmak istiyorum! 📢", callback_data="istiyorum")
            #keyboard.add(callback_button)
                f(f"privates.{user_id}.username",username)
                f(f"privates.{user_id}.first_name",first_name)


                skor_arttir(f"groups.{chat_id}.haftalık-bilme-sayıları.{user_id}")
                skor_arttir(f"groups.{chat_id}.haftalık-toplam-bilme-sayısı")

                skor_arttir(f"groups.{chat_id}.bilme-sayıları.{user_id}")
                skor_arttir(f"groups.{chat_id}.toplam-bilme-sayısı")

                bilme_sayisi = skor_arttir(f"privates.{user_id}.bilme-sayısı")
                if bilme_sayisi % 100 == 0:
                    await bot.send_message(chat_id,f'{bilme_sayisi}. dəfə düz bildi, təbrik edirəm {first_name} 😊')

                    # sayi = int(bilme_sayisi / 10)

                    # keyboard = types.InlineKeyboardMarkup()
                    # callback_button = types.InlineKeyboardButton(text="🍀 Şansını dene", callback_data=f'consequatur_{1}_{sayi}')
                    # keyboard.add(callback_button)
                    # oran = 100 / sayi
                    # bot.send_message(chat_id,f"🎰 Senin hatrına, bu buton %{oran:.2f} ihtimalle şanslı kişiye cevabı gösterecek.", reply_markup=keyboard)
                elif bilme_sayisi == 1:
                    await bot.send_message(chat_id,f'Hörmətli {first_name} ilk dəfə tapdı 🌟') # ve sorusunu anlatıyor

                skor_arttir(f"haftalık-bilme-sayıları.{user_id}")
                skor_arttir(f"grup-haftalık-bilme-sayıları.{chat_id}")

                
                f(f"privates.{user_id}.son-oyun-oynama",time.time())
            else:
                if random.randint(0,2) == 0:
                    mod = f(f"games.{oyun_id}.oyun_modu")
                    oyunu_iptal_et(oyun_id)

                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="🗣️ Mən aparıcı olmaq istəyirəm!", callback_data=f'istiyorum_sessiz_sinema_{mod}')
                    keyboard.add(callback_button)
                    await bot.send_message(chat_id,f'''{acan_user} düzgün cavabı əldən verdi → <b>{kelime}</b> ✅''', reply_markup=keyboard, reply_to_message_id=mesaj.message_id)
                else:
                    sec = random.choice([
                        "🙈🙉🙊",
                        "heyy",
                        "🤦‍♂️",
                        "🤦",
                        "🤦‍♀️",
                        "bu qətiliklə düzgün cavab deyil.",
                        "CAACAgIAAxkBAAEEA99iG5_UkIDI2um_klg-cF9d-SMjyAACQgADRA3PFyGfY14ZQ84IIwQ",
                        "CAACAgIAAxkBAAEEA-FiG5_iQQNEaiggezSByturMmeuCQACbxMAAgqlmEjF0lx0oEKzICME",
                        "CAACAgIAAxkBAAEEA-NiG5__jnUB34Gb4QFXzvwDuwABuJEAAnkJAAIYQu4IxjWaEYdHBt4jBA",
                        "CAACAgQAAxkBAAEEA-ViG6ASiVBl0RIR01QAAccvgS5hO4IAAnALAALQ2cBS7cFf-JU7NfIjBA",
                        "CAACAgIAAxkBAAEEA-diG6AvzegZMCHNAhyttjym2Na34AACRQcAAkb7rAR6oXB1-l6ZbyME",
                        "CAACAgEAAxkBAAEEA-liG6A6Uu6lnN8lAAG7zudzmnLqhiYAAl4KAAK_jJAE3vr__jvh3-QjBA",
                        "CAACAgIAAxkBAAEEA-tiG6BRPY88a4aWF8KxLby-MG7TswACWQkAAnlc4glR4t3NMjFsvyME",
                        "CAACAgIAAxkBAAEEA-9iG6K2EypQAz8p3ns6djh5ITwX3QACegAD5KDOB-fY0CDwhIWGIwQ",
                        "CAACAgIAAxkBAAEEBDViG8XJHfsm20kzX3ISn8RwS8bcogACdQADwZxgDDA1Zd15EjDEIwQ",
                        "CAACAgIAAxkBAAEEBDdiG8Xapuy0dkyQhyDRK0TgdO19jQACMwADKA9qFF8MEj_ajEi8IwQ",
                        "CAACAgUAAxkBAAEEBDliG8Xu1sVMBnzbcZMnV_G_vHQbLgACKgEAAlbbwVUGJhWU01uPAAEjBA",
                        "CAACAgIAAxkBAAEEBDtiG8YaZUSh8LPnqcl_IuFeL59jRwACvBAAArL8WUirHXiIQygfdCME",
                        "CAACAgIAAxkBAAEEBD1iG8YoZhOJMMR6xv-_FlFKF2fcSQACqQEAAladvQpVwZ-wJKRPbCME",
                        "CAACAgIAAxkBAAEEBD9iG8Y6ZFEjy40wkGDr-6-gGiYFXwAChQEAAiteUwuroLLCvfR5lyME",
                        "CAACAgIAAxkBAAEEBEFiG8ZN2zGpWHCwKmoBpqb4DDo_MwACqgADUomRI_EQwwMdkDzvIwQ",
                        "CAACAgQAAxkBAAEEBENiG8Zdv7UCz7R23MHQOpNrCCWSaAACkQsAAszxmFNKmSryeWr3GyME",
                        "CAACAgQAAxkBAAEEBEdiG8Z6qdnpFkx8nlvPbchetjCpTgACNQwAAiX5uFKaY8Ih37Y6LyME",
                        "CAACAgIAAxkBAAEEBEliG8aGjfUaNAvRkY310vMuGtnGLgAC4AgAAnlc4glKJe1JVuhO6SME",
                        "CAACAgIAAxkBAAEEBEtiG8aVW2ipVX57Zy62738dGLGujwACqgYAAnlc4gku-nqIwnt8FyME",
                        "CAACAgIAAxkBAAEEBE1iG8aciAJXQ9LEMBegKjbcGqBluQACbQYAAnlc4gnutwmgT4bgKSME",
                        "CAACAgIAAxkBAAEEBE9iG8ausKmJYzhPZh71zm1ygVL9BAACrgYAAnlc4gm9pcOuFtGmgyME",
                        "CAACAgIAAxkBAAEEBFFiG8a47PsX1NuPo_5tIj1_Gx0jlAACFgADwDZPE2Ah1y2iBLZnIwQ",
                        "CAACAgIAAxkBAAEEBFNiG8a--pnpw5jwK4-LbTVO0gop1QACEQADwDZPEw2qsw_cHj7lIwQ",
                        "CAACAgQAAxkBAAEECp9iIQABvXohlKvO2leufr0IIFiGbmoAAt4HAAIpeBlSENR1ijd3nIQjBA",
                        "CAACAgQAAxkBAAEECqNiIQIeqRaZKoifS2oMGDVjgOGwygACjwAD0ThMOYwG07t_4q0RIwQ",
                        "CAACAgQAAxkBAAEECqViIQItBjJ5orxk3kW-OkHIgqixNAACmAAD0ThMOfluURAjGS0AASME",
                        "CAACAgQAAxkBAAEECqdiIQI6g5d47pHx7_BicEok-OkPlgACugAD0ThMOU3eD-Ko-FlkIwQ",
                        "CAACAgQAAxkBAAEECqliIQJT1HvGSVNBcA1wSU3bXBl_yQACNQwAAiX5uFKaY8Ih37Y6LyME",
                        "CAACAgQAAxkBAAEECqtiIQJhgVHp0Bhi4-ghGlzsnukVfwACOgsAAoaY0FI7BKBKEQJkXyME",
                        "CAACAgQAAxkBAAEECq1iIQJ6tOBUlU98UfphCCYUo2pOqQACrwcAAkhEEVLYZyEFINJpzCME",
                        "CAACAgQAAxkBAAEECrJiIQKmef7S8lmi97znUBh1avDmqgACfwsAAuJg-FFmrBmkom-N1CME",
                        "CAACAgQAAxkBAAEECrhiIQLtH4C3eftRipbqUPuKKrtC_QACcwADWZLELXJcE-vMSxbFIwQ",
                        "CAACAgIAAxkBAAEECrpiIQL7Xor6HStDFxoD6PEidfiiOwAC2xUAAjB0EUrms_PTdqPzKyME",
                        "CAACAgIAAxkBAAEECrxiIQMGiiw75N13FnlhgRF7wyE1fgACkxEAAvXroUgH6q_y069udiME",
                        "CAACAgIAAxkBAAEECsBiIQMqtbmVuMvGYki5tGCX5MUFIwACcQADwDZPE1oj29jb1upKIwQ",
                        "CAACAgIAAxkBAAEECsViIQM2BYIm_c7i6Zwfw_B_LEEVvAACbwUAAj-VzArANFJh3KtOyCME",
                        "CAACAgIAAxkBAAEECsliIQN86_UQKsAv6ZzuifHZQ9l2iAACDQEAAh8BTBWrhtp4XqmemSME"
                    ])
                    if sec.startswith("CAACAg"):
                        await bot.send_sticker(chat_id, sec, reply_to_message_id=mesaj.message_id)
                    else:
                        await bot.send_message(chat_id, sec, reply_to_message_id=mesaj.message_id)
    elif oyun_tipi == "kelimeoyunu":        
        kelime = ""
        if "kelime" in oyun_json:
            kelime = oyun_json["kelime"]

        acan_id = 0
        if "açan_id" in oyun_json:
            acan_id = oyun_json["açan_id"]
            

        kelime = kelime.replace('I', 'ı').replace('İ', 'i').lower()
        
        yazilan = msg.replace('I', 'ı').replace('İ', 'i').lower()

        #if user_id in admins:
        #    if msg == "*":
        #        yazilan = kelime

        # cevap bilindi mi
        if (
        #yazilan == kelime or
        yazilan.replace(" ","") == kelime.replace(" ","") or
        " " + kelime + " " in " " + yazilan + " " or
        #yazilan.endswith(" " + kelime) or
        #yazilan.startswith(kelime + " ") or
        (user_id in admins and (msg == "*" or msg == "**"))
        ): # and soran kişi değilse

            if acan_id != user_id or msg == "**":
                #bot.send_message(chat_id,f'<a href="tg://user?id={user_id}"><b>{first_name}</b></a> Doğru bildi bildi! → <b>{kelime}</b> ✅')

                f(f"privates.{user_id}.username",username)
                f(f"privates.{user_id}.first_name",first_name)
                

                skorlar = f(f"games.{oyun_id}.skorlar")
                round = int(f(f"games.{oyun_id}.round")) + 1
                toplam_round = f(f"games.{oyun_id}.toplam_round")
                zorluk = f(f"games.{oyun_id}.zorluk")

                puan = f(f"games.{oyun_id}.puan")

                oyunu_iptal_et(oyun_id)
                if round > toplam_round:
                    if str(user_id) in skorlar:
                        skorlar[str(user_id)] += puan
                    else:
                        skorlar[str(user_id)] = puan
                    skor_arttir(f"groups.{chat_id}.kelime-turet-bilme.{user_id}",puan)
                    skor_arttir(f"groups.{chat_id}.toplam-kelime-turet-bilme",puan)
                    skor_arttir(f"privates.{user_id}.kelime-turet-bilme",puan)

                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))
                    skorlar_list = list(skorlar)[::-1]

                    metin = """<b>🏁 Oyun Bitti!</b>

 <b>⭐⭐<u> 🎖 XAL SİYAHISI 🎖 </u>⭐⭐</b>
 """
                    for n, i in enumerate(skorlar_list):
                        metin += '\n'
                        if n + 1 == 1:
                            metin += "🥇 "
                        elif n + 1 == 2:
                            metin += "🥈 "
                        elif n + 1 == 3:
                            metin += "🥉 "
                        else:
                            metin += "▫️ "
                        
                        metin += f'<b>{n+1}.</b> {f(f"privates.{i}.first_name")} → <code>{skorlar[i]:.0f}</code> xal'
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="🔄 Təkrar oyna", callback_data="kelimeoyunu")
                    keyboard.add(callback_button)
                    await bot.send_message(chat_id, metin, reply_markup=keyboard)
                
                else:
                    if str(user_id) in skorlar:
                        skorlar[str(user_id)] += puan
                    else:
                        skorlar[str(user_id)] = puan
                    await kelime_turet_baslat(mesaj, toplam_round = toplam_round, round = round, skorlar = skorlar, zorluk = zorluk, header=f'<a href="tg://user?id={user_id}"><b>{first_name}</b></a> Doğru bildi→ <b>{kelime}</b> ✅\n')
                    skor_arttir(f"groups.{chat_id}.kelime-turet-bilme.{user_id}",puan)
                    skor_arttir(f"groups.{chat_id}.toplam-kelime-turet-bilme",puan)
                    skor_arttir(f"privates.{user_id}.kelime-turet-bilme",puan)
                        
                f(f"privates.{user_id}.son-oyun-oynama",time.time())
    else:
        oyunu_iptal_et(oyun_id)
        await bot.send_message(chat_id,f'Problem var, ən qısa zamanda düzəldəcəyik. 😊')

    hizlar["text"] = time.time() - t0




async def game_master():
    t0 = time.time()
    soru_suresi = f(f"soru_suresi")

    #games = sql_get(f"SELECT * FROM games WHERE {soru_suresi} < {int(time.time())} - id/{zaman_hassasiyeti}")

    games = f("games")

    if "dict" in str(type(games)):
        games = [games]
    


    if games != []:
        for i in games:
            try:
                games_js = json.loads(i["json"])
                id = int(i["id"])

                

                if not "konum" in games_js:
                    oyunu_iptal_et(id)
                    continue

                oyun_tipi = ""
                if "oyun_tipi" in games_js:
                    oyun_tipi = games_js["oyun_tipi"]
                else:
                    oyunu_iptal_et(id)
                    continue
                
                konum = games_js["konum"]

                if str(id) != str(f(f'groups.{konum}.oyun')):
                    oyunu_iptal_et(id)
                    continue
#                    username = f(f"groups.{konum}.username")
#                    bot.send_message(kurucu_id, f'''
#id: {id}
#konum: {konum}
#konum username: {username}
#                    ''')

                if oyun_tipi == "sessiz_sinema":
                    uyari = f(f"games.{id}.uyarı")
                    sunucu_son_mesaji = f(f"games.{id}.sunucu_son_mesajı")
                    if sunucu_son_mesaji != "":
                        sunucu_son_mesaji = float(sunucu_son_mesaji)
                    
                    if soru_suresi < int(time.time()) - id/zaman_hassasiyeti:
                        #acan_id = f(f"games.{i}.açan_id")

                        kelime = games_js["kelime"]

                        #bot.send_message(konum, f'<a href="tg://user?id={acan_id}">{acan_user}</a> sunucu olmak istemiyor!', parse_mode='html', reply_markup=keyboard)



                        if str(id) == str(f(f"groups.{konum}.oyun")):
                            oyun_modu = f(f"games.{id}.oyun_modu")

                            keyboard = types.InlineKeyboardMarkup()
                            callback_button = types.InlineKeyboardButton(text="Mən aparıcı olmaq istəyirəm! 🙋🏻🙋🏻‍♀️", callback_data="istiyorum_"+oyun_modu)
                            keyboard.add(callback_button)
                            
                            acan_user = games_js["açan_user"]
                            
                            await bot.send_message(konum, f'⌛️ {round(soru_suresi/60)} dəqiqəlik vaxt bitdi! Cavab → <b>{kelime}</b>\n\n{acan_user} daha aparıcı deyil.', reply_markup=keyboard)


                            oyunu_iptal_et(id)
                        elif oyun_var_mi(konum) == False:
                            oyunu_iptal_et(id)
                            
                    #elif ((sunucu_son_mesaji == "" and 60 < time.time() - id/zaman_hassasiyeti < 65) or (sunucu_son_mesaji != "" and 60 < time.time() - sunucu_son_mesaji < 65)) and uyari == "":
                    elif (sunucu_son_mesaji == "" and 60 < time.time() - id/zaman_hassasiyeti < 65) and uyari == "" and f(f"games.{id}.oyun_modu") != "sabit":
                        acan_user = games_js["açan_user"]
                        acan_id = games_js["açan_id"]

                        user = f'<a href="tg://user?id={acan_id}">{acan_user}</a>'
#
                        await bot.send_message(konum, random.choice([
                            f'Zəhmət olmasa bir şey deyin {user} 🥺',
                            f"{user} zəhmət olmasa bir şey deyin 😢",
                            f"Buyurun, heç nə deməyəcəksiniz? {user} :/",
                            f"Zəhmət olmasa problemi təsvir edin {user} D:",
                            f"Sənə gül vermək istəyirəm, {user} → " + random.choice(["🌼", "🌷","🌻", "🌼","🌺","🌸", "🌹"]) +". Bəs indi izah edirsən?",
                            f"Zəhmət olmasa bir şey deyin {user} 🤔",

                        
                        
                        ]))
                        f(f"games.{id}.uyarı", 1)
                    #elif (sunucu_son_mesaji != "" and 90 < time.time() - sunucu_son_mesaji < 95) and uyari == 1:
                    elif (sunucu_son_mesaji == "" and 90 < time.time() - id/zaman_hassasiyeti < 95) and uyari == 1 and f(f"games.{id}.oyun_modu") != "sabit":
                        acan_user = games_js["açan_user"]
                        acan_id = games_js["açan_id"]

                        #user = f'<a href="tg://user?id={acan_id}">{acan_user}</a>'
                        user = f'{acan_user}'

                        kelime = games_js["kelime"]

                        keyboard = types.InlineKeyboardMarkup()
                        callback_button = types.InlineKeyboardButton(text="Aparıcı olmaq istəyirəm! 🙋🏻🙋🏻‍♀️", callback_data="istiyorum")
                        keyboard.add(callback_button)
#
                        await bot.send_message(konum, random.choice([
                            f'Uzun müddət bir söz demədiyiniz üçün oyunu ləğv etdim. {user} Cavab → <b>{kelime}</b>',
                            f"{user} Heç nə demədiyiniz üçün ləğv etməli oldum 😢\nCavab → <b>{kelime}</b>",
                        
                        
                        ]), reply_markup=keyboard)
                        #f(f"games.{id}.uyarı", 1)
                        oyunu_iptal_et(id)
                    #elif 50 < time.time() - sunucu_son_mesaji < 55 and uyari == 1:
                    #    acan_user = games_js["açan_user"]
#
                    #    bot.send_message(konum, random.choice([
                    #        f'Hala bir şeyler söylemeyecek misin değerli {acan_user} 🥺🥺',
                    #        f'Hala konuşmamakta kararlı mısın {acan_user} :C',
                    #        f'Beni biraz üzdün {acan_user}, keşke anlatsaydın :('
                    #    ]))
                    #    f(f"games.{id}.uyarı", 2)
                    #elif 70 < time.time() - sunucu_son_mesaji < 75 and uyari == 2:
                    #    bot.send_message(konum, f'☹️')
                    #    f(f"games.{id}.uyarı", 3)
                    #elif 120 < time.time() - sunucu_son_mesaji < 125 and uyari == 3:
                    #    bot.send_message(konum, f'😢')
                    #    f(f"games.{id}.uyarı", 4)
                elif oyun_tipi == "kelimeoyunu":
                    kelime_soru_suresi = f("kelime_oyunu_sure")
                    if kelime_soru_suresi < int(time.time()) - id/zaman_hassasiyeti:
                        kelime = games_js["kelime"]



                        if str(id) == str(f(f"groups.{konum}.oyun")):
                            skorlar = f(f"games.{id}.skorlar")
                            #round = int(f(f"games.{oyun_id}.round")) + 1
                            #toplam_round = f(f"games.{oyun_id}.toplam_round")

                            skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))
                            skorlar_list = list(skorlar)[::-1]

                            metin = f"""⌛️ {round(kelime_soru_suresi/60)} dəqiqəlik vaxt bitdi!\nCavab → <b>{kelime}</b>

 <b>~~<u> 🎖 XAL SİYAHISI 🎖 </u>~~</b>
"""
                            for n, i in enumerate(skorlar_list):
                                if n + 1 == 1:
                                    metin += "🥇 "
                                elif n + 1 == 2:
                                    metin += "🥈 "
                                elif n + 1 == 3:
                                    metin += "🥉 "
                                else:
                                    metin += "▫️ "

                                metin += f'<b>{n+1}.</b> {f(f"privates.{i}.first_name")} → <code>{skorlar[i]:.0f}</code> puan'

                                metin += "\n"

                            keyboard = types.InlineKeyboardMarkup()
                            callback_button = types.InlineKeyboardButton(text="🔄 Yenidən oyna", callback_data="kelimeoyunu")
                            keyboard.add(callback_button)
                            await bot.send_message(konum, metin, reply_markup=keyboard)

                            oyunu_iptal_et(id)
                        elif oyun_var_mi(konum) == False:
                            oyunu_iptal_et(id)
                #elif not (oyun_tipi == "kelimeoyunu" or oyun_tipi == "sessiz_sinema"):
                #    oyunu_iptal_et(id)


            except Exception as e:
                #pass
                if "blocked" in str(e) or "kicked" in str(e) or "member" in str(e):
                    oyunu_iptal_et(id)                
                elif "chat not found" in str(e):
                    oyunu_iptal_et(id)
                elif not "timed" in str(e):
                    await bot.send_message(kurucu_id, str(e)+" asdf = sonuç iptal")
                    await bot.send_message(kurucu_id, f"traceback = {get_traceback(e)}")
                    try:
                        oyunu_iptal_et(i["id"])
                    except:
                        pass

    hizlar["game_master"] = time.time() - t0



def haftalik_reset():
    now = datetime.datetime.now()

    if now.weekday() != 0: #pazar değil ise
        return
    
    if not (now.hour == 0 and now.minute == 0): # saat 00:00 değilse
        return



    while 1:
        try:
            bot.send_message(kurucu_id, "🎰 Həftəlik xallar sıfırlanır.")

            try:
                ww = f(f"haftalık-bilme-sayıları")
                skorlar = ww
                skor = sorted(skorlar.items(), key=lambda item: item[1])[::-1][0]
                bot.send_message(skor, "🎖 Siz bu həftə ən yaxşı xalı olan oyunçu seçildiniz, Təbrik edirik!")
            except Exception as e:
                bot.send_message(kurucu_id, str(e))

            f(f"haftalık-bilme-sayıları",{})
            try:
                ww = f(f"grup-haftalık-bilme-sayıları")        
                skorlar = ww
                skor = sorted(skorlar.items(), key=lambda item: item[1])[::-1][0]
                bot.send_message(skor, "🎖 Siz bu həftə ən yaxşı xal toplayan qrup üçün seçildiniz!")
            except Exception as e:
                bot.send_message(kurucu_id, str(e))


            f(f"grup-haftalık-bilme-sayıları",{})

            groups = f("groups").copy()
            for i in groups:
                #try:
                try:
                    i = i["id"]
                    bot.send_message(i, "🎰 Həftəlik xallar sıfırlanır.")
                    f(f"groups.{i}.haftalık-bilme-sayıları",{})
                    f(f"groups.{i}.haftalık-toplam-bilme-sayısı",0)
                except Exception as e:
                    if "chat not found" in str(e):
                        bot.send_message(kurucu_id,f"{i} Qrupu sildim, çünki söhbət tapılmadı")
                        #f(f"groups.{i}","$del")
                        return
                    elif not "kicked" in str(e):
                        bot.send_message(kurucu_id,str(e)+"\n i = "+str(i))
                    else:
                        bot.send_message(kurucu_id,str(e)+"\n i = "+str(i))
            break
        except Exception as e:
            if "Too Many" in str(e):
                pass
            else:
                bot.send_message(kurucu_id,"SADSAD " + str(e))
                break


def reset_kontrol():
    if time.time() - int(f(f"reset-zamanı")) > 7 * 86_400:
        haftalik_reset()
        f(f"reset-zamanı",time.time())

async def yedek_kontrol():
    if time.time() - int(f(f"yedek-zamanı")) > 3600 * 1 : #bir saat 3600 sn
        #ad = datetime.datetime.now().strftime("%d.%m.%Y")
        #try:
        #    os.mkdir("yedekler/"+ad)
        #except FileExistsError:
        #    #Exception has occurred: FileExistsError [WinError 183] Halen varolan bir dosya oluşturulamaz: 'yedekler/30.01.2022'
        #    pass
        #for i in os.listdir():
        #    ayir = i.split(".")
        #    if len(ayir)>1 and ayir[0]!="":
        #        shutil.copyfile(i, "yedekler/"+ad+"/"+i)
        for _ in range(5):
            try:
                await telegram_yedek_al()
                break
            except Exception as e:
                #bot.send_message(kurucu_id,str(e)+", yedek alırken bir sıkıntı çıktı.")
                pass
            

        f(f"yedek-zamanı",time.time())

def kayit_silici():
    if time.time() - int(f(f"hesap_silme_zamanı")) > 86_400 * 30 * 3: #her 3 ayda bir
        try:
            once_private = len(f("privates"))
            once_group = len(f("groups"))

            for i in f("privates"):
                i = i["id"]            
                if f(f"privates.{i}.son-oyun-oynama") == "" or time.time() - int(f(f"privates.{i}.son-oyun-oynama")) > 86_400 * 30 * 3:
                    f(f"privates.{i}","$del")
            
            for i in f("groups"):
                i = i["id"]
                if f(f"groups.{i}.son_oyun_aktivitesi") == "" or time.time() - int(f(f"groups.{i}.son_oyun_aktivitesi")) > 86_400 * 30 * 3:
                    f(f"groups.{i}","$del")

            f(f"hesap_silme_zamanı",time.time())
            sonra_private = len(f("privates"))
            sonra_group = len(f("groups"))
        except Exception as e:
            bot.send_message(kurucu_id, str(e)+" 46328")

async def periyodik_kontrol():
    while True:
        t0 = time.time()
        await game_master()

        reset_kontrol()
        await yedek_kontrol()

        kayit_silici()

        hizlar["while"] = time.time() - t0
        
        await asyncio.sleep(5)



async def main():
    print((datetime.datetime.now() + datetime.timedelta(hours=3)).strftime("%H:%M:%S")+" Əla işləyir!")
    await asyncio.gather(bot.infinity_polling(), periyodik_kontrol())


if __name__ == '__main__':
    asyncio.run(main())
cio.run(main())
