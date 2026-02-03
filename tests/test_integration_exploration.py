"""
Integration tests per il sistema di esplorazione (Sprint 1)
"""

import pytest
import json
from datetime import datetime
from pathlib import Path
from models.world import World, CellType
from core.movement import MovementManager


class TestExplorationIntegration:
    """Test suite per integrazione esplorazione"""
    
    @pytest.fixture
    def test_results_dir(self):
        """Directory per i risultati"""
        results_dir = Path(__file__).parent / "test_results"
        results_dir.mkdir(exist_ok=True)
        return results_dir
    
    @pytest.fixture
    def dungeon_world(self):
        """Crea un dungeon completo per i test"""
        grid = [
            [3, 0, 1, 0, 4],
            [0, 1, 1, 0, 0],
            [0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0],
            [0, 0, 1, 5, 0]
        ]
        return World(grid=grid, name="Test Dungeon")
    
    def test_complete_dungeon_exploration(self, dungeon_world, test_results_dir):
        """Test esplorazione completa di un dungeon"""
        manager = MovementManager(dungeon_world)
        
        
        commands = ['d', 's', 's', 'd', 's', 'd', 'd', 'w', 'w', 'd']
        
        results = {
            "test_name": "complete_dungeon_exploration",
            "timestamp": datetime.now().isoformat(),
            "dungeon": dungeon_world.name,
            "start_position": manager.get_position(),
            "movements": []
        }
        
        for i, cmd in enumerate(commands, 1):
            pos_before = manager.get_position()
            result = manager.move(cmd)
            pos_after = manager.get_position()
            
            movement_data = {
                "step": i,
                "command": cmd,
                "position_before": pos_before,
                "position_after": pos_after,
                "success": result.success,
                "message": result.message,
                "trigger": result.trigger
            }
            
            results["movements"].append(movement_data)
        
        results["final_position"] = manager.get_position()
        results["total_successful_moves"] = sum(1 for m in results["movements"] if m["success"])
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"exploration_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        
        assert results["total_successful_moves"] > 0
        assert output_file.exists()
        
        print(f"\n✓ Esplorazione completata: {results['total_successful_moves']}/{len(commands)} movimenti riusciti")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_collision_detection(self, dungeon_world, test_results_dir):
        """Test rilevamento collisioni con muri"""
        manager = MovementManager(dungeon_world)
        
        
        collision_tests = [
            {'from': (0, 0), 'command': 'w', 'expected': 'OUT_OF_BOUNDS'},
            {'from': (0, 0), 'command': 'a', 'expected': 'OUT_OF_BOUNDS'},
            {'from': (1, 0), 'command': 'w', 'expected': 'OUT_OF_BOUNDS'},
            {'from': (1, 0), 'command': 'd', 'expected': 'WALL'},
        ]
        
        results = {
            "test_name": "collision_detection",
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
        
        for test in collision_tests:
            manager.position_x, manager.position_y = test['from']
            result = manager.move(test['command'])
            
            test_result = {
                "from": test['from'],
                "command": test['command'],
                "expected_block": test['expected'],
                "blocked": not result.success,
                "message": result.message,
                "passed": not result.success
            }
            
            results["tests"].append(test_result)
        
        results["all_passed"] = all(t["passed"] for t in results["tests"])
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"collision_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        assert results["all_passed"]
        
        print(f"\n✓ Test collisioni: {len(results['tests'])}/{len(results['tests'])} passati")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_trigger_detection(self, dungeon_world, test_results_dir):
        """Test rilevamento trigger (DANGER, EXIT, TREASURE)"""
        manager = MovementManager(dungeon_world)
        
        
        trigger_cells = []
        for y in range(dungeon_world.height):
            for x in range(dungeon_world.width):
                cell = dungeon_world.get_cell(x, y)
                if cell in [CellType.DANGER.value, CellType.EXIT.value, CellType.TREASURE.value]:
                    trigger_cells.append({
                        'position': (x, y),
                        'type': dungeon_world.get_cell_type_name(x, y)
                    })
        
        results = {
            "test_name": "trigger_detection",
            "timestamp": datetime.now().isoformat(),
            "trigger_cells": trigger_cells,
            "detected_triggers": []
        }
        
        
        for cell_info in trigger_cells:
            x, y = cell_info['position']
            
            manager.position_x = max(0, x - 1)
            manager.position_y = y
            
            
            if x > manager.position_x:
                result = manager.move('d')
            elif x < manager.position_x:
                result = manager.move('a')
            elif y > manager.position_y:
                result = manager.move('s')
            else:
                result = manager.move('w')
            
            if result.success and manager.get_position() == (x, y):
                results["detected_triggers"].append({
                    "position": (x, y),
                    "expected_type": cell_info['type'],
                    "trigger": result.trigger,
                    "message": result.message,
                    "matched": result.trigger is not None
                })
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"trigger_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        
        detected_count = sum(1 for t in results["detected_triggers"] if t["matched"])
        assert detected_count > 0
        
        print(f"\n✓ Trigger rilevati: {detected_count}/{len(trigger_cells)}")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_map_loading_and_navigation(self, test_results_dir):
        """Test caricamento mappa da file e navigazione"""
        
        map_path = Path("data/maps/map_01.json")
        
        if not map_path.exists():
            pytest.skip("Map file not found")
        
        
        world = World.load_from_file(str(map_path))
        manager = MovementManager(world)
        
        results = {
            "test_name": "map_loading_navigation",
            "timestamp": datetime.now().isoformat(),
            "map_file": str(map_path),
            "map_name": world.name,
            "map_size": {"width": world.width, "height": world.height},
            "start_position": manager.get_position(),
            "test_movements": []
        }
        
        
        test_moves = ['d', 's', 'a', 'w']
        for cmd in test_moves:
            result = manager.move(cmd)
            results["test_movements"].append({
                "command": cmd,
                "success": result.success,
                "position": manager.get_position()
            })
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"map_loading_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        assert world.width > 0
        assert world.height > 0
        
        print(f"\n✓ Mappa caricata: {world.name} ({world.width}x{world.height})")
        print(f"✓ Risultati salvati in: {output_file}")
    
    def test_pathfinding_to_exit(self, dungeon_world, test_results_dir):
        """Test percorso dall'inizio all'uscita"""
        manager = MovementManager(dungeon_world)
        
        
        exit_pos = None
        for y in range(dungeon_world.height):
            for x in range(dungeon_world.width):
                if dungeon_world.get_cell(x, y) == CellType.EXIT.value:
                    exit_pos = (x, y)
                    break
            if exit_pos:
                break
        
        if not exit_pos:
            pytest.skip("No exit found in map")
        
        
        path = ['d', 's', 's', 's', 'd', 'd', 'd', 'w', 'w', 'w']
        
        results = {
            "test_name": "pathfinding_to_exit",
            "timestamp": datetime.now().isoformat(),
            "start": manager.get_position(),
            "exit_position": exit_pos,
            "path_attempted": path,
            "movements": []
        }
        
        for cmd in path:
            result = manager.move(cmd)
            results["movements"].append({
                "command": cmd,
                "success": result.success,
                "position": manager.get_position(),
                "reached_exit": manager.get_position() == exit_pos
            })
            
            if manager.get_position() == exit_pos:
                break
        
        results["reached_exit"] = manager.get_position() == exit_pos
        
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = test_results_dir / f"pathfinding_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Test pathfinding: Uscita {'raggiunta' if results['reached_exit'] else 'non raggiunta'}")
        print(f"✓ Risultati salvati in: {output_file}")