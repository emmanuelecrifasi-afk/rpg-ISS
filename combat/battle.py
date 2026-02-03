"""
Battle System - Gestisce l'intero flusso di combattimento
"""

import random
from typing import List, Optional, Tuple
from models.party import Party
from models.character import Character
from combat.enemy import Enemy
from combat.turn_manager import TurnManager, Combatant


class BattleResult:
    """Risultato di una battaglia"""
    
    def __init__(self, victory: bool, survivors: List[Character], 
                 enemy_defeated: bool, rounds: int):
        """
        Inizializza il risultato
        
        Args:
            victory: True se i giocatori hanno vinto
            survivors: Lista dei personaggi sopravvissuti
            enemy_defeated: True se il nemico è stato sconfitto
            rounds: Numero di round della battaglia
        """
        self.victory = victory
        self.survivors = survivors
        self.enemy_defeated = enemy_defeated
        self.rounds = rounds
        self.game_over = len(survivors) == 0


class BattleAction:
    """Rappresenta un'azione di battaglia"""
    
    def __init__(self, action_type: str, actor: str, target: str, 
                 value: int, message: str):
        """
        Inizializza un'azione
        
        Args:
            action_type: Tipo di azione (attack, heal, defend)
            actor: Nome di chi esegue l'azione
            target: Nome del bersaglio
            value: Valore (danno o cura)
            message: Messaggio descrittivo
        """
        self.action_type = action_type
        self.actor = actor
        self.target = target
        self.value = value
        self.message = message


class Battle:
    """Classe principale per gestire un combattimento"""
    
    def __init__(self, party: Party, enemy: Enemy):
        """
        Inizializza una battaglia
        
        Args:
            party: Party dei giocatori
            enemy: Nemico da affrontare
        """
        self.party = party
        self.enemy = enemy
        self.turn_manager = TurnManager(party.characters, enemy)
        self.battle_log: List[BattleAction] = []
        self.is_active = False
    
    def start_battle(self) -> str:
        """
        Inizia la battaglia
        
        Returns:
            Messaggio di inizio battaglia
        """
        self.is_active = True
        return self._get_battle_intro()
    
    def _get_battle_intro(self) -> str:
        """Genera il messaggio di introduzione"""
        lines = []
        lines.append("=" * 50)
        lines.append("⚔️  INIZIO COMBATTIMENTO!")
        lines.append("=" * 50)
        lines.append(f"\n{self.enemy.description}")
        lines.append(f"\n{self.enemy}")
        lines.append("\nIl tuo party:")
        for char in self.party.characters:
            lines.append(f"  • {char}")
        lines.append("\n" + "=" * 50)
        return "\n".join(lines)
    
    def execute_player_turn(self, player: Character, action: str, 
                           target: Optional[Character] = None, item_id: Optional[str] = None) -> BattleAction:
        """
        Esegue il turno di un giocatore
        
        Args:
            player: Personaggio che agisce
            action: Azione da eseguire (attack, heal, use_item, magic)
            target: Bersaglio (per heal o item)
            item_id: ID dell'oggetto da usare (per use_item)
            
        Returns:
            BattleAction eseguita
        """
        if action == "attack":
            return self._execute_attack(player, self.enemy)
        elif action == "magic":
            return self._execute_magic_attack(player, self.enemy)
        elif action == "heal":
            if target and target.is_alive:
                return self._execute_heal(player, target)
            else:
                # Auto-heal se nessun target specificato
                return self._execute_heal(player, player)
        elif action == "use_item":
            if item_id:
                return self._execute_use_item(player, item_id, target)
            else:
                return BattleAction(
                    action_type="skip",
                    actor=player.name,
                    target="",
                    value=0,
                    message="Nessun oggetto specificato"
                )
        
        # Azione non valida, passa il turno
        return BattleAction(
            action_type="skip",
            actor=player.name,
            target="",
            value=0,
            message=f"{player.name} passa il turno"
        )
    
    def execute_enemy_turn(self) -> BattleAction:
        """
        Esegue il turno del nemico (IA base)
        
        Returns:
            BattleAction eseguita
        """
        # IA: Sceglie casualmente un giocatore vivo da attaccare
        alive_players = self.turn_manager.get_alive_players()
        
        if not alive_players:
            return BattleAction(
                action_type="skip",
                actor=self.enemy.name,
                target="",
                value=0,
                message=f"{self.enemy.name} non ha bersagli validi"
            )
        
        # Scelta casuale del bersaglio
        target = random.choice(alive_players)
        
        return self._execute_attack(self.enemy, target)
    
    def _execute_attack(self, attacker, target) -> BattleAction:
        """Esegue un attacco"""
        # Calcola danno
        if isinstance(attacker, Enemy):
            damage = attacker.attack()
        else:
            # Usa il danno fisico con bonus ATK
            damage = attacker.calculate_physical_damage()
        
        # Infliggi danno
        actual_damage = target.take_damage(damage)
        
        # Crea messaggio
        message = f"⚔️  {attacker.name} attacca {target.name} per {actual_damage} danni!"
        
        if not target.is_alive:
            message += f"\n💀 {target.name} è stato sconfitto!"
        
        action = BattleAction(
            action_type="attack",
            actor=attacker.name,
            target=target.name,
            value=actual_damage,
            message=message
        )
        
        self.battle_log.append(action)
        return action
    
    def _execute_use_item(self, user: Character, item_id: str, target: Optional[Character] = None) -> BattleAction:
        """Esegue l'uso di un oggetto"""
        from models.item import ItemEffect
        
        # Usa l'oggetto dall'inventario del party
        result = self.party.inventory.use_item(item_id, target)
        
        if not result['success']:
            return BattleAction(
                action_type="skip",
                actor=user.name,
                target="",
                value=0,
                message=result['message']
            )
        
        # Applica l'effetto
        effect = result['effect']
        value = result['value']
        actual_value = 0
        target_name = target.name if target else user.name
        final_target = target if target else user
        
        if effect == ItemEffect.HEAL:
            actual_value = final_target.heal(value)
            message = f"💚 {user.name} usa {self.party.inventory.items.get(item_id, type('obj', (), {'name': 'oggetto'})).name if item_id in self.party.inventory.items else 'un oggetto'} su {target_name}: +{actual_value} HP!"
        elif effect == ItemEffect.RESTORE_MP:
            actual_value = final_target.restore_mp(value)
            message = f"💙 {user.name} usa un oggetto su {target_name}: +{actual_value} MP!"
        elif effect == ItemEffect.DAMAGE:
            actual_value = self.enemy.take_damage(value)
            target_name = self.enemy.name
            message = f"💣 {user.name} usa un oggetto su {target_name}: {actual_value} danni!"
            
            if not self.enemy.is_alive:
                message += f"\n💀 {self.enemy.name} è stato sconfitto!"
        else:
            message = result['message']
        
        action = BattleAction(
            action_type="use_item",
            actor=user.name,
            target=target_name,
            value=actual_value,
            message=message
        )
        
        self.battle_log.append(action)
        return action
    
    def _execute_magic_attack(self, attacker: Character, target) -> BattleAction:
        """Esegue un attacco magico"""
        mp_cost = 10
        
        # Controlla se ha abbastanza MP
        if not attacker.use_mp(mp_cost):
            return BattleAction(
                action_type="skip",
                actor=attacker.name,
                target="",
                value=0,
                message=f"{attacker.name} non ha abbastanza MP!"
            )
        
        # Calcola danno magico con bonus MAG
        damage = attacker.calculate_magic_damage()
        
        # Infliggi danno
        actual_damage = target.take_damage(damage)
        
        # Crea messaggio
        message = f"✨ {attacker.name} lancia un incantesimo su {target.name} per {actual_damage} danni! (-{mp_cost} MP)"
        
        if not target.is_alive:
            message += f"\n💀 {target.name} è stato sconfitto!"
        
        action = BattleAction(
            action_type="magic",
            actor=attacker.name,
            target=target.name,
            value=actual_damage,
            message=message
        )
        
        self.battle_log.append(action)
        return action
    
    def _execute_heal(self, healer: Character, target: Character) -> BattleAction:
        """Esegue una cura"""
        heal_amount = random.randint(15, 30)
        actual_heal = target.heal(heal_amount)
        
        message = f"💚 {healer.name} cura {target.name} di {actual_heal} HP!"
        
        action = BattleAction(
            action_type="heal",
            actor=healer.name,
            target=target.name,
            value=actual_heal,
            message=message
        )
        
        self.battle_log.append(action)
        return action
    
    def check_battle_end(self) -> Optional[BattleResult]:
        """
        Controlla se la battaglia è finita
        
        Returns:
            BattleResult se finita, None altrimenti
        """
        if not self.turn_manager.is_battle_active():
            self.is_active = False
            
            survivors = self.turn_manager.get_alive_players()
            victory = self.enemy.is_alive == False
            
            self.end_battle(victory)

            return BattleResult(
                victory=victory,
                survivors=survivors,
                enemy_defeated=not self.enemy.is_alive,
                rounds=self.turn_manager.round_number
            )
        
        return None
    
    def get_current_state(self) -> dict:
        """Ottiene lo stato corrente della battaglia"""
        return {
            'round': self.turn_manager.round_number,
            'enemy': {
                'name': self.enemy.get_display_name(),
                'hp': self.enemy.hp,
                'max_hp': self.enemy.max_hp,
                'alive': self.enemy.is_alive
            },
            'players': [
                {
                    'name': char.name,
                    'hp': char.hp,
                    'max_hp': char.max_hp,
                    'alive': char.is_alive
                }
                for char in self.party.characters
            ],
            'active': self.is_active
        }
    
    def get_battle_summary(self) -> str:
        """Genera un riepilogo della battaglia"""
        lines = []
        lines.append("\n" + "=" * 50)
        lines.append("📊 RIEPILOGO BATTAGLIA")
        lines.append("=" * 50)
        lines.append(f"Round totali: {self.turn_manager.round_number}")
        lines.append(f"Azioni totali: {len(self.battle_log)}")
        
        result = self.check_battle_end()
        if result:
            if result.victory:
                lines.append("\n🎉 VITTORIA!")
            else:
                lines.append("\n💀 SCONFITTA!")
            
            lines.append(f"\nSopravvissuti: {len(result.survivors)}/{len(self.party.characters)}")
        
        lines.append("=" * 50)
        return "\n".join(lines)
    
    def __str__(self) -> str:
        status = "IN CORSO" if self.is_active else "TERMINATA"
        return f"Battle(Round {self.turn_manager.round_number}, Status: {status})"
    
    def end_battle(self, victory: bool):
        """Gestisce la fine della battaglia e i premi"""
        if victory:
            
            for member in self.party.characters:
                
                if member.is_alive:  
                    if hasattr(member, 'apply_victory_bonus'):
                        member.apply_victory_bonus()
 
            
        else:
            print("\n--- GAME OVER ---")
            