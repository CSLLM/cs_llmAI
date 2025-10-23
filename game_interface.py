"""
Game Interface Module
Handles screen capture, game state detection, and action execution
"""

import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import keyboard
import time

class GameInterface:
    """Interface between AI and CS:GO"""
    
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.stats = {
            'kills': 0,
            'deaths': 0,
            'score': 0,
            'headshots': 0
        }
        
    def get_state(self):
        """Capture and analyze current game state"""
        screen = self._capture_screen()
        
        state = {
            'timestamp': time.time(),
            'screen': screen,
            'enemy_detected': False,
            'enemy_x': 0,
            'enemy_y': 0,
            'enemy_distance': 0,
            'player_health': self._detect_health(screen),
            'ammo': self._detect_ammo(screen),
            'cover_nearby': self._detect_cover(screen),
            'recent_kill_rate': self._calculate_kill_rate()
        }
        
        # Enemy detection
        enemy_data = self._detect_enemy(screen)
        if enemy_data['detected']:
            state.update(enemy_data)
        
        return state
    
    def _capture_screen(self):
        """Capture game screen"""
        screenshot = ImageGrab.grab(bbox=(0, 0, self.screen_width, self.screen_height))
        return np.array(screenshot)
    
    def _detect_enemy(self, screen):
        """Detect enemy players using computer vision"""
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(screen, cv2.COLOR_RGB2HSV)
        
        # Define color range for enemy models (red tones)
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest contour (closest enemy)
            largest = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest) > 500:  # Minimum size threshold
                x, y, w, h = cv2.boundingRect(largest)
                
                return {
                    'enemy_detected': True,
                    'enemy_x': x + w // 2,
                    'enemy_y': y + h // 2,
                    'enemy_distance': self._estimate_distance(w, h),
                    'enemy_velocity': self._estimate_velocity(x, y)
                }
        
        return {'enemy_detected': False}
    
    def _estimate_distance(self, width, height):
        """Estimate distance based on bounding box size"""
        size = width * height
        # Inverse relationship: larger size = closer enemy
        return max(5, min(100, 15000 / max(size, 100)))
    
    def _estimate_velocity(self, x, y):
        """Estimate enemy movement velocity"""
        # Simplified: would track position over frames
        return (random.randint(-5, 5), random.randint(-5, 5))
    
    def _detect_health(self, screen):
        """Detect player health from HUD"""
        # Health is typically shown in bottom-left
        health_region = screen[980:1020, 100:200]
        
        # OCR or color analysis would go here
        # For demo, return random value
        return random.randint(50, 100)
    
    def _detect_ammo(self, screen):
        """Detect remaining ammunition"""
        # Ammo shown in bottom-right
        return {'clip': random.randint(10, 30), 'reserve': random.randint(60, 90)}
    
    def _detect_cover(self, screen):
        """Detect if cover is nearby"""
        # Analyze edges and shapes for cover
        return random.choice([True, False])
    
    def _calculate_kill_rate(self):
        """Calculate recent kill success rate"""
        if self.stats['kills'] + self.stats['deaths'] == 0:
            return 0.5
        return self.stats['kills'] / (self.stats['kills'] + self.stats['deaths'])
    
    def execute_action(self, action):
        """Execute AI action in game"""
        action_type = action.get('action')
        
        # Action mapping
        if action_type == 'attack':
            pass  # Already executed in AI controller
        elif action_type == 'retreat':
            direction = action.get('direction', 's')
            keyboard.press(direction)
            time.sleep(0.3)
            keyboard.release(direction)
        elif action_type == 'patrol':
            self._patrol_movement()
        elif action_type == 'reload':
            keyboard.press('r')
            time.sleep(0.1)
            keyboard.release('r')
    
    def _patrol_movement(self):
        """Execute patrol movement pattern"""
        movements = ['w', 'a', 'd']
        move = random.choice(movements)
        keyboard.press(move)
        time.sleep(random.uniform(0.2, 0.5))
        keyboard.release(move)
    
    def get_stats(self):
        """Return current match statistics"""
        return self.stats.copy()
    
    def reset(self):
        """Reset stats for new match"""
        self.stats = {
            'kills': 0,
            'deaths': 0,
            'score': 0,
            'headshots': 0
        }
