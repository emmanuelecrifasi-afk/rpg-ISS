"""
Test per il sistema di rendering Pygame
Sprint 4: The Big Switch
"""

import pytest
import pygame
from rendering.renderer import Renderer, Color
from models.world import World, CellType
from models.party import Party
from models.character import Character


@pytest.fixture
def renderer():
    """Fixture per il renderer"""
    pygame.init()
    r = Renderer(width=800, height=600, title="Test")
    yield r
    r.quit()


@pytest.fixture
def simple_world():
    """Crea un mondo semplice per i test"""
    grid = [
        [3, 0, 0, 4],
        [0, 1, 2, 0],
        [0, 0, 0, 0]
    ]
    return World(grid=grid, name="Test World")


@pytest.fixture
def test_party():
    """Crea un party di test"""
    party = Party()
    char1 = Character(name="TestHero1", character_class="warrior")
    char2 = Character(name="TestHero2", character_class="mage")
    party.add_character(char1)
    party.add_character(char2)
    return party


class TestRenderer:
    """Test per la classe Renderer"""
    
    def test_renderer_initialization(self, renderer):
        """Test inizializzazione renderer"""
        assert renderer.width == 800
        assert renderer.height == 600
        assert renderer.screen is not None
        assert renderer.fps == 60
    
    def test_clear_screen(self, renderer):
        """Test pulizia schermo"""
        renderer.clear(Color.BLACK)
        
        assert True
    
    def test_draw_text(self, renderer):
        """Test disegno testo"""
        renderer.clear()
        renderer.draw_text("Test", 100, 100, Color.WHITE, "medium", centered=False)
        renderer.draw_text("Centered", 400, 300, Color.YELLOW, "large", centered=True)
        
        assert True
    
    def test_draw_rect(self, renderer):
        """Test disegno rettangolo"""
        renderer.clear()
        renderer.draw_rect(10, 10, 100, 50, Color.RED, filled=True)
        renderer.draw_rect(150, 10, 100, 50, Color.BLUE, filled=False)
        assert True
    
    def test_draw_world_view(self, renderer, simple_world, test_party):
        """Test rendering vista mondo"""
        renderer.clear()
        player_pos = (0, 0)
        
        
        renderer.draw_world_view(simple_world, player_pos, test_party, offset_x=50, offset_y=50)
        
        assert True
    
    def test_draw_hp_bar(self, renderer):
        """Test barra HP"""
        renderer.clear()
        
        renderer.draw_hp_bar(100, 100, 200, 30, 100, 100)
        
        renderer.draw_hp_bar(100, 150, 200, 30, 50, 100)
        
        renderer.draw_hp_bar(100, 200, 200, 30, 20, 100)
        
        renderer.draw_hp_bar(100, 250, 200, 30, 0, 100)
        assert True
    
    def test_draw_mp_bar(self, renderer):
        """Test barra MP"""
        renderer.clear()
        renderer.draw_mp_bar(100, 100, 200, 30, 75, 100)
        renderer.draw_mp_bar(100, 150, 200, 30, 0, 100)
        assert True
    
    def test_cell_size(self, renderer):
        """Test dimensione celle"""
        assert renderer.cell_size == 64
    
    def test_fonts_loaded(self, renderer):
        """Test caricamento font"""
        assert renderer.font_small is not None
        assert renderer.font_medium is not None
        assert renderer.font_large is not None


class TestColor:
    """Test per la classe Color"""
    
    def test_color_values(self):
        """Test valori colori predefiniti"""
        assert Color.BLACK == (0, 0, 0)
        assert Color.WHITE == (255, 255, 255)
        assert Color.RED == (220, 20, 60)
        assert Color.GREEN == (34, 139, 34)
        assert Color.BLUE == (30, 144, 255)
        assert Color.YELLOW == (255, 215, 0)
    
    def test_color_types(self):
        """Test tipi dei colori (tuple di 3 int)"""
        for color_name in dir(Color):
            if not color_name.startswith('_'):
                color = getattr(Color, color_name)
                assert isinstance(color, tuple)
                assert len(color) == 3
                for value in color:
                    assert isinstance(value, int)
                    assert 0 <= value <= 255