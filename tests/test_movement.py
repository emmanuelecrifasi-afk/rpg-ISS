"""
Unit tests per il sistema di movimento (Sprint 1)
"""

import pytest
from models.world import World, CellType
from core.movement import MovementManager, Direction, MovementResult


class TestMovementManager:
    """Test suite per MovementManager"""
    
    @pytest.fixture
    def simple_world(self):
        """Mondo semplice 3x3"""
        grid = [
            [3, 0, 1],
            [0, 1, 0],
            [2, 0, 4]
        ]
        return World(grid=grid, name="Test World")
    
    @pytest.fixture
    def movement_manager(self, simple_world):
        """Movement manager per i test"""
        return MovementManager(simple_world)
    
    def test_initialization_with_start(self, simple_world):
        """Test inizializzazione con posizione START"""
        manager = MovementManager(simple_world)
        
        assert manager.get_position() == (0, 0)
    
    def test_initialization_custom_position(self, simple_world):
        """Test inizializzazione con posizione custom"""
        manager = MovementManager(simple_world, start_x=1, start_y=0)
        
        
        assert manager.get_position() == (0, 0)
    
    def test_initialization_no_start(self):
        """Test inizializzazione senza START"""
        grid = [[0, 1], [1, 0]]
        world = World(grid=grid)
        manager = MovementManager(world)
        
        
        assert manager.get_position() == (0, 0)
    
    def test_move_up_success(self):
        """Test movimento su con successo"""
        grid = [
            [0, 0],
            [3, 0]
        ]
        world = World(grid=grid)
        manager = MovementManager(world)
        
        result = manager.move('w')
        
        assert result.success is True
        assert manager.get_position() == (0, 0)
    
    def test_move_down_success(self, movement_manager):
        """Test movimento giù con successo"""
        result = movement_manager.move('s')
        
        assert result.success is True
        assert movement_manager.get_position() == (0, 1)
    
    def test_move_left_blocked(self, movement_manager):
        """Test movimento sinistra bloccato (fuori mappa)"""
        result = movement_manager.move('a')
        
        assert result.success is False
        assert movement_manager.get_position() == (0, 0)
    
    def test_move_right_success(self, movement_manager):
        """Test movimento destra con successo"""
        result = movement_manager.move('d')
        
        assert result.success is True
        assert movement_manager.get_position() == (1, 0)
    
    def test_move_into_wall(self, movement_manager):
        """Test movimento verso un muro"""
        movement_manager.move('d')  
        result = movement_manager.move('d')  
        
        assert result.success is False
        assert "muro" in result.message.lower()
        assert movement_manager.get_position() == (1, 0)
    
    def test_move_out_of_bounds(self, movement_manager):
        """Test movimento fuori dai limiti"""
        result = movement_manager.move('w')  
        
        assert result.success is False
        assert "confini" in result.message.lower()
    
    def test_move_invalid_command(self, movement_manager):
        """Test comando di movimento non valido"""
        result = movement_manager.move('x')
        
        assert result.success is False
        assert "non valido" in result.message.lower()
    
    def test_move_to_danger_cell(self, movement_manager):
        """Test movimento su cella DANGER"""
        
        movement_manager.move('s')
        result = movement_manager.move('s')
        
        assert result.success is True
        assert result.trigger == "DANGER"
        assert "PERICOLO" in result.message or "nemico" in result.message.lower()
    
    def test_move_to_exit_cell(self, movement_manager):
        """Test movimento su cella EXIT"""
        
        movement_manager.move('d')  
        movement_manager.move('s')  
        
        
        
        movement_manager.position_x = 1
        movement_manager.position_y = 2
        result = movement_manager.move('d')
        
        assert result.success is True
        assert result.trigger == "EXIT"
    
    def test_move_direction_enum(self, movement_manager):
        """Test movimento con enum Direction"""
        result = movement_manager.move_direction(Direction.RIGHT)
        
        assert result.success is True
        assert movement_manager.get_position() == (1, 0)
    
    def test_move_forward(self, movement_manager):
        """Test metodo move_forward"""
        success = movement_manager.move_forward(Direction.DOWN)
        
        assert success is True
        assert movement_manager.get_position() == (0, 1)
    
    def test_command_aliases(self, movement_manager):
        """Test alias dei comandi di movimento"""
        
        result = movement_manager.move('down')
        assert result.success is True
        
        
        movement_manager.position_x = 0
        movement_manager.position_y = 0
        
          
        result = movement_manager.move('right')
        assert result.success is True
    
    def test_get_surrounding_cells(self, movement_manager):
        """Test ottenimento celle circostanti"""
        surroundings = movement_manager.get_surrounding_cells()
        
        assert 'up' in surroundings
        assert 'down' in surroundings
        assert 'left' in surroundings
        assert 'right' in surroundings
        
        assert surroundings['up'] == "OUT_OF_BOUNDS"
        assert surroundings['left'] == "OUT_OF_BOUNDS"
        assert surroundings['right'] == "EMPTY"
        assert surroundings['down'] == "EMPTY"
    
    def test_get_description(self, movement_manager):
        """Test ottenimento descrizione posizione"""
        description = movement_manager.get_description()
        
        assert isinstance(description, str)
        assert len(description) > 0
        assert "partenza" in description.lower() or "start" in description.lower()
    
    def test_sequential_movements(self, movement_manager):
        """Test sequenza di movimenti"""
        
        result1 = movement_manager.move('s')
        assert result1.success is True
        
        result2 = movement_manager.move('s')
        assert result2.success is True
        assert result2.trigger == "DANGER"
        
        assert movement_manager.get_position() == (0, 2)
    
    def test_backtrack_movement(self, movement_manager):
        """Test movimento in avanti e indietro"""
        
        movement_manager.move('d')
        assert movement_manager.get_position() == (1, 0)
        
        
        result = movement_manager.move('a')
        assert result.success is True
        assert movement_manager.get_position() == (0, 0)
    
    def test_case_insensitive_commands(self, movement_manager):
        """Test comandi case-insensitive"""
        result = movement_manager.move('D')
        
        assert result.success is True
        assert movement_manager.get_position() == (1, 0)
    
    def test_whitespace_handling(self, movement_manager):
        """Test gestione spazi nei comandi"""
        result = movement_manager.move('  d  ')
        
        assert result.success is True
        assert movement_manager.get_position() == (1, 0)