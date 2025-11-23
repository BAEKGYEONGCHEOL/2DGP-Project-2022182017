from pico2d import *

# hp 틀
class HPTool:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('hp_tool.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

# hp 바
class HPBar:
    def __init__(self, character, x, y):
        self.character = character     # 해당 캐릭터 체력바!
        self.x = x
        self.y = y
        self.image = load_image('hp_bar.png')

    def update(self):
        pass

    def draw(self):
        # hp 비율 계산!
        hp_rate = self.character.current_hp / self.character.max_hp
        width = int(self.image.w * hp_rate)
        # 그리기!
        self.image.clip_draw(0, 0, width, self.image.h, self.x, self.y)