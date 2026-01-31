from core.pygame_game_engine import PygameGameEngine


def main():
    """Avvia il gioco con interfaccia Pygame"""

    # Inizializza e avvia il game engine
    engine = PygameGameEngine()
    engine.run()


if __name__ == "__main__":
    main()