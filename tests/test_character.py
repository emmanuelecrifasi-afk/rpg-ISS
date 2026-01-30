"""
Unit tests per la classe Character
"""
import pytest
import sys
import os

# Aggiungi la root del progetto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.character import Character

class TestCharacter:
    """Test suite per Character"""

    def test_character_creation_default(self):
        """Test creazione personaggio con valori di default"""
        char = Character(name="Test Hero", character_class="guerriero")
        assert char.name == "Test Hero"
        assert char.character_class == "guerriero"
        assert char.hp == 120
        assert char.max_hp == 120
        assert char.is_alive is True

    def test_character_creation_all_classes(self):
        """Test creazione personaggio per tutte le classi"""
        classes_hp = {
            'guerriero': 120,
            'mago': 80,
            'ladro': 90,
            'paladino': 110,
            'ranger': 95
        }
        
        for class_name, expected_hp in classes_hp.items():
            char = Character(name="Hero", character_class=class_name)
            assert char.hp == expected_hp
            assert char.max_hp == expected_hp

    def test_take_damage(self):
        """Test danno al personaggio"""
        char = Character(name="Hero", character_class="guerriero")
        damage = char.take_damage(30)
        assert damage == 30
        assert char.hp == 90
        assert char.is_alive is True

    def test_take_damage_ko(self):
        """Test personaggio va KO"""
        char = Character(name="Hero", character_class="mago")
        damage = char.take_damage(100)
        assert damage == 80  # HP massimi del mago
        assert char.hp == 0
        assert char.is_alive is False

    def test_take_damage_overkill(self):
        """Test danno superiore agli HP rimanenti"""
        char = Character(name="Hero", character_class="guerriero")
        char.hp = 10
        damage = char.take_damage(50)
        assert damage == 10  # Solo gli HP rimanenti
        assert char.hp == 0
        assert char.is_alive is False

    def test_heal(self):
        """Test cura personaggio"""
        char = Character(name="Hero", character_class="guerriero")
        char.hp = 50
        healed = char.heal(30)
        assert healed == 30
        assert char.hp == 80

    def test_heal_max_hp(self):
        """Test cura non supera HP massimi"""
        char = Character(name="Hero", character_class="guerriero")
        char.hp = 100
        healed = char.heal(50)
        assert healed == 20
        assert char.hp == 120

    def test_heal_ko_character(self):
        """Test cura su personaggio KO non funziona"""
        char = Character(name="Hero", character_class="guerriero")
        char.hp = 0
        char.is_alive = False
        healed = char.heal(50)
        assert healed == 0
        assert char.hp == 0

    def test_get_hp_percentage(self):
        """Test calcolo percentuale HP"""
        char = Character(name="Hero", character_class="guerriero")
        char.hp = 60
        percentage = char.get_hp_percentage()
        assert percentage == 50.0

    def test_get_class_info(self):
        """Test ottenimento info classe"""
        info = Character.get_class_info("guerriero")
        assert info is not None
        assert info['name'] == 'Guerriero'
        assert info['hp'] == 120
        assert 'description' in info

    def test_get_available_classes(self):
        """Test lista classi disponibili"""
        classes = Character.get_available_classes()
        assert len(classes) == 5
        assert 'guerriero' in classes
        assert 'mago' in classes
