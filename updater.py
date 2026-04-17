import sqlite3

# НАСТРОЙКИ — МЕНЯЙ ЗДЕСЬ
columns_to_add = [
    {'name': 'watermelon_cooldown', 'type': 'TIMESTAMP'},
    {'name': 'fishing_cooldown', 'type': 'TIMESTAMP'},
]

def add_columns():
    conn = sqlite3.connect('capy.db')
    cursor = conn.cursor()
    
    # Получаем все таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("🔄 Добавление колонок во все таблицы...")
    print("-" * 50)
    
    for table in tables:
        table_name = table[0]
        
        # Пропускаем служебные таблицы SQLite
        if table_name.startswith('sqlite_'):
            continue
        
        print(f"\n📋 Таблица: {table_name}")
        
        # Получаем существующие колонки
        cursor.execute(f'PRAGMA table_info("{table_name}")')
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        for col in columns_to_add:
            col_name = col['name']
            col_type = col['type']
            
            if col_name not in existing_columns:
                try:
                    cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN {col_name} {col_type}')
                    conn.commit()
                    print(f"  ✅ Добавлена {col_name} ({col_type})")
                except Exception as e:
                    print(f"  ❌ Ошибка при добавлении {col_name}: {e}")
            else:
                print(f"  ⏭️ {col_name} уже есть")
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("🎉 Готово!")

if __name__ == "__main__":
    add_columns()