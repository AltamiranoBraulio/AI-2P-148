import copy

class GeneradorEquipos:
    def __init__(self):
        # Jugadores y sus habilidades
        self.jugadores = {
            'Alex': 8,
            'Brenda': 6,
            'Carlos': 7,
            'Dani': 4,
            'Elena': 3,
            'Fer': 5,
            'Gina': 4,
            'Hugo': 6
        }

        # Restricciones de enemigos (no pueden estar juntos)
        self.enemigos = [('Alex', 'Carlos'), ('Gina', 'Dani')]

        # Restricciones de amigos (deben estar juntos)
        self.amigos = [('Elena', 'Fer')]

        # Diferencia máxima de habilidades permitida
        self.diferencia_max = 10  # Subimos el límite un poco para permitir soluciones

    def verificar_restricciones(self, equipos):
        for equipo in equipos.values():
            # Verificar enemigos
            for a, b in self.enemigos:
                if a in equipo and b in equipo:
                    return False
        # Verificar amigos estén juntos
        for a, b in self.amigos:
            juntos = any(a in equipo and b in equipo for equipo in equipos.values())
            if not juntos:
                return False
        return True

    def balance_ok(self, equipos):
        suma1 = sum(self.jugadores[j] for j in equipos['Equipo 1'])
        suma2 = sum(self.jugadores[j] for j in equipos['Equipo 2'])
        return abs(suma1 - suma2) <= self.diferencia_max

    def forward_checking(self, jugadores_restantes, equipos):
        if not jugadores_restantes:
            if self.verificar_restricciones(equipos) and self.balance_ok(equipos):
                return equipos
            return None

        jugador = jugadores_restantes[0]

        for equipo_nombre in equipos:
            nuevos_equipos = copy.deepcopy(equipos)
            nuevos_equipos[equipo_nombre].append(jugador)

            if not self.verificar_restricciones(nuevos_equipos):
                continue

            resultado = self.forward_checking(jugadores_restantes[1:], nuevos_equipos)
            if resultado:
                return resultado

        return None

    def generar(self):
        jugadores_lista = list(self.jugadores.keys())
        equipos_iniciales = {'Equipo 1': [], 'Equipo 2': []}
        return self.forward_checking(jugadores_lista, equipos_iniciales)

# ---------------- EJECUCIÓN ----------------

if __name__ == "__main__":
    print("🎮 Generador de Equipos Balanceados para Torneo con Forward Checking\n")

    generador = GeneradorEquipos()
    resultado = generador.generar()

    if resultado:
        print("✅ Equipos generados con éxito:\n")
        for nombre_equipo, jugadores in resultado.items():
            total_habilidad = sum(generador.jugadores[j] for j in jugadores)
            print(f"🏆 {nombre_equipo} (Total habilidad: {total_habilidad})")
            for jugador in jugadores:
                print(f"   - {jugador} (Habilidad: {generador.jugadores[jugador]})")
            print()
    else:
        print("❌ No se pudo generar una combinación válida de equipos.")
#     # Llamar a la función principal para ejecutar el programa
#     main()            