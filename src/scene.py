
SCN_MENU = 'menu'
SCN_GAME = 'game'
SCN_QUIT = 'quit' # dummy scene, enables quitting the game within a scene

class Scene():
    
    def tick(self, ms):
        pass
    def pause(self):
        pass
    def reset_resume(self, **kwargs):
        pass
    