import sqlite3

def add_user_id_column():
    conn = sqlite3.connect('capy.db')
    cursor = conn.cursor()
    
    # Получаем все таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    updated_count = 0
    skipped_count = 0
    
    print("🔄 Добавление колонки user_id во все таблицы...")
    print("-" * 50)
    
    for table in tables:
        table_name = table[0]
        
        # Пропускаем служебные таблицы SQLite
        if table_name.startswith('sqlite_'):
            skipped_count += 1
            continue
        
        try:
            # Проверяем, есть ли уже колонка user_id
            cursor.execute(f'PRAGMA table_info("{table_name}")')
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'user_id' not in columns:
                # Добавляем колонку
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN user_id INTEGER')
                conn.commit()
                print(f"✅ Добавлена колонка user_id в {table_name}")
                updated_count += 1
            else:
                print(f"⏭️ Колонка user_id уже есть в {table_name}")
                
        except Exception as e:
            print(f"❌ Ошибка в {table_name}: {e}")
    
    conn.close()
    
    print("-" * 50)
    print(f"\n📊 Статистика:")
    print(f"   - Добавлено колонок: {updated_count}")
    print(f"   - Пропущено служебных таблиц: {skipped_count}")
    print(f"   - Всего таблиц: {len(tables)}")
    
    if updated_count > 0:
        print("\n🎉 Готово! Колонка user_id добавлена!")
    else:
        print("\n⚠️ Колонка user_id уже есть во всех таблицах.")

if __name__ == "__main__":
    add_user_id_column()