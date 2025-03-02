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
police_titre = pygame.font.Font("DeliciousHandrawn-Regular.ttf", 45) # CREER UNE POLICE 
police_principale = pygame.font.Font("DeliciousHandrawn-Regular.ttf", 35)

# INFOS ECRAN
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # SURFACE DE JEU
DISPLAYSURFACE.fill(BLANC)
pygame.display.set_caption("Meg")


# ----------------------------- CLASSES -----------------------------
class Boite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # CHARGEMENT DE L'IMAGE
        self.image = pygame.image.load("box.png")
        self.rect = self.image.get_rect()

        # DEPLACEMENTS ET POSITIONS
        self.rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2)

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
            if self.rect.center == self.droite: # SI LA BOITE EST A GAUCHE
                self.rect.center = self.gauche

        if pressed_keys[K_RIGHT]:
            if self.rect.center == self.gauche:
                self.rect.center = self.droite
                    


# ----------------------------- VARIABLES -----------------------------
# ------- LUTINS ET ASSETS -------
all_sprites = pygame.sprite.Group() # GROUPE UTILISE POUR AFFICHER

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

    # ----------------- QUITTER JEU -----------------
    
    # SI APPUI SUR LA CROIX
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

    # QUITTE LE JEU SI APPUI SUR ESC
    if pygame.key.get_pressed()[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # ----------------- JEU -----------------


    # ----------------- AFFICHAGE -----------------

    # REPEINDRE L'ECRAN
    DISPLAYSURFACE.fill(BLANC)

    # AFFICHER CHAQUE ELEMENT
    for lutin in all_sprites:
        lutin.afficher(DISPLAYSURFACE)

    # REAFFICHER L'ECRAN
    pygame.display.update()
    FramePerSec.tick(FPS)

play()