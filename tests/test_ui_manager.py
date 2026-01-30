"""
Test per l'UI Manager
Sprint 4: The Big Switch
"""

import pytest
import pygame
from rendering.renderer import Renderer, Color
from rendering.ui_manager import UIManager
from models.party import Party
from models.character import Character
from combat.enemy import Enemy


@pytest.fixture
def setup_pygame():
    """Setup e cleanup Pygame"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def renderer(setup_pygame):
    """Fixture per il renderer"""
    return Renderer(width=1024, height=768, title="Test UI")


@pytest.fixture
def ui_manager(renderer):
    """Fixture per l'UI Manager"""
    return UIManager(renderer)


@pytest.fixture
def test_party():
    """Crea un party di test"""
    party = Party()
    char1 = Character(name="Kael", character_class="warrior")
    char1.hp = 80
    char1.max_hp = 100
    char1.mp = 20
    char1.max_mp = 30
    
    char2 = Character(name="Elara", character_class="mage")
    char2.hp = 50
    char2.max_hp = 70
    char2.mp = 60
    char2.max_mp = 80
    
    party.add_character(char1)
    party.add_character(char2)
    return party


@pytest.fixture
def test_enemy():
    """Crea un nemico di test"""
    enemy = Enemy.create_random(min_level=1, max_level=2)
    enemy.name = "Goblin"
    return enemy


class TestUIManager:
    """Test per l'UI Manager"""
    
    def test_initialization(self, ui_manager, renderer):
        """Test inizializzazione UI Manager"""
        assert ui_manager.renderer == renderer
    
    def test_draw_combat_ui_split_screen(self, ui_manager, test_party, test_enemy):
        """Test UI combattimento split screen"""
        ui_manager.renderer.clear()
        ui_manager.draw_combat_ui_split_screen(
            test_party, 
            test_enemy, 
            current_turn="Kael"
        )
        # Verifica che non ci siano eccezioni
        assert True
    
    def test_draw_combat_ui_no_active_turn(self, ui_manager, test_party, test_enemy):
        """Test UI combattimento senza turno attivo"""
        ui_manager.renderer.clear()
        ui_manager.draw_combat_ui_split_screen(
            test_party, 
            test_enemy, 
            current_turn=None
        )
        assert True
    
    def test_draw_combat_ui_enemy_turn(self, ui_manager, test_party, test_enemy):
        """Test UI combattimento durante turno nemico"""
        ui_manager.renderer.clear()
        ui_manager.draw_combat_ui_split_screen(
            test_party, 
            test_enemy, 
            current_turn="EnemyTurn"
        )
        assert True
    
    def test_draw_stat_bar_labeled(self, ui_manager):
        """Test disegno barra statistica con etichetta"""
        ui_manager.renderer.clear()
        ui_manager.draw_stat_bar_labeled(100, 100, 200, 15, 75, 100, Color.GREEN, "HP")
        ui_manager.draw_stat_bar_labeled(100, 130, 200, 15, 50, 100, Color.BLUE, "MP")
        assert True
    
    def test_draw_stat_bar_zero_max(self, ui_manager):
        """Test barra con valore massimo zero"""
        ui_manager.renderer.clear()
        ui_manager.draw_stat_bar_labeled(100, 100, 200, 15, 0, 0, Color.GREEN, "TEST")
        assert True
    
    def test_draw_stat_bar_overflow(self, ui_manager):
        """Test barra con valore superiore al massimo"""
        ui_manager.renderer.clear()
        # Il sistema dovrebbe gestire questo caso senza crash
        ui_manager.draw_stat_bar_labeled(100, 100, 200, 15, 150, 100, Color.GREEN, "HP")
        assert True
    
    def test_draw_exploration_ui(self, ui_manager, test_party):
        """Test UI esplorazione"""
        ui_manager.renderer.clear()
        ui_manager.draw_exploration_ui(test_party, "Test Dungeon", (5, 3))
        assert True
    
    def test_draw_menu(self, ui_manager):
        """Test disegno menu"""
        ui_manager.renderer.clear()
        options = ["Nuova Partita", "Carica", "Esci"]
        ui_manager.draw_menu("MENU PRINCIPALE", options, selected=1)
        assert True
    
    def test_draw_menu_empty(self, ui_manager):
        """Test menu vuoto"""
        ui_manager.renderer.clear()
        ui_manager.draw_menu("TEST", [], selected=0)
        assert True
    
    def test_draw_message_box(self, ui_manager):
        """Test message box"""
        ui_manager.renderer.clear()
        ui_manager.draw_message_box("Questo è un messaggio di test")
        assert True
    
    def test_draw_message_box_multiline(self, ui_manager):
        """Test message box multi-riga"""
        ui_manager.renderer.clear()
        message = "Riga 1\nRiga 2\nRiga 3"
        ui_manager.draw_message_box(message)
        assert True
    
    def test_draw_message_box_custom_position(self, ui_manager):
        """Test message box posizione personalizzata"""
        ui_manager.renderer.clear()
        ui_manager.draw_message_box("Test", x=100, y=100, width=400, height=80)
        assert True
    
    def test_draw_inventory_ui_empty(self, ui_manager):
        """Test inventario vuoto"""
        from models.inventory import Inventory
        ui_manager.renderer.clear()
        empty_inv = Inventory()
        ui_manager.draw_inventory_ui(empty_inv, selected_index=0)
        assert True
    
    def test_draw_inventory_ui_with_items(self, ui_manager):
        """Test inventario con oggetti"""
        from models.inventory import Inventory
        ui_manager.renderer.clear()
        inv = Inventory()
        inv.add_item('health_potion', 3)
        inv.add_item('mana_potion', 2)
        ui_manager.draw_inventory_ui(inv, selected_index=0)
        assert True
    
    def test_draw_inventory_ui_selection(self, ui_manager):
        """Test selezione in inventario"""
        from models.inventory import Inventory
        ui_manager.renderer.clear()
        inv = Inventory()
        inv.add_item('health_potion', 5)
        inv.add_item('mana_potion', 3)
        # Seleziona il secondo oggetto
        ui_manager.draw_inventory_ui(inv, selected_index=1)
        assert True
    
    def test_hero_sprite_warrior(self, ui_manager):
        """Test sprite eroe guerriero"""
        ui_manager.renderer.clear()
        char = Character(name="Kael", character_class="warrior")
        ui_manager._draw_hero_sprite(400, 400, char, is_active=False)
        assert True
    
    def test_hero_sprite_mage(self, ui_manager):
        """Test sprite eroe mago"""
        ui_manager.renderer.clear()
        char = Character(name="Elara", character_class="mage")
        ui_manager._draw_hero_sprite(400, 400, char, is_active=False)
        assert True
    
    def test_hero_sprite_active(self, ui_manager):
        """Test sprite eroe attivo (turno)"""
        ui_manager.renderer.clear()
        char = Character(name="TestHero", character_class="warrior")
        ui_manager._draw_hero_sprite(400, 400, char, is_active=True)
        assert True
    
    def test_hero_sprite_ko(self, ui_manager):
        """Test sprite eroe KO"""
        ui_manager.renderer.clear()
        char = Character(name="TestHero", character_class="warrior")
        char.hp = 0
        char.is_alive = False
        ui_manager._draw_hero_sprite(400, 400, char, is_active=False)
        assert True
    
    def test_enemy_sprite_dragon(self, ui_manager):
        """Test sprite drago"""
        ui_manager.renderer.clear()
        ui_manager._draw_enemy_sprite(300, 100, 180, "Drago Rosso")
        assert True
    
    def test_enemy_sprite_ancient_dragon(self, ui_manager):
        """Test sprite drago antico (boss)"""
        ui_manager.renderer.clear()
        ui_manager._draw_enemy_sprite(300, 100, 180, "DRAGO ANTICO")
        assert True
    
    def test_enemy_sprite_orc(self, ui_manager):
        """Test sprite orco"""
        ui_manager.renderer.clear()
        ui_manager._draw_enemy_sprite(300, 100, 180, "Orco Guerriero")
        assert True
    
    def test_enemy_sprite_troll(self, ui_manager):
        """Test sprite troll"""
        ui_manager.renderer.clear()
        ui_manager._draw_enemy_sprite(300, 100, 180, "Troll delle Caverne")
        assert True
    
    def test_enemy_sprite_goblin(self, ui_manager):
        """Test sprite goblin"""
        ui_manager.renderer.clear()
        ui_manager._draw_enemy_sprite(300, 100, 180, "Goblin Ladro")
        assert True
    
    def test_enemy_sprite_skeleton(self, ui_manager):
        """Test sprite scheletro"""
        ui_manager.renderer.clear()
        ui_manager._draw_enemy_sprite(300, 100, 180, "Scheletro Guerriero")
        assert True
    
    def test_enemy_sprite_fallback(self, ui_manager):
        """Test sprite nemico generico (fallback)"""
        ui_manager.renderer.clear()
        ui_manager._draw_enemy_sprite(300, 100, 180, "Mostro Sconosciuto")
        assert True


class TestUIManagerIntegration:
    """Test di integrazione per l'UI Manager"""
    
    def test_full_combat_screen(self, ui_manager, test_party, test_enemy):
        """Test schermata completa di combattimento"""
        ui_manager.renderer.clear()
        
        # Simula turno giocatore
        ui_manager.draw_combat_ui_split_screen(test_party, test_enemy, "Kael")
        ui_manager.renderer.update()
        
        # Simula turno nemico
        ui_manager.draw_combat_ui_split_screen(test_party, test_enemy, None)
        ui_manager.renderer.update()
        
        assert True
    
    def test_damaged_party(self, ui_manager, test_party, test_enemy):
        """Test UI con party danneggiato"""
        ui_manager.renderer.clear()
        
        # Danneggia il party
        test_party.characters[0].hp = 10
        test_party.characters[1].hp = 5
        test_party.characters[1].mp = 10
        
        ui_manager.draw_combat_ui_split_screen(test_party, test_enemy, "Kael")
        assert True
    
    def test_ko_character(self, ui_manager, test_party, test_enemy):
        """Test UI con personaggio KO"""
        ui_manager.renderer.clear()
        
        # KO primo personaggio
        test_party.characters[0].hp = 0
        test_party.characters[0].is_alive = False
        
        ui_manager.draw_combat_ui_split_screen(test_party, test_enemy, "Elara")
        assert True