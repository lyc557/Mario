import json
import os

class SaveSystem:
    def __init__(self):
        self.save_file = "save_data.json"
        
    def save_game(self, game):
        save_data = {
            'current_level': game.current_level,
            'lives': game.mario.lives,
            'game_won': game.game_won,
            'game_over': game.game_over
        }
        try:
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f)
            return True
        except:
            return False
            
    def load_game(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return None
        
    def delete_save(self):
        if os.path.exists(self.save_file):
            try:
                os.remove(self.save_file)
                return True
            except:
                pass
        return False 