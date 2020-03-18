import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

class PygameView(object):
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, fps=FPS):
        pygame.init()
        pygame.display.set_caption("PyGame")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0,0,0))
        self.clock = pygame.time.Clock()
        self.fps=fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)

    def paint(self):
        pygame.draw.polygon(self.background, (0,180,0), ((250,100),(300,0),(350,50)))

    def run(self):
        self.paint()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            
            pygame.display.flip()
            self.screen.blit(self.background, (0,0))

        pygame.quit()

if __name__ == '__main__':
    PygameView().run()