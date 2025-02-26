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
    await bot.send_message(kurucu_id,"Yedek alÄ±nÄ±yor...", disable_notification=True)
    for i in os.listdir():
        if "." in i:
            await bot.send_document(kurucu_id,open(i, 'rb'), disable_notification=True)
    await bot.send_message(kurucu_id,"Yedek alÄ±ndÄ±.", disable_notification=True)

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
    txt = "\n".join([f"{i} â†’ {hizlar[i]}" for i in hizlar])
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
        kelime = kelime.replace('I', 'Ä±').replace('Ä°', 'i').replace('\'', '').lower().strip()
        try:
            sql_execute("INSERT INTO " + tablo + " (kelime) VALUES ('"+kelime+"');")
        except Exception as e:
            if not "UNIQUE" in str(e):
                print("ahhh",e,kelime)
    sec = len(sql_get("SELECT * FROM '"+tablo+"';"))
    return str(frst) + " âŸ¶ " + str(sec) + f" = {sec-frst}"

def read_file(where):
    with open(where, encoding="UTF8") as f:
        return [i.strip() for i in f.readlines()]

def random_from_table(tablo = "kelimeler"):
    return sql_get("SELECT * FROM " + tablo + " ORDER BY RANDOM() LIMIT 1;")


def f(path, process="$read", **kwargs):
    """veritabanÄ± yardÄ±mcÄ±sÄ±
a.b.c.d ÅŸeklinde yazÄ±lÄ±r ve her birisi bir daldÄ±r.
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
<b> ~~ ðŸ“¢ Log ~~</b>

ðŸ’¬: <code>{f(f"groups.{chat_id}.username")}</code>
ðŸ†”: <code>{kwargs.get('user_id','')}</code>
Qrup ðŸ†”: <code>{chat_id}</code>
FÉ™aliyyÉ™t: <code>{kwargs.get('eylem','')}</code>

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

    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id #sabit    

    msg = message.text



    if chat_tipi == "private":
        ayrik = msg.split(" ")
        if len(ayrik) == 2:
            acan_id = f(f"games.{ayrik[1]}.aÃ§an_id") 
            if acan_id == "":
                await bot.send_message(user_id,'Ãœzr istÉ™yirik, bu oyunun vaxtÄ± bitib .')
                return


            if acan_id == user_id:
                konum = f(f"games.{ayrik[1]}.konum")
                sent = await bot.send_message(user_id,'ðŸ—’ ZÉ™hmÉ™t olmasa soruÅŸmaq istÉ™diyiniz sÃ¶zÃ¼ deyÉ™ bilÉ™rsinizmi?:')
                #bot.register_next_step_handler(sent, kelime_gir, konum)

                temp[f"{user_id}.kelime"] = {}
                temp[f"{user_id}.kelime"]["konum"] = konum
            else:
                await bot.send_message(user_id,'Bu oyunu siz aÃ§mamÄ±sÄ±nÄ±z ðŸš«')
        else:
            f(f"privates.{user_id}.start",True)
            keyboard = types.InlineKeyboardMarkup()

            callback_button = types.InlineKeyboardButton(text="ðŸ‡¦ðŸ‡¿Qrupa ÆlavÉ™ EtðŸ‡¦ðŸ‡¿", url="https://t.me/CrocodileGame_Robot?startgroup=a")
            callback_button2 = types.InlineKeyboardButton(text="ðŸ§¬DigÉ™r botlarðŸ§¬", url="https://t.me/NeonGroupResmi")
            callback_button3 = types.InlineKeyboardButton(text="ðŸ«‚TanÄ±ÅŸlÄ±q botu", url="https://t.me/tanisliqbot?start=r815485") 
            keyboard.add(callback_button)
            keyboard.add(callback_button2)
            keyboard.add(callback_button3)
            await bot.send_message(chat_id, f'<b>âœ‹ðŸ» Salam, mÉ™n Crocodile Lite oyun botuyam ðŸŠ\n\nðŸŽ¯ MÃ¼xtÉ™lif oyunlar oynamaq vÉ™ É™ylÉ™nmÉ™k Ã¼Ã§Ã¼n mÉ™nimlÉ™ oynaya bilÉ™rsiniz.\n\nâš™ï¸ MÉ™ni qrupa É™lavÉ™ edin vÉ™ mÉ™nimlÉ™ oynamaq Ã¼Ã§Ã¼n mÉ™ni qrupda Admin et.</b >',  reply_markup=keyboard)



async def sessiz_sinema_baslat(message, **kwargs): 
    t0 = time.time()
    chat_tipi = message.chat.type

    oyun_modu = kwargs.get("mod", "oto-sunucu") # oto-sunucu, sabit, normal

    if chat_tipi == "private":
        await bot.send_message(message.chat.id, "Bu É™mr yalnÄ±z qrup Ã¼Ã§Ã¼n istifadÉ™ edilÉ™ bilÉ™r.")
        return

    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
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
        await bot.send_message(kurucu_id, f'Bu 456456 istifadÉ™ olunur')
        await bot.send_message(chat_id, f'âŒ HÃ¶rmÉ™tli <a href="tg://user?id={user_id}">{first_name}</a>,HazÄ±rda aktiv oyunlar var. ')
        return


    text = kwargs.get("text", f'<a href="tg://user?id={user_id}">{first_name}</a> ðŸ—£ï¸ sÃ¶zÃ¼nÃ¼ tÉ™qdim edir')


    try:
        dict_name = f(f"groups.{chat_id}.bilme-sayÄ±larÄ±")
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
                    ayir[a] = "ðŸ‘‘ " + ayir[a]
            text = "\n".join(ayir)
            #text += f'\n\nðŸ‘‘ Bu kiÅŸi bu grubun birincisi ðŸ‘‘'
        elif ikinci == suser_id:
            ayir = text.split("\n")
            for a in range(len(ayir)):
                if first_name in ayir[a]:
                    ayir[a] = "ðŸ¥ˆ " + ayir[a]
            text = "\n".join(ayir)
            #text += f'\n\nðŸ¥ˆ Bu kiÅŸi bu grubun ikincisi ðŸ¥ˆ'
        elif ucuncu == suser_id:
            ayir = text.split("\n")
            for a in range(len(ayir)):
                if first_name in ayir[a]:
                    ayir[a] = "ðŸ¥‰ " + ayir[a]
            text = "\n".join(ayir)
            #text += f'\n\nðŸ¥‰ Bu kiÅŸi bu grubun ikincisi ðŸ¥‰'
        elif dorduncu == suser_id or besinci == suser_id:
            ayir = text.split("\n")
            for a in range(len(ayir)):
                if first_name in ayir[a]:
                    ayir[a] = "ðŸ‘‘ " + ayir[a]
            text = "\n".join(ayir)

            
    except Exception as e:
        # eÄŸer ilk 5te kimse yoksa hata
        pass
        #bot.send_message(kurucu_id, str(e))
    
        
    if user_id in admins and user_id != 5898049921 and user_id != 5898049921:
        ayir = text.split("\n")
        for a in range(len(ayir)):
            if first_name in ayir[a]:
                ayir[a] = "â€¢ " + ayir[a] # + " ðŸ”¥"
        text = "\n".join(ayir)
    elif user_id==6276057244 or user_id==6276057244:
        ayir = text.split("\n")
        for a in range(len(ayir)):
            if first_name in ayir[a]:
                ayir[a] = "ðŸ… " + ayir[a] # + " ðŸ”¥"
        text = "\n".join(ayir)
    
    incele_emoji = random.choice(["ðŸ”¬","ðŸ”­","ðŸ‘","ðŸ‘€","ðŸ”","ðŸ”Ž"])
    soru_yaz_emoji = random.choice(["âœï¸", "ðŸ“", "âœï¸", "ðŸ—¯"])
    istemiyorum_emoji = random.choice(["âœ–ï¸", "âŒ", "âŽ", "ðŸš«", "ðŸ™…"])
    gec_emoji = random.choice(["âž¡ï¸", "â™»ï¸", "ðŸ‘‰"])
    
    oyun_id = int(time.time() * zaman_hassasiyeti)

    callback_button3 = types.InlineKeyboardButton(text="SÃ¶zÉ™ baxÄ±n ðŸ‘€", callback_data="kelime_bak")
    callback_button2 = types.InlineKeyboardButton(text="SÃ¶zÃ¼ keÃ§in â™»ï¸", callback_data="siradaki_kelime")
    #callback_button = types.InlineKeyboardButton(text="Kelime Yaz âœï¸", callback_data="kelime_gir")
    callback_button = types.InlineKeyboardButton(text="Ã–z sÃ¶zÃ¼m ðŸ“", url=f"https://t.me/CrocodileGame_Robot?start={oyun_id}")


    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(callback_button2)
    keyboard.add(callback_button, callback_button3)
    if oyun_modu != "sabit":
        callback_button4 = types.InlineKeyboardButton(text="AparÄ±cÄ± olmaq istÉ™mirÉ™m â›”", callback_data="istemiyorum")
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
                "aÃ§an_id":user_id,
                "aÃ§an_user":first_name,
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
            skor_arttir(f"privates.{user_id}.sunucu-sayÄ±sÄ±")

            skor_arttir(f"groups.{chat_id}.toplam-sunucu-sayÄ±sÄ±") 
            skor_arttir(f"groups.{chat_id}.sunucu-sayÄ±larÄ±.{user_id}")



            

            await log_gonder(user_id=user_id, chat_id=chat_id, eylem="sessiz sinema baÅŸlattÄ±", game_id=oyun_id)

            return rastgele_kelime
        except Exception as e:
            if "Too Many" in str(e):
                #bot.send_message(chat_id, "âŒ Siz Ã§ok hÄ±zlÄ± oynuyorsunuz deÄŸerli oyuncular! Bu da bir hataya yol aÃ§tÄ±.")
                #pass
                if hata_msg == None:                        
                    hata_msg = bot.send_message(chat_id, "âŒ›ï¸ Æziz oyunÃ§ular, sizi Ã§ox az gÃ¶zlÉ™tÉ™cÉ™yÉ™m.").id
                time.sleep(1)
            else:
                await bot.send_message(chat_id, "âŒ XÉ™ta baÅŸ verdi. ZÉ™hmÉ™t olmasa bir daha cÉ™hd edin.")
                await bot.send_message(kurucu_id, str(e))
                await bot.send_message(kurucu_id, get_traceback(e))
                break



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
        bot.send_message(kurucu_id, f'bu asdasd istifadÉ™ olunur')
        bot.send_message(chat_id, f'âŒ HÃ¶rmÉ™tli <a href="tg://user?id={user_id}">{first_name}</a>, Hal-hazÄ±rda aktiv oyun var')
        return

    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="NÃ¶vbÉ™tiyÉ™ keÃ§ ðŸ§©", callback_data="pas_gec")
    callback_button2 = types.InlineKeyboardButton(text="Ä°pucu ðŸ”Ž", callback_data="ipucu_kelime")
   
    keyboard.add(callback_button1, callback_button2) #, callback_button3

    zorluk = kwargs.get("zorluk", "kolay")

    rastgele_kelime = ""
    #anlam_getir = ""
    if zorluk == "kolay":
        rastgele_sec = random_from_table(tablo = "kelime_turetme_kelimeler")
        rastgele_kelime = rastgele_sec["kelime"]

        
    elif zorluk == "zor":
        connection = sqlite3.connect("tdk_kelimeler.db")

        connection.row_factory = dict_factory

        crsr = connection.cursor()
        crsr.execute("SELECT * FROM kelimeler ORDER BY RANDOM() LIMIT 1;")
        ans = crsr.fetchall()

        rastgele_kelime = ans[0]["kelime"]

        
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



    while ''.join(tum_harfler) == rastgele_kelime:
        random.shuffle(tum_harfler)

    harfler = ' '.join(tum_harfler)

    shuffled = ' '.join(shuffled)

    js = {}
    

    katsayi = 0.1
    if zorluk == "zor":
        katsayi = 0.4
    puan = harf_sayisi * katsayi

    round_sayisi = kwargs.get("round",1)
    toplam_round = kwargs.get("toplam_round",30)


    text = kwargs.get("text",f"""
ðŸ’° VerilÉ™cÉ™k xal: <b>{puan:.1f}</b>
ðŸŽ¯ Raund: <b>{round_sayisi}/{toplam_round}</b>
ðŸ§© {harf_sayisi} hÉ™rf: <code>{harfler}</code>
ðŸŽ² Ä°pucu: <code>{shuffled}</code>
""")

    text = kwargs.get("header","") + text


        

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
            await log_gonder(user_id=user_id, chat_id=chat_id, eylem="sÃ¶z tÃ¶rÉ™mÉ™si baÅŸladÄ±", game_id = oyun_id)

            return rastgele_kelime
        except Exception as e:
            if "Too Many" in str(e):

                if hata_msg == None:
                    hata_msg = bot.send_message(chat_id, "âŒ›ï¸ Æziz oyunÃ§ular, sizi Ã§ox az gÃ¶zlÉ™tÉ™cÉ™yÉ™m.").id
                time.sleep(1)
            else:
                bot.send_message(chat_id, "âŒ XÉ™ta baÅŸ verdi. ZÉ™hmÉ™t olmasa bir daha cÉ™hd edin.")
                bot.send_message(kurucu_id, str(e))
                bot.send_message(kurucu_id, get_traceback(e))
                break   

@bot.message_handler(commands=['oban'])
def oban(message):
    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id

    if not user_id in admins:
        return
    

    msg = message.text

    ayrik = msg.split()
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
    keyboard.add(callback_button1)

    if len(ayrik) == 1:
        try:
            alintilanan_user_id = message.reply_to_message.from_user.id
            
            banli_mi = sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{alintilanan_user_id}'") != []

            if banli_mi:            
                sql_execute(f'DELETE FROM ban_listesi WHERE id="{alintilanan_user_id}"') 
                bot.send_message(chat_id, f"âœ… {message.reply_to_message.from_user.first_name} ({alintilanan_user_id}) artÄ±k yasaksÄ±z", reply_markup=keyboard, reply_to_message_id=message.id)
            else:
                sql_execute(f"INSERT INTO ban_listesi (id) VALUES ('{alintilanan_user_id}')") 
                bot.send_message(chat_id, f"ðŸ—¡ {message.reply_to_message.from_user.first_name} ({alintilanan_user_id}) artÄ±k yasaklÄ±", reply_markup=keyboard, reply_to_message_id=message.id)
                try:
                    if alintilanan_user_id == chat_id:
                        bot.send_message(chat_id, "âš ï¸ Grup bot tarafÄ±ndan engellenmiÅŸtir.")
                        bot.leave_chat(chat_id)
                except Exception as e:
                    print("sadsadsad",e,chat_id)
        except:
            bot.send_message(chat_id,f"""
HeÃ§ bir adam sitat gÉ™tirmÉ™yib!
            """, reply_to_message_id=message.id, reply_markup=keyboard)

    elif len(ayrik) == 2:
        banli_mi = sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{ayrik[1]}'") != []

        if banli_mi:            
            sql_execute(f'DELETE FROM ban_listesi WHERE id="{ayrik[1]}"') 
            bot.send_message(chat_id, f"âœ… {ayrik[1]} artÄ±q qadaÄŸan deyil", reply_markup=keyboard, reply_to_message_id=message.id)
        else:
            sql_execute(f"INSERT INTO ban_listesi (id) VALUES ('{ayrik[1]}')") 
            bot.send_message(chat_id, f"ðŸ—¡ {ayrik[1]} indi qadaÄŸandÄ±r", reply_markup=keyboard, reply_to_message_id=message.id)
            try:
                if alintilanan_user_id == chat_id:
                    bot.send_message(chat_id, "âš ï¸ Qrup bot tÉ™rÉ™findÉ™n bloklanÄ±b.")
                    bot.leave_chat(chat_id)
            except Exception as e:
                print("sadsadsad",e,chat_id)
                pass
    elif len(ayrik) == 3:
        bot.send_message(chat_id, f"ZÉ™hmÉ™t olmasa É™mri belÉ™ daxil edin: /oban {ayrik[2]}", reply_markup=keyboard, reply_to_message_id=message.id)

@bot.message_handler(commands=['games'])
async def games(message):
    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
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
            {f(f"games.{i}.kelime")} - {f(f"games.{i}.aÃ§an_user")}

        """


    if txt == "":
        txt = "HeÃ§ bir oyun yoxdur"

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


    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id #sabit    
    
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="ðŸŽ¯ DoÄŸruluq", callback_data="dogrulukcesaret_d")
    callback_button2 = types.InlineKeyboardButton(text="ðŸŒŸ CÉ™sarÉ™t", callback_data="dogrulukcesaret_c")
    keyboard.add(callback_button1, callback_button2)
    
    yazi = f"<a href='tg://user?id={user_id}'>{first_name}</a> <b>cÉ™sarÉ™ti</b> seÃ§di\n\n"

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

   
    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id #sabit    
    
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="ðŸ™‚ DoÄŸruluq", callback_data="dogrulukcesaret_d")
    callback_button2 = types.InlineKeyboardButton(text="ðŸ¥³ CÉ™sarÉ™t ", callback_data="dogrulukcesaret_c")
    keyboard.add(callback_button1, callback_button2)
    
    yazi = f"<a href='tg://user?id={user_id}'>{first_name}</a> <b>doÄŸruluÄŸu</b> seÃ§di\n\n"

    getir = sql_get(f"SELECT * FROM dogruluk_cesaret WHERE tur LIKE 'd' ORDER BY RANDOM() LIMIT 1;")
    yazi = yazi + getir["yazi"]
    await send_msgimg(chat_id,yazi)

@bot.message_handler(commands=['reytinq'])
async def skorlar_komut(message):    #chat_tipi = message.chat.type
    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id


    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="âœï¸ SÃ¶z oyunu", callback_data="skor_sessizsinema")
    callback_button2 = types.InlineKeyboardButton(text="ðŸ§© BoÅŸ xana", callback_data="skor_kelimeoyunu")
    keyboard.add(callback_button1)
    keyboard.add(callback_button2)
    yazi = f"ðŸ“œ HansÄ± oyunun xallarÉ™nÉ™ gÃ¶rmÉ™k istÉ™rdiniz?"
    try:
        id = message.id
        await bot.edit_message_text(chat_id=chat_id, message_id=id, text=yazi, reply_markup=keyboard)
    except:
        await bot.send_message(chat_id, yazi, reply_to_message_id=message.id, reply_markup=keyboard)

@bot.message_handler(commands=['game'])
async def baslat(message):
    chat_tipi = message.chat.type

    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id #sabit    


    if sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{chat_id}'") != []:
        await bot.send_message(chat_id, "âš ï¸ Qrup bot tÉ™rÉ™findÉ™n bloklanÄ±b.")
        await bot.leave_chat(chat_id)
        return
    elif sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{user_id}'") != []:
        return
       
    konumlar = oyun_var_mi(chat_id) #oyun_konum grup_konum
    if chat_tipi == "private":
        await bot.send_message(message.chat.id, "Bu É™mr yalnÄ±z qrup Ã¼Ã§Ã¼n istifadÉ™ edilÉ™ bilÉ™r.")
        return
    if konumlar != False:
        await bot.send_message(message.chat.id, "ðŸŽ¯ Oyun artÄ±q baÅŸlayÄ±b.\nDayandÄ±rmaq Ã¼Ã§Ã¼n /stop")
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
    callback_button1 = types.InlineKeyboardButton(text="ðŸŠ SÃ¶z oyunu", callback_data="sessiz_sinema")
    callback_button2 = types.InlineKeyboardButton(text="ðŸ§© BoÅŸ xana", callback_data="kelimeoyunu")
    callback_button3 = types.InlineKeyboardButton(text="ðŸ”ž DoÄŸruluq yoxsa CÉ™sarÉ™t", callback_data="dogrulukcesaret")
    keyboard.add(callback_button1)
    keyboard.add(callback_button2)
    keyboard.add(callback_button3)
    await bot.send_message(chat_id, f"ðŸ“œ ZÉ™hmÉ™t olmasa oyun nÃ¶vÃ¼ seÃ§in.", reply_markup=keyboard)

#@bot.message_handler(state=MyStates.kelime)
async def kelime_gir(message, grup_id): #grup_id    
    user_id = message.from_user.id #sabit
    chat_id = grup_id

    oyun_id = f(f"groups.{chat_id}.oyun")

    if f(f"games.{oyun_id}.aÃ§an_id") == user_id:
        yeni_kelime = message.text[:500]

        await bot.send_message(user_id,"ðŸ‘ Ä°ndi yeni sual: "+yeni_kelime) #, reply_markup=keyboard
        f(f"games.{oyun_id}.kelime", yeni_kelime)

        with open('girilen_kelimeler.txt', 'a') as myfile:
            myfile.write(yeni_kelime+"\n")


async def is_subscribed(chat_id, user_id):
    try:
        get = await bot.get_chat_member(chat_id, user_id) #gruba hiÃ§ girmemiÅŸse

        if get.status == "left": #gruptan Ã§Ä±kmÄ±ÅŸsa
            return False
        return True
    except ApiTelegramException as e:
        if e.result_json['description'] == 'SÉ™hv sorÄŸu: istifadÉ™Ã§i tapÄ±lmadÄ±':
            return False


async def skor_master(cagri):    
    max_skor = 20

    sorgu = cagri.data
    chat_id = str(cagri.message.json["chat"]["id"]) #deÄŸiÅŸken
    user_id = cagri.from_user.id #sabit        
   
    keyboard = types.InlineKeyboardMarkup()

    
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
            callback_button1 = types.InlineKeyboardButton(text="Qlobal puan ðŸŒ", callback_data="skor_sessizsinema_kureselskor")
            callback_button2 = types.InlineKeyboardButton(text="MÉ™nim puam ðŸ“Š", callback_data="skor_sessizsinema_skorum")
            callback_button3 = types.InlineKeyboardButton(text="Qrup puan ðŸ’¬", callback_data="skor_sessizsinema_skor")           
            geri_don_btn = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data='skor_')
            keyboard.add(callback_button2, callback_button1)
            keyboard.add(callback_button3)
            keyboard.add(geri_don_btn)

            await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="ðŸ”¸ HansÄ± puanlarÄ± gÃ¶rmÉ™k istÉ™rdiniz?", reply_markup=keyboard)
        elif ne_skoru == "kelimeoyunu":
            callback_button1 = types.InlineKeyboardButton(text="Qlobal puan ðŸŒ", callback_data="skor_kelimeoyunu_kureselskor")
            callback_button3 = types.InlineKeyboardButton(text="Qrup puan ðŸ’¬", callback_data="skor_kelimeoyunu_skor")
            geri_don_btn = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data='skor_')
            keyboard.add(callback_button1, callback_button3)
            keyboard.add(geri_don_btn)

            await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="ðŸ”¸ HansÄ± puanlarÄ± gÃ¶rmÉ™k istÉ™rdiniz?", reply_markup=keyboard)
        else:
            await bot.answer_callback_query(cagri.id, text="ðŸ˜ž")
    else:
        tip = ayir[2]

        if ne_skoru == "sessizsinema":
            if tip == "skor":
                skorlar = f(f"groups.{chat_id}.bilme-sayÄ±larÄ±")

                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)

                if skorlar!=[] and "dict" in str(type(skorlar)):
                    txt = f"Bu qrupda É™n yaxÅŸÄ± {max_skor} oyunÃ§u ðŸ“œ\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))
                    skorlar_list = list(skorlar)[::-1][:max_skor]


                    #txt += "\n".join([f"<b>{n+1}</b>. {f('privates.{i}.first_name')} - {skorlar[i]} cevap" for n,i in enumerate(skorlar_list)])
                    for n,i in enumerate(skorlar_list):
                        if n+1 < 4:
                            txt += "ðŸ‘‘ "
                        else:
                            txt += "â–«ï¸ "
                            
                        first_name = f(f'privates.{i}.first_name')
                        username = f(f'privates.{i}.username')
                        if first_name != "":
                            txt += f"<b>{n+1}</b>. {first_name} - <code>{skorlar[i]}</code> cavab"
                        elif username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{skorlar[i]}</code> cavab"

                        txt += "\n"


                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="HÉ™lÉ™ heÃ§ bir xal yoxdur.", reply_markup=keyboard)
            elif tip == "skorum":                  
                sunucu_sayisi = f(f"groups.{chat_id}.sunucu-sayÄ±larÄ±.{user_id}")
                if sunucu_sayisi == "":
                    sunucu_sayisi = 0

                anlatmis = f(f"groups.{chat_id}.anlatma-sayÄ±larÄ±.{user_id}")
                if anlatmis == "":
                    anlatmis = 0

                bilme = f(f"groups.{chat_id}.bilme-sayÄ±larÄ±.{user_id}")
                if bilme == "":
                    bilme = 0

                txt = f'''ðŸ‘¤ {first_name} oyunÃ§unun puanlarÄ±

ðŸ”¹ Bu qrupda
AparÄ±cÄ± olub: \t{sunucu_sayisi}
UÄŸurla tÉ™qdim edildi: \t{anlatmis}
TapdÄ±ÄŸÄ± cavablar: \t{bilme}

ðŸ”¸ BÃ¼tÃ¼n qruplarda
AparÄ±cÄ± olub: \t{f(f"privates.{user_id}.sunucu-sayÄ±sÄ±")}
UÄŸurla tÉ™qdim edildi: \t{f(f"privates.{user_id}.anlatma-sayÄ±sÄ±")}
TapdÄ±ÄŸÄ± cavablar: \t{f(f"privates.{user_id}.bilme-sayÄ±sÄ±")}
            '''

                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
            elif tip == "kureselskor":
                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                
                kullanicilar = f(f"privates", output="$array")

                if "dict" in str(type(kullanicilar)):
                    kullanicilar = [kullanicilar]


                liste = []

                for kullanici in kullanicilar:   
                    id = kullanici["id"]
                    bilme_sayisi = json.loads(kullanici["json"])
                    #bilme_sayisi = f(f"privates.{kullanici}.bilme-sayÄ±sÄ±")

                    if "bilme-sayÄ±sÄ±" in bilme_sayisi:
                        kullanici = id
                        bilme_sayisi = bilme_sayisi["bilme-sayÄ±sÄ±"]

                        liste.append([kullanici,int(bilme_sayisi)])

                liste.sort(key=lambda x:x[1])
                skorlar_list = list(liste)[::-1]

                sira = "âˆž"
                for n, i in enumerate(skorlar_list):
                    if i[0] == str(user_id):
                        sira = n+1
                        break
                
                skorlar_list = skorlar_list[:max_skor]


                #txt = "En iyi max_skor Grup ðŸ“œ\n\n" + "\n".join([f"<b>{n+1}</b>. {f(f'groups.{i[0]}.username')} - {i[1]} cevap" for n,i in enumerate(skorlar_list)])
                txt = f"BÃ¼tÃ¼n zamanlarÄ±n É™n yaxÅŸÄ± {max_skor} oyunÃ§usu ðŸ“œ\n\n"
                
                for n,i in enumerate(skorlar_list):
                    if n+1 < 6:
                        if n+1 == 1:
                            txt += "ðŸ¥‡ "
                        elif n+1 == 2:
                            txt += "ðŸ¥ˆ "
                        elif n+1 == 3:
                            txt += "ðŸ¥‰ "
                        else:
                            txt += "ðŸ‘‘ "
                    else:
                        txt += "â–«ï¸ "

                    firstname = f(f'privates.{i[0]}.first_name')
                    username = f(f'privates.{i[0]}.username')
                    if firstname != "":
                        txt += f"<b>{n+1}</b>. {firstname} - <code>{i[1]}</code> cavab"
                        
                    elif username != "":
                        txt += f"<b>{n+1}</b>. {username} - <code>{i[1]}</code> cavab"


                    txt += "\n"

                txt += f"\nðŸ’Ž SÉ™n {sira} sÄ±radasan {first_name}"
                #bot.send_message(chat_id, txt, reply_markup=keyboard)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
            elif tip == "haftalikgrup":
                skorlar = f(f"groups.{chat_id}.haftalÄ±k-bilme-sayÄ±larÄ±")

                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)

                if skorlar!=[] and skorlar != "":
                    txt = "Qrupda hÉ™ftÉ™nin É™n yaxÅŸÄ± oyunÃ§ularÄ± ðŸ“œ\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))

                    sira = "âˆž"
                    
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


                    txt += "\n"

                    txt += f"\nðŸ’Ž SÉ™n {sira} sÄ±radasan {first_name}"
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="HÉ™lÉ™ heÃ§ bir xal yoxdur.", reply_markup=keyboard)
            elif tip == "haftalikskorprivate":

                ww = f(f"haftalÄ±k-bilme-sayÄ±larÄ±")        
                skorlar = ww

                for i in ww.copy():
                    try:
                        _ = int(ww[i])
                    except:
                        del ww[i]

                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                if skorlar!=[]:
                    txt = "Qlobal hÉ™ftÉ™nin É™n yaxÅŸÄ± oyunÃ§ularÄ± ðŸ“œ\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1])[::-1])


                    for n, i in enumerate(skorlar):
                        if n+1>max_skor:
                            break
                        first_name = f(f'privates.{i}.first_name')
                        username = f(f'privates.{i}.username')

                        cevap_sayisi = skorlar[i]


                        if n+1 < 4:
                            if n+1 == 1:
                                txt += "ðŸ¥‡ "
                            elif n+1 == 2:
                                txt += "ðŸ¥ˆ "
                            elif n+1 == 3:
                                txt += "ðŸ¥‰ "
                        else:
                            txt += "â–«ï¸ "

                        if first_name != "":
                            txt += f"<b>{n+1}</b>. {first_name} - <code>{cevap_sayisi}</code> cavab"
                            
                        elif username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{cevap_sayisi}</code> cavab"

                        txt += "\n"

                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="HÉ™lÉ™ xal yoxdur.", reply_markup=keyboard)
            elif tip == "haftalikskorgroup":
               
                ww = f(f"grup-haftalÄ±k-bilme-sayÄ±larÄ±")        
                skorlar = ww

                for i in ww.copy():
                    try:
                        _ = int(ww[i])
                    except:
                        del ww[i]

                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                if skorlar!=[]:
                    txt = "Qlobal hÉ™ftÉ™nin É™n yaxÅŸÄ± qruplarÄ± ðŸ“œ\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1])[::-1])


                    for n, i in enumerate(skorlar):
                        if n+1>max_skor:
                            break
                        username = f(f'groups.{i}.username')

                        cevap_sayisi = skorlar[i]


                        if n+1 < 4:
                            if n+1 == 1:
                                txt += "ðŸ¥‡ "
                            elif n+1 == 2:
                                txt += "ðŸ¥ˆ "
                            elif n+1 == 3:
                                txt += "ðŸ¥‰ "
                        else:
                            txt += "â–«ï¸ "
                            
                        if username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{cevap_sayisi}</code> cavab"
                        else:
                            txt += f"<b>{n+1}</b>. ? - <code>{cevap_sayisi}</code> cavab"


                        txt += "\n"

                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="HÉ™lÉ™ xal yoxdur", reply_markup=keyboard)
            elif tip == "kureselgrup":
                groups = f(f"groups", output="$array")


                liste = []
                for group in groups:
                    bilme_sayisi = json.loads(group["json"])
                    #bilme_sayisi = f(f"privates.{kullanici}.bilme-sayÄ±sÄ±")

                    if "toplam-bilme-sayÄ±sÄ±" in bilme_sayisi:
                        group = group["id"]
                        bilme_sayisi = bilme_sayisi["toplam-bilme-sayÄ±sÄ±"]
                        #liste.append([[kullanici,int(bilme_sayisi)]])

                        liste.append([group,int(bilme_sayisi)])
                        
                        

                liste.sort(key=lambda x:x[1])
                skorlar_list = list(liste)[::-1]

                
                sira = "âˆž"
                for n, i in enumerate(skorlar_list):
                    if i[0] == chat_id:
                        sira = n+1
                        break

                skorlar_list = skorlar_list[:max_skor]

                #txt = "En iyi max_skor Grup ðŸ“œ\n\n" + "\n".join([f"<b>{n+1}</b>. {f(f'groups.{i[0]}.username')} - {i[1]} cevap" for n,i in enumerate(skorlar_list)])
                txt = f"Æn yaxÅŸÄ± {max_skor} Qrup ðŸ“œ\n\n"
                
                for n,i in enumerate(skorlar_list):
                    first_name = f(f'groups.{i[0]}.first_name')
                    username = f(f'groups.{i[0]}.username')
                    if n+1 < 4:
                        if n+1 == 1:
                            txt += "ðŸ’ŽðŸ¥‡ "
                        elif n+1 == 2:
                            txt += "ðŸ¥ˆ "
                        elif n+1 == 3:
                            txt += "ðŸ¥‰ "
                    else:
                        txt += "â–«ï¸ "

                    if first_name != "":
                        txt += f"<b>{n+1}</b>. {first_name} - <code>{i[1]}</code> cavab"
                        
                    elif username != "":
                        txt += f"<b>{n+1}</b>. {username} - <code>{i[1]}</code> cavab"

                    txt += "\n"
                txt += f"\nðŸ’Ž Bu qrup {sira} sÄ±radadÄ±r."

                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
        
        elif ne_skoru == "kelimeoyunu":          
            if tip == "kureselskor":
                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                
                kullanicilar = f(f"privates", output="$array")

                if "dict" in str(type(kullanicilar)):
                    kullanicilar = [kullanicilar]


                liste = []

                for kullanici in kullanicilar:   
                    id = kullanici["id"]
                    bilme_sayisi = json.loads(kullanici["json"])
                    #bilme_sayisi = f(f"privates.{kullanici}.bilme-sayÄ±sÄ±")

                    if "kelime-turet-bilme" in bilme_sayisi:
                        kullanici = id
                        bilme_sayisi = bilme_sayisi["kelime-turet-bilme"]

                        liste.append([kullanici,bilme_sayisi])

                liste.sort(key=lambda x:x[1])
                skorlar_list = list(liste)[::-1]

                sira = "âˆž"
                for n, i in enumerate(skorlar_list):
                    if i[0] == str(user_id):
                        sira = n+1
                        break
                
                skorlar_list = skorlar_list[:max_skor]


                #txt = "En iyi max_skor Grup ðŸ“œ\n\n" + "\n".join([f"<b>{n+1}</b>. {f(f'groups.{i[0]}.username')} - {i[1]} cevap" for n,i in enumerate(skorlar_list)])
                txt = f"BÃ¼tÃ¼n zamanlarÄ±n É™n yaxÅŸÄ± {max_skor} oyunÃ§usu ðŸ“œ\n\n"
                
                for n,i in enumerate(skorlar_list):
                    if n+1 < 6:
                        if n+1 == 1:
                            txt += "ðŸ¥‡ "
                        elif n+1 == 2:
                            txt += "ðŸ¥ˆ "
                        elif n+1 == 3:
                            txt += "ðŸ¥‰ "
                        else:
                            txt += "ðŸ‘‘ "
                    else:
                        txt += "â–«ï¸ "

                    firstname = f(f'privates.{i[0]}.first_name')
                    username = f(f'privates.{i[0]}.username')
                    
                    if firstname != "":
                        txt += f"<b>{n+1}</b>. {firstname} - <code>{i[1]:.0f}</code> xal" #:.2f
                        
                    elif username != "":
                        txt += f"<b>{n+1}</b>. {username} - <code>{i[1]:.0f}</code> xal"


                    txt += "\n"

                txt += f"\nðŸ’Ž SÉ™n {sira} sÄ±radasan {first_name}"
                #bot.send_message(chat_id, txt, reply_markup=keyboard)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
            elif tip == "skor":
                skorlar = f(f"groups.{chat_id}.kelime-turet-bilme")

                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)

                if skorlar!=[] and "dict" in str(type(skorlar)):
                    txt = f"Bu qrupda É™n yaxÅŸÄ± {max_skor} oyunÃ§u ðŸ“œ\n\n"


                    skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))                   

                    skorlar_list = list(skorlar)[::-1][:max_skor]

                    #txt += "\n".join([f"<b>{n+1}</b>. {f('privates.{i}.first_name')} - {skorlar[i]} cevap" for n,i in enumerate(skorlar_list)])
                    for n,i in enumerate(skorlar_list):
                        if n+1 < 4:
                            txt += "ðŸ‘‘ "
                        else:
                            txt += "â–«ï¸ "
                        first_name = f(f'privates.{i}.first_name')
                        username = f(f'privates.{i}.username')

                        if first_name != "":
                            txt += f"<b>{n+1}</b>. {first_name} - <code>{skorlar[i]:.0f}</code> xal"
                        elif username != "":
                            txt += f"<b>{n+1}</b>. {username} - <code>{skorlar[i]:.0f}</code> xal"

                        txt += "\n"

                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text="HÉ™lÉ™ heÃ§ bir xal yoxdur.", reply_markup=keyboard)
            elif tip == "kureselgrup":
                groups = f(f"groups", output="$array")


                liste = []
                for group in groups:
                    bilme_sayisi = json.loads(group["json"])
                    #bilme_sayisi = f(f"privates.{kullanici}.bilme-sayÄ±sÄ±")

                    if "toplam-kelime-turet-bilme" in bilme_sayisi:
                        group = group["id"]
                        bilme_sayisi = bilme_sayisi["toplam-kelime-turet-bilme"]
                        #liste.append([[kullanici,int(bilme_sayisi)]])

                        liste.append([group,bilme_sayisi])
                        
                        
                liste.sort(key=lambda x:x[1])
                skorlar_list = list(liste)[::-1]
                
                sira = "âˆž"
                for n, i in enumerate(skorlar_list):
                    if i[0] == chat_id:
                        sira = n+1
                        break
                
                skorlar_list = skorlar_list[:max_skor]

                #txt = "En iyi max_skor Grup ðŸ“œ\n\n" + "\n".join([f"<b>{n+1}</b>. {f(f'groups.{i[0]}.username')} - {i[1]} cevap" for n,i in enumerate(skorlar_list)])
                txt = f"Æn yaxÅŸÄ± {max_skor} Qrup ðŸ“œ\n\n"
                
                for n,i in enumerate(skorlar_list):
                    first_name = f(f'groups.{i[0]}.first_name')
                    username = f(f'groups.{i[0]}.username')
                    if n+1 < 4:
                        if n+1 == 1:
                            txt += "ðŸ’ŽðŸ¥‡ "
                        elif n+1 == 2:
                            txt += "ðŸ¥ˆ "
                        elif n+1 == 3:
                            txt += "ðŸ¥‰ "
                    else:
                        txt += "â–«ï¸ "

                    if first_name != "":
                        txt += f"<b>{n+1}</b>. {first_name} - <code>{i[1]:.0f}</code> xal"
                        
                    elif username != "":
                        txt += f"<b>{n+1}</b>. {username} - <code>{i[1]:.0f}</code> xal"

                    txt += "\n"
                
                txt += f"\nðŸ’Ž Bu qrup isÉ™ {sira} sÄ±radadÄ±r."

                callback_button1 = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                callback_button3 = types.InlineKeyboardButton(text="ðŸ”™ Geri", callback_data=f'skor_{ne_skoru}')
                keyboard.add(callback_button1, callback_button3)
                await bot.edit_message_text(chat_id=chat_id, message_id=cagri.message.message_id, text=txt, reply_markup=keyboard)

        else:
            await bot.answer_callback_query(cagri.id, text="ðŸ˜ž")

@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(cagri): #Ã§aÄŸrÄ±cÄ± cagrici
    #grup veya kullanÄ±cÄ± id
    t0 = time.time()

    chat_id = str(cagri.message.json["chat"]["id"]) #deÄŸiÅŸken
    user_id = cagri.from_user.id #sabit

    

    if sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{chat_id}'") != []:
        await bot.send_message(chat_id, "âš ï¸ Qrup bot tÉ™rÉ™findÉ™n bloklanÄ±b.")
        await bot.leave_chat(chat_id)
        return
    elif sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{user_id}'") != []:
        await bot.answer_callback_query(cagri.id, 'âš ï¸ Siz botdan bloklanmÄ±sÄ±nÄ±z.', show_alert=True)
        return

    sorgu = cagri.data


    if not await is_subscribed(chat_id, user_id):
        # user is not subscribed. send message to the user
        await bot.answer_callback_query(cagri.id, 'â›± ZÉ™hmÉ™t olmasa qrupa daxil olun.')
        #bot.send_message(kurucu_id, "Gereksiz deÄŸil. 11223344")
        return

    first_name = None
    if cagri.from_user.first_name != None:
        first_name = cagri.from_user.first_name
        first_name = first_name.replace("'","").replace("<","").replace(">","")

    username = None
    if cagri.from_user.username != None:
        username = cagri.from_user.username
        username = username.replace("'","").replace("<","").replace(">","")

    cagri.message.from_user = cagri.from_user #eÄŸer bunu yapmazsak bot sunar


    #private or group
    msg_type = cagri.message.json["chat"]["type"]


    if "group" in msg_type:
        grup_username = cagri.message.json["chat"]["title"]
        grup_username = grup_username.replace("'","")

        if f(f"groups.{chat_id}.username") == "":
            await bot.send_message(-1002119059079, f"ðŸ“œ {grup_username} âŸ¶ {len(f('groups')) + 1}")
            
        f(f"groups.{chat_id}.username", grup_username) 
        f(f"groups.{chat_id}.son_oyun_aktivitesi", time.time())

    if sorgu == "kelimeturet_harf":
        await bot.answer_callback_query(cagri.id, f'YaxÄ±nda... â˜ºï¸', show_alert=False)
        return
    elif sorgu.startswith("sessiz_sinema"):               
        if oyun_var_mi(chat_id) != False:
            await bot.answer_callback_query(cagri.id, f'âŒ HÃ¶rmÉ™tli {first_name}, hazÄ±rda aktiv oyunlar var.', show_alert=False)
            return
        
        if sorgu == "sessiz_sinema":
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text="ðŸ‘¥ SÄ±ralÄ± aparÄ±cÄ±", callback_data="sessiz_sinema_oto-sunucu")
            callback_button2 = types.InlineKeyboardButton(text="ðŸ“Œ Sabit aparÄ±cÄ±", callback_data="sessiz_sinema_sabit")
            callback_button3 = types.InlineKeyboardButton(text="ðŸ”ˆ Normal aparÄ±cÄ±", callback_data="sessiz_sinema_normal")
            keyboard.add(callback_button1, callback_button2)
            keyboard.add(callback_button3)
            await bot.edit_message_text(f'ðŸŽ¯ Oyun modu nÉ™ olsun?', chat_id, cagri.message.id, reply_markup=keyboard)
        else:
            mod = sorgu.split("_")[-1]    
        
            await bot.delete_message(chat_id, cagri.message.id)

            await sessiz_sinema_baslat(cagri.message, mod = mod)

        return
    elif sorgu.startswith("kelimeoyunu"):       
        if oyun_var_mi(chat_id) != False:
            await bot.answer_callback_query(cagri.id, f'âŒ HÃ¶rmÉ™tli {first_name}, hazÄ±rda aktiv oyunlar var.', show_alert=False)
            return

        if sorgu.startswith("kelimeoyunu_"):   
            ayir = sorgu.split("_")
            if len(ayir) == 2:
                birlestir = "_".join(ayir[:2])
                kolay_callback = birlestir + "_kolay"
                zor_callback = birlestir + "_zor"

                keyboard = types.InlineKeyboardMarkup()
                callback_button1 = types.InlineKeyboardButton(text="ðŸ§  Asan (x1 puan)", callback_data=kolay_callback)
                callback_button2 = types.InlineKeyboardButton(text="ðŸ’£ Ã‡É™tin (x4 puan)", callback_data=zor_callback)
                keyboard.add(callback_button1, callback_button2)
                #bot.send_message(chat_id, f'ðŸŽ¯ <a href="tg://user?id={user_id}">{first_name}</a>, {ayir[1]} round oyunun zorluÄŸu ne olsun?', reply_markup=keyboard)                
                await bot.edit_message_text(f'<a href="tg://user?id={user_id}">{first_name}</a> {ayir[1]} raund seÃ§di.\nðŸ¤” Oyunun Ã§É™tinliyi nÉ™ olsun?', chat_id, cagri.message.id, reply_markup=keyboard)
                return
            elif len(ayir) == 3:
                if ayir[1] == "inf":
                    ayir[1] = 999999
                await kelime_turet_baslat(cagri.message, toplam_round = int(ayir[1]), zorluk = ayir[2])                
                await bot.delete_message(chat_id, cagri.message.id)
            else:
                await bot.send_message(chat_id, f'ðŸ¤·')
        else:
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text="15", callback_data="kelimeoyunu_15")
            callback_button2 = types.InlineKeyboardButton(text="30", callback_data="kelimeoyunu_30")
            callback_button3 = types.InlineKeyboardButton(text="45", callback_data="kelimeoyunu_45")
            callback_button4 = types.InlineKeyboardButton(text="60", callback_data="kelimeoyunu_60")
            callback_button5 = types.InlineKeyboardButton(text="75", callback_data="kelimeoyunu_75")
            callback_button6 = types.InlineKeyboardButton(text="90", callback_data="kelimeoyunu_90")
            callback_button7 = types.InlineKeyboardButton(text="Sonsuz â™¾", callback_data="kelimeoyunu_inf")
            
            keyboard.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6)
            keyboard.add(callback_button7)
            await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{first_name}</a> oyun neÃ§É™ raund olsun?', reply_markup=keyboard)
            
            if not "skor" in cagri.message.text.lower():
                await bot.delete_message(chat_id, cagri.message.id)
            return      
    elif sorgu.startswith("ipucu"):
        #ipucu_kelime
        oyun = oyun_var_mi(chat_id)
        if oyun_var_mi(chat_id) == False:
            await bot.answer_callback_query(cagri.id, f'HÃ¶rmÉ™tli {first_name} hazÄ±rda aktiv oyun yoxdur.', show_alert=False)
            return

        oyun_id = oyun[0]

        if sorgu == "ipucu_kelime":
            kelime = f(f"games.{oyun_id}.kelime")
            anlamlar = ""
            try:
                anlam = anlam_getir(kelime)
                anlamlar = "\n".join([f"âœï¸ TÉ™rif {say+1}: {i}" for say, i in enumerate(random.sample(anlam,min(2,len(anlam))))])

            except:
                pass
            if anlamlar == "":
                anlamlar = "âŒ TÉ™ssÃ¼f ki, yox."
            else:                
                anlamlar = ireplace(kelime, 'â“', anlamlar).strip()

            try:
                await bot.answer_callback_query(cagri.id, f'ðŸ”Ž MÉ™slÉ™hÉ™tlÉ™r:\n{anlamlar}', show_alert=True)
            except:
                await bot.answer_callback_query(cagri.id, f'ðŸ”Ž MÉ™slÉ™hÉ™tlÉ™r:\n{anlamlar[:100]}', show_alert=True)

    elif sorgu.startswith("istiyorum"):
        oyun = oyun_var_mi(chat_id)
        if oyun != False:
            await bot.answer_callback_query(cagri.id, "ðŸ“œ Oyun onsuzda baÅŸladÄ±.", show_alert=False)
            return

        if "sinema_" in sorgu:
            ayir = sorgu.split("_")
            mod = ayir[3]
         
            if len(ayir) == 4: #istiyorum_mod
                await sessiz_sinema_baslat(cagri.message, mod = mod)
            elif len(ayir) == 5: # istiyorum_mod_userid
                userid = ayir[4]
                if time.time() - cagri.message.date < 7:
                    if userid == str(user_id):
                        await sessiz_sinema_baslat(cagri.message,  mod = mod)
                    else:
                        bekle = int(time.time() - cagri.message.date)
                        await bot.answer_callback_query(cagri.id, f"ðŸ“œ {7-bekle} saniyÉ™ gÃ¶zlÉ™yin.", show_alert=False)
                        #print(f"{first_name} âŸ¹ {userid} ({type(userid)}) | {user_id} ({type(user_id)})")
                else:
                    await sessiz_sinema_baslat(cagri.message, mod = mod)
        else:
            await sessiz_sinema_baslat(cagri.message)

        return    
    elif sorgu == "pas_gec":
        konumlar = oyun_var_mi(chat_id) #oyun_konum grup_konum
        if konumlar != False:
            oyun_id = konumlar[0]

            gecen = int(time.time() - oyun_id/zaman_hassasiyeti)
            if gecen < 6:
                await bot.answer_callback_query(cagri.id, f"ðŸ“œ KeÃ§mÉ™k Ã¼Ã§Ã¼n 6 saniyÉ™ keÃ§mÉ™lidir, hazÄ±rda keÃ§ir: {gecen}", show_alert=True)
                return

            if f(f"games.{oyun_id}.oyun_tipi") == "kelimeoyunu":
                kelime = f(f"games.{oyun_id}.kelime")

                skorlar = f(f"games.{oyun_id}.skorlar")
                round = f(f"games.{oyun_id}.round")
                toplam_round = f(f"games.{oyun_id}.toplam_round")
                zorluk = f(f"games.{oyun_id}.zorluk")

                oyunu_iptal_et(oyun_id)
               
                await kelime_turet_baslat(cagri.message, toplam_round = toplam_round, round = round, skorlar = skorlar, zorluk = zorluk, header = f'âŒ <a href="tg://user?id={user_id}">{first_name}</a> sÃ¶z keÃ§di!\nDÃ¼zgÃ¼n cavab â†’ <b>{kelime}</b> idi.\n')

            else:
                await bot.answer_callback_query(cagri.id, f"â™¦ï¸ Bu É™mr yalnÄ±z wordplay oyununda iÅŸlÉ™yir!")
        else:
            await bot.answer_callback_query(cagri.id, f"â™¦ï¸ Aktiv sÃ¶z oyunu yoxdur.")
    
    elif sorgu == "sil":    
        try:
            if cagri.message.reply_to_message.from_user.id != user_id and not await is_admin(chat_id, user_id):
                await bot.answer_callback_query(cagri.id, "ðŸ“œ Siz bu É™mri gÃ¶ndÉ™rmÉ™diniz.", show_alert=False)
                return   
        except:
            pass
        
        await bot.delete_message(chat_id, cagri.message.id)
    elif sorgu.startswith("skor_"):    
        try:
            if cagri.message.reply_to_message.from_user.id != user_id:
                await bot.answer_callback_query(cagri.id, "ðŸ“œ Siz bu É™mri gÃ¶ndÉ™rmÉ™diniz.", show_alert=False)
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
            await bot.answer_callback_query(cagri.id, f"â™¦ï¸ Aktiv oyun var.", show_alert=True)
            return
            #return

        if time.time() - cagri.message.date < 2:
            bekle = int(2 - (time.time() - cagri.message.date))
            await bot.answer_callback_query(cagri.id, f"â™¦ï¸ {bekle} saniyÉ™ gÃ¶zlÉ™yin.", show_alert=False)
            return
        
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="ðŸ™‚ DoÄŸruluq", callback_data="dogrulukcesaret_d")
        callback_button2 = types.InlineKeyboardButton(text="ðŸ¥³ CÉ™sarÉ™t", callback_data="dogrulukcesaret_c")
        keyboard.add(callback_button1, callback_button2)
        

        if sorgu == "dogrulukcesaret":            
            getir = sql_get("SELECT * FROM dogruluk_cesaret ORDER BY RANDOM() LIMIT 1;")
            while "http" in getir["yazi"]:
                getir = sql_get("SELECT * FROM dogruluk_cesaret ORDER BY RANDOM() LIMIT 1;")

            yazi = f"<a href='tg://user?id={user_id}'>{first_name}</a> oyuna baÅŸladÄ±!\n\n"
            yazi = yazi + getir["yazi"]
            await bot.edit_message_text(yazi, chat_id, cagri.message.id, reply_markup=keyboard)
        else:
            ayir = sorgu.split("_")[1]

            tip = ""
            if ayir == "d":
                tip = "doÄŸruluÄŸu"
            elif ayir == "c":
                tip = "cesareti"
            
            yazi = f"<a href='tg://user?id={user_id}'>{first_name}</a>, <b>{tip}</b> seÃ§di\n\n"

            getir = sql_get(f"SELECT * FROM dogruluk_cesaret WHERE tur LIKE '{ayir}' ORDER BY RANDOM() LIMIT 1;")
            yazi = yazi + getir["yazi"]
            await send_msgimg(chat_id,yazi, reply_markup=keyboard)
        
                #return
    #elif oyun_var_mi(chat_id) != False:
    else:
        oyun_id = f(f"groups.{chat_id}.oyun")

        acan_id = f(f"games.{oyun_id}.aÃ§an_id")

        if oyun_var_mi(chat_id) == False:
            await bot.answer_callback_query(cagri.id, f'â“ HazÄ±rda aktiv oyun yoxdur. BaÅŸlamaq Ã¼Ã§Ã¼n /game yazÄ±n.', show_alert=True)
            return

    # or " " + first_name +" kelime" in cagri.message.text
        if acan_id == user_id:
           
            if sorgu == "kelime_bak":
                #def yap():
                kelime = f(f"games.{oyun_id}.kelime")
                txt = "ðŸ—£ï¸ SualÄ±n: " +kelime + "\n\n"

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


                await bot.answer_callback_query(cagri.id, txt, show_alert=True)

            elif sorgu == "siradaki_kelime":
                #def yap():
                yeni_kelime = random_from_table()["kelime"].replace("'", "")

                txt = "ðŸ”„ Yeni sÃ¶zÃ¼n: " +yeni_kelime + "\n\n"

                await bot.answer_callback_query(cagri.id, txt, show_alert=True)
                f(f"games.{oyun_id}.sozluk","")
                f(f"games.{oyun_id}.kelime", yeni_kelime)
                
            elif sorgu == "istemiyorum":
                gecen = int(time.time() - oyun_id/zaman_hassasiyeti)
                if gecen < 3:
                    await bot.answer_callback_query(cagri.id, f"ðŸ“œ AparÄ±cÄ±lÄ±qdan imtina etmÉ™k Ã¼Ã§Ã¼n 3 saniyÉ™ keÃ§mÉ™lidir: {gecen}", show_alert=True)
                    return
                
                oyun_tipi = f(f"games.{oyun_id}.oyun_tipi")

                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="ðŸ—£ï¸ AparÄ±cÄ± olmaq istÉ™yirÉ™m!", callback_data="istiyorum_"+oyun_tipi)
                keyboard.add(callback_button)
                kelime = f(f"games.{oyun_id}.kelime")
                await bot.send_message(chat_id, f'ðŸ”´ <a href="tg://user?id={user_id}">{first_name}</a> AparÄ±cÄ± olmaq istÉ™mir!\nâ†’ {kelime}', reply_markup=keyboard)
                
                #f(f"games.{oyun_id}", "$del")
                oyunu_iptal_et(oyun_id)
        else:
            acan_user = f(f"games.{oyun_id}.aÃ§an_user")
            await bot.answer_callback_query(cagri.id, f'âŒ SÉ™n izah etmirsÉ™n.\n{acan_user} izah edir..!', show_alert=False)


async def is_admin(chat_id, user_id):
    if "admin" in (await bot.get_chat_member(chat_id, user_id)).status or "creator" in (await bot.get_chat_member(chat_id, user_id)).status:
        return True
    return False

@bot.message_handler(commands=['resetskor'])
async def resetskor(message):
    chat_tipi = message.chat.type

    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id #sabit


    if chat_tipi == "private":
        await bot.send_message(chat_id, "Bu É™mr yalnÄ±z qruplarda iÅŸlÉ™yir.")
        return


    if "creator" in bot.get_chat_member(chat_id, user_id).status or (user_id == kurucu_id and "!" in message.text):
        await bot.send_message(chat_id, "BÃ¼tÃ¼n xallar sÄ±fÄ±rlandÄ±!")
        f(f"groups.{chat_id}.anlatma-sayÄ±larÄ±",{})
        f(f"groups.{chat_id}.bilme-sayÄ±larÄ±",{})
        f(f"groups.{chat_id}.sunucu-sayÄ±larÄ±",{})

        f(f"groups.{chat_id}.anlatma-sayÄ±sÄ±",0)
        f(f"groups.{chat_id}.bilme-sayÄ±sÄ±",0)
        f(f"groups.{chat_id}.sunucu-sayÄ±sÄ±",0)
    else:
        await bot.send_message(chat_id, "Siz tÉ™sisÃ§i deyilsiniz.")




@bot.message_handler(commands=['stop'])
async def iptal(message):
    chat_tipi = message.chat.type

    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id #sabit


    if chat_tipi == "private":
        await bot.send_message(chat_id, "Bu É™mr yalnÄ±z qruplarda iÅŸlÉ™yir.")
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

                metin = f"""â—ï¸ Oyun dayandÄ±rÄ±ldÄ±

QaliblÉ™r ðŸ‘‘
"""
                for n, i in enumerate(skorlar_list):
                    if n + 1 == 1:
                        metin += "ðŸ¥‡ "
                    elif n + 1 == 2:
                        metin += "ðŸ¥ˆ "
                    elif n + 1 == 3:
                        metin += "ðŸ¥‰ "
                    else:
                        metin += "â–«ï¸ "

                    skorlar[i] = round(skorlar[i])
                    metin += f'<b>{n+1}.</b> {f(f"privates.{i}.first_name")} â†’ <code>{skorlar[i]}</code> puan'
                    
                    metin += "\n"
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="TÉ™krar oyna ðŸ”ƒ", callback_data="kelimeoyunu")
                keyboard.add(callback_button)
                await bot.send_message(chat_id, metin, reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="TÉ™krar baÅŸlat ðŸ”ƒ", callback_data=oyun_tipi)
                keyboard.add(callback_button)

                await bot.send_message(chat_id, f"â• Oyun uÄŸurla lÉ™ÄŸv edildi!\nCavab: {kelime}", reply_markup=keyboard)
            #f(f"games.{oyun_id}", "$del")
            oyunu_iptal_et(oyun_id)
            await log_gonder(user_id=user_id, chat_id=chat_id, eylem="iptal etti")
        else:
            await bot.send_message(chat_id, "â­ï¸ Siz admin deyilsiniz")
    else:
        await bot.send_message(chat_id, "ðŸ§© Aktiv bir oyun yoxdur.")

@bot.message_handler(commands=['jdjdjd'])
async def rehber(message):
    #chat_tipi = message.chat.type

    chat_id = message.chat.id #deÄŸiÅŸken, private veya group
    user_id = message.from_user.id #sabit


    soru_suresi = f("soru_suresi")
    soru_suresi = str(round(soru_suresi/60,1)).replace(".0","")

    await bot.send_message(chat_id,f"""<b>ðŸ« Oyun qaydalarÄ± ðŸ“– :</b

ðŸ“š SÃ¶z oyunu 2 roldan ibarÉ™tdir. AparÄ±cÄ±nÄ±n (sÃ¶zÃ¼ deyÉ™n) izah etmÉ™k Ã¼Ã§Ã¼n 4 dÉ™qiqÉ™ vaxtÄ± var. 4 dÉ™qiqÉ™ É™rzindÉ™ deyilÉ™n sÃ¶z lÉ™ÄŸv edilir vÉ™ yeni rÉ™vayÉ™tÃ§inin hÃ¼ququ Ã§Ä±xÄ±r.

ðŸ“š Ã–z sÃ¶zÃ¼nÃ¼zÃ¼ É™lavÉ™ etmÉ™k Ã¼Ã§Ã¼n siz botun profilinÉ™ daxil olmalÄ± vÉ™ bota birdÉ™fÉ™lik ilk mesaj gÃ¶ndÉ™rmÉ™lisiniz. Sonra, mÉ™nim Ã¶z sÃ¶zÃ¼m dÃ¼ymÉ™sini basdÄ±ÄŸÄ±nÄ±z zaman, botun sizÉ™ gÃ¶ndÉ™rdiyi mesaja cavab vermÉ™klÉ™ Ã¶z sÃ¶zÃ¼nÃ¼zÃ¼ É™lavÉ™ edÉ™ bilÉ™rsiniz.0

ðŸ“š SÃ¶z tÃ¶rÉ™mÉ™ botunda botun verdiyi qarÄ±ÅŸÄ±q sÃ¶zlÉ™rdÉ™n dÃ¼zgÃ¼nÃ¼nÃ¼ tapmalÄ±sÄ±nÄ±z.

ðŸ“š Qrupdaxili hÉ™ftÉ™lik ballar vÉ™ qlobal hÉ™ftÉ™lik ballarla yarÄ±ÅŸlar tÉ™ÅŸkil edÉ™ bilÉ™rsiniz.

ðŸ‘¨ðŸ»â€ðŸ’» TÉ™klif vÉ™ suallar Ã¼Ã§Ã¼n: @The_ferid
""")


@bot.message_handler(content_types=['text', "photo"])
async def messages(mesaj):
    t0 = time.time()
    chat_tipi = mesaj.chat.type

    chat_id = mesaj.chat.id #deÄŸiÅŸken, private veya ggroup
    user_id = mesaj.from_user.id #sabit

    content_type = mesaj.content_type



    if sql_get(f"SELECT * FROM ban_listesi WHERE id LIKE '{chat_id}'") != []:
        bot.send_message(chat_id, "âš ï¸ Qrup bot tÉ™rÉ™findÉ™n bloklanÄ±b.")
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
            await bot.send_message(chat_id, f"<b>â€¢ {first_name}:</b> {msg[1:].strip()}")
            
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
               
            elif msg.lower() == "/id":
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="âŒ Sil", callback_data='sil')
                keyboard.add(callback_button)

                try:
                    await bot.send_message(chat_id,f"""
<b>Ä°stifadÉ™Ã§i ID:</b> <code>{mesaj.reply_to_message.from_user.id}</code>
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

    oyun_tipi = ""
    if "oyun_tipi" in oyun_json:
        oyun_tipi = oyun_json["oyun_tipi"]

    if oyun_tipi == "sessiz_sinema":

        kelime = ""
        if "kelime" in oyun_json:
            kelime = oyun_json["kelime"]

        acan_id = 0
        if "aÃ§an_id" in oyun_json:
            acan_id = oyun_json["aÃ§an_id"]

        acan_user = ""
        if "aÃ§an_user" in oyun_json:
            acan_user = oyun_json["aÃ§an_user"]
            
        kelime = kelime.replace('I', 'Ä±').replace('Ä°', 'i').lower()
        
        yazilan = msg.replace('I', 'Ä±').replace('Ä°', 'i').lower()

        if user_id in admins:
            if msg == "*":
                yazilan = kelime
        
        if acan_id == user_id:
            f(f"games.{oyun_id}.sunucu_son_mesajÄ±", time.time())

        
        skor_arttir(f"games.{oyun_id}.atÄ±lan_mesaj")

        if (
        yazilan.replace(" ","") == kelime.replace(" ","") or
        " " + kelime + " " in " " + yazilan + " " or
        
        (mesaj.reply_to_message != None and "text" in mesaj.reply_to_message.json and (mesaj.reply_to_message.json["text"].replace('I', 'Ä±').replace('Ä°', 'i').lower() + yazilan == kelime.replace(" ","")) ) or
        (user_id in admins and (msg == "*" or msg == "**"))
        ): # and soran kiÅŸi deÄŸilse
            if acan_id != user_id or msg == "**":
                
                mod = f(f"games.{oyun_id}.oyun_modu")
                acan_id = f(f"games.{oyun_id}.aÃ§an_id")
                acan_user = f(f"games.{oyun_id}.aÃ§an_user")



                if first_name == "Channel" or first_name == "Group":
                    await bot.send_message(chat_id, "Kanal vÉ™ ya qrup hesabÄ± sualÄ± bilÉ™ bilmÉ™z, Ã¼zr istÉ™yirik ðŸ¥º")
                    await bot.delete_message(chat_id, mesaj.message_id)
                    return
                
                oyunu_iptal_et(oyun_id)


                if mod == "sabit":
                    sec = random.choice(["ðŸ“", "ðŸ“Œ"])
                    await sessiz_sinema_baslat(mesaj,text = f'''<a href="tg://user?id={user_id}"><b>{first_name}</b></a> â†’ <b>{kelime}</b> âœ…

{sec} <a href="tg://user?id={acan_id}"><b>{acan_user}</b></a> sÃ¶zÃ¼ izah edir.''', mod = mod, acan_id = acan_id, acan_user = acan_user)                  
                elif mod == "oto-sunucu":
                    await sessiz_sinema_baslat(mesaj,text = f'''DoÄŸru bildiâ†’ <b>{kelime}</b> âœ…

<a href="tg://user?id={user_id}"><b>{first_name}</b></a> dÃ¼z baÅŸa dÃ¼ÅŸdÃ¼ vÉ™ sÃ¶zÃ¼ izah edir ðŸ—£ï¸''', mod = mod)
                elif mod == "normal":
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="ðŸ—£ï¸ AparÄ±cÄ± olmaq istÉ™yirÉ™m!", callback_data=f'istiyorum_sessiz_sinema_{mod}_{user_id}')
                    keyboard.add(callback_button)
                    await bot.send_message(chat_id,f'''DoÄŸru bildiâ†’ <b>{kelime}</b> âœ…

<a href="tg://user?id={user_id}"><b>{first_name}</b></a> doÄŸru tapdÄ±''', reply_markup=keyboard)
                

                skor_arttir(f"groups.{chat_id}.anlatma-sayÄ±larÄ±.{user_id}")


                anlatma_sayisi = skor_arttir(f"privates.{acan_id}.anlatma-sayÄ±sÄ±")
                if anlatma_sayisi % 100 == 0:
                    await bot.send_message(chat_id,f'{anlatma_sayisi}. uÄŸurla dediniz {acan_user} ðŸ˜Š')

                f(f"privates.{user_id}.username",username)
                f(f"privates.{user_id}.first_name",first_name)


                skor_arttir(f"groups.{chat_id}.haftalÄ±k-bilme-sayÄ±larÄ±.{user_id}")
                skor_arttir(f"groups.{chat_id}.haftalÄ±k-toplam-bilme-sayÄ±sÄ±")

                skor_arttir(f"groups.{chat_id}.bilme-sayÄ±larÄ±.{user_id}")
                skor_arttir(f"groups.{chat_id}.toplam-bilme-sayÄ±sÄ±")

                bilme_sayisi = skor_arttir(f"privates.{user_id}.bilme-sayÄ±sÄ±")
                if bilme_sayisi % 100 == 0:
                    await bot.send_message(chat_id,f'{bilme_sayisi}. dÉ™fÉ™ dÃ¼z bildi, tÉ™brik edirÉ™m {first_name} ðŸ˜Š')

                elif bilme_sayisi == 1:
                    await bot.send_message(chat_id,f'HÃ¶rmÉ™tli {first_name} ilk dÉ™fÉ™ tapdÄ± ðŸŒŸ') # ve sorusunu anlatÄ±yor

                skor_arttir(f"haftalÄ±k-bilme-sayÄ±larÄ±.{user_id}")
                skor_arttir(f"grup-haftalÄ±k-bilme-sayÄ±larÄ±.{chat_id}")

                
                f(f"privates.{user_id}.son-oyun-oynama",time.time())
            else:
                if random.randint(0,2) == 0:
                    mod = f(f"games.{oyun_id}.oyun_modu")
                    oyunu_iptal_et(oyun_id)

                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="ðŸ—£ï¸ MÉ™n aparÄ±cÄ± olmaq istÉ™yirÉ™m!", callback_data=f'istiyorum_sessiz_sinema_{mod}')
                    keyboard.add(callback_button)
                    await bot.send_message(chat_id,f'''{acan_user} dÃ¼zgÃ¼n cavabÄ± É™ldÉ™n verdi â†’ <b>{kelime}</b> âœ…''', reply_markup=keyboard, reply_to_message_id=mesaj.message_id)
                else:
                    sec = random.choice([
                        "ðŸ™ˆðŸ™‰ðŸ™Š",
                        "heyy",
                        "ðŸ¤¦â€â™‚ï¸",
                        "ðŸ¤¦",
                        "ðŸ¤¦â€â™€ï¸",
                        "bu qÉ™tiliklÉ™ dÃ¼zgÃ¼n cavab deyil.",
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
        if "aÃ§an_id" in oyun_json:
            acan_id = oyun_json["aÃ§an_id"]
            

        kelime = kelime.replace('I', 'Ä±').replace('Ä°', 'i').lower()
        
        yazilan = msg.replace('I', 'Ä±').replace('Ä°', 'i').lower()

        if (
        yazilan.replace(" ","") == kelime.replace(" ","") or
        " " + kelime + " " in " " + yazilan + " " or

        (user_id in admins and (msg == "*" or msg == "**"))
        ):

            if acan_id != user_id or msg == "**":
                
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

                    metin = """<b>ðŸ Oyun Bitti!</b>

 <b>â­â­<u> ðŸŽ– XAL SÄ°YAHISI ðŸŽ– </u>â­â­</b>
 """
                    for n, i in enumerate(skorlar_list):
                        metin += '\n'
                        if n + 1 == 1:
                            metin += "ðŸ¥‡ "
                        elif n + 1 == 2:
                            metin += "ðŸ¥ˆ "
                        elif n + 1 == 3:
                            metin += "ðŸ¥‰ "
                        else:
                            metin += "â–«ï¸ "
                        
                        metin += f'<b>{n+1}.</b> {f(f"privates.{i}.first_name")} â†’ <code>{skorlar[i]:.0f}</code> xal'
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="ðŸ”„ TÉ™krar oyna", callback_data="kelimeoyunu")
                    keyboard.add(callback_button)
                    await bot.send_message(chat_id, metin, reply_markup=keyboard)
                
                else:
                    if str(user_id) in skorlar:
                        skorlar[str(user_id)] += puan
                    else:
                        skorlar[str(user_id)] = puan
                    await kelime_turet_baslat(mesaj, toplam_round = toplam_round, round = round, skorlar = skorlar, zorluk = zorluk, header=f'<a href="tg://user?id={user_id}"><b>{first_name}</b></a> DoÄŸru bildiâ†’ <b>{kelime}</b> âœ…\n')
                    skor_arttir(f"groups.{chat_id}.kelime-turet-bilme.{user_id}",puan)
                    skor_arttir(f"groups.{chat_id}.toplam-kelime-turet-bilme",puan)
                    skor_arttir(f"privates.{user_id}.kelime-turet-bilme",puan)
                        
                f(f"privates.{user_id}.son-oyun-oynama",time.time())
    else:
        oyunu_iptal_et(oyun_id)
        await bot.send_message(chat_id,f'Problem var, É™n qÄ±sa zamanda dÃ¼zÉ™ldÉ™cÉ™yik. ðŸ˜Š')

    hizlar["text"] = time.time() - t0




async def game_master():
    t0 = time.time()
    soru_suresi = f(f"soru_suresi")

    
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


                if oyun_tipi == "sessiz_sinema":
                    uyari = f(f"games.{id}.uyarÄ±")
                    sunucu_son_mesaji = f(f"games.{id}.sunucu_son_mesajÄ±")
                    if sunucu_son_mesaji != "":
                        sunucu_son_mesaji = float(sunucu_son_mesaji)
                    
                    if soru_suresi < int(time.time()) - id/zaman_hassasiyeti:
                        #acan_id = f(f"games.{i}.aÃ§an_id")

                        kelime = games_js["kelime"]

                        #bot.send_message(konum, f'<a href="tg://user?id={acan_id}">{acan_user}</a> sunucu olmak istemiyor!', parse_mode='html', reply_markup=keyboard)



                        if str(id) == str(f(f"groups.{konum}.oyun")):
                            oyun_modu = f(f"games.{id}.oyun_modu")

                            keyboard = types.InlineKeyboardMarkup()
                            callback_button = types.InlineKeyboardButton(text="MÉ™n aparÄ±cÄ± olmaq istÉ™yirÉ™m! ðŸ™‹ðŸ»ðŸ™‹ðŸ»â€â™€ï¸", callback_data="istiyorum_"+oyun_modu)
                            keyboard.add(callback_button)
                            
                            acan_user = games_js["aÃ§an_user"]
                            
                            await bot.send_message(konum, f'âŒ›ï¸ {round(soru_suresi/60)} dÉ™qiqÉ™lik vaxt bitdi! Cavab â†’ <b>{kelime}</b>\n\n{acan_user} daha aparÄ±cÄ± deyil.', reply_markup=keyboard)


                            oyunu_iptal_et(id)
                        elif oyun_var_mi(konum) == False:
                            oyunu_iptal_et(id)
                            
                    #elif ((sunucu_son_mesaji == "" and 60 < time.time() - id/zaman_hassasiyeti < 65) or (sunucu_son_mesaji != "" and 60 < time.time() - sunucu_son_mesaji < 65)) and uyari == "":
                    elif (sunucu_son_mesaji == "" and 60 < time.time() - id/zaman_hassasiyeti < 65) and uyari == "" and f(f"games.{id}.oyun_modu") != "sabit":
                        acan_user = games_js["aÃ§an_user"]
                        acan_id = games_js["aÃ§an_id"]

                        user = f'<a href="tg://user?id={acan_id}">{acan_user}</a>'
#
                        await bot.send_message(konum, random.choice([
                            f'ZÉ™hmÉ™t olmasa bir ÅŸey deyin {user} ðŸ¥º',
                            f"{user} zÉ™hmÉ™t olmasa bir ÅŸey deyin ðŸ˜¢",
                            f"Buyurun, heÃ§ nÉ™ demÉ™yÉ™cÉ™ksiniz? {user} :/",
                            f"ZÉ™hmÉ™t olmasa problemi tÉ™svir edin {user} D:",
                            f"SÉ™nÉ™ gÃ¼l vermÉ™k istÉ™yirÉ™m, {user} â†’ " + random.choice(["ðŸŒ¼", "ðŸŒ·","ðŸŒ»", "ðŸŒ¼","ðŸŒº","ðŸŒ¸", "ðŸŒ¹"]) +". BÉ™s indi izah edirsÉ™n?",
                            f"ZÉ™hmÉ™t olmasa bir ÅŸey deyin {user} ðŸ¤”",

                        
                        
                        ]))
                        f(f"games.{id}.uyarÄ±", 1)
                       
                    elif (sunucu_son_mesaji == "" and 90 < time.time() - id/zaman_hassasiyeti < 95) and uyari == 1 and f(f"games.{id}.oyun_modu") != "sabit":
                        acan_user = games_js["aÃ§an_user"]
                        acan_id = games_js["aÃ§an_id"]

                        user = f'{acan_user}'

                        kelime = games_js["kelime"]

                        keyboard = types.InlineKeyboardMarkup()
                        callback_button = types.InlineKeyboardButton(text="AparÄ±cÄ± olmaq istÉ™yirÉ™m! ðŸ™‹ðŸ»ðŸ™‹ðŸ»â€â™€ï¸", callback_data="istiyorum")
                        keyboard.add(callback_button)
#
                        await bot.send_message(konum, random.choice([
                            f'Uzun mÃ¼ddÉ™t bir sÃ¶z demÉ™diyiniz Ã¼Ã§Ã¼n oyunu lÉ™ÄŸv etdim. {user} Cavab â†’ <b>{kelime}</b>',
                            f"{user} HeÃ§ nÉ™ demÉ™diyiniz Ã¼Ã§Ã¼n lÉ™ÄŸv etmÉ™li oldum ðŸ˜¢\nCavab â†’ <b>{kelime}</b>",
                        
                        
                        ]), reply_markup=keyboard)
                        oyunu_iptal_et(id)

                elif oyun_tipi == "kelimeoyunu":
                    kelime_soru_suresi = f("kelime_oyunu_sure")
                    if kelime_soru_suresi < int(time.time()) - id/zaman_hassasiyeti:
                        kelime = games_js["kelime"]



                        if str(id) == str(f(f"groups.{konum}.oyun")):
                            skorlar = f(f"games.{id}.skorlar")

                            skorlar = dict(sorted(skorlar.items(), key=lambda item: item[1]))
                            skorlar_list = list(skorlar)[::-1]

                            metin = f"""âŒ›ï¸ {round(kelime_soru_suresi/60)} dÉ™qiqÉ™lik vaxt bitdi!\nCavab â†’ <b>{kelime}</b>

 <b>~~<u> ðŸŽ– XAL SÄ°YAHISI ðŸŽ– </u>~~</b>
"""
                            for n, i in enumerate(skorlar_list):
                                if n + 1 == 1:
                                    metin += "ðŸ¥‡ "
                                elif n + 1 == 2:
                                    metin += "ðŸ¥ˆ "
                                elif n + 1 == 3:
                                    metin += "ðŸ¥‰ "
                                else:
                                    metin += "â–«ï¸ "

                                metin += f'<b>{n+1}.</b> {f(f"privates.{i}.first_name")} â†’ <code>{skorlar[i]:.0f}</code> puan'

                                metin += "\n"

                            keyboard = types.InlineKeyboardMarkup()
                            callback_button = types.InlineKeyboardButton(text="ðŸ”„ YenidÉ™n oyna", callback_data="kelimeoyunu")
                            keyboard.add(callback_button)
                            await bot.send_message(konum, metin, reply_markup=keyboard)

                            oyunu_iptal_et(id)
                        elif oyun_var_mi(konum) == False:
                            oyunu_iptal_et(id)
            


            except Exception as e:
                #pass
                if "blocked" in str(e) or "kicked" in str(e) or "member" in str(e):
                    oyunu_iptal_et(id)                
                elif "chat not found" in str(e):
                    oyunu_iptal_et(id)
                elif not "timed" in str(e):
                    await bot.send_message(kurucu_id, str(e)+" asdf = sonuÃ§ iptal")
                    await bot.send_message(kurucu_id, f"traceback = {get_traceback(e)}")
                    try:
                        oyunu_iptal_et(i["id"])
                    except:
                        pass

    hizlar["game_master"] = time.time() - t0



def haftalik_reset():
    now = datetime.datetime.now()

    if now.weekday() != 0: #pazar deÄŸil ise
        return
    
    if not (now.hour == 0 and now.minute == 0): # saat 00:00 deÄŸilse
        return



    while 1:
        try:
            bot.send_message(kurucu_id, "ðŸŽ° HÉ™ftÉ™lik xallar sÄ±fÄ±rlanÄ±r.")

            try:
                ww = f(f"haftalÄ±k-bilme-sayÄ±larÄ±")
                skorlar = ww
                skor = sorted(skorlar.items(), key=lambda item: item[1])[::-1][0]
                bot.send_message(skor, "ðŸŽ– Siz bu hÉ™ftÉ™ É™n yaxÅŸÄ± xalÄ± olan oyunÃ§u seÃ§ildiniz, TÉ™brik edirik!")
            except Exception as e:
                bot.send_message(kurucu_id, str(e))

            f(f"haftalÄ±k-bilme-sayÄ±larÄ±",{})
            try:
                ww = f(f"grup-haftalÄ±k-bilme-sayÄ±larÄ±")        
                skorlar = ww
                skor = sorted(skorlar.items(), key=lambda item: item[1])[::-1][0]
                bot.send_message(skor, "ðŸŽ– Siz bu hÉ™ftÉ™ É™n yaxÅŸÄ± xal toplayan qrup Ã¼Ã§Ã¼n seÃ§ildiniz!")
            except Exception as e:
                bot.send_message(kurucu_id, str(e))


            f(f"grup-haftalÄ±k-bilme-sayÄ±larÄ±",{})

            groups = f("groups").copy()
            for i in groups:
                #try:
                try:
                    i = i["id"]
                    bot.send_message(i, "ðŸŽ° HÉ™ftÉ™lik xallar sÄ±fÄ±rlanÄ±r.")
                    f(f"groups.{i}.haftalÄ±k-bilme-sayÄ±larÄ±",{})
                    f(f"groups.{i}.haftalÄ±k-toplam-bilme-sayÄ±sÄ±",0)
                except Exception as e:
                    if "chat not found" in str(e):
                        bot.send_message(kurucu_id,f"{i} Qrupu sildim, Ã§Ã¼nki sÃ¶hbÉ™t tapÄ±lmadÄ±")
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
    reset_zamani = f(f"reset-zamanı")

    # Əgər reset_zamani boşdursa və ya rəqəm deyilsə, 0 götür
    if not reset_zamani or not reset_zamani.isdigit():
        reset_zamani = "0"

    if time.time() - int(reset_zamani) > 7 * 86_400:
        haftalik_reset()
        f(f"reset-zamanı", time.time())

async def yedek_kontrol():
    yedek_zamani = f("yedek-zamanı")

    # Əgər yedek_zamani boşdursa və ya rəqəm deyilsə, 0 götür
    if not yedek_zamani or not yedek_zamani.isdigit():
        yedek_zamani = "0"

    if time.time() - int(yedek_zamani) > 3600 * 1:
        for _ in range(5):
            try:
                await telegram_yedek_al()
                break
            except Exception as e:
                pass
            

        f(f"yedek-zamanÄ±",time.time())

def kayit_silici():
    if time.time() - int(f(f"hesap_silme_zamanÄ±")) > 86_400 * 30 * 3: #her 3 ayda bir
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

            f(f"hesap_silme_zamanÄ±",time.time())
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
    print((datetime.datetime.now() + datetime.timedelta(hours=3)).strftime("%H:%M:%S")+" Æla iÅŸlÉ™yir!")
    await asyncio.gather(bot.infinity_polling(), periyodik_kontrol())


if __name__ == '__main__':
    asyncio.run(main())
cio.run(main())
