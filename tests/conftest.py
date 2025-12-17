"""
Configurazione pytest condivisa per tutti i test
"""
import pytest
import sys
from pathlib import Path

# Aggiungi la root del progetto al path (va su di 2 livelli: tests -> rpg-ISS)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def project_root_dir():
    """Fixture che restituisce la directory root del progetto"""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def test_results_dir(project_root_dir):
    """Crea e restituisce la directory per i risultati dei test"""
    results_dir = project_root_dir / "tests" / "test_results"
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir

def pytest_configure(config):
    """Hook eseguito prima dell'inizio dei test"""
    print("\n" + "="*50)
    print("AVVIO TEST SUITE - RPG GAME SPRINT 0")
    print("="*50)

def pytest_sessionfinish(session, exitstatus):
    """Hook eseguito alla fine di tutti i test"""
    print("\n" + "="*50)
    print("✓ TEST SUITE COMPLETATA")
    print(f"Exit status: {exitstatus}")
    print("="*50)
