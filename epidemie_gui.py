import pygame
import os; os.chdir(r'C:\path')
from epidemie_functions import *

pygame.init()

###INIT BEGIN###
gameOver, gameEnded = False, False

#Window Parameters
displayWidth = 800
bordure = 50
dot_size = 2.5

#Gameplay parameters
fps = 30
n = 100 #This will draw a square-grid of size n
p1 = .5
p2 =.4

#Colours Definition
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (50, 50, 255)
grey = (100, 100, 130)
###INIT END###
displayHeight = displayWidth

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('= Epid. Sim.=')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

centers_grid = grille(n)
G = init(n)
x_atteinte = 0
compteur = 0

lg_grille = displayWidth - 2*(displayWidth /bordure)
#Cases centers computing
lg_case = lg_grille / n

for i in range(n):
    for j in range(n):
        if j==0:
            x = displayWidth/ bordure + lg_case/2
            y = displayHeight/bordure + lg_case/2 + lg_case * i
            centers_grid[i][j]=(round(x), round(y))
        else:
            x = x + lg_case
            centers_grid[i][j]=(round(x), round(y))

def get_suivant(G):
    '''compte_ = compte(G)
    if compte_[1] == 1 and compte_[2] == 0 and compte_[3] == 0:
        
        return G'''

    return suivant(G, p1, p2)
    
def display_grid(G):
    for i in range(n):
        for j in range(n):
            if G[i][j] == 0:
                pygame.draw.circle(gameDisplay, green, (centers_grid[i][j][0], centers_grid[i][j][1]), round(lg_case/dot_size), 0)
            elif G[i][j] == 1:
                pygame.draw.circle(gameDisplay, red, (centers_grid[i][j][0], centers_grid[i][j][1]), round(lg_case/dot_size), 0)
            elif G[i][j] == 2:
                pygame.draw.circle(gameDisplay, white, (centers_grid[i][j][0], centers_grid[i][j][1]), round(lg_case/dot_size), 0)
            elif G[i][j] == 3:
                pygame.draw.circle(gameDisplay, black, (centers_grid[i][j][0], centers_grid[i][j][1]), round(lg_case/dot_size), 0)

while not gameOver:
    while not gameEnded:
        gameDisplay.fill(black)
        compteur +=1
        
        ##Events handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                gameOver, gameEnded = True, True
            
        ##Displaying
        #Scenery
        pygame.draw.line(gameDisplay, grey, (displayWidth / bordure, displayHeight / bordure), (displayWidth / bordure, displayHeight *(bordure-1) /bordure), 3)
        pygame.draw.line(gameDisplay, grey, (displayWidth*(bordure-1) /bordure, displayHeight/ bordure), (displayWidth *(bordure-1) /bordure, displayHeight *(bordure-1) /bordure),3)
        pygame.draw.line(gameDisplay, grey, (displayWidth / bordure, displayHeight / bordure), (displayWidth*(bordure-1) /bordure, displayHeight / bordure), 3)
        pygame.draw.line(gameDisplay, grey, (displayWidth/bordure, displayHeight*(bordure-1) /bordure), (displayWidth *(bordure-1) /bordure, displayHeight *(bordure-1) /bordure), 3)
        
        for i in range(n-1):
            i+=1
            pygame.draw.line(gameDisplay, grey, ((lg_grille/n*i) + displayWidth/bordure, displayHeight / bordure), ((lg_grille/n*i) + displayWidth/bordure, displayHeight*(bordure-1) /bordure), 2)
            pygame.draw.line(gameDisplay, grey, (displayWidth / bordure, (lg_grille/n*i) + displayWidth/bordure), (displayWidth*(bordure-1) /bordure, (lg_grille/n*i) + displayWidth/bordure), 2)
            
        G = get_suivant(G)
        display_grid(G)
        
        compte_list = compte(G)
        if compte_list[1] == 0:gameEnded = True
        x_atteinte =  compte_list[1] + compte_list[2] + compte_list[3]
        
        pygame.display.set_caption('= Epid. Sim.= Pop size: {} || Sain: {} | Inf: {} | Retab: {} | Decede: {} || Prog: {} lap(s) | Reached: {}'.format(n**2, compte_list[0], compte_list[1], compte_list[2], compte_list[3], compteur, x_atteinte))
        
        pygame.display.update()
        clock.tick(fps)

    pandemie = x_atteinte / n**2 > .5
    pand_tx = round(x_atteinte / n**2, 2)
    
    if pandemie:
        pygame.display.set_caption('= Epid. Sim.= Pop size: {} ||Sain: {} |Inf: {} |Retab: {} |Decede: {} ||Comp: {} lap(s) |Reached: {} | /!\ {}'.format(n**2, compte_list[0], compte_list[1], compte_list[2], compte_list[3], compteur, x_atteinte, pand_tx))
    else:
        pygame.display.set_caption('= Epid. Sim.= Pop size: {} || Sain: {} | Inf: {} | Retab: {} | Decede: {} || Comp: {} lap(s) | Reached: {}'.format(n**2, compte_list[0], compte_list[1], compte_list[2], compte_list[3], compteur, x_atteinte))
                
    print(compte(G)); print(pand_tx)
    
    while not gameOver:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                gameOver = True

pygame.quit()
