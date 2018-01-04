from collections import deque


# encounter kinds
ENC_ATM1 = 'artemis meet'
ENC_ATM2 = 'artemis mad'
ENC_DFLT = 'default'
ENC_FRST = 'forest'
ENC_FBCK = 'fallback'
ENC_SHYD = 'shipyard'
ENC_TUT1 = 'tutorial mana'
ENC_TUT2 = 'tutorial go'
ENC_TUT3 = 'tutorial punish'

# encounter_render effects 
def _mana_increase(x):
    def f(state):
        state.increase_mana(x)
    return f 
def _add_encounter(kind=ENC_DFLT, n=1, immediate=False):
    def f(state):
        for _ in range(n):
            state.append_encounter(kind, immediate)
    return f 
def _lose_game():
    def f(state):
        state.lose_game()
    return f

# encounter_render data 
# TODO: card data is a pain to edit, store in JSON instead? 
encounter_data = {
    ENC_ATM1: {
        'bgcolor': (88, 88, 88),
        'mid': {
            'txt': 'Artemis: Hey I\'m Artemis.\nThanks for growing the forest so I can hunt!',
            'bgcolor': (125, 41, 155),
            },
        'left': {
            'txt': 'Don\'t mention it! Bye!',
            'bgcolor': (88, 111, 111),
            'effects': [_mana_increase(10)]
            },
        'right': {
            'txt': 'It\'ll cost you a favor, like 20 mana please...',
            'bgcolor': (222, 55, 111),
            'effects': [_add_encounter(ENC_ATM2, immediate=True)] 
            }
        },
    ENC_ATM2: {
        'bgcolor': (88, 88, 88),
        'mid': {
            'txt': 'Artemis: I owe you nothing.',
            'bgcolor': (125, 41, 155),
            },
        'left': {
            'txt': 'Alright, whatever.',
            'bgcolor': (111, 111, 111),
            'effects': []
            },
        'right': {
            'txt': 'Then we shall fight.',
            'bgcolor': (222, 55, 55),
            'effects': []  # TODO: add battle with Artemis 
            }
        },
    ENC_DFLT: {
        'bgcolor': (55, 111, 55),
        'mid': {
            'txt': 'Lorem ipsum dolor sit amet\nSupercalifragilisticexpialidocious',
            'bgcolor': (222, 55, 11),
            },
        'left': {
            'txt': 'Say what?\n+10 mana',
            'bgcolor': (55, 111, 111),
            'effects': [_mana_increase(10)]
            },
        'right': {
            'txt': 'Do nothing (-5 mana)',
            'bgcolor': (111, 55, 111),
            'effects': [_add_encounter(ENC_DFLT, n=2), _mana_increase(-5)] 
            }
        },
    ENC_FBCK: {
        'bgcolor': (0, 0, 0),
        'mid': {
            'txt': 'Oops...\nLooks like we run out of encounters :(',
            'bgcolor': (33, 50, 127)
            },
        'left': {
            'txt': 'This must mean game over!',
            'bgcolor': (222, 0, 0),
            'effects': [_lose_game()]
            },
        'right': {
            'txt': 'Add the forest card',
            'bgcolor': (55, 155, 55),
            'effects': [_add_encounter(ENC_FRST), _mana_increase(25)] 
            }
        },
    ENC_FRST: {
        'bgcolor': (0, 55, 0),
        'mid': {
            'txt': 'This forest is suspiciously not growing.',
            'bgcolor': (166, 42, 42)
            },
        'left': {
            'txt': 'Let it be.',
            'bgcolor': (111, 111, 111),
            'effects': [_add_encounter(ENC_SHYD)]
            },
        'right': {
            'txt': 'Cast a spell to make it grow.',
            'bgcolor': (55, 188, 55),
            'effects': [_add_encounter(ENC_ATM1), _mana_increase(-5)] 
            }
        },
    ENC_SHYD: {
        'bgcolor': (50, 153, 204),
        'mid': {
            'txt': 'Ship builders can\'t find wood.',
            'bgcolor': (41, 43, 155)
            },
        'left': {
            'txt': 'Slugs! Bad faith! Kill them all in a torrent of fire!',
            'bgcolor': (22, 22, 22),
            'effects': [_mana_increase(-10)]
            },
        'right': {
            'txt': 'Go check the forest.',
            'bgcolor': (222, 55, 55),
            'effects': [_add_encounter(ENC_FRST), _mana_increase(5)]
            }
        },
    ENC_TUT1: {
        'bgcolor': (138, 155, 66),
        'mid': {
            'txt': 'Will you gather enough mana to become the one true god?',
            'bgcolor': (193, 175, 122)
            },
        'left': {
            'txt': 'No',
            'bgcolor': (22, 22, 22),
            'effects': [_add_encounter(ENC_TUT3), _mana_increase(-5)]
            },
        'right': {
            'txt': 'Yes',
            'bgcolor': (222, 55, 55),
            'effects': [_add_encounter(ENC_TUT2), _mana_increase(50)]
            }
        },
    ENC_TUT2: {
        'bgcolor': (138, 155, 66),
        'mid': {
            'txt': 'Where will you go?',
            'bgcolor': (193, 175, 122)
            },
        'left': {
            'txt': 'Forest',
            'bgcolor': (55, 155, 55),
            'effects': [_add_encounter(ENC_FRST)]
            },
        'right': {
            'txt': 'Shipyard',
            'bgcolor': (55, 55, 222),
            'effects': [_add_encounter(ENC_SHYD)]
            }
        },
    ENC_TUT3: {
        'bgcolor': (138, 155, 66),
        'mid': {
            'txt': '...\nThen press ESC to leave the game.\nF11 is fullscreen by the way.',
            'bgcolor': (193, 175, 122)
            },
        'left': {
            'txt': 'Bring up the game over screen!',
            'bgcolor': (22, 22, 22),
            'effects': [_lose_game()]
            },
        'right': {
            'txt': 'OK. I am ready for adventure.',
            'bgcolor': (222, 55, 55),
            'effects': [_add_encounter(ENC_TUT2), _mana_increase(30)]
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
        self.encounters = deque([ENC_TUT1])
        self.cur_enc = None
        self.next_enc()
        
    def next_enc(self):
        """ pop the next encounter_render """
        try:
            self.cur_enc = self.encounters.popleft()
        except IndexError:  # empty: add fallback card
            self.encounters.extend([ENC_FBCK])  # TODO: game over instead?
            self.cur_enc = self.encounters.popleft()
        self.encounters_seen += 1
            
    def game_lost(self):
        self.game_status = GST_LOST
    
    # encounter_render effects exposed    
    def append_encounter(self, enc_kind, immediate=False):
        if immediate:
            self.encounters.appendleft(enc_kind)
        else:
            self.encounters.append(enc_kind)
    def increase_mana(self, x):
        self.mana = min(self.mana + x, self.mana_max)
        if self.mana <= 0:
            self.game_lost()
    def lose_game(self):
        self.game_lost()
    
    # making a choice
    def choose(self, choice):
        """ choice can be 'left' or 'right' """
        for effect_cb in encounter_data[self.cur_enc][choice]['effects']:
            effect_cb(self)  # update state
        self.next_enc()
