"""
Classe Character - Rappresenta un singolo personaggio
"""


class Character:
    """Classe che rappresenta un personaggio del gioco"""
    
    # Definizione delle classi disponibili
    CLASSES = {
        'guerriero': {
            'name': 'Guerriero',
            'hp': 120,
            'max_hp': 120,
            'description': 'Forte e resistente, specializzato nel combattimento corpo a corpo'
        },
        'mago': {
            'name': 'Mago',
            'hp': 80,
            'max_hp': 80,
            'description': 'Fragile ma potente, maestro delle arti arcane'
        },
        'ladro': {
            'name': 'Ladro',
            'hp': 90,
            'max_hp': 90,
            'description': 'Agile e veloce, esperto in attacchi furtivi'
        },
        'paladino': {
            'name': 'Paladino',
            'hp': 110,
            'max_hp': 110,
            'description': 'Bilanciato tra attacco e difesa, può curare gli alleati'
        },
        'ranger': {
            'name': 'Ranger',
            'hp': 95,
            'max_hp': 95,
            'description': 'Arciere esperto, ottimo per attacchi a distanza'
        }
    }
    
    def __init__(self, name: str, character_class: str = 'guerriero', hp: int = None, max_hp: int = None):
        """
        Inizializza un personaggio
        
        Args:
            name: Nome del personaggio
            character_class: Classe del personaggio (guerriero, mago, etc.)
            hp: Punti vita attuali (Debugging, usa quello della classe se non specificato)
            max_hp: Punti vita massimi (Debugging, usa quello della classe se non specificato)
        """
        self.name = name
        self.character_class = character_class.lower()
        
        # Usa gli HP della classe se non specificati
        if character_class.lower() in self.CLASSES:
            class_data = self.CLASSES[character_class.lower()]
            self.hp = hp if hp is not None else class_data['hp']
            self.max_hp = max_hp if max_hp is not None else class_data['max_hp']
        else:
            self.hp = hp if hp is not None else 100
            self.max_hp = max_hp if max_hp is not None else 100
        
        self.is_alive = True
    
    def take_damage(self, amount: int) -> int:
        """
        Infligge danno al personaggio
        
        Args:
            amount: Quantità di danno
            
        Returns:
            Danno effettivo inflitto
        """
        actual_damage = min(amount, self.hp)
        self.hp -= actual_damage
        
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """
        Cura il personaggio
        
        Args:
            amount: Quantità di cura
            
        Returns:
            HP effettivamente recuperati
        """
        if not self.is_alive:
            return 0
            
        old_hp = self.hp
        self.hp = min(self.hp + amount, self.max_hp)
        return self.hp - old_hp
    
    def get_hp_percentage(self) -> float:
        """Ritorna la percentuale di HP rimanenti"""
        return (self.hp / self.max_hp) * 100
    
    def __str__(self) -> str:
        """Rappresentazione testuale del personaggio"""
        status = "✓ VIVO" if self.is_alive else "✗ KO"
        class_name = self.CLASSES.get(self.character_class, {}).get('name', self.character_class.title())
        return f"{self.name} ({class_name}) [{self.hp}/{self.max_hp} HP] {status}"
    
    def __repr__(self) -> str:
        return f"Character(name='{self.name}', class='{self.character_class}', hp={self.hp}, max_hp={self.max_hp})"
    
    @classmethod
    def get_class_info(cls, character_class: str) -> dict:
        """Ottiene le informazioni su una classe"""
        return cls.CLASSES.get(character_class.lower(), None)
    
    @classmethod
    def get_available_classes(cls) -> list:
        """Ritorna la lista delle classi disponibili"""
        return list(cls.CLASSES.keys())