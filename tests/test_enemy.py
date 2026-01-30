"""
Unit tests per la classe Enemy (Sprint 2)
"""

import pytest
from combat.enemy import Enemy


class TestEnemy:
    """Test suite per Enemy"""
    
    def test_enemy_creation_default(self):
        """Test creazione nemico con valori di default"""
        enemy = Enemy()
        
        assert enemy.enemy_type == "goblin"
        assert enemy.level == 1
        assert enemy.is_alive is True
        assert enemy.hp > 0
    
    def test_enemy_creation_orc(self):
        """Test creazione orco"""
        enemy = Enemy(enemy_type="orc", level=1)
        
        assert enemy.enemy_type == "orc"
        assert enemy.name == "Orco"
        assert enemy.hp == 60
        assert enemy.max_hp == 60
    
    def test_enemy_creation_with_level(self):
        """Test creazione con livello superiore"""
        enemy = Enemy(enemy_type="goblin", level=3)
        
        assert enemy.level == 3
        assert enemy.max_hp > 40  # HP scalati
        assert enemy.min_damage > 5  # Danno scalato
    
    def test_enemy_invalid_type_defaults_to_goblin(self):
        """Test tipo non valido usa goblin"""
        enemy = Enemy(enemy_type="invalid_type")
        
        assert enemy.enemy_type == "goblin"
    
    def test_take_damage(self):
        """Test danno al nemico"""
        enemy = Enemy(enemy_type="goblin")
        initial_hp = enemy.hp
        
        damage = enemy.take_damage(20)
        
        assert damage == 20
        assert enemy.hp == initial_hp - 20
        assert enemy.is_alive is True
    
    def test_take_damage_death(self):
        """Test nemico muore"""
        enemy = Enemy(enemy_type="goblin")
        
        damage = enemy.take_damage(100)
        
        assert damage == enemy.max_hp
        assert enemy.hp == 0
        assert enemy.is_alive is False
    
    def test_take_damage_overkill(self):
        """Test danno eccessivo"""
        enemy = Enemy(enemy_type="goblin")
        enemy.hp = 10
        
        damage = enemy.take_damage(50)
        
        assert damage == 10
        assert enemy.hp == 0
    
    def test_attack(self):
        """Test attacco del nemico"""
        enemy = Enemy(enemy_type="goblin")
        
        damage = enemy.attack()
        
        assert enemy.min_damage <= damage <= enemy.max_damage
    
    def test_attack_when_dead(self):
        """Test attacco quando morto"""
        enemy = Enemy(enemy_type="goblin")
        enemy.hp = 0
        enemy.is_alive = False
        
        damage = enemy.attack()
        
        assert damage == 0
    
    def test_get_hp_percentage(self):
        """Test calcolo percentuale HP"""
        enemy = Enemy(enemy_type="goblin")
        enemy.hp = enemy.max_hp // 2
        
        percentage = enemy.get_hp_percentage()
        
        assert 49 <= percentage <= 51  # ~50%
    
    def test_get_hp_percentage_full(self):
        """Test percentuale HP pieno"""
        enemy = Enemy(enemy_type="goblin")
        
        percentage = enemy.get_hp_percentage()
        
        assert percentage == 100.0
    
    def test_get_hp_percentage_zero(self):
        """Test percentuale HP zero"""
        enemy = Enemy(enemy_type="goblin")
        enemy.hp = 0
        
        percentage = enemy.get_hp_percentage()
        
        assert percentage == 0.0
    
    def test_get_display_name_level_1(self):
        """Test nome display livello 1"""
        enemy = Enemy(enemy_type="goblin", level=1)
        
        name = enemy.get_display_name()
        
        assert name == "Goblin"
    
    def test_get_display_name_higher_level(self):
        """Test nome display livello superiore"""
        enemy = Enemy(enemy_type="orc", level=5)
        
        name = enemy.get_display_name()
        
        assert "Lv.5" in name
        assert "Orco" in name
    
    def test_create_random(self):
        """Test creazione casuale"""
        enemy = Enemy.create_random(min_level=1, max_level=3)
        
        assert enemy.enemy_type in Enemy.ENEMY_TEMPLATES
        assert 1 <= enemy.level <= 3
        assert enemy.is_alive is True
    
    def test_get_enemy_types(self):
        """Test lista tipi di nemici"""
        types = Enemy.get_enemy_types()
        
        assert len(types) == 5
        assert "goblin" in types
        assert "orc" in types
        assert "troll" in types
        assert "skeleton" in types
        assert "dragon" in types
    
    def test_all_enemy_types_creation(self):
        """Test creazione di tutti i tipi"""
        for enemy_type in Enemy.get_enemy_types():
            enemy = Enemy(enemy_type=enemy_type, level=1)
            
            assert enemy.enemy_type == enemy_type
            assert enemy.is_alive is True
            assert enemy.hp > 0
    
    def test_str_representation(self):
        """Test rappresentazione stringa"""
        enemy = Enemy(enemy_type="goblin", level=1)
        
        str_repr = str(enemy)
        
        assert "Goblin" in str_repr
        assert "HP" in str_repr
    
    def test_str_representation_dead(self):
        """Test rappresentazione stringa quando morto"""
        enemy = Enemy(enemy_type="goblin")
        enemy.hp = 0
        enemy.is_alive = False
        
        str_repr = str(enemy)
        
        assert "💀" in str_repr