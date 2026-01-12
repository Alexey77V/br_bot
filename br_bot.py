import telebot
import requests
from telebot import types
import urllib3
import datetime
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- 1. МИКРО-СЕРВЕР ДЛЯ RENDER (УСТРАНЯЕТ ОШИБКУ PORT) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    # Render сам назначит порт, мы его подхватываем
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Запуск сервера в фоновом потоке
threading.Thread(target=run_health_server, daemon=True).start()

# --- 2. НАСТРОЙКИ БОТА ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = '8259946892:AAHISfQ5T_5fjxUWb5mp86d8xo3xiAF_z3M'
API_URL = "https://blackrussia.online/api/gameservers/" 

bot = telebot.TeleBot(TOKEN)

# ВНИМАНИЕ: Вставь сюда свой ПОЛНЫЙ список из 90 серверов!
FORUM_DATA = {
    "1": ("red", "18"), "2": ("green", "19"), "3": ("blue", "133"), "4": ("yellow", "169"), 
    "5": ("orange", "246"), "6": ("purple", "286"), "7": ("lime", "326"), "8": ("pink", "368"), 
    "9": ("cherry", "409"), "10": ("black", "449"), "11": ("indigo", "492"), "12": ("white", "532"),
    "13": ("magenta", "573"), "14": ("crimson", "614"), "15": ("gold", "661"), "16": ("azure", "702"), 
    "17": ("platinum", "758"), "18": ("aqua", "817"), "19": ("gray", "858"), "20": ("ice", "927"), 
    "21": ("chilli", "967"), "22": ("choco", "1009"), "23": ("moscow", "1055"), "24": ("spb", "1097"),
    "25": ("ufa", "1140"), "26": ("sochi", "1207"), "27": ("kazan", "1249"), "28": ("samara", "1293"), 
    "29": ("rostov", "1335"), "30": ("anapa", "1375"), "31": ("ekb", "1417"), "32": ("krasnodar", "1461"), 
    "33": ("arzamas", "1503"), "34": ("novosibirsk", "1545"), "35": ("grozny", "1587"), "36": ("saratov", "1629"),
    "37": ("omsk", "1671"), "38": ("irkutsk", "1713"), "39": ("volgograd", "1759"), "40": ("voronezh", "1801"), 
    "41": ("belgorod", "1843"), "42": ("makhachkala", "1885"), "43": ("vladikavkaz", "1927"), "44": ("vladivostok", "1969"), 
    "45": ("kaliningrad", "2011"), "46": ("chelyabinsk", "2053"), "47": ("krasnoyarsk", "2095"), "48": ("cheboksary", "2137"),
    "49": ("khabarovsk", "2179"), "50": ("perm", "2221"), "51": ("tula", "2263"), "52": ("ryazan", "2305"), 
    "53": ("murmansk", "2347"), "54": ("penza", "2389"), "55": ("kursk", "2431"), "56": ("arkhangelsk", "2473"), 
    "57": ("orenburg", "2517"), "58": ("kirov", "2518"), "59": ("kemerovo", "2599"), "60": ("tyumen", "2641"),
    "61": ("tolyatti", "2683"), "62": ("ivanovo", "2716"), "63": ("stavropol", "2748"), "64": ("smolensk", "2780"), 
    "65": ("pskov", "2812"), "66": ("bryansk", "2844"), "67": ("orel", "2876"), "68": ("yaroslavl", "2908"), 
    "69": ("barnaul", "2940"), "70": ("lipetsk", "2972"), "71": ("ulyanovsk", "3004"), "72": ("yakutsk", "3036"),
    "73": ("tambov", "3290"), "74": ("bratsk", "3325"), "75": ("astrakhan", "3360"), "76": ("chita", "3395"), 
    "77": ("kostroma", "3430"), "78": ("vladimir", "3465"), "79": ("kaluga", "3500"), "80": ("novgorod", "3536"),
    "81": ("taganrog", "3571"), "82": ("vologda", "3606"), "83": ("tver", "3647"), "84": ("tomsk", "3709"), 
    "85": ("izhevsk", "3748"), "86": ("surgut", "3781"), "87": ("podolsk", "3818"), "88": ("magadan", "3913"), 
    "89": ("cherepovets", "3948"), "90": ("norilsk", "3986")
}

def get_data():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, headers=headers, timeout=20, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data.get('msg', data) if isinstance(data, dict) else data
    except: return None

def format_all_servers(servers):
    if not servers: return "❌ Ошибка загрузки данных."
    text = "🖥 **BLACK RUSSIA - Онлайн**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
    total = 0
    for s in servers:
        s_id = str(s.get('id'))
        name_str = s.get('name', '???').upper()
        online = s.get('online', 0)
        max_p = 1300 if s.get('max_players', 1300) <= 1000 else s.get('max_players', 1300)
        total += online
        status = "🔴" if online >= (max_p * 0.95) else "🟢"
        
        forum_info = FORUM_DATA.get(s_id)
        if forum_info:
            slug, f_id = forum_info
            url = f"https://forum.blackrussia.online/forums/Сервер-№{s_id}-{slug}.{f_id}/"
            server_display = f"[{name_str}]({url})"
        else: server_display = name_str
        
        text += f"{status} **{server_display}**: **{online}** / **{max_p}**\n"
        
    text += (
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"💡 *Нажмите на название сервера для перехода на форум.*\n\n"
        f"📊 **ОБЩИЙ ОНЛАЙН СЕРВЕРОВ:** `{total:,}` **игроков**"
    )
    return text

def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔄 Обновить", callback_data="refresh"),
        types.InlineKeyboardButton("🔝 ТОП-10", callback_data="show_top")
    )
    markup.add(types.InlineKeyboardButton("🔎 Поиск", callback_data="start_search"))
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    data = get_data()
    bot.send_message(message.chat.id, format_all_servers(data), 
                     parse_mode="Markdown", reply_markup=get_main_keyboard(), 
                     disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    data = get_data()
    if call.data == "refresh":
        try:
            bot.edit_message_text(format_all_servers(data), call.message.chat.id, call.message.message_id, 
                                  parse_mode="Markdown", reply_markup=get_main_keyboard(), 
                                  disable_web_page_preview=True)
        except: pass
        bot.answer_callback_query(call.id, "✅ Обновлено")
    elif call.data == "show_top":
        sorted_list = sorted(data, key=lambda x: x.get('online', 0), reverse=True)
        text = "🔝 **ТОП-10 СЕРВЕРОВ**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
        for i, s in enumerate(sorted_list[:10], 1):
            text += f"{i}. 🏆 **{s.get('name')}**: **{s.get('online')}**\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                              parse_mode="Markdown", reply_markup=get_main_keyboard())
    elif call.data == "start_search":
        msg = bot.send_message(call.message.chat.id, "🔢 **Введите номер сервера (1-90):**")
        bot.register_next_step_handler(msg, execute_search)

def execute_search(message):
    user_input = message.text.strip()
    if not user_input.isdigit(): return
    data = get_data()
    server = next((s for s in data if str(s.get('id')) == user_input), None)
    if server:
        name_str = server.get('name', '???').upper()
        online = server.get('online', 0)
        max_p = 1300 if server.get('max_players', 1300) <= 1000 else server.get('max_players', 1300)
        forum_info = FORUM_DATA.get(user_input)
        server_display = name_str
        link_str = ""
        if forum_info:
            slug, f_id = forum_info
            url = f"https://forum.blackrussia.online/forums/Сервер-№{user_input}-{slug}.{f_id}/"
            server_display = f"[{name_str}]({url})"
            link_str = f"\n\n🔗 [Открыть раздел на форуме]({url})"
        res = (f"📍 **Сервер #{user_input} — {server_display}**\n\n"
               f"👤 Онлайн: **{online}** / **{max_p}**\n"
               f"📊 Нагрузка: **{int((online/max_p)*100)}%**{link_str}")
        bot.send_message(message.chat.id, res, parse_mode="Markdown", 
                         reply_markup=get_main_keyboard(), disable_web_page_preview=True)

if __name__ == "__main__":
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] >>> БОТ И ВЕБ-СЕРВЕР ДЛЯ RENDER ЗАПУЩЕНЫ!")
    bot.polling(none_stop=True)
