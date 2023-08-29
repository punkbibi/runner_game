import pygame
import random
import pickle
import os


def enemy_movement(enemy_list):
    global enemy_speed_factor
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5 * enemy_speed_factor
            if enemy_rect.bottom == 335: screen.blit(ground_enemy_surf,enemy_rect)
            else: screen.blit(bird_surf, enemy_rect)
        return  [enemy for enemy in enemy_list if enemy.right > -100]
    else: return []

def collisions(player, enemies):
    global score, highest_score, enemy_speed_factor
    if enemies:
        for enemy_rect in enemies:
            if player.colliderect(enemy_rect):
                enemy_speed_factor = 1
                if score > highest_score:
                    highest_score = score
                    save_highest_score(highest_score)  
                return 2
    return 1

def update_score(added_score, enemy_list, player):
    global score, enemy_speed_factor
    for enemy in enemy_list:
        if abs(player.centerx - enemy.centerx) <= 2:
            score += added_score
            if score % 10 == 0:  
                enemy_speed_factor += 0.2

def player_animation():
    global player_surf, player_index, draw_pos, player_rect
    if player_rect.bottom <= 312:
        draw_pos = (player_rect.x - 1, player_rect.y - 9)
        player_surf = jump_surf
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

def save_highest_score(score):
    with open("highest_score.pkl", "wb") as f:
        pickle.dump(score, f)

def read_highest_score():
    if os.path.exists("highest_score.pkl"):
        with open("highest_score.pkl", "rb") as f:
            return pickle.load(f)
    return 0


pygame.init()
screen = pygame.display.set_mode((798,398))
pygame.display.set_caption('runner pppy')
# icon
icon_surf = pygame.image.load("pekingese.png")
pygame.display.set_icon(icon_surf)


clock = pygame.time.Clock()
text_font = pygame.font.Font('ARCADECLASSIC.TTF', 25)


# surfaces
ground_surf = pygame.image.load('ground.jpg').convert()

player_walk_1 = pygame.image.load('dog_1.png').convert_alpha()
player_walk_2 = pygame.image.load('dog_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
jump_surf = pygame.image.load('jump.png').convert_alpha()
player_index = 0
player_surf = player_walk[player_index]

ground_enemy_surf = pygame.image.load('death.png').convert_alpha()

bird_1 = pygame.image.load('bird_1.png').convert_alpha()
bird_2 = pygame.image.load('bird_2.png').convert_alpha()
bird_list = [bird_1, bird_2]
bird_index = 0
bird_surf = bird_list[bird_index]

welcome_text_surf = text_font.render('welcome', True, 'black')
text_surface = pygame.transform.scale2x(text_font.render('press    space    to    start', True,'black'))


# rectangles
player_rect  = player_surf.get_rect(midbottom = (132,312))
welcome_text_rect = welcome_text_surf.get_rect(center = (399, 20))
text_rect = text_surface.get_rect(center = (399,350))

enemy_rect_list = []

# variables
base_speed = 900
enemy_speed_factor = 1
gravity = 0
game_activ = 0
score = 0
jump = 2
highest_score = read_highest_score()

# timers
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, base_speed)

bird_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(bird_animation_timer, 200)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:pygame.quit()
             
        # main event
        if game_activ == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and  jump>0:
                    jump -= 1 
                    gravity = -15
                    
            if event.type == enemy_timer:
                if random.randint(0,1):
                    enemy_rect_list.append(ground_enemy_surf.get_rect(midbottom= (random.randint(900,1000),335)))
                else:
                    enemy_rect_list.append(bird_surf.get_rect(midbottom= (random.randint(900,1000),random.randint(150,330))))
            if event.type == bird_animation_timer:
                if bird_index == 0: bird_index = 1
                else: bird_index = 0
                bird_surf = bird_list[bird_index]
                
        #end/start screen    
        if game_activ == 0 or game_activ == 2:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                score = 0
                game_activ = 1
                
                        
    # main event
    if game_activ == 1:             
        gravity += 1
        player_rect.y += gravity 
        if player_rect.y >= 312:
            player_rect.y = 312
            jump = 2 
        
        screen.blit(ground_surf,(0,0))
        draw_pos = player_rect
        player_animation()
        screen.blit(player_surf, draw_pos)
        
        # enemy movement
        enemy_rect_list = enemy_movement(enemy_rect_list)
        
        # socre
        update_score(1, enemy_rect_list,player_rect)
        screen.blit(text_font.render(f'score {score}', False, "black"), (359, 10))
        
        #checking lose condition 
        game_activ = collisions(player_rect, enemy_rect_list)
                   
    # start screen    
    if game_activ == 0:
        screen.fill('green')
        screen.blit(text_surface, text_rect)
        screen.blit(welcome_text_surf,welcome_text_rect)
        enemy_rect_list.clear()
        
    # end screen
    elif game_activ == 2:
        screen.fill("#1D5B79")
        screen.blit(text_font.render(f'highest score   {highest_score}', True, "#FE0000"), (280, 100))
        screen.blit(text_font.render(f'current score   {score}', False, "#FE0000"), (290, 220))
        enemy_rect_list.clear()
        
        
    pygame.display.update()
    
    clock.tick(60)