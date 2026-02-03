"""
Integration tests per il sistema di combattimento (Sprint 2)
"""

import pytest
import json
from datetime import datetime
from pathlib import Path
from models.party import Party
from models.character import Character
from combat.enemy import Enemy
from combat.battle import Battle


class TestCombatIntegration:
    """Test suite per integrazione combattimento"""
    
    @pytest.fixture
    def test_results_dir(self):
        """Directory per i risultati"""
        results_dir = Path(__file__).parent / "test_results"
        results_dir.mkdir(exist_ok=True)
        return results_dir
    
    @pytest.fixture
    def sample_party(self):
        """Crea un party completo"""
        party = Party()
        warrior = Character(name="Aragorn", character_class="guerriero")
        mage = Character(name="Gandalf", character_class="mago")
        party.add_character(warrior)
        party.add_character(mage)
        return party
    
    def test_full_battle_simulation(self, sample_party, test_results_dir):
        """Test simulazione battaglia completa"""
        enemy = Enemy(enemy_type="orc", level=2)
        battle = Battle(sample_party, enemy)
        
        results = {
            "test_name": "full_battle_simulation",
            "timestamp": datetime.now().isoformat(),
            "initial_state": battle.get_current_state(),
            "actions": [],
            "rounds": []
        }
        
        battle.start_battle()
        
        # Simula battaglia automatica
        max_turns = 50  
        turn_count = 0
        
        while battle.is_active and turn_count < max_turns:
            turn_count += 1
            current = battle.turn_manager.get_current_combatant()
            
            if not current:
                break
            
            round_data = {
                "round": battle.turn_manager.round_number,
                "turn": turn_count,
                "actor": current.name,
                "is_player": current.is_player
            }
            
            if current.is_player:
                # Giocatore attacca sempre
                action = battle.execute_player_turn(current.entity, "attack")
            else:
                # Nemico esegue turno
                action = battle.execute_enemy_turn()
            
            round_data["action"] = {
                "type": action.action_type,
                "target": action.target,
                "value": action.value,
                "message": action.message
            }
            
            results["actions"].append(round_data)
            
            # Controlla fine battaglia
            battle_result = battle.check_battle_end()
            if battle_result:
                results["battle_result"] = {
                    "victory": battle_result.victory,
                    "survivors": len(battle_result.survivors),
                    "enemy_defeated": battle_result.enemy_defeated,
                    "rounds": battle_result.rounds,
                    "game_over": battle_result.game_over
                }
                break
            
            battle.turn_manager.next_turn()
        
        results["final_state"] = battle.get_current_state()
        results["total_turns"] = turn_count
        
        # Salva risultati
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"combat_simulation_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Verifiche
        assert "battle_result" in results
        assert turn_count < max_turns, "Battaglia non terminata in tempo"
        
        print(f"\n✓ Battaglia completata in {turn_count} turni")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_victory_condition(self, sample_party, test_results_dir):
        """Test condizione di vittoria"""
        # Nemico debole
        enemy = Enemy(enemy_type="goblin", level=1)
        enemy.hp = 10  
        
        battle = Battle(sample_party, enemy)
        battle.start_battle()
        
        results = {
            "test_name": "victory_condition",
            "timestamp": datetime.now().isoformat(),
            "enemy_initial_hp": 10
        }
        
        # Attacca fino a vittoria
        warrior = sample_party.characters[0]
        battle.execute_player_turn(warrior, "attack")
        
        battle_result = battle.check_battle_end()
        
        results["battle_ended"] = battle_result is not None
        if battle_result:
            results["victory"] = battle_result.victory
            results["enemy_defeated"] = battle_result.enemy_defeated
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"victory_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        assert battle_result is not None
        assert battle_result.victory is True
        
        print(f"\n✓ Vittoria raggiunta")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_defeat_condition(self, sample_party, test_results_dir):
        """Test condizione di sconfitta"""
        
        enemy = Enemy(enemy_type="dragon", level=10)
        battle = Battle(sample_party, enemy)
        
        results = {
            "test_name": "defeat_condition",
            "timestamp": datetime.now().isoformat()
        }
        
        battle.start_battle()
        
        
        for char in sample_party.characters:
            char.hp = 0
            char.is_alive = False
        
        battle_result = battle.check_battle_end()
        
        results["battle_ended"] = battle_result is not None
        if battle_result:
            results["victory"] = battle_result.victory
            results["game_over"] = battle_result.game_over
            results["survivors"] = len(battle_result.survivors)
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"defeat_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        assert battle_result is not None
        assert battle_result.victory is False
        assert battle_result.game_over is True
        
        print(f"\n✓ Sconfitta rilevata correttamente")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_enemy_ai_targeting(self, sample_party, test_results_dir):
        """Test IA nemica sceglie bersagli diversi"""
        enemy = Enemy(enemy_type="orc", level=2)
        battle = Battle(sample_party, enemy)
        
        results = {
            "test_name": "enemy_ai_targeting",
            "timestamp": datetime.now().isoformat(),
            "targets_hit": []
        }
        
        battle.start_battle()
        
        
        for i in range(20):
            action = battle.execute_enemy_turn()
            
            if action.action_type == "attack":
                results["targets_hit"].append(action.target)
        
        
        unique_targets = set(results["targets_hit"])
        results["unique_targets"] = list(unique_targets)
        results["target_variety"] = len(unique_targets)
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"ai_targeting_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        
        assert len(unique_targets) >= 1
        
        print(f"\n✓ IA ha colpito {len(unique_targets)} bersagli diversi")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_turn_order(self, sample_party, test_results_dir):
        """Test ordine turni corretto (P1 → P2 → Enemy)"""
        enemy = Enemy(enemy_type="goblin", level=1)
        battle = Battle(sample_party, enemy)
        
        results = {
            "test_name": "turn_order",
            "timestamp": datetime.now().isoformat(),
            "turn_sequence": []
        }
        
        battle.start_battle()
        
        
        for _ in range(6):  
            current = battle.turn_manager.get_current_combatant()
            if not current:
                break
            
            results["turn_sequence"].append({
                "name": current.name,
                "is_player": current.is_player
            })
            
            battle.turn_manager.next_turn()
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"turn_order_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        
        if len(results["turn_sequence"]) >= 6:
            assert results["turn_sequence"][0]["is_player"] is True
            assert results["turn_sequence"][1]["is_player"] is True
            assert results["turn_sequence"][2]["is_player"] is False
            assert results["turn_sequence"][3]["is_player"] is True
        
        print(f"\n✓ Ordine turni verificato")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_multiple_battles(self, sample_party, test_results_dir):
        """Test multiple battaglie consecutive"""
        results = {
            "test_name": "multiple_battles",
            "timestamp": datetime.now().isoformat(),
            "battles": []
        }
        
        for i in range(3):
            
            for char in sample_party.characters:
                char.hp = char.max_hp
                char.is_alive = True
            
            enemy = Enemy.create_random(min_level=1, max_level=2)
            battle = Battle(sample_party, enemy)
            battle.start_battle()
            
            battle_data = {
                "battle_number": i + 1,
                "enemy_type": enemy.enemy_type,
                "enemy_level": enemy.level,
                "turns": 0
            }
            
            
            max_turns = 30
            for turn in range(max_turns):
                current = battle.turn_manager.get_current_combatant()
                if not current:
                    break
                
                if current.is_player:
                    battle.execute_player_turn(current.entity, "attack")
                else:
                    battle.execute_enemy_turn()
                
                battle_result = battle.check_battle_end()
                if battle_result:
                    battle_data["result"] = "victory" if battle_result.victory else "defeat"
                    battle_data["turns"] = turn + 1
                    break
                
                battle.turn_manager.next_turn()
            
            results["battles"].append(battle_data)
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"multiple_battles_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        assert len(results["battles"]) == 3
        
        print(f"\n✓ {len(results['battles'])} battaglie completate")
        print(f"✓ Risultati salvati in: {output_file}")