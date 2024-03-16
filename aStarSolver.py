import pygame
import random

class State:

    def __init__(self, position, parent):
        self.position = position
        self.score = self.computeScore()
        self.parent = parent
    
    def computeScore(self):
        return ((abs(58-self.position[0]))**2 + (abs(58-self.position[1]))**2)**0.5

def loadMaze(file):
    maze = []
    file = open(file, "r")
    for line in file:
        row = []
        for char in line:
            if char != "\n":
                row.append(int(char))
        maze.append(row)
    file.close()
    return maze

def drawMaze(maze, screen):
    # color the maze
    for y in range(60):
        for x in range(60):
            if maze[y][x] == 0:
                # draw black square
                pygame.draw.rect(screen, (0,0,0), (x*10, y*10, 10, 10))
            elif maze[y][x] == 1:
                # draw green square
                pygame.draw.rect(screen, (0,255,0), (x*10, y*10, 10, 10))
            elif maze[y][x] == 2:
                # draw red square
                pygame.draw.rect(screen, (255,0,0), (x*10, y*10, 10, 10))
            else:
                # draw white square
                pygame.draw.rect(screen, (255,255,255), (x*10, y*10, 10, 10))

def drawPath(state, screen):
    while state.parent != None:
        pygame.draw.rect(screen, (0,0,255), (state.position[0]*10, state.position[1]*10, 10, 10))
        state = state.parent
    pygame.display.flip()

def saveMaze(state, maze):
    # in image
    image = pygame.Surface((600,600))

    for y in range(60):
        for x in range(60):
            if maze[y][x] == 0:
                # draw black square
                pygame.draw.rect(image, (0,0,0), (x*10, y*10, 10, 10))
            elif maze[y][x] == 1:
                # draw green square
                pygame.draw.rect(image, (0,255,0), (x*10, y*10, 10, 10))
            elif maze[y][x] == 2:
                # draw red square
                pygame.draw.rect(image, (255,0,0), (x*10, y*10, 10, 10))
            else:
                # draw white square
                pygame.draw.rect(image, (255,255,255), (x*10, y*10, 10, 10))
    
    while state.parent != None:
        pygame.draw.rect(image, (0,0,255), (state.position[0]*10, state.position[1]*10, 10, 10))
        state = state.parent
    
    pygame.image.save(image, "mazeSolve.png")

def drawState(state, screen):
    while state.parent != None:
        pygame.draw.rect(screen, (0,0,255), (state.position[0]*10, state.position[1]*10, 10, 10))
        state = state.parent



# --- Main --

# Initialize the game engine
pygame.init()

screen = pygame.display.set_mode((600,600))

pygame.display.set_caption("Maze Runner")

maze = loadMaze("maze.txt")

bagStates = []
stateVisited = []
bagStates.append(State([1,1], None))

loop = True
while loop:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        

    while len(bagStates) != 0:

        # slow down the monster
        pygame.time.wait(10)

        # draw the maze
        drawMaze(maze, screen)

        # sort the bag by score
        bagStates.sort(key=lambda x: x.score)

        # take the smaller score
        state = bagStates.pop(0)

        # draw the state
        drawState(state, screen)

        # update the screen
        pygame.display.flip()

        # if the state is the end
        if maze[state.position[1]][state.position[0]] == 2:
            # draw the path
            drawPath(state, screen)
            saveMaze(state, maze)
            break

        # if the state is not the end
        else:

            stateVisited.append(state.position)

            # add the neighbors to the bag
            
            # up
            if maze[state.position[1]-1][state.position[0]] != 0:
                # check if the state is not visited
                if [state.position[0], state.position[1]-1] not in stateVisited:
                    bagStates.append(State([state.position[0], state.position[1]-1], state))
            
            # down
            if maze[state.position[1]+1][state.position[0]] != 0:
                # check if the state is not visited
                if [state.position[0], state.position[1]+1] not in stateVisited:
                    bagStates.append(State([state.position[0], state.position[1]+1], state))
            
            # left
            if maze[state.position[1]][state.position[0]-1] != 0:
                # check if the state is not visited
                if [state.position[0]-1, state.position[1]] not in stateVisited:
                    bagStates.append(State([state.position[0]-1, state.position[1]], state))
            
            # right
            if maze[state.position[1]][state.position[0]+1] != 0:
                # check if the state is not visited
                if [state.position[0]+1, state.position[1]] not in stateVisited:
                    bagStates.append(State([state.position[0]+1, state.position[1]], state))
        
    
    print("path found")
    loop = False

    


