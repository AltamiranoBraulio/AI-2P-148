import sqlite3

# 🧠 Establecemos la conexión a la base de datos SQLite
# Si la base de datos no existe, se crea automáticamente
conn = sqlite3.connect('empleados.db')

# 📚 Creamos un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# 💻 Ejemplo: Creamos una tabla "empleados" (si no existe)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        puesto TEXT NOT NULL,
        salario REAL NOT NULL
    )
''')

# 💻 Insertamos algunos datos de ejemplo en la tabla empleados
cursor.execute("INSERT INTO empleados (nombre, puesto, salario) VALUES ('Juan', 'Gerente', 55000)")
cursor.execute("INSERT INTO empleados (nombre, puesto, salario) VALUES ('Ana', 'Desarrolladora', 45000)")
cursor.execute("INSERT INTO empleados (nombre, puesto, salario) VALUES ('Carlos', 'Diseñador', 40000)")
cursor.execute("INSERT INTO empleados (nombre, puesto, salario) VALUES ('Laura', 'Tester', 38000)")

# 💾 Guardamos los cambios en la base de datos
conn.commit()

# 🔎 Recuperamos datos de la tabla empleados
cursor.execute("SELECT * FROM empleados")

# 💬 Mostramos los resultados
print("Datos de empleados:")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Nombre: {row[1]}, Puesto: {row[2]}, Salario: {row[3]}")

# 🧹 Cerramos la conexión a la base de datos
conn.close()
