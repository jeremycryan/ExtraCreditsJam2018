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

        while True:

            now = time()
            dt = now - then
            then = now

            pygame.event.pump()
            pressed = pygame.event.get(pygame.KEYDOWN)
            if len(pressed):
                keys = [item.key for item in pressed]
                print(keys)
                if 13 in keys:
                    script.go_to_next()

            self.screen.fill((50, 50, 50))
            line = script.lines[0]
            line.update(dt)
            line.draw(self.screen)

            scaled_down = pygame.transform.scale(self.screen, self.res)
            self.display_screen.blit(scaled_down, (0, 0))
            pygame.display.flip()



class Scene(object):

    def __init__(self):
        self.lines = []

    def add_lines(self, line_list):
        self.lines += line_list

    def go_to_next(self):
        self.lines = self.lines[1:]



class Line(object):

    def __init__(self, char, expr, text):
        """ Char says text in expr way """
        self.char = char
        self.expr = expr
        self.text = text.strip(" ").strip('"')
        self.characters_shown = 0
        self.time = 0
        self.chars_per_second = READING_SPEED

    def __repr__(self):
        return ("%s (%s): %s" % (self.char, self.expr, self.text))

    def draw(self, screen):
        self.draw_character(screen)
        self.draw_text_box(screen)
        self.draw_text(screen)

    def update(self, dt):
        self.time += dt

    def draw_character(self, screen):
        expressions = CHAR_DICT[self.char]
        correct_expression = expressions[self.expr.lower().capitalize()]
        try:
            img = pygame.image.load("images/" + correct_expression)
        except:
            img = pygame.image.load("images/hero_angry.png")

        screen.blit(img, CHAR_POS)

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

            print(len(text_renders))
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
