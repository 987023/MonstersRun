import pygame
import sys
import random
import os



# Janela de inicialização
pygame.init()  # Iniciar o pygame
LARGURA = 580
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # Fim
clock = pygame.time.Clock()

# Para acessar os assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Menu:
    def __init__(self, tela):
        self.fonte = None
        self.tela = tela
        #Imagem do fundo
        self.bg = pygame.image.load(os.path.join(BASE_DIR, "asset", "MenuBg.png"))
        self.bg = pygame.transform.scale(self.bg, (LARGURA, ALTURA))
        # Música do menu
        pygame.mixer.music.load(os.path.join(BASE_DIR, "asset", "Menu.mp3"))
        pygame.mixer.music.play(-1)


    def run(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE: # Entra no jogo
                    return "game"  # Vai para a fase
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.tela.blit(self.bg, (0, 0))
        fonte_titulo = pygame.font.SysFont("papyrus", 70)
        titulo = fonte_titulo.render("MONSTERS RUN", True, (255, 106, 0))
        rect_titulo = titulo.get_rect(center=(LARGURA // 2, ALTURA // 2 - 120))
        self.tela.blit(titulo, rect_titulo)

        self.fonte = pygame.font.SysFont("papyrus", 30)
        texto1 = self.fonte.render("PARA JOGAR PRESSIONE SPACE", True, (255, 106, 0))
        rect1 = texto1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 35))
        self.tela.blit(texto1, rect1)

        # Segundo texto
        self.fonte = pygame.font.SysFont("papyrus", 30)
        texto2 = self.fonte.render("DESVIE DOS OBJETOS USANDO AS SETAS", True, (255, 106, 0))
        rect2 = texto2.get_rect(center=(LARGURA // 2, ALTURA // 2 + 35))
        self.tela.blit(texto2, rect2)

        # Terceiro texto
        self.fonte = pygame.font.SysFont("papyrus", 23)
        texto3 = self.fonte.render("OBJETIVO: NÃO SER ATINGIDO!", True, (255, 106, 0))
        rect3 = texto3.get_rect(center=(LARGURA // 2, ALTURA // 2 + 52))
        self.tela.blit(texto3, rect3)
        return "menu"

  # Montando a classe do game
class Game:
    def __init__(self, tela) :
        self.tela = tela
        # Imagem do jogador
        self.jogador_img = pygame.image.load(os.path.join(BASE_DIR, "asset", "Player1.png"))
        self.jogador_img = pygame.transform.scale(self.jogador_img, (61, 61))

        # Imagem do objeto
        self.skull_img = pygame.image.load(os.path.join(BASE_DIR, "asset", "Icon.png"))
        self.skull_img = pygame.transform.scale(self.skull_img, (32, 32))
        self.jogador = pygame.Rect(LARGURA // 2 - 25, ALTURA - 80, 50, 50)
        self.skulls = []
        self.velocidade = 5
        self.fonte = pygame.font.SysFont(None, 40)
        self.tempo_inicio = pygame.time.get_ticks()

        # Imagem do fundo do game - Level 1
        self.bg = pygame.image.load(os.path.join(BASE_DIR, "asset", "Level1Bg.png"))
        self.bg = pygame.transform.scale(self.bg, (LARGURA, ALTURA))
        self.tempo_inicio = pygame.time.get_ticks()

        # Música do Level 1
        pygame.mixer.music.load(os.path.join(BASE_DIR, "asset", "Level1.mp3"))
        pygame.mixer.music.play(-1)

    def criar_skull(self): # Objetos do jogo
        x = random.randint(0, LARGURA - 40)
        skull = pygame.Rect(x, -40, 40, 40)
        self.skulls.append(skull)

    def run(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "menu"

        # Movimentos do jogador - setas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.jogador.left > 0:
            self.jogador.x -= 7
        if teclas[pygame.K_RIGHT] and self.jogador.right < LARGURA:
            self.jogador.x += 7

        # Criar objetos aleatórios que caem
        if random.randint(1, 30) == 1:
            self.criar_skull()

        # Atualizar os objetos
        for skull in self.skulls[:]:
            skull.y += self.velocidade
            if skull.colliderect(self.jogador):
                return "menu"
            if skull.top > ALTURA:
                self.skulls.remove(skull)

        # Calculo da pontuação de tempo
        tempo = (pygame.time.get_ticks() - self.tempo_inicio) // 1000

        # Desenho do game
        self.tela.blit(self.bg, (0, 0))
        self.tela.blit(self.jogador_img, (self.jogador.x, self.jogador.y))
        for skull in self.skulls:
            self.tela.blit(self.skull_img, (skull.x, skull.y))
        texto = self.fonte.render(f"Time: {tempo}", True, (0, 255, 80))
        self.tela.blit(texto, (10, 10))

        return "game"


# Loop principal
menu = Menu(TELA)
game = None
opcao = "menu"

while True:
    clock.tick(60)

    if opcao == "menu":
        opcao = menu.run()

        if opcao == "game":
            pygame.mixer.music.stop()
            game = Game(TELA)

    elif opcao == "game":
        opcao = game.run()

        if opcao == "menu":
            pygame.mixer.music.stop()
            menu = Menu(TELA)

    pygame.display.update()
