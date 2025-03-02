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
class Lutin(pygame.sprite.Sprite):
    """
    Cette classe regroupe toutes les méthodes communes à tout les lutins (en plus de donner 
    donner accès aux méthodes de la classe Sprite de pygame).
    """
    def __init__(self):
        super().__init__()
    
    def afficher(self, surface):
        """
        Affiche l'élément sur la surface donnée en paramètre
        pre: surface (SURFACE)
        post:
        """
        surface.blit(self.image, self.rect) 

class Joueur(Lutin):
    def __init__(self):
        super().__init__()

        # CHARGEMENT DE L'IMAGE
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()

        # DEPLACEMENTS ET POSITIONS
        self.rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2) # POSTITION DE DEPART
        self.delta_x = 4
        self.delta_y = 4
    
    def deplacer(self):
        """
        Permet le deplacement de la boite
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            if self.rect.left > 0:
                self.rect.move_ip(-1*self.delta_x, 0)

        if pressed_keys[K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH:
                self.rect.move_ip(self.delta_x, 0)

        if pressed_keys[K_UP]:
            if self.rect.center[1] > 0:
                self.rect.move_ip(0, -1*self.delta_y)
        
        if pressed_keys[K_DOWN]:
            if self.rect.bottom < SCREEN_HEIGHT :
                self.rect.move_ip(0, self.delta_y)

class Eleve(Lutin):
    def __init__(self, infos):
        """
        Structure du dictionnaire contenant les informations du pnj:
        {
            "chemin_image": (str)
            "nom": (str),
            "position": (tuple)
            "textes": (list)
            "jeu": (?) # (lambda / class / fonction)
            "": , # Et si on ajoutait des récompenses ????
        }
        """
        super().__init__()

        # CHARGEMENT DE L'IMAGE
        self.image = pygame.image.load(infos["chemin_image"])
        self.rect = self.image.get_rect()

        # INFOS PERSO
        self.infos_dict = infos
        self.nom = infos["nom"]
        self.textes = infos["textes"]

        if "jeu" in infos: 
            self.pnj_special = callable(infos["jeu"])
            if self.pnj_special:
                self.fonction_jeu = infos["jeu"]

        # DEPLACEMENTS ET POSITIONS
        self.rect.center = infos["position"]

# ----------------------------- VARIABLES -----------------------------
# ------- LUTINS ET ASSETS -------
JOUEUR = Joueur() # LE JOUEUR
ELEVE_1 = Eleve({
    "chemin_image": "assets/pnj.png",
    "nom": "Bob",
    "position": (120, 40),
    "textes": ["Salut !", "Tu veux jouer ?"]
})

all_sprites = pygame.sprite.Group() # GROUPE UTILISE POUR AFFICHER
all_sprites.add(ELEVE_1)

all_sprites.add(JOUEUR) # L'ORDRE D'AJOUT DES LUTINS DANS LE GROUPE INFLUE SUR
#LE PARCOURS DES VALEURS LORSQU'ON AFFICHE LES LUTINS, LE DERNIER LUTIN AJOUTE EST
#LE PLUS AU DESSUS, UN PEU COMME UN TAMPON

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
