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
            'mp': 20,
            'max_mp': 20,
            'atk_bonus': 10,
            'def_bonus': 5,
            'mag_bonus': 0,
            'description': 'Forte e resistente, specializzato nel combattimento corpo a corpo'
        },
        'mago': {
            'name': 'Mago',
            'hp': 80,
            'max_hp': 80,
            'mp': 50,
            'max_mp': 50,
            'atk_bonus': 0,
            'def_bonus': 0,
            'mag_bonus': 15,
            'description': 'Fragile ma potente, maestro delle arti arcane'
        },
        'ladro': {
            'name': 'Ladro',
            'hp': 90,
            'max_hp': 90,
            'mp': 30,
            'max_mp': 30,
            'atk_bonus': 7,
            'def_bonus': 2,
            'mag_bonus': 0,
            'description': 'Agile e veloce, esperto in attacchi furtivi'
        },
        'paladino': {
            'name': 'Paladino',
            'hp': 110,
            'max_hp': 110,
            'mp': 40,
            'max_mp': 40,
            'atk_bonus': 5,
            'def_bonus': 7,
            'mag_bonus': 5,
            'description': 'Bilanciato tra attacco e difesa, può curare gli alleati'
        },
        'ranger': {
            'name': 'Ranger',
            'hp': 95,
            'max_hp': 95,
            'mp': 35,
            'max_mp': 35,
            'atk_bonus': 6,
            'def_bonus': 3,
            'mag_bonus': 3,
            'description': 'Arciere esperto, ottimo per attacchi a distanza'
        }
    }
    
    def __init__(self, name: str, character_class: str = 'guerriero', hp: int = None, max_hp: int = None):
        """
        Inizializza un personaggio
        
        Args:
            name: Nome del personaggio
            character_class: Classe del personaggio (guerriero, mago, etc.)
            hp: Punti vita attuali (opzionale, usa quello della classe se non specificato)
            max_hp: Punti vita massimi (opzionale, usa quello della classe se non specificato)
        """
        self.name = name
        self.character_class = character_class.lower()
        
        # Usa gli HP della classe se non specificati
        if character_class.lower() in self.CLASSES:
            class_data = self.CLASSES[character_class.lower()]
            self.hp = hp if hp is not None else class_data['hp']
            self.max_hp = max_hp if max_hp is not None else class_data['max_hp']
            self.mp = class_data['mp']
            self.max_mp = class_data['max_mp']
            self.atk_bonus = class_data['atk_bonus']
            self.def_bonus = class_data['def_bonus']
            self.mag_bonus = class_data['mag_bonus']
        else:
            self.hp = hp if hp is not None else 100
            self.max_hp = max_hp if max_hp is not None else 100
            self.mp = 30
            self.max_mp = 30
            self.atk_bonus = 0
            self.def_bonus = 0
            self.mag_bonus = 0
        
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
    
    def restore_mp(self, amount: int) -> int:
        """
        Ripristina gli MP del personaggio
        
        Args:
            amount: Quantità di MP da ripristinare
            
        Returns:
            MP effettivamente recuperati
        """
        if not self.is_alive:
            return 0
        
        old_mp = self.mp
        self.mp = min(self.mp + amount, self.max_mp)
        return self.mp - old_mp
    
    def use_mp(self, amount: int) -> bool:
        """
        Usa MP per un'abilità
        
        Args:
            amount: Quantità di MP da usare
            
        Returns:
            True se i MP sono sufficienti, False altrimenti
        """
        if self.mp < amount:
            return False
        
        self.mp -= amount
        return True
    
    def calculate_physical_damage(self) -> int:
        """
        Calcola il danno fisico base del personaggio
        
        Returns:
            Danno fisico (include bonus ATK)
        """
        import random
        base_damage = random.randint(10, 25)
        return base_damage + self.atk_bonus
    
    def calculate_magic_damage(self) -> int:
        """
        Calcola il danno magico base del personaggio
        
        Returns:
            Danno magico (include bonus MAG)
        """
        import random
        base_damage = random.randint(15, 30)
        return base_damage + self.mag_bonus
    
    def get_hp_percentage(self) -> float:
        """Ritorna la percentuale di HP rimanenti"""
        return (self.hp / self.max_hp) * 100
    
    def __str__(self) -> str:
        """Rappresentazione testuale del personaggio"""
        status = "✓ VIVO" if self.is_alive else "✗ KO"
        class_name = self.CLASSES.get(self.character_class, {}).get('name', self.character_class.title())
        return f"{self.name} ({class_name}) [{self.hp}/{self.max_hp} HP | {self.mp}/{self.max_mp} MP] {status}"
    
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
    
    

    def apply_victory_bonus(self):
        """Aumenta HP e Mana massimi dopo una vittoria"""
        hp_boost = 10
        mp_boost = 5
        
        
        self.max_hp += hp_boost
        self.hp += hp_boost  
        
        
        if hasattr(self, 'mp') and hasattr(self, 'max_mp'):
            self.max_mp += mp_boost
            self.mp += mp_boost
            