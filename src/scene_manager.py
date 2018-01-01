from constants import OUT_NONE, OUT_QUIT
from game_scene import GameScene
from menu_scene import MenuScene
from scene import SCN_MENU, SCN_GAME, SCN_QUIT, SCN_OVER
from game_over_scene import GameOverScene

scene_manager = None

class SceneManager():
    def __init__(self, scenes, first_scene_id):
        self.scenes = scenes
        self.cur_scene = self.scenes[first_scene_id]

    def tick(self, ms):
        """ update current scene. Return an outcome (eg quit game). """
        next_scene_id, kwargs = self.cur_scene.tick(ms)
        if next_scene_id == SCN_QUIT:  # quit via dummy scene constant
            return OUT_QUIT
        elif next_scene_id is not None:  # change scene
            self.cur_scene.pause()
            self.cur_scene = self.scenes[next_scene_id]
            self.cur_scene.resume(**kwargs)
        return OUT_NONE
    
    def redraw(self):
        """ controls switched to full screen, so redraw scene from scratch """
        self.cur_scene.redraw()

def init():
    """ needed because Scenes need pygame to be initialized 
    before they are created """
    global scene_manager
    scenes = { 
        SCN_MENU: MenuScene(), 
        SCN_GAME: GameScene(),
        SCN_OVER: GameOverScene() 
        }
    scene_manager = SceneManager(scenes, SCN_MENU)
