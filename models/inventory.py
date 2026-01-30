"""
Modello Inventory - Gestisce l'inventario condiviso del party
"""

from typing import Optional, List, Dict
from models.item import Item, ItemType


class Inventory:
    """Classe che gestisce l'inventario condiviso"""
    
    def __init__(self, max_slots: int = 20):
        """
        Inizializza l'inventario
        
        Args:
            max_slots: Numero massimo di slot (tipi di oggetti diversi)
        """
        self.items: Dict[str, Item] = {}
        self.max_slots = max_slots
    
    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Aggiunge un oggetto all'inventario
        
        Args:
            item_id: ID dell'oggetto da aggiungere
            quantity: Quantità da aggiungere
            
        Returns:
            True se l'oggetto è stato aggiunto, False altrimenti
        """
        # Se l'oggetto esiste già, aumenta la quantità
        if item_id in self.items:
            self.items[item_id].quantity += quantity
            return True
        
        # Controlla se c'è spazio
        if len(self.items) >= self.max_slots:
            return False
        
        # Crea nuovo oggetto
        try:
            self.items[item_id] = Item(item_id, quantity)
            return True
        except ValueError:
            return False
    
    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Rimuove un oggetto dall'inventario
        
        Args:
            item_id: ID dell'oggetto da rimuovere
            quantity: Quantità da rimuovere
            
        Returns:
            True se l'oggetto è stato rimosso, False altrimenti
        """
        if item_id not in self.items:
            return False
        
        item = self.items[item_id]
        
        if item.quantity < quantity:
            return False
        
        item.quantity -= quantity
        
        # Rimuovi l'oggetto se la quantità è 0
        if item.quantity == 0:
            del self.items[item_id]
        
        return True
    
    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Verifica se l'inventario contiene un oggetto
        
        Args:
            item_id: ID dell'oggetto
            quantity: Quantità minima richiesta
            
        Returns:
            True se l'oggetto è presente in quantità sufficiente
        """
        if item_id not in self.items:
            return False
        
        return self.items[item_id].quantity >= quantity
    
    def get_item(self, item_id: str) -> Optional[Item]:
        """
        Ottiene un oggetto dall'inventario
        
        Args:
            item_id: ID dell'oggetto
            
        Returns:
            Item se presente, None altrimenti
        """
        return self.items.get(item_id)
    
    def get_items_by_type(self, item_type: ItemType) -> List[Item]:
        """
        Ottiene tutti gli oggetti di un certo tipo
        
        Args:
            item_type: Tipo di oggetto
            
        Returns:
            Lista di Item del tipo specificato
        """
        return [item for item in self.items.values() if item.item_type == item_type]
    
    def get_consumables(self) -> List[Item]:
        """Ottiene tutti gli oggetti consumabili"""
        return self.get_items_by_type(ItemType.CONSUMABLE)
    
    def use_item(self, item_id: str, target=None) -> dict:
        """
        Usa un oggetto dall'inventario
        
        Args:
            item_id: ID dell'oggetto da usare
            target: Bersaglio dell'oggetto
            
        Returns:
            Dizionario con il risultato dell'uso
        """
        if not self.has_item(item_id):
            return {
                'success': False,
                'message': f"Oggetto non presente nell'inventario!",
                'effect': None,
                'value': 0
            }
        
        item = self.items[item_id]
        result = item.use(target)
        
        # Rimuovi l'oggetto se la quantità è 0
        if item.quantity == 0:
            del self.items[item_id]
        
        return result
    
    def get_item_count(self, item_id: str) -> int:
        """
        Ottiene la quantità di un oggetto
        
        Args:
            item_id: ID dell'oggetto
            
        Returns:
            Quantità dell'oggetto (0 se non presente)
        """
        if item_id not in self.items:
            return 0
        return self.items[item_id].quantity
    
    def get_total_items(self) -> int:
        """Ritorna il numero totale di oggetti (somma quantità)"""
        return sum(item.quantity for item in self.items.values())
    
    def get_unique_items(self) -> int:
        """Ritorna il numero di tipi di oggetti diversi"""
        return len(self.items)
    
    def is_full(self) -> bool:
        """Verifica se l'inventario è pieno"""
        return len(self.items) >= self.max_slots
    
    def clear(self):
        """Svuota l'inventario"""
        self.items.clear()
    
    def get_inventory_list(self) -> List[str]:
        """
        Ottiene la lista formattata dell'inventario
        
        Returns:
            Lista di stringhe con le info degli oggetti
        """
        if not self.items:
            return ["Inventario vuoto"]
        
        return [item.get_info() for item in self.items.values()]
    
    def to_dict(self) -> dict:
        """Converte l'inventario in dizionario"""
        return {
            'items': {
                item_id: {
                    'quantity': item.quantity,
                    'name': item.name
                }
                for item_id, item in self.items.items()
            },
            'max_slots': self.max_slots,
            'unique_items': self.get_unique_items(),
            'total_items': self.get_total_items()
        }
    
    def __str__(self) -> str:
        items_str = ", ".join(str(item) for item in self.items.values())
        return f"Inventory({items_str if items_str else 'vuoto'})"
    
    def __len__(self) -> int:
        """Ritorna il numero di tipi di oggetti diversi"""
        return len(self.items)