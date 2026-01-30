"""
Unit tests per il modello World (Sprint 1)
"""

import pytest
import json
from pathlib import Path
from models.world import World, CellType


class TestWorld:
    """Test suite per World"""
    
    @pytest.fixture
    def simple_grid(self):
        """Grid semplice 3x3"""
        return [
            [3, 0, 1],
            [0, 1, 0],
            [2, 0, 4]
        ]
    
    @pytest.fixture
    def sample_world(self, simple_grid):
        """Mondo di esempio"""
        return World(grid=simple_grid, name="Test Dungeon")
    
    def test_world_creation_empty(self):
        """Test creazione mondo vuoto"""
        world = World()
        
        assert world.name == "Dungeon"
        assert world.width == 2
        assert world.height == 2
    
    def test_world_creation_with_grid(self, sample_world):
        """Test creazione mondo con griglia"""
        assert sample_world.name == "Test Dungeon"
        assert sample_world.width == 3
        assert sample_world.height == 3
    
    def test_get_cell_valid(self, sample_world):
        """Test recupero cella valida"""
        cell = sample_world.get_cell(0, 0)
        
        assert cell == CellType.START.value
    
    def test_get_cell_invalid(self, sample_world):
        """Test recupero cella fuori dai limiti"""
        cell = sample_world.get_cell(10, 10)
        
        assert cell is None
    
    def test_is_valid_position(self, sample_world):
        """Test validazione posizione"""
        assert sample_world.is_valid_position(0, 0) is True
        assert sample_world.is_valid_position(2, 2) is True
        assert sample_world.is_valid_position(-1, 0) is False
        assert sample_world.is_valid_position(0, -1) is False
        assert sample_world.is_valid_position(3, 0) is False
        assert sample_world.is_valid_position(0, 3) is False
    
    def test_is_walkable_empty(self, sample_world):
        """Test cella vuota è percorribile"""
        assert sample_world.is_walkable(1, 0) is True
    
    def test_is_walkable_wall(self, sample_world):
        """Test muro non è percorribile"""
        assert sample_world.is_walkable(2, 0) is False
        assert sample_world.is_walkable(1, 1) is False
    
    def test_is_walkable_danger(self, sample_world):
        """Test cella pericolosa è percorribile"""
        assert sample_world.is_walkable(0, 2) is True
    
    def test_is_walkable_out_of_bounds(self, sample_world):
        """Test fuori dai limiti non è percorribile"""
        assert sample_world.is_walkable(10, 10) is False
    
    def test_get_cell_type_name(self, sample_world):
        """Test ottenimento nome tipo cella"""
        assert sample_world.get_cell_type_name(0, 0) == "START"
        assert sample_world.get_cell_type_name(2, 0) == "WALL"
        assert sample_world.get_cell_type_name(0, 2) == "DANGER"
        assert sample_world.get_cell_type_name(2, 2) == "EXIT"
        assert sample_world.get_cell_type_name(10, 10) == "OUT_OF_BOUNDS"
    
    def test_find_start_position(self, sample_world):
        """Test ricerca posizione START"""
        start = sample_world.start_position
        
        assert start is not None
        assert start == (0, 0)
    
    def test_find_start_position_not_present(self):
        """Test ricerca START quando non è presente"""
        grid = [[0, 0], [0, 0]]
        world = World(grid=grid)
        
        assert world.start_position is None
    
    def test_to_dict(self, sample_world):
        """Test conversione a dizionario"""
        data = sample_world.to_dict()
        
        assert data['name'] == "Test Dungeon"
        assert data['width'] == 3
        assert data['height'] == 3
        assert data['grid'] == sample_world.grid
    
    def test_from_dict(self, simple_grid):
        """Test creazione da dizionario"""
        data = {
            "name": "Dict World",
            "width": 3,
            "height": 3,
            "grid": simple_grid
        }
        
        world = World.from_dict(data)
        
        assert world.name == "Dict World"
        assert world.width == 3
        assert world.height == 3
    
    def test_save_and_load_file(self, sample_world, tmp_path):
        """Test salvataggio e caricamento da file"""
        file_path = tmp_path / "test_map.json"
        
        # Salva
        sample_world.save_to_file(str(file_path))
        assert file_path.exists()
        
        # Carica
        loaded_world = World.load_from_file(str(file_path))
        
        assert loaded_world.name == sample_world.name
        assert loaded_world.width == sample_world.width
        assert loaded_world.height == sample_world.height
        assert loaded_world.grid == sample_world.grid
    
    def test_load_file_not_found(self):
        """Test caricamento file inesistente"""
        with pytest.raises(FileNotFoundError):
            World.load_from_file("nonexistent.json")
    
    def test_print_map_without_player(self, sample_world):
        """Test stampa mappa senza giocatore"""
        map_str = sample_world.print_map()
        
        assert "Test Dungeon" in map_str
        assert "3x3" in map_str
        assert "S" in map_str  # START
        assert "#" in map_str  # WALL
        assert "!" in map_str  # DANGER
        assert "E" in map_str  # EXIT
    
    def test_print_map_with_player(self, sample_world):
        """Test stampa mappa con giocatore"""
        player_pos = (1, 1)
        map_str = sample_world.print_map(player_pos)
        
        assert "@" in map_str  # Simbolo giocatore
    
    def test_all_cell_types(self):
        """Test tutti i tipi di cella"""
        grid = [
            [CellType.EMPTY.value, CellType.WALL.value, CellType.DANGER.value],
            [CellType.START.value, CellType.EXIT.value, CellType.TREASURE.value],
        ]
        world = World(grid=grid, name="All Types")
        
        assert world.get_cell_type_name(0, 0) == "EMPTY"
        assert world.get_cell_type_name(1, 0) == "WALL"
        assert world.get_cell_type_name(2, 0) == "DANGER"
        assert world.get_cell_type_name(0, 1) == "START"
        assert world.get_cell_type_name(1, 1) == "EXIT"
        assert world.get_cell_type_name(2, 1) == "TREASURE"