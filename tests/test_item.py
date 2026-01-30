"""
Unit tests per Item (Sprint 3)
"""

import pytest
from models.item import Item, ItemType, ItemEffect


class TestItem:
    """Test suite per Item"""
    
    def test_item_creation_health_potion(self):
        """Test creazione pozione vita"""
        item = Item('health_potion', quantity=3)
        
        assert item.item_id == 'health_potion'
        assert item.name == 'Pozione di Vita'
        assert item.quantity == 3
        assert item.consumable is True
        assert item.effect == ItemEffect.HEAL
        assert item.value == 50
    
    def test_item_creation_invalid_id(self):
        """Test creazione con ID non valido"""
        with pytest.raises(ValueError):
            Item('invalid_item_id')
    
    def test_item_use_success(self):
        """Test uso oggetto con successo"""
        item = Item('health_potion', quantity=2)
        
        result = item.use()
        
        assert result['success'] is True
        assert item.quantity == 1
        assert result['effect'] == ItemEffect.HEAL
        assert result['value'] == 50
    
    def test_item_use_depleted(self):
        """Test uso oggetto quando finito"""
        item = Item('health_potion', quantity=0)
        
        result = item.use()
        
        assert result['success'] is False
        assert "Non hai più" in result['message']
    
    def test_item_consumable_reduces_quantity(self):
        """Test oggetto consumabile riduce quantità"""
        item = Item('health_potion', quantity=5)
        
        item.use()
        item.use()
        
        assert item.quantity == 3
    
    def test_item_get_info(self):
        """Test get_info"""
        item = Item('mana_potion', quantity=2)
        
        info = item.get_info()
        
        assert 'Pozione di Mana' in info
        assert 'x2' in info
    
    def test_all_item_templates(self):
        """Test tutti i template"""
        for item_id in Item.get_item_ids():
            item = Item(item_id, quantity=1)
            
            assert item.item_id == item_id
            assert item.name is not None
            assert item.description is not None
    
    def test_health_potion_major(self):
        """Test pozione vita maggiore"""
        item = Item('health_potion_major')
        
        assert item.value == 100
        assert item.effect == ItemEffect.HEAL
    
    def test_mana_potion(self):
        """Test pozione mana"""
        item = Item('mana_potion')
        
        assert item.value == 30
        assert item.effect == ItemEffect.RESTORE_MP
    
    def test_bomb(self):
        """Test bomba"""
        item = Item('bomb')
        
        assert item.value == 40
        assert item.effect == ItemEffect.DAMAGE
    
    def test_elixir(self):
        """Test elisir"""
        item = Item('elixir')
        
        assert item.value == 999
        assert item.item_type == ItemType.CONSUMABLE
    
    def test_str_representation(self):
        """Test rappresentazione stringa"""
        item = Item('health_potion', quantity=3)
        
        str_repr = str(item)
        
        assert 'Pozione di Vita' in str_repr
        assert 'x3' in str_repr
    
    def test_get_item_templates(self):
        """Test get_item_templates"""
        templates = Item.get_item_templates()
        
        assert isinstance(templates, dict)
        assert len(templates) > 0
        assert 'health_potion' in templates
    
    def test_get_item_ids(self):
        """Test get_item_ids"""
        ids = Item.get_item_ids()
        
        assert isinstance(ids, list)
        assert 'health_potion' in ids
        assert 'mana_potion' in ids