#!/usr/bin/env python

import pygame
from constants import *

from time import time, sleep
import sys
from math import sin

class Game(object):

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()
        self.res, fullscreen = self.prompt_resolution()
        pygame.display.quit()
        self.load_images()
        self.load_sounds()
        self.display_screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption(GAME_TITLE)
        if fullscreen:
            pygame.display.toggle_fullscreen()
        self.screen = pygame.Surface(GAME_SIZE)

        self.script_path = "script/"
        self.image_path = "images/"
        self.start_file = "start.txt"

        self.annoyance = 0

        self.main()

    def load_sounds(self):
        self.heins = pygame.mixer.Sound(file="sounds/hiens_theme.wav")
        self.battle = pygame.mixer.Sound(file="sounds/heat_of_battle.wav")
        self.music = {"Heins": self.heins,
            "Battle": self.battle}

        self.blip = pygame.mixer.Sound("sounds/blip.wav")
        self.blip.set_volume(0.17)

        self.music_playing = None

    def prompt_resolution(self):

        screen = pygame.display.set_mode((320, 240))
        pygame.display.set_caption(GAME_TITLE)
        tfont = pygame.font.SysFont("Courier", 20, bold=True)
        font = pygame.font.SysFont("Courier", 20)

        hey = tfont.render("Choose a resolution:", 1, (255, 255, 255))

        reses = ["800x450 windowed",
            "1280x720 windowed",
            "1920x1080 windowed",
            "1920x1080 fullscreen"]
        actual_reses = [(800, 450),
            (1280, 720),
            (1920, 1080),
            (1920, 1080)]
        selection = 0

        ose = []
        for i, res in enumerate(reses):
            bright = 150+(105*(selection==i))
            o = font.render(res, 1, (bright, bright, bright))
            ose.append(o)

        screen.blit(hey, (int(160-hey.get_width()/2), 65))
        for i, item in enumerate(ose):
            screen.blit(item, (int(160-item.get_width()/2), 90 + 20*i))
        pygame.display.flip()

        while True:
            screen.fill((0, 0, 0))
            events = pygame.event.get(pygame.KEYDOWN)
            keys = [event.key for event in events]
            if len(keys):
                if 274 in keys:
                    selection += 1
                    selection = min(selection, 3)
                if 273 in keys:
                    selection -= 1
                    selection = max(selection, 0)
                if 13 in keys:
                    break


            ose = []
            for i, res in enumerate(reses):
                bright = 150+(105*(selection==i))
                o = font.render(res, 1, (bright, bright, bright))
                ose.append(o)

            screen.blit(hey, (int(160-hey.get_width()/2), 65))
            for i, item in enumerate(ose):
                screen.blit(item, (int(160-item.get_width()/2), 90 + 20*i))
            pygame.display.flip()

        resolution = actual_reses[selection]
        go_full = (selection==3)

        return resolution, go_full

    def scene(self):
        pass

    def parse_script(self):
        txt = open(self.script_path+self.start_file, "r").read()
        by_char = txt.split("#")

        scene = Scene()

        for item in by_char:
            char = item.split("\n")[0]

            if char == "Prompt" or char == "TestAnnoyance":

                by_option = item.split("/")[1:]
                options = []
                links = []

                for opt in by_option:

                    split = opt.split("\n")
                    options.append(split[0])
                    links.append(split[1])

                line_to_add = Prompt(char, "Default", "Add links.")
                line_to_add.set_options(options)
                line_to_add.set_links(links)
                scene.add_lines([line_to_add])
                continue

            by_mood = (item.split("/"))[1:]

            for mood_item in by_mood:
                mood = mood_item.split("\n")[0]

                by_line = mood_item.split("\n")[1:]
                for line_item in by_line:

                    if len(line_item)>1:
                        line_to_add = Line(char, mood, line_item, sound=self.blip)
                        scene.add_lines([line_to_add])

        # for item in scene.lines:line_text
        #     print(item)

        return scene

    def load_images(self):

        self.bkdrops = {}
        for item in BACKGROUNDS:
            backdrop = pygame.image.load("images/"+BACKGROUNDS[item])
            backdrop = pygame.transform.scale(backdrop, (160, 90))
            self.bkdrops[item] = pygame.transform.scale(backdrop, GAME_SIZE)

        for character in CHAR_DICT:
            pose_dict = CHAR_DICT[character]
            for pose in pose_dict:
                image_path = pose_dict[pose]
                try:
                    new_img = pygame.image.load("images/"+image_path)
                    new_img = pygame.transform.scale(new_img, CHAR_RECT)
                except:
                    new_img = pygame.Surface(CHAR_RECT)
                    new_img.fill((200, 200, 90))
                pose_dict[pose] = new_img

    def main(self):

        script = self.parse_script()

        then = time()
        sleep(0.01)
        background = pygame.Surface((1920, 1080))
        background.fill((50, 50, 50))

        line = script.lines[0]


        self.lockout = False
        fade_surf = pygame.Surface((self.res))
        fade_surf.fill((0, 0, 0))
        fade_surf.set_alpha(0)
        target_fade = 0
        cur_fade = 0

        first_scene = True

        while True:

            now = time()
            dt = now - then
            then = now

            if line.has_expired():
                self.start_file = line.get_link(1)
                script = self.parse_script()
            line = script.lines[0]

            speed = 220
            if cur_fade < target_fade:
                cur_fade = min(target_fade, cur_fade + speed*dt)
            else:
                cur_fade = max(target_fade, cur_fade - speed*dt)
            fade_surf.set_alpha(cur_fade)

            while line.char in ["Scene", "GoTo", "AddAnnoyance", "Music", "TestAnnoyance"]:
                if line.char == "Scene":
                    if not first_scene:
                        target_fade = 255
                        if cur_fade < target_fade:
                            if self.music_playing:
                                self.music_playing.fadeout(1000)
                                self.music_playing = None
                            self.lockout = True
                            break
                        self.lockout = False
                        target_fade = 0
                    first_scene = False
                    background = self.bkdrops[line.text]
                    script.go_to_next()
                if line.char == "GoTo":
                    self.start_file = line.text
                    script = self.parse_script()
                if line.char == "AddAnnoyance":
                    amt = float(line.text)
                    self.annoyance += amt
                    script.go_to_next()
                if line.char == "Music":
                    if self.music_playing:
                        self.music_playing.fadeout(2000)
                    self.music[line.text].play(loops=-1)
                    self.music_playing = self.music[line.text]
                    script.go_to_next()
                if line.char == "TestAnnoyance":
                    modes = [int(option) for option in line.options]
                    for i, mode in enumerate(modes):
                        if self.annoyance >= mode:
                            self.start_file = line.links[i]
                            script = self.parse_script()
                            break

                line = script.lines[0]

            if line.char not in ["Scene", "GoTo", "AddAnnoyance", "Music", "TestAnnoyance"]:
                last_char_line = line

            self.temp_lock = False
            if line.char == "Prompt":
                if line.prop_done() < 0.25:
                    self.temp_lock = True


            pygame.event.pump()
            pressed = pygame.event.get(pygame.KEYDOWN)
            if len(pressed):
                keys = [item.key for item in pressed]
                if 27 in keys:
                    self.close_game()
                if 292 in keys:
                    pygame.display.toggle_fullscreen()

                if not self.lockout and not self.temp_lock:
                    if 13 in keys or 275 in keys:
                        if line.is_prompt:
                            self.start_file = line.get_link(0)
                            script = self.parse_script()
                            continue
                        script.go_to_next()

            self.screen.blit(background, (0, 0))

            if not self.lockout:
                if cur_fade == target_fade:
                    line.update(dt)
                    line.draw(self.screen)
                else:
                    line.draw_text_box(self.screen)
            else:
                last_char_line.target_opacity = 0
                last_char_line.target_yoff = 9999
                last_char_line.update(dt)
                last_char_line.draw(self.screen)


            scaled_down = pygame.transform.scale(self.screen, self.res)
            scaled_down.blit(fade_surf, (0, 0))

            annoy_font = pygame.font.SysFont("Arial", 30)
            scaled_down.blit(annoy_font.render(str(self.annoyance), 1, (255, 255, 255)), (50, 50))

            self.display_screen.blit(scaled_down, (0, 0))
            pygame.display.flip()

    def close_game(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()



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
        else:
            self.lines[0].bounce_mag = 8

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


    def __init__(self, char, expr, text, sound=None):
        """ Char says text in expr way """
        self.char = char
        self.expr = expr
        self.text = text.strip(" ").strip('"')
        self.characters_shown = 0
        self.time = 0
        self.chars_per_second = READING_SPEED
        self.char_opacity = 255
        self.char_yoff = 0
        self.target_opacity = 255
        self.target_yoff = 0
        self.text_abs_yoff = 0

        self.bounce_mag = 0
        self.bounce_freq = 6.28*6.0

        self.is_prompt = False

        self.time_since_blip = 5
        self.sound = sound

    def set_options(self, options):
        self.options = options

    def set_links(self, links):
        self.links = links

    def __repr__(self):
        return ("%s (%s): %s" % (self.char, self.expr, self.text))

    def has_expired(self):
        # normal lines can't expire
        return False

    def draw(self, screen):
        self.text_abs_yoff = 0
        self.draw_character(screen)
        self.draw_text_box(screen)
        self.draw_text(screen)
        self.draw_name(screen)

    def update(self, dt):
        self.time += dt

        # self.time_since_blip += dt
        # if self.time_since_blip > BLIP_PER and self.sound and self.characters_shown < len(self.text)-5:
        #     self.sound.stop()
        #     self.sound.play()
        #     self.time_since_blip = 0

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

        self.bounce_mag *= 0.02**dt
        if self.bounce_mag < 2:
            self.bounce_mag = 0


    def character_fade_in(self):
        self.char_opacity = 0
        self.target_opacity = 255

        self.char_yoff = CHAR_FADE_IN_OFFSET
        self.target_yoff = 0

    def draw_character(self, screen, force_char = False):
        if force_char:
            char = force_char
        else:
            char = self.char
        expressions = CHAR_DICT[char]
        try:
            img = expressions[self.expr]
        except:
            img = pygame.Surface(CHAR_RECT)
            img.fill((230, 230, 90))

        #img.set_colorkey((0, 255, 0))
        img = img.convert()
        trans_color = img.get_at((0,0))
        img.set_colorkey(trans_color)
        img.set_alpha(self.char_opacity)

        bounce_off = self.bounce_mag * sin(time()*self.bounce_freq)
        screen.blit(img, (CHAR_POS[0], CHAR_POS[1] + self.char_yoff + bounce_off))

    def draw_text_box(self, screen):

        surf = pygame.Surface((TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT))
        surf.set_alpha(120)
        screen.blit(surf, TEXT_BOX_POS)

    def draw_name(self, screen):

        if self.char in DO_NOT_SHOW_NAME:
            return

        xoff = 100

        font = pygame.font.SysFont("Arial", 60, bold=True)
        text = self.char
        render = font.render(self.char.upper(), 1, (255, 255, 255))
        box = pygame.Surface((render.get_width()+NAME_BORDER_X*2 + xoff - TEXT_POS[0] + TEXT_BORDER_X, render.get_height()+NAME_BORDER_Y))
        box.fill((0, 0, 0))
        box.blit(render, (NAME_BORDER_X+xoff-TEXT_BORDER_X, NAME_BORDER_Y))
        box.set_alpha(120)

        xpos = TEXT_POS[0] - TEXT_BORDER_X
        ypos = int(TEXT_POS[1] - box.get_height() - TEXT_BORDER_TOP)

        screen.blit(box, (xpos, ypos))


    def draw_text(self, screen, instant = False):

        if instant:
            self.time = 999

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
            screen.blit(item, (TEXT_POS[0], TEXT_POS[1] + offset + self.text_abs_yoff))

class Prompt(Line):
    def __init__(self, char, expr, text):
        Line.__init__(self, char, expr, text)
        self.time_started = False
        self.start_time = 0
        self.reaction_time = 8.0
        self.is_prompt = True

    def prop_done(self):
        return (time()-self.start_time)/self.reaction_time

    def has_expired(self):
        if time() - self.start_time >= self.reaction_time + 0.1:
            return True
        return False

    def start_time_func(self):
        if not self.time_started:
            self.time_started = True
            self.start_time = time()

    def set_options(self, options):
        self.options = options

    def set_links(self, links):
        self.links = links

    def get_link(self, option_idx):
        return self.links[option_idx]

    def draw(self, screen):
        self.draw_character(screen, force_char = "Sprite")

        self.start_time_func()
        text_spacing = 100
        self.text_abs_yoff = int(TEXT_HEIGHT/2 - text_spacing/2*len(self.options)) + 25
        self.draw_text_box(screen)
        for item in self.options:
            self.text = item
            self.draw_text(screen, instant = True)
            self.text_abs_yoff += text_spacing

        self.draw_time_bar(screen)

    def draw_text(self, screen, instant = True):

        do_font = pygame.font.SysFont("Tahoma", 50)
        dont_font = pygame.font.SysFont("Tahoma", 30)

        do = do_font.render(self.options[0], 1, (255, 255, 255))
        dont = dont_font.render("OR "+self.options[1].upper(), 1, (200, 200, 200))

        do_x = GAME_SIZE[0]/2 - do.get_width()/2
        do_y = TEXT_POS[1] + 50
        screen.blit(do, (do_x, do_y))

        dont_x = GAME_SIZE[0]/2 - dont.get_width()/2
        dont_y = TEXT_POS[1] + 120
        screen.blit(dont, (dont_x, dont_y))

    def draw_time_bar(self, screen):
        max_width = 1600
        height = 6

        time_elapsed = min(self.reaction_time, time() - self.start_time)
        prop_left = (self.reaction_time-time_elapsed)/self.reaction_time
        cur_width = max_width*prop_left**1.6

        if cur_width < 1:
            return

        bar = pygame.Surface((cur_width, height))
        bar_shadow = pygame.Surface((cur_width, height))
        prop_done = 1-prop_left
        r = 200
        b = 200 - 100*prop_done
        g = 200 - 100*prop_done
        bar.fill((int(r), int(g), int(b)))
        r -= 50
        g -= 50
        b -= 50
        bar_shadow.fill((int(r), int(g), int(b)))

        xpos = GAME_SIZE[0]/2 - int(cur_width/2)
        ypos = TEXT_BOX_POS[1] + 30

        screen.blit(bar, (xpos, ypos))
        screen.blit(bar_shadow, (xpos, ypos+height))


if __name__ == '__main__':
    a = Prompt("Benethir", "Angry", "Hello")
    a = Game()
