"""
Turn Manager - Gestisce i turni di combattimento
"""

from typing import List, Union, Optional
from models.character import Character
from combat.enemy import Enemy


class Combatant:
    """Wrapper per unificare Character e Enemy"""
    
    def __init__(self, entity: Union[Character, Enemy], is_player: bool):
        """
        Inizializza un combattente
        
        Args:
            entity: Character o Enemy
            is_player: True se è un personaggio giocatore
        """
        self.entity = entity
        self.is_player = is_player
        self.name = entity.name if hasattr(entity, 'name') else "Unknown"
    
    def is_alive(self) -> bool:
        """Controlla se il combattente è vivo"""
        return self.entity.is_alive
    
    def __str__(self) -> str:
        return f"{'[PLAYER]' if self.is_player else '[ENEMY]'} {self.name}"


class TurnManager:
    """Gestisce l'ordine e l'esecuzione dei turni"""
    
    def __init__(self, players: List[Character], enemy: Enemy):
        """
        Inizializza il turn manager
        
        Args:
            players: Lista dei personaggi giocatori
            enemy: Nemico da combattere
        """
        self.players = players
        self.enemy = enemy
        
        # Crea la lista dei turni: [P1, P2, Nemico]
        self.turn_order = self._initialize_turn_order()
        self.current_turn_index = 0
        self.round_number = 1
    
    def _initialize_turn_order(self) -> List[Combatant]:
        """
        Inizializza l'ordine dei turni
        
        Returns:
            Lista di Combatant nell'ordine di turno
        """
        turn_order = []
        
        # Aggiungi tutti i giocatori
        for player in self.players:
            turn_order.append(Combatant(player, is_player=True))
        
        # Aggiungi il nemico
        turn_order.append(Combatant(self.enemy, is_player=False))
        
        return turn_order
    
    def get_current_combatant(self) -> Optional[Combatant]:
        """
        Ottiene il combattente del turno corrente
        
        Returns:
            Combatant corrente o None se combattimento finito
        """
        if not self.is_battle_active():
            return None
        
        # Salta combattenti morti
        while True:
            combatant = self.turn_order[self.current_turn_index]
            
            if combatant.is_alive():
                return combatant
            
            # Se morto, passa al prossimo
            self.next_turn()
            
            # Previeni loop infiniti se tutti sono morti
            if not self.is_battle_active():
                return None
    
    def next_turn(self):
        """Passa al turno successivo"""
        self.current_turn_index += 1
        
        # Se abbiamo completato un round, ricomincia
        if self.current_turn_index >= len(self.turn_order):
            self.current_turn_index = 0
            self.round_number += 1
    
    def is_battle_active(self) -> bool:
        """
        Verifica se la battaglia è ancora attiva
        
        Returns:
            True se la battaglia continua
        """
        # Controlla se almeno un giocatore è vivo
        players_alive = any(p.is_alive for p in self.players)
        
        # Controlla se il nemico è vivo
        enemy_alive = self.enemy.is_alive
        
        # La battaglia continua se entrambe le parti hanno almeno un combattente vivo
        return players_alive and enemy_alive
    
    def get_battle_status(self) -> dict:
        """
        Ottiene lo stato della battaglia
        
        Returns:
            Dizionario con lo stato completo
        """
        return {
            'round': self.round_number,
            'current_turn': self.current_turn_index,
            'total_turns': len(self.turn_order),
            'players_alive': sum(1 for p in self.players if p.is_alive),
            'enemy_alive': self.enemy.is_alive,
            'battle_active': self.is_battle_active()
        }
    
    def get_alive_players(self) -> List[Character]:
        """Ritorna la lista dei giocatori vivi"""
        return [p for p in self.players if p.is_alive]
    
    def get_alive_combatants(self) -> List[Combatant]:
        """Ritorna la lista di tutti i combattenti vivi"""
        return [c for c in self.turn_order if c.is_alive()]
    
    def reset(self):
        """Reset del turn manager (nuovo combattimento)"""
        self.current_turn_index = 0
        self.round_number = 1
        self.turn_order = self._initialize_turn_order()
    
    def __str__(self) -> str:
        status = "ACTIVE" if self.is_battle_active() else "ENDED"
        return f"TurnManager(Round {self.round_number}, Status: {status})"