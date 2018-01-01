""" Scenes consist of the menu, the game itself, the game-over screen, etc.
"""

SCN_MENU = 'menu'
SCN_GAME = 'game'
SCN_QUIT = 'quit' # dummy scene, enables quitting the game within a scene
SCN_OVER = 'over' # game over scene

class Scene():
    
    def tick(self, ms):
        """ Process player inputs, and display animations.
        Also draw to screen if the scene does not use dirty sprites. 
        ms is the time in milliseconds elapsed since last clock tick.
        Return id of next scene, and args to pass to next scene's resume(). 
        """
        return None, {}
    def pause(self):
        """ Scene is replaced by another one. Cancel ongoing animations. """
        pass
    def resume(self, **kwargs):
        """ Scene is active again. """
        pass
    def redraw(self):
        """ Redraw from scratch when switching from/to fullscreen.
        Recompute background and sprites for scenes using dirty sprites.
        Nothing to do for scenes not using dirty sprites (they draw every tick).
        """
        pass 