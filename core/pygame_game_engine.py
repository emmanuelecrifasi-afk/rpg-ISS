"""
Pygame Game Engine - Loop principale con grafica
"""

import pygame
import sys
from pathlib import Path
from models.party import Party
from models.character import Character
from models.world import World
from core.movement import MovementManager
from combat.battle import Battle
from combat.enemy import Enemy
from rendering.renderer import Renderer, Color
from rendering.ui_manager import UIManager
from utils.display import print_separator


class GameState:
    """Stati del gioco"""
    MENU = "menu"
    CHAR_CREATION = "char_creation"
    STORY_INTRO = "story_intro"
    LEVEL_SELECTION = "level_selection"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    INVENTORY = "inventory"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class PygameGameEngine:
    """Game Engine principale con Pygame"""
    
    def __init__(self):
        """Inizializza il game engine"""
        
        pygame.init()
        self.renderer = Renderer(width=1024, height=768, title="The Last Dream")
        self.ui_manager = UIManager(self.renderer)

        
        self.party = Party()
        self.world = None
        self.movement_manager = None
        self.current_battle = None
        
        
        self.current_level_index = 0
        
        self.level_files = [
            "map_01.json",      
            "map_maze.json",    
            "map_arena.json",   
            "map_large.json"    
        ]
        
        # --- STATO DEL GIOCO ---
        self.state = GameState.MENU
        self.running = False
        
        
        self.menu_options = ["Nuova Partita", "Esci"]
        self.menu_selected = 0
        self.previous_state = None  
        
        # Inventory UI
        self.inventory_selected = 0
        
        # Messaggi temporanei
        self.message = ""
        self.message_timer = 0
        
        # Creazione personaggi
        self.creation_phase = 0
        self.temp_name = ""
        self.temp_class_index = 0
        self.available_classes = Character.get_available_classes()
        
        # Input handling
        self.key_cooldown = 0
        self.COOLDOWN_TIME = 200

        self.current_level_index = 0
        self.max_unlocked_index = 0  # 0 = Solo il primo livello sbloccato
        
        # Nomi descrittivi per il menu
        self.level_files = ["map_01.json", "map_maze.json", "map_arena.json", "map_large.json"]
        self.level_names = [
            "1. Il Bosco Atro ", 
            "2. Il Labirinto Oscuro", 
            "3. L'Arena dei Campioni", 
            "4. La Tana del Drago"
        ]
        
        # Selezione nel menu livelli
        self.level_selection_index = 0

        self.intro_lines = []        # Conterrà le frasi della storia
        self.current_intro_line = 0  # A che frase siamo
        self.text_buffer = ""        # Testo attualmente visibile (effetto macchina da scrivere)
        self.last_char_time = 0      # Timer per la velocità del testo
        self.text_complete = False   # Se la frase corrente è finita

        self.dialogue_next_state = GameState.LEVEL_SELECTION

    def _handle_menu_input(self, key):
        """Input del menu principale (Corretto per gestire Riprendi)"""
        # Navigazione SU
        if key == pygame.K_UP or key == pygame.K_w:
            self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
            self.key_cooldown = pygame.time.get_ticks()
        
        # Navigazione GIÙ
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
            self.key_cooldown = pygame.time.get_ticks()
        
        # Selezione (INVIO)
        elif key == pygame.K_RETURN:
            
            selected_text = self.menu_options[self.menu_selected]
            
            if selected_text == "Riprendi":
                
                if self.previous_state:
                    self.state = self.previous_state
            
            elif selected_text == "Nuova Partita":
                # Logica di reset per nuova partita
                self.state = GameState.CHAR_CREATION
                self.creation_phase = 0
                self.temp_name = ""
                self.temp_class_index = 0
                self.party = Party() 
                self.menu_options = ["Nuova Partita", "Esci"] # Resetta il menu
                
            elif selected_text == "Esci":
                self.running = False
                
            self.key_cooldown = pygame.time.get_ticks()
    
    def run(self):
        """Loop principale del gioco"""
        self.running = True
        clock = pygame.time.Clock()
        
        while self.running:
            dt = clock.tick(60)  # 60 FPS
            
            # Gestisci eventi
            self._handle_events()
            
            # Aggiorna logica
            self._update(dt)
            
            # Renderizza
            self._render()
            
            # Aggiorna display
            self.renderer.update()
        
        # Cleanup
        self.renderer.quit()
        pygame.quit()
        sys.exit()
    
    def _handle_events(self):
        """Gestisce gli eventi Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
    
    def _handle_keydown(self, key):
        """Gestisce la pressione dei tasti"""
        # Controlla cooldown
        current_time = pygame.time.get_ticks()
        if current_time - self.key_cooldown < self.COOLDOWN_TIME:
            return
        
        if self.state == GameState.MENU:
            self._handle_menu_input(key)
        
        elif self.state == GameState.CHAR_CREATION:
            self._handle_char_creation_input(key)

        elif self.state == GameState.STORY_INTRO:
            self._handle_story_intro_input(key)

        elif self.state == GameState.LEVEL_SELECTION:
            self._handle_level_selection_input(key)
            

        elif self.state == GameState.EXPLORATION:
            self._handle_exploration_input(key)
        
        elif self.state == GameState.COMBAT:
            self._handle_combat_input(key)
        
        elif self.state == GameState.INVENTORY:
            self._handle_inventory_input(key)
        
        elif self.state == GameState.GAME_OVER or self.state == GameState.VICTORY:
            if key == pygame.K_RETURN:
                self.state = GameState.MENU
                self.key_cooldown = current_time
    
    def _handle_menu_input(self, key):
        """Input del menu principale"""
        
        # --- MOVIMENTO SU ---
        if key == pygame.K_UP or key == pygame.K_w:
            self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
            self.key_cooldown = pygame.time.get_ticks()
        
        # --- MOVIMENTO GIÙ ---
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
            self.key_cooldown = pygame.time.get_ticks()
        
        # --- SELEZIONE (INVIO) ---
        elif key == pygame.K_RETURN:
            
            selected_text = self.menu_options[self.menu_selected]
            
            
            
            
            # 2. CONTROLLA IL TESTO ESATTO
            if selected_text == "Riprendi":
                if self.previous_state:
                    self.state = self.previous_state
                    
            
            elif selected_text == "Nuova Partita":
                
                self.state = GameState.CHAR_CREATION
                self.creation_phase = 0
                self.temp_name = ""
                self.temp_class_index = 0
                self.party = Party() # Resetta il party
                # Reset menu standard 
                self.menu_options = ["Nuova Partita", "Esci"] 
                
            elif selected_text == "Esci":
                self.running = False
                
            self.key_cooldown = pygame.time.get_ticks()
    
    def _handle_char_creation_input(self, key):
        """Input per creazione personaggi"""
        current_time = pygame.time.get_ticks()
        
        # Navigazione classi 
        if key == pygame.K_LEFT:  
            self.temp_class_index = (self.temp_class_index - 1) % len(self.available_classes)
            self.key_cooldown = current_time
        
        elif key == pygame.K_RIGHT:  
            self.temp_class_index = (self.temp_class_index + 1) % len(self.available_classes)
            self.key_cooldown = current_time
        
        # Input nome
        elif key == pygame.K_BACKSPACE:
            self.temp_name = self.temp_name[:-1]
            self.key_cooldown = current_time - 150
        
        elif key == pygame.K_RETURN and len(self.temp_name) > 0:
            # Crea personaggio
            selected_class = self.available_classes[self.temp_class_index]
            char = Character(name=self.temp_name, character_class=selected_class)
            self.party.add_character(char)
            
            if self.creation_phase == 0:
                self.creation_phase = 1
                self.temp_name = ""
                self.temp_class_index = 0
            else:
                # SETUP COMPLETATO -> VAI AL MENU LIVELLI
                self._setup_game()           # Inizializza variabili di gioco
                self._setup_story_intro()    # Prepara il testo della storia
                self.state = GameState.STORY_INTRO  
            
            self.key_cooldown = current_time
        
        
        elif key in range(pygame.K_a, pygame.K_z + 1) or key == pygame.K_SPACE:
            if len(self.temp_name) < 12:
                char = pygame.key.name(key)
                if key == pygame.K_SPACE:
                    char = " "
                elif len(self.temp_name) == 0:
                    char = char.upper() 
                self.temp_name += char
                self.key_cooldown = current_time - 100
    
    def _render_story_intro(self):
        """Renderizza la storia con il nuovo sfondo scenico"""
        width = self.renderer.width
        height = self.renderer.height
        current_time = pygame.time.get_ticks()
        
        
        self.ui_manager.draw_story_background()
        
        # 2. BOX DI TESTO 
        box_height = 200
        box_y = height - box_height - 20
        
        
        pygame.draw.rect(self.renderer.screen, (15, 15, 25), (40, box_y, width - 80, box_height), 0, 5)
        
        # Bordo decorativo doppio
        pygame.draw.rect(self.renderer.screen, (100, 100, 150), (40, box_y, width - 80, box_height), 3, 5)
        pygame.draw.rect(self.renderer.screen, (255, 255, 255), (45, box_y + 5, width - 90, box_height - 10), 1, 5)
        
        # 3. LOGICA MACCHINA DA SCRIVERE 
        target_text = self.intro_lines[self.current_intro_line]
        
        if not self.text_complete:
            if current_time - self.last_char_time > 30:
                if len(self.text_buffer) < len(target_text):
                    self.text_buffer += target_text[len(self.text_buffer)]
                    self.last_char_time = current_time
                else:
                    self.text_complete = True
        
        # 4. DISEGNA IL TESTO
        
        self.renderer.draw_text(self.text_buffer, 70, box_y + 40, Color.WHITE, "medium", centered=False)
        
        # 5. INDICATORE "PREMI INVIO" 
        if self.text_complete:
            if (current_time // 500) % 2 == 0:
                #
                pygame.draw.polygon(self.renderer.screen, Color.YELLOW, [
                    (width - 80, height - 60), 
                    (width - 60, height - 60), 
                    (width - 70, height - 50)
                ])
                self.renderer.draw_text("PREMI INVIO", width - 110, height - 85, Color.YELLOW, "small", centered=True)

    def _handle_story_intro_input(self, key):
        """Gestisce l'avanzamento della storia"""
        current_time = pygame.time.get_ticks()
        
        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            # A) Se il testo non ha finito di scriversi, completalo subito
            if not self.text_complete:
                self.text_buffer = self.intro_lines[self.current_intro_line]
                self.text_complete = True
                
            # B) Se il testo è finito, passa alla prossima frase
            else:
                self.current_intro_line += 1
                
                # Se ci sono ancora frasi
                if self.current_intro_line < len(self.intro_lines):
                    self.text_buffer = ""
                    self.text_complete = False
                    self.last_char_time = current_time
                else:
                    
                    self.state = self.dialogue_next_state
            
            self.key_cooldown = current_time

    def _setup_story_intro(self):
        """Prepara il testo della storia usando i nomi dei personaggi"""
        # Recupera i nomi (se esistono, altrimenti usa default)
        name1 = self.party.characters[0].name if len(self.party.characters) > 0 else "Elara"
        name2 = self.party.characters[1].name if len(self.party.characters) > 1 else "Kael"
        
        self.intro_lines = [
            f"Tutto ebbe inizio nella Caverna del Sussurro Perduto...",
            f"{name1} e {name2}, spinti dalla curiosità, si spinsero nelle profondità.",
            "Le leggende parlavano di un segreto dimenticato da ere...",
            "Trovarono un antico portale. Una luce pulsava nell'ombra.",
            f"Ignorando i pericoli, attivarono la stele proibita!",
            "Un lampo accecante... Il mondo conosciuto svanì nel nulla.",
            "...",
            "Vi siete risvegliati in Aethelgard, il Mondo Specchio.",
            "Un luogo sull'orlo del collasso, consumato dall'Oscurità.",
            "Per tornare a casa, dovete trovare la leggendaria Chiave dell'Eco.",
            "Il vostro destino è stato scritto. Il viaggio ha inizio."
        ]
        
        self.current_intro_line = 0
        self.text_buffer = ""
        self.text_complete = False
        self.last_char_time = pygame.time.get_ticks()


    def _handle_exploration_input(self, key):
        """Input durante esplorazione"""
        current_time = pygame.time.get_ticks()
        
        # Movimento P1 (WASD)
        if key == pygame.K_w:
            self._try_move('w')
            self.key_cooldown = current_time
        elif key == pygame.K_a:
            self._try_move('a')
            self.key_cooldown = current_time
        elif key == pygame.K_s:
            self._try_move('s')
            self.key_cooldown = current_time
        elif key == pygame.K_d:
            self._try_move('d')
            self.key_cooldown = current_time
        
        # Movimento P2 (Frecce) - stesso movimento condiviso
        elif key == pygame.K_UP:
            self._try_move('w')
            self.key_cooldown = current_time
        elif key == pygame.K_LEFT:
            self._try_move('a')
            self.key_cooldown = current_time
        elif key == pygame.K_DOWN:
            self._try_move('s')
            self.key_cooldown = current_time
        elif key == pygame.K_RIGHT:
            self._try_move('d')
            self.key_cooldown = current_time
        
        
        elif key == pygame.K_i:
            self.state = GameState.INVENTORY
            self.inventory_selected = 0
            self.key_cooldown = current_time
        
        elif key == pygame.K_ESCAPE:
            self.previous_state = self.state  
            self.state = GameState.MENU
            self.menu_options = ["Riprendi", "Nuova Partita", "Esci"]
            self.menu_selected = 0
            self.key_cooldown = current_time
    
    def _handle_combat_input(self, key):
        """Input durante combattimento"""
        current_time = pygame.time.get_ticks()
        
        # Ottieni combattente corrente
        current = self.current_battle.turn_manager.get_current_combatant()
        
        if not current or not current.is_player:
            return
        
        player = current.entity
        
        # Azioni di combattimento
        if key == pygame.K_1:  # Attacco fisico
            action = self.current_battle.execute_player_turn(player, "attack")
            self._show_message(action.message)
            self._next_combat_turn()
            self.key_cooldown = current_time
        
        elif key == pygame.K_2:  # Attacco magico
            action = self.current_battle.execute_player_turn(player, "magic")
            self._show_message(action.message)
            self._next_combat_turn()
            self.key_cooldown = current_time
        
        elif key == pygame.K_3:  # Cura se stesso
            action = self.current_battle.execute_player_turn(player, "heal", player)
            self._show_message(action.message)
            self._next_combat_turn()
            self.key_cooldown = current_time
        
        elif key == pygame.K_4:  # Cura alleato
            alive_allies = [p for p in self.party.characters if p.is_alive and p != player]
            if alive_allies:
                target = alive_allies[0]
                action = self.current_battle.execute_player_turn(player, "heal", target)
                self._show_message(action.message)
                self._next_combat_turn()
            self.key_cooldown = current_time
    
    def _handle_inventory_input(self, key):
        """Input nell'inventario (FIX: Recupera ID corretti dal dizionario)"""
        current_time = pygame.time.get_ticks()
        
        
        items_data = list(self.party.inventory.items.items())
        
        # Navigazione SU
        if key == pygame.K_UP or key == pygame.K_w:
            if items_data:
                self.inventory_selected = (self.inventory_selected - 1) % len(items_data)
            self.key_cooldown = current_time
        
        # Navigazione GIÙ
        elif key == pygame.K_DOWN or key == pygame.K_s:
            if items_data:
                self.inventory_selected = (self.inventory_selected + 1) % len(items_data)
            self.key_cooldown = current_time
        
        # CHIUDI
        elif key == pygame.K_ESCAPE or key == pygame.K_i:
            self.state = GameState.EXPLORATION
            self.key_cooldown = current_time
            
        # USA OGGETTO (INVIO)
        elif key == pygame.K_RETURN:
            if items_data:
                # 1. Recupera ID e Oggetto dalla tupla
                selected_id, selected_item = items_data[self.inventory_selected]
                
                # 2. Logica effetto basata sul nome 
                used = False
                name_lower = selected_item.name.lower()
                
                if "vita" in name_lower or "health" in name_lower:
                    # Cura tutto il party di 50 HP
                    for char in self.party.characters:
                        if char.is_alive:
                            char.heal(50)
                    self._show_message(f"❤️ Party curato con {selected_item.name}!")
                    used = True
                    
                elif "mana" in name_lower:
                    # Ripristina 30 MP a tutto il party
                    for char in self.party.characters:
                        if char.is_alive:
                            char.restore_mp(30)
                    self._show_message(f"✨ Mana ripristinato con {selected_item.name}!")
                    used = True
                
                else:
                    self._show_message("Non puoi usare questo oggetto qui.")
                
                # 3. Se usato, rimuovi usando l'ID corretto
                if used:
                    self.party.inventory.remove_item(selected_id, 1) 
                    
                    
                    items_after = list(self.party.inventory.items.items())
                    if self.inventory_selected >= len(items_after) and len(items_after) > 0:
                        self.inventory_selected = len(items_after) - 1
            
            self.key_cooldown = current_time
    
    def _try_move(self, direction):
        """Prova a muoversi in una direzione"""
        if not self.movement_manager:
            return
        
        result = self.movement_manager.move(direction)
        
        # --- 1. NEMICO ---
        if result.trigger == "DANGER":
            self._start_combat()
            
        # --- 2. TESORO ---
        elif result.trigger == "TREASURE":
            self.party.inventory.add_item('health_potion', 1)
            self._show_message("💎 Hai trovato una Pozione di Vita!")
            px, py = self.movement_manager.get_position()
            if self.world:
                self.world.grid[py][px] = 0
            
        # --- 3. USCITA (EXIT) ---
        elif result.trigger == "EXIT":
            # A) Controllo Nemici
            if not self._are_all_enemies_defeated():
                self._show_message("⛔ Devi sconfiggere tutti i nemici prima!")
                return 

            # B) Controllo Boss (Solo Ultimo Livello)
            is_last_level = (self.current_level_index == len(self.level_files) - 1)
            if is_last_level and not self.final_boss_defeated:
                self._start_boss_fight()
                return
            
            # C) FINE LIVELLO -> TORNA AL MENU
            self._show_message("Livello Completato!")
            
            if not is_last_level:
                # 1. Calcola quale sarebbe il prossimo livello
                next_level_idx = self.current_level_index + 1
                
                # 2. Sblocca il livello
                if next_level_idx > self.max_unlocked_index:
                    self.max_unlocked_index = next_level_idx
                    self._show_message(f"🔓 {self.level_names[next_level_idx]} Sbloccato!")
                
                
                self.state = GameState.LEVEL_SELECTION
                self.level_selection_index = next_level_idx 
                
            else:
                # Era l'ultimo livello: Vittoria Finale
                self.state = GameState.VICTORY
    
    def _start_combat(self):
        """Inizia un combattimento"""
        enemy = Enemy.create_random(min_level=1, max_level=2)
        self.current_battle = Battle(self.party, enemy)
        self.current_battle.start_battle()
        self.state = GameState.COMBAT
        self._show_message(f"⚔️ Combattimento contro {enemy.get_display_name()}!")
    
    # Controlla fine battaglia
        result = self.current_battle.check_battle_end()
        if result:
            if result.victory:
                self._show_message("🎉 VITTORIA! La via è libera.")
                
               
                px, py = self.movement_manager.get_position()
                self.world.grid[py][px] = 0  # 0 = Cella Vuota
                
                
                self.state = GameState.EXPLORATION
                self.current_battle = None
            else:
                self.state = GameState.GAME_OVER
            return
        
        # Prossimo turno
        self.current_battle.turn_manager.next_turn()
        
        # Se è il turno del nemico, eseguilo automaticamente
        current = self.current_battle.turn_manager.get_current_combatant()
        if current and not current.is_player:
            action = self.current_battle.execute_enemy_turn()
            self._show_message(action.message)
            
            # Controlla di nuovo fine battaglia
            result = self.current_battle.check_battle_end()
            if result:
                if result.victory:
                    self._show_message("🎉 VITTORIA!")
                    self.state = GameState.EXPLORATION
                    self.current_battle = None
                else:
                    self.state = GameState.GAME_OVER
                return
            
            # Passa al prossimo giocatore
            self.current_battle.turn_manager.next_turn()

    def _start_boss_fight(self):
        """Prepara la Boss Fight con dialogo introduttivo"""
        # 1. Crea il Boss
        boss = Enemy.create_random(min_level=5, max_level=5)
        boss.name = "DRAGO ANTICO"
        boss.max_hp = 300
        boss.hp = 300
        boss.damage = 25
        boss.xp_reward = 5000
        
        self.current_battle = Battle(self.party, boss)
        
        # 2. Dialogo 
        self.intro_lines = [
            "...",
            "La terra trema sotto i vostri piedi!",
            "Un'ombra gigantesca copre l'uscita.",
            "Il DRAGO ANTICO vi osserva con occhi di fuoco.",
            "DRAGO: 'Piccoli insetti... credete di poter fuggire?'",
            "DRAGO: 'La Chiave dell'Eco rimarrà mia per sempre!'",
            "Preparatevi alla battaglia finale!"
        ]
        
        # 3. Setup Dialogo
        self.current_intro_line = 0
        self.text_buffer = ""
        self.text_complete = False
        self.last_char_time = pygame.time.get_ticks()
        
        # 4. Dopo il dialogo -> COMBATTIMENTO
        self.dialogue_next_state = GameState.COMBAT
        self.state = GameState.STORY_INTRO

    def _next_combat_turn(self):
        """Passa al turno successivo (Gestisce Vittoria, Rimozione Nemici e Dialoghi)"""
        
        # 1. CONTROLLO FINE BATTAGLIA
        result = self.current_battle.check_battle_end()
        
        if result:
            if result.victory:
                enemy_name = self.current_battle.enemy.name
                self._show_message(f"🎉 VITTORIA! {enemy_name} sconfitto. LEVEL UP: +HP/MP!")
                
                # CASO A: È IL DRAGO ANTICO (BOSS FINALE) 
                if enemy_name == "DRAGO ANTICO":
                    self.final_boss_defeated = True
                    
                    # 1. Dialogo Epico Finale
                    self.intro_lines = [
                        "Il Drago Antico lancia un ultimo ruggito straziante...",
                        "Il suo corpo colossale crolla in polvere.",
                        "Tra le ceneri, qualcosa brilla di luce pura.",
                        "È la CHIAVE DELL'ECO!",
                        "L'avete trovata. Il portale per casa si sta aprendo.",
                        "Il vostro viaggio in questo mondo è finito.",
                        "Siete liberi.",
                        "GRAZIE PER AVER GIOCATO!"
                    ]
                    # 2. Setup Dialogo
                    self.current_intro_line = 0
                    self.text_buffer = ""
                    self.text_complete = False
                    self.last_char_time = pygame.time.get_ticks()
                    
                    # 3. Dopo il dialogo -> VITTORIA
                    self.dialogue_next_state = GameState.VICTORY
                    self.state = GameState.STORY_INTRO
                    return

                # --- CASO B: È UN NEMICO NORMALE ---
                else:
                    
                    px, py = self.movement_manager.get_position()
                    if self.world:
                        self.world.grid[py][px] = 0  
                    
                    
                    self.state = GameState.EXPLORATION
                    self.current_battle = None
                    return
            else:
                # Sconfitta
                self.state = GameState.GAME_OVER
            return
        
        # 2. SE LA BATTAGLIA CONTINUA
        self.current_battle.turn_manager.next_turn()
        
        # 3. TURNO NEMICO (IA)
        current = self.current_battle.turn_manager.get_current_combatant()
        if current and not current.is_player:
            action = self.current_battle.execute_enemy_turn()
            self._show_message(action.message)
            
            # Ricontrolla fine battaglia dopo colpo nemico
            result = self.current_battle.check_battle_end()
            if result:
                if result.victory:
                    
                    self._show_message("🎉 VITTORIA!")
                    if self.current_battle.enemy.name != "DRAGO ANTICO":
                        px, py = self.movement_manager.get_position()
                        if self.world:
                            self.world.grid[py][px] = 0
                    
                    self.state = GameState.EXPLORATION
                    self.current_battle = None
                else:
                    self.state = GameState.GAME_OVER
                return
            
            self.current_battle.turn_manager.next_turn()

    def _are_all_enemies_defeated(self):
        """Controlla se ci sono ancora nemici (valore 2) nella griglia"""
        if not self.world:
            return True
            
        for row in self.world.grid:
            if 2 in row:  
                return False
        return True
    
    def _show_message(self, message: str, duration: int = 3000):
        """Mostra un messaggio temporaneo"""
        self.message = message
        self.message_timer = pygame.time.get_ticks() + duration

    def _load_current_level(self):
        """Carica il livello corrente dalla lista"""
        if self.current_level_index < len(self.level_files):
            filename = self.level_files[self.current_level_index]
            map_path = Path(f"data/maps/{filename}")
            
            if map_path.exists():
                self.world = World.load_from_file(str(map_path))
                # Mostra un messaggio all'inizio del livello
                self._show_message(f"CAPITOLO {self.current_level_index + 1}: {self.world.name}")
            else:
                print(f"⚠️ Errore: Mappa {filename} non trovata!")
                
                self.world = World(grid=[[3,4]], name="Livello Buggato")
            
            # Collega il movimento al nuovo mondo caricato
            self.movement_manager = MovementManager(self.world)

    def _setup_game(self):
        """Setup iniziale del gioco"""
        
        self.party.inventory.items.clear()
        self.party.inventory.add_item('health_potion', 3)
        self.party.inventory.add_item('mana_potion', 2)
        
        # Reset livelli
        self.current_level_index = 0
        
        
        self.final_boss_defeated = False
        
        
        self._load_current_level()
    
    def _update(self, dt):
        """Aggiorna la logica del gioco"""
        
        if self.message_timer > 0 and pygame.time.get_ticks() > self.message_timer:
            self.message = ""
            self.message_timer = 0
    
    def _render(self):
        """Renderizza la scena corrente"""
        self.renderer.clear(Color.BLACK)
        
        if self.state == GameState.MENU:
            self._render_menu()
        
        elif self.state == GameState.CHAR_CREATION:
            self._render_char_creation()

        elif self.state == GameState.STORY_INTRO:
            self._render_story_intro()

        elif self.state == GameState.LEVEL_SELECTION:
            self._render_level_selection()

        elif self.state == GameState.EXPLORATION:
            self._render_exploration()
        
        elif self.state == GameState.COMBAT:
            self._render_combat()
        
        elif self.state == GameState.INVENTORY:
            self._render_inventory()
        
        elif self.state == GameState.GAME_OVER:
            self._render_game_over()
        
        elif self.state == GameState.VICTORY:
            self._render_victory()
        
        # Mostra messaggio temporaneo
        if self.message:
            self.ui_manager.draw_message_box(self.message)
    
    def _render_menu(self):
        """Renderizza il menu principale"""
        width = self.renderer.width
        height = self.renderer.height
        
        # --- 1. SFONDO ---
        
        self.renderer.clear((15, 10, 25))
        
        # Disegna una griglia sottile 
        grid_color = (25, 20, 35)
        for x in range(0, width, 50):
            pygame.draw.line(self.renderer.screen, grid_color, (x, 0), (x, height), 1)
        for y in range(0, height, 50):
            pygame.draw.line(self.renderer.screen, grid_color, (0, y), (width, y), 1)
            
        

        # --- 2. TITOLO ---
        title_text = "THE LAST DREAM"
        subtitle_text = "Il Risveglio"
        title_y = 120
        
        
        
        # Ombra del titolo (
        self.renderer.draw_text(title_text, width // 2 + 4, title_y + 4, Color.BLACK, "large", centered=True)
        # Titolo vero (Oro)
        self.renderer.draw_text(title_text, width // 2, title_y, Color.YELLOW, "large", centered=True)
        
        # Sottotitolo (Azzurro chiaro)
        self.renderer.draw_text(subtitle_text, width // 2, title_y + 60, (150, 200, 255), "medium", centered=True)
        
        # --- 3. PULSANTI MENU ---
        start_y = 380
        
        for i, option in enumerate(self.menu_options):
            opt_y = start_y + (i * 80) 
            is_selected = (i == self.menu_selected)
            
            if is_selected:
                
                box_rect = (width//2 - 200, opt_y - 15, 400, 60)
                pygame.draw.rect(self.renderer.screen, (40, 40, 80), box_rect, 0, 15) 
                pygame.draw.rect(self.renderer.screen, Color.YELLOW, box_rect, 2, 15) # Bordo Oro
                
                # Decorazioni laterali (Spade)
                
                self.renderer.draw_text("⚔", width//2 - 170, opt_y + 5, Color.YELLOW, "medium", centered=True)
                self.renderer.draw_text("⚔", width//2 + 170, opt_y + 5, Color.YELLOW, "medium", centered=True)
                
                # Testo Bianco Acceso
                self.renderer.draw_text(option.upper(), width // 2, opt_y + 5, Color.WHITE, "medium", centered=True)
            else:
                
                self.renderer.draw_text(option, width // 2, opt_y + 5, (100, 100, 120), "medium", centered=True)
        
        # --- 4. FOOTER ---
        self.renderer.draw_text("Usa FRECCE per muoverti, INVIO per confermare", width // 2, height - 40, (60, 60, 80), "small", centered=True)

    def _render_level_selection(self):
        """Disegna il menu di selezione livelli"""
        width = self.renderer.width
        height = self.renderer.height
        
        self.renderer.clear((15, 15, 25))
        
        # Titolo
        self.renderer.draw_text("SELEZIONA LIVELLO", width // 2, 80, Color.YELLOW, "large", centered=True)
        pygame.draw.line(self.renderer.screen, Color.GRAY, (50, 120), (width-50, 120), 1)
        
        # Lista Livelli
        start_y = 200
        for i, level_name in enumerate(self.level_names):
            y = start_y + (i * 80)
            
            # Determina stato livello (Sbloccato / Bloccato)
            is_unlocked = i <= self.max_unlocked_index
            is_selected = (i == self.level_selection_index)
            
            # Colore base
            if not is_unlocked:
                color = (100, 100, 100) 
                prefix = "🔒 "
            elif is_selected:
                color = Color.YELLOW
                prefix = "► "
            else:
                color = Color.WHITE
                prefix = "   "
                
            # Disegna Box
            box_rect = (width//2 - 250, y - 20, 500, 60)
            if is_selected:
                pygame.draw.rect(self.renderer.screen, (50, 50, 80), box_rect)
                pygame.draw.rect(self.renderer.screen, color, box_rect, 2)
            elif not is_unlocked:
                pygame.draw.rect(self.renderer.screen, (30, 30, 30), box_rect)
            
            self.renderer.draw_text(f"{prefix}{level_name}", width // 2, y, color, "medium", centered=True)

        self.renderer.draw_text("INVIO: Gioca  |  ESC: Menu Principale", width // 2, height - 50, Color.GRAY, "small", centered=True)

    def _handle_level_selection_input(self, key):
        """Gestisce input nel menu livelli"""
        current_time = pygame.time.get_ticks()
        
        if key == pygame.K_UP or key == pygame.K_w:
            self.level_selection_index = (self.level_selection_index - 1) % len(self.level_files)
            self.key_cooldown = current_time
            
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.level_selection_index = (self.level_selection_index + 1) % len(self.level_files)
            self.key_cooldown = current_time
            
        elif key == pygame.K_RETURN:
            # Controlla se è sbloccato
            if self.level_selection_index <= self.max_unlocked_index:
                # Carica il livello selezionato
                self.current_level_index = self.level_selection_index
                self._load_current_level()
                self.state = GameState.EXPLORATION
            else:
                self._show_message("🔒 Livello bloccato! Completa i precedenti.")
            self.key_cooldown = current_time
            
        elif key == pygame.K_ESCAPE:
            self.state = GameState.MENU
            self.key_cooldown = current_time

    def _render_char_creation(self):
        """Renderizza la creazione personaggi"""
        width = self.renderer.width
        height = self.renderer.height
        
        player_num = self.creation_phase + 1
        
        # Sfondo
        self.renderer.clear((15, 15, 20))
        
        # TITOLO FASE
        self.renderer.draw_text(f"CREAZIONE EROE {player_num}/2", width // 2, 40, Color.YELLOW, "large", centered=True)
        pygame.draw.line(self.renderer.screen, Color.GRAY, (50, 80), (width-50, 80), 1)
        
        # --- BOX SINISTRO: NOME ---
        
        input_y = 130
        self.renderer.draw_text("1. SCEGLI IL NOME", width // 2, input_y, Color.LIGHT_BLUE, "medium", centered=True)
        
        # Box Input
        box_width = 400
        box_x = (width - box_width) // 2
        pygame.draw.rect(self.renderer.screen, (30, 30, 40), (box_x, input_y + 40, box_width, 50))
        pygame.draw.rect(self.renderer.screen, Color.WHITE, (box_x, input_y + 40, box_width, 50), 2)
        
        # Testo Nome 
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        name_display = (self.temp_name + cursor) if len(self.temp_name) < 12 else self.temp_name
        self.renderer.draw_text(name_display, width // 2, input_y + 55, Color.GREEN, "medium", centered=True)
        
        # --- BOX CENTRALE: CLASSE ---
        class_y = 260
        self.renderer.draw_text("2. SCEGLI LA CLASSE", width // 2, class_y, Color.LIGHT_BLUE, "medium", centered=True)
        
        # Recupera info classe corrente
        selected_class = self.available_classes[self.temp_class_index]
        class_info = Character.get_class_info(selected_class)
        
        # Selettore a Frecce
        arrow_y = class_y + 50
        pygame.draw.polygon(self.renderer.screen, Color.YELLOW, [(width//2 - 160, arrow_y), (width//2 - 140, arrow_y - 15), (width//2 - 140, arrow_y + 15)])
        self.renderer.draw_text(class_info['name'], width // 2, arrow_y - 10, Color.YELLOW, "large", centered=True)
        pygame.draw.polygon(self.renderer.screen, Color.YELLOW, [(width//2 + 160, arrow_y), (width//2 + 140, arrow_y - 15), (width//2 + 140, arrow_y + 15)])
        
        self.renderer.draw_text("Usa le freccette per cambiare", width // 2, arrow_y + 35, Color.GRAY, "small", centered=True)
        
        # --- BOX INFERIORE: STATISTICHE E DESCRIZIONE ---
        stats_y = 400
        panel_w = 600
        panel_x = (width - panel_w) // 2
        
        # Sfondo pannello stats
        pygame.draw.rect(self.renderer.screen, (25, 25, 35), (panel_x, stats_y, panel_w, 250), 0, 10)
        pygame.draw.rect(self.renderer.screen, (60, 60, 80), (panel_x, stats_y, panel_w, 250), 2, 10)
        
        
        self.ui_manager.draw_stat_bar_labeled(panel_x + 50, stats_y + 30, 200, 15, class_info['max_hp'], 200, Color.GREEN, "HP ")
        self.ui_manager.draw_stat_bar_labeled(panel_x + 320, stats_y + 30, 200, 15, class_info['max_mp'], 100, Color.BLUE, "MP ")
        
        
        self.ui_manager.draw_stat_bar_labeled(panel_x + 50, stats_y + 70, 200, 15, class_info['atk_bonus'], 15, Color.ORANGE, "ATK")
        self.ui_manager.draw_stat_bar_labeled(panel_x + 320, stats_y + 70, 200, 15, class_info['mag_bonus'], 15, Color.PURPLE, "MAG")
        
        # Descrizione
        pygame.draw.line(self.renderer.screen, (60, 60, 80), (panel_x + 20, stats_y + 110), (panel_x + panel_w - 20, stats_y + 110), 1)
        
        desc_lines = class_info['description'].split('.') 
        text_y = stats_y + 130
        for line in desc_lines:
            if line.strip():
                self.renderer.draw_text(line.strip() + ".", width // 2, text_y, Color.WHITE, "small", centered=True)
                text_y += 25
        
        # Istruzioni finali
        self.renderer.draw_text("Premi INVIO per Confermare", width // 2, height - 60, Color.GREEN, "medium", centered=True)
    
    def _render_exploration(self):
        """Renderizza la modalità esplorazione"""
        if not self.world or not self.movement_manager:
            return
        
        # Disegna mappa 
        pos = self.movement_manager.get_position()
        self.renderer.draw_world_view(self.world, pos, self.party, offset_x=262, offset_y=150)
        
        # UI esplorazione
        self.ui_manager.draw_exploration_ui(self.party, self.world.name, pos)
        
        # Istruzioni
        width = self.renderer.width
        height = self.renderer.height
        self.renderer.draw_text("WASD/Frecce: Muovi | I: Inventario | ESC: Menu",
                               width // 2, height - 20, Color.GRAY, "small", centered=True)
    
    def _render_combat(self):
        """Renderizza il combattimento"""
        if not self.current_battle:
            return
        
        current = self.current_battle.turn_manager.get_current_combatant()
        current_name = current.name if current and current.is_player else None
        
        self.ui_manager.draw_combat_ui_split_screen(
            self.party,
            self.current_battle.enemy,
            current_name
        )
    
    def _render_inventory(self):
        """Renderizza l'inventario"""
        self.ui_manager.draw_inventory_ui(self.party.inventory, self.inventory_selected)
        
        # Istruzioni
        width = self.renderer.width
        height = self.renderer.height
        self.renderer.draw_text("↑↓: Naviga | ESC/I: Chiudi", width // 2, height - 20,
                               Color.GRAY, "small", centered=True)
    
    def _render_game_over(self):
        """Renderizza il game over (Drammatico)"""
        width = self.renderer.width
        height = self.renderer.height
        
        # Sfondo 
        self.renderer.clear((20, 0, 0))
        
        self.renderer.draw_text("SCONFITTA...", width // 2, height // 2 - 50, Color.RED, "large", centered=True)
        
        # Testo narrativo
        self.renderer.draw_text("Le tenebre hanno avvolto i tuoi eroi.", width // 2, height // 2 + 10, Color.WHITE, "medium", centered=True)
        self.renderer.draw_text("La loro leggenda finisce qui.", width // 2, height // 2 + 40, Color.GRAY, "small", centered=True)
        
        self.renderer.draw_text("Premi INVIO per tornare al menu", width // 2, height // 2 + 100, Color.WHITE, "small", centered=True)
    
    def _render_victory(self):
        """Renderizza la vittoria (Epica)"""
        width = self.renderer.width
        height = self.renderer.height
        
        # Sfondo dorato scuro
        self.renderer.clear((20, 20, 0))
        
        self.renderer.draw_text("MISSIONE COMPIUTA!", width // 2, height // 2 - 50, Color.YELLOW, "large", centered=True)
        
        # Testo narrativo
        self.renderer.draw_text("Hai sconfitto il male che infestava questo luogo!", width // 2, height // 2 + 10, Color.WHITE, "medium", centered=True)
        self.renderer.draw_text("Il bottino è tuo.", width // 2, height // 2 + 40, Color.GRAY, "small", centered=True)
        
        self.renderer.draw_text("Premi INVIO per la gloria", width // 2, height // 2 + 100, Color.WHITE, "small", centered=True)


def main():
    """Entry point"""
    engine = PygameGameEngine()
    engine.run()


if __name__ == "__main__":
    main()