import pygame, sys, time
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
police_titre = pygame.font.Font("assets/font/IndieFlower-Regular.ttf", 45) # CREER UNE POLICE 
police_principale = pygame.font.Font("assets/font/IndieFlower-Regular.ttf", 35)
police_nom =  pygame.font.Font("assets/font/IndieFlower-Regular.ttf", 35) # CHANGER LA POLICE D'AFFFICHAGE DES NOMS

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
    
    def idle(self):
        """
        """
        self.deplacer()

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
        self.copie_textes = self.textes.copy()

        if "jeu" in infos: 
            self.pnj_special = callable(infos["jeu"])
            if self.pnj_special:
                self.fonction_jeu = infos["jeu"]

        # DEPLACEMENTS ET POSITIONS
        self.rect.center = infos["position"]
        self.etat = "IDLE"
        
    def idle(self):
        """
        Cette methode accomplit toutes les actions que le PNJ doit pouvoir executer 
        en permanence si les conditions sont remplies
        """
        if self.rect.colliderect(JOUEUR.rect): # SI LE JOUEUR EST PROCHE DU PNJ
            if pygame.key.get_pressed()[K_SPACE] and self.etat != "DIALOGUE_EN_COURS": # LANCEMENT DU DIALOGUE
                self.etat = "DIALOGUE_EN_COURS"
                time.sleep(0.2)
                return
            
            if pygame.key.get_pressed()[K_SPACE] and self.etat == "DIALOGUE_EN_COURS": # SUITE DU DIALOGUE
                if self.copie_textes != []:
                    self.copie_textes.pop(0)
                time.sleep(0.2)
                return

            if self.etat == "DIALOGUE_EN_COURS": # AFFCICHAGE DU DIALOGUE
                if self.copie_textes == []:
                    self.copie_textes = self.textes.copy()
                    self.etat = "IDLE"
                    return
                bulle_info(self.copie_textes[0], self.nom, DISPLAYSURFACE)
                return
            
            return

        self.copie_textes = self.textes.copy()
        self.etat = "IDLE"
        
        
    def dialogue(self):
        pass

LISTE_ETATS = ["IDLE", "ATTENTE_CONFIRMATION_DIALOGUE", "DIALOGUE_EN_COURS"]

# ----------------------------- VARIABLES -----------------------------
# ------- LUTINS ET ASSETS -------
JOUEUR = Joueur() # LE JOUEUR

ELEVE_1 = Eleve({ # NOTRE PNJ 1
    "chemin_image": "assets/pnj/01.png",
    "nom": "Nom 1",
    "position": (120, 40),
    "textes": ["Salut !", "Bla bla bla bla bla bla bla bla bla bla bla bla ", "bla bla bla bla ", "bla bla bla bla bla "]
})

ELEVE_2 = Eleve({
    "chemin_image": "assets/pnj/02.png",
    "nom": "Nom 2",
    "position": (160, 50),
    "textes": ["125carLa vie est un voyage plein de surprises, il faut savoir apprécier chaque moment et saisir les opportunités qui se présentent"]
})

ELEVE_3 = Eleve({
    "chemin_image": "assets/pnj/03.png",
    "nom": "Nom 3",
    "position": (SCREEN_WIDTH//3, SCREEN_HEIGHT//2),
    "textes": ["ok"],
    # "jeu": 
})

all_sprites = pygame.sprite.Group() # GROUPE UTILISE POUR AFFICHER
all_sprites.add(ELEVE_1)
all_sprites.add(ELEVE_2)
all_sprites.add(ELEVE_3)

all_sprites.add(JOUEUR) # L'ORDRE D'AJOUT DES LUTINS DANS LE GROUPE INFLUE SUR
#LE PARCOURS DES VALEURS LORSQU'ON AFFICHE LES LUTINS, LE DERNIER LUTIN AJOUTE EST
#LE PLUS AU DESSUS, UN PEU COMME UN TAMPON

# ------- TEMPS -------
horloge_globale = pygame.time.get_ticks()

# ----------------------------- FONCTIONS -----------------------------

# ------- COLLISIONS -------

# ------- TEXTE -------
# !! AJOUTER UNE ANIMATION MACHINE A ECRIRE
def bulle_info(texte, nom, surface, choix=False):
    """
    """
    bulle = pygame.image.load("assets/bulle.png")
    liste_texte = []
    
    # AFFICHER LE NOM
    surface_nom = police_nom.render(nom, True, NOIR)
    surface.blit(surface_nom, (50, 370))
    
    # AFFICHER LA BULLE
    surface.blit(bulle, (50, 400))

    if choix:
        assert len(texte["texte"]) < 78, "Le texte est trop long pour être affiché en une fois (max 78car)"
    assert len(texte) < 131, "Le texte est trop long pour être affiché en une fois (max 130car)"

    # COUPER LE TEXTE
    while len(texte) > 26 * len(liste_texte) + 1:
        liste_texte.append(texte[0 + 26*len(liste_texte) : 26 + 26*len(liste_texte)])
    
    # AFFICHER LE TEXTE
    for i in range(len(liste_texte)):
        txt = liste_texte[i]
        surface_texte = police_principale.render(txt, True, NOIR)    
        
        surface.blit(surface_texte, (50, 400 + 30*i))
    return
    
def dialogue(liste_texte, index):
    """
    """
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

    # ----------------- AFFICHAGE -----------------
    # REPEINDRE L'ECRAN
    DISPLAYSURFACE.fill(BLANC)

    # AFFICHER CHAQUE ELEMENT ET EXECUTER LEURS ACTIONS
    for lutin in all_sprites:
        lutin.afficher(DISPLAYSURFACE)
        lutin.idle()

    # bulle_info("Test, dialogue de fouuuuuu lifoz fiejfezoi ufeoiz ufoiezufoiez ufoiezufioezuioezufi zoifuezoifeuoiz", DISPLAYSURFACE)

    # REAFFICHER L'ECRAN
    pygame.display.update()
    FramePerSec.tick(FPS)
