"""
Integration tests con file CSV di comandi
"""
import pytest
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Aggiungi la root del progetto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.party import Party
from models.character import Character
from core.input_manager import InputManager

class TestIntegrationCSV:
    """Test suite per integration testing con CSV"""

    @pytest.fixture
    def test_data_dir(self):
        """Fixture per la directory dei dati di test"""
        return Path(__file__).parent / "test_data"

    @pytest.fixture
    def test_results_dir(self):
        """Fixture per la directory dei risultati"""
        results_dir = Path(__file__).parent / "test_results"
        results_dir.mkdir(exist_ok=True)
        return results_dir

    @pytest.fixture
    def sample_party(self):
        """Crea un party di test"""
        party = Party()
        char1 = Character(name="TestHero1", character_class="guerriero")
        char2 = Character(name="TestHero2", character_class="mago")
        party.add_character(char1)
        party.add_character(char2)
        return party

    @pytest.fixture
    def input_manager(self):
        """Crea un input manager"""
        return InputManager()

    def test_csv_commands_execution(self, test_data_dir, test_results_dir, sample_party, input_manager):
        """Test esecuzione comandi da file CSV e salvataggio risultati in JSON"""
        csv_file = test_data_dir / "game_commands.csv"
        
        # Verifica che il file CSV esista
        if not csv_file.exists():
            pytest.skip(f"File CSV non trovato: {csv_file}")

        # Leggi i comandi dal CSV
        commands = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            commands = list(reader)

        # Risultati del test
        test_results = {
            "test_name": "csv_commands_execution",
            "timestamp": datetime.now().isoformat(),
            "total_commands": len(commands),
            "results": []
        }

        # Esegui ogni comando
        for i, row in enumerate(commands, 1):
            command_text = row.get('command', '').strip()
            expected_result = row.get('expected_result', '').strip()
            description = row.get('description', '').strip()

            # Parsea il comando
            parsed_cmd = input_manager.parse(command_text)

            # Prepara il risultato
            result = {
                "step": i,
                "command": command_text,
                "description": description,
                "expected": expected_result,
                "parsed": parsed_cmd is not None,
                "party_state_before": self._get_party_state(sample_party)
            }

            # Esegui il comando se valido
            if parsed_cmd:
                result["action"] = parsed_cmd.action
                result["target"] = parsed_cmd.target
                result["args"] = parsed_cmd.args
                
                # Simula l'esecuzione del comando
                execution_result = self._execute_command(parsed_cmd, sample_party)
                result["execution"] = execution_result
            else:
                result["execution"] = {"status": "failed", "reason": "Invalid command"}

            result["party_state_after"] = self._get_party_state(sample_party)
            test_results["results"].append(result)

        # Salva i risultati in JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"test_results_{timestamp}.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)

        # Verifica che almeno alcuni comandi siano stati eseguiti correttamente
        successful_commands = sum(1 for r in test_results["results"] if r["parsed"])
        assert successful_commands > 0, "Nessun comando è stato parsato correttamente"

        print(f"\n✓ Test completato: {successful_commands}/{len(commands)} comandi eseguiti")
        print(f"✓ Risultati salvati in: {output_file}")

    def _get_party_state(self, party):
        """Ottiene lo stato corrente del party"""
        return {
            "characters": [
                {
                    "name": char.name,
                    "class": char.character_class,
                    "hp": char.hp,
                    "max_hp": char.max_hp,
                    "is_alive": char.is_alive
                }
                for char in party.characters
            ]
        }

    def _execute_command(self, command, party):
        """Simula l'esecuzione di un comando"""
        try:
            if command.action == "status":
                return {"status": "success", "message": "Status displayed"}
                
            elif command.action == "atk":
                if not command.target:
                    return {"status": "failed", "reason": "No target specified"}
                    
                attacker = party.get_character(command.target)
                if not attacker:
                    return {"status": "failed", "reason": "Character not found"}
                if not attacker.is_alive:
                    return {"status": "failed", "reason": "Character is KO"}
                    
                # Trova un target casuale
                possible_targets = [c for c in party.characters if c != attacker and c.is_alive]
                if not possible_targets:
                    return {"status": "failed", "reason": "No valid targets"}
                    
                target = possible_targets[0]
                damage = 25  # Danno fisso per testing
                actual_damage = target.take_damage(damage)
                
                return {
                    "status": "success",
                    "attacker": attacker.name,
                    "target": target.name,
                    "damage": actual_damage,
                    "target_ko": not target.is_alive
                }
                
            elif command.action == "heal":
                if not command.target:
                    return {"status": "failed", "reason": "No target specified"}
                    
                healer = party.get_character(command.target)
                if not healer:
                    return {"status": "failed", "reason": "Character not found"}
                if not healer.is_alive:
                    return {"status": "failed", "reason": "Character is KO"}
                    
                heal_amount = 20
                if command.args and command.args[0].isdigit():
                    heal_amount = int(command.args[0])
                    
                actual_heal = healer.heal(heal_amount)
                
                return {
                    "status": "success",
                    "healer": healer.name,
                    "heal_amount": actual_heal
                }
            else:
                return {"status": "success", "message": f"Command {command.action} acknowledged"}
                
        except Exception as e:
            return {"status": "error", "exception": str(e)}

    def test_save_party_snapshot(self, test_results_dir, sample_party):
        """Test salvataggio snapshot del party in JSON"""
        # Modifica lo stato del party
        sample_party.characters[0].take_damage(30)
        sample_party.characters[1].heal(10)

        # Crea lo snapshot
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "party": self._get_party_state(sample_party)
        }

        # Salva in JSON
        output_file = test_results_dir / "party_snapshot.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        # Verifica che il file esista
        assert output_file.exists()

        # Rileggi e verifica
        with open(output_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)

        assert "party" in loaded
        assert len(loaded["party"]["characters"]) == 2

        print(f"\n✓ Snapshot salvato in: {output_file}")
