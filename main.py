from core.game_engine import GameEngine


def main():
    """Funzione principale che avvia il gioco"""
    
    # Inizializza e avvia il game engine
    engine = GameEngine()
    engine.run()


if __name__ == "__main__":
    main()