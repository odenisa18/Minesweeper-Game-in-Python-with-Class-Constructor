import pygame
import sys
from game import Game

# afisarea textului pe ecran
def draw_text(screen, text, font, color, rect, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2
    font_height = font.size("Tg")[1]
    lines = text.split('\n')
    
    for line in lines:
         # atata timp cat mai exista text în linie
        while line:
            i = 1
             # verifica daca urmatoarea linie va depasi partea de jos a dreptunghiului
            if y + font_height > rect.bottom:
                break
            # creste i pana cand latimea textului este mai mica decat latimea dreptunghiului sau pana la sfarsitul liniei
            while font.size(line[:i])[0] < rect.width and i < len(line):
                i += 1
                 # daca linia este prea lunga, gaseste ultimul spatiu pentru a imparti linia
            if i < len(line):
                i = line.rfind(" ", 0, i) + 1
                  # deseneaza textul pe un fundal daca este specificat
            if bkg:
                image = font.render(line[:i], 1, color, bkg)
                image.set_colorkey(bkg)
                   # deseneaza textul fara fundal daca nu este specificat
            else:
                image = font.render(line[:i], aa, color)
            # afisează textul pe ecran la pozitia specificata
            screen.blit(image, (rect.left, y))
            y += font_height + line_spacing
            line = line[i:]
        y += font_height
    return text

# afisez informatiile de joc pe ecran in meniul INFO
def display_info(screen, font):
    info_text = (
        "Game Instructions:\n"
        "- Use arrow keys to navigate the menu.\n"
        "- Press Enter to select an option.\n"
        "- Set an alias before starting the game.\n"
        "- Select difficulty to adjust game settings.\n"
        "- Start the game to play."
    )
    # apelez pur si simplu FUNCTIA DE AFISARE TEXT
    draw_text(screen, info_text, font, (255, 255, 255), pygame.Rect(100, 100, 600, 400))

# afisarea meniului info
def info_menu(screen, font):
    while True:
        screen.fill((0, 0, 0))
        display_info(screen, font)
        draw_text(screen, "Back", font, (255, 255, 255), pygame.Rect(100, 500, 600, 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 # inchide Pygame
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # iese din program
                if event.key == pygame.K_RETURN:
                    return
                #actualizeaza ecranul! pt a arata noile modificari
        pygame.display.flip()

# afisez un mesaj de avertizare pe ecran
def draw_warning(screen, font, message):
    shadow_color = (50, 50, 50)
    #creez un dreptunghi pentru umbra pe ecran
    shadow_rect = pygame.Rect(205, 205, 390, 190)
    pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)
    # culoarea casetei de mesaj ROSIE
    box_color = (255, 0, 0)
    box_rect = pygame.Rect(200, 200, 400, 200)
    # creez un dreptunghi pentru caseta de mesaj cu poz/dim
    pygame.draw.rect(screen, box_color, box_rect, border_radius=10)
    draw_text(screen, message, font, (255, 255, 255), pygame.Rect(220, 220, 360, 140))
    button_color = (255, 255, 255)
    button_rect = pygame.Rect(360, 340, 80, 40)
    # cu colturi rotunjite
    pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
    draw_text(screen, "OK", font, (0, 0, 0), pygame.Rect(370, 350, 60, 30))

def draw_confirmation(screen, font, message):
    shadow_color = (50, 50, 50)
    shadow_rect = pygame.Rect(155, 205, 490, 190)
    pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)
    
    box_color = (255, 0, 0)
    box_rect = pygame.Rect(150, 200, 500, 200)
    pygame.draw.rect(screen, box_color, box_rect, border_radius=10)
    
    draw_text(screen, message, font, (255, 255, 255), pygame.Rect(170, 220, 460, 140))
    
    button_yes_rect = pygame.Rect(270, 340, 80, 40)
    pygame.draw.rect(screen, (255, 255, 255), button_yes_rect, border_radius=5)
    draw_text(screen, "Yes", font, (0, 0, 0), pygame.Rect(280, 350, 60, 30))
    
    button_no_rect = pygame.Rect(450, 340, 80, 40)
    pygame.draw.rect(screen, (255, 255, 255), button_no_rect, border_radius=5)
    draw_text(screen, "No", font, (0, 0, 0), pygame.Rect(460, 350, 60, 30))
    
    return button_yes_rect, button_no_rect


# main function: pt meniul de start
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Main Menu")
    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 35)
    background = pygame.image.load("path_to_main_background_image.jpg")
    background = pygame.transform.scale(background, (900, 600))
    
    alias = ""
    difficulty = "Easy"
    selected_option = 0
    options = ["Alias: ", "Difficulty: Easy", "Info", "Start Game", "Exit"]
    alias_input_active = False
    show_warning = False
    show_confirmation = False
    size, prob = (9, 9), 0.1
    
    while True:
        screen.blit(background, (0, 0))
        for i, option in enumerate(options):
            display_text = option + alias if option.startswith("Alias: ") else option
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            draw_text(screen, display_text, font, color, pygame.Rect(100, 100 + i * 100, 600, 50))
        
        if show_warning:
            draw_warning(screen, small_font, "Alias is required to start the game.")
        
        if show_confirmation:
            button_yes, button_no = draw_confirmation(screen, small_font, "Do you really want to leave the game?")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if alias_input_active:
                    if event.key == pygame.K_RETURN:
                        alias_input_active = False
                        options[0] = f"Alias: "
                    elif event.key == pygame.K_BACKSPACE:
                        alias = alias[:-1]
                    else:
                        alias += event.unicode
                elif show_confirmation:
                    if event.key == pygame.K_RETURN:
                        show_confirmation = False
                        if event.key == pygame.K_RETURN:
                            pygame.quit()
                            sys.exit()
                else:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if show_warning:
                            show_warning = False
                        else:
                            if options[selected_option].startswith("Alias"):
                                alias_input_active = True
                                alias = ""
                            elif options[selected_option].startswith("Difficulty"):
                                if difficulty == "Easy":
                                    difficulty = "Medium"
                                    size, prob = (13, 13), 0.15
                                elif difficulty == "Medium":
                                    difficulty = "Hard"
                                    size, prob = (16, 16), 0.20
                                else:
                                    difficulty = "Easy"
                                    size, prob = (9, 9), 0.1
                                options[1] = f"Difficulty: {difficulty}"
                            elif options[selected_option] == "Info":
                                info_menu(screen, small_font)
                            elif options[selected_option] == "Start Game":
                                if alias:
                                    result = "play_again"
                                    while result == "play_again":
                                        g = Game(size, prob)
                                        g.run()
                                        result = g.show_end_menu()
                                        if result == "main_menu":
                                            return main_menu()
                                        elif result == "quit":
                                            pygame.quit()
                                            sys.exit()
                                else:
                                    show_warning = True
                            elif options[selected_option] == "Exit":
                                show_confirmation = True
            
            if event.type == pygame.MOUSEBUTTONDOWN and show_confirmation:
                mouse_pos = event.pos
                if button_yes.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif button_no.collidepoint(mouse_pos):
                    show_confirmation = False
        
        pygame.display.flip()

if __name__ == '__main__':
    main_menu()
