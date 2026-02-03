"""
Display Utilities - Funzioni per visualizzare lo stato del gioco
"""

from models.party import Party
from models.character import Character


def clear_screen():
    """Pulisce lo schermo """
    print("\n" * 2)


def print_separator(char="-", length=50):
    
    print(char * length)


def print_party_status(party: Party):
    """
    Stampa lo stato completo del party in modo formattato
    
    Args:
        party: Oggetto Party da visualizzare
    """
    print_separator("=")
    print("📊 STATO DEL PARTY")
    print_separator("=")
    
    if len(party) == 0:
        print("⚠️  Il party è vuoto!")
    else:
        print(party.get_party_status())
        print()
        alive_count = len(party.get_alive_characters())
        print(f"Personaggi vivi: {alive_count}/{len(party)}")
    
    print_separator("=")


def print_character_hp_bar(character: Character, bar_length: int = 20):
    """
    Stampa una barra HP visuale per un personaggio
    
    Args:
        character: Personaggio da visualizzare
        bar_length: Lunghezza della barra in caratteri
    """
    percentage = character.get_hp_percentage()
    filled = int((percentage / 100) * bar_length)
    empty = bar_length - filled
    
    bar = "█" * filled + "░" * empty
    
    # Colore basato su HP 
    if percentage > 66:
        status_icon = "🟢"
    elif percentage > 33:
        status_icon = "🟡"
    else:
        status_icon = "🔴"
    
    print(f"{character.name:12} {status_icon} [{bar}] {character.hp}/{character.max_hp} HP")


def print_action_result(message: str, success: bool = True):
    """
    Stampa il risultato di un'azione
    
    Args:
        message: Messaggio da visualizzare
        success: Se True, mostra come successo, altrimenti come errore
    """
    icon = "✓" if success else "✗"
    print(f"{icon} {message}")


def print_combat_message(attacker: str, target: str, damage: int):
    """
    Stampa un messaggio di combattimento formattato
    
    Args:
        attacker: Nome dell'attaccante
        target: Nome del bersaglio
        damage: Danno inflitto
    """
    print(f"⚔️  {attacker} attacca {target} per {damage} danni!")


def print_heal_message(healer: str, amount: int):
    """
    Stampa un messaggio di cura formattato
    
    Args:
        healer: Nome del personaggio che si cura
        amount: HP recuperati
    """
    print(f"💚 {healer} si cura di {amount} HP!")


def print_death_message(character_name: str):
    """
    Stampa un messaggio quando un personaggio viene sconfitto
    
    Args:
        character_name: Nome del personaggio sconfitto
    """
    print(f"💀 {character_name} è stato sconfitto!")


def print_welcome():
    """Stampa il messaggio di benvenuto"""
    print("""
    ╔════════════════════════════════════════╗
    ║     🎮 RPG GAME - SPRINT 0 & 1 🎮     ║
    ║   Sistema di combattimento testuale   ║
    ║        ed esplorazione dungeons       ║
    ╚════════════════════════════════════════╝
    """)


def print_goodbye():
    """Stampa il messaggio di uscita"""
    print()
    print_separator("=")
    print("👋 Grazie per aver giocato!")
    print("   Arrivederci!")
    print_separator("=")