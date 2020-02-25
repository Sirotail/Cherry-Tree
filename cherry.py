import pygame, sys
from pygame.locals import *
import time
import random
import math


white = (250,250,250)
lightgray = (200,200,200)
gray = (150,150,150)
darkgray = (100,100,100)
black = (50,50,50)
pink = (255,160,180)

class Node():

    # default origin
    x = 0
    y = 0

    # default brunch length
    v = 50
    v_x = 0
    v_y = 50

    # default brunch grow time
    t = 1

    # default brunch direction, in rad
    theta = 0

    # set end point
    x_end = 0
    y_end = 50
    
    # default index, default root
    index = 0

    # default leaf, default False
    leaf = False

    # default thickness, default 6
    thickness = 10
    
    def __init__(self, index):
        self.index = index
        self.father = None
        self.left = None
        self.right = None
        self.thickness = int(10*0.75**index)
    
    # when setting, set random_theta first, then set_v, set_origin at last
    def set_v(self, v):
        self.v = v
        self.v_x = self.v * math.sin(self.theta)
        self.v_y = self.v * math.cos(self.theta)

        if self.father is None:
            self.x = 0
            self.y = 0
        else:
            self.x = self.father.x_end
            self.y = self.father.y_end
        # set end point
        self.x_end = self.x+self.v_x*self.t
        self.y_end = self.y+self.v_y*self.t

    def random_theta(self, direction):

        if self.father is None:
            return

        # random d_theta from 20~40 degree
        d_theta = random.randrange(15,46)*3.14/180

        if direction == 'left':
            self.theta = self.father.theta - d_theta
        else:
            self.theta = self.father.theta + d_theta

class Tree():

    def __init__(self):
        self.root = Node(0)
        self.root.set_v(60)

    def add(self, node):

        q = [self.root]

        while True:

            pop_node = q.pop(0)
            
            if pop_node.left is None:
                
                node.father = pop_node
                node.x = node.father.x_end
                node.y = node.father.y_end
                node.random_theta('left')
                node.set_v(60*(0.6+0.3*random.random())**node.index)
                pop_node.left = node
                return
            
            elif pop_node.right is None:
                
                node.father = pop_node
                node.x = node.father.x_end
                node.y = node.father.y_end
                node.random_theta('right')
                node.set_v(60*(0.6+0.3*random.random())**node.index)
                pop_node.right = node
                return
            
            else:
                q.append(pop_node.left)
                q.append(pop_node.right)

    def get_nodes(self):
        

        q = [self.root]
        nodes = [self.root]

        # dont know how to jump out loop, set 100 times
        while len(q)!=0:
            pop_node = q.pop(0)
            # if no child nodes, label as leaf
            if (pop_node.left is None)and(pop_node.right is None):
                pop_node.leaf = True
            if pop_node.left is not None:
                nodes.append(pop_node.left)
                q.append(pop_node.left)
            if pop_node.right is not None:
                nodes.append(pop_node.right)
                q.append(pop_node.right)

        return nodes

def draw_tree(screen):

    # randomize
    random.seed()

    cherry = Tree()

    # plant a tree, brunch from 0 to 3
    for i in range(1,6):
        for j in range(0,2**i):
            node = Node(i)
            cherry.add(node)
            
    nodes = cherry.get_nodes()

    # draw out the tree

    screen.fill(gray)
    pygame.draw.rect(screen,black,[0,350,300,150])

    label = 0
    
    while label <6:

        dt = 0.1
        
        for node in nodes:

            x0 = int(node.x+150)
            y0 = int(-1*node.y+350)
            x1 = int(node.x_end+150)
            y1 = int(-1*node.y_end+350)

            y = y0
            r = node.thickness//2
            
            if node.index == label:
                    
                pygame.draw.line(screen,black,[x0,y0],[x1,y1],node.thickness)

        time.sleep(dt)
        pygame.display.update()

        label += 1
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    # draw flowers
    for node in nodes:
        x0 = int(node.x+150)
        y0 = int(-1*node.y+350)
        x1 = int(node.x_end+150)
        y1 = int(-1*node.y_end+350)
        if node.left is not None:
            x2 = int(node.left.x_end+150)
            y2 = int(-1*node.left.y_end+350)
        if node.right is not None:
            x3 = int(node.right.x_end+150)
            y3 = int(-1*node.right.y_end+350)
            
        if node.index == 4:
            draw_flower(screen,x1,y1)
            draw_flower(screen,x2,y2)
            draw_flower(screen,x3,y3)
            pygame.display.update()

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()


# draw flower on screen, x, y the global coordinates
def draw_flower(screen,x,y):

    # some brunch no flower
    if random.random()>=0.8:
        return
    
    r = 8
    c = 6
    pygame.draw.ellipse(screen,pink,[x-r,y-r,2*r,2*r])
    pygame.draw.line(screen,white,[x-c,y],[x+c,y],4)
    pygame.draw.line(screen,white,[x,y-c],[x,y+c],4)

    time.sleep(0.03)

# main func, initialize pygame, then draw tree
def main():
    pygame.init()
    screen = pygame.display.set_mode((300,500))
    pygame.display.set_caption('Cherry Tree')
    draw_tree(screen)

if __name__ == '__main__':
    main()
    
        
