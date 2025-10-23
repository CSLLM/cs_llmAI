"""
AI CS:GO Battle Simulator
Main entry point for running AI matches
"""

import argparse
import time
from ai_controller import ClaudeAI, ChatGPTAI, GeminiAI, GrokAI
from game_interface import GameInterface
from match_logger import MatchLogger

def main():
    parser = argparse.ArgumentParser(description='AI CS:GO Battle Simulator')
    parser.add_argument('--model', type=str, required=True, 
                       choices=['claude', 'chatgpt', 'gemini', 'grok', 'all'],
                       help='AI model to use')
    parser.add_argument('--match-duration', type=int, default=600,
                       help='Match duration in seconds')
    parser.add_argument('--difficulty', type=str, default='medium',
                       choices=['easy', 'medium', 'hard'],
                       help='Game difficulty level')
    
    args = parser.parse_args()
    
    # Initialize game interface
    game = GameInterface()
    logger = MatchLogger()
    
    print("🎮 AI CS:GO Battle Simulator")
    print("=" * 50)
    
    # Select AI model
    ai_models = {
        'claude': ClaudeAI(difficulty=args.difficulty),
        'chatgpt': ChatGPTAI(difficulty=args.difficulty),
        'gemini': GeminiAI(difficulty=args.difficulty),
        'grok': GrokAI(difficulty=args.difficulty)
    }
    
    if args.model == 'all':
        print("🤖 Starting tournament with all AI models...")
        run_tournament(ai_models, game, logger, args.match_duration)
    else:
        print(f"🤖 Loading {args.model.upper()} AI...")
        ai = ai_models[args.model]
        run_single_match(ai, game, logger, args.match_duration)
    
    print("\n✅ Match completed! Check logs for details.")

def run_single_match(ai, game, logger, duration):
    """Run a single match with one AI"""
    print(f"\n▶️  Match started - Duration: {duration}s")
    
    start_time = time.time()
    frame_count = 0
    
    try:
        while time.time() - start_time < duration:
            # Capture game state
            game_state = game.get_state()
            
            # AI makes decision
            action = ai.decide_action(game_state)
            
            # Execute action
            game.execute_action(action)
            
            # Log stats every 5 seconds
            if frame_count % 150 == 0:
                stats = game.get_stats()
                logger.log_stats(ai.name, stats)
                print(f"⏱️  {int(time.time() - start_time)}s | K: {stats['kills']} | D: {stats['deaths']} | Score: {stats['score']}")
            
            frame_count += 1
            time.sleep(0.033)  # ~30 FPS
            
    except KeyboardInterrupt:
        print("\n⚠️  Match interrupted by user")
    
    final_stats = game.get_stats()
    logger.save_match_report(ai.name, final_stats)

def run_tournament(ai_models, game, logger, duration):
    """Run tournament with all AI models"""
    results = {}
    
    for name, ai in ai_models.items():
        print(f"\n{'='*50}")
        print(f"🎯 {name.upper()} is now playing...")
        print(f"{'='*50}")
        
        game.reset()
        run_single_match(ai, game, logger, duration)
        results[name] = game.get_stats()
        
        time.sleep(5)  # Cooldown between matches
    
    # Display final rankings
    print("\n" + "="*50)
    print("🏆 FINAL RANKINGS")
    print("="*50)
    
    sorted_results = sorted(results.items(), 
                           key=lambda x: x[1]['score'], 
                           reverse=True)
    
    for rank, (name, stats) in enumerate(sorted_results, 1):
        print(f"{rank}. {name.upper():10} | Score: {stats['score']:4} | K/D: {stats['kills']}/{stats['deaths']}")

if __name__ == "__main__":
    main()
