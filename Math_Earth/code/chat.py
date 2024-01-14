import pygame
from pygame import draw, display
from pygame.font import Font
from pygame import Rect
from random import randint
from settings import *

from pygame.math import Vector2

class ChatUi:
    def __init__(self) -> None:
        self.chat_font = Font(UI_FONT,CHAT_FONT_SIZE)
        # 四行文字的初始位置
        self.text_pos = [Vector2(180,10),Vector2(180,50),Vector2(180,90),Vector2(180,130)]

    def draw_text(self, text, pos, layer):
        # 文字位置
        pos_new = Vector2(0,540) + pos

        text_surf = self.chat_font.render(text,False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft=pos_new)
        layer.blit(text_surf,text_rect)

    def draw_dialog(self, npc_icon, layer):
        # 對話框背景
        bg_rect = Rect(0,540,1280,180)
        draw.rect(layer,UI_BG_COLOR,bg_rect)
        draw.rect(layer,UI_BORDER_COLOR,bg_rect.inflate(5,5),5)
        # NPC頭像
        npc_icon = pygame.transform.scale(npc_icon, (NPC_ICON_SIZE,NPC_ICON_SIZE))
        icon_rect = npc_icon.get_rect(topleft=(20,560))
        layer.blit(npc_icon,icon_rect)

class ChatScriptOfPaul(ChatUi):
    def __init__(self) -> None:
        super().__init__()
        # 第一次對話
        self.first_time = True
        # 鎖住不能換文本
        self.script_lock = False
        # 現在使用中的文本
        self.active_script = None
        self.trigger_times = 0
        self.script = [
            [
                "我是保羅~ 不是唱歌的、不是跳舞的、也不是玩蛇的。",
                "我是數學方面的專家，我是被派來指導你們數學的。",
                "如果有任何數學上的問題，隨時問我，我會很樂意幫助你的！",
            ],
            [
                "你需要學習數學，可是在這末世資源嚴重不足，",
                "你需要賺取貢獻點數，來換取數學書來學習魔法。",
                "能者多勞～你可以透過外出打敗魔物來換取點數。",
                "不要害怕挑戰，每次成功擊敗魔物，都是你邁向更強大魔法的一步。",
            ],
            [
                "這裡有一些數學書，你看看你想學習哪一款？畢竟會的魔法越多越安全嘛~！",
                "哈哈哈~無論你選擇哪一款，只要用心學習，你將能夠施展更強大的魔法！",
            ],
            [
                "嘿嘿~ 我這裡有一些便當，自從夫人要求我學烹飪後，這漸漸成為我的興趣。",
                "如果你有興趣，不妨買來試試看~ 說不定會有一些神奇的事情發生呢。",
            ],
            [
                "祝你好運，勇者！",
            ],
            [
                "你好，勇者，我是保羅。是你的數學特訓導師。",
                "哎呀～誰也沒想到這年代竟然會突然跑出一堆魔物。現在都快要變成無政府",
                "狀態了。物理攻擊基本上都對魔物無效。暫時我們只能躲起來避開魔物了。",
                "這裡是安全區域，你可以放心學習魔法。",
                "雖然不知道是什麼原理，但沒想到你們會的數學越多，魔法就越強。",
                "唔... 暫時看來你只會一些基本數學，所以能使用的魔法不多阿...",
                "數學這東西沒辦法馬上全學會的，只能靠多練習了。",
                "所以，加油吧！孩子們！人類的未來就交給你們了！",
            ],
        ]

    def script_unlock(self):
        # 可以切換下一個文本
        self.script_lock = False
        self.trigger_times += 1
        if self.trigger_times == 2:
            self.first_time = False

    def get_scripts(self):
        # 依照不同randint選擇不同文本
        s = randint(1,100)
        if s < 25:
            return self.script[0]
        elif s < 45:
            return self.script[1]
        elif s < 55:
            return self.script[2]
        elif s < 65:
            return self.script[3]
        else:
            return self.script[4]

    def show_first_time_dialog(self, layer):
        # 第一次對話的上半部  因為一次最多印4行
        if self.trigger_times == 0:
            self.draw_text(self.script[5][0], self.text_pos[0], layer)
            self.draw_text(self.script[5][1], self.text_pos[1], layer)
            self.draw_text(self.script[5][2], self.text_pos[2], layer)
            self.draw_text(self.script[5][3], self.text_pos[3], layer)
        else:
            # 第一次對話的下半部
            self.draw_text(self.script[5][4], self.text_pos[0], layer)
            self.draw_text(self.script[5][5], self.text_pos[1], layer)
            self.draw_text(self.script[5][6], self.text_pos[2], layer)
            self.draw_text(self.script[5][7], self.text_pos[3], layer)

    def show_dialog(self, icon):

        layer = display.get_surface()
        self.draw_dialog(icon, layer)

        if self.first_time:
            # 第一次對話用特別的文本
            self.show_first_time_dialog(layer)
            # 因為有bug所以鎖起來不能換
            self.script_lock = True
            return

        # 鎖住的話就用上一次的
        if self.script_lock:
            scripts = self.active_script
        else:
            # 拿新的文本
            scripts = self.get_scripts()
            self.active_script = scripts

        # 印出文本
        for index in range(len(scripts)):
            self.draw_text(scripts[index], self.text_pos[index], layer)

        # 因為有bug所以鎖起來不能換
        self.script_lock = True