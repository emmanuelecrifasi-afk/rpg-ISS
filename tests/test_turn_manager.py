"""
Unit tests per TurnManager (Sprint 2)
"""

import pytest
from models.character import Character
from combat.enemy import Enemy
from combat.turn_manager import TurnManager, Combatant


class TestTurnManager:
    """Test suite per TurnManager"""
    
    @pytest.fixture
    def sample_players(self):
        """Crea due personaggi di esempio"""
        p1 = Character(name="Hero1", character_class="guerriero")
        p2 = Character(name="Hero2", character_class="mago")
        return [p1, p2]
    
    @pytest.fixture
    def sample_enemy(self):
        """Crea un nemico di esempio"""
        return Enemy(enemy_type="goblin", level=1)
    
    @pytest.fixture
    def turn_manager(self, sample_players, sample_enemy):
        """Crea un TurnManager"""
        return TurnManager(sample_players, sample_enemy)
    
    def test_initialization(self, turn_manager):
        """Test inizializzazione"""
        assert turn_manager.round_number == 1
        assert turn_manager.current_turn_index == 0
        assert len(turn_manager.turn_order) == 3  
    
    def test_turn_order_structure(self, turn_manager):
        """Test struttura ordine turni"""
        
        assert turn_manager.turn_order[0].is_player is True
        assert turn_manager.turn_order[1].is_player is True
        
        
        assert turn_manager.turn_order[2].is_player is False
    
    def test_get_current_combatant(self, turn_manager):
        """Test ottenimento combattente corrente"""
        current = turn_manager.get_current_combatant()
        
        assert current is not None
        assert current.is_player is True
        assert current.name == "Hero1"
    
    def test_next_turn(self, turn_manager):
        """Test passaggio turno successivo"""
        turn_manager.next_turn()
        
        assert turn_manager.current_turn_index == 1
        
        current = turn_manager.get_current_combatant()
        assert current.name == "Hero2"
    
    def test_next_turn_wraps_around(self, turn_manager):
        """Test turno torna a zero dopo ultimo"""
        
        turn_manager.next_turn()
        turn_manager.next_turn()
        turn_manager.next_turn()
        
        assert turn_manager.current_turn_index == 0
        assert turn_manager.round_number == 2
    
    def test_is_battle_active_all_alive(self, turn_manager):
        """Test battaglia attiva con tutti vivi"""
        assert turn_manager.is_battle_active() is True
    
    def test_is_battle_active_players_dead(self, sample_players, sample_enemy):
        """Test battaglia finita se giocatori morti"""
        
        for player in sample_players:
            player.hp = 0
            player.is_alive = False
        
        manager = TurnManager(sample_players, sample_enemy)
        
        assert manager.is_battle_active() is False
    
    def test_is_battle_active_enemy_dead(self, sample_players, sample_enemy):
        """Test battaglia finita se nemico morto"""
        sample_enemy.hp = 0
        sample_enemy.is_alive = False
        
        manager = TurnManager(sample_players, sample_enemy)
        
        assert manager.is_battle_active() is False
    
    def test_is_battle_active_one_player_alive(self, sample_players, sample_enemy):
        """Test battaglia attiva con un giocatore vivo"""
        sample_players[0].hp = 0
        sample_players[0].is_alive = False
        
        manager = TurnManager(sample_players, sample_enemy)
        
        assert manager.is_battle_active() is True
    
    def test_get_alive_players(self, turn_manager, sample_players):
        """Test ottenimento giocatori vivi"""
        alive = turn_manager.get_alive_players()
        
        assert len(alive) == 2
        assert all(p.is_alive for p in alive)
    
    def test_get_alive_players_one_dead(self, turn_manager, sample_players):
        """Test ottenimento giocatori con uno morto"""
        sample_players[0].hp = 0
        sample_players[0].is_alive = False
        
        alive = turn_manager.get_alive_players()
        
        assert len(alive) == 1
        assert alive[0].name == "Hero2"
    
    def test_get_alive_combatants(self, turn_manager):
        """Test ottenimento tutti combattenti vivi"""
        alive = turn_manager.get_alive_combatants()
        
        assert len(alive) == 3  
    
    def test_get_battle_status(self, turn_manager):
        """Test ottenimento stato battaglia"""
        status = turn_manager.get_battle_status()
        
        assert status['round'] == 1
        assert status['current_turn'] == 0
        assert status['total_turns'] == 3
        assert status['players_alive'] == 2
        assert status['enemy_alive'] is True
        assert status['battle_active'] is True
    
    def test_reset(self, turn_manager):
        """Test reset manager"""
        
        turn_manager.next_turn()
        turn_manager.next_turn()
        turn_manager.round_number = 5
        
        
        turn_manager.reset()
        
        assert turn_manager.round_number == 1
        assert turn_manager.current_turn_index == 0
    
    def test_skip_dead_combatants(self, turn_manager, sample_players):
        """Test che salta combattenti morti"""
        
        sample_players[0].hp = 0
        sample_players[0].is_alive = False
        
        
        current = turn_manager.get_current_combatant()
        
        assert current.name == "Hero2"
    
    def test_str_representation(self, turn_manager):
        """Test rappresentazione stringa"""
        str_repr = str(turn_manager)
        
        assert "Round 1" in str_repr
        assert "ACTIVE" in str_repr


class TestCombatant:
    """Test suite per Combatant"""
    
    def test_combatant_creation_player(self):
        """Test creazione combattente giocatore"""
        char = Character(name="Hero", character_class="guerriero")
        combatant = Combatant(char, is_player=True)
        
        assert combatant.is_player is True
        assert combatant.name == "Hero"
        assert combatant.is_alive() is True
    
    def test_combatant_creation_enemy(self):
        """Test creazione combattente nemico"""
        enemy = Enemy(enemy_type="goblin")
        combatant = Combatant(enemy, is_player=False)
        
        assert combatant.is_player is False
        assert combatant.name == "Goblin"
        assert combatant.is_alive() is True
    
    def test_combatant_is_alive(self):
        """Test verifica vitalità"""
        char = Character(name="Hero", character_class="guerriero")
        combatant = Combatant(char, is_player=True)
        
        assert combatant.is_alive() is True
        
        char.hp = 0
        char.is_alive = False
        
        assert combatant.is_alive() is False
    
    def test_combatant_str(self):
        """Test rappresentazione stringa"""
        char = Character(name="Hero", character_class="guerriero")
        combatant = Combatant(char, is_player=True)
        
        str_repr = str(combatant)
        
        assert "[PLAYER]" in str_repr
        assert "Hero" in str_repr