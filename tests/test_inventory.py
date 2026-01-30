"""
Unit tests per Inventory (Sprint 3)
"""

import pytest
from models.inventory import Inventory
from models.item import ItemType


class TestInventory:
    """Test suite per Inventory"""
    
    def test_inventory_creation(self):
        """Test creazione inventario"""
        inv = Inventory()
        
        assert len(inv) == 0
        assert inv.max_slots == 20
    
    def test_add_item_new(self):
        """Test aggiunta nuovo oggetto"""
        inv = Inventory()
        
        result = inv.add_item('health_potion', 2)
        
        assert result is True
        assert len(inv) == 1
        assert inv.get_item_count('health_potion') == 2
    
    def test_add_item_existing(self):
        """Test aggiunta oggetto esistente"""
        inv = Inventory()
        inv.add_item('health_potion', 2)
        
        result = inv.add_item('health_potion', 3)
        
        assert result is True
        assert len(inv) == 1
        assert inv.get_item_count('health_potion') == 5
    
    def test_add_item_full_inventory(self):
        """Test aggiunta quando inventario pieno"""
        inv = Inventory(max_slots=2)
        inv.add_item('health_potion')
        inv.add_item('mana_potion')
        
        result = inv.add_item('bomb')
        
        assert result is False
        assert len(inv) == 2
    
    def test_remove_item_success(self):
        """Test rimozione oggetto con successo"""
        inv = Inventory()
        inv.add_item('health_potion', 5)
        
        result = inv.remove_item('health_potion', 2)
        
        assert result is True
        assert inv.get_item_count('health_potion') == 3
    
    def test_remove_item_all(self):
        """Test rimozione tutti gli oggetti"""
        inv = Inventory()
        inv.add_item('health_potion', 3)
        
        result = inv.remove_item('health_potion', 3)
        
        assert result is True
        assert len(inv) == 0
    
    def test_remove_item_insufficient(self):
        """Test rimozione quantità insufficiente"""
        inv = Inventory()
        inv.add_item('health_potion', 2)
        
        result = inv.remove_item('health_potion', 5)
        
        assert result is False
        assert inv.get_item_count('health_potion') == 2
    
    def test_remove_item_not_present(self):
        """Test rimozione oggetto non presente"""
        inv = Inventory()
        
        result = inv.remove_item('health_potion')
        
        assert result is False
    
    def test_has_item_true(self):
        """Test has_item quando presente"""
        inv = Inventory()
        inv.add_item('health_potion', 3)
        
        assert inv.has_item('health_potion') is True
        assert inv.has_item('health_potion', 2) is True
    
    def test_has_item_false(self):
        """Test has_item quando non presente"""
        inv = Inventory()
        
        assert inv.has_item('health_potion') is False
    
    def test_has_item_insufficient_quantity(self):
        """Test has_item con quantità insufficiente"""
        inv = Inventory()
        inv.add_item('health_potion', 2)
        
        assert inv.has_item('health_potion', 5) is False
    
    def test_get_item(self):
        """Test get_item"""
        inv = Inventory()
        inv.add_item('health_potion', 3)
        
        item = inv.get_item('health_potion')
        
        assert item is not None
        assert item.item_id == 'health_potion'
        assert item.quantity == 3
    
    def test_get_item_not_present(self):
        """Test get_item quando non presente"""
        inv = Inventory()
        
        item = inv.get_item('health_potion')
        
        assert item is None
    
    def test_get_consumables(self):
        """Test get_consumables"""
        inv = Inventory()
        inv.add_item('health_potion')
        inv.add_item('mana_potion')
        
        consumables = inv.get_consumables()
        
        assert len(consumables) == 2
    
    def test_use_item_success(self):
        """Test uso oggetto"""
        inv = Inventory()
        inv.add_item('health_potion', 2)
        
        result = inv.use_item('health_potion')
        
        assert result['success'] is True
        assert inv.get_item_count('health_potion') == 1
    
    def test_use_item_last_one(self):
        """Test uso ultimo oggetto"""
        inv = Inventory()
        inv.add_item('health_potion', 1)
        
        result = inv.use_item('health_potion')
        
        assert result['success'] is True
        assert len(inv) == 0
    
    def test_use_item_not_present(self):
        """Test uso oggetto non presente"""
        inv = Inventory()
        
        result = inv.use_item('health_potion')
        
        assert result['success'] is False
    
    def test_get_total_items(self):
        """Test get_total_items"""
        inv = Inventory()
        inv.add_item('health_potion', 3)
        inv.add_item('mana_potion', 2)
        
        total = inv.get_total_items()
        
        assert total == 5
    
    def test_get_unique_items(self):
        """Test get_unique_items"""
        inv = Inventory()
        inv.add_item('health_potion', 5)
        inv.add_item('mana_potion', 3)
        
        unique = inv.get_unique_items()
        
        assert unique == 2
    
    def test_is_full(self):
        """Test is_full"""
        inv = Inventory(max_slots=2)
        
        assert inv.is_full() is False
        
        inv.add_item('health_potion')
        inv.add_item('mana_potion')
        
        assert inv.is_full() is True
    
    def test_clear(self):
        """Test clear"""
        inv = Inventory()
        inv.add_item('health_potion', 3)
        inv.add_item('mana_potion', 2)
        
        inv.clear()
        
        assert len(inv) == 0
    
    def test_get_inventory_list_empty(self):
        """Test get_inventory_list quando vuoto"""
        inv = Inventory()
        
        inv_list = inv.get_inventory_list()
        
        assert "vuoto" in inv_list[0].lower()
    
    def test_get_inventory_list_with_items(self):
        """Test get_inventory_list con oggetti"""
        inv = Inventory()
        inv.add_item('health_potion', 2)
        
        inv_list = inv.get_inventory_list()
        
        assert len(inv_list) > 0
        assert any('Pozione' in item for item in inv_list)
    
    def test_to_dict(self):
        """Test to_dict"""
        inv = Inventory()
        inv.add_item('health_potion', 3)
        
        data = inv.to_dict()
        
        assert 'items' in data
        assert 'max_slots' in data
        assert 'health_potion' in data['items']
    
    def test_str_representation_empty(self):
        """Test rappresentazione stringa vuoto"""
        inv = Inventory()
        
        str_repr = str(inv)
        
        assert 'vuoto' in str_repr.lower()
    
    def test_str_representation_with_items(self):
        """Test rappresentazione stringa con oggetti"""
        inv = Inventory()
        inv.add_item('health_potion', 2)
        
        str_repr = str(inv)
        
        assert 'Pozione' in str_repr