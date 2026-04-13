from datetime import datetime
import functools
import sqlite3
from controller import get_current_time
import random

def log_to_file(text):
    with open('bot_log.txt', 'a',encoding='UTF-8') as f:
        f.write(f"{get_current_time()} - {text}\n")


def try_ex_deco(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            log_to_file(f"ОШИБКА в {func.__name__}: {str(e)}")
            return None
    return wrapper


def try_ex_deco_sync(func):
    """Декоратор для синхронных функций"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_to_file(f"ОШИБКА в {func.__name__}: {str(e)}")
            return None
    return wrapper









def troll_check(func):
    """Декоратор для проверки режима троллинга"""
    async def wrapper(message, *args, **kwargs):
        try:
            username = message.from_user.username
            if username:
                conn = sqlite3.connect('capy.db')
                cursor = conn.cursor()
                
                # Проверяем, есть ли таблица пользователя
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{username}'")
                if cursor.fetchone():
                    cursor.execute(f'SELECT troll_mode FROM "{username}"')
                    result = cursor.fetchone()
                    conn.close()
                    
                    # Если троллинг включён и сработал 50% шанс
                    if result and result[0] == 1:
                        if random.random() < 0.5:
                            await message.reply("❌ ОШИБКА!")
                            return
                else:
                    conn.close()
        except Exception as e:
            print(f"Ошибка в troll_check: {e}")
        return await func(message, *args, **kwargs)
    return wrapper