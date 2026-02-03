"""
Modello Item - Rappresenta gli oggetti del gioco
"""

from typing import Optional
from enum import Enum


class ItemType(Enum):
    """Tipi di oggetti"""
    CONSUMABLE = "consumable"  
    EQUIPMENT = "equipment"    
    KEY_ITEM = "key_item"      
    MATERIAL = "material"      


class ItemEffect(Enum):
    """Effetti degli oggetti"""
    HEAL = "heal"              
    RESTORE_MP = "restore_mp"  
    DAMAGE = "damage"          
    BUFF_ATK = "buff_atk"      
    BUFF_DEF = "buff_def"      


class Item:
    """Classe che rappresenta un oggetto"""
    
    #
    ITEM_TEMPLATES = {
        'health_potion': {
            'name': 'Pozione di Vita',
            'description': 'Ripristina 50 HP',
            'item_type': ItemType.CONSUMABLE,
            'effect': ItemEffect.HEAL,
            'value': 50,
            'consumable': True
        },
        'health_potion_major': {
            'name': 'Pozione di Vita Maggiore',
            'description': 'Ripristina 100 HP',
            'item_type': ItemType.CONSUMABLE,
            'effect': ItemEffect.HEAL,
            'value': 100,
            'consumable': True
        },
        'mana_potion': {
            'name': 'Pozione di Mana',
            'description': 'Ripristina 30 MP',
            'item_type': ItemType.CONSUMABLE,
            'effect': ItemEffect.RESTORE_MP,
            'value': 30,
            'consumable': True
        },
        'elixir': {
            'name': 'Elisir',
            'description': 'Ripristina completamente HP e MP',
            'item_type': ItemType.CONSUMABLE,
            'effect': ItemEffect.HEAL,
            'value': 999,
            'consumable': True
        },
        'bomb': {
            'name': 'Bomba',
            'description': 'Infligge 40 danni al nemico',
            'item_type': ItemType.CONSUMABLE,
            'effect': ItemEffect.DAMAGE,
            'value': 40,
            'consumable': True
        },
        'strength_tonic': {
            'name': 'Tonico della Forza',
            'description': 'Aumenta l\'attacco per 3 turni',
            'item_type': ItemType.CONSUMABLE,
            'effect': ItemEffect.BUFF_ATK,
            'value': 5,
            'consumable': True
        }
    }
    
    def __init__(self, item_id: str, quantity: int = 1):
        """
        Inizializza un oggetto
        
        Args:
            item_id: ID dell'oggetto (chiave in ITEM_TEMPLATES)
            quantity: Quantità iniziale
        """
        if item_id not in self.ITEM_TEMPLATES:
            raise ValueError(f"Item ID '{item_id}' non valido")
        
        template = self.ITEM_TEMPLATES[item_id]
        
        self.item_id = item_id
        self.name = template['name']
        self.description = template['description']
        self.item_type = template['item_type']
        self.effect = template['effect']
        self.value = template['value']
        self.consumable = template['consumable']
        self.quantity = quantity
    
    def use(self, target=None) -> dict:
        """
        Usa l'oggetto
        
        Args:
            target: Bersaglio dell'oggetto (se necessario)
            
        Returns:
            Dizionario con il risultato dell'uso
        """
        if self.quantity <= 0:
            return {
                'success': False,
                'message': f"Non hai più {self.name}!",
                'effect': None,
                'value': 0
            }
        
        # Consuma l'oggetto se consumabile
        if self.consumable:
            self.quantity -= 1
        
        return {
            'success': True,
            'message': f"Hai usato {self.name}!",
            'effect': self.effect,
            'value': self.value
        }
    
    def get_info(self) -> str:
        """Ottiene informazioni sull'oggetto"""
        return f"{self.name} x{self.quantity} - {self.description}"
    
    @classmethod
    def get_item_templates(cls) -> dict:
        """Ritorna tutti i template disponibili"""
        return cls.ITEM_TEMPLATES.copy()
    
    @classmethod
    def get_item_ids(cls) -> list:
        """Ritorna la lista di tutti gli ID oggetti"""
        return list(cls.ITEM_TEMPLATES.keys())
    
    def __str__(self) -> str:
        return f"{self.name} x{self.quantity}"
    
    def __repr__(self) -> str:
        return f"Item(id='{self.item_id}', quantity={self.quantity})"