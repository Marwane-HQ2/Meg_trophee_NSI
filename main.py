import pygame, sys
from pygame.locals import * # ici il y a vraiment toutes les touches genre espace ou flèches directionnelles, pas mal

# ----------------------------- PARAMETRAGES DU JEU -----------------------------
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# COULEURS PREDEFINIES
BLEU  = (0, 0, 255)
ROUGE   = (255, 0, 0)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)

# TEXTE 
police_titre = pygame.font.Font("IndieFlower-Regular.ttf", 45) # CREER UNE POLICE 
police_principale = pygame.font.Font("IndieFlower-Regular.ttf", 35)

# INFOS ECRAN
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # SURFACE DE JEU
DISPLAYSURFACE.fill(BLANC)
pygame.display.set_caption("Meg")


# ----------------------------- CLASSES -----------------------------
class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # CHARGEMENT DE L'IMAGE
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()

        # DEPLACEMENTS ET POSITIONS
        self.rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2) # POSTITION DE DEPART
        self.delta_x = 4
        self.delta_y = 4

    def afficher(self, surface):
        """
        Affiche l'élément sur la surface donnée en paramètre
        pre: surface (SURFACE)
        post:
        """
        surface.blit(self.image, self.rect) 
    
    def deplacer(self):
        """
        Permet le deplacement de la boite
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            if self.rect.left > 0: # SI LA BOITE EST A GAUCHE
                self.rect.move_ip(-1*self.delta_x, 0)

        if pressed_keys[K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH:
                self.rect.move_ip(self.delta_x, 0)

        if pressed_keys[K_UP]:
            if self.rect.top > 0:
                self.rect.move_ip(0, -1*self.delta_y)
        
        if pressed_keys[K_DOWN]:
            if self.rect.bottom < SCREEN_HEIGHT :
                self.rect.move_ip(0, self.delta_y)


# ----------------------------- VARIABLES -----------------------------
# ------- LUTINS ET ASSETS -------
JOUEUR = Joueur() # LE JOUEUR

all_sprites = pygame.sprite.Group() # GROUPE UTILISE POUR AFFICHER
all_sprites.add(JOUEUR)

# ------- TEMPS -------
horloge_globale = pygame.time.get_ticks()

# ----------------------------- FONCTIONS -----------------------------

# ------- COLLISIONS -------

# ------- TEXTE -------
def bulle_info(texte):
    pass

# ------- JEU ------- 

# ----------------------------- BOUCLE DU JEU -----------------------------
while True:
    # OBTENIR L'HEURE QU'IL EST A CHAQUE ITERATION
    heure = pygame.time.get_ticks()

    # ----------------- GESTION DES EVENNEMENTS-----------------    
    for event in pygame.event.get():              
        if event.type == QUIT: # SI APPUI SUR LA CROIX
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN: # AFFICHER LA POSITION DU CURSEUR QUAND ON CLIQUE. 
            print(pygame.mouse.get_pos())

    # QUITTE LE JEU SI APPUI SUR ESC
    if pygame.key.get_pressed()[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # ----------------- JEU -----------------
    # PERMETTRE LE DEPLACEMENT DU JOUEUR
    JOUEUR.deplacer()

    # ----------------- AFFICHAGE -----------------
    # REPEINDRE L'ECRAN
    DISPLAYSURFACE.fill(BLANC)

    # AFFICHER CHAQUE ELEMENT
    for lutin in all_sprites:
        lutin.afficher(DISPLAYSURFACE)

    # REAFFICHER L'ECRAN
    pygame.display.update()
    FramePerSec.tick(FPS)
