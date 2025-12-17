"""
Game Engine - Loop principale del gioco
"""

import random
from models.party import Party
from models.character import Character
from core.input_manager import InputManager
from utils.display import (
    print_party_status,
    print_action_result,
    print_combat_message,
    print_heal_message,
    print_death_message,
    print_welcome,
    print_goodbye,
    print_separator
)


class GameEngine:
    """Classe principale che gestisce il loop del gioco"""
    
    def __init__(self):
        """Inizializza il game engine"""
        self.party = Party()
        self.input_manager = InputManager()
        self.running = False
        
        # Il party verrà creato durante la fase di setup
    
    def _create_character(self, player_number: int) -> Character:
        """
        Guida l'utente nella creazione di un personaggio
        
        Args:
            player_number: Numero del giocatore (1 o 2)
            
        Returns:
            Character creato
        """
        print_separator("=")
        print(f"Chi sei? dimmi Giocatore {player_number}")
        print_separator("=")
        print()
        
        # Scelta del nome
        while True:
            name = input(f"Nome del Personaggio {player_number}: ").strip()
            if name:
                break
            print_action_result("Il nome non può essere vuoto!", success=False)
        
        print()
        
        # Mostra le classi disponibili
        print("CLASSI DISPONIBILI:")
        print()
        
        classes = Character.get_available_classes()
        for i, class_name in enumerate(classes, 1):
            class_info = Character.get_class_info(class_name)
            print(f"  [{i}] {class_info['name']}")
            print(f"      HP: {class_info['hp']}")
            print(f"      {class_info['description']}")
            print()
        
        # Scelta della classe
        while True:
            choice = input(f"Scegli la classe (1-{len(classes)}) o digita il nome: ").strip().lower()
            
            # Controlla se è un numero
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(classes):
                    selected_class = classes[index]
                    break
            # Controlla se è il nome della classe
            elif choice in classes:
                selected_class = choice
                break
            
            print_action_result("Scelta non valida, Riprova.", success=False)
        
        # Crea il personaggio
        character = Character(name=name, character_class=selected_class)
        
        print()
        print_action_result(f"{character.name} il {Character.get_class_info(selected_class)['name']} è pronto per l'avventura!", success=True)
        print()
        
        return character
    
    def _setup_party(self):
        """Configura il party iniziale con 2 personaggi"""
        print()
        print("Benvenuto a DreamLand")
        print()
        print("Crea il tuo party di 2 personaggi per iniziare l'avventura.")
        print()
        
        # Crea i 2 personaggi
        char1 = self._create_character(1)
        self.party.add_character(char1)
        
        input("Premi INVIO per continuare...")
        print()
        
        char2 = self._create_character(2)
        self.party.add_character(char2)
        
        print()
        print_separator("=")
        print("PARTY COMPLETO!")
        print_separator("=")
        print()
        print_party_status(self.party)
        print()
        input("Premi INVIO per iniziare l'avventura...")
        print()
    
    def run(self):
        """Loop principale del gioco"""
        self.running = True
        print_welcome()
        
        # Fase di setup: creazione del party
        self._setup_party()
        
        print()
        
        while self.running:
            try:
                # Ottieni input dall'utente
                user_input = input("🎮 Cosa vuoi fare? > ").strip()
                
                if not user_input:
                    continue
                
                # Parsea il comando
                command = self.input_manager.parse(user_input)
                
                if command is None:
                    print_action_result(
                        "Comando non riconosciuto. Digita 'help' per l'elenco comandi.",
                        success=False
                    )
                    continue
                
                # Esegui il comando
                self._execute_command(command)
                print()
                
            except KeyboardInterrupt:
                print("\n")
                self._handle_quit()
            except Exception as e:
                print_action_result(f"Errore: {str(e)}", success=False)
        
        print_goodbye()
    
    def _execute_command(self, command):
        """
        Esegue un comando parsato
        
        Args:
            command: Oggetto Command da eseguire
        """
        action_handlers = {
            'status': self._handle_status,
            'atk': self._handle_attack,
            'heal': self._handle_heal,
            'help': self._handle_help,
            'quit': self._handle_quit,
        }
        
        handler = action_handlers.get(command.action)
        if handler:
            handler(command)
        else:
            print_action_result(f"Azione '{command.action}' non implementata.", success=False)
    
    def _handle_status(self, command):
        """Mostra lo stato del party"""
        print_party_status(self.party)
    
    def _handle_attack(self, command):
        """Gestisce un attacco"""
        if not command.target:
            print_action_result("Specifica chi deve attaccare (es. 'p1 atk')", success=False)
            return
        
        attacker = self.party.get_character(command.target)
        if not attacker:
            print_action_result(f"Personaggio '{command.target}' non trovato.", success=False)
            return
        
        if not attacker.is_alive:
            print_action_result(f"{attacker.name} è KO e non può attaccare!", success=False)
            return
        
        # Per ora, attacca un personaggio casuale diverso dall'attaccante
        possible_targets = [c for c in self.party.characters if c != attacker and c.is_alive]
        
        if not possible_targets:
            print_action_result("Non ci sono bersagli validi!", success=False)
            return
        
        target = random.choice(possible_targets)
        damage = random.randint(10, 30)
        
        actual_damage = target.take_damage(damage)
        print_combat_message(attacker.name, target.name, actual_damage)
        
        if not target.is_alive:
            print_death_message(target.name)
        
        print_separator()
        print_party_status(self.party)
    
    def _handle_heal(self, command):
        """Gestisce una cura"""
        if not command.target:
            print_action_result("Specifica chi deve curarsi (es. 'p1 heal')", success=False)
            return
        
        healer = self.party.get_character(command.target)
        if not healer:
            print_action_result(f"Personaggio '{command.target}' non trovato.", success=False)
            return
        
        if not healer.is_alive:
            print_action_result(f"{healer.name} è KO e non può curarsi!", success=False)
            return
        
        # Quantità di cura (default 20, oppure specificata dall'utente)
        heal_amount = 20
        if command.args and command.args[0].isdigit():
            heal_amount = int(command.args[0])
        
        actual_heal = healer.heal(heal_amount)
        
        if actual_heal > 0:
            print_heal_message(healer.name, actual_heal)
        else:
            print_action_result(f"{healer.name} ha già HP al massimo!", success=False)
        
        print_separator()
        print_party_status(self.party)
    
    def _handle_help(self, command):
        """Mostra l'aiuto"""
        print(self.input_manager.get_help_text())
    
    def _handle_quit(self, command=None):
        """Termina il gioco"""
        self.running = False