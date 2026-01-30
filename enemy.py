"""
Modello Enemy - Rappresenta i nemici nel combattimento
"""

import random
from typing import Optional


class Enemy:
    """Classe che rappresenta un nemico"""
    
    # Template dei nemici con statistiche predefinite
    ENEMY_TEMPLATES = {
        'goblin': {
            'name': 'Goblin',
            'hp': 40,
            'min_damage': 5,
            'max_damage': 12,
            'description': 'Un piccolo e astuto goblin armato di pugnale'
        },
        'orc': {
            'name': 'Orco',
            'hp': 60,
            'min_damage': 8,
            'max_damage': 18,
            'description': 'Un feroce guerriero orco con una grossa ascia'
        },
        'troll': {
            'name': 'Troll',
            'hp': 80,
            'min_damage': 10,
            'max_damage': 25,
            'description': 'Un enorme troll con capacità rigenerative'
        },
        'skeleton': {
            'name': 'Scheletro',
            'hp': 35,
            'min_damage': 6,
            'max_damage': 14,
            'description': 'Uno scheletro animato da magia oscura'
        },
        'dragon': {
            'name': 'Drago',
            'hp': 120,
            'min_damage': 15,
            'max_damage': 35,
            'description': 'Un terribile drago con soffio di fuoco'
        }
    }
    
    def __init__(self, enemy_type: str = 'goblin', level: int = 1):
        """
        Inizializza un nemico
        
        Args:
            enemy_type: Tipo di nemico (goblin, orc, troll, etc.)
            level: Livello del nemico (scala gli HP e i danni)
        """
        if enemy_type not in self.ENEMY_TEMPLATES:
            enemy_type = 'goblin'
        
        template = self.ENEMY_TEMPLATES[enemy_type]
        
        self.enemy_type = enemy_type
        self.name = template['name']
        self.level = level
        self.description = template['description']
        
        # Scala statistiche in base al livello
        self.max_hp = int(template['hp'] * (1 + (level - 1) * 0.3))
        self.hp = self.max_hp
        self.min_damage = int(template['min_damage'] * (1 + (level - 1) * 0.2))
        self.max_damage = int(template['max_damage'] * (1 + (level - 1) * 0.2))
        
        self.is_alive = True
    
    def take_damage(self, amount: int) -> int:
        """
        Infligge danno al nemico
        
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
    
    def attack(self) -> int:
        """
        Il nemico attacca (genera danno casuale)
        
        Returns:
            Danno inflitto
        """
        if not self.is_alive:
            return 0
        
        damage = random.randint(self.min_damage, self.max_damage)
        return damage
    
    def get_hp_percentage(self) -> float:
        """Ritorna la percentuale di HP rimanenti"""
        if self.max_hp == 0:
            return 0
        return (self.hp / self.max_hp) * 100
    
    def get_display_name(self) -> str:
        """Ritorna il nome con livello se > 1"""
        if self.level > 1:
            return f"{self.name} (Lv.{self.level})"
        return self.name
    
    @classmethod
    def create_random(cls, min_level: int = 1, max_level: int = 3) -> 'Enemy':
        """
        Crea un nemico casuale
        
        Args:
            min_level: Livello minimo
            max_level: Livello massimo
            
        Returns:
            Istanza di Enemy casuale
        """
        enemy_type = random.choice(list(cls.ENEMY_TEMPLATES.keys()))
        level = random.randint(min_level, max_level)
        return cls(enemy_type=enemy_type, level=level)
    
    @classmethod
    def get_enemy_types(cls) -> list:
        """Ritorna la lista dei tipi di nemici disponibili"""
        return list(cls.ENEMY_TEMPLATES.keys())
    
    def __str__(self) -> str:
        """Rappresentazione testuale del nemico"""
        status = "💀" if not self.is_alive else "⚔️"
        return f"{status} {self.get_display_name()} [{self.hp}/{self.max_hp} HP]"
    
    def __repr__(self) -> str:
        return f"Enemy(type='{self.enemy_type}', level={self.level}, hp={self.hp}/{self.max_hp})"