"""
Integration tests per il sistema di inventario (Sprint 3)
"""

import pytest
import json
from datetime import datetime
from pathlib import Path
from models.party import Party
from models.character import Character
from models.inventory import Inventory
from combat.enemy import Enemy
from combat.battle import Battle


class TestInventoryIntegration:
    """Test suite per integrazione inventario"""
    
    @pytest.fixture
    def test_results_dir(self):
        """Directory per i risultati"""
        results_dir = Path(__file__).parent / "test_results"
        results_dir.mkdir(exist_ok=True)
        return results_dir
    
    @pytest.fixture
    def sample_party(self):
        """Crea un party con inventario"""
        party = Party()
        warrior = Character(name="Warrior", character_class="guerriero")
        mage = Character(name="Mage", character_class="mago")
        party.add_character(warrior)
        party.add_character(mage)
        
        # Aggiungi oggetti
        party.inventory.add_item('health_potion', 3)
        party.inventory.add_item('mana_potion', 2)
        party.inventory.add_item('bomb', 1)
        
        return party
    
    def test_class_modifiers(self, test_results_dir):
        """Test modificatori di classe"""
        warrior = Character(name="TestWarrior", character_class="guerriero")
        mage = Character(name="TestMage", character_class="mago")
        
        results = {
            "test_name": "class_modifiers",
            "timestamp": datetime.now().isoformat(),
            "classes": []
        }
        
        for char in [warrior, mage]:
            class_data = {
                "name": char.name,
                "class": char.character_class,
                "hp": char.hp,
                "max_hp": char.max_hp,
                "mp": char.mp,
                "max_mp": char.max_mp,
                "atk_bonus": char.atk_bonus,
                "def_bonus": char.def_bonus,
                "mag_bonus": char.mag_bonus
            }
            results["classes"].append(class_data)
        
        # Verifica modificatori
        assert warrior.atk_bonus > mage.atk_bonus
        assert mage.mag_bonus > warrior.mag_bonus
        assert warrior.hp > mage.hp
        assert mage.mp > warrior.mp
        
        # Salva risultati
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"class_modifiers_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Modificatori di classe verificati")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_inventory_usage_in_combat(self, sample_party, test_results_dir):
        """Test uso inventario in combattimento"""
        enemy = Enemy(enemy_type="goblin", level=1)
        battle = Battle(sample_party, enemy)
        
        results = {
            "test_name": "inventory_usage_combat",
            "timestamp": datetime.now().isoformat(),
            "initial_inventory": sample_party.inventory.to_dict(),
            "actions": []
        }
        
        battle.start_battle()
        warrior = sample_party.characters[0]
        
        # Test uso pozione vita
        warrior.hp = 50
        action = battle.execute_player_turn(warrior, "use_item", warrior, "health_potion")
        
        results["actions"].append({
            "action": "use_health_potion",
            "success": action.action_type == "use_item",
            "warrior_hp_after": warrior.hp,
            "inventory_after": sample_party.inventory.get_item_count('health_potion')
        })
        
        assert warrior.hp > 50
        assert sample_party.inventory.get_item_count('health_potion') == 2
        
        # Test uso bomba
        initial_enemy_hp = enemy.hp
        action = battle.execute_player_turn(warrior, "use_item", None, "bomb")
        
        results["actions"].append({
            "action": "use_bomb",
            "success": action.action_type == "use_item",
            "enemy_hp_before": initial_enemy_hp,
            "enemy_hp_after": enemy.hp,
            "inventory_after": sample_party.inventory.get_item_count('bomb')
        })
        
        assert enemy.hp < initial_enemy_hp
        assert sample_party.inventory.get_item_count('bomb') == 0
        
        results["final_inventory"] = sample_party.inventory.to_dict()
        
        # Salva risultati
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"inventory_combat_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Uso inventario in combattimento verificato")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_physical_vs_magic_damage(self, test_results_dir):
        """Test differenza danno fisico vs magico"""
        warrior = Character(name="Warrior", character_class="guerriero")
        mage = Character(name="Mage", character_class="mago")
        
        results = {
            "test_name": "physical_vs_magic_damage",
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
        
        # Test 10 attacchi per tipo
        for i in range(10):
            phys_dmg = warrior.calculate_physical_damage()
            mag_dmg = mage.calculate_magic_damage()
            
            results["tests"].append({
                "round": i + 1,
                "warrior_physical": phys_dmg,
                "mage_magic": mag_dmg
            })
        
        # Calcola medie
        avg_phys = sum(t["warrior_physical"] for t in results["tests"]) / 10
        avg_mag = sum(t["mage_magic"] for t in results["tests"]) / 10
        
        results["averages"] = {
            "warrior_physical_avg": avg_phys,
            "mage_magic_avg": avg_mag,
            "warrior_atk_bonus": warrior.atk_bonus,
            "mage_mag_bonus": mage.mag_bonus
        }
        
        # Salva risultati
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"damage_comparison_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Il guerriero dovrebbe fare più danno fisico
        assert avg_phys > avg_mag - mage.mag_bonus
        
        print(f"\n✓ Danno fisico medio (Guerriero): {avg_phys:.1f}")
        print(f"✓ Danno magico medio (Mago): {avg_mag:.1f}")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_mp_system(self, test_results_dir):
        """Test sistema MP"""
        mage = Character(name="Mage", character_class="mago")
        
        results = {
            "test_name": "mp_system",
            "timestamp": datetime.now().isoformat(),
            "initial_mp": mage.mp,
            "max_mp": mage.max_mp,
            "actions": []
        }
        
        # Test uso MP
        initial_mp = mage.mp
        success = mage.use_mp(10)
        
        results["actions"].append({
            "action": "use_mp",
            "amount": 10,
            "success": success,
            "mp_after": mage.mp
        })
        
        assert success is True
        assert mage.mp == initial_mp - 10
        
        # Test ripristino MP
        restored = mage.restore_mp(5)
        
        results["actions"].append({
            "action": "restore_mp",
            "amount": 5,
            "restored": restored,
            "mp_after": mage.mp
        })
        
        assert restored == 5
        
        # Test uso MP insufficienti
        mage.mp = 5
        success = mage.use_mp(10)
        
        results["actions"].append({
            "action": "use_mp_insufficient",
            "amount": 10,
            "success": success,
            "mp_before": 5
        })
        
        assert success is False
        
        results["final_mp"] = mage.mp
        
        # Salva risultati
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"mp_system_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Sistema MP verificato")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_shared_inventory(self, sample_party, test_results_dir):
        """Test inventario condiviso tra personaggi"""
        results = {
            "test_name": "shared_inventory",
            "timestamp": datetime.now().isoformat(),
            "initial_state": sample_party.inventory.to_dict()
        }
        
        # Entrambi i personaggi usano lo stesso inventario
        warrior = sample_party.characters[0]
        mage = sample_party.characters[1]
        
        # Warrior usa pozione
        warrior.hp = 50
        initial_count = sample_party.inventory.get_item_count('health_potion')
        sample_party.inventory.use_item('health_potion')
        
        # Mage vede lo stesso inventario
        count_after = sample_party.inventory.get_item_count('health_potion')
        
        results["test"] = {
            "initial_count": initial_count,
            "count_after_warrior_use": count_after,
            "shared": count_after == initial_count - 1
        }
        
        assert count_after == initial_count - 1
        
        results["final_state"] = sample_party.inventory.to_dict()
        
        # Salva risultati
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"shared_inventory_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Inventario condiviso verificato")
        print(f"✓ Risultati salvati in: {output_file}")