"""
Renderer - Sistema di rendering Pygame
"""

import pygame
from typing import Tuple, Optional, List
from models.world import World, CellType
from models.party import Party


class Color:
    """Colori predefiniti e Palette Dungeon"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Colori UI Base
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    RED = (220, 20, 60)
    GREEN = (34, 139, 34)
    BLUE = (30, 144, 255)
    YELLOW = (255, 215, 0)
    ORANGE = (255, 140, 0)
    PURPLE = (147, 112, 219)
    LIGHT_BLUE = (135, 206, 250)

    # Palette Dungeon (Nuovi)
    FLOOR_1 = (30, 25, 35)      # Pavimento scuro (base)
    FLOOR_2 = (38, 32, 44)      # Pavimento chiaro (scacchiera)
    WALL_TOP = (160, 160, 170)  # Tetto del muro (luce)
    WALL_FACE = (70, 70, 80)    # Facciata del muro (ombra)
    WALL_SHADOW = (40, 40, 50)  # Ombra alla base
    WOOD = (101, 67, 33)        # Legno (Bauli)
    WOOD_LIGHT = (133, 94, 66)  # Legno chiaro
    GOLD = (255, 215, 0)        # Oro


class Renderer:
    """Classe principale per il rendering"""
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "RPG Game"):
        """
        Inizializza il renderer
        
        Args:
            width: Larghezza finestra
            height: Altezza finestra
            title: Titolo finestra
        """
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        # Font
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Clock per FPS
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Dimensioni celle mappa
        self.cell_size = 64
    
    def clear(self, color: Tuple[int, int, int] = None):
        """Pulisce lo schermo"""
        if color is None:
            color = Color.BLACK
        self.screen.fill(color)
    
    def draw_text(self, text: str, x: int, y: int, 
                  color: Tuple[int, int, int] = Color.WHITE,
                  font_size: str = "medium", centered: bool = False):
        """
        Disegna testo sullo schermo
        
        Args:
            text: Testo da disegnare
            x: Posizione X
            y: Posizione Y
            color: Colore del testo
            font_size: Dimensione font ("small", "medium", "large")
            centered: Se True, centra il testo su (x, y)
        """
        if font_size == "small":
            font = self.font_small
        elif font_size == "large":
            font = self.font_large
        else:
            font = self.font_medium
        
        text_surface = font.render(text, True, color)
        
        if centered:
            rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, rect)
        else:
            self.screen.blit(text_surface, (x, y))
    
    def draw_rect(self, x: int, y: int, width: int, height: int,
                  color: Tuple[int, int, int], filled: bool = True):
        """Disegna un rettangolo"""
        rect = pygame.Rect(x, y, width, height)
        if filled:
            pygame.draw.rect(self.screen, color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect, 2)


    def draw_floor_tile(self, x, y, size, grid_x, grid_y):
        """Disegna il pavimento a scacchiera con dettagli"""
        # Scacchiera basata sulla posizione x,y della griglia
        if (grid_x + grid_y) % 2 == 0:
            color = Color.FLOOR_1
        else:
            color = Color.FLOOR_2
        
        pygame.draw.rect(self.screen, color, (x, y, size, size))
        
        # Dettagli casuali (Sassolini/Crepe) fissi in base alle coordinate
        # Usiamo le coordinate come "seed" per la casualità, così non tremolano
        pseudo_random = (grid_x * grid_y * 13 + grid_x) % 10
        
        if pseudo_random == 0: # Sassolini
            pygame.draw.circle(self.screen, (50, 50, 60), (x + size//3, y + size//2), 3)
            pygame.draw.circle(self.screen, (50, 50, 60), (x + size//2 + 5, y + size//2 + 5), 2)
        elif pseudo_random == 1: # Crepa
            pygame.draw.line(self.screen, (20, 20, 25), (x + 10, y + 10), (x + 20, y + 20), 2)

    def draw_wall_tile(self, x, y, size, grid_x, grid_y):
        """Disegna un muro 2.5D con dettagli e torce occasionali"""
        face_height = int(size * 0.45) # Faccia un po' più alta per stile cartoon
        
        # 1. Facciata (Mattoni scuri)
        pygame.draw.rect(self.screen, Color.WALL_FACE, (x, y + size - face_height, size, face_height))
        
        # Dettaglio Mattoni (Linee orizzontali scure)
        brick_y = y + size - face_height + 10
        pygame.draw.line(self.screen, (50, 50, 60), (x, brick_y), (x + size, brick_y), 2)
        
        # 2. Tetto (Pietra più chiara)
        pygame.draw.rect(self.screen, Color.WALL_TOP, (x, y, size, size - face_height))
        
        # 3. Highlight "Cartoon" (Bordo bianco semitrasparente simulato)
        pygame.draw.line(self.screen, (190, 190, 200), (x + 2, y + 2), (x + size - 2, y + 2), 2)
        
        # 4. Ombra netta sotto il tetto (Pop-out effect)
        pygame.draw.rect(self.screen, (30, 30, 40), (x, y + size - face_height, size, 4))

        # 5. TORCIA (Solo su alcuni muri, basato su coordinate fisse)
        # Mette una torcia se le coordinate soddisfano una regola matematica (es. numeri dispari)
        if (grid_x + grid_y * 3) % 5 == 0:
            self.draw_torch(x + size // 2, y + size - face_height + 10)

    def draw_chest_tile(self, x, y, size):
        """Disegna un baule del tesoro"""
        # Sfondo pavimento prima
        pygame.draw.rect(self.screen, Color.FLOOR_1, (x, y, size, size))
        
        margin = 10
        chest_w = size - (margin * 2)
        chest_h = size - (margin * 2) - 5
        cx, cy = x + margin, y + margin + 5
        
        # Corpo baule
        pygame.draw.rect(self.screen, Color.WOOD, (cx, cy, chest_w, chest_h))
        # Bordo Oro
        pygame.draw.rect(self.screen, Color.GOLD, (cx, cy, chest_w, chest_h), 2)
        # Serratura
        pygame.draw.rect(self.screen, Color.GOLD, (cx + chest_w//2 - 3, cy + chest_h//2 - 3, 6, 8))

    def draw_stairs_tile(self, x, y, size, is_exit=True):
        """Disegna scale (Uscita)"""
        color = Color.BLACK if is_exit else Color.FLOOR_2
        pygame.draw.rect(self.screen, color, (x, y, size, size))
        
        # Disegna quadrati concentrici per simulare la discesa
        steps = 4
        for i in range(steps):
            inset = i * 5
            c = 50 + (i * 30) # Gradiente di grigio
            rect = (x + inset, y + inset, size - inset*2, size - inset*2)
            pygame.draw.rect(self.screen, (c, c, c), rect, 2)
    
    def draw_torch(self, x, y):
        """Disegna una torcia animata sul muro"""
        # Supporto in ferro scuro
        pygame.draw.line(self.screen, (40, 30, 20), (x, y + 5), (x, y + 15), 4)
        
        # Calcola sfarfallio basato sul tempo
        import math
        ticks = pygame.time.get_ticks()
        flicker_size = math.sin(ticks / 100) * 2     # Pulsazione lenta
        flicker_pos = math.cos(ticks / 50) * 1       # Tremolio veloce
        
        # Alone di luce (semitrasparente simulato con cerchi concentrici)
        glow_color = (60, 40, 20) # Alone scuro su muro
        pygame.draw.circle(self.screen, glow_color, (x, y), 12 + flicker_size)
        
        # Fiamma Esterna (Arancione/Rosso)
        pygame.draw.circle(self.screen, (255, 69, 0), (x + flicker_pos, y), 6 + flicker_size)
        
        # Fiamma Interna (Giallo/Bianco)
        pygame.draw.circle(self.screen, (255, 255, 100), (x, y + 2), 3)

    def get_hero_style(self, character_class: str):
        """Restituisce colori e stile in base alla classe del personaggio"""
        # Normalizza il nome (es. "Warrior" -> "warrior")
        cls = str(character_class).lower()
        
        if "warrior" in cls or "guerriero" in cls:
            return (50, 100, 200), (180, 180, 190), "knight" # Blu/Argento
        elif "paladin" in cls or "sentinella" in cls:
            return (220, 220, 220), (255, 215, 0), "knight"  # Bianco/Oro
        elif "mage" in cls or "mago" in cls:
            return (75, 0, 130), (255, 215, 0), "mage"       # Viola/Oro
        elif "rogue" in cls or "ladro" in cls:
            return (60, 60, 60), (30, 30, 30), "mage"        # Grigio scuro (Cappuccio)
        elif "ranger" in cls or "cacciatore" in cls:
            return (34, 139, 34), (101, 67, 33), "mage"      # Verde/Marrone
        else:
            return (100, 100, 100), (50, 50, 50), "knight"   # Default
        
    def draw_mini_hero(self, x, y, color_body, color_hat, style="knight"):
        """Disegna un piccolo eroe in stile Chibi (Testa grande)"""
        # Ombra sotto i piedi
        pygame.draw.ellipse(self.screen, (0, 0, 0), (x - 8, y + 8, 16, 6))
        
        # Corpo (piccolo rettangolo)
        pygame.draw.rect(self.screen, color_body, (x - 6, y, 12, 10), 0, 3)
        
        # Testa (grande cerchio/quadrato arrotondato)
        head_y = y - 10
        pygame.draw.circle(self.screen, (255, 220, 200), (x, head_y), 9) # Pelle
        
        # Cappello/Elmo
        if style == "knight":
            # Elmo grigio con visiera
            pygame.draw.arc(self.screen, color_hat, (x - 10, head_y - 12, 20, 22), 0, 3.14, 10)
            pygame.draw.line(self.screen, (50, 50, 50), (x - 9, head_y - 2), (x + 9, head_y - 2), 2)
            # Pennacchio rosso
            pygame.draw.line(self.screen, (220, 20, 20), (x, head_y - 12), (x, head_y - 16), 3)
        else: # Mago/Rogue
            # Cappuccio
            pygame.draw.polygon(self.screen, color_hat, [
                (x - 10, head_y), (x + 10, head_y), (x, head_y - 18)
            ])
        
        # Occhi (due puntini neri carini)
        eye_y = head_y + 1
        pygame.draw.circle(self.screen, (0, 0, 0), (x - 3, eye_y), 2)
        pygame.draw.circle(self.screen, (0, 0, 0), (x + 3, eye_y), 2)


    def draw_portal_tile(self, x, y, size):
        """
        Disegna un portale rosso (vortice) animato al posto del nemico.
        """
        # Centro della cella
        cx = x + size // 2
        cy = y + size // 2
        
        # Gestione tempo per animazione rotazione/pulsazione
        import math
        ticks = pygame.time.get_ticks()
        
        # Effetto pulsazione (il portale si allarga e stringe leggermente)
        pulse = math.sin(ticks / 200) * 2 
        
        # 1. Base nera (Il buco nel vuoto)
        pygame.draw.circle(self.screen, (0, 0, 0), (cx, cy), size // 2 - 5)
        
        # 2. Anello esterno Rosso Scuro (Bordo del vortice)
        pygame.draw.circle(self.screen, (139, 0, 0), (cx, cy), size // 2 - 5 + pulse, 3)
        
        # 3. Spirale interna (Linee che ruotano per simulare il vortice)
        # Disegniamo 3 archi che ruotano
        angle_offset = ticks / 500 # Velocità rotazione
        
        for i in range(3):
            # Calcola angoli sfasati di 120 gradi (2/3 pigreco)
            start_angle = angle_offset + (i * (2 * math.pi / 3))
            end_angle = start_angle + math.pi # Arco di 180 gradi
            
            rect_spiral = (cx - 15, cy - 15, 30, 30)
            pygame.draw.arc(self.screen, (255, 50, 50), rect_spiral, start_angle, end_angle, 2)
            
            # Un secondo livello di spirale più largo
            rect_spiral_out = (cx - 22, cy - 22, 44, 44)
            pygame.draw.arc(self.screen, (100, 0, 0), rect_spiral_out, start_angle - 0.5, end_angle - 0.5, 3)

        # 4. Centro luminoso (Il cuore del pericolo)
        pygame.draw.circle(self.screen, (255, 0, 0), (cx, cy), 4)


    def draw_world_view(self, world: World, player_pos: Tuple[int, int], party: Party,
                       offset_x: int = 50, offset_y: int = 50):
        """
        Versione aggiornata: Mostra i portali al posto dei nemici.
        """
        px, py = player_pos
        
        # --- 1. DISEGNA LA MAPPA ---
        for y in range(world.height):
            for x in range(world.width):
                cell_value = world.get_cell(x, y)
                screen_x = offset_x + x * self.cell_size
                screen_y = offset_y + y * self.cell_size
                
                # Pavimento base
                self.draw_floor_tile(screen_x, screen_y, self.cell_size, x, y)
                
                if cell_value == CellType.WALL.value:
                    self.draw_wall_tile(screen_x, screen_y, self.cell_size, x, y)
                elif cell_value == CellType.TREASURE.value:
                    self.draw_chest_tile(screen_x, screen_y, self.cell_size)
                elif cell_value == CellType.EXIT.value:
                    self.draw_stairs_tile(screen_x, screen_y, self.cell_size)
                
                # --- MODIFICA QUI ---
                elif cell_value == CellType.DANGER.value:
                    # Invece di draw_mini_enemy, usiamo draw_portal_tile
                    self.draw_portal_tile(screen_x, screen_y, self.cell_size)
                # --------------------

                elif cell_value == CellType.START.value:
                     pygame.draw.rect(self.screen, (50, 100, 50), (screen_x + 10, screen_y + 10, self.cell_size - 20, self.cell_size - 20), 0, 5)
                     pygame.draw.rect(self.screen, (80, 150, 80), (screen_x + 10, screen_y + 10, self.cell_size - 20, self.cell_size - 20), 2, 5)

        # --- 2. DISEGNA GLI EROI DEL PARTY (RESTO DEL CODICE INVARIATO) ---
        player_screen_x = offset_x + px * self.cell_size
        player_screen_y = offset_y + py * self.cell_size
        center_x = player_screen_x + self.cell_size // 2
        center_y = player_screen_y + self.cell_size // 2 + 5
        
        import math
        breath_y = math.sin(pygame.time.get_ticks() / 150) * 2
        
        num_heroes = len(party.characters)
        start_offset = -12 if num_heroes > 1 else 0
        spacing = 24 if num_heroes > 1 else 0
        
        for i, char in enumerate(party.characters):
            body_col, hat_col, style = self.get_hero_style(char.character_class)
            hero_x = center_x + start_offset + (i * spacing)
            self.draw_mini_hero(hero_x, center_y + breath_y, body_col, hat_col, style)
    
    def draw_hp_bar(self, x: int, y: int, width: int, height: int,
                   current: int, maximum: int, color: Tuple[int, int, int] = Color.GREEN):
        """
        Disegna una barra HP
        
        Args:
            x, y: Posizione
            width, height: Dimensioni
            current: HP attuali
            maximum: HP massimi
            color: Colore della barra
        """
        # Bordo
        self.draw_rect(x, y, width, height, Color.WHITE, filled=False)
        
        # Background
        self.draw_rect(x + 2, y + 2, width - 4, height - 4, Color.DARK_GRAY)
        
        # Barra HP
        if maximum > 0:
            hp_percentage = current / maximum
            hp_width = int((width - 4) * hp_percentage)
            
            # Cambia colore in base agli HP
            if hp_percentage > 0.6:
                bar_color = Color.GREEN
            elif hp_percentage > 0.3:
                bar_color = Color.YELLOW
            else:
                bar_color = Color.RED
            
            if hp_width > 0:
                self.draw_rect(x + 2, y + 2, hp_width, height - 4, bar_color)
        
        # Testo HP
        hp_text = f"{current}/{maximum}"
        self.draw_text(hp_text, x + width // 2, y + height // 2, 
                      Color.WHITE, "small", centered=True)
    
    def draw_mp_bar(self, x: int, y: int, width: int, height: int,
                   current: int, maximum: int):
        """Disegna una barra MP (simile a HP ma blu)"""
        # Bordo
        self.draw_rect(x, y, width, height, Color.WHITE, filled=False)
        
        # Background
        self.draw_rect(x + 2, y + 2, width - 4, height - 4, Color.DARK_GRAY)
        
        # Barra MP
        if maximum > 0:
            mp_percentage = current / maximum
            mp_width = int((width - 4) * mp_percentage)
            
            if mp_width > 0:
                self.draw_rect(x + 2, y + 2, mp_width, height - 4, Color.LIGHT_BLUE)
        
        # Testo MP
        mp_text = f"{current}/{maximum}"
        self.draw_text(mp_text, x + width // 2, y + height // 2,
                      Color.WHITE, "small", centered=True)
    
    def update(self):
        """Aggiorna il display"""
        pygame.display.flip()
        self.clock.tick(self.fps)
    
    def quit(self):
        """Chiude Pygame"""
        pygame.quit()