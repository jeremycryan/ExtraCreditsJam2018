#!/usr/bin/env python

import pygame
from constants import *

from time import time, sleep

class Game(object):

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()
        self.res = self.prompt_resolution()
        self.display_screen = pygame.display.set_mode(self.res)
        self.screen = pygame.Surface(GAME_SIZE)

        self.script_path = "script/"
        self.image_path = "images/"
        self.start_file = "start.txt"
        self.main()

    def prompt_resolution(self):
        resolution = (1200, 675)
        return resolution

    def scene(self):
        pass

    def parse_script(self):
        txt = open(self.script_path+self.start_file, "r").read()
        by_char = txt.split("#")

        scene = Scene()

        for item in by_char:
            char = item.split("\n")[0]

            by_mood = (item.split("/"))[1:]

            for mood_item in by_mood:
                mood = mood_item.split("\n")[0]

                by_line = mood_item.split("\n")[1:]
                for line_item in by_line:

                    if len(line_item)>1:
                        line_to_add = Line(char, mood, line_item)
                        scene.add_lines([line_to_add])

        # for item in scene.lines:
        #     print(item)

        return scene

    def main(self):

        script = self.parse_script()

        then = time()
        sleep(0.01)
        background = pygame.Surface((1920, 1080))
        background.fill((50, 50, 50))

        line = script.lines[0]
        self.bkdrops = {}
        for item in BACKGROUNDS:
            backdrop = pygame.image.load("images/"+BACKGROUNDS[item])
            backdrop = pygame.transform.scale(backdrop, (80, 45))
            self.bkdrops[item] = pygame.transform.scale(backdrop, GAME_SIZE)

        while True:

            now = time()
            dt = now - then
            then = now

            line = script.lines[0]
            while line.char in ["Scene", "GoTo"]:
                if line.char == "Scene":
                    background = self.bkdrops[line.text]
                    script.go_to_next()
                if line.char == "GoTo":
                    self.start_file = line.text
                    script = self.parse_script()
                line = script.lines[0]

            pygame.event.pump()
            pressed = pygame.event.get(pygame.KEYDOWN)
            if len(pressed):
                keys = [item.key for item in pressed]
                if 13 in keys:
                    script.go_to_next()

            self.screen.blit(background, (0, 0))
            line.update(dt)
            line.draw(self.screen)

            scaled_down = pygame.transform.scale(self.screen, self.res)
            self.display_screen.blit(scaled_down, (0, 0))
            pygame.display.flip()



class Scene(object):

    def __init__(self):
        self.lines = []
        self.past_lines = []

    def add_lines(self, line_list):
        self.lines += line_list

    def go_to_next(self):
        self.past_lines.append(self.lines[0])
        self.lines = self.lines[1:]
        if self.char_has_changed():
            self.lines[0].character_fade_in()

    def last_line(self):
        return self.past_lines[-1]

    def last_character(self):
        try:
            return self.last_line().char
        except:
            return "Narrator"

    def char_has_changed(self):
        if self.last_character() == self.lines[0].char:
            return False
        return True



class Line(object):

    def __init__(self, char, expr, text):
        """ Char says text in expr way """
        self.char = char
        self.expr = expr
        print(text)
        self.text = text.strip(" ").strip('"').decode()
        self.characters_shown = 0
        self.time = 0
        self.chars_per_second = READING_SPEED
        self.char_opacity = 255
        self.char_yoff = 0
        self.target_opacity = 255
        self.target_yoff = 0

    def __repr__(self):
        return ("%s (%s): %s" % (self.char, self.expr, self.text))

    def draw(self, screen):
        self.draw_character(screen)
        self.draw_text_box(screen)
        self.draw_text(screen)

    def update(self, dt):
        self.time += dt

        fade_speed = 255.0/CHAR_FADE_IN_TIME
        float_speed = 1.0*CHAR_FADE_IN_OFFSET/CHAR_FADE_IN_TIME

        if self.char_yoff < self.target_yoff:
            self.char_yoff = min(self.target_yoff, self.char_yoff + float_speed*dt)
        else:
            self.char_yoff = max(self.target_yoff, self.char_yoff - float_speed*dt)

        if self.char_opacity < self.target_opacity:
            self.char_opacity = min(self.target_opacity, self.char_opacity + fade_speed*dt)
        else:
            self.char_opacity = max(self.target_opacity, self.char_opacity - fade_speed*dt)


    def character_fade_in(self):
        self.char_opacity = 0
        self.target_opacity = 255

        self.char_yoff = CHAR_FADE_IN_OFFSET
        self.target_yoff = 0

    def draw_character(self, screen):
        expressions = CHAR_DICT[self.char]
        correct_expression = expressions[self.expr.lower().capitalize()]
        try:
            img = pygame.image.load("images/" + correct_expression)
        except:
            img = pygame.image.load("images/hero_angry.png")

        #img.set_colorkey((0, 255, 0))
        img = img.convert()
        trans_color = img.get_at((0,0))
        img.set_colorkey(trans_color)
        img.set_alpha(self.char_opacity)

        screen.blit(img, (CHAR_POS[0], CHAR_POS[1] + self.char_yoff))

    def draw_text_box(self, screen):

        surf = pygame.Surface((TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT))
        surf.set_alpha(140)
        screen.blit(surf, TEXT_BOX_POS)

    def draw_text(self, screen):

        font = pygame.font.SysFont("Tahoma", 40)
        self.characters_shown = int(self.time*self.chars_per_second)
        text_to_show = self.text[:self.characters_shown]
        text_to_try = text_to_show
        font_img = font.render(text_to_try, 1, (255, 255, 255))

        text_done = ""
        text_renders = []

        text_to_try = text_to_try.split()[:]
        test_img = self.text[len(text_done):]
        test_img = " ".join(test_img.split()[:len(text_to_try)])
        text_to_try = " ".join(text_to_try)
        font_img = font.render(test_img.strip(" ").strip('"'), 1, (255, 255, 255))

        while len(text_done) < len(text_to_show):

            #text_to_try = text_to_try[:].split()
            test_img = self.text[len(text_done):]
            test_img = " ".join(test_img.split()[:len(text_to_try.split())])
            #text_to_try = " ".join(text_to_try)
            font_img = font.render(test_img.strip(" ").strip('"'), 1, (255, 255, 255))


            while font_img.get_width() > TEXT_WIDTH:
                text_to_try = text_to_try[:-1].split()
                test_img = self.text[len(text_done):]
                test_img = " ".join(test_img.split()[:len(text_to_try)])
                text_to_try = " ".join(text_to_try)
                font_img = font.render(test_img.strip(" ").strip('"'), 1, (255, 255, 255))

            text_to_try = text_to_try[max(len(text_renders)-1, 0):]
            font_img = font.render(text_to_try.strip(" ").strip('"'), 1, (255, 255, 255))
            text_renders.append(font_img)
            text_done += text_to_try + " "*max(len(text_renders) - 1, 0)
            text_to_try = text_to_show[len(text_done):]


        for i, item in enumerate(text_renders):
            offset = i*TEXT_SPACING_Y
            screen.blit(item, (TEXT_POS[0], TEXT_POS[1] + offset))


if __name__ == '__main__':
    a = Game()
