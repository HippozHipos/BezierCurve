import pygame
import sys

pygame.init()

textSize = 25
font = pygame.font.Font(pygame.font.get_default_font(), textSize)
_t = 0

red = (255, 0, 0)
green = (0, 255 , 0)
blue = (0, 0 , 255)
black = (0, 0 , 0)

def drawPoint(window, p, color):
    pygame.draw.circle(window, color, (p.x, p.y), p.radius)

def getPs(t):
    tt = t * t
    ttt = t * t * t
    return(
        -ttt + 3 * tt -3 * t + 1,
        3 * ttt - 6 * tt + 3 * t,
        -3 * ttt + 3 * tt,
        ttt
    )

def drawPointOnCurve(window, p, t, color, scale):
    pygame.draw.circle(window, color, (5 + (t * scale), 50 + (p * scale)), 5)

def drawCurvePixel(window, p, t, color, scale):
    window.set_at((5 + int(t * scale), 50 + int(p * scale)), color)

def drawVectorsAdded(window, origin, vecs):
    p0End = (vecs[0][0] + origin[0], vecs[0][1] + origin[1])
    p1End = (vecs[1][0] + p0End[0], vecs[1][1] + p0End[1])
    p2End = (vecs[2][0] + p1End[0], vecs[2][1] + p1End[1])
    p3End = (vecs[3][0] + p2End[0], vecs[3][1] + p2End[1])
    
    pygame.draw.line(window, red, origin, p0End, 2)
    pygame.draw.line(window, green, p0End, p1End, 2)
    pygame.draw.line(window, blue, p1End, p2End, 2)
    pygame.draw.line(window, black, p2End, p3End, 2)

class Point:
    def __init__(self, origin, x, y):
        self.origin = origin
        self.x = x
        self.y = y
        self.radius = 10
        self.move = False

    def moveable(self, mouse, mousepos):
        if mouse[0]:
            rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
            if rect.collidepoint(mousepos):
                self.move = True

        if not mouse[0]:
            self.move = False

        if self.move:
            self.x, self.y = mousepos

class Curve:
    def __init__(self, origin):
        self.origin = origin
        self.p0 = Point(origin, origin[0] - 120, origin[1] + 30)
        self.p1 = Point(origin, origin[0] + 120, origin[1] + 30)
        self.p2 = Point(origin, origin[0] - 110, origin[1] - 120)
        self.p3 = Point(origin, origin[0] + 110, origin[1] - 120)

    def moveable(self, mouse, mousepos):
        self.p0.moveable(mouse, mousepos)
        self.p1.moveable(mouse, mousepos)
        self.p2.moveable(mouse, mousepos)
        self.p3.moveable(mouse, mousepos)
        ps = (self.p0, self.p1, self.p2, self.p3)
        for i in range(4):
            if ps[i].move:
                for j in range(4):
                    if i != j:
                        ps[j].move = False

    def draw(self, window):
        drawPoint(window, self.p0, red)
        drawPoint(window, self.p1, green)
        drawPoint(window, self.p2, blue)
        drawPoint(window, self.p3, black)

        pygame.draw.line(window, red, (self.p0.x, self.p0.y), (self.p1.x, self.p1.y), 3)
        pygame.draw.line(window, green, (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), 3)
        pygame.draw.line(window, blue, (self.p2.x, self.p2.y), (self.p3.x, self.p3.y), 3)

    def getControlVectors(self):
        findVector = lambda p : (p.x - self.origin[0], p.y - self.origin[1])
        return (findVector(self.p0), findVector(self.p1), findVector(self.p2), findVector(self.p3))

    def getScaledControlVectors(self, pVals):
        vectors = self.getControlVectors()
        scaleVector = lambda x : (vectors[x][0] *  pVals[x], vectors[x][1] *  pVals[x])
        return (scaleVector(0), scaleVector(1), scaleVector(2), scaleVector(3))

    def getPointOnCurve(self, pVals):
        vectors = self.getScaledControlVectors(pVals)
        addVector = lambda v1, v2 : (v1[0] + v2[0], v1[1] + v2[1])
        return addVector(self.origin, addVector(addVector(vectors[0], vectors[1]), addVector(vectors[2], vectors[3])))

    def getControlPoints(self):
        return (self.p0, self.p1, self.p2, self.p3)

        
curve = Curve((700, 500))   

scale = 380
window = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    events = pygame.event.get()    
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    curve.moveable(mouse, mousePos)
    pygame.display.set_caption(f"Bezier Curves - fps - {int(clock.get_fps())}")
    
    if keys[pygame.K_w]: _t += 0.005
    if keys[pygame.K_q]: _t -= 0.005
    _t = min(1, max(_t, 0))

    window.fill((255, 255, 255))
    pygame.draw.rect(window, (0, 0, 0), (5, 50, 380, 380), 1)

    t = 0
    while t <= 1:
        cp0, cp1, cp2, cp3 = getPs(t)
        drawCurvePixel(window, cp0, t, red, scale)
        drawCurvePixel(window, cp1, t, green, scale)
        drawCurvePixel(window, cp2, t, blue, scale)
        drawCurvePixel(window, cp3, t, black, scale)

        pointAtTValue = curve.getPointOnCurve((cp0, cp1, cp2, cp3))
        pygame.draw.circle(window, (255, 0, 255), pointAtTValue, 3)

        t += 0.001
        
    cp0, cp1, cp2, cp3 = getPs(_t)
    drawPointOnCurve(window, cp0, _t, red, scale)
    drawPointOnCurve(window, cp1, _t, green, scale)
    drawPointOnCurve(window, cp2, _t, blue, scale)
    drawPointOnCurve(window, cp3, _t, black, scale)

    pygame.draw.rect(window, red, (5, 450, cp0 * 380, 50))
    pygame.draw.rect(window, green, (5, 510, cp1 * 380, 50))
    pygame.draw.rect(window, blue, (5, 570, cp2 * 380, 50))
    pygame.draw.rect(window, black, (5, 630, cp3 * 380, 50))

    curve.draw(window)
    pygame.draw.circle(window, black, curve.origin, 5, 1)
    pVals = (cp0, cp1, cp2, cp3)
    drawVectorsAdded(window, curve.origin, curve.getScaledControlVectors(pVals))
    pointAtTValue = curve.getPointOnCurve(pVals)
    pygame.draw.circle(window, (255, 0, 255), pointAtTValue, 10)

    val = str(_t)[0:5]
    tvalue = font.render(f"t = {val}", True, black)
    window.blit(tvalue, (10, 10))
    
    pygame.display.flip()

