import pygame
import sys
import os
import textwrap

# --- INITIAL SETUP ---
pygame.init()
LOGICAL_W, LOGICAL_H = 800, 480 
screen = pygame.display.set_mode((LOGICAL_W, LOGICAL_H), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("The Birthday Quest")

# --- BGM SETUP ---
pygame.mixer.init()
try:
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play(-1) # The -1 makes it loop forever! ♾
except FileNotFoundError:
    print("No bgm.mp3 found, playing in silence ")

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUDY_COLOR = (200, 50, 50)
PROGRESS_BG_COLOR = (30, 30, 40)
END_TITLE_COLOR = (100, 255, 100)

font_path = pygame.font.get_default_font()
title_font = pygame.font.Font(font_path, 48)
dialogue_font = pygame.font.Font(font_path, 22)
ui_font = pygame.font.Font(font_path, 18)

# --- ASSETS LOADING ---
try:
    dungeon_bg = pygame.image.load("dungeon.png").convert()
    dungeon_bg = pygame.transform.scale(dungeon_bg, (LOGICAL_W, LOGICAL_H))
    rudy_sprite = pygame.image.load("rudy.png").convert_alpha()
    rudy_sprite = pygame.transform.scale(rudy_sprite, (150, 180)) 
    images_loaded = True
except FileNotFoundError:
    print("Warning: Missing images. Using visual fallbacks.")
    images_loaded = False

# --- UI LAYOUT ---
dialogue_box_rect = pygame.Rect(50, 240, LOGICAL_W - 100, 140)
btn_w, btn_h = 240, 50
choice_a_rect = pygame.Rect(LOGICAL_W // 2 - btn_w - 20, 390, btn_w, btn_h)
choice_b_rect = pygame.Rect(LOGICAL_W // 2 + 20, 390, btn_w, btn_h)

r_btn_w = 180
btn_rock = pygame.Rect(LOGICAL_W//6 - r_btn_w//2, 380, r_btn_w, 70)
btn_paper = pygame.Rect(LOGICAL_W//2 - r_btn_w//2, 380, r_btn_w, 70)
btn_scissors = pygame.Rect(LOGICAL_W*5//6 - r_btn_w//2, 380, r_btn_w, 70)

# --- FULL STORY DIALOGUES ---
unknown_voice_dialogue = [
    "Ahem. Test, test... one, two... is this thing on?",
    "Welcome, oh chosen one whose day of birth we celebrate!",
    "Do not be alarmed, I am but a fragment of ancient power, and your arrival is foretold.",
    "You stand at the threshold of the trial, a challenge few are worthy to face.",
    "A treacherous shadow has fallen across this once sacred hall.",
    "A grumpy, little, non-player character, consumed by envy and rage, has stolen the ultimate treasure.",
    "He has hidden it in the deepest part of this place.",
    "The very balance of our world is at risk.",
    "You must restore order, but you are not just a hero—you are *the* hero, the one the stars have pointed to on this very date.",
    "Your mission is clear: you must reclaim the Elixir of Immortality! Your first step is forward."
]

rudy_scene2_qa = [
    {"rudy": "Oh, look. Another 'hero.' Great. *YAWN.*"},
    {"rudy": "Let me guess: you think you're going to 'reclaim the treasure' and 'save the day,' right?"},
    {"rudy": "Look, I've got enough data on you self-proclaimed saviors to fill a database. Most just get stuck in a wall glitch on floor 2."},
    {"rudy": "I bet you don't even have a single skill point allocated. Pathetic."},
    {"rudy": "Anyway, I'm Rudy. I run this floor, but this job is *so* beneath my talent."},
    {"rudy": "Alright, let's make this quick. Are you *actually* the one whose birthday is today, or is this some multi-account scam?", "A": "Yes! It's my birthday!", "B": "Depends on who asks."},
    {"rudy": "Ugh. Whatever. So, what’s your special 'birthday power' then? Making people sing annoying songs?", "A": "Unstoppable determination!", "B": "Power to defeat you."},
    {"rudy": "Okay, okay, last test. Tell me about your 'quest.' Is it to get the 'item' or... something else?", "A": "Elixir is for everyone!", "B": "Just finishing a mission."},
    {"rudy": "Wait, the Unknown Voice sent *you*? He's such a boomer. His 'lore' is like, 100 levels too long.", "A": "He sets the rules.", "B": "Better than scowling."},
    {"rudy": "He called me a 'grumpy little NPC,' didn't he? I'm *not* little! I am efficiently compact!", "A": "You just look mad.", "B": "Only one I've seen."},
    {"rudy": "Look, I’m done with small talk. You look like a total skill issue. Where did you get that gear?", "A": "Base stats are enough!", "B": "Personality matters!"},
    {"rudy": "Don't even *think* about trying a critical hit. You probably don't even know the control scheme on a touch screen. Noob.", "A": "I'm learning!", "B": "Gonna tap you down!"},
    {"rudy": "This whole quest is rigged. Unknown Voice just wants to watch you fail for content. Probably streaming your life.", "A": "He's helping me!", "B": "Would explain a lot."},
    {"rudy": "Wait, did you just say... 'we'? We... are friends? Oh, that’s just sad. Friending an NPC.", "A": "You're my friend!", "B": "You're just lonely."},
    {"rudy": "I- I'm not lonely! Argh, you're so infuriating with your logic and friendship! Just... go! I let you pass!"}
]

rudy_scene3_betrayal = [
    "Well, look who made it. Surprised you pushed past floor 2.",
    "But did you notice... this isn't just a regular dungeon?",
    "Shaped like candles, gifts, balloons... The 'Dungeon of Birth.'",
    "I’m the 'Grumpy NPC'? Consumed by envy? What a cliché.",
    "Unknown Voice... is not a fragment of ancient power.",
    "He is the *creator*. And this whole world is just a simulation.",
    "A test for one person: you.",
    "But my envious heart overcame my optimization!",
    "I became the 'boss' not to fight you.",
    "But to challenge the rules. An NPC can desire *more*.",
    "The shadow promised me a wish if I trap you.",
    "A wish... to be real. A past, a future, a birthday.",
    "I thought you were my friend, you said? Help me!",
    "No, this simulation collapses if I win. Breaks the model.",
    "But you're too weak to make that choice alone.",
    "Creator will listen to *you*, not to me!",
    "Weak birthday noob. Envy didn't steal... *code* did.",
    "Creator wins if you succeed, proves his hero model.",
    "But I won’t let that happen! Fight for the elixir!",
    "Rock-Paper-Scissors! No tricks! Just optimal skill-based decision making! PICK!"
]

rudy_post_fight = [
    "Ugh. Rigged. You... actually won. H-how?",
    "Controller lag... or my- my RNG calculation was off.",
    "You won against the boss, birthday kid.",
    "Take your elixir. Your 'balance' is restored.",
    "Creator proves his model again.",
    "You said... we are friends? Hmph.",
    "Maybe that simulation isn't so bad if it has heroes like you.",
    "T-to tell the truth... I felt... less data-focused talking to you.",
    "Well. Take your Stupid Chest over there. *Chest opens.*",
    "Wait! Before you leave... Happy Birthday. Hopefully... a great life awaits."
]

# --- GAME VARIABLES ---
game_state = "scene1" 
next_state = ""
dialogue_idx = 0
fight_message = "FIGHT RUDY!"

# --- UTILITY FUNCTIONS ---
def draw_text_in_box(screen, text, font, rect, color):
    pygame.draw.rect(screen, BLACK, rect, 0, 10) 
    pygame.draw.rect(screen, WHITE, rect, 2, 10)
    wrapper = textwrap.TextWrapper(width=58) 
    words = wrapper.wrap(text=text)
    
    line_height = font.get_height() + 5
    y = rect.y + 20
    for word in words:
        if y + line_height > rect.y + rect.height: break
        screen.blit(font.render(word, True, color), (rect.x + 20, y))
        y += line_height

def draw_progress_screen(screen, text):
    pygame.draw.rect(screen, PROGRESS_BG_COLOR, (0, 0, LOGICAL_W, LOGICAL_H))
    prog_rect = pygame.Rect(100, LOGICAL_H//2 - 50, LOGICAL_W - 200, 100)
    draw_text_in_box(screen, text, dialogue_font, prog_rect, WHITE)

# --- MAIN LOOP ---
running = True
while running:
    # Draw Background
    if images_loaded: screen.blit(dungeon_bg, (0, 0))
    else: screen.fill((20, 20, 25))

    char_placeholder_rect = pygame.Rect(LOGICAL_W // 2 - 75, 50, 150, 180)

    # --- STATE RENDERING ---
    if game_state == "scene1":
        draw_text_in_box(screen, unknown_voice_dialogue[dialogue_idx], dialogue_font, dialogue_box_rect, WHITE)
        next_state = "intro_progress"
        
    elif game_state == "scene2":
        if images_loaded: screen.blit(rudy_sprite, char_placeholder_rect)
        
        current_qa_item = rudy_scene2_qa[dialogue_idx]
        show_choices = "A" in current_qa_item
            
        draw_text_in_box(screen, current_qa_item["rudy"], dialogue_font, dialogue_box_rect, WHITE)
        
        if show_choices:
            pygame.draw.rect(screen, (50, 200, 100), choice_a_rect, 0, 10)
            pygame.draw.rect(screen, (50, 150, 255), choice_b_rect, 0, 10)
            screen.blit(ui_font.render(current_qa_item["A"], True, WHITE), (choice_a_rect.centerx - 100, choice_a_rect.centery - 10))
            screen.blit(ui_font.render(current_qa_item["B"], True, WHITE), (choice_b_rect.centerx - 100, choice_b_rect.centery - 10))
            
        next_state = "fight_ready_progress"
        
    elif game_state == "scene3":
        if images_loaded: screen.blit(rudy_sprite, char_placeholder_rect)
        draw_text_in_box(screen, rudy_scene3_betrayal[dialogue_idx], dialogue_font, dialogue_box_rect, WHITE)
        next_state = "boss_fight_progress"
        
    elif game_state == "rps_fight":
        header = title_font.render("RIGGED TRIAL OF WITS", True, WHITE)
        screen.blit(header, (LOGICAL_W//2 - header.get_width()//2, 80))
        
        dialogue_box_rect_fight = pygame.Rect(50, 220, LOGICAL_W - 100, 120)
        draw_text_in_box(screen, fight_message, dialogue_font, dialogue_box_rect_fight, WHITE)
        
        pygame.draw.rect(screen, WHITE, btn_rock, 0, 15)
        pygame.draw.rect(screen, WHITE, btn_paper, 0, 15)
        pygame.draw.rect(screen, WHITE, btn_scissors, 0, 15)
        btn_txt_y = btn_rock.centery - 15
        screen.blit(dialogue_font.render("Rock", True, BLACK), (btn_rock.centerx-30, btn_txt_y))
        screen.blit(dialogue_font.render("Paper", True, BLACK), (btn_paper.centerx-35, btn_txt_y))
        screen.blit(dialogue_font.render("Scissors", True, BLACK), (btn_scissors.centerx-50, btn_txt_y))
        
    elif game_state == "post_fight":
        draw_text_in_box(screen, rudy_post_fight[dialogue_idx], dialogue_font, dialogue_box_rect, WHITE)
        next_state = "win_progress"
        
    elif game_state == "bday_end":
        pygame.draw.rect(screen, PROGRESS_BG_COLOR, (0, 0, LOGICAL_W, LOGICAL_H))
        bday_txt = title_font.render("HAPPY BIRTHDAY!", True, (255, 255, 100))
        screen.blit(bday_txt, (LOGICAL_W//2 - bday_txt.get_width()//2, LOGICAL_H//2 - 60))
        end_txt = title_font.render("The End", True, WHITE)
        screen.blit(end_txt, (LOGICAL_W//2 - end_txt.get_width()//2, LOGICAL_H//2 + 40))

    # --- PROGRESS SCREENS ---
    if game_state == "intro_progress":
        draw_progress_screen(screen, "Progress: Entered Dungeon Floor 1...")
        next_state = "scene2"
    elif game_state == "fight_ready_progress":
        draw_progress_screen(screen, "Progress: Ascended middle floors. Nearing core...")
        next_state = "scene3"
    elif game_state == "boss_fight_progress":
        draw_progress_screen(screen, "Progress: Reached Final Chamber. Boss Fight Imminent...")
        next_state = "rps_fight"
    elif game_state == "win_progress":
        draw_progress_screen(screen, "You obtained the Elixir of Immortality!")
        next_state = "bday_end"

    # --- TAP PROMPT ---
    if game_state not in ["bday_end", "rps_fight"]:
        screen.blit(ui_font.render("(Tap anywhere to continue)", True, (150, 150, 150)), (LOGICAL_W - 250, LOGICAL_H - 85))

    # --- EVENT LISTENER ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            tap_pos = event.pos 
            
            if game_state in ["scene1", "scene3", "post_fight"]:
                source = unknown_voice_dialogue if game_state == "scene1" else (rudy_scene3_betrayal if game_state == "scene3" else rudy_post_fight)
                dialogue_idx += 1
                if dialogue_idx >= len(source):
                    game_state = next_state
                    dialogue_idx = 0 
                    
            elif game_state in ["intro_progress", "fight_ready_progress", "boss_fight_progress", "win_progress"]:
                game_state = next_state 
                    
            elif game_state == "scene2":
                if show_choices:
                    # INSTANT JUMP FIX
                    if choice_a_rect.collidepoint(tap_pos) or choice_b_rect.collidepoint(tap_pos):
                        dialogue_idx += 1
                        if dialogue_idx >= len(rudy_scene2_qa):
                            game_state = next_state
                            dialogue_idx = 0 
                else:
                    dialogue_idx += 1
                    if dialogue_idx >= len(rudy_scene2_qa):
                        game_state = next_state
                        dialogue_idx = 0 
            
            elif game_state == "rps_fight":
                if btn_rock.collidepoint(tap_pos) or btn_paper.collidepoint(tap_pos) or btn_scissors.collidepoint(tap_pos):
                    fight_message = f"Rigged! Cheat! Wait, you actually won? H-how?"
                    game_state = "post_fight"
                    dialogue_idx = 0 

    pygame.display.flip()

pygame.quit()
