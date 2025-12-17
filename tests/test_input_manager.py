"""
Unit tests per InputManager
"""
import pytest
import sys
import os

# Aggiungi la root del progetto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.input_manager import InputManager, Command

class TestInputManager:
    """Test suite per InputManager"""

    @pytest.fixture
    def manager(self):
        """Fixture che crea un InputManager"""
        return InputManager()

    def test_parse_status_command(self, manager):
        """Test parsing comando status"""
        cmd = manager.parse("status")
        assert cmd is not None
        assert cmd.action == "status"
        assert cmd.target is None
        assert cmd.args == []

    def test_parse_status_alias_s(self, manager):
        """Test alias 's' per status"""
        cmd = manager.parse("s")
        assert cmd is not None
        assert cmd.action == "status"

    def test_parse_help_command(self, manager):
        """Test comando help"""
        cmd = manager.parse("help")
        assert cmd is not None
        assert cmd.action == "help"

    def test_parse_help_aliases(self, manager):
        """Test alias per help"""
        for alias in ["h", "?", "aiuto"]:
            cmd = manager.parse(alias)
            assert cmd is not None
            assert cmd.action == "help"

    def test_parse_quit_command(self, manager):
        """Test comando quit"""
        cmd = manager.parse("quit")
        assert cmd is not None
        assert cmd.action == "quit"

    def test_parse_quit_aliases(self, manager):
        """Test alias per quit"""
        for alias in ["q", "exit", "esci"]:
            cmd = manager.parse(alias)
            assert cmd is not None
            assert cmd.action == "quit"

    def test_parse_attack_with_target(self, manager):
        """Test comando attacco con target"""
        cmd = manager.parse("p1 atk")
        assert cmd is not None
        assert cmd.action == "atk"
        assert cmd.target == "p1"
        assert cmd.args == []

    def test_parse_attack_aliases(self, manager):
        """Test alias per attacco"""
        for alias in ["attack", "attacca", "colpisci"]:
            cmd = manager.parse(f"p1 {alias}")
            assert cmd is not None
            assert cmd.action == "atk"

    def test_parse_heal_with_target(self, manager):
        """Test comando cura con target"""
        cmd = manager.parse("p2 heal")
        assert cmd is not None
        assert cmd.action == "heal"
        assert cmd.target == "p2"

    def test_parse_heal_with_amount(self, manager):
        """Test comando cura con quantità"""
        cmd = manager.parse("p1 heal 50")
        assert cmd is not None
        assert cmd.action == "heal"
        assert cmd.target == "p1"
        assert cmd.args == ["50"]

    def test_parse_empty_string(self, manager):
        """Test parsing stringa vuota"""
        cmd = manager.parse("")
        assert cmd is None

    def test_parse_whitespace_only(self, manager):
        """Test parsing solo spazi"""
        cmd = manager.parse("   ")
        assert cmd is None

    def test_parse_invalid_command(self, manager):
        """Test comando non valido"""
        cmd = manager.parse("invalidcommand")
        assert cmd is None

    def test_parse_case_insensitive(self, manager):
        """Test parsing case-insensitive"""
        cmd = manager.parse("STATUS")
        assert cmd is not None
        assert cmd.action == "status"

    def test_parse_mixed_case(self, manager):
        """Test parsing con maiuscole e minuscole"""
        cmd = manager.parse("P1 ATK")
        assert cmd is not None
        assert cmd.action == "atk"
        assert cmd.target == "p1"

    def test_normalize_action(self, manager):
        """Test normalizzazione azioni"""
        assert manager._normalize_action("atk") == "atk"
        assert manager._normalize_action("attack") == "atk"
        assert manager._normalize_action("attacca") == "atk"

    def test_is_valid_target(self, manager):
        """Test validazione target"""
        assert manager._is_valid_target("p1") is True
        assert manager._is_valid_target("p2") is True
        assert manager._is_valid_target("p9") is True
        assert manager._is_valid_target("px") is False
        assert manager._is_valid_target("player1") is False

    def test_get_help_text(self, manager):
        """Test generazione testo aiuto"""
        help_text = manager.get_help_text()
        assert "COMANDI DISPONIBILI" in help_text
        assert "status" in help_text
        assert "atk" in help_text
        assert "quit" in help_text
