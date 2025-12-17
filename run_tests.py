"""
Script helper per eseguire i test
"""
import subprocess
import sys
from pathlib import Path

def run_all_tests():
    """Esegue tutti i test"""
    print("Esecuzione di TUTTI i test...")
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=Path(__file__).parent)
    return result.returncode

def run_unit_tests():
    """Esegue solo gli unit test"""
    print("Esecuzione UNIT tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v", "-m", "unit",
        "tests/test_character.py",
        "tests/test_party.py",
        "tests/test_input_manager.py"
    ], cwd=Path(__file__).parent)
    return result.returncode

def run_integration_tests():
    """Esegue i test di integrazione con CSV"""
    print("Esecuzione INTEGRATION tests (CSV)...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_integration_csv.py"
    ], cwd=Path(__file__).parent)
    return result.returncode

def run_with_coverage():
    """Esegue i test con coverage report"""
    print("🧪 Esecuzione test con COVERAGE...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-v",
        "--cov=models",
        "--cov=core",
        "--cov-report=html",
        "--cov-report=term"
    ], cwd=Path(__file__).parent)
    return result.returncode

def main():
    """Menu principale"""
    print("\n" + "="*50)
    print("The Last Dream - TEST RUNNER")
    print("="*50)
    print("\nScegli quale test eseguire:")
    print("1. Tutti i test")
    print("2. Solo unit tests")
    print("3. Solo integration tests (CSV)")
    print("4. Test con coverage report")
    print("0. Esci")
    print()
    
    choice = input("Scelta (0-4): ").strip()
    
    if choice == "1":
        return run_all_tests()
    elif choice == "2":
        return run_unit_tests()
    elif choice == "3":
        return run_integration_tests()
    elif choice == "4":
        return run_with_coverage()
    elif choice == "0":
        print("Uscita...")
        return 0
    else:
        print("Scelta non valida")
        return 1

if __name__ == "__main__":
    sys.exit(main())
