#!/usr/bin/env python

import pygame

##########################################################
################## CHARACTERS AND POSES ##################
##########################################################


HERO_POSES = {"Default": "hero_default.png",
    "Angry": "hero_angry.png",
    "Sad": "hero_sad.png",
    "Eager": "hero_eager.png",
    "Annoyed": "hero_annoyed.png",
    "More annoyed": "hero_more_annoyed.png",
    "Defeated": "hero_defeated.png"}

WIZARD_POSES = {"Default": "wizard_default.png",
    "Touched": "wizard_touched.png",
    "Hands raised": "wizard_hand_raised.png"}

SPRITE_POSES = {"Default": "sprite_default.png"}

NARRATOR_POSES = {"Default": "empty.png"}

BANDIT_POSES = {}

DRAGON_POSES = {}

CHAR_DICT = {"Hiens": WIZARD_POSES,
    "Benethir": HERO_POSES,
    "Sprite": SPRITE_POSES,
    "Bandit": BANDIT_POSES,
    "Dragon": DRAGON_POSES,
    "Narrator": NARRATOR_POSES}

BACKGROUNDS = {"Intro": "workshop_placeholder.jpg",
    "Act 2": "woodland_placeholder.jpg"}

#########################################################
################# WINDOW AND DISPLAY ####################
#########################################################

GAME_SIZE = (1920, 1080)

TEXT_BOX_BORDER_X = 70
TEXT_BOX_BORDER_Y = 70
TEXT_BOX_WIDTH = GAME_SIZE[0] - 2*TEXT_BOX_BORDER_X
TEXT_BOX_HEIGHT = 360
TEXT_BOX_POS = (TEXT_BOX_BORDER_X,
    GAME_SIZE[1] - TEXT_BOX_BORDER_Y - TEXT_BOX_HEIGHT)

TEXT_BORDER_X = 70
TEXT_BORDER_Y = 70
TEXT_POS = (TEXT_BOX_POS[0] + TEXT_BORDER_X,
    TEXT_BOX_POS[1] + TEXT_BORDER_Y)
TEXT_WIDTH = TEXT_BOX_WIDTH - 2*TEXT_BORDER_X
TEXT_HEIGHT = TEXT_BOX_HEIGHT - 2*TEXT_BORDER_Y
TEXT_SPACING_Y = 60
READING_SPEED = 30

#########################################################
###################### CHARACTER RENDER #################
#########################################################

CHAR_POS = (200, 170)
CHAR_FADE_IN_TIME = 0.5
CHAR_FADE_IN_OFFSET = 50
