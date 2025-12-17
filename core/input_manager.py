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
        'status': ['stato', 'info', 's'],
        'help': ['aiuto', 'h', '?'],
        'quit': ['exit', 'esci', 'q'],
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
        """
        Parsea l'input dell'utente e restituisce un Command
        
        Args:
            user_input: Stringa di input dell'utente
            
        Returns:
            Command parsato o None se l'input non è valido
            
        Esempi:
            "p1 atk" -> Command(action='atk', target='p1')
            "status" -> Command(action='status')
            "p2 heal 50" -> Command(action='heal', target='p2', args=['50'])
        """
        if not user_input or not user_input.strip():
            return None
        
        # Pulisci e dividi l'input
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
            "• status / s           - Mostra lo stato del party",
            "• p1 atk / p2 atk     - Personaggio attacca (danno casuale)",
            "• p1 heal [amount]    - Personaggio si cura (default: 20 HP)",
            "• help / h / ?        - Mostra questo aiuto",
            "• quit / q / exit     - Esci dal gioco",
            "",
            "Esempi:",
            "  > status",
            "  > p1 atk",
            "  > p2 heal 30",
        ]
        return "\n".join(help_text)