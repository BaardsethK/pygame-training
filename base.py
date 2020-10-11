import pygame
import math

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1,1,-1))
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))

def WireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def SolidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def Ship():
    glBegin(GL_LINES)
    for shipEdge in shipEdges:
        for vertex in shipEdge:
            glVertex3fv(shipVertices[vertex])
    glEnd()

class GameState():
    def __init__(self):
        self.shipVertices = ((-0.25,0,0), (0,1,0), (0.25,0,0))
        self.shipEdges = ((0,1),(0,2),(1,2))
        self.player_max_speed = 10
        self.player_speed = 0
        self.player_rotation = 0
        self.daccl = 0.01

    def ship(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glRotatef(self.player_rotation,0,0,1)
        glBegin(GL_LINES)
        for shipEdge in self.shipEdges:
            for vertex in shipEdge:
                glVertex3fv(self.shipVertices[vertex])
        glEnd()
        glPopMatrix()


    def update(self, rotation, accl):
        self.player_rotation += rotation
        self.player_speed += accl
        if self.player_speed > self.player_max_speed:
            self.player_speed = self.player_max_speed
        self.player_speed += self.daccl

class App:

    def __init__(self):
        self._running = True
        self._window = None
        self._gluPerspective = None
        self._gameState = GameState()
        self.size = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.cameraPos = [0,0,-20]

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Dank memes and tough dreams")
        self._window = pygame.display.set_mode(self.size, DOUBLEBUF|OPENGL)
        self._running = True
        self._gluPerspective = gluPerspective(34, (self.width/self.height), 0.1, 50.0)
        glTranslatef(0,0,-20)

    def on_event(self, event=None):
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            self._running = False
        if keys[pygame.K_ESCAPE]:
            self._running = False
        if keys[pygame.K_w]:
            self.cameraPos[1] += 0.01
        if keys[pygame.K_s]:
            self.cameraPos[1] -= 0.01
        if keys[pygame.K_a]:
            self._gameState.update(0.5,0)
        if keys[pygame.K_d]:
            self._gameState.update(-0.5,0)

    def on_loop(self):
        pass

    def on_render_player(self):
        self._gameState.ship()
       
    def on_render(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.cameraPos[0],self.cameraPos[1],self.cameraPos[2])
        WireCube()
        glPopMatrix()
        
    def on_cleanup(self):
        pygame.quit()        

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            for event in pygame.event.get():
                self.on_event(event)
            if pygame.key.get_focused:
                self.on_event(event)
            self.on_loop()
            self.on_render_player()
            glPushMatrix() 
            self.on_render()
            glPopMatrix()
            pygame.display.flip()

        self.on_cleanup()

if __name__ == "__main__" :
    app = App()
    app.on_execute()