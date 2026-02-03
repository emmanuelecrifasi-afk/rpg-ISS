"""
UI Manager - Gestisce le interfacce utente
"""

import pygame
from typing import List, Tuple
from models.party import Party
from models.character import Character
from combat.enemy import Enemy
from rendering.renderer import Renderer, Color


class UIManager:
    """Gestisce le interfacce utente del gioco"""
    
    def __init__(self, renderer: Renderer):
        """
        Inizializza l'UI Manager
        
        Args:
            renderer: Istanza del Renderer
        """
        self.renderer = renderer
    
    def _draw_hero_sprite(self, x, y, char, is_active):
        """
        Disegna lo sprite dell'eroe.
        - Guerriero: Versione "Warlord" (Platino, Oro, Mantello Epico)
        - Ladro, Paladino, Ranger, Mago: Versioni Deluxe (Migliorate)
        """
        x = int(x)
        y = int(y)
        
        # Animazione Respiro
        bounce_y = 0
        if is_active:
            import math
            bounce_y = int(math.sin(pygame.time.get_ticks() / 150) * 5)
        
        draw_y = y + bounce_y
        
        SKIN = (255, 200, 180)
        cls = str(char.character_class).upper()

        # --- 1. GUERRIERO (WARRIOR) ---
        if "WARRIOR" in cls or "GUERRIERO" in cls or "FENDENTE" in cls:
            PLATINUM = (229, 228, 226)
            STEEL_DARK = (112, 128, 144)
            GOLD_TRIM = (255, 215, 0)
            CRIMSON = (139, 0, 0)
            
            # Mantello 
            pygame.draw.polygon(self.renderer.screen, CRIMSON, [
                (x - 20, draw_y - 35), # Spalla SX
                (x + 20, draw_y - 35), # Spalla DX
                (x + 35, draw_y + 20), # Fondo DX largo
                (x - 35, draw_y + 20)  # Fondo SX largo
            ])
            
            # Corpo (Corazza)
            pygame.draw.rect(self.renderer.screen, PLATINUM, (x - 22, draw_y - 35, 44, 50), 0, 8)
            # Dettaglio pettorale
            pygame.draw.line(self.renderer.screen, GOLD_TRIM, (x - 22, draw_y - 30), (x, draw_y - 10), 3)
            pygame.draw.line(self.renderer.screen, GOLD_TRIM, (x + 22, draw_y - 30), (x, draw_y - 10), 3)
            # Cintura 
            pygame.draw.rect(self.renderer.screen, STEEL_DARK, (x - 22, draw_y - 5, 44, 6))
            pygame.draw.circle(self.renderer.screen, GOLD_TRIM, (x, draw_y - 2), 5) # Fibbia

            # Spallacci 
            pygame.draw.circle(self.renderer.screen, PLATINUM, (x - 28, draw_y - 32), 14)
            pygame.draw.circle(self.renderer.screen, PLATINUM, (x + 28, draw_y - 32), 14)
            pygame.draw.circle(self.renderer.screen, GOLD_TRIM, (x - 28, draw_y - 32), 6) # Borchia oro
            pygame.draw.circle(self.renderer.screen, GOLD_TRIM, (x + 28, draw_y - 32), 6)

            # Testa 
            pygame.draw.circle(self.renderer.screen, PLATINUM, (x, draw_y - 48), 16)
            # Visiera a croce scura
            pygame.draw.line(self.renderer.screen, (20, 20, 20), (x - 12, draw_y - 48), (x + 12, draw_y - 48), 3) # Orizzontale
            pygame.draw.line(self.renderer.screen, (20, 20, 20), (x, draw_y - 58), (x, draw_y - 38), 3) # Verticale
            
            # Cresta Rossa 
            pygame.draw.polygon(self.renderer.screen, (220, 20, 60), [
                (x - 5, draw_y - 60), 
                (x + 5, draw_y - 60), 
                (x + 20, draw_y - 45), # Coda della cresta
                (x - 10, draw_y - 65)  # Punta in alto
            ])

            # Scudo  
            pygame.draw.rect(self.renderer.screen, (20, 30, 60), (x - 50, draw_y - 25, 25, 50), 0, 4) # Blu notte
            pygame.draw.rect(self.renderer.screen, GOLD_TRIM, (x - 50, draw_y - 25, 25, 50), 3, 4) # Bordo Oro
            pygame.draw.line(self.renderer.screen, GOLD_TRIM, (x - 50, draw_y - 25), (x - 25, draw_y + 25), 2) # Decorazione diagonale

            # Spadone 
            pygame.draw.rect(self.renderer.screen, (240, 240, 240), (x + 35, draw_y - 70, 10, 55)) # Lama larga
            pygame.draw.line(self.renderer.screen, (100, 100, 100), (x + 40, draw_y - 70), (x + 40, draw_y - 20), 1) # Scanalatura lama
            
            pygame.draw.line(self.renderer.screen, GOLD_TRIM, (x + 25, draw_y - 15), (x + 55, draw_y - 15), 5)

        # --- 2. LADRO (ROGUE)  ---
        elif "ROGUE" in cls or "LADRO" in cls:
            CLOTH_DARK = (40, 40, 45)
            CLOTH_ACCENT = (70, 70, 80)
            SCARF = (30, 30, 30)
            
            # Mantello 
            pygame.draw.polygon(self.renderer.screen, (20, 20, 20), [(x - 15, draw_y - 30), (x + 15, draw_y - 30), (x, draw_y + 10)])
            # Corpo
            pygame.draw.rect(self.renderer.screen, CLOTH_DARK, (x - 15, draw_y - 35, 30, 45), 0, 5)
            # Cintura 
            pygame.draw.rect(self.renderer.screen, (60, 50, 40), (x - 15, draw_y - 5, 30, 6))
            pygame.draw.rect(self.renderer.screen, (80, 70, 50), (x + 5, draw_y - 2, 6, 8))
            # Testa 
            pygame.draw.circle(self.renderer.screen, CLOTH_ACCENT, (x, draw_y - 45), 15)
            # Ombra nera 
            pygame.draw.ellipse(self.renderer.screen, (0, 0, 0), (x - 10, draw_y - 48, 20, 18))
            # Sciarpa
            pygame.draw.rect(self.renderer.screen, SCARF, (x - 12, draw_y - 35, 24, 8), 0, 2)
            # Pugnali
            pygame.draw.line(self.renderer.screen, (180, 180, 180), (x - 25, draw_y - 10), (x - 25, draw_y + 10), 3)
            pygame.draw.line(self.renderer.screen, (100, 50, 0), (x - 28, draw_y - 5), (x - 22, draw_y - 5), 4)
            pygame.draw.line(self.renderer.screen, (180, 180, 180), (x + 25, draw_y - 10), (x + 25, draw_y + 10), 3)
            pygame.draw.line(self.renderer.screen, (100, 50, 0), (x + 28, draw_y - 5), (x + 22, draw_y - 5), 4)

        # --- 3. PALADINO (PALADIN) ---
        elif "PALADIN" in cls or "SENTINELLA" in cls:
            PLATE_WHITE = (240, 240, 255)
            GOLD_TRIM = (255, 223, 0)
            CAPE_WHITE = (255, 255, 255)
            pygame.draw.rect(self.renderer.screen, CAPE_WHITE, (x - 18, draw_y - 30, 36, 60)) # Mantello
            pygame.draw.rect(self.renderer.screen, PLATE_WHITE, (x - 22, draw_y - 35, 44, 50), 0, 6) # Corpo
            # Croce Oro
            pygame.draw.line(self.renderer.screen, GOLD_TRIM, (x, draw_y - 30), (x, draw_y + 10), 5)
            pygame.draw.line(self.renderer.screen, GOLD_TRIM, (x - 10, draw_y - 10), (x + 10, draw_y - 10), 5)
            # Spallacci
            pygame.draw.circle(self.renderer.screen, GOLD_TRIM, (x - 26, draw_y - 32), 11)
            pygame.draw.circle(self.renderer.screen, GOLD_TRIM, (x + 26, draw_y - 32), 11)
            # Testa
            pygame.draw.circle(self.renderer.screen, PLATE_WHITE, (x, draw_y - 45), 15)
            pygame.draw.line(self.renderer.screen, GOLD_TRIM, (x, draw_y - 60), (x, draw_y - 35), 2)
            pygame.draw.rect(self.renderer.screen, (0, 0, 0), (x - 8, draw_y - 48, 16, 3))
            # Scudo 
            pygame.draw.rect(self.renderer.screen, PLATE_WHITE, (x - 45, draw_y - 25, 24, 45), 0, 5)
            pygame.draw.rect(self.renderer.screen, GOLD_TRIM, (x - 45, draw_y - 25, 24, 45), 3, 5)
            pygame.draw.line(self.renderer.screen, (200, 0, 0), (x - 33, draw_y - 20), (x - 33, draw_y + 15), 4)
            pygame.draw.line(self.renderer.screen, (200, 0, 0), (x - 40, draw_y - 5), (x - 26, draw_y - 5), 4)
            # Martello
            pygame.draw.line(self.renderer.screen, (100, 60, 20), (x + 30, draw_y + 15), (x + 30, draw_y - 35), 4)
            pygame.draw.rect(self.renderer.screen, (150, 150, 150), (x + 20, draw_y - 45, 20, 15))

        # --- 4. RANGER  ---
        elif "RANGER" in cls or "ARCHER" in cls or "CACCIATORE" in cls:
            CLOAK_GREEN = (40, 80, 40)
            LEATHER = (139, 69, 19)
            pygame.draw.polygon(self.renderer.screen, CLOAK_GREEN, [(x, draw_y - 35), (x - 20, draw_y + 20), (x + 20, draw_y + 20)])
            pygame.draw.rect(self.renderer.screen, (60, 100, 60), (x - 18, draw_y - 35, 36, 45), 0, 5)
            pygame.draw.line(self.renderer.screen, LEATHER, (x - 18, draw_y), (x + 18, draw_y), 4)
            pygame.draw.line(self.renderer.screen, LEATHER, (x - 18, draw_y - 30), (x + 18, draw_y + 15), 2)
            # Faretra
            pygame.draw.rect(self.renderer.screen, (160, 82, 45), (x + 10, draw_y - 55, 10, 30))
            pygame.draw.line(self.renderer.screen, (255, 255, 255), (x + 12, draw_y - 55), (x + 10, draw_y - 65), 2)
            pygame.draw.line(self.renderer.screen, (255, 255, 255), (x + 16, draw_y - 55), (x + 18, draw_y - 65), 2)
            # Testa
            pygame.draw.circle(self.renderer.screen, CLOAK_GREEN, (x, draw_y - 45), 15)
            pygame.draw.circle(self.renderer.screen, SKIN, (x, draw_y - 45), 9)
            # Arco
            pygame.draw.arc(self.renderer.screen, (100, 50, 0), (x - 45, draw_y - 40, 30, 70), 3.14, 6.28, 3)
            pygame.draw.line(self.renderer.screen, (200, 200, 200), (x - 45, draw_y - 5), (x - 15, draw_y - 5), 1)

        # --- 5. MAGO (MAGE)  ---
        elif "MAGE" in cls or "MAGO" in cls or "ARCANA" in cls:
            ROBE_PURPLE = (75, 0, 130)
            ROBE_GOLD = (255, 215, 0)
            pygame.draw.polygon(self.renderer.screen, ROBE_PURPLE, [(x, draw_y - 45), (x - 30, draw_y + 25), (x + 30, draw_y + 25)])
            pygame.draw.line(self.renderer.screen, ROBE_GOLD, (x, draw_y - 40), (x, draw_y + 25), 3)
            pygame.draw.circle(self.renderer.screen, SKIN, (x, draw_y - 45), 13)
            pygame.draw.polygon(self.renderer.screen, (240, 240, 240), [(x - 8, draw_y - 40), (x + 8, draw_y - 40), (x, draw_y - 25)]) # Barba
            pygame.draw.polygon(self.renderer.screen, ROBE_PURPLE, [(x - 20, draw_y - 55), (x + 20, draw_y - 55), (x, draw_y - 90)]) # Cappello
            staff_top_y = draw_y - 60
            pygame.draw.line(self.renderer.screen, (100, 50, 20), (x + 35, draw_y + 20), (x + 35, staff_top_y), 3)
            import math
            pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 5
            glow_color = (0, 255, 255)
            pygame.draw.circle(self.renderer.screen, glow_color, (x + 35, staff_top_y), 5 + pulse)
            part_y = staff_top_y + int(math.cos(pygame.time.get_ticks()/100) * 10)
            pygame.draw.circle(self.renderer.screen, (255, 255, 255), (x + 45, part_y), 2)

        
        else:
            pygame.draw.rect(self.renderer.screen, (100, 100, 100), (x - 20, draw_y - 35, 40, 50))
            pygame.draw.circle(self.renderer.screen, SKIN, (x, draw_y - 45), 14)

        # INDICATORE TURNO
        if is_active:
            pygame.draw.polygon(self.renderer.screen, (255, 255, 0), [(x, draw_y - 95), (x - 10, draw_y - 110), (x + 10, draw_y - 110)])

        # KO
        if not char.is_alive:
            pygame.draw.line(self.renderer.screen, (255, 0, 0), (x-20, draw_y-20), (x+20, draw_y+20), 5)
            pygame.draw.line(self.renderer.screen, (255, 0, 0), (x+20, draw_y-20), (x-20, draw_y+20), 5)
    
    def _draw_enemy_sprite(self, x, y, size, name):
        
        x = int(x)
        y = int(y)
        center_x = x + size // 2
        center_y = y + size // 2
        
        # Animazioni
        import math
        time_val = pygame.time.get_ticks()
        breath = int(math.sin(time_val / 200) * 3)
        float_y = int(math.sin(time_val / 300) * 5)
        
        draw_y = y + breath
        center_draw_y = center_y + breath
        
        name_upper = name.upper()

        # --- 1. DRAGHI  ---
        if "DRAGO" in name_upper:
            # Setup Colori
            if "ANTICO" in name_upper: # BOSS
                BODY = (255, 215, 0)       # Oro
                WING = (184, 134, 11)      # Bronzo
                BELLY = (255, 250, 205)    # Crema
                EYE = (220, 20, 60)        # Rubino
                HORN = (255, 255, 255)     # Avorio
                smoke_col = (255, 255, 255)
            else: # NORMALE
                BODY = (180, 30, 30)       # Rosso
                WING = (100, 0, 0)         # Rosso 
                BELLY = (220, 100, 100)    # Rosato
                EYE = (255, 255, 0)        # Giallo
                HORN = (40, 40, 40)        # Grigio 
                smoke_col = (100, 100, 100)

            # Ali 
            wing_y = center_draw_y - 20 + (breath * 2) 
            pygame.draw.polygon(self.renderer.screen, WING, [(center_x, wing_y), (center_x - 140, wing_y - 80), (center_x - 40, wing_y + 60)])
            pygame.draw.polygon(self.renderer.screen, WING, [(center_x, wing_y), (center_x + 140, wing_y - 80), (center_x + 40, wing_y + 60)])
            
            # Coda 
            pygame.draw.polygon(self.renderer.screen, WING, [(center_x - 15, center_draw_y + 40), (center_x + 15, center_draw_y + 40), (center_x, center_draw_y + 130)])
            pygame.draw.circle(self.renderer.screen, HORN, (center_x, center_draw_y + 130), 8) 
            
            # Corpo 
            pygame.draw.ellipse(self.renderer.screen, BODY, (center_x - 50, center_draw_y - 40, 100, 110))
            # Pancia a scaglie 
            pygame.draw.ellipse(self.renderer.screen, BELLY, (center_x - 25, center_draw_y - 20, 50, 80))
            for i in range(0, 60, 15):
                pygame.draw.line(self.renderer.screen, BODY, (center_x - 15, center_draw_y - 10 + i), (center_x + 15, center_draw_y - 10 + i), 2)
            
            # Testa
            head_y = center_draw_y - 70
            head_points = [(center_x, head_y - 40), (center_x - 35, head_y), (center_x, head_y + 40), (center_x + 35, head_y)]
            pygame.draw.polygon(self.renderer.screen, BODY, head_points)
            
            # Occhi 
            pygame.draw.circle(self.renderer.screen, EYE, (center_x - 15, head_y), 6)
            pygame.draw.circle(self.renderer.screen, EYE, (center_x + 15, head_y), 6)
            pygame.draw.line(self.renderer.screen, (0,0,0), (center_x - 15, head_y - 3), (center_x - 12, head_y + 3), 2) # Pupilla
            pygame.draw.line(self.renderer.screen, (0,0,0), (center_x + 15, head_y - 3), (center_x + 18, head_y + 3), 2)
            
            # Corna
            pygame.draw.line(self.renderer.screen, HORN, (center_x - 20, head_y - 20), (center_x - 50, head_y - 50), 5)
            pygame.draw.line(self.renderer.screen, HORN, (center_x + 20, head_y - 20), (center_x + 50, head_y - 50), 5)

            # Fumo 
            off = (time_val // 150) % 5 * 4
            pygame.draw.circle(self.renderer.screen, smoke_col, (center_x - 15, head_y + 30 + off), 5 - off//4)
            pygame.draw.circle(self.renderer.screen, smoke_col, (center_x + 15, head_y + 30 + off), 5 - off//4)

        # --- 2. ORCO  ---
        elif "ORCO" in name_upper or "ORC" in name_upper:
            SKIN = (85, 107, 47)  # Verde 
            ARMOR = (50, 50, 50)  
            LEATHER = (139, 69, 19)
            
            # Corpo 
            pygame.draw.ellipse(self.renderer.screen, SKIN, (center_x - 60, center_draw_y - 30, 120, 100))
            
            # Armatura 
            pygame.draw.rect(self.renderer.screen, ARMOR, (center_x - 65, center_draw_y - 35, 40, 30), 0, 5)
            pygame.draw.line(self.renderer.screen, (200, 200, 200), (center_x - 60, center_draw_y - 40), (center_x - 50, center_draw_y - 25), 3) # Chiodo
            
            # Cinghia 
            pygame.draw.line(self.renderer.screen, LEATHER, (center_x - 50, center_draw_y - 20), (center_x + 40, center_draw_y + 40), 8)
            
            # Testa 
            pygame.draw.circle(self.renderer.screen, SKIN, (center_x, center_draw_y - 40), 35)
            # Elmo 
            pygame.draw.arc(self.renderer.screen, ARMOR, (center_x - 36, center_draw_y - 75, 72, 70), 0, 3.14, 10)
            
            # Zanne 
            pygame.draw.polygon(self.renderer.screen, (240, 240, 220), [(center_x - 20, center_draw_y - 20), (center_x - 20, center_draw_y - 45), (center_x - 10, center_draw_y - 20)])
            pygame.draw.polygon(self.renderer.screen, (240, 240, 220), [(center_x + 20, center_draw_y - 20), (center_x + 20, center_draw_y - 45), (center_x + 10, center_draw_y - 20)])
            
            # Ascia da Guerra 
            pygame.draw.line(self.renderer.screen, (100, 60, 20), (center_x + 50, center_draw_y + 20), (center_x + 50, center_draw_y - 60), 6) # Manico
            pygame.draw.polygon(self.renderer.screen, (100, 100, 100), [(center_x + 50, center_draw_y - 50), (center_x + 80, center_draw_y - 70), (center_x + 80, center_draw_y - 30)]) # Lama

        # --- 3. TROLL  ---
        elif "TROLL" in name_upper:
            SKIN = (100, 110, 120) # Grigio 
            MOSS = (50, 100, 50)   # Muschio
            
            # Corpo 
            pygame.draw.rect(self.renderer.screen, SKIN, (center_x - 50, center_draw_y - 30, 100, 110), 0, 20)
            # Muschio sulle spalle
            pygame.draw.circle(self.renderer.screen, MOSS, (center_x - 40, center_draw_y - 20), 15)
            pygame.draw.circle(self.renderer.screen, MOSS, (center_x + 30, center_draw_y - 15), 20)
            
            # Testa 
            pygame.draw.rect(self.renderer.screen, SKIN, (center_x - 25, center_draw_y - 60, 50, 50), 0, 10)
            
            # Cresta 
            pygame.draw.polygon(self.renderer.screen, (200, 50, 0), [(center_x, center_draw_y - 80), (center_x - 10, center_draw_y - 60), (center_x + 10, center_draw_y - 60)])
            
            # Faccia
            pygame.draw.circle(self.renderer.screen, (50, 50, 60), (center_x, center_draw_y - 40), 8) # Nasone scuro
            pygame.draw.circle(self.renderer.screen, (255, 255, 255), (center_x - 15, center_draw_y - 50), 4) # Occhio SX
            pygame.draw.circle(self.renderer.screen, (255, 255, 255), (center_x + 15, center_draw_y - 45), 3) # Occhio DX (storto)
            
            # Clava 
            pygame.draw.line(self.renderer.screen, (80, 50, 20), (center_x - 50, center_draw_y + 40), (center_x - 70, center_draw_y - 40), 12)
            pygame.draw.circle(self.renderer.screen, (80, 50, 20), (center_x - 70, center_draw_y - 40), 15) # Testa clava

        # --- 4. GOBLIN  ---
        elif "GOBLIN" in name_upper:
            SKIN = (50, 160, 50) # Verde 
            CLOTH = (100, 70, 50) # Cuoio
            
            # Orecchie 
            pygame.draw.polygon(self.renderer.screen, SKIN, [(center_x - 30, center_draw_y - 10), (center_x - 75, center_draw_y - 30), (center_x - 30, center_draw_y + 10)])
            pygame.draw.polygon(self.renderer.screen, SKIN, [(center_x + 30, center_draw_y - 10), (center_x + 75, center_draw_y - 30), (center_x + 30, center_draw_y + 10)])
            
            # Testa
            pygame.draw.circle(self.renderer.screen, SKIN, (center_x, center_draw_y), 40)
            
            # Bandana
            pygame.draw.rect(self.renderer.screen, (200, 50, 50), (center_x - 38, center_draw_y - 25, 76, 12))
            
            # Occhi
            pygame.draw.ellipse(self.renderer.screen, (255, 215, 0), (center_x - 20, center_draw_y - 5, 15, 10))
            pygame.draw.ellipse(self.renderer.screen, (255, 215, 0), (center_x + 5, center_draw_y - 5, 15, 10))
            
            # Sorriso 
            pygame.draw.arc(self.renderer.screen, (0, 0, 0), (center_x - 15, center_draw_y + 5, 30, 20), 3.14, 6.28, 3)
            # Dente 
            pygame.draw.polygon(self.renderer.screen, (255, 255, 255), [(center_x + 5, center_draw_y + 20), (center_x + 8, center_draw_y + 15), (center_x + 11, center_draw_y + 20)])
            
            # Pugnale
            pygame.draw.line(self.renderer.screen, (100, 100, 100), (center_x + 40, center_draw_y + 30), (center_x + 60, center_draw_y + 10), 4)

        # --- 5. SCHELETRO  ---
        elif "SCHELETRO" in name_upper or "SKELETON" in name_upper:
            BONE = (230, 230, 230)
            SHADOW = (20, 20, 20)
            
            # Cassa Toracica
            pygame.draw.rect(self.renderer.screen, BONE, (center_x - 25, center_draw_y + 20, 50, 60), 2)
            for i in range(25, 70, 10):
                pygame.draw.line(self.renderer.screen, BONE, (center_x - 20, center_draw_y + i), (center_x + 20, center_draw_y + i), 2)
            pygame.draw.line(self.renderer.screen, BONE, (center_x, center_draw_y + 20), (center_x, center_draw_y + 80), 4) # Spina dorsale
            
            # Testa (
            pygame.draw.circle(self.renderer.screen, BONE, (center_x, center_draw_y - 20), 35)
            # Mascella
            pygame.draw.rect(self.renderer.screen, BONE, (center_x - 15, center_draw_y + 5, 30, 15))
            
            # Occhi 
            pygame.draw.circle(self.renderer.screen, SHADOW, (center_x - 12, center_draw_y - 20), 8)
            pygame.draw.circle(self.renderer.screen, SHADOW, (center_x + 12, center_draw_y - 20), 8)
            # Naso
            pygame.draw.polygon(self.renderer.screen, SHADOW, [(center_x, center_draw_y - 5), (center_x - 5, center_draw_y + 5), (center_x + 5, center_draw_y + 5)])
            
            # Spada 
            pygame.draw.line(self.renderer.screen, (150, 150, 150), (center_x + 40, center_draw_y), (center_x + 40, center_draw_y - 60), 3)
            pygame.draw.line(self.renderer.screen, (100, 80, 50), (center_x + 30, center_draw_y - 15), (center_x + 50, center_draw_y - 15), 4) # Elsa

        

    def draw_story_background(self):
        """
        Disegna lo sfondo per le scene di dialogo.
        """
        width = self.renderer.width
        height = self.renderer.height
        import math
        import random
        
        ticks = pygame.time.get_ticks()
        
        # 1. Sfondo Cosmico 
        self.renderer.clear((10, 5, 20))
        
        # 2. PORTALE
        center_x = width // 2
        center_y = height // 2 - 50 
        
        # Cerchi pulsanti
        pulse = math.sin(ticks / 500) * 10
        pygame.draw.circle(self.renderer.screen, (30, 20, 50), (center_x, center_y), 150 + pulse)
        pygame.draw.circle(self.renderer.screen, (50, 30, 80), (center_x, center_y), 120 + pulse * 0.8)
        pygame.draw.circle(self.renderer.screen, (20, 10, 30), (center_x, center_y), 90 + pulse * 0.5)
        
        # Runa 
        angle = ticks / 1000
        points = []
        radius = 100
        for i in range(5): 
            theta = angle + i * (2 * math.pi / 5)
            px = center_x + int(radius * math.cos(theta))
            py = center_y + int(radius * math.sin(theta))
            points.append((px, py))
        pygame.draw.lines(self.renderer.screen, (100, 100, 255), True, points, 2)
        
        
        for i in range(20):
            
            p_seed = i * 100
            p_x = (ticks // 2 + p_seed * 50) % width
            p_y = (height - (ticks // 5 + p_seed * 20) % height)
            
            size = (i % 3) + 1
            alpha = 100 + (i % 10) * 15
            color = (alpha, alpha, 255)
            
            if p_y < height - 200: 
                 pygame.draw.circle(self.renderer.screen, color, (p_x, p_y), size)

        # 4. COLONNE 
        col_width = 60
        col_color = (40, 40, 50)
        col_detail = (20, 20, 30)
        
        # Colonna SX
        pygame.draw.rect(self.renderer.screen, col_color, (0, 0, col_width, height))
        pygame.draw.line(self.renderer.screen, col_detail, (10, 0), (10, height), 2)
        pygame.draw.line(self.renderer.screen, col_detail, (40, 0), (40, height), 2)
        
        # Colonna DX
        pygame.draw.rect(self.renderer.screen, col_color, (width - col_width, 0, col_width, height))
        pygame.draw.line(self.renderer.screen, col_detail, (width - 20, 0), (width - 20, height), 2)
        pygame.draw.line(self.renderer.screen, col_detail, (width - 50, 0), (width - 50, height), 2)
        
        # Capitelli e Basi 
        for y_dec in range(50, height, 150):
            pygame.draw.rect(self.renderer.screen, (60, 60, 80), (0, y_dec, col_width + 10, 20)) # SX
            pygame.draw.rect(self.renderer.screen, (60, 60, 80), (width - col_width - 10, y_dec, col_width + 10, 20)) # DX

        
        pygame.draw.rect(self.renderer.screen, (0, 0, 0), (0, 0, width, 60)) # Banda Alta
        
        # Titolo Scena 
        self.renderer.draw_text("◇ THE LAST DREAM ◇", width // 2, 25, (100, 100, 150), "small", centered=True)
        

    def draw_combat_ui_split_screen(self, party, enemy, current_turn=None):
        """
        UI COMBATTIMENTO COMPLETA CON BESTIARIO GRAFICO
        """
        width = self.renderer.width
        height = self.renderer.height
        
        # --- 1. SFONDO ---
        self.renderer.clear((30, 20, 20)) 
        
        # --- 2. DISEGNA IL NEMICO ---
        enemy_x = width // 2 - 100
        enemy_y = 60
        enemy_size = 180
        
        # CHIAMA LA FUNZIONE CHE DISEGNA IL NEMICO CORRETTO
        self._draw_enemy_sprite(enemy_x, enemy_y, enemy_size, enemy.name)
        
        # Nome e Barra Vita
        name_color = Color.YELLOW if "DRAGO" in enemy.name else Color.RED
        self.renderer.draw_text(enemy.name, width // 2, 30, name_color, "large", centered=True)

        bar_x = width // 2 - 150
        bar_y = 260
        pct = max(0, enemy.hp / enemy.max_hp) if enemy.max_hp > 0 else 0
        pygame.draw.rect(self.renderer.screen, (50, 0, 0), (bar_x, bar_y, 300, 15))
        pygame.draw.rect(self.renderer.screen, Color.RED, (bar_x, bar_y, int(300 * pct), 15))
        self.renderer.draw_text(f"{enemy.hp}/{enemy.max_hp}", width // 2, bar_y + 20, Color.WHITE, "small", centered=True)

        # --- 3. DISEGNA GLI EROI  ---
        hero_ground_y = 380 
        num_heroes = len(party.characters)
        spacing = 150 
        start_hero_x = (width - (num_heroes - 1) * spacing) // 2
        
        for i, char in enumerate(party.characters):
            hero_x = start_hero_x + (i * spacing)
            is_active = (current_turn == char.name)
            self._draw_hero_sprite(hero_x, hero_ground_y, char, is_active)

        # --- 4. PANNELLO STATISTICHE ---
        panel_y = 440
        pygame.draw.rect(self.renderer.screen, (20, 20, 30), (0, panel_y, width, height - panel_y))
        pygame.draw.line(self.renderer.screen, (255, 215, 0), (0, panel_y), (width, panel_y), 3) 
        
        panel_width = width // num_heroes if num_heroes > 0 else width
        
        for i, char in enumerate(party.characters):
            panel_x = i * panel_width
            center_panel = panel_x + panel_width // 2
            is_active = (current_turn == char.name)
            
            color = Color.YELLOW if is_active else Color.WHITE
            self.renderer.draw_text(char.name, center_panel, panel_y + 20, color, "medium", centered=True)
            self.draw_stat_bar_labeled(panel_x + 40, panel_y + 50, panel_width - 80, 12, char.hp, char.max_hp, Color.GREEN, "HP")
            self.draw_stat_bar_labeled(panel_x + 40, panel_y + 75, panel_width - 80, 12, char.mp, char.max_mp, Color.BLUE, "MP")

        # --- 5. COMANDI ---
        footer_y = height - 40
        if current_turn and any(c.name == current_turn for c in party.characters):
            cmds = "[1] Attacco  [2] Magia  [3] Cura  [I] Oggetti"
            self.renderer.draw_text(cmds, width // 2, footer_y, Color.YELLOW, "medium", centered=True)
        else:
            self.renderer.draw_text("TURNO NEMICO...", width // 2, footer_y, (255, 100, 100), "medium", centered=True)

    def draw_stat_bar_labeled(self, x, y, width, height, value, max_value, color, label):
        """Disegna una barra statistica con etichetta (es. ATK: [====..])"""
        # Etichetta
        self.renderer.draw_text(label, x, y, Color.WHITE, "small")
        
        # Sfondo barra 
        bar_x = x + 60
        bar_width = width - 60
        self.renderer.draw_rect(bar_x, y, bar_width, height, (60, 60, 60))
        
        # Barra piena
        if max_value > 0:
            fill_pct = min(1.0, value / max_value)
            fill_w = int(bar_width * fill_pct)
            self.renderer.draw_rect(bar_x, y, fill_w, height, color)
        
        # Bordo
        self.renderer.draw_rect(bar_x, y, bar_width, height, Color.WHITE, filled=False)
        
        # Valore numerico
        self.renderer.draw_text(str(value), bar_x + bar_width + 10, y, Color.WHITE, "small")

    def _draw_player_panel(self, character: Character, x: int, y: int, 
                          is_active: bool = False):
        """
        Disegna il pannello di un giocatore
        
        Args:
            character: Personaggio da disegnare
            x: Posizione X
            y: Posizione Y
            is_active: Se True, evidenzia il pannello
        """
        # Bordo pannello
        panel_width = 300
        panel_height = 250
        
        border_color = Color.YELLOW if is_active else Color.WHITE
        self.renderer.draw_rect(x, y, panel_width, panel_height, border_color, filled=False)
        
        # Nome e classe
        class_name = Character.CLASSES.get(character.character_class, {}).get('name', 
                                                                              character.character_class.title())
        self.renderer.draw_text(character.name, x + 150, y + 20, 
                               Color.WHITE, "medium", centered=True)
        self.renderer.draw_text(f"({class_name})", x + 150, y + 45,
                               Color.GRAY, "small", centered=True)
        
        # Stato
        status_text = "VIVO" if character.is_alive else "KO"
        status_color = Color.GREEN if character.is_alive else Color.RED
        self.renderer.draw_text(status_text, x + 150, y + 70,
                               status_color, "small", centered=True)
        
        # Barra HP
        self.renderer.draw_text("HP:", x + 10, y + 100, Color.WHITE, "small")
        self.renderer.draw_hp_bar(x + 50, y + 100, 230, 30, 
                                 character.hp, character.max_hp)
        
        # Barra MP
        self.renderer.draw_text("MP:", x + 10, y + 140, Color.WHITE, "small")
        self.renderer.draw_mp_bar(x + 50, y + 140, 230, 30,
                                 character.mp, character.max_mp)
        
        # Stats
        self.renderer.draw_text(f"ATK: +{character.atk_bonus}", x + 10, y + 185,
                               Color.ORANGE, "small")
        self.renderer.draw_text(f"MAG: +{character.mag_bonus}", x + 150, y + 185,
                               Color.PURPLE, "small")
        
        # Bonus visivo se turno attivo
        if is_active:
            self.renderer.draw_text("► TURNO ATTIVO ◄", x + 150, y + 220,
                                   Color.YELLOW, "small", centered=True)
    
    def _draw_enemy_panel(self, enemy: Enemy, x: int, y: int):
        """Disegna il pannello del nemico"""
        panel_width = 400
        
        # Nome nemico
        enemy_name = enemy.get_display_name()
        self.renderer.draw_text(enemy_name, x, y, Color.RED, "medium", centered=True)
        
        # Barra HP nemico
        self.renderer.draw_hp_bar(x - 200, y + 30, panel_width, 40,
                                 enemy.hp, enemy.max_hp, Color.RED)
        
        # Stato
        if not enemy.is_alive:
            self.renderer.draw_text("✗ SCONFITTO ✗", x, y + 80,
                                   Color.GRAY, "small", centered=True)
    
    def _draw_combat_instructions(self, x: int, y: int):
        """Disegna le istruzioni di combattimento aggiornate"""
        # Riga 1: Le azioni di combattimento 
        
        self.renderer.draw_text("[1] Attacco  [2] Magia  [3] Cura Self  [4] Cura Party", 
                               x, y - 25, Color.YELLOW, "small", centered=True)
        
        # Riga 2: Istruzioni di sistema 
        self.renderer.draw_text("ESC: Menu", x, y,
                               Color.GRAY, "small", centered=True)
    
    def draw_exploration_ui(self, party: Party, world_name: str, position: Tuple[int, int]):
        """
        Disegna l'UI di esplorazione
        
        Args:
            party: Party dei giocatori
            world_name: Nome del dungeon
            position: Posizione corrente (x, y)
        """
        width = self.renderer.width
        
        # Titolo e posizione
        self.renderer.draw_text(f"Dungeon: {world_name}", 10, 10, Color.WHITE, "small")
        self.renderer.draw_text(f"Posizione: ({position[0]}, {position[1]})", 
                               10, 35, Color.GRAY, "small")
        
        # Party status 
        self._draw_party_status_compact(width - 320, 10, party)
    
    def _draw_party_status_compact(self, x: int, y: int, party: Party):
        """Disegna lo stato del party in formato compatto"""
        self.renderer.draw_text("PARTY:", x, y, Color.WHITE, "small")
        
        offset_y = 25
        for i, char in enumerate(party.characters):
            char_y = y + offset_y + (i * 60)
            
            # Nome
            self.renderer.draw_text(char.name, x, char_y, Color.WHITE, "small")
            
            # HP Bar 
            self.renderer.draw_hp_bar(x, char_y + 20, 200, 15, char.hp, char.max_hp)
            
            # MP Bar 
            self.renderer.draw_mp_bar(x, char_y + 37, 200, 12, char.mp, char.max_mp)
    
    def draw_menu(self, title: str, options: List[str], selected: int = 0):
        """
        Disegna un menu
        
        Args:
            title: Titolo del menu
            options: Lista di opzioni
            selected: Indice opzione selezionata
        """
        width = self.renderer.width
        height = self.renderer.height
        
        # Background 
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(200)
        overlay.fill(Color.BLACK)
        self.renderer.screen.blit(overlay, (0, 0))
        
        # Titolo
        self.renderer.draw_text(title, width // 2, 100, Color.YELLOW, "large", centered=True)
        
        # Opzioni
        start_y = 200
        spacing = 50
        
        for i, option in enumerate(options):
            y = start_y + (i * spacing)
            color = Color.YELLOW if i == selected else Color.WHITE
            prefix = "► " if i == selected else "  "
            
            self.renderer.draw_text(f"{prefix}{option}", width // 2, y, 
                                   color, "medium", centered=True)
    
    def draw_message_box(self, message: str, x: int = None, y: int = None,
                        width: int = 600, height: int = 100):
        """
        Disegna un box con un messaggio
        
        Args:
            message: Messaggio da mostrare
            x, y: Posizione (se None, centra)
            width, height: Dimensioni del box
        """
        screen_width = self.renderer.width
        screen_height = self.renderer.height
        
        if x is None:
            x = (screen_width - width) // 2
        if y is None:
            y = screen_height - height - 20
        
        # Background box
        self.renderer.draw_rect(x, y, width, height, Color.DARK_GRAY)
        self.renderer.draw_rect(x, y, width, height, Color.WHITE, filled=False)
        
        # Messaggio 
        lines = message.split('\n')
        line_height = 25
        start_y = y + (height - len(lines) * line_height) // 2
        
        for i, line in enumerate(lines):
            self.renderer.draw_text(line, x + width // 2, start_y + i * line_height,
                                   Color.WHITE, "small", centered=True)
    
    def draw_inventory_ui(self, inventory, selected_index: int = 0):
        """
        Disegna l'inventario in stile RPG (Lista a sinistra, Dettagli a destra)
        """
        width = self.renderer.width
        height = self.renderer.height
        items = list(inventory.items.values())
        
        # 1. SFONDO
        self.renderer.clear((15, 15, 20)) 
        
        # Titolo
        self.renderer.draw_text("INVENTARIO", width // 2, 40, Color.YELLOW, "large", centered=True)
        pygame.draw.line(self.renderer.screen, Color.GRAY, (50, 70), (width-50, 70), 1)

        
        if not items:
            self.renderer.draw_text("Il tuo zaino è vuoto.", width // 2, height // 2, Color.GRAY, "medium", centered=True)
            self.renderer.draw_text("ESC: Torna al gioco", width // 2, height - 50, Color.WHITE, "small", centered=True)
            return

        
        margin = 50
        list_width = 400
        details_x = margin + list_width + 40
        details_width = width - details_x - margin
        start_y = 100
        
        
        pygame.draw.rect(self.renderer.screen, (25, 25, 35), (margin - 10, start_y - 10, list_width + 20, height - 200))
        pygame.draw.rect(self.renderer.screen, (60, 60, 80), (margin - 10, start_y - 10, list_width + 20, height - 200), 1)
        
        for i, item in enumerate(items):
            item_y = start_y + (i * 50)
            
            
            if i == selected_index:
                # Sfondo giallo trasparente 
                pygame.draw.rect(self.renderer.screen, (50, 50, 100), (margin, item_y, list_width, 40))
                pygame.draw.rect(self.renderer.screen, Color.YELLOW, (margin, item_y, list_width, 40), 2)
                text_color = Color.YELLOW
                prefix = "► "
            else:
                text_color = Color.WHITE
                prefix = "  "
            
            # Nome oggetto e quantità
            self.renderer.draw_text(f"{prefix}{item.name}", margin + 10, item_y + 10, text_color, "medium")
            self.renderer.draw_text(f"x{item.quantity}", margin + list_width - 50, item_y + 10, Color.GRAY, "medium")

        
        selected_item = items[selected_index]
        
        # Box Dettagli
        pygame.draw.rect(self.renderer.screen, (30, 30, 40), (details_x, start_y, details_width, 300))
        pygame.draw.rect(self.renderer.screen, Color.WHITE, (details_x, start_y, details_width, 300), 2)
        
        
        icon_size = 80
        icon_x = details_x + 30
        icon_y = start_y + 30
        
        
        name_lower = selected_item.name.lower()
        
        if "vita" in name_lower or "health" in name_lower:
            icon_color = (200, 50, 50) 
            symbol = "HP"
        elif "mana" in name_lower:
            icon_color = (50, 50, 200) 
            symbol = "MP"
        else:
            icon_color = (150, 150, 150) 
            symbol = "?"
            
        pygame.draw.rect(self.renderer.screen, icon_color, (icon_x, icon_y, icon_size, icon_size))
        pygame.draw.rect(self.renderer.screen, Color.WHITE, (icon_x, icon_y, icon_size, icon_size), 2)
        self.renderer.draw_text(symbol, icon_x + 25, icon_y + 30, Color.WHITE, "medium")
        
        
        self.renderer.draw_text(selected_item.name, icon_x + 100, icon_y + 10, Color.YELLOW, "large")
        self.renderer.draw_text("Oggetto Consumabile", icon_x + 100, icon_y + 50, Color.GRAY, "small")
        
        
        pygame.draw.line(self.renderer.screen, Color.GRAY, (details_x + 20, start_y + 140), (details_x + details_width - 20, start_y + 140), 1)
        
        # Descrizione
        desc_y = start_y + 160
        # Splitto la descrizione se è troppo lunga 
        words = selected_item.description.split()
        line = ""
        for word in words:
            if len(line) + len(word) > 35: # Lunghezza max riga
                self.renderer.draw_text(line, details_x + 30, desc_y, Color.WHITE, "medium")
                desc_y += 30
                line = ""
            line += word + " "
        self.renderer.draw_text(line, details_x + 30, desc_y, Color.WHITE, "medium")
        
        # 4. FOOTER COMANDI
        self.renderer.draw_text("INVIO: Usa Oggetto  |  ESC: Chiudi", width // 2, height - 50, Color.GREEN, "small", centered=True)

        