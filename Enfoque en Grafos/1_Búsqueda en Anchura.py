from collections import deque

red social= {
    'Tú': ['Ana', 'Juan', 'Luis'],
    'Ana': ['Tú', 'Carlos'],
    'Juan': ['Tú', 'Mario'],
    'Luis': ['Tú', 'Marta'],
    'Carlos': ['Ana', 'Pedro'],
    'Mario': ['Juan'],
    'Marta': ['Luis', 'Famoso'],  # ¡Marta conoce al famoso!
    'Pedro': ['Carlos'],
    'Famoso': ['Marta']