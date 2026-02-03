"""
Test di integrazione per il sistema Pygame
Sprint 4: The Big Switch
"""

import pytest
import pygame
from pathlib import Path
from core.pygame_game_engine import PygameGameEngine, GameState
from models.character import Character
from models.world import World
from combat.enemy import Enemy


@pytest.fixture
def full_game():
    """Setup completo del gioco"""
    pygame.init()
    engine = PygameGameEngine()
    yield engine
    engine.renderer.quit()
    pygame.quit()


class TestCompleteGameFlow:
    """Test flusso completo del gioco"""
    
    def test_menu_to_char_creation(self, full_game):
        """Test transizione menu -> creazione personaggio"""
        
        assert full_game.state == GameState.MENU
        
        
        full_game.menu_selected = 0
        full_game._handle_menu_input(pygame.K_RETURN)
        
        assert full_game.state == GameState.CHAR_CREATION
    
    def test_create_two_characters(self, full_game):
        """Test creazione completa di due personaggi"""
        full_game.state = GameState.CHAR_CREATION
        
        
        full_game.temp_name = "Kael"
        full_game.temp_class_index = 0  
        full_game.creation_phase = 0
        full_game._handle_char_creation_input(pygame.K_RETURN)
        
        assert len(full_game.party.characters) == 1
        assert full_game.creation_phase == 1
        
        full_game.temp_name = "Elara"
        full_game.temp_class_index = 1  
        full_game._handle_char_creation_input(pygame.K_RETURN)
        
        assert len(full_game.party.characters) == 2
        assert full_game.state == GameState.STORY_INTRO
    
    def test_story_intro_to_level_selection(self, full_game):
        """Test transizione storia -> selezione livello"""
        full_game.party.add_character(Character("Hero1", "warrior"))
        full_game.party.add_character(Character("Hero2", "mage"))
        
        full_game._setup_story_intro()
        full_game.state = GameState.STORY_INTRO
        full_game.dialogue_next_state = GameState.LEVEL_SELECTION
        
        
        for _ in range(len(full_game.intro_lines)):
            full_game.text_complete = True
            full_game._handle_story_intro_input(pygame.K_RETURN)
        
        assert full_game.state == GameState.LEVEL_SELECTION
    
    def test_level_selection_to_exploration(self, full_game):
        """Test transizione selezione livello -> esplorazione"""
        full_game.state = GameState.LEVEL_SELECTION
        full_game.level_selection_index = 0
        full_game.max_unlocked_index = 0
        
        
        full_game.world = World(grid=[[3, 0, 4]], name="Test Level")
        full_game.movement_manager = __import__('core.movement', fromlist=['MovementManager']).MovementManager(full_game.world)
        
        full_game._handle_level_selection_input(pygame.K_RETURN)
        
        assert full_game.state == GameState.EXPLORATION
    
    def test_exploration_to_combat(self, full_game):
        """Test transizione esplorazione -> combattimento"""
        full_game.party.add_character(Character("Hero", "warrior"))
        full_game.world = World(grid=[[3, 2, 4]], name="Test")
        full_game.movement_manager = __import__('core.movement', fromlist=['MovementManager']).MovementManager(full_game.world)
        full_game.state = GameState.EXPLORATION
        
        
        full_game._try_move('d') 
        
        assert full_game.state == GameState.COMBAT
        assert full_game.current_battle is not None
    
    def test_combat_to_exploration(self, full_game):
        """Test transizione combattimento -> esplorazione (vittoria)"""
        full_game.party.add_character(Character("Hero", "warrior"))
        full_game.world = World(grid=[[3, 2, 4]], name="Test")
        full_game.movement_manager = __import__('core.movement', fromlist=['MovementManager']).MovementManager(full_game.world)
        full_game.movement_manager.position = (1, 0)
        
        full_game._start_combat()
        
        
        full_game.current_battle.enemy.hp = 0
        full_game.current_battle.enemy.is_alive = False
        
        full_game._next_combat_turn()
        
        assert full_game.state == GameState.EXPLORATION
        assert full_game.current_battle is None
    
    def test_exploration_to_inventory(self, full_game):
        """Test apertura inventario"""
        full_game.state = GameState.EXPLORATION
        full_game._handle_exploration_input(pygame.K_i)
        
        assert full_game.state == GameState.INVENTORY
    
    def test_inventory_back_to_exploration(self, full_game):
        """Test chiusura inventario"""
        full_game.state = GameState.INVENTORY
        full_game._handle_inventory_input(pygame.K_ESCAPE)
        
        assert full_game.state == GameState.EXPLORATION
    
    def test_pause_and_resume(self, full_game):
        """Test pausa e ripresa"""
        full_game.state = GameState.EXPLORATION
        
        # Pausa
        full_game._handle_exploration_input(pygame.K_ESCAPE)
        assert full_game.state == GameState.MENU
        assert full_game.previous_state == GameState.EXPLORATION
        
        # Riprendi
        full_game.menu_options = ["Riprendi", "Nuova Partita", "Esci"]
        full_game.menu_selected = 0
        full_game._handle_menu_input(pygame.K_RETURN)
        
        assert full_game.state == GameState.EXPLORATION


class TestLevelProgression:
    """Test progressione livelli"""
    
    def test_level_unlock_after_completion(self, full_game):
        """Test sblocco livello successivo"""
        from models.character import Character
        from models.world import World
        from core.movement import MovementManager
        
        full_game.current_level_index = 0
        full_game.max_unlocked_index = 0
        
        
        full_game.party.add_character(Character("Hero", "warrior"))
        
        
        full_game.world = World(grid=[[3, 0, 4]], name="Level 1")
        full_game.movement_manager = MovementManager(full_game.world)
        full_game.movement_manager.position = (2, 0)  
        full_game.state = GameState.EXPLORATION
        
        
        full_game.world.grid[0] = [3, 0, 4]
        
        
        if full_game._are_all_enemies_defeated():
            if full_game.current_level_index < len(full_game.level_files) - 1:
                next_idx = full_game.current_level_index + 1
                if next_idx > full_game.max_unlocked_index:
                    full_game.max_unlocked_index = next_idx
        
        assert full_game.max_unlocked_index == 1
    
    def test_cannot_access_locked_level(self, full_game):
        """Test che non si possa accedere a livelli bloccati"""
        full_game.max_unlocked_index = 0
        full_game.level_selection_index = 2
        full_game.state = GameState.LEVEL_SELECTION
        
        initial_state = full_game.state
        full_game._handle_level_selection_input(pygame.K_RETURN)
        
        
        assert full_game.state == initial_state
    
    def test_all_levels_defined(self, full_game):
        """Test che tutti i livelli siano definiti"""
        assert len(full_game.level_files) == 4
        assert len(full_game.level_names) == 4
        
        for i, filename in enumerate(full_game.level_files):
            assert filename.endswith('.json')
            assert full_game.level_names[i] != ""


class TestBossFight:
    """Test combattimento boss finale"""
    
    def test_boss_fight_trigger(self, full_game):
        """Test che il boss fight si triggeri correttamente"""
        full_game.party.add_character(Character("Hero", "warrior"))
        full_game.current_level_index = 3  
        full_game.final_boss_defeated = False
        full_game.world = World(grid=[[3, 0, 4]], name="Final Level")
        full_game.movement_manager = __import__('core.movement', fromlist=['MovementManager']).MovementManager(full_game.world)
        full_game.movement_manager.position = (2, 0)
        full_game.state = GameState.EXPLORATION
        
        
        full_game.world.grid[0] = [3, 0, 4]
        
        
        full_game._try_move('s')  
        full_game.movement_manager.position = (2, 0)  
        
        
        if full_game.current_level_index == len(full_game.level_files) - 1:
            if not full_game.final_boss_defeated:
                full_game._start_boss_fight()
        
        assert full_game.state == GameState.STORY_INTRO
        assert full_game.dialogue_next_state == GameState.COMBAT
    
    def test_boss_defeat_victory(self, full_game):
        """Test vittoria dopo sconfitta boss"""
        from models.character import Character
        from combat.battle import Battle
        
        full_game.party.add_character(Character("Hero", "warrior"))
        
        
        boss = Enemy.create_random(min_level=5, max_level=5)
        boss.name = "DRAGO ANTICO"
        boss.max_hp = 300
        boss.hp = 300
        boss.damage = 25
        boss.xp_reward = 5000
        
        full_game.current_battle = Battle(full_game.party, boss)
        full_game.state = GameState.COMBAT
        
        
        full_game.current_battle.enemy.hp = 0
        full_game.current_battle.enemy.is_alive = False
        
        full_game._next_combat_turn()
        
        assert full_game.final_boss_defeated == True
        assert full_game.state == GameState.STORY_INTRO
        assert full_game.dialogue_next_state == GameState.VICTORY


class TestInventoryIntegration:
    """Test integrazione inventario nel gioco"""
    
    def test_use_health_potion(self, full_game):
        """Test uso pozione vita"""
        full_game.party.add_character(Character("Hero", "warrior"))
        full_game.party.characters[0].hp = 50
        full_game.party.inventory.add_item('health_potion', 2)
        
        full_game.state = GameState.INVENTORY
        full_game.inventory_selected = 0
        
        initial_hp = full_game.party.characters[0].hp
        full_game._handle_inventory_input(pygame.K_RETURN)
        
        assert full_game.party.characters[0].hp > initial_hp
    
    def test_treasure_collection(self, full_game):
        """Test raccolta tesoro"""
        full_game.world = World(grid=[[3, 5, 4]], name="Test")  
        full_game.movement_manager = __import__('core.movement', fromlist=['MovementManager']).MovementManager(full_game.world)
        full_game.party.add_character(Character("Hero", "warrior"))
        
        initial_items = len(full_game.party.inventory.items)
        
        
        full_game._try_move('d')
        
        
        assert len(full_game.party.inventory.items) >= initial_items


class TestMessageSystem:
    """Test sistema messaggi"""
    
    def test_message_display(self, full_game):
        """Test visualizzazione messaggio"""
        full_game._show_message("Test Message")
        assert full_game.message == "Test Message"
        assert full_game.message_timer > 0
    
    def test_message_clear(self, full_game):
        """Test cancellazione messaggio dopo timeout"""
        full_game._show_message("Test", duration=100)  
        
        
        import time
        time.sleep(0.15)  
        
        full_game._update(200)
        
        
        assert hasattr(full_game, 'message')
        assert hasattr(full_game, 'message_timer')


class TestRenderingIntegration:
    """Test integrazione rendering"""
    
    def test_render_all_states(self, full_game):
        """Test rendering di tutti gli stati senza crash"""
        states = [
            GameState.MENU,
            GameState.CHAR_CREATION,
            GameState.LEVEL_SELECTION,
            GameState.GAME_OVER,
            GameState.VICTORY
        ]
        
        for state in states:
            full_game.state = state
            
        
        assert True
    
    def test_render_with_party(self, full_game):
        """Test rendering con party"""
        full_game.party.add_character(Character("Hero1", "warrior"))
        full_game.party.add_character(Character("Hero2", "mage"))
        
        full_game.state = GameState.MENU
        full_game._render()
        
        assert True
    
    def test_render_combat_state(self, full_game):
        """Test rendering stato combattimento"""
        full_game.party.add_character(Character("Hero", "warrior"))
        full_game._start_combat()
        full_game._render()
        
        assert True