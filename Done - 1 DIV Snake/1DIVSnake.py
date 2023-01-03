from random import randint
from graphics import *
import keyboard
import time

def getInput(dir):
	if((keyboard.is_pressed("w") or keyboard.is_pressed("up")) and dir != [0, 1]):
		return([0, -1])
	elif((keyboard.is_pressed("d") or keyboard.is_pressed("right")) and dir != [-1, 0]):
		return([1, 0])
	elif((keyboard.is_pressed("s") or keyboard.is_pressed("down")) and dir != [0, -1]):
		return([0, 1])
	elif((keyboard.is_pressed("a") or keyboard.is_pressed("left")) and dir != [1, 0]):
		return([-1, 0])
	else:
		return(dir)


class Snake():
	def __init__(self):
		self.alive = 1
		self.headDir = [1, 0]
		self.bodyPos = [[xwin / 2, ywin / 2], [xwin / 2 - self.headDir[0], ywin / 2 - self.headDir[1]]]
		
	def update(self):
		for i in range(1, len(self.bodyPos)):
			self.bodyPos[-i] = self.bodyPos[-i - 1]
		self.bodyPos[0] = [self.bodyPos[0][0] + self.headDir[0], self.bodyPos[0][1] + self.headDir[1]]
		self.checkDead()

	def updateDir(self):
		self.headDir = getInput(self.headDir)

	def grow(self):
		self.bodyPos.append([0, 0])

	def show(self):
		for body in self.bodyPos:
			r = Rectangle(Point(body[0], body[1]), Point(body[0] + 1, body[1] + 1))
			r.setFill("cyan")
			r.setOutline("black")
			r.setWidth(3)
			r.draw(win)
		win.update()

	def futureHead(self):
		return([self.bodyPos[0][0] + self.headDir[0], self.bodyPos[0][1] + self.headDir[1]])

	def checkDead(self):
		if(self.bodyPos[0] in self.bodyPos[1:] or self.bodyPos[0][0] > xwin - 1 or self.bodyPos[0][0] < 0 or self.bodyPos[0][1] > ywin - 1 or self.bodyPos[0][1] < 0):
			self.alive = 0

class Food():
	def __init__(self, div, snake, pos = 1):
		if(pos == 1):
			self.pos = [randint(1, xwin - 2), randint(1, ywin - 2)]
			while(self.pos in snake.bodyPos or self.pos in [food.pos for food in foods]):
				self.pos = [randint(1, xwin - 2), randint(1, ywin - 2)]
		else:
			self.pos = pos
		
		self.div = div

	def show(self):
		t = Text(Point(self.pos[0] + 0.5, self.pos[1] + 0.5), f"1/{self.div}")
		t.setStyle("bold")
		r = Rectangle(Point(self.pos[0], self.pos[1]), Point(self.pos[0] + 1, self.pos[1] + 1))
		r.setFill({1:"white", 2:"red", 4:"blue", 8:"green", 16:"#630000"}[self.div])
		r.setOutline("black")
		r.setWidth(3)
		r.draw(win)
		t.draw(win)

	def push(self, snake):
		f = [i for i in foods]
		f.remove(self)
		self.pos = [self.pos[0] + snake.headDir[0], self.pos[1] + snake.headDir[1]]
		for food in f:
			if(food.div == self.div and self.pos == food.pos):
				foods.pop(foods.index(food))
				foods.pop(foods.index(self))
				foods.append(self.__class__(self.div // 2, snake, self.pos))
			elif(food.div != self.div and self.pos == food.pos):
				food.push(snake)
def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

win = GraphWin("1/Snake", 600, 600)
win.setBackground("grey")


xwin = 16
ywin = 16
win.setCoords(0, ywin, xwin, 0)

snake = Snake()
foods = []
foods = [Food(1, snake)]

#         2,  4,  8, 16
stages = [4, 8, 16, 32]

while(1):
	stime = time.time()
	while(time.time() - stime < 0.5):
		snake.updateDir()

	clear(win)
	
	for food in foods:
		if(snake.futureHead() == food.pos and food.div == 1):
			snake.grow()
			if(len(snake.bodyPos) < stages[0]): 
				foods = []
				for i in range(1):
					foods.append(Food(1, snake))
			if(stages[0] <= len(snake.bodyPos) < stages[1]):
				foods = []
				for i in range(2):
					foods.append(Food(2, snake))
			if(stages[1] <= len(snake.bodyPos) < stages[2]):
				foods = []
				for i in range(4):
					foods.append(Food(4, snake))
			if(stages[2] <= len(snake.bodyPos)):
				foods = []
				for i in range(8):
					foods.append(Food(8, snake))
			if(stages[3] <= len(snake.bodyPos)):
				foods = []
				for i in range(16):
					foods.append(Food(16, snake))
		
	for food in foods:
		if(snake.futureHead() == food.pos):
			food.push(snake)
		if(0 > food.pos[0] or food.pos[0] > xwin - 1 or 0 > food.pos[1] or food.pos[1] > ywin - 1):
			snake.alive = 0

	snake.update()

	snake.show()
	for food in foods:
		food.show()

	if(snake.alive == 0):
		win.close()
		break