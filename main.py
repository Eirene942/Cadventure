import pygame
import sys
import textwrap
import random

pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

#   game state
game_state = "start"  # "start", "game", "dead", "win"


#  characters
characters = [
    {
        "name": "Ragdoll",
        "image": "ragdoll.png",
        "traits": ["sweet", "courageous", "resilient"],
        "chances": {
            "room1": [0.6, 0.9, 0.6],
            "room2": [0.8, 0.8, 0.0],
            "room3": [0.8, 0.9, 0.7],
            "room4": [0.7, 0.7, 0.9],
            "room5": [1.0, 1.0, 1.0],
        },
    },
    {
        "name": "Orange Cat",
        "image": "orangecat.png",
        "traits": ["witty", "charming", "tenacious"],
        "chances": {
            "room1": [0.7, 0.7, 0.9],
            "room2": [0.8, 0.9, 0.0],
            "room3": [0.9, 0.7, 0.8],
            "room4": [0.9, 0.8, 0.8],
            "room5": [1.0, 1.0, 1.0],
        },
    },
    {
        "name": "Savannah",
        "image": "savannah.png",
        "traits": ["strong", "brave", "clever"],
        "chances": {
            "room1": [0.9, 0.6, 0.7],
            "room2": [0.9, 0.8, 0.0],
            "room3": [0.8, 0.7, 0.9],
            "room4": [0.8, 0.9, 0.7],
            "room5": [1.0, 1.0, 1.0],
        },
    },
]

selected_index = 0
chosen_character = None

#   rooms
scenes = {
    "room1": {
        "image": "dog.png",
        "text": "You arrive at the cave entrance. A big dog guards the way. What do you do? ",
        "choices": [
            "Attack!",
            "Talk to the dog, befriend him and ask him nicely if you can come in.",
            "Take the wooden stick next to you and throw it as far as you can. While the stupid dog is busy sneak into the cave.",
        ],
        "next": "room2",
    },
    "room2": {
        "image": "wall.png",
        "text": "You walk on until a high wall bars your way. The path above lies just out of reach. To your left, broken boxes lean against each other, marked with a strange sign that warns of poison or worse. What do you do?  ",
        "choices": [
            "Well certainly no challenge for me. I'll jump all the way to the top.",
            "You jump upwards over the boxes and risk the boxes collapsing and you falling into the poison.",
            "You don't care. You decide to go home to mommy and daddy and sleep and eat all day like your life was meant to be.",
        ],
        "next": "room3",
    },
    "room3": {
        "image": "rats.png",
        "text": "You descend into the cave's gloom. Hundreds of rats swarm from the shadows.  One wearing a tiny rusted crown must be leader. What do you do?  "

,
        "choices": ["Meow as loudly as you can, hiss as loudly as you can, and scare them away. When they freeze in fear, sneak past them.",  "Talk to the leader and convince him you mean no harm and ask if you can pass.","Attack !!!",],
        "next": "room4",
    },
    "room4": {
        "image": "gate.png",
        "text": "You walk on. A great gate appears. A snake lies in front of the gate and a silver chain around it's neck upon it hangs a single key. The key must open the gate you think. What do you do?  ",
        "choices": ["I think the snake is asleep. I'll sneak up and carefully take the necklace.", "Attack!!!", "The snake looks friendly. I'll wake her up and ask for the key."],
        "next": "room5",
    },
    "room5": {
        "image": "treasure.png",
        "text": "You find the treasure of endless treats! You made it!",
        "choices": ["Eat treats!", "Nap", "Purr loudly."],
        "next": None,
    },
}

current_room = "room1"
choice_selected = 0

choice_rects = []  #  list of pygame.Rect for current choices

#  fonts
font = pygame.font.SysFont(None, 28)
title_font = pygame.font.SysFont(None, 64)


def draw_start_screen(): # start screen
    screen.fill((30, 30, 30))
    try:
        bg = pygame.image.load("cave2.jpg").convert()
        bg = pygame.transform.scale(bg, (1200, 800))
        screen.blit(bg, (0, 0))
    except:
        screen.fill((50, 50, 50))

    title = title_font.render("Cadventure", True, (255, 255, 255))
    screen.blit(title, (450, 100))

    #   characters
    for i, char in enumerate(characters):
        x = 250 + i * 300
        y = 250

        # load images
        try:
            img = pygame.image.load(char["image"]).convert_alpha()
            img = pygame.transform.scale(img, (150, 150))
            screen.blit(img, (x, y))
        except:
            pygame.draw.rect(screen, (150, 150, 150), (x, y, 150, 150))

        # frame
        if i == selected_index:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 150, 150), 3)

        # name
        name_surface = font.render(char["name"], True, (255, 255, 255))
        screen.blit(name_surface, (x + 10, y + 160))

        # list of traits
        for j, trait in enumerate(char["traits"]):
            trait_surface = font.render(f"- {trait}", True, (200, 200, 200))
            screen.blit(trait_surface, (x + 10, y + 190 + j * 20))

    # hint text
    hint_text = (
        "It is said that in the dark cave in the greenest forest "
        "there is a treasure hidden full of treats.                         "
        "So much treats that indeed no cat could eat all in seven lifetimes.                                                       "
        "Choose your cat and let's get the treats!"
    )
    wrapped_lines = textwrap.wrap(hint_text, width=100)
    y = 700
    for line in wrapped_lines:
        hint_surface = font.render(line, True, (220, 220, 220))
        screen.blit(hint_surface, (100, y))
        y += 25

def draw_scene():
    scene = scenes[current_room]
    
    # Black background for the whole screen
    screen.fill((0, 0, 0))

    #   Load and draw scene image in upper-right quarter  
    try:
        img = pygame.image.load(scene["image"]).convert()
        
        # Scale image to 1/4 of the window (400x600 as used previously)
        img = pygame.transform.scale(img, (400, 600))
         
        # Draw image in the upper-right corner
        screen.blit(img, (800, 0))

    except:
        # If image fails, draw a placeholder gray box (kept consistent with image placement)
        pygame.draw.rect(screen, (50, 50, 50), (800, 0, 400, 600))

    #   Draw the scene text  
    wrapped = textwrap.wrap(scene["text"], 80)
    for i, line in enumerate(wrapped):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (20, 500 + i * 25))

    # --- Draw choices and build clickable rects ---
    # Clear old rects for this frame
    choice_rects.clear()  # English: clear the rects list and rebuild for current choices

    for i, choice in enumerate(scene["choices"]):
        color = (255, 255, 0) if i == choice_selected else (255, 255, 255)
        txt = font.render(f"{i+1}. {choice}", True, color)
        x = 50
        y = 650 + i * 30
        screen.blit(txt, (x, y))

        # English: create a slightly padded rect around each rendered choice for mouse hits
        padding_x = 8
        padding_y = 4
        rect = pygame.Rect(x - padding_x, y - padding_y, txt.get_width() + padding_x * 2, txt.get_height() + padding_y * 2)
        choice_rects.append(rect)
        # Uncomment below to debug clickable areas:
        # pygame.draw.rect(screen, (255,0,0), rect, 1)

    #   Show chosen character  
    if chosen_character:
        char_text = font.render(f"Character: {chosen_character['name']}  ", True, (255, 255, 0))
        screen.blit(char_text, (10, 10))




def draw_game_over():
    screen.fill((0, 0, 0))
    msg = title_font.render("GAME OVER", True, (255, 50, 50))
    screen.blit(msg, (450, 300))
    hint = font.render("Press R to restart", True, (200, 200, 200))
    screen.blit(hint, (500, 400))


def draw_win():
    screen.fill((0, 0, 0))
    msg = title_font.render("YOU WIN!", True, (50, 255, 50))
    screen.blit(msg, (470, 300))
    hint = font.render("Press R to play again", True, (200, 200, 200))
    screen.blit(hint, (480, 400))


#   main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "start":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(characters)):
                    rect = pygame.Rect(250 + i * 300, 250, 150, 150)
                    if rect.collidepoint(mouse_pos):
                        selected_index = i
                        chosen_character = characters[i]
                        game_state = "game"

        elif game_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    choice_selected = (choice_selected - 1) % len(scenes[current_room]["choices"])
                elif event.key == pygame.K_DOWN:
                    choice_selected = (choice_selected + 1) % len(scenes[current_room]["choices"])
                elif event.key == pygame.K_RETURN:
                    survival_chance = chosen_character["chances"][current_room][choice_selected]
                    if random.random() < survival_chance:
                        next_room = scenes[current_room]["next"]
                        if next_room:
                            current_room = next_room
                        else:
                            game_state = "win"
                    else:
                        game_state = "dead"

            # handle mouse clicks on choices
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # iterate clickable rects created in draw_scene()
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        # set the selected index and perform the same selection logic as RETURN
                        choice_selected = i
                        survival_chance = chosen_character["chances"][current_room][choice_selected]
                        if random.random() < survival_chance:
                            next_room = scenes[current_room]["next"]
                            if next_room:
                                current_room = next_room
                            else:
                                game_state = "win"
                        else:
                            game_state = "dead"
                        break  # stop after handling the clicked choice

        elif game_state in ["dead", "win"]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                current_room = "room1"
                game_state = "start"
                chosen_character = None

    if game_state == "start":
        draw_start_screen()
    elif game_state == "game":
        draw_scene()
    elif game_state == "dead":
        draw_game_over()
    elif game_state == "win":
        draw_win()

    pygame.display.flip()
    clock.tick(10)