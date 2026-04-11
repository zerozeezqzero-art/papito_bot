import sqlite3
from datetime import datetime, timedelta
import os

def fix_local_database():
    # Проверяем, существует ли файл БД
    if not os.path.exists('capy.db'):
        print("❌ Файл capy.db не найден в текущей папке!")
        return
    
    # Делаем резервную копию
    import shutil
    shutil.copy2('capy.db', 'capy.db.backup')
    print("✅ Создана резервная копия: capy.db.backup")
    
    conn = sqlite3.connect('capy.db')
    cursor = conn.cursor()
    
    # Получаем все таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    updated_count = 0
    now = datetime.now()
    
    for table in tables:
        table_name = table[0]
        if table_name.startswith('sqlite_'):
            continue
        
        try:
            # Устанавливаем last_feed на 5 минут назад
            new_time = now - timedelta(minutes=5)
            
            cursor.execute(f'UPDATE "{table_name}" SET last_feed = ?', (new_time,))
            updated_count += 1
            print(f"✅ Обновлён {table_name} -> {new_time}")
        except Exception as e:
            print(f"❌ Ошибка в {table_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Готово! Обновлено {updated_count} таблиц.")
    print("📁 Файл capy.db обновлён. Резервная копия: capy.db.backup")

if __name__ == "__main__":
    fix_local_database()