#!/usr/bin/env python

import pygame

##########################################################
################## CHARACTERS AND POSES ##################
##########################################################

GAME_TITLE = "Game Title"

DO_NOT_SHOW_NAME = ["Scene", "Prompt", "Narrator"]

HERO_POSES = {"Default": "Knight-Default.png",
    "Angry": "Knight-Angry.png",
    "Sad": "Knight-sad.png",
    "Eager": "Knight-eager.png",
    "Annoyed": "Knight-Angry.png",
    "More annoyed": "Knight-Angry.png",
    "Defeated": "Knight-sad.png",
    "Confident": "Knight-Confident.png",
    "Calm": "Knight-calm.png",
    "Frightened": "Knight-Angry.png"}

WIZARD_POSES = {"Default": "Wizard-Default.png",
    "Touched": "Wizard-Touched.png",
    "Hands Raised": "Wizard-Hands Rasied.png",
    "Busy": "Wizard-Busy.png",
    "Angry": "Wizard-Angry.png"}

SPRITE_POSES = {"Default": "Fairy-Default.png",
    "Alarmed": "Fairy-Default.png"}

NARRATOR_POSES = {"Default": "empty.png"}

PRIEST_POSES = {"Default": "empty.png",
    "Frightened": "empty.png"}

BANDIT_POSES = {}

DRAGON_POSES = {}

CHAR_DICT = {"Hiens": WIZARD_POSES,
    "Benethir": HERO_POSES,
    "Sprite": SPRITE_POSES,
    "Bandit": BANDIT_POSES,
    "Dragon": DRAGON_POSES,
    "Narrator": NARRATOR_POSES,
    "Priest": PRIEST_POSES}

BACKGROUNDS = {"Intro": "workshop_placeholder.jpg",
    "Act 2": "woodland_placeholder.jpg",
    "Act 4": "workshop_placeholder.jpg"}

#########################################################
################# WINDOW AND DISPLAY ####################
#########################################################

GAME_SIZE = (1920, 1080)

TEXT_BOX_BORDER_X = 70
TEXT_BOX_BORDER_Y = 70
TEXT_BOX_WIDTH = GAME_SIZE[0] - 2*TEXT_BOX_BORDER_X
TEXT_BOX_HEIGHT = 300
TEXT_BOX_POS = (TEXT_BOX_BORDER_X,
    GAME_SIZE[1] - TEXT_BOX_BORDER_Y - TEXT_BOX_HEIGHT)

TEXT_BORDER_X = 70
TEXT_BORDER_TOP = 60
TEXT_BORDER_BOT = 60
TEXT_POS = (TEXT_BOX_POS[0] + TEXT_BORDER_X,
    TEXT_BOX_POS[1] + TEXT_BORDER_TOP)
TEXT_WIDTH = TEXT_BOX_WIDTH - 2*TEXT_BORDER_X
TEXT_HEIGHT = TEXT_BOX_HEIGHT - TEXT_BORDER_TOP - TEXT_BORDER_BOT
TEXT_SPACING_Y = 60
READING_SPEED = 30
NAME_BORDER_X = 30
NAME_BORDER_Y = 20

#########################################################
###################### CHARACTER RENDER #################
#########################################################

CHAR_POS = (160, 50)
CHAR_FADE_IN_TIME = 0.5
CHAR_FADE_IN_OFFSET = 50
CHAR_RECT = (int(480*1.5), int(720*1.5))
BLIP_PER = 0.05
