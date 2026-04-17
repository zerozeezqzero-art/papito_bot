#lib
import sqlite3
from datetime import datetime, timedelta
import re
import json
import random

def get_current_time():
    return datetime.utcnow()

class Capybara_Controller:
    def __init__(self, message):
        self.us = message.from_user.username or message.from_user.first_name or str(message.from_user.id)
        self.conn = sqlite3.connect('capy.db')
        self.cursor = self.conn.cursor()
        self.admin_id = 1404725120
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', str(self.us))
        if safe and safe[0].isdigit():
            safe = 'user_' + safe
        self.usern = safe
        self.images = {
           
            'mangomons' : {
                'basic_mango' : 'mangomons/mangomon_basic.png',
                'epic_mango' : 'mangomons/mangomon_epic.png',
                'mythic_mango' : 'mangomons/mangomon_mythic.png',
                'legendary_mango' : 'mangomons/mangomon_legendary.png'
            },

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
            'capy_leader_board': 'capy_baras/capy_bara_leader.png',
            "capy_pokormlena" : 'capy_baras/capy_bara_pokormlena.jpg',
            'capy_shop' : 'capy_baras/capy_shop.jpg',
            "capy_fish" : 'capy_baras/capy_bara_ulov.png'
        }
        
        self.shop_items = {
            1: {'name': 'Яблоко🍎', 'price': 50, 'emoji': '🍎', 'description': 'Ускоряет кормление на 1 минуту'},
            2: {'name': 'Арбуз🍉', 'price': 100, 'description': 'Даёт +2 уровня сразу'},
            3: {'name': 'Лотерейный билет🎲', 'price': 45, 'description': 'Случайный приз от 0 до 100 токенов'},
            4: {'name': 'Обычная удочка🎣', 'price': 100, 'description': 'Разблокируют рыбалку'},
            5: {'name': 'Эпическая удочка🎣', 'price': 500, 'description': 'Шанс на эпическую рыбу'},
            6: {'name': 'Легендарная удочка🎣', 'price': 1000, 'description': 'Шанс на легендарную рыбу'},
        }


        self.fishs = {
            'basic': [  
                {'name': 'Плотва🐟', 'min': 3, 'max': 10},
                {'name': 'Окунь🐠', 'min': 5, 'max': 11},
                {'name': 'Карась🐡', 'min': 8, 'max': 12},
                {'name': 'Щука🐟', 'min': 10, 'max': 13}
            ],
            'epic': [
                {'name': 'Лосось🍣', 'min': 13, 'max': 30},
                {'name': 'Сом🐋', 'min': 15, 'max': 31},
                {'name': 'Форель🎣', 'min': 20, 'max': 32}
            ],
            'legendary': [
                {'name': 'Тунец🍣', 'min': 50, 'max': 100},
                {'name': 'Акула🦈', 'min': 75, 'max': 100}
            ]}
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
        now = get_current_time()
        cooldown = 5
        self.cursor.execute(f'SELECT inventory FROM "{self.usern}"')
        result = self.cursor.fetchone()
        if result:
            inventory = json.loads(result[0])
            if 'Яблоко🍎' in inventory:
                cooldown = cooldown - 1
        
        self.cursor.execute(f'SELECT mangomon FROM "{self.usern}"')
        result = self.cursor.fetchone()
        if result and result[0]:
            if 'basic_mango' in result[0]:
                cooldown = cooldown - 2
            elif 'epic_mango' in result[0]:
                cooldown = cooldown - 2
            elif 'mythic_mango' in result[0]:
                cooldown = cooldown - 2
            elif 'legendary_mango' in result[0]:
                cooldown = cooldown - 3


        if cooldown < 1:
            cooldown = 1


        self.cursor.execute(f'SELECT last_feed FROM "{self.usern}"')
        last_feed_result = self.cursor.fetchone()  
        if not last_feed_result or not last_feed_result[0]:
            self.cursor.execute(f'UPDATE "{self.usern}" SET last_feed = ?', (now,))
            self.conn.commit()
            return ('🐹 Капибара готова к кормлению!', True)
        
        last_feed = last_feed_result[0]
        if isinstance(last_feed, str):
            last_feed = datetime.fromisoformat(last_feed)
        
        if hasattr(last_feed, 'tzinfo') and last_feed.tzinfo is not None:
            last_feed = last_feed.replace(tzinfo=None)

        if now - last_feed < timedelta(minutes=cooldown):
            next_feed_time = last_feed + timedelta(minutes=cooldown)
            time_left = next_feed_time - now
            minutes_left = int(time_left.total_seconds() // 60)
            seconds_left = int(time_left.total_seconds() % 60)
            return (f'🐹 Капибара сыта! Приходи через {minutes_left} мин {seconds_left} сек 🕐', False)
        else:
            self.cursor.execute(f'SELECT mangomon FROM "{self.usern}"')
            result = self.cursor.fetchone()
            papito_tok_za_lvl = 25
            if result and result[0]:
                if result[0] == 'legendary_mango':
                    papito_tok_za_lvl = 125
            
            self.cursor.execute(f'''UPDATE "{self.usern}" 
                            SET capybara_level = capybara_level + 1, 
                            last_feed = ?,
                            papito_tokens = papito_tokens + {papito_tok_za_lvl}''', (now,))
            self.conn.commit()
            return (f'✅ Капибара покормлена! +1 уровень и + {papito_tok_za_lvl} токенов 🎉🐹💰', True)


    def create_capy(self):
        time = get_current_time()
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
                inventory TEXT DEFAULT '[]',
                mangomon TEXT,
                troll_mode INTEGER DEFAULT 0,
                fishing_cooldown TIMESTAMP,
                watermelon_cooldown TIMESTAMP
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
            
            
            self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens - ?', (pay,))
            self.conn.commit()
            return (f"✅ {item} куплен!", True)
        
        
        elif item_id == 2:
            self.cursor.execute(f'SELECT watermelon_cooldown FROM "{self.usern}"')
            t = self.cursor.fetchone()
            if t[0]:
                last_time = datetime.fromisoformat(t[0])
                if get_current_time() - last_time < timedelta(seconds=30):
                    wait = int(30 - (get_current_time() - last_time).total_seconds())
                    return (f'⏰ Подожди {wait} секунд!', False)
            self.cursor.execute(f'UPDATE "{self.usern}" SET watermelon_cooldown = ?', (get_current_time(),))
            self.cursor.execute(f'UPDATE "{self.usern}" SET capybara_level = capybara_level + 2')
           
           
            self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens - ?', (pay,))
            self.conn.commit()
            return (f"✅ {item} куплен!", True)
            
        elif item_id == 3:
            self.cursor.execute(f'SELECT mangomon FROM "{self.usern}"')
            result = self.cursor.fetchone()
            random_tok = random.randint(1, 101)
            
            if result and result[0]:
                if result[0] == 'mythic_mango':
                    random_tok = random.randint(25, 101)
            self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens + ?', (random_tok,))
            
            
            self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens - ?', (pay,))
            self.conn.commit()
            
            
            return (f"✅ {item} куплен! +{random_tok} токенов", True)
        elif item_id in [4,5,6]:
            self.cursor.execute(f'SELECT inventory FROM "{self.usern}"')
            result = self.cursor.fetchone()
            inventory = json.loads(result[0]) if result and result[0] else []
            if item in inventory:
                return ('Вы уже купили это', False)
            inventory = [i for i in inventory if 'удочка' not in i.lower()]
            inventory.append(item)
            self.cursor.execute(f'UPDATE "{self.usern}" SET inventory = ?', (json.dumps(inventory),))
            
            
            self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens - ?', (pay,))
            self.conn.commit()
            return (f"✅ {item} куплен!", True)

        
    @capybara_req_dec
    def buy_mangomon(self,message):
        self.cursor.execute(f'SELECT papito_tokens FROM "{self.usern}"')
        result = self.cursor.fetchone()
        if result[0] < 350:
            return (f"Не хватает папито токенов! Нужно 350 а у тебя {result[0]}",False)
        else:
            mango_types = list(self.images['mangomons'].keys())
            chances = [45, 30, 15, 10]
            new_mango = random.choices(mango_types,weights=chances,k=1)[0]
            self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens - 350')
            self.cursor.execute(f'UPDATE "{self.usern}" SET mangomon =?',(new_mango,))
            if new_mango == 'epic_mango':
                self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens + 500')
            elif new_mango == 'mythic_mango':
                self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens + 500')     
            self.conn.commit()
            return (new_mango,True)
        

    @capybara_req_dec
    def get_my_mango(self,message):
        self.cursor.execute(f'SELECT mangomon FROM "{self.usern}"')
        result = self.cursor.fetchone()
        if result and result[0]:
            return (result[0],True)
        else:
            return ('У вас нету мангомона! Купите командой /buy_mango',False)
        
    @capybara_req_dec
    def tapalka(self,message):
        self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens + 1')
        self.conn.commit()
        return (f'🪙 +1 папито токен!', True)
    

    @capybara_req_dec
    def dudosing(self,message,target_username):
        self.cursor.execute(f'UPDATE "{target_username}" SET troll_mode = 1')
        self.conn.commit()
        return (f'🤡 Режим троллинга включён для @{target_username}!', True)


    @capybara_req_dec
    def stop_dudosing(self,message,target_username):
        self.cursor.execute(f'UPDATE "{target_username}" SET troll_mode = 0')
        self.conn.commit()
        return (f'✅ Режим троллинга выключен для @{target_username}', True)


    def is_troll_mode(self, username):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{username}'")
        if not self.cursor.fetchone():
            return False
        else:
            self.cursor.execute(f'SELECT troll_mode FROM "{username}"')
            result = self.cursor.fetchone()
            return result and result[0] == 1
        
    @capybara_req_dec 
    def fishing(self, message):
        now = get_current_time()
        
        # Проверяем инвентарь
        self.cursor.execute(f'SELECT inventory FROM "{self.usern}"')
        result = self.cursor.fetchone()
        inventory = json.loads(result[0]) if result and result[0] else []
        
        if 'Обычная удочка🎣' in inventory:
            rarity = 'basic'
            cd = 20
        elif 'Эпическая удочка🎣' in inventory:
            rarity = random.choices(['basic', 'epic'], weights=[40, 60])[0]
            cd = 10
        elif 'Легендарная удочка🎣' in inventory:
            rarity = random.choices(['basic', 'epic', 'legendary'], weights=[25, 40, 35])[0]
            cd = 5
        else:
            return (f'❌ У тебя нет удочки! Купи в магазине /shop', False)
        
        # Проверяем кулдаун
        self.cursor.execute(f'SELECT fishing_cooldown FROM "{self.usern}"')
        r = self.cursor.fetchone()
        
        if r and r[0]:
            last_time = datetime.fromisoformat(r[0]) if isinstance(r[0], str) else r[0]
            seconds_passed = (now - last_time).total_seconds()
            
            if seconds_passed < cd:
                wait = int(cd - seconds_passed)
                return (f'⏰ Подожди {wait} секунд перед следующей рыбалкой!', False)
        
        # Рыбалка
        fish_data = random.choice(self.fishs[rarity])
        fish_name = fish_data['name']
        fish_reward = random.randint(fish_data['min'], fish_data['max'])
        
        self.cursor.execute(f'UPDATE "{self.usern}" SET papito_tokens = papito_tokens + ?', (fish_reward,))
        self.cursor.execute(f'UPDATE "{self.usern}" SET fishing_cooldown = ?', (now,))
        self.conn.commit()
        
        return (f'🎣 Ты поймал: {fish_name}!\n💰 +{fish_reward} токенов!', True)