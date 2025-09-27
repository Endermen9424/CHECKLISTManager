import sqlite3
from config import database

class DBManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS checklists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aircraft_name TEXT NOT NULL,
                aircraft_brand_id INTEGER NOT NULL,
                checklist TEXT NOT NULL,
                FOREIGN KEY (aircraft_brand_id) REFERENCES AircraftBrand(id)
            )
        ''')

        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS AircraftBrand (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_checklist(self, aircraft_name, aircraft_brand_name, checklist):
        # 1. AircraftBrand tablosunda marka var mı kontrol et
        self.cursor.execute('SELECT id FROM AircraftBrand WHERE name = ?', (aircraft_brand_name,))
        result = self.cursor.fetchone()

        if result:
            aircraft_brand_id = result[0]  # varsa id'yi al
        else:
            # yoksa ekle ve id'yi al
            self.cursor.execute('INSERT INTO AircraftBrand (name) VALUES (?)', (aircraft_brand_name,))
            aircraft_brand_id = self.cursor.lastrowid

        # 2. checklist tablosuna ekle
        self.cursor.execute(
            'INSERT INTO checklists (aircraft_name, aircraft_brand_id, checklist) VALUES (?, ?, ?)',
            (aircraft_name, aircraft_brand_id, checklist)
        )
        self.connection.commit()


    def get_checklists(self):
        self.cursor.execute('SELECT * FROM checklists')
        return self.cursor.fetchall()

    def delete_checklist(self, checklist_id):
        self.cursor.execute('DELETE FROM checklists WHERE id = ?', (checklist_id,))
        self.connection.commit()

    def add_brand(self, brand_name):
        self.cursor.execute('INSERT INTO AircraftBrand (name) VALUES (?)', (brand_name,))
        self.connection.commit()

    def get_brands(self):
        self.cursor.execute('SELECT * FROM AircraftBrand')
        return self.cursor.fetchall()
    
    def delete_brand(self, brand_id):
        self.cursor.execute('DELETE FROM AircraftBrand WHERE id = ?', (brand_id,))
        self.connection.commit()

    def open_checklists(self, checklist_id):
        self.cursor.execute('SELECT checklist FROM checklists WHERE id = ?', (checklist_id,))
        result = self.cursor.fetchone()

        if not result:
            return
        
        checklist_value = result[0]

        if checklist_value.startswith("http"):
            import webbrowser
            webbrowser.open(checklist_value)
        elif checklist_value.startswith("C:") or checklist_value.startswith("D:") or checklist_value.startswith("E:"):
            import os
            os.startfile(checklist_value)
        else:
            print("Desteklenmeyen checklist formatı:", checklist_value)
        #print(result[0])

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    db = DBManager(database)