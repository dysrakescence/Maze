from random import choice
import pygame
import pygame.freetype
import sys

class Node:
    def __init__(self, id, x, y):
        self.x = x
        self.y = y
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self._id = id

    def setConnections(self, nodeNorth, nodeSouth, nodeEast, nodeWest):
        self._numConnections = 0
        if nodeNorth:
            self.north = nodeNorth
        if nodeSouth:
            self.south = nodeSouth
        if nodeEast:
            self.east = nodeEast
        if nodeWest:
            self.west = nodeWest
        return self

    def drawPaths(self, window, x, y):
        if self.north:
            pygame.draw.rect(window, (255, 255, 255), (x + 10, y - 20, 20, 20))
        if self.south:
            pygame.draw.rect(window, (255, 255, 255), (x + 10, y + 40, 20, 20))
        if self.east:
            pygame.draw.rect(window, (255, 255, 255), (x + 40, y + 10, 20, 20))
        if self.west:
            pygame.draw.rect(window, (255, 255, 255), (x - 20, y + 10, 20, 20))
  

    def __str__(self):
        north = self.north
        if north:
            north = north._id
        south = self.south
        if south:
            south = south._id
        east = self.east
        if east:
            east = east._id
        west = self.west
        if west:
            west = west._id
        return f"Node (ID: {self._id}) at ({self.x}, {self.y}):\nN: {north}, S: {south}, E: {east}, W: {west}"

class Maze:
    def __init__(self, width: int, height: int):
        pygame.init()
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.player = Player(self.window, self.width / 2 - 20, self.height / 2 - 20, (255, 0, 0), 40, 40)

    def createRandomMaze(self, rooms: int = 25):
        def compare(items, node):
            for item in items:
                if item.x == node.x and item.y == node.y:
                    return True
            else:
                return False

        if rooms < 5:
            rooms = 5
        nodes = [Node("0", 0, 0)]
        while len(nodes) < rooms:
            node = choice(nodes)
            x, y = node.x, node.y
            directions = [i for i, direction in enumerate((node.north, node.south, node.west, node.east)) if not direction]
            try:
                direction = choice(directions)
            except Exception:
                continue
            directionNode = Node(str(len(nodes)), x, y)
            if direction == 0:
                directionNode.y += 1
                if compare(nodes, directionNode):
                    continue
                node.north = directionNode
                directionNode.south = node
            elif direction == 1:
                directionNode.y -= 1
                if compare(nodes, directionNode):
                    continue
                node.south = directionNode
                directionNode.north = node
            elif direction == 2:
                directionNode.x -= 1
                if compare(nodes, directionNode):
                    continue
                node.west = directionNode
                directionNode.east = node
            else:
                directionNode.x += 1
                if compare(nodes, directionNode):
                    continue
                node.east = directionNode
                directionNode.west = node
            nodes.append(directionNode)
        self.start = nodes[0]
        self.finish = nodes[-1]

    def traverseMaze(self):
        self.player.x, self.player.y = 380, 280
        current = self.start
        while current != self.finish:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w) and current.north:
                        current = current.north
                        pygame.draw.rect(self.window, (0, 255, 255), (self.player.x, self.player.y, 40, 40))
                        self.player.y -= 60
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and current.south:
                        current = current.south
                        pygame.draw.rect(self.window, (0, 255, 255), (self.player.x, self.player.y, 40, 40))
                        self.player.y += 60
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and current.east:
                        current = current.east
                        pygame.draw.rect(self.window, (0, 255, 255), (self.player.x, self.player.y, 40, 40))
                        self.player.x += 60
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and current.west:
                        current = current.west
                        pygame.draw.rect(self.window, (0, 255, 255), (self.player.x, self.player.y, 40, 40))
                        self.player.x -= 60
                elif event.type == pygame.QUIT:
                    self.quit()
            pygame.draw.rect(self.window, (0, 255, 255), (self.player.x, self.player.y, 40, 40))
            pygame.draw.rect(self.window, (255, 0, 0), (self.player.x + 10, self.player.y + 10, 20, 20))
            current.drawPaths(self.window, self.player.x, self.player.y)
            pygame.display.update()
        print("You've reached the exit!")
        font = pygame.font.SysFont("Papyrus", 60)
        text = font.render("You've reached the exit!", True, (0, 150, 0))
        rect = text.get_rect(center = (400, 300))
        self.window.blit(text, rect)
        pygame.display.update()
        for i in range(5):
            print(i)
            self.clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def menu(self):
        playButton = Button(self.window, self.width / 2, self.height / 2 - 150, (0, 100, 20), "Play", self.traverseMaze)
        optionsButton = Button(self.window, self.width / 2 + 250, self.height / 2 + 150, (0, 100, 100), "Options", print)
        modesButton = Button(self.window, self.width / 2 - 250, self.height / 2, (0, 100, 100), "Modes", print)
        skinsButton = Button(self.window, self.width / 2 + 250, self.height / 2, (0, 100, 100), "Skins", print)
        controlsButton = Button(self.window, self.width / 2 - 250, self.height / 2 - 150, (0, 100, 100), "Controls", print)
        creditsButton = Button(self.window, self.width / 2 + 250, self.height / 2 - 150, (0, 100, 100), "Credits", print)
        highscoresButton = Button(self.window, self.width / 2 - 250, self.height / 2 + 150, (0, 100, 100), "Highscores", print)
        quitButton = Button(self.window, self.width / 2, self.height / 2 + 150, (200, 0, 50), "Quit", self.quit)
        buttons = (playButton, optionsButton, modesButton, skinsButton, controlsButton, creditsButton, highscoresButton, quitButton)
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.y -= 5
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.y += 5
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.x += 5
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.x -= 5
            pygame.draw.rect(self.window, (0, 0, 0), (0, 0, self.width, self.height))
            for button in buttons:
                button.setStatus(self.player)
                button.draw()
            self.player.draw()
            pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()

class Button:
    def __init__(self, window, x: int, y: int, color: tuple, text: str, function, font: str = "niagaraengraved"):
        self.window = window
        self.x = x
        self.y = y
        self.originalColor = color
        self.color = color
        self.text = text
        self.function = function
        self.font = pygame.freetype.SysFont(font, 60)
        rect = self.font.render(text)
        self.halfWidth = rect[1].width // 2
        self.halfHeight = rect[1].height // 2

    def draw(self):
        pygame.draw.rect(self.window, self.color, (self.x - 90, self.y - 50, 180, 100))
        pygame.draw.rect(self.window, (0, 200, 200), (self.x - 100, self.y - 60, 200, 120), 10, 8, 8, 8, 8)
        self.font.render_to(self.window, (self.x - self.halfWidth, self.y - self.halfHeight), self.text, (0, 200, 200))

    def setStatus(self, player):
        if self.x - 90 - player.width < player.x < self.x + 90 and self.y - 50 - player.height < player.y < self.y + 50:
            self.color = (min(self.originalColor[0] + 50, 255), min(self.originalColor[1] + 50, 255), min(self.originalColor[2] + 50, 255))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.callFunction()
        else:
            self.color = self.originalColor

    def callFunction(self):
        self.function()

class Player:
    def __init__(self, window, x, y, color, width, height):
        self.window = window
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height))

def main():
    maze = Maze(800, 600)
    maze.createRandomMaze(50)
    maze.menu()

if __name__ == "__main__":
    main()