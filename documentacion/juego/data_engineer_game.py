"""
╔══════════════════════════════════════════════════════════════════════════╗
║                      DATA ENGINEER: THE GAME                             ║
║                                                                          ║
║  Un simulador de Data Engineering donde aprendes mientras te diviertes  ║
╚══════════════════════════════════════════════════════════════════════════╝

CÓMO JUGAR:
1. Ejecuta: python data_engineer_game.py
2. Completa misiones, gana XP, sube de nivel
3. Desbloquea tecnologías y proyectos
4. Tu progreso se guarda automáticamente
5. ¡Conviértete en Senior Data Engineer!
"""

import json
import math
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# ============================================================================
# SISTEMA DE COLORES (Cross-platform)
# ============================================================================


class Colors:
    """Colores para terminal (cross-platform)."""

    # Colores básicos
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Colores de texto
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Colores de fondo
    BG_BLACK = "\033[40m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"

    # Estilos especiales
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"

    @staticmethod
    def disable():
        """Desactiva colores (para Windows antiguo)."""
        Colors.RESET = ""
        Colors.BOLD = ""
        # ... (desactivar todos)


# ============================================================================
# MOTOR DEL JUEGO
# ============================================================================


class GameEngine:
    """Motor principal del juego."""

    SAVE_FILE = "game_save.json"

    # Niveles y XP requerido
    XP_PER_LEVEL = [
        0,
        100,
        250,
        450,
        700,
        1000,
        1400,
        1900,
        2500,
        3200,  # 0-9
        4000,
        5000,
        6200,
        7600,
        9200,
        11000,
        13000,
        15500,
        18500,
        22000,  # 10-19
    ]

    # Rangos profesionales
    RANKS = [
        {"level": 0, "name": "Trainee", "emoji": "🎓"},
        {"level": 3, "name": "Junior Data Engineer", "emoji": "💼"},
        {"level": 7, "name": "Data Engineer", "emoji": "🔧"},
        {"level": 12, "name": "Senior Data Engineer", "emoji": "⭐"},
        {"level": 17, "name": "Lead Data Engineer", "emoji": "👑"},
        {"level": 20, "name": "Data Architect", "emoji": "🏆"},
    ]

    def __init__(self):
        """Inicializar el motor del juego."""
        self.player_data = self.load_or_create_save()
        self.current_module = 1
        self.current_tema = 1

    def load_or_create_save(self) -> Dict[str, Any]:
        """Cargar partida guardada o crear una nueva."""
        if os.path.exists(self.SAVE_FILE):
            with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return self.create_new_game()

    def create_new_game(self) -> Dict[str, Any]:
        """Crear una nueva partida."""
        return {
            "player_name": "",
            "level": 1,
            "xp": 0,
            "total_xp_earned": 0,
            "current_module": 1,
            "current_tema": 1,
            "completed_missions": [],
            "unlocked_achievements": [],
            "unlocked_technologies": ["Python", "Git"],
            "stats": {
                "lines_of_code": 0,
                "tests_passed": 0,
                "bugs_fixed": 0,
                "projects_completed": 0,
                "study_hours": 0,
                "exercises_solved": 0,
            },
            "created_at": datetime.now().isoformat(),
            "last_played": datetime.now().isoformat(),
            "play_time_minutes": 0,
        }

    def save_game(self):
        """Guardar el progreso del jugador."""
        self.player_data["last_played"] = datetime.now().isoformat()
        with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.player_data, f, indent=2, ensure_ascii=False)

    def get_current_rank(self) -> Dict:
        """Obtener el rango profesional actual."""
        level = self.player_data["level"]
        for i in range(len(self.RANKS) - 1, -1, -1):
            if level >= self.RANKS[i]["level"]:
                return self.RANKS[i]
        return self.RANKS[0]

    def get_next_rank(self) -> Dict:
        """Obtener el siguiente rango a desbloquear."""
        level = self.player_data["level"]
        for rank in self.RANKS:
            if level < rank["level"]:
                return rank
        return self.RANKS[-1]  # Ya es max rank

    def calculate_xp_for_next_level(self) -> int:
        """Calcular XP necesario para el siguiente nivel."""
        level = self.player_data["level"]
        if level >= len(self.XP_PER_LEVEL):
            return 999999  # Max level
        return self.XP_PER_LEVEL[level]

    def add_xp(self, amount: int, reason: str = ""):
        """Añadir XP al jugador."""
        self.player_data["xp"] += amount
        self.player_data["total_xp_earned"] += amount

        print(f"\n{Colors.GREEN}+{amount} XP{Colors.RESET}", end="")
        if reason:
            print(f" {Colors.CYAN}({reason}){Colors.RESET}", end="")
        print()

        # Check level up
        while self.check_level_up():
            self.level_up()

        self.save_game()

    def check_level_up(self) -> bool:
        """Verificar si el jugador sube de nivel."""
        xp_needed = self.calculate_xp_for_next_level()
        return self.player_data["xp"] >= xp_needed

    def level_up(self):
        """Subir de nivel al jugador."""
        old_level = self.player_data["level"]
        self.player_data["level"] += 1
        new_level = self.player_data["level"]

        # Restar XP usado
        xp_used = self.XP_PER_LEVEL[old_level]
        self.player_data["xp"] -= xp_used

        # Animación de level up
        self.clear_screen()
        self.print_level_up_animation(old_level, new_level)

        # Check rank up
        old_rank = self.get_rank_at_level(old_level)
        new_rank = self.get_current_rank()

        if old_rank["name"] != new_rank["name"]:
            self.rank_up(old_rank, new_rank)

    def get_rank_at_level(self, level: int) -> Dict:
        """Obtener el rango en un nivel específico."""
        for i in range(len(self.RANKS) - 1, -1, -1):
            if level >= self.RANKS[i]["level"]:
                return self.RANKS[i]
        return self.RANKS[0]

    def rank_up(self, old_rank: Dict, new_rank: Dict):
        """Promoción de rango."""
        time.sleep(1)
        print(f"\n{Colors.BOLD}{Colors.YELLOW}╔{'═' * 68}╗{Colors.RESET}")
        print(
            f"{Colors.BOLD}{Colors.YELLOW}║{' ' * 22}🎉 ¡PROMOCIÓN! 🎉{' ' * 23}║{Colors.RESET}"
        )
        print(f"{Colors.BOLD}{Colors.YELLOW}╚{'═' * 68}╝{Colors.RESET}")
        print(f"\n{Colors.CYAN}Has sido promovido de:{Colors.RESET}")
        print(f"  {old_rank['emoji']} {old_rank['name']}")
        print(f"{Colors.GREEN}  ⬇️{Colors.RESET}")
        print(f"  {new_rank['emoji']} {Colors.BOLD}{new_rank['name']}{Colors.RESET}")
        input(f"\n{Colors.YELLOW}Presiona ENTER para continuar...{Colors.RESET}")

    def print_level_up_animation(self, old_level: int, new_level: int):
        """Animación de subida de nivel."""
        print(f"\n{Colors.BOLD}{Colors.GREEN}╔{'═' * 68}╗{Colors.RESET}")
        print(
            f"{Colors.BOLD}{Colors.GREEN}║{' ' * 23}🎊 LEVEL UP! 🎊{' ' * 24}║{Colors.RESET}"
        )
        print(f"{Colors.BOLD}{Colors.GREEN}╚{'═' * 68}╝{Colors.RESET}")
        print(f"\n{Colors.YELLOW}  Nivel {old_level} → Nivel {new_level}{Colors.RESET}")

        # Stats bonus
        print(f"\n{Colors.CYAN}  ✨ Recompensas desbloqueadas:{Colors.RESET}")
        print(f"     • Nuevas misiones disponibles")
        print(f"     • Mayor complejidad de proyectos")

        if new_level % 5 == 0:
            print(
                f"     • {Colors.YELLOW}¡Tecnología nueva desbloqueada!{Colors.RESET}"
            )

        input(f"\n{Colors.GREEN}Presiona ENTER para continuar...{Colors.RESET}")

    def unlock_achievement(self, achievement_id: str, name: str, description: str):
        """Desbloquear un logro."""
        if achievement_id not in self.player_data["unlocked_achievements"]:
            self.player_data["unlocked_achievements"].append(achievement_id)
            print(f"\n{Colors.YELLOW}🏆 LOGRO DESBLOQUEADO: {name}{Colors.RESET}")
            print(f"   {description}")
            self.add_xp(50, "Logro desbloqueado")
            time.sleep(2)

    def update_stat(self, stat_name: str, amount: int = 1):
        """Actualizar una estadística del jugador."""
        if stat_name in self.player_data["stats"]:
            self.player_data["stats"][stat_name] += amount
            self.save_game()

    def clear_screen(self):
        """Limpiar la pantalla."""
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self):
        """Imprimir cabecera del juego."""
        rank = self.get_current_rank()
        xp_current = self.player_data["xp"]
        xp_needed = self.calculate_xp_for_next_level()
        xp_progress = (xp_current / xp_needed) * 100 if xp_needed > 0 else 100

        print(f"{Colors.BOLD}{Colors.CYAN}╔{'═' * 68}╗{Colors.RESET}")
        print(
            f"{Colors.BOLD}{Colors.CYAN}║{' ' * 18}DATA ENGINEER: THE GAME{' ' * 27}║{Colors.RESET}"
        )
        print(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * 68}╝{Colors.RESET}")

        print(
            f"\n{Colors.YELLOW}👤 {self.player_data['player_name']}{Colors.RESET}",
            end="",
        )
        print(f" | {rank['emoji']} {Colors.BOLD}{rank['name']}{Colors.RESET}", end="")
        print(f" | Nivel {Colors.GREEN}{self.player_data['level']}{Colors.RESET}")

        # Barra de XP
        bar_length = 40
        filled = int((xp_progress / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"XP: [{Colors.GREEN}{bar}{Colors.RESET}] {xp_current}/{xp_needed}")
        print("─" * 70)

    def show_dashboard(self):
        """Mostrar dashboard del jugador."""
        self.clear_screen()
        self.print_header()

        stats = self.player_data["stats"]
        rank = self.get_current_rank()
        next_rank = self.get_next_rank()

        print(f"\n{Colors.BOLD}📊 TUS ESTADÍSTICAS{Colors.RESET}\n")

        # Columna 1: Stats de código
        print(f"{Colors.CYAN}💻 CÓDIGO:{Colors.RESET}")
        print(f"   Líneas escritas:        {stats['lines_of_code']:,}")
        print(f"   Tests pasados:          {stats['tests_passed']:,}")
        print(f"   Bugs corregidos:        {stats['bugs_fixed']:,}")

        # Columna 2: Stats de progreso
        print(f"\n{Colors.CYAN}📚 PROGRESO:{Colors.RESET}")
        print(f"   Proyectos completados:  {stats['projects_completed']}")
        print(f"   Ejercicios resueltos:   {stats['exercises_solved']}")
        print(f"   Horas de estudio:       {stats['study_hours']}")

        # XP Total
        print(f"\n{Colors.CYAN}⭐ EXPERIENCIA:{Colors.RESET}")
        print(f"   XP Total ganado:        {self.player_data['total_xp_earned']:,}")
        print(
            f"   Logros desbloqueados:   {len(self.player_data['unlocked_achievements'])}"
        )

        # Próximo rank
        if rank["name"] != next_rank["name"]:
            levels_needed = next_rank["level"] - self.player_data["level"]
            print(f"\n{Colors.YELLOW}🎯 PRÓXIMA PROMOCIÓN:{Colors.RESET}")
            print(f"   {next_rank['emoji']} {next_rank['name']}")
            print(f"   Faltan {levels_needed} niveles")
        else:
            print(f"\n{Colors.GOLD}🏆 ¡HAS ALCANZADO EL RANGO MÁXIMO!{Colors.RESET}")

        # Tecnologías desbloqueadas
        print(f"\n{Colors.CYAN}🔧 TECNOLOGÍAS DESBLOQUEADAS:{Colors.RESET}")
        techs = self.player_data["unlocked_technologies"]
        for i in range(0, len(techs), 4):
            row = techs[i : i + 4]
            print(f"   {' | '.join(row)}")

        input(f"\n{Colors.YELLOW}Presiona ENTER para volver...{Colors.RESET}")


# ============================================================================
# SISTEMA DE MISIONES
# ============================================================================


class Mission:
    """Clase base para misiones."""

    def __init__(
        self,
        mission_id: str,
        title: str,
        description: str,
        xp_reward: int,
        difficulty: str,
    ):
        self.mission_id = mission_id
        self.title = title
        self.description = description
        self.xp_reward = xp_reward
        self.difficulty = difficulty

    def start(self, game: GameEngine):
        """Iniciar la misión."""
        game.clear_screen()
        game.print_header()

        diff_color = {
            "Fácil": Colors.GREEN,
            "Medio": Colors.YELLOW,
            "Difícil": Colors.RED,
        }.get(self.difficulty, Colors.WHITE)

        print(f"\n{Colors.BOLD}{Colors.CYAN}📋 NUEVA MISIÓN{Colors.RESET}")
        print(f"\n{Colors.BOLD}{self.title}{Colors.RESET}")
        print(
            f"Dificultad: {diff_color}{self.difficulty}{Colors.RESET} | Recompensa: {Colors.GREEN}+{self.xp_reward} XP{Colors.RESET}"
        )
        print(f"\n{self.description}")
        print("\n" + "─" * 70)

    def execute(self, game: GameEngine) -> bool:
        """Ejecutar la misión (override en subclases)."""
        raise NotImplementedError

    def complete(self, game: GameEngine):
        """Completar la misión."""
        game.player_data["completed_missions"].append(self.mission_id)
        game.add_xp(self.xp_reward, f"Misión completada: {self.title}")
        game.save_game()


# ============================================================================
# MÓDULO 1 - TEMA 1: ESTADÍSTICA
# ============================================================================


class Modulo1Tema1:
    """Módulo 1, Tema 1: Estadística Descriptiva."""

    @staticmethod
    def start(game: GameEngine):
        """Iniciar el Tema 1 del Módulo 1."""
        game.clear_screen()
        game.print_header()

        print(f"\n{Colors.BOLD}{Colors.MAGENTA}╔{'═' * 68}╗{Colors.RESET}")
        print(
            f"{Colors.BOLD}{Colors.MAGENTA}║{' ' * 10}MÓDULO 1: FUNDAMENTOS DE PROGRAMACIÓN{' ' * 21}║{Colors.RESET}"
        )
        print(
            f"{Colors.BOLD}{Colors.MAGENTA}║{' ' * 10}TEMA 1: Estadística Descriptiva con Python{' ' * 16}║{Colors.RESET}"
        )
        print(f"{Colors.BOLD}{Colors.MAGENTA}╚{'═' * 68}╝{Colors.RESET}")

        print(f"\n{Colors.CYAN}📖 HISTORIA:{Colors.RESET}")
        print(
            """
¡Bienvenido a DataFlow Industries!

Eres un nuevo Data Engineer y hoy es tu primer día. Tu jefa, María,
te ha asignado al equipo de análisis de datos de negocios.

"Tu primera tarea será analizar datos de ventas y tiempos de respuesta
de nuestra API. Necesito que entiendas estadística descriptiva: media,
mediana, desviación estándar... lo básico para un Data Engineer."

¿Estás listo para tu primera misión?
        """
        )

        input(
            f"\n{Colors.YELLOW}Presiona ENTER para aceptar la misión...{Colors.RESET}"
        )

        # Primera misión: Tutorial de Media
        Modulo1Tema1.mission_01_calcular_media(game)

    @staticmethod
    def mission_01_calcular_media(game: GameEngine):
        """Misión 1: Calcular la media de ventas."""
        mission = Mission(
            mission_id="m1t1_mission_01",
            title="Calcular la Media de Ventas",
            description="""
María te pasa los datos de ventas de la última semana:

    Ventas: [145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40]

Tu tarea: Calcular la venta promedio (media) para saber si cumplimos
nuestro objetivo de 170€ por día.

RECORDATORIO: Media = Suma de valores / Cantidad de valores
            """,
            xp_reward=100,
            difficulty="Fácil",
        )

        mission.start(game)

        ventas = [145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40]

        print(f"\n{Colors.CYAN}📝 EJERCICIO:{Colors.RESET}")
        print(f"Calcula la media de: {ventas}")
        print(f"\nObjetivo: > 170€")

        intentos = 3
        while intentos > 0:
            try:
                respuesta = float(
                    input(f"\n{Colors.YELLOW}Tu respuesta (en €): {Colors.RESET}")
                )

                media_correcta = sum(ventas) / len(ventas)

                if abs(respuesta - media_correcta) < 0.5:  # Tolerancia de 0.50€
                    print(f"\n{Colors.GREEN}✅ ¡CORRECTO!{Colors.RESET}")
                    print(f"\nLa media es {media_correcta:.2f}€")
                    print(f"Objetivo: 170€")
                    print(
                        f"Resultado: {Colors.GREEN}¡CUMPLIMOS EL OBJETIVO!{Colors.RESET} ✓"
                    )

                    mission.complete(game)
                    game.update_stat("exercises_solved")
                    game.update_stat("lines_of_code", 10)

                    input(
                        f"\n{Colors.YELLOW}Presiona ENTER para continuar...{Colors.RESET}"
                    )

                    # Siguiente misión
                    Modulo1Tema1.mission_02_calcular_mediana(game)
                    return
                else:
                    intentos -= 1
                    if intentos > 0:
                        print(
                            f"\n{Colors.RED}❌ Incorrecto. Te quedan {intentos} intentos.{Colors.RESET}"
                        )
                        print(
                            f"{Colors.CYAN}Pista: Suma todos los valores y divide por 7{Colors.RESET}"
                        )
                    else:
                        print(
                            f"\n{Colors.RED}❌ Se acabaron los intentos.{Colors.RESET}"
                        )
                        print(f"La respuesta correcta era: {media_correcta:.2f}€")
                        print(
                            f"\n{Colors.YELLOW}💡 No te preocupes, puedes reintentar.{Colors.RESET}"
                        )
                        input(f"\nPresiona ENTER para volver al menú...")
                        return

            except ValueError:
                print(f"{Colors.RED}Por favor ingresa un número válido.{Colors.RESET}")

    @staticmethod
    def mission_02_calcular_mediana(game: GameEngine):
        """Misión 2: Calcular la mediana."""
        mission = Mission(
            mission_id="m1t1_mission_02",
            title="Detectar Outliers con la Mediana",
            description="""
María: "¡Buen trabajo! Ahora un desafío más complejo."

Un sensor de temperatura reportó estos valores:

    Temperaturas: [22, 23, 21, 24, 22, 500, 23]

Uno de los sensores falló y reportó 500°C (¡imposible!).

Tu tarea: Calcular la MEDIANA para obtener un valor más representativo
que no se vea afectado por el outlier.

RECORDATORIO:
1. Ordena los valores
2. Toma el del medio
            """,
            xp_reward=150,
            difficulty="Medio",
        )

        mission.start(game)

        temperaturas = [22, 23, 21, 24, 22, 500, 23]

        print(f"\n{Colors.CYAN}📝 EJERCICIO:{Colors.RESET}")
        print(f"Calcula la mediana de: {temperaturas}")
        print(
            f"\n{Colors.YELLOW}Pista: Ordena primero, luego toma el valor central{Colors.RESET}"
        )

        intentos = 3
        while intentos > 0:
            try:
                respuesta = float(
                    input(f"\n{Colors.YELLOW}Tu respuesta (en °C): {Colors.RESET}")
                )

                temps_ordenadas = sorted(temperaturas)
                mediana_correcta = temps_ordenadas[len(temps_ordenadas) // 2]

                if abs(respuesta - mediana_correcta) < 0.1:
                    print(f"\n{Colors.GREEN}✅ ¡EXCELENTE!{Colors.RESET}")
                    print(f"\nOrdenado: {temps_ordenadas}")
                    print(f"Mediana: {mediana_correcta}°C")
                    print(f"Media: {sum(temperaturas) / len(temperaturas):.1f}°C")
                    print(
                        f"\n{Colors.CYAN}La mediana ({mediana_correcta}°C) representa mucho mejor"
                    )
                    print(
                        f"la temperatura real que la media (80.7°C) afectada por el outlier.{Colors.RESET}"
                    )

                    mission.complete(game)
                    game.update_stat("exercises_solved")
                    game.update_stat("bugs_fixed", 1)

                    # Logro
                    if (
                        "first_outlier_detected"
                        not in game.player_data["unlocked_achievements"]
                    ):
                        game.unlock_achievement(
                            "first_outlier_detected",
                            "Detective de Datos",
                            "Detectaste tu primer outlier usando la mediana",
                        )

                    input(
                        f"\n{Colors.YELLOW}Presiona ENTER para ver tus stats y volver al menú...{Colors.RESET}"
                    )
                    game.show_dashboard()
                    return
                else:
                    intentos -= 1
                    if intentos > 0:
                        print(
                            f"\n{Colors.RED}❌ Incorrecto. Te quedan {intentos} intentos.{Colors.RESET}"
                        )
                    else:
                        print(f"\n{Colors.RED}Se acabaron los intentos.{Colors.RESET}")
                        print(f"Respuesta: {mediana_correcta}°C")
                        input(f"\nPresiona ENTER...")
                        return

            except ValueError:
                print(f"{Colors.RED}Por favor ingresa un número válido.{Colors.RESET}")


# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================


def main_menu(game: GameEngine):
    """Menú principal del juego."""
    while True:
        game.clear_screen()
        game.print_header()

        print(f"\n{Colors.BOLD}🎮 MENÚ PRINCIPAL{Colors.RESET}\n")
        print(
            f"  1. 🚀 Continuar Aventura (Módulo {game.player_data['current_module']}, Tema {game.player_data['current_tema']})"
        )
        print(f"  2. 📊 Ver Dashboard y Estadísticas")
        print(f"  3. 🏆 Ver Logros")
        print(f"  4. 📚 Biblioteca de Aprendizaje")
        print(f"  5. ⚙️  Configuración")
        print(f"  6. 💾 Guardar y Salir")

        choice = input(f"\n{Colors.YELLOW}Elige una opción (1-6): {Colors.RESET}")

        if choice == "1":
            # Continuar aventura
            if (
                game.player_data["current_module"] == 1
                and game.player_data["current_tema"] == 1
            ):
                Modulo1Tema1.start(game)

        elif choice == "2":
            game.show_dashboard()

        elif choice == "3":
            show_achievements(game)

        elif choice == "4":
            show_library(game)

        elif choice == "5":
            show_settings(game)

        elif choice == "6":
            game.save_game()
            print(f"\n{Colors.GREEN}✅ Progreso guardado.{Colors.RESET}")
            print(
                f"{Colors.CYAN}¡Hasta pronto, {game.player_data['player_name']}!{Colors.RESET}\n"
            )
            sys.exit(0)

        else:
            print(f"{Colors.RED}Opción inválida.{Colors.RESET}")
            time.sleep(1)


def show_achievements(game: GameEngine):
    """Mostrar logros."""
    game.clear_screen()
    game.print_header()
    print(f"\n{Colors.BOLD}🏆 TUS LOGROS{Colors.RESET}\n")

    achievements_unlocked = game.player_data["unlocked_achievements"]

    if len(achievements_unlocked) == 0:
        print(f"{Colors.YELLOW}Aún no has desbloqueado logros.{Colors.RESET}")
        print(f"{Colors.CYAN}¡Completa misiones para desbloquearlos!{Colors.RESET}")
    else:
        for i, ach in enumerate(achievements_unlocked, 1):
            print(f"  {i}. 🏅 {ach}")

    input(f"\n{Colors.YELLOW}Presiona ENTER para volver...{Colors.RESET}")


def show_library(game: GameEngine):
    """Biblioteca de aprendizaje."""
    game.clear_screen()
    game.print_header()
    print(f"\n{Colors.BOLD}📚 BIBLIOTECA DE APRENDIZAJE{Colors.RESET}\n")
    print(f"{Colors.CYAN}Aquí podrás repasar conceptos aprendidos:{Colors.RESET}\n")
    print(f"  1. Teoría de Estadística Descriptiva")
    print(f"  2. Ejemplos Resueltos")
    print(f"  3. Cheat Sheet de Fórmulas")
    print(f"  4. Volver")

    choice = input(f"\n{Colors.YELLOW}Elige una opción: {Colors.RESET}")

    if choice == "1":
        print(f"\n{Colors.CYAN}📖 Abriendo teoría...{Colors.RESET}")
        print(f"Consulta: modulo-01-fundamentos/tema-1-python-estadistica/01-TEORIA.md")
        input(f"\n{Colors.YELLOW}Presiona ENTER...{Colors.RESET}")


def show_settings(game: GameEngine):
    """Configuración."""
    game.clear_screen()
    game.print_header()
    print(f"\n{Colors.BOLD}⚙️  CONFIGURACIÓN{Colors.RESET}\n")
    print(f"  1. Cambiar nombre")
    print(f"  2. Resetear progreso (¡CUIDADO!)")
    print(f"  3. Volver")

    choice = input(f"\n{Colors.YELLOW}Elige una opción: {Colors.RESET}")

    if choice == "1":
        new_name = input(f"\n{Colors.CYAN}Nuevo nombre: {Colors.RESET}")
        game.player_data["player_name"] = new_name
        game.save_game()
        print(f"{Colors.GREEN}✅ Nombre actualizado.{Colors.RESET}")
        time.sleep(1)


# ============================================================================
# INICIO DEL JUEGO
# ============================================================================


def start_game():
    """Iniciar el juego."""
    game = GameEngine()

    # Si es nuevo jugador, mostrar intro
    if not game.player_data["player_name"]:
        game.clear_screen()
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 18 + "DATA ENGINEER: THE GAME" + " " * 27 + "║")
        print("╚" + "═" * 68 + "╝")
        print(f"{Colors.RESET}")

        print(
            f"\n{Colors.YELLOW}¡Bienvenido al simulador de Data Engineering más adictivo!{Colors.RESET}\n"
        )
        print("Aprende Data Engineering mientras juegas.")
        print("Completa misiones, sube de nivel, desbloquea tecnologías.\n")

        name = input(f"{Colors.CYAN}¿Cómo te llamas? {Colors.RESET}")
        game.player_data["player_name"] = name
        game.save_game()

        print(f"\n{Colors.GREEN}¡Perfecto, {name}!{Colors.RESET}")
        print(
            f"{Colors.CYAN}Tu aventura como Data Engineer comienza ahora...{Colors.RESET}\n"
        )
        time.sleep(2)

    # Menú principal
    main_menu(game)


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    try:
        start_game()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Juego interrumpido.{Colors.RESET}")
        print(
            f"{Colors.CYAN}Tu progreso ha sido guardado automáticamente.{Colors.RESET}\n"
        )
        sys.exit(0)
