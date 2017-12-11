from scene import SCN_1, SCN_2
from scene_1 import Scene1
from scene_2 import Scene2


class SceneManager():
    def __init__(self, scenes, first_scene_id):
        self.scenes = scenes
        self.cur_scene = self.scenes[first_scene_id]

    def tick(self, ms):
        """ update current scene """
        next_scene_id, kwargs = self.cur_scene.tick(ms)
        if next_scene_id:
            self.cur_scene.pause()
            self.cur_scene = self.scenes[next_scene_id]
            self.cur_scene.reset_resume(**kwargs)


scene_manager = SceneManager({ SCN_1: Scene1(), SCN_2: Scene2() }, SCN_1)