"""
Unit tests per la classe Party
"""
import pytest
import sys
import os

# Aggiungi la root del progetto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.party import Party
from models.character import Character

class TestParty:
    """Test suite per Party"""

    @pytest.fixture
    def sample_party(self):
        """Fixture che crea un party di esempio"""
        party = Party()
        char1 = Character(name="Hero1", character_class="guerriero")
        char2 = Character(name="Hero2", character_class="mago")
        party.add_character(char1)
        party.add_character(char2)
        return party

    def test_party_creation_empty(self):
        """Test creazione party vuoto"""
        party = Party()
        assert len(party) == 0
        assert party.characters == []

    def test_party_creation_with_characters(self):
        """Test creazione party con personaggi"""
        char1 = Character(name="Hero1", character_class="guerriero")
        char2 = Character(name="Hero2", character_class="mago")
        party = Party(characters=[char1, char2])
        assert len(party) == 2

    def test_add_character(self, sample_party):
        """Test aggiunta personaggio"""
        char3 = Character(name="Hero3", character_class="ladro")
        sample_party.add_character(char3)
        assert len(sample_party) == 3

    def test_remove_character_success(self, sample_party):
        """Test rimozione personaggio esistente"""
        result = sample_party.remove_character("Hero1")
        assert result is True
        assert len(sample_party) == 1

    def test_remove_character_fail(self, sample_party):
        """Test rimozione personaggio non esistente"""
        result = sample_party.remove_character("NonExistent")
        assert result is False
        assert len(sample_party) == 2

    def test_get_character_by_name(self, sample_party):
        """Test recupero personaggio per nome"""
        char = sample_party.get_character("Hero1")
        assert char is not None
        assert char.name == "Hero1"

    def test_get_character_by_alias_p1(self, sample_party):
        """Test recupero personaggio con alias p1"""
        char = sample_party.get_character("p1")
        assert char is not None
        assert char.name == "Hero1"

    def test_get_character_by_alias_p2(self, sample_party):
        """Test recupero personaggio con alias p2"""
        char = sample_party.get_character("p2")
        assert char is not None
        assert char.name == "Hero2"

    def test_get_character_invalid_alias(self, sample_party):
        """Test recupero con alias non valido"""
        char = sample_party.get_character("p5")
        assert char is None

    def test_get_character_case_insensitive(self, sample_party):
        """Test recupero case-insensitive"""
        char = sample_party.get_character("HERO1")
        assert char is not None
        assert char.name == "Hero1"

    def test_get_alive_characters(self, sample_party):
        """Test recupero personaggi vivi"""
        sample_party.characters[0].is_alive = False
        alive = sample_party.get_alive_characters()
        assert len(alive) == 1
        assert alive[0].name == "Hero2"

    def test_is_party_alive_all_alive(self, sample_party):
        """Test party vivo con tutti i personaggi vivi"""
        assert sample_party.is_party_alive() is True

    def test_is_party_alive_one_alive(self, sample_party):
        """Test party vivo con un personaggio vivo"""
        sample_party.characters[0].is_alive = False
        assert sample_party.is_party_alive() is True

    def test_is_party_alive_all_dead(self, sample_party):
        """Test party morto"""
        sample_party.characters[0].is_alive = False
        sample_party.characters[1].is_alive = False
        assert sample_party.is_party_alive() is False

    def test_get_party_status(self, sample_party):
        """Test visualizzazione stato party"""
        status = sample_party.get_party_status()
        assert "Hero1" in status
        assert "Hero2" in status
        assert "[P1]" in status
        assert "[P2]" in status
