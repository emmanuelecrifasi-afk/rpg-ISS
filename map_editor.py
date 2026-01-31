import json
from pathlib import Path


def create_default_map():
    """Crea la mappa di default"""
    return {
        "name": "Dungeon Tutorial",
        "width": 5,
        "height": 5,
        "grid": [
            [3, 0, 1, 0, 0],  # 3 = START
            [0, 1, 1, 2, 0],  # 2 = DANGER (nemico)
            [0, 0, 0, 1, 0],  # 0 = EMPTY (percorribile)
            [1, 0, 2, 0, 5],  # 1 = WALL (muro)
            [0, 0, 1, 0, 4]   # 4 = EXIT, 5 = TREASURE
        ]
    }


def create_dungeon_large():
    """Crea un dungeon più grande"""
    return {
        "name": "Grande Dungeon",
        "width": 10,
        "height": 10,
        "grid": [
            [3, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 2, 0, 1],
            [1, 0, 1, 5, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 0, 0, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 1, 1, 0, 2, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 4, 1]
        ]
    }


def create_arena():
    """Crea un'arena di combattimento"""
    return {
        "name": "Arena dei Campioni",
        "width": 7,
        "height": 7,
        "grid": [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 2, 0, 1],
            [1, 0, 0, 3, 0, 0, 1],
            [1, 0, 2, 0, 2, 0, 1],
            [1, 0, 0, 5, 0, 0, 1],
            [1, 1, 1, 4, 1, 1, 1]
        ]
    }


def create_maze():
    """Crea un labirinto"""
    return {
        "name": "Labirinto Oscuro",
        "width": 8,
        "height": 8,
        "grid": [
            [3, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 2, 1],
            [1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 5, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 0, 4, 1]
        ]
    }


def save_map(map_data, filename):
    """Salva una mappa in un file JSON"""
    maps_dir = Path("data/maps")
    maps_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = maps_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(map_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Mappa salvata in: {filepath}")


def print_map_legend():
    """Stampa la legenda dei simboli"""
    print("\n📖 LEGENDA CELLE:")
    print("  0 = EMPTY      (Cella vuota, percorribile)")
    print("  1 = WALL       (Muro, blocca il movimento)")
    print("  2 = DANGER     (Cella pericolosa, nemico)")
    print("  3 = START      (Punto di partenza)")
    print("  4 = EXIT       (Uscita/Obiettivo)")
    print("  5 = TREASURE   (Tesoro/Oggetto)")
    print()


def print_map_preview(map_data):
    """Stampa un'anteprima della mappa"""
    symbols = {
        0: '.',
        1: '#',
        2: '!',
        3: 'S',
        4: 'E',
        5: '$'
    }
    
    print(f"\n📍 {map_data['name']} ({map_data['width']}x{map_data['height']})")
    print("─" * (map_data['width'] * 2 + 1))
    
    for row in map_data['grid']:
        print(' '.join(symbols.get(cell, '?') for cell in row))
    
    print("─" * (map_data['width'] * 2 + 1))


def create_custom_map_interactive():
    """Crea una mappa personalizzata in modo interattivo"""
    print("\n🎨 CREAZIONE MAPPA PERSONALIZZATA")
    print("=" * 50)
    
    # Input dimensioni
    while True:
        try:
            width = int(input("\nLarghezza mappa (5-15): "))
            if 5 <= width <= 15:
                break
            print("❌ Inserisci un valore tra 5 e 15")
        except ValueError:
            print("❌ Inserisci un numero valido")
    
    while True:
        try:
            height = int(input("Altezza mappa (5-15): "))
            if 5 <= height <= 15:
                break
            print("❌ Inserisci un valore tra 5 e 15")
        except ValueError:
            print("❌ Inserisci un numero valido")
    
    name = input("\nNome mappa: ").strip() or "Mappa Personalizzata"
    
    # Crea griglia vuota
    grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Aggiungi START (obbligatorio)
    print("\n📍 Posiziona lo START (punto di partenza)")
    start_x = int(input(f"  X (0-{width-1}): "))
    start_y = int(input(f"  Y (0-{height-1}): "))
    grid[start_y][start_x] = 3
    
    # Aggiungi EXIT (obbligatorio)
    print("\n🚪 Posiziona l'EXIT (uscita)")
    exit_x = int(input(f"  X (0-{width-1}): "))
    exit_y = int(input(f"  Y (0-{height-1}): "))
    grid[exit_y][exit_x] = 4
    
    print("\n✅ Mappa base creata!")
    print("💡 Suggerimento: Edita il file JSON manualmente per aggiungere")
    print("   muri (1), nemici (2) e tesori (5)")
    
    return {
        "name": name,
        "width": width,
        "height": height,
        "grid": grid
    }


def main():
    """Menu principale"""
    print("=" * 60)
    print("  🗺️  MAP EDITOR - RPG GAME")
    print("=" * 60)
    
    print_map_legend()
    
    print("MAPPE PREDEFINITE:")
    print("  1. Dungeon Tutorial (5x5) - Mappa base")
    print("  2. Grande Dungeon (10x10) - Più grande e complessa")
    print("  3. Arena dei Campioni (7x7) - Combattimenti multipli")
    print("  4. Labirinto Oscuro (8x8) - Percorso tortuoso")
    print("  5. Crea mappa personalizzata")
    print("  0. Esci")
    print()
    
    while True:
        choice = input("Scegli un'opzione (0-5): ").strip()
        
        if choice == "0":
            print("\n👋 Arrivederci!")
            break
        
        elif choice == "1":
            map_data = create_default_map()
            print_map_preview(map_data)
            save_map(map_data, "map_01.json")
        
        elif choice == "2":
            map_data = create_dungeon_large()
            print_map_preview(map_data)
            save_map(map_data, "map_large.json")
        
        elif choice == "3":
            map_data = create_arena()
            print_map_preview(map_data)
            save_map(map_data, "map_arena.json")
        
        elif choice == "4":
            map_data = create_maze()
            print_map_preview(map_data)
            save_map(map_data, "map_maze.json")
        
        elif choice == "5":
            map_data = create_custom_map_interactive()
            print_map_preview(map_data)
            filename = input("\nNome file (es. my_map.json): ").strip()
            if not filename.endswith('.json'):
                filename += '.json'
            save_map(map_data, filename)
        
        else:
            print("❌ Scelta non valida")
        
        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()