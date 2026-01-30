"""
Unit tests per Battle System (Sprint 2)
"""

import pytest
from models.party import Party
from models.character import Character
from combat.enemy import Enemy
from combat.battle import Battle, BattleResult, BattleAction


class TestBattle:
    """Test suite per Battle"""
    
    @pytest.fixture
    def sample_party(self):
        """Crea un party di esempio"""
        party = Party()
        char1 = Character(name="Warrior", character_class="guerriero")
        char2 = Character(name="Mage", character_class="mago")
        party.add_character(char1)
        party.add_character(char2)
        return party
    
    @pytest.fixture
    def sample_enemy(self):
        """Crea un nemico di esempio"""
        return Enemy(enemy_type="goblin", level=1)
    
    @pytest.fixture
    def battle(self, sample_party, sample_enemy):
        """Crea una battaglia"""
        return Battle(sample_party, sample_enemy)
    
    def test_battle_initialization(self, battle):
        """Test inizializzazione battaglia"""
        assert battle.is_active is False  # Non ancora iniziata
        assert len(battle.battle_log) == 0
    
    def test_start_battle(self, battle):
        """Test inizio battaglia"""
        intro = battle.start_battle()
        
        assert battle.is_active is True
        assert isinstance(intro, str)
        assert len(intro) > 0
    
    def test_execute_player_attack(self, battle, sample_party):
        """Test attacco giocatore"""
        player = sample_party.characters[0]
        enemy_hp_before = battle.enemy.hp
        
        action = battle.execute_player_turn(player, "attack")
        
        assert action.action_type == "attack"
        assert action.actor == player.name
        assert battle.enemy.hp < enemy_hp_before
    
    def test_execute_player_heal(self, battle, sample_party):
        """Test cura giocatore"""
        player = sample_party.characters[0]
        player.hp = 50  # Riduci HP
        
        action = battle.execute_player_turn(player, "heal", player)
        
        assert action.action_type == "heal"
        assert player.hp > 50
    
    def test_execute_player_heal_ally(self, battle, sample_party):
        """Test cura alleato"""
        healer = sample_party.characters[0]
        target = sample_party.characters[1]
        target.hp = 30
        
        action = battle.execute_player_turn(healer, "heal", target)
        
        assert action.action_type == "heal"
        assert action.target == target.name
        assert target.hp > 30
    
    def test_execute_enemy_turn(self, battle, sample_party):
        """Test turno nemico"""
        # Salva HP iniziali
        initial_hp = {char.name: char.hp for char in sample_party.characters}
        
        action = battle.execute_enemy_turn()
        
        assert action.action_type == "attack"
        
        # Almeno un giocatore ha perso HP
        damaged = any(
            sample_party.characters[i].hp < initial_hp[char.name]
            for i, char in enumerate(sample_party.characters)
        )
        assert damaged or not any(p.is_alive for p in sample_party.characters)
    
    def test_check_battle_end_active(self, battle):
        """Test battaglia ancora attiva"""
        result = battle.check_battle_end()
        
        assert result is None
    
    def test_check_battle_end_victory(self, battle):
        """Test vittoria (nemico morto)"""
        battle.enemy.hp = 0
        battle.enemy.is_alive = False
        
        result = battle.check_battle_end()
        
        assert result is not None
        assert result.victory is True
        assert result.enemy_defeated is True
    
    def test_check_battle_end_defeat(self, battle, sample_party):
        """Test sconfitta (tutti i giocatori morti)"""
        for char in sample_party.characters:
            char.hp = 0
            char.is_alive = False
        
        result = battle.check_battle_end()
        
        assert result is not None
        assert result.victory is False
        assert result.game_over is True
    
    def test_get_current_state(self, battle):
        """Test ottenimento stato corrente"""
        state = battle.get_current_state()
        
        assert 'round' in state
        assert 'enemy' in state
        assert 'players' in state
        assert 'active' in state
        
        assert isinstance(state['enemy'], dict)
        assert isinstance(state['players'], list)
    
    def test_battle_log_records_actions(self, battle, sample_party):
        """Test che le azioni vengano registrate"""
        player = sample_party.characters[0]
        
        battle.execute_player_turn(player, "attack")
        
        assert len(battle.battle_log) == 1
        assert battle.battle_log[0].action_type == "attack"
    
    def test_get_battle_summary(self, battle):
        """Test riepilogo battaglia"""
        summary = battle.get_battle_summary()
        
        assert isinstance(summary, str)
        assert "RIEPILOGO" in summary
    
    def test_str_representation(self, battle):
        """Test rappresentazione stringa"""
        str_repr = str(battle)
        
        assert "Battle" in str_repr
        assert "Round" in str_repr


class TestBattleResult:
    """Test suite per BattleResult"""
    
    def test_victory_result(self):
        """Test risultato vittoria"""
        survivors = [
            Character(name="Hero1", character_class="guerriero"),
            Character(name="Hero2", character_class="mago")
        ]
        
        result = BattleResult(
            victory=True,
            survivors=survivors,
            enemy_defeated=True,
            rounds=5
        )
        
        assert result.victory is True
        assert len(result.survivors) == 2
        assert result.enemy_defeated is True
        assert result.rounds == 5
        assert result.game_over is False
    
    def test_defeat_result(self):
        """Test risultato sconfitta"""
        result = BattleResult(
            victory=False,
            survivors=[],
            enemy_defeated=False,
            rounds=3
        )
        
        assert result.victory is False
        assert len(result.survivors) == 0
        assert result.game_over is True


class TestBattleAction:
    """Test suite per BattleAction"""
    
    def test_battle_action_creation(self):
        """Test creazione azione"""
        action = BattleAction(
            action_type="attack",
            actor="Warrior",
            target="Goblin",
            value=25,
            message="Warrior attacks Goblin for 25 damage"
        )
        
        assert action.action_type == "attack"
        assert action.actor == "Warrior"
        assert action.target == "Goblin"
        assert action.value == 25
        assert "Warrior" in action.message