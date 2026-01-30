"""
Game Engine - Loop principale del gioco
"""

import random
from pathlib import Path
from models.party import Party
from models.character import Character
from models.world import World
from core.input_manager import InputManager
from core.movement import MovementManager, MovementResult
from combat.battle import Battle
from combat.enemy import Enemy
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
        
        # Sistema di esplorazione (Sprint 1)
        self.world = None
        self.movement_manager = None
        
        # Sistema di combattimento (Sprint 2)
        self.current_battle = None
        self.in_combat = False
        
        # Il party verrà creato durante la fase di setup
        # Non inizializziamo più il party di default qui
    
    def _initialize_default_party(self):
        """Crea un party di default con 2 personaggi (non più usato)"""
        pass
    
    def _create_character(self, player_number: int) -> Character:
        """
        Guida l'utente nella creazione di un personaggio
        
        Args:
            player_number: Numero del giocatore (1 o 2)
            
        Returns:
            Character creato
        """
        print_separator("=")
        print(f"🎭 CREAZIONE PERSONAGGIO {player_number}")
        print_separator("=")
        print()
        
        # Scelta del nome
        while True:
            name = input(f"📝 Nome del Personaggio {player_number}: ").strip()
            if name:
                break
            print_action_result("Il nome non può essere vuoto!", success=False)
        
        print()
        
        # Mostra le classi disponibili
        print("⚔️  CLASSI DISPONIBILI:")
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
            choice = input(f"🎯 Scegli la classe (1-{len(classes)}) o digita il nome: ").strip().lower()
            
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
            
            print_action_result("Scelta non valida! Riprova.", success=False)
        
        # Crea il personaggio
        character = Character(name=name, character_class=selected_class)
        
        print()
        print_action_result(f"✨ {character.name} il {Character.get_class_info(selected_class)['name']} è pronto per l'avventura!", success=True)
        print()
        
        return character
    
    def _setup_party(self):
        """Configura il party iniziale con 2 personaggi"""
        print()
        print("🌟 Benvenuto nell'RPG Game! 🌟")
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
        
        # Aggiungi oggetti iniziali all'inventario
        self.party.inventory.add_item('health_potion', 3)
        self.party.inventory.add_item('mana_potion', 2)
        
        print()
        print_separator("=")
        print("🎉 PARTY COMPLETO!")
        print_separator("=")
        print()
        print_party_status(self.party)
        print()
        print("📦 INVENTARIO INIZIALE:")
        for item_info in self.party.inventory.get_inventory_list():
            print(f"  • {item_info}")
        print()
        input("Premi INVIO per iniziare l'avventura...")
        print()
    
    def run(self):
        """Loop principale del gioco"""
        self.running = True
        print_welcome()
        
        # Fase di setup: creazione del party
        self._setup_party()
        
        # Carica il mondo (Sprint 1)
        self._load_world()
        
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
            'map': self._handle_map,
            'look': self._handle_look,
            'move': self._handle_move,
            'inventory': self._handle_inventory,
        }
        
        handler = action_handlers.get(command.action)
        if handler:
            handler(command)
        else:
            # Controlla se è un comando di movimento (w/a/s/d)
            if command.action in ['w', 'a', 's', 'd']:
                self._handle_movement_wasd(command.action)
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
    
    def _handle_inventory(self, command):
        """Mostra l'inventario"""
        print()
        print_separator("=")
        print("📦 INVENTARIO DEL PARTY")
        print_separator("=")
        
        if len(self.party.inventory) == 0:
            print("L'inventario è vuoto!")
        else:
            for item_info in self.party.inventory.get_inventory_list():
                print(f"  • {item_info}")
            
            print()
            print(f"Spazio usato: {self.party.inventory.get_unique_items()}/{self.party.inventory.max_slots} slot")
            print(f"Oggetti totali: {self.party.inventory.get_total_items()}")
        
        print_separator("=")
    
    def _load_world(self):
        """Carica il mondo di gioco (Sprint 1)"""
        print_separator("=")
        print("🗺️  CARICAMENTO MAPPA")
        print_separator("=")
        
        # Prova a caricare map_01.json
        map_path = Path("data/maps/map_01.json")
        
        if map_path.exists():
            try:
                self.world = World.load_from_file(str(map_path))
                print_action_result(f"Mappa '{self.world.name}' caricata con successo!", success=True)
            except Exception as e:
                print_action_result(f"Errore nel caricamento: {e}", success=False)
                self._create_default_world()
        else:
            print_action_result("Mappa non trovata, carico mappa di default", success=False)
            self._create_default_world()
        
        # Inizializza il movement manager
        self.movement_manager = MovementManager(self.world)
        
        print()
        print(self.world.print_map(self.movement_manager.get_position()))
        print()
        print(self.movement_manager.get_description())
        print()
        input("Premi INVIO per iniziare l'esplorazione...")
        print()
    
    def _create_default_world(self):
        """Crea un mondo di default"""
        default_grid = [
            [3, 0, 1, 0, 4],
            [0, 1, 1, 0, 0],
            [0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0],
            [0, 0, 1, 5, 0]
        ]
        self.world = World(grid=default_grid, name="Dungeon Default")
    
    def _handle_map(self, command):
        """Mostra la mappa"""
        if not self.world or not self.movement_manager:
            print_action_result("Nessuna mappa caricata!", success=False)
            return
        
        print()
        print(self.world.print_map(self.movement_manager.get_position()))
        print()
        x, y = self.movement_manager.get_position()
        print(f"📍 Posizione attuale: ({x}, {y})")
    
    def _handle_look(self, command):
        """Guarda i dintorni"""
        if not self.movement_manager:
            print_action_result("Sistema di esplorazione non inizializzato!", success=False)
            return
        
        print()
        print("👀 OSSERVI I DINTORNI...")
        print_separator()
        print(self.movement_manager.get_description())
        print()
        
        surroundings = self.movement_manager.get_surrounding_cells()
        print("Puoi andare:")
        for direction, cell_type in surroundings.items():
            if cell_type not in ["WALL", "OUT_OF_BOUNDS"]:
                symbol = "✓"
            else:
                symbol = "✗"
            print(f"  {symbol} {direction.upper()}: {cell_type}")
    
    def _handle_move(self, command):
        """Gestisce il comando di movimento esplicito"""
        if not self.movement_manager:
            print_action_result("Sistema di esplorazione non inizializzato!", success=False)
            return
        
        if not command.args:
            print_action_result("Specifica la direzione: move w/a/s/d", success=False)
            return
        
        direction = command.args[0].lower()
        self._handle_movement_wasd(direction)
    
    def _handle_movement_wasd(self, direction: str):
        """Gestisce il movimento con i tasti WASD"""
        if not self.movement_manager:
            print_action_result("Sistema di esplorazione non inizializzato!", success=False)
            return
        
        result = self.movement_manager.move(direction)
        
        print()
        print_action_result(result.message, success=result.success)
        
        if result.success:
            # Mostra la mappa aggiornata
            print()
            print(self.world.print_map(self.movement_manager.get_position()))
            
                            # Gestisci trigger
            if result.trigger == "DANGER":
                print()
                print_separator()
                self._start_combat()
            elif result.trigger == "TREASURE":
                print()
                print_separator()
                print("💎 Hai trovato 50 monete d'oro!")
                print_separator()
            elif result.trigger == "EXIT":
                print()
                print_separator()
                print("🎉 HAI COMPLETATO IL DUNGEON!")
                print_separator()
    
    def _start_combat(self):
        """Inizia un combattimento"""
        # Crea un nemico casuale
        enemy = Enemy.create_random(min_level=1, max_level=2)
        
        # Crea la battaglia
        self.current_battle = Battle(self.party, enemy)
        self.in_combat = True
        
        # Mostra intro
        print(self.current_battle.start_battle())
        
        # Loop di combattimento
        self._combat_loop()
    
    def _combat_loop(self):
        """Loop principale del combattimento"""
        while self.in_combat and self.current_battle.is_active:
            print()
            print_separator("=")
            print(f"🎲 ROUND {self.current_battle.turn_manager.round_number}")
            print_separator("=")
            
            # Ottieni il combattente corrente
            current = self.current_battle.turn_manager.get_current_combatant()
            
            if not current:
                break
            
            if current.is_player:
                # Turno del giocatore
                self._handle_player_combat_turn(current.entity)
            else:
                # Turno del nemico
                self._handle_enemy_combat_turn()
            
            # Controlla fine battaglia
            result = self.current_battle.check_battle_end()
            if result:
                self._end_combat(result)
                break
            
            # Prossimo turno
            self.current_battle.turn_manager.next_turn()
    
    def _handle_player_combat_turn(self, player: Character):
        """Gestisce il turno di un giocatore"""
        print()
        print(f"🎯 Turno di: {player.name}")
        print(f"   HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp}")
        print()
        print("Azioni disponibili:")
        print("  1. Attacco Fisico")
        print("  2. Attacco Magico (costa 10 MP)")
        print("  3. Cura te stesso")
        print("  4. Cura un alleato")
        print("  5. Usa oggetto")
        print()
        
        # Input azione
        choice = input("Scegli azione (1-5): ").strip()
        
        if choice == "1":
            action = self.current_battle.execute_player_turn(player, "attack")
        elif choice == "2":
            action = self.current_battle.execute_player_turn(player, "magic")
        elif choice == "3":
            action = self.current_battle.execute_player_turn(player, "heal", player)
        elif choice == "4":
            # Scegli alleato da curare
            alive_allies = [p for p in self.party.characters if p.is_alive and p != player]
            if alive_allies:
                print("\nAlleati:")
                for i, ally in enumerate(alive_allies, 1):
                    print(f"  {i}. {ally.name} ({ally.hp}/{ally.max_hp} HP)")
                
                ally_choice = input("Scegli alleato da curare: ").strip()
                try:
                    ally_index = int(ally_choice) - 1
                    if 0 <= ally_index < len(alive_allies):
                        target = alive_allies[ally_index]
                        action = self.current_battle.execute_player_turn(player, "heal", target)
                    else:
                        print("Scelta non valida, passi il turno")
                        return
                except ValueError:
                    print("Scelta non valida, passi il turno")
                    return
            else:
                print("Nessun alleato da curare!")
                action = self.current_battle.execute_player_turn(player, "heal", player)
        elif choice == "5":
            # Usa oggetto
            self._handle_use_item_in_combat(player)
            return
        else:
            print("Azione non valida, passi il turno")
            return
        
        # Mostra risultato
        print()
        print(action.message)
        
        # Mostra stato
        print()
        self._show_combat_status()
    
    def _handle_use_item_in_combat(self, player: Character):
        """Gestisce l'uso di oggetti in combattimento"""
        consumables = self.party.inventory.get_consumables()
        
        if not consumables:
            print("\nNessun oggetto disponibile!")
            input("Premi INVIO per continuare...")
            return
        
        print("\n📦 OGGETTI DISPONIBILI:")
        for i, item in enumerate(consumables, 1):
            print(f"  {i}. {item.get_info()}")
        print("  0. Annulla")
        
        item_choice = input("\nScegli oggetto: ").strip()
        
        if item_choice == "0":
            return
        
        try:
            item_index = int(item_choice) - 1
            if 0 <= item_index < len(consumables):
                selected_item = consumables[item_index]
                
                # Scegli target
                print("\nSu chi usare l'oggetto?")
                print("  1. Te stesso")
                print("  2. Un alleato")
                print("  3. Il nemico")
                
                target_choice = input("Scelta: ").strip()
                
                target = None
                if target_choice == "1":
                    target = player
                elif target_choice == "2":
                    alive_allies = [p for p in self.party.characters if p.is_alive and p != player]
                    if alive_allies:
                        for i, ally in enumerate(alive_allies, 1):
                            print(f"    {i}. {ally.name}")
                        ally_choice = input("  Scegli: ").strip()
                        try:
                            ally_index = int(ally_choice) - 1
                            if 0 <= ally_index < len(alive_allies):
                                target = alive_allies[ally_index]
                        except ValueError:
                            pass
                elif target_choice == "3":
                    target = None  # Per oggetti offensivi
                
                action = self.current_battle.execute_player_turn(
                    player, "use_item", target, selected_item.item_id
                )
                
                print()
                print(action.message)
                print()
                self._show_combat_status()
            else:
                print("Scelta non valida!")
        except ValueError:
            print("Scelta non valida!")
        
        input("\nPremi INVIO per continuare...")
    
    def _handle_enemy_combat_turn(self):
        """Gestisce il turno del nemico"""
        print()
        print(f"👹 Turno di: {self.current_battle.enemy.get_display_name()}")
        print()
        
        # IA esegue l'azione
        action = self.current_battle.execute_enemy_turn()
        
        print(action.message)
        
        # Mostra stato
        print()
        self._show_combat_status()
        
        input("\nPremi INVIO per continuare...")
    
    def _show_combat_status(self):
        """Mostra lo stato del combattimento"""
        print_separator("-")
        print("STATO BATTAGLIA:")
        print()
        print(f"👹 {self.current_battle.enemy}")
        print()
        print("👥 Party:")
        for char in self.party.characters:
            icon = "✓" if char.is_alive else "✗"
            print(f"   {icon} {char.name}: {char.hp}/{char.max_hp} HP | {char.mp}/{char.max_mp} MP")
        print()
        print("📦 Oggetti chiave:")
        consumables = self.party.inventory.get_consumables()
        if consumables:
            for item in consumables[:3]:  # Mostra i primi 3
                print(f"   • {item}")
        else:
            print("   • Nessun oggetto")
        print_separator("-")
    
    def _end_combat(self, result):
        """Termina il combattimento"""
        self.in_combat = False
        
        print()
        print(self.current_battle.get_battle_summary())
        
        if result.victory:
            print()
            print("🎉 VITTORIA! Il nemico è stato sconfitto!")
            print()
            print("Il party può continuare l'esplorazione.")
            input("\nPremi INVIO per continuare...")
        else:
            print()
            print("💀 SCONFITTA! Il party è stato annientato...")
            print()
            print("=== GAME OVER ===")
            self.running = False
            return
        
        # Reset battaglia
        self.current_battle = None