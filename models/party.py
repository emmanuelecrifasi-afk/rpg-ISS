"""
Classe Party - Gestisce un gruppo di personaggi
"""

from typing import List, Optional
from models.character import Character


class Party:
    """Classe che rappresenta un gruppo di personaggi"""
    
    def __init__(self, characters: List[Character] = None):
        """
        Inizializza un party
        
        Args:
            characters: Lista di personaggi (opzionale)
        """
        self.characters: List[Character] = characters if characters else []
    
    def add_character(self, character: Character) -> None:
        """Aggiunge un personaggio al party"""
        self.characters.append(character)
    
    def remove_character(self, name: str) -> bool:
        """
        Rimuove un personaggio dal party per nome
        
        Returns:
            True se il personaggio è stato rimosso, False altrimenti
        """
        for i, char in enumerate(self.characters):
            if char.name.lower() == name.lower():
                self.characters.pop(i)
                return True
        return False
    
    def get_character(self, identifier: str) -> Optional[Character]:
        """
        Ottiene un personaggio per nome o alias (p1, p2, etc.)
        
        Args:
            identifier: Nome del personaggio o alias (p1, p2)
            
        Returns:
            Character se trovato, None altrimenti
        """
        # Controlla se è un alias (p1, p2, etc.)
        if identifier.lower().startswith('p') and len(identifier) == 2:
            try:
                index = int(identifier[1]) - 1
                if 0 <= index < len(self.characters):
                    return self.characters[index]
            except (ValueError, IndexError):
                pass
        
        # Cerca per nome
        for char in self.characters:
            if char.name.lower() == identifier.lower():
                return char
        
        return None
    
    def get_alive_characters(self) -> List[Character]:
        """Ritorna la lista dei personaggi vivi"""
        return [char for char in self.characters if char.is_alive]
    
    def is_party_alive(self) -> bool:
        """Verifica se almeno un personaggio è vivo"""
        return any(char.is_alive for char in self.characters)
    
    def get_party_status(self) -> str:
        """Ritorna lo stato del party come stringa formattata"""
        if not self.characters:
            return "Party vuoto"
        
        status_lines = []
        for i, char in enumerate(self.characters, 1):
            status_lines.append(f"[P{i}] {char}")
        
        return "\n".join(status_lines)
    
    def __len__(self) -> int:
        """Ritorna il numero di personaggi nel party"""
        return len(self.characters)
    
    def __str__(self) -> str:
        return self.get_party_status()