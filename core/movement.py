"""
Sistema di Movimento - Gestisce il movimento del party sulla mappa
"""

from typing import Tuple, Optional, Dict
from enum import Enum
from models.world import World, CellType
from models.party import Party


class Direction(Enum):
    """Direzioni di movimento"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class MovementResult:
    """Risultato di un tentativo di movimento"""
    
    def __init__(self, success: bool, new_position: Tuple[int, int], 
                 message: str, trigger: Optional[str] = None):
        """
        Inizializza il risultato del movimento
        
        Args:
            success: Se il movimento è riuscito
            new_position: Nuova posizione (x, y)
            message: Messaggio descrittivo
            trigger: Tipo di trigger attivato (es. "DANGER", "TREASURE")
        """
        self.success = success
        self.new_position = new_position
        self.message = message
        self.trigger = trigger


class MovementManager:
    """Gestisce il movimento del party sulla mappa"""
    
    # Mapping comandi -> direzioni
    COMMAND_TO_DIRECTION = {
        'w': Direction.UP,
        'a': Direction.LEFT,
        's': Direction.DOWN,
        'd': Direction.RIGHT,
        'up': Direction.UP,
        'left': Direction.LEFT,
        'down': Direction.DOWN,
        'right': Direction.RIGHT,
    }
    
    # Delta coordinate per ogni direzione
    DIRECTION_DELTAS = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0)
    }
    
    def __init__(self, world: World, start_x: int = 0, start_y: int = 0):
        """
        Inizializza il movement manager
        
        Args:
            world: Mondo di gioco
            start_x: Posizione iniziale X
            start_y: Posizione iniziale Y
        """
        self.world = world
        self.position_x = start_x
        self.position_y = start_y
        
        # Se il mondo ha una posizione START, usala
        if world.start_position:
            self.position_x, self.position_y = world.start_position
        
        # Verifica che la posizione iniziale sia valida
        if not self.world.is_walkable(self.position_x, self.position_y):
            # Trova la prima cella percorribile
            found = False
            for y in range(self.world.height):
                for x in range(self.world.width):
                    if self.world.is_walkable(x, y):
                        self.position_x, self.position_y = x, y
                        found = True
                        break
                if found:
                    break
    
    def get_position(self) -> Tuple[int, int]:
        """Ritorna la posizione corrente"""
        return (self.position_x, self.position_y)
    
    def move(self, command: str) -> MovementResult:
        """
        Muove il party in base al comando
        
        Args:
            command: Comando di movimento (w/a/s/d o up/left/down/right)
            
        Returns:
            MovementResult con il risultato del movimento
        """
        command = command.lower().strip()
        direction = self.COMMAND_TO_DIRECTION.get(command)
        
        if not direction:
            return MovementResult(
                success=False,
                new_position=self.get_position(),
                message=f"Comando di movimento non valido: '{command}'"
            )
        
        return self.move_direction(direction)
    
    def move_direction(self, direction: Direction) -> MovementResult:
        """
        Muove il party in una direzione specifica
        
        Args:
            direction: Direzione del movimento
            
        Returns:
            MovementResult con il risultato
        """
        delta_x, delta_y = self.DIRECTION_DELTAS[direction]
        new_x = self.position_x + delta_x
        new_y = self.position_y + delta_y
        
        # Verifica se la nuova posizione è valida
        if not self.world.is_valid_position(new_x, new_y):
            return MovementResult(
                success=False,
                new_position=self.get_position(),
                message="🚫 Non puoi andare oltre i confini della mappa!"
            )
        
        # Verifica collisioni con muri
        if not self.world.is_walkable(new_x, new_y):
            cell_type = self.world.get_cell_type_name(new_x, new_y)
            return MovementResult(
                success=False,
                new_position=self.get_position(),
                message=f"🧱 C'è un muro! Non puoi passare."
            )
        
        # Movimento riuscito - aggiorna posizione
        old_x, old_y = self.position_x, self.position_y
        self.position_x = new_x
        self.position_y = new_y
        
        # Controlla trigger della nuova cella
        cell_value = self.world.get_cell(new_x, new_y)
        trigger = None
        message = f"Ti sei mosso da ({old_x}, {old_y}) a ({new_x}, {new_y})"
        
        if cell_value == CellType.DANGER.value:
            trigger = "DANGER"
            message = "⚔️ PERICOLO! Hai incontrato un nemico!"
        elif cell_value == CellType.TREASURE.value:
            trigger = "TREASURE"
            message = "💎 Hai trovato un tesoro!"
        elif cell_value == CellType.EXIT.value:
            trigger = "EXIT"
            message = "🚪 Hai raggiunto l'uscita!"
        elif cell_value == CellType.START.value:
            message = "📍 Sei tornato al punto di partenza"
        
        return MovementResult(
            success=True,
            new_position=self.get_position(),
            message=message,
            trigger=trigger
        )
    
    def move_forward(self, direction: Direction) -> bool:
        """
        Muove in avanti in una direzione (metodo semplificato)
        
        Args:
            direction: Direzione del movimento
            
        Returns:
            True se il movimento è riuscito
        """
        result = self.move_direction(direction)
        return result.success
    
    def get_surrounding_cells(self) -> Dict[str, str]:
        """
        Ottiene informazioni sulle celle circostanti
        
        Returns:
            Dizionario con le celle in ogni direzione
        """
        surroundings = {}
        
        for direction, (dx, dy) in self.DIRECTION_DELTAS.items():
            check_x = self.position_x + dx
            check_y = self.position_y + dy
            
            if self.world.is_valid_position(check_x, check_y):
                cell_type = self.world.get_cell_type_name(check_x, check_y)
                surroundings[direction.value] = cell_type
            else:
                surroundings[direction.value] = "OUT_OF_BOUNDS"
        
        return surroundings
    
    def get_description(self) -> str:
        """
        Ottiene una descrizione della posizione corrente
        
        Returns:
            Stringa descrittiva
        """
        x, y = self.get_position()
        cell_type = self.world.get_cell_type_name(x, y)
        
        descriptions = {
            "EMPTY": "Ti trovi in un corridoio vuoto.",
            "START": "Sei al punto di partenza.",
            "DANGER": "Questa zona sembra pericolosa...",
            "TREASURE": "Qualcosa brilla qui!",
            "EXIT": "Vedi un'uscita davanti a te!"
        }
        
        base_desc = descriptions.get(cell_type, "Ti trovi in una zona sconosciuta.")
        
        # Aggiungi info sulle celle circostanti
        surroundings = self.get_surrounding_cells()
        warnings = []
        
        if surroundings.get('up') == 'WALL':
            warnings.append("muro a nord")
        if surroundings.get('down') == 'WALL':
            warnings.append("muro a sud")
        if surroundings.get('left') == 'WALL':
            warnings.append("muro a ovest")
        if surroundings.get('right') == 'WALL':
            warnings.append("muro a est")
        
        if warnings:
            base_desc += f" Vedi: {', '.join(warnings)}."
        
        return base_desc