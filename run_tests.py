import subprocess
import sys
from pathlib import Path


def run_all_tests():
    """Esegue tutti i test"""
    print("🧪 Esecuzione di TUTTI i test...")
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=Path(__file__).parent)
    return result.returncode


def run_unit_tests():
    """Esegue solo gli unit test"""
    print("🧪 Esecuzione UNIT tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_character.py",
        "tests/test_party.py", 
        "tests/test_input_manager.py",
        "tests/test_world.py",
        "tests/test_movement.py",
        "tests/test_enemy.py",
        "tests/test_turn_manager.py",
        "tests/test_battle.py",
        "tests/test_item.py",
        "tests/test_inventory.py"
    ], cwd=Path(__file__).parent)
    return result.returncode


def run_integration_tests():
    """Esegue i test di integrazione"""
    print("🧪 Esecuzione INTEGRATION tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_integration_csv.py",
        "tests/test_integration_exploration.py",
        "tests/test_integration_combat.py",
        "tests/test_integration_inventory.py"
    ], cwd=Path(__file__).parent)
    return result.returncode


def run_sprint0_tests():
    """Esegue i test dello Sprint 0"""
    print("🧪 Esecuzione test SPRINT 0...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_character.py",
        "tests/test_party.py",
        "tests/test_input_manager.py"
    ], cwd=Path(__file__).parent)
    return result.returncode


def run_sprint1_tests():
    """Esegue i test dello Sprint 1"""
    print("🧪 Esecuzione test SPRINT 1...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_world.py",
        "tests/test_movement.py",
        "tests/test_integration_exploration.py"
    ], cwd=Path(__file__).parent)
    return result.returncode


def run_sprint2_tests():
    """Esegue i test dello Sprint 2"""
    print("🧪 Esecuzione test SPRINT 2...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_enemy.py",
        "tests/test_turn_manager.py",
        "tests/test_battle.py",
        "tests/test_integration_combat.py"
    ], cwd=Path(__file__).parent)
    return result.returncode


def run_sprint3_tests():
    """Esegue i test dello Sprint 3"""
    print("🧪 Esecuzione test SPRINT 3...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_item.py",
        "tests/test_inventory.py",
        "tests/test_integration_inventory.py"
    ], cwd=Path(__file__).parent)
    return result.returncode

def run_sprint4_tests():
    """Esegue i test dello Sprint 4"""
    print("🧪 Esecuzione test SPRINT 4 (Pygame)...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_renderer.py",
        "tests/test_ui_manager.py",
        "tests/test_pygame_engine.py",
        "tests/test_integration_pygame.py"
    ], cwd=Path(__file__).parent)
    return result.returncode


def run_with_coverage():
    """Esegue i test con coverage report"""
    print("🧪 Esecuzione test con COVERAGE...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "--cov=models",
        "--cov=core",
        "--cov=utils",
        "--cov=combat",
        "--cov-report=html",
        "--cov-report=term"
    ], cwd=Path(__file__).parent)
    return result.returncode


def main():
    """Menu principale"""
    print("\n" + "="*50)
    print("🎮 RPG GAME - TEST RUNNER")
    print("="*50)
    print("\nScegli quale test eseguire:")
    print("1. Tutti i test")
    print("2. Solo unit tests")
    print("3. Solo integration tests")
    print("4. Test Sprint 0 (Fondamenta)")
    print("5. Test Sprint 1 (Esplorazione)")
    print("6. Test Sprint 2 (Combattimento)")
    print("7. Test Sprint 3 (Inventario & Classi)")
    print("8. Test Sprint 4 (Pygame)")
    print("9. Test con coverage report")
    print("0. Esci")
    print()
    
    choice = input("Scelta (0-9): ").strip()
    
    if choice == "1":
        return run_all_tests()
    elif choice == "2":
        return run_unit_tests()
    elif choice == "3":
        return run_integration_tests()
    elif choice == "4":
        return run_sprint0_tests()
    elif choice == "5":
        return run_sprint1_tests()
    elif choice == "6":
        return run_sprint2_tests()
    elif choice == "7":
        return run_sprint3_tests()
    elif choice == "8":
        return run_sprint4_tests()
    elif choice == "9":
        return run_with_coverage()
    elif choice == "0":
        print("Uscita...")
        return 0
    else:
        print("❌ Scelta non valida!")
        return 1


if __name__ == "__main__":
    sys.exit(main())