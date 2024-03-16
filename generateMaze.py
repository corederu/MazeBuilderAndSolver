import pygame
import random


def newMaze():
    # Create a 2D array of 10x10
    maze = [[0 for x in range(60)] for y in range(60)]
    
    # Set start and end
    maze[1][1] = 1
    maze[58][58] = 2

    return maze


def draw(maze, builder, screen):
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
    
    # draw the builder
    pygame.draw.rect(screen, (0,0,255), (builder[0]*10, builder[1]*10, 10, 10))

def updateMaze(maze, builder):

    walk = False

    xBuilder = builder[0]
    yBuilder = builder[1]
    
    # choose a direction for the builder
    direction = random.randint(0,3)

    # up
    if direction == 0 and yBuilder > 1:

        # go back
        if maze[yBuilder-1][xBuilder] == 3:
            builder[1] -= 1
            walk = True
        
        # want to dig (check if not cut a wall)
        if maze[yBuilder-1][xBuilder] == 0:
            
            # check it close arround th hole
            if maze[yBuilder-2][xBuilder] == 0 and maze[yBuilder-1][xBuilder+1] == 0 and maze[yBuilder-1][xBuilder-1] == 0 and maze[yBuilder-2][xBuilder+1] == 0 and maze[yBuilder-2][xBuilder-1] == 0:
                maze[yBuilder-1][xBuilder] = 3
                builder[1] -= 1

    # right
    elif direction == 1 and xBuilder < 58:

        # go back
        if maze[yBuilder][xBuilder+1] == 3:
            builder[0] += 1
            walk = True
        
        # want to dig (check if not cut a wall)
        if maze[yBuilder][xBuilder+1] == 0:
            
            # check it close arround th hole
            if (maze[yBuilder][xBuilder+2] == 0 and maze[yBuilder+1][xBuilder+1] == 0 and maze[yBuilder-1][xBuilder+1] == 0 and maze[yBuilder+1][xBuilder+2] == 0 and maze[yBuilder-1][xBuilder+2] == 0) or (maze[yBuilder][xBuilder+2] == 2):
                maze[yBuilder][xBuilder+1] = 3
                builder[0] += 1
        
        # check if builder is out
        if maze[yBuilder][xBuilder+1] == 2:
            builder[0] += 1
            
        
    
    # down
    elif direction == 2 and yBuilder < 58:

        # go back
        if maze[yBuilder+1][xBuilder] == 3:
            builder[1] += 1
            walk = True
        
        # want to dig (check if not cut a wall)
        if maze[yBuilder+1][xBuilder] == 0:
            
            # check it close arround th hole
            if (maze[yBuilder+2][xBuilder] == 0 and maze[yBuilder+1][xBuilder+1] == 0 and maze[yBuilder+1][xBuilder-1] == 0 and maze[yBuilder+2][xBuilder+1] == 0 and maze[yBuilder+2][xBuilder-1] == 0) or (maze[yBuilder+2][xBuilder] == 2):
                maze[yBuilder+1][xBuilder] = 3
                builder[1] += 1
        
        # check if builder is out
        if maze[yBuilder+1][xBuilder] == 2:
            builder[1] += 1
        

    # left
    elif direction == 3 and xBuilder > 1:

        # go back
        if maze[yBuilder][xBuilder-1] == 3:
            builder[0] -= 1
            walk = True
        
        # want to dig (check if not cut a wall)
        if maze[yBuilder][xBuilder-1] == 0:
            
            # check it close arround th hole
            if maze[yBuilder][xBuilder-2] == 0 and maze[yBuilder+1][xBuilder-1] == 0 and maze[yBuilder-1][xBuilder-1] == 0 and maze[yBuilder+1][xBuilder-2] == 0 and maze[yBuilder-1][xBuilder-2] == 0:
                maze[yBuilder][xBuilder-1] = 3
                builder[0] -= 1
        

    return maze, builder, walk

def findOut(builder):
    if builder[0] == 58 and builder[1] == 58:
        return True
    else:
        return False

def randomRestart(maze):

    x = random.randint(1,58)
    y = random.randint(1,58)

    if maze[y][x] == 3:
        return [x,y]
    else:
        return randomRestart(maze)

def saveMaze(maze):
    # in a txt
    file = open("maze.txt", "w")
    for y in range(60):
        for x in range(60):
            file.write(str(maze[y][x]))
        file.write("\n")
    file.close()

    # in a image
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
    
    pygame.image.save(image, "maze.png")


# --- Main --

# Initialize the game engine
pygame.init()

screen = pygame.display.set_mode((600,600))

pygame.display.set_caption("Maze Builder")

maze = newMaze()
builder = [1,1]

numberWalk = 0

loop = True
while loop:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze = newMaze()
                builder = [1,1]
    
    # clear screen
    screen.fill((0,0,0))

    # update maze
    maze, builder, walk = updateMaze(maze, builder)

    if walk:
        numberWalk += 1
    
    # if the builder is stuck we place it at a random place
    if numberWalk > 1000:
        builder = randomRestart(maze)
        numberWalk = 0

    # draw maze
    draw(maze, builder, screen)

    # check if builder is out
    if findOut(builder):
        saveMaze(maze)
        print("Builder is out")
        loop = False

    # update screen
    pygame.display.flip()


