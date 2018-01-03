from collections import deque


# encounter_gfx kinds
ENC_DFLT = 'default'

# encounter_gfx effects 
def _mana_increase(x):
    def f(state):
        state.increase_mana(x)
    return f 
def _add_encounter(kind=ENC_DFLT, n=1):
    def f(state):
        for _ in range(n):
            state.append_encounter(kind)
    return f

# encounter_gfx data
encounter_data = {
    ENC_DFLT: {
        'bgcolor': (55,111,55),
        'mid': {
            'txt': 'A Sphinx looks at you....\nWhat do you do?',
            'bgcolor': (222, 55, 11),
            },
        'left': {
            'txt': 'Say Hi!\n+10 mana',
            'bgcolor': (55, 111, 111),
            'effects': [_mana_increase(10)]
            },
        'right': {
            'txt': 'nothing',
            'bgcolor': (111, 55, 111),
            'effects': [_add_encounter(ENC_DFLT, n=2), _mana_increase(-5)] 
            }
        }
    }
  
# game states
GST_LOST = 'lost'
GST_LIVE = 'live'
class GameModel():
    """ game state - can save this via pickle """
    def __init__(self):
        self.game_status = GST_LIVE
        self.mana = 10
        self.mana_max = 100
        self.encounters_seen = 0
        self.encounters = deque([ENC_DFLT, ENC_DFLT])
        self.cur_enc = None
        self.next_enc()
        
    def next_enc(self):
        """ pop the next encounter_gfx """
        try:
            self.cur_enc = self.encounters.popleft()
        except IndexError:  # empty: add 2 default ones
            self.encounters.extend([ENC_DFLT, ENC_DFLT])  # TODO: game over instead?
            self.cur_enc = self.encounters.popleft()
        self.encounters_seen += 1
            
    def game_lost(self):
        self.game_status = GST_LOST
    
    # encounter_gfx effects exposed    
    def append_encounter(self, enc_kind):
        self.encounters.append(enc_kind)
    def increase_mana(self, x):
        self.mana = min(self.mana + x, self.mana_max)
        if self.mana <= 0:
            self.game_lost()
    
    # making a choice
    def choose(self, choice):
        """ choice can be 'left' or 'right' """
        for effect_cb in encounter_data[self.cur_enc][choice]['effects']:
            effect_cb(self)  # update state
        self.next_enc()
