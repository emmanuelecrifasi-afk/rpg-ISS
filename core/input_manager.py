"""
Input Manager - Parser dei comandi di gioco
"""

from typing import Dict, Optional, List


class Command:
    """Rappresenta un comando parsato"""
    
    def __init__(self, action: str, target: Optional[str] = None, args: List[str] = None):
        self.action = action
        self.target = target
        self.args = args if args else []
    
    def __str__(self):
        return f"Command(action='{self.action}', target='{self.target}', args={self.args})"


class InputManager:
    """Gestisce il parsing e la validazione degli input utente"""
    
    # Comandi validi e loro alias
    VALID_ACTIONS = {
        'atk': ['attack', 'attacca', 'colpisci'],
        'heal': ['cura', 'guarisci'],
        'status': ['stato', 'info', 'st'],
        'help': ['aiuto', 'h', '?'],
        'quit': ['exit', 'esci', 'q'],
        'map': ['mappa', 'm'],
        'look': ['guarda', 'osserva', 'l'],
        'move': ['muovi', 'vai'],
        'inventory': ['inventario', 'inv', 'i'],
        'w': ['up', 'nord', 'n'],
        'a': ['left', 'ovest', 'o'],
        's': ['down', 'sud'],
        'd': ['right', 'est', 'e'],
    }
    
    def __init__(self):
        """Inizializza l'Input Manager"""
        # Crea una mappa inversa per gli alias
        self.action_map: Dict[str, str] = {}
        for main_action, aliases in self.VALID_ACTIONS.items():
            self.action_map[main_action] = main_action
            for alias in aliases:
                self.action_map[alias] = main_action
    
    def parse(self, user_input: str) -> Optional[Command]:
        
        if not user_input or not user_input.strip():
            return None
        
        
        parts = user_input.strip().lower().split()
        
        if len(parts) == 0:
            return None
        
        # Caso 1: Comando senza target (es. "status", "help")
        if len(parts) == 1:
            action = self._normalize_action(parts[0])
            if action:
                return Command(action=action)
            return None
        
        # Caso 2: Target + Action (es. "p1 atk")
        if len(parts) >= 2:
            potential_target = parts[0]
            potential_action = parts[1]
            
            # Verifica se il primo elemento è un target valido (p1, p2, etc.)
            if self._is_valid_target(potential_target):
                action = self._normalize_action(potential_action)
                if action:
                    args = parts[2:] if len(parts) > 2 else []
                    return Command(action=action, target=potential_target, args=args)
            
            # Altrimenti, prova ad interpretare come action + args
            action = self._normalize_action(parts[0])
            if action:
                return Command(action=action, args=parts[1:])
        
        return None
    
    def _normalize_action(self, action: str) -> Optional[str]:
        """
        Normalizza un'azione usando la mappa degli alias
        
        Returns:
            Azione normalizzata o None se non valida
        """
        return self.action_map.get(action.lower())
    
    def _is_valid_target(self, target: str) -> bool:
        """
        Verifica se il target è nel formato valido (p1, p2, etc.)
        """
        return target.startswith('p') and len(target) == 2 and target[1].isdigit()
    
    def get_help_text(self) -> str:
        """Ritorna il testo di aiuto con tutti i comandi disponibili"""
        help_text = [
            "📖 COMANDI DISPONIBILI:",
            "",
            "🎮 Party:",
            "• status / st           - Mostra lo stato del party",
            "• inventory / inv / i  - Mostra l'inventario",
            "",
            "🗺️  Esplorazione:",
            "• w / a / s / d       - Muovi su/sinistra/giù/destra",
            "• map / m             - Mostra la mappa",
            "• look / l            - Osserva i dintorni",
            "",
            "⚔️  Durante il Combattimento:",
            "• 1                   - Attacco Fisico (usa ATK bonus)",
            "• 2                   - Attacco Magico (usa MAG bonus, costa MP)",
            "• 3                   - Cura te stesso",
            "• 4                   - Cura un alleato",
            "• 5                   - Usa oggetto dall'inventario",
            "",
            "🔧 Sistema:",
            "• help / h / ?        - Mostra questo aiuto",
            "• quit / q / exit     - Esci dal gioco",
            "",
            "Esempi:",
            "  > w                 (muovi su)",
            "  > inventory         (vedi oggetti)",
            "  > 5                 (usa oggetto in battaglia)",
        ]
        return "\n".join(help_text)