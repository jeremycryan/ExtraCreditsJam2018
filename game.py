#!/usr/bin/env python

import pygame

class Game(object):

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()
        res = self.prompt_resolution()
        pygame.display.set_mode(res)

        self.script_path = "script/"
        self.start_file = "start.txt"
        self.main()

    def prompt_resolution(self):
        resolution = (640, 480)
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

        print(self.parse_script())
        while True:
            pass


class Scene(object):

    def __init__(self):
        self.lines = []

    def add_lines(self, line_list):
        self.lines += line_list

    def __repr__(self):
        for item in self.lines:
            print(item)
        return("End of script.")


class Line(object):

    def __init__(self, char, expr, text):
        """ Char says text in expr way """
        self.char = char
        self.expr = expr
        self.text = text

    def __repr__(self):
        return ("%s (%s): %s" % (self.char, self.expr, self.text))

    def draw(self):



if __name__ == '__main__':
    a = Game()
