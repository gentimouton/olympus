from scene import SCN_MENU, SCN_GAME, SCN_QUIT
from menu_scene import MenuScene
from game_scene import GameScene


class SceneManager():
    def __init__(self, scenes, first_scene_id):
        self.scenes = scenes
        self.cur_scene = self.scenes[first_scene_id]

    def tick(self, ms):
        """ update current scene """
        next_scene_id, kwargs = self.cur_scene.tick(ms)
        if next_scene_id == SCN_QUIT: # quit via dummy scene constant
            return True
        elif next_scene_id is not None: # change scene
            self.cur_scene.pause()
            self.cur_scene = self.scenes[next_scene_id]
            self.cur_scene.reset_resume(**kwargs)


scene_manager = SceneManager({ SCN_MENU: MenuScene(), SCN_GAME: GameScene() },
                             SCN_MENU)
