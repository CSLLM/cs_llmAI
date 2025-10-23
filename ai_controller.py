"""
AI Controller Classes
Each AI model has its own decision-making logic
"""

import pyautogui
import keyboard
import random
import time
from abc import ABC, abstractmethod

class BaseAI(ABC):
    """Base class for all AI controllers"""
    
    def __init__(self, name, difficulty='medium'):
        self.name = name
        self.difficulty = difficulty
        self.reaction_time = self._set_reaction_time()
        self.accuracy = self._set_accuracy()
        
    def _set_reaction_time(self):
        """Set reaction time based on difficulty"""
        times = {
            'easy': random.uniform(0.3, 0.5),
            'medium': random.uniform(0.15, 0.25),
            'hard': random.uniform(0.08, 0.15)
        }
        return times.get(self.difficulty, 0.2)
    
    def _set_accuracy(self):
        """Set accuracy based on difficulty"""
        accuracy = {
            'easy': 0.4,
            'medium': 0.6,
            'hard': 0.85
        }
        return accuracy.get(self.difficulty, 0.6)
    
    @abstractmethod
    def decide_action(self, game_state):
        """Each AI implements its own decision logic"""
        pass
    
    def aim_at(self, x, y):
        """Aim at specific coordinates with AI-specific accuracy"""
        time.sleep(self.reaction_time)
        
        # Add accuracy variance
        offset_x = random.randint(-int(50 * (1 - self.accuracy)), 
                                  int(50 * (1 - self.accuracy)))
        offset_y = random.randint(-int(50 * (1 - self.accuracy)), 
                                  int(50 * (1 - self.accuracy)))
        
        pyautogui.moveTo(x + offset_x, y + offset_y, duration=0.1)
    
    def shoot(self, burst=3):
        """Fire weapon"""
        for _ in range(burst):
            pyautogui.click()
            time.sleep(0.1)


class ClaudeAI(BaseAI):
    """Claude - Analytical and tactical player"""
    
    def __init__(self, difficulty='medium'):
        super().__init__('Claude', difficulty)
        self.strategy = 'defensive'
        
    def decide_action(self, game_state):
        """Claude's decision logic: careful and analytical"""
        
        if game_state['enemy_detected']:
            # Analyze threat level
            distance = game_state['enemy_distance']
            health = game_state['player_health']
            
            if health < 30:
                # Retreat and find cover
                return {'action': 'retreat', 'direction': 's'}
            
            elif distance < 15:
                # Close combat - crouch and spray
                keyboard.press('ctrl')
                self.aim_at(game_state['enemy_x'], game_state['enemy_y'])
                self.shoot(burst=5)
                keyboard.release('ctrl')
                return {'action': 'attack', 'type': 'spray'}
            
            else:
                # Long range - tap shooting
                self.aim_at(game_state['enemy_x'], game_state['enemy_y'] - 60)
                self.shoot(burst=2)
                return {'action': 'attack', 'type': 'tap'}
        
        else:
            # Patrol mode - check corners carefully
            return {'action': 'patrol', 'pattern': 'methodical'}


class ChatGPTAI(BaseAI):
    """ChatGPT - Balanced and adaptive player"""
    
    def __init__(self, difficulty='medium'):
        super().__init__('ChatGPT', difficulty)
        self.learning_rate = 0.1
        
    def decide_action(self, game_state):
        """ChatGPT's decision logic: adaptive and balanced"""
        
        if game_state['enemy_detected']:
            # Adaptive strategy based on previous encounters
            success_rate = game_state.get('recent_kill_rate', 0.5)
            
            if success_rate > 0.6:
                # Aggressive approach
                keyboard.press('w')
                time.sleep(0.2)
                keyboard.release('w')
                self.aim_at(game_state['enemy_x'], game_state['enemy_y'])
                self.shoot(burst=4)
                return {'action': 'aggressive_push'}
            
            else:
                # Defensive approach
                keyboard.press('a')
                time.sleep(0.15)
                keyboard.release('a')
                self.aim_at(game_state['enemy_x'], game_state['enemy_y'])
                self.shoot(burst=3)
                return {'action': 'defensive_strafe'}
        
        else:
            return {'action': 'explore', 'speed': 'moderate'}


class GeminiAI(BaseAI):
    """Gemini - Intelligent and strategic player"""
    
    def __init__(self, difficulty='medium'):
        super().__init__('Gemini', difficulty)
        self.position_memory = []
        
    def decide_action(self, game_state):
        """Gemini's decision logic: intelligent positioning"""
        
        if game_state['enemy_detected']:
            # Smart positioning before engaging
            cover_available = game_state.get('cover_nearby', False)
            
            if cover_available and game_state['player_health'] < 50:
                # Use cover strategically
                keyboard.press('shift')  # Walk
                keyboard.press('d')
                time.sleep(0.3)
                keyboard.release('d')
                keyboard.release('shift')
            
            # Precise aim with prediction
            enemy_velocity = game_state.get('enemy_velocity', (0, 0))
            predicted_x = game_state['enemy_x'] + enemy_velocity[0] * 0.2
            predicted_y = game_state['enemy_y'] + enemy_velocity[1] * 0.2
            
            self.aim_at(predicted_x, predicted_y)
            self.shoot(burst=3)
            
            return {'action': 'tactical_engagement'}
        
        else:
            return {'action': 'rotate', 'strategy': 'map_control'}


class GrokAI(BaseAI):
    """Grok - Aggressive and fast-paced player"""
    
    def __init__(self, difficulty='medium'):
        super().__init__('Grok', difficulty)
        self.aggression = 0.8
        
    def decide_action(self, game_state):
        """Grok's decision logic: fast and aggressive"""
        
        if game_state['enemy_detected']:
            # Immediate aggressive response
            # Rush forward
            keyboard.press('shift')  # Unshift for speed
            keyboard.press('w')
            time.sleep(0.15)
            keyboard.release('w')
            keyboard.release('shift')
            
            # Quick flick shot
            self.aim_at(game_state['enemy_x'], game_state['enemy_y'])
            
            # Burst fire while moving
            keyboard.press('a')
            self.shoot(burst=6)
            keyboard.release('a')
            
            return {'action': 'rush', 'aggression_level': 'high'}
        
        else:
            # Aggressive rotation
            keyboard.press('w')
            time.sleep(0.4)
            keyboard.release('w')
            return {'action': 'aggressive_push', 'speed': 'fast'}
