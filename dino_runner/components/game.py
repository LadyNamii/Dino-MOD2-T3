import pygame

 

from dino_runner.utils.constants import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.powerups.power_up_manager import PowerUpManager


BUTTON_WITDH_PLAY = 800
BUTTON_HEIGHT_PLAY = 400

WITDH_TEXT = 0    #mexe na horizontal
HEIGHT_TEXT = 50  #mexe na vertical

class Game:                            #metodos de executar , lida com ev entos , atualiza elementos  do jogo
    def __init__(self) :            #desenha e exibe o menu na tela
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0 
        self.death_count = 0
        self.game_speed = 20 
        self.x_pos_bg = 0 
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
       
        
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                
                self.show_menu()
        pygame.display.quit()
        pygame.quit() 
        
    def run (self):
        self.playing = True
        self.obstacle_manager.reset_obstacles() 
        self.power_up_manager.reset_power_ups()
        self.game_speed = 20 
        self.score = 0 
        while self.playing:
            self.events()
            self.update() 
            self.draw()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
    
    def update(self):
        user_input = pygame.key.get_pressed() 
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score,self.game_speed, self.player)   
        
    def update_score(self):
        self.score += 1
        if self.score % 100 == 0 :
            self.game_speed += 5
            
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255,255,255))
        self.screen.blit(IMAGEM_FUNDO, (0,0))
        self.draw_background() 
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score ()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
                                    #desenha o fundo em movimento
    def draw_background(self):   #ilusão de movimento
        image_width =BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG,(image_width + self.x_pos_bg, self.y_pos_bg)) 
        if self.x_pos_bg <= - image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg  -= 2
            
    def draw_score(self):
        draw_message_component(
         f"PONTUAÇÃO :{self.score}",
         self.screen,
         pos_x_center = 1000,
         pos_y_center= 50  
        )
        
    def draw_power_up_time(self): 
       if self.player.has_power_up:             # tempo atual do que o tempo  power up foi ativo
           time_to_show = round ((self.player.power_up_time - pygame.time.get_ticks())/ 1000,2) 
           if time_to_show >= 0:
               draw_message_component(
                   f"{self.player.type.capitalize()} FALTAM {time_to_show} SEGUNDOS",
                   self.screen,
                   font_size= 18,
                   pos_x_center= 500,
                   pos_y_center= 40
               )
           else:
               self.player.has_power_up = False
               self.player.type = DEFAULT_TYPE
               
    def handle_events_on_menu(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.run()
            pygame.display.flip()  #Após processar os eventos, o código atualiza a tela do jogo 
     
            
    def show_menu(self):
        
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        color = (255,255,255)  
        color_light = (170,170,170)  
        color_dark = (100,100,100)  
        
        smallfont = pygame.font.SysFont('exo',60) 
        smallfont2 = pygame.font.SysFont('Roboto',30)  
        text = smallfont2.render('BEM VINDOO AO MELHOR JOGO DE CORRIDA DOS ULTIMOS TEMPOS \n CLICK NO START  PARA COMEÇAR!' , True , color )
         # Renderizar = criar uma imagem /texto que será exibida na tela.
         
        print(f"show menu {self.death_count}")  
        if self.death_count == 0:
            test = True
            
            while test:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        
                        
                    if ev.type == pygame.MOUSEBUTTONDOWN:# verifica se ocorreu um evento de clique do mouse.
                              # verifica se o cursor do mouse está dentro das coordenadas do botão "PLAY"
                        if BUTTON_WITDH_PLAY / 2 <= mouse[0] <= BUTTON_WITDH_PLAY / 2 + 140 and BUTTON_HEIGHT_PLAY / 2 <= mouse[1] <= BUTTON_HEIGHT_PLAY / 2 + 40:
                            self.run()
                            test = False
                    self.screen.fill((60, 25, 60))
                    mouse = pygame.mouse.get_pos() 
                    # permite  saber onde o mouse está localizado na tela.
                    
                  
  
              
                if BUTTON_WITDH_PLAY / 2 <= mouse[0] <= BUTTON_WITDH_PLAY / 2 + 140 and BUTTON_HEIGHT_PLAY / 2 <= mouse[1] <= BUTTON_HEIGHT_PLAY / 2 + 40:
                    pygame.draw.rect(self.screen, color_light, [BUTTON_WITDH_PLAY / 2, BUTTON_HEIGHT_PLAY / 2, 190, 90])
                #ajusta a cor do retângulo com base na posição do mouse
                else:
                    pygame.draw.rect(self.screen, color_dark, [BUTTON_WITDH_PLAY / 2, BUTTON_HEIGHT_PLAY / 2, 190, 90])

                    #elementos visuais na tela
                    # posição  onde quer desenhar a imagem play na tela                    
                self.screen.blit(START, (BUTTON_WITDH_PLAY / 2 + 1, BUTTON_HEIGHT_PLAY / 2))
                self.screen.blit(text, (WITDH_TEXT / 2 + 40, HEIGHT_TEXT / 2))
                   
                pygame.display.update()
                pygame.display.flip()  #atualiza a tela
        else:
                                    
            draw_message_component(
                "Aperte qualquer tecla para reiniciar",
                self.screen,
                font_size= 24,
                pos_x_center= half_screen_width,
                pos_y_center= half_screen_height - 200
            )
            draw_message_component(
                f"SUA PONTUAÇÃO: {self.score}",
                self.screen,
                pos_y_center= half_screen_width
            )
            self.screen.blit(ICON, (half_screen_width - (ICON.get_width()/2), half_screen_height-100))      
            self.handle_events_on_menu()
        
        
       
                        
 
    

      
        
        