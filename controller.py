import sqlite3
from datetime import datetime, timedelta
import re
import json
import random
import os

def get_current_time():
    # Прибавляем 3 часа для сервера Bot Host.ru
    # Если на сервере переменная окружения BOTHOST не установлена, проверяем по hostname
    if 'BOTHOST' in os.environ or (os.environ.get('HOSTNAME', '').lower().find('bot_host') != -1):
        return datetime.now() + timedelta(hours=3)
    return datetime.now()

class Capybara_Controller:
    def __init__(self, message):
        self.us = message.from_user.username or message.from_user.first_name or str(message.from_user.id)
        self.conn = sqlite3.connect('capy.db')
        self.cursor = self.conn.cursor()

        safe = re.sub(r'[^a-zA-Z0-9_]', '_', str(self.us))
        if safe and safe[0].isdigit():
            safe = 'user_' + safe
        self.usern = safe

        self.images = {
            'random_capy': [
                "capy_baras/capy_bara.png",
                "capy_baras/capy_bara2.jpg",
                "capy_baras/capy_bara3.jpg",
                "capy_baras/capy_bara4.jpg",
                "capy_baras/capy_bara5.jpg",
                "capy_baras/capy_bara6.jpg"
            ],
            'greeting_photo': "capy_baras/capy_bara_greet.jpg",
            'help_photo': "capy_baras/capy_bara_help.jpg",
            'gpt_photo': 'capy_baras/capy_bara_gpt.jpg',
            'capy_born': 'capy_baras/capy_bara_rodilas.jpg',
            'capy_eat': 'capy_baras/capybara_eat.jpg',
            'capy_leader_board': 'capy_baras/capy_bara_leader.png'
        }
        
        self.shop_items = {
            1: {'name': 'Яблоко🍎', 'price': 50, 'emoji': '🍎', 'description': 'Ускоряет кормление на 1 минуту'},
            2: {'name': 'Арбуз🍉', 'price': 100, 'description': 'Даёт +2 уровня сразу'},
            3: {'name': 'Лотерейный билет🎲', 'price': 25, 'description': 'Случайный приз от 0 до 100 токенов'},
        }

    def capybara_req_dec(func):
        def wrapper(self, message, *args, **kwargs):
            temp_capy = Capybara_Controller(message)
            temp_capy.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{temp_capy.usern}'")
            result = temp_capy.cursor.fetchone()
            if result:
                return func(self, message, *args, **kwargs)
            else:
                return (None, 'No_capy')
        return wrapper

    @capybara_req_dec
    def feed_capy(self, message):
        cooldown = 5
        'aaaa'
        self.cursor.execute(f'SELECT inventory FROM "{self.usern}"')
        result = self.cursor.fetchone()
        if result:
            inventory = json.loads(result[0])
            if 'Яблоко🍎' in inventory:
                cooldown = 4

        now = get_current_time()

        self.cursor.execute(f'SELECT last_feed FROM "{self.usern}"')
        last_feed_result = self.cursor.fetchone()
        if not last_feed_result or not last_feed_result[0]:
            # Если нет last_feed, создаём новую запись
            self.cursor.execute(f'''UPDATE "{self.usern}" SET last_feed = ?''', (now,))
            self.conn.commit()
            return ('🐹 Капибара готова к кормлению!', True)
        
        last_feed = last_feed_result[0]
        if isinstance(last_feed, str):
            last_feed = datetime.fromisoformat(last_feed)

        if now - last_feed < timedelta(minutes=cooldown):
            next_feed_time = last_feed + timedelta(minutes=cooldown)
            time_left = next_feed_time - now
            minutes_left = int(time_left.total_seconds() // 60)
            seconds_left = int(time_left.total_seconds() % 60)
            return (f'🐹 Капибара сыта и довольна! Приходи покормить её через {minutes_left} мин {seconds_left} сек 🕐', False)
        else:
            self.cursor.execute(f'''UPDATE "{self.usern}" 
                            SET capybara_level = capybara_level + 1, 
                            last_feed = ?,
                            papito_tokens = papito_tokens + 25''', (now,))
            self.conn.commit()
            return ('✅ Капибара покормлена! +1 уровень и +25 токенов 🎉🐹💰', True)

    def create_capy(self):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.usern}'")
        table_exists = self.cursor.fetchone()
        if table_exists:
            self.cursor.execute(f'SELECT COUNT(*) FROM "{self.usern}"')
            count = self.cursor.fetchone()[0]
            if count > 0:
                return False
            self.cursor.execute(f'''INSERT INTO "{self.usern}" 
                                (capybara_name, last_feed) VALUES (?, ?)''',
                                (f"Capy_{self.usern}", get_current_time()))
            self.conn.commit()
            return True
        else:
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{self.usern}" (
                                    capybara_name TEXT,
                                    capybara_level INTEGER DEFAULT 1,
                                    last_feed TIMESTAMP,
                                    papito_tokens INTEGER DEFAULT 1,
                                    inventory TEXT DEFAULT '[]'
                                )''')
            self.cursor.execute(f'''INSERT INTO "{self.usern}" 
                                (capybara_name, last_feed) VALUES (?, ?)''',
                                (f"Capy_{self.usern}", get_current_time()))
            self.conn.commit()
            return True

    def close(self):
        self.conn.close()

    @capybara_req_dec
    def get_capy_level(self, message):
        self.cursor.execute(f'SELECT capybara_level FROM "{self.usern}"')
        result = self.cursor.fetchone()
        if result:
            return (result[0], True)
        else:
            return (None, False)

    def leaderboard(self):
        self.cursor.execute(f'SELECT name FROM sqlite_master WHERE type="table"')
        names = [item[0] for item in self.cursor.fetchall() if not item[0].startswith('sqlite_')]
        values = []

        for table_name in names:
            self.cursor.execute(f'SELECT capybara_level FROM "{table_name}"')
            level_result = self.cursor.fetchone()
            if level_result:
                values.append(level_result[0])

        leaderboard_dict = dict(zip(names, values))

        if not leaderboard_dict:
            return "🏆 Пока нет капибар для рейтинга! Создайте первую капибару командой /capybara"

        sorted_items = sorted(leaderboard_dict.items(), key=lambda x: x[1], reverse=True)
        top_items = sorted_items[:10]

        lines = ["🏆 **ТОП КАПИБАР** 🏆", ""]

        for i, (name, level) in enumerate(top_items, 1):
            if i == 1:
                medal = "👑"
                name = f"**{name}**"
            elif i == 2:
                medal = "🥈"
            elif i == 3:
                medal = "🥉"
            else:
                medal = "📊"
            lines.append(f"{medal} {i}. {name} — {level} lvl")

        lines.append("")
        lines.append(f"📊 Всего капибар: {len(leaderboard_dict)}")
        return "\n".join(lines)

    @capybara_req_dec
    def get_papito_tokens(self, message):
        self.cursor.execute(f'SELECT papito_tokens FROM "{self.usern}"')
        result = self.cursor.fetchone()
        if result:
            return (f'🪙 У вас {result[0]} папито токенов!', True)
        return ('❌ Ошибка получения токенов', False)

    @capybara_req_dec
    def purchase_item(self, message, item_id):
        if item_id not in self.shop_items:
            return ('❌ Товар не найден!', False)
            
        pay = self.shop_items[item_id]['price']
        item = self.shop_items[item_id]['name']
        
        self.cursor.execute(f'SELECT papito_tokens FROM "{self.usern}"')
        tokens_result = self.cursor.fetchone()
        tokens = tokens_result[0] if tokens_result else 0
        
        if tokens < pay:
            return (f"❌ Не хватает токенов! Нужно {pay}, у тебя {tokens}", False)
        
        if item_id == 1:
            self.cursor.execute(f'SELECT inventory FROM "{self.usern}"')
            result = self.cursor.fetchone()
            inventory = json.loads(result[0]) if result and result[0] else []
            if item in inventory:
                return ('Вы уже купили это', False)
            inventory.append(item)
            self.cursor.execute(f'UPDATE "{self.usern}" SET inventory = ?', (json.dumps(inventory),))
        elif item_id == 2:
            self.cursor.execute(f'UPDATE "{self.usern}" SET capybara_level = capybara_level + 2')
        elif item_id == 3:
            random_tok = random.randint(1, 101)
            self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens + ?', (random_tok,))
            self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens - ?', (pay,))
            self.conn.commit()
            return (f"✅ {item} куплен! +{random_tok} токенов", True)
        
        self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens - ?', (pay,))
        self.conn.commit()
        return (f"✅ {item} куплен!", True)