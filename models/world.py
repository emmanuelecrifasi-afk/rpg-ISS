"""
Modello del Mondo di Gioco - Gestisce mappe e celle
"""

import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from enum import Enum


class CellType(Enum):
    """Tipi di cella della mappa"""
    EMPTY = 0       # Cella vuota, percorribile
    WALL = 1        # Muro, blocca il movimento
    DANGER = 2      # Cella pericolosa, trigger nemico
    START = 3       # Punto di partenza
    EXIT = 4        # Uscita/obiettivo
    TREASURE = 5    # Tesoro/oggetto


class World:
    """Classe che rappresenta il mondo di gioco"""
    
    def __init__(self, grid: List[List[int]] = None, name: str = "Dungeon"):
        """
        Inizializza il mondo
        
        Args:
            grid: Matrice della mappa (lista di liste)
            name: Nome del mondo/dungeon
        """
        self.name = name
        self.grid = grid if grid else [[0, 0], [0, 0]]
        self.width = len(self.grid[0]) if self.grid else 0
        self.height = len(self.grid) if self.grid else 0
        
        # Trova la posizione di START se presente
        self.start_position = self._find_cell_type(CellType.START)
    
    def get_cell(self, x: int, y: int) -> Optional[int]:
        """
        Ottiene il tipo di cella alle coordinate specificate
        
        Args:
            x: Coordinata X (colonna)
            y: Coordinata Y (riga)
            
        Returns:
            Tipo di cella o None se fuori dai limiti
        """
        if not self.is_valid_position(x, y):
            return None
        return self.grid[y][x]
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Verifica se una posizione è valida (dentro i limiti)
        
        Args:
            x: Coordinata X
            y: Coordinata Y
            
        Returns:
            True se la posizione è valida
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_walkable(self, x: int, y: int) -> bool:
        """
        Verifica se una cella è percorribile
        
        Args:
            x: Coordinata X
            y: Coordinata Y
            
        Returns:
            True se la cella è percorribile
        """
        cell = self.get_cell(x, y)
        if cell is None:
            return False
        
        # I muri (WALL) non sono percorribili
        return cell != CellType.WALL.value
    
    def get_cell_type_name(self, x: int, y: int) -> str:
        """
        Ottiene il nome del tipo di cella
        
        Args:
            x: Coordinata X
            y: Coordinata Y
            
        Returns:
            Nome del tipo di cella
        """
        cell = self.get_cell(x, y)
        if cell is None:
            return "OUT_OF_BOUNDS"
        
        cell_names = {
            CellType.EMPTY.value: "EMPTY",
            CellType.WALL.value: "WALL",
            CellType.DANGER.value: "DANGER",
            CellType.START.value: "START",
            CellType.EXIT.value: "EXIT",
            CellType.TREASURE.value: "TREASURE"
        }
        
        return cell_names.get(cell, "UNKNOWN")
    
    def _find_cell_type(self, cell_type: CellType) -> Optional[Tuple[int, int]]:
        """
        Trova la prima occorrenza di un tipo di cella
        
        Args:
            cell_type: Tipo di cella da cercare
            
        Returns:
            Tupla (x, y) o None se non trovata
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == cell_type.value:
                    return (x, y)
        return None
    
    def to_dict(self) -> Dict:
        """Converte il mondo in un dizionario"""
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "grid": self.grid
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'World':
        """
        Crea un World da un dizionario
        
        Args:
            data: Dizionario con i dati del mondo
            
        Returns:
            Istanza di World
        """
        return cls(
            grid=data.get("grid", []),
            name=data.get("name", "Dungeon")
        )
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'World':
        """
        Carica un mondo da file JSON
        
        Args:
            filepath: Percorso del file JSON
            
        Returns:
            Istanza di World
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Map file not found: {filepath}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def save_to_file(self, filepath: str) -> None:
        """
        Salva il mondo in un file JSON
        
        Args:
            filepath: Percorso del file JSON
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def print_map(self, player_pos: Optional[Tuple[int, int]] = None) -> str:
        """
        Genera una rappresentazione testuale della mappa
        
        Args:
            player_pos: Posizione del giocatore (x, y) opzionale
            
        Returns:
            Stringa con la mappa visualizzata
        """
        symbols = {
            CellType.EMPTY.value: ".",
            CellType.WALL.value: "#",
            CellType.DANGER.value: "!",
            CellType.START.value: "S",
            CellType.EXIT.value: "E",
            CellType.TREASURE.value: "$"
        }
        
        lines = []
        lines.append(f"=== {self.name} ({self.width}x{self.height}) ===")
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if player_pos and player_pos == (x, y):
                    row.append("@")  # Simbolo del giocatore
                else:
                    cell_value = self.grid[y][x]
                    row.append(symbols.get(cell_value, "?"))
            lines.append(" ".join(row))
        
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return f"World(name='{self.name}', size={self.width}x{self.height})"