import engineM6 as e, math, random

gameState = "begin"
paddle = e.sprite(e.screenW/2-16,e.screenH - 64, "paddle.png")
shield = e.sprite(e.screenW/2,e.screenH-32, "shield.png")
shield.visible = False
spike = e.sprite(e.screenW-16,e.screenH - 64, "realspike.png")
spike.visible=False
paddle.speed=14
blockList=[]
hSpace = 64
vSpace = 64
blockPictureList=["health block.png", "sheild block.png", "powerup.png", "spike.png", "regular block.png"]
points=0
lives=3
ball = e.sprite(e.screenW/2-16,e.screenH - 300, "ball.png")
startButton = e.sprite(e.screenW/2-60, e.screenH/2-45, "start_button.png")
pointsText = e.text("points:"+str(points), 24, (255,0,0), 25, 520)
livesText = e.text("lives:"+str(lives), 24, (255,0,0), 25, 570)
timer=3*20
def makeGrid():
    global hSpace, vSpace
    
    for i in range(0, 12):
        for j in range(0, 4):
            blockPicture=random.choice(blockPictureList)
            newBlock = e.sprite(i*hSpace,+ j*vSpace, blockPicture)
            newBlock.blockString = blockPicture
            blockList.append(newBlock)
    
def beginState():
    global points, lives, gameState
    if e.mc.spriteClick(startButton, 0):
        paddle.x = paddle.xStart
        makeGrid()
        ball.rotation = 270
        startButton.visible = False
        gameState = "play"


def bounceOff(givenSprite):
    directionOfImpact = e.directionToPoint(ball.x+ball.width/2, ball.y+ball.height/2, givenSprite.x+givenSprite.width/2, givenSprite.y+givenSprite.height/2)
    ball.rotation = directionOfImpact + 180
        
    
def playState():
    global points, lives, timer
    
    if e.kb.held(e.pygame.K_LEFT) and paddle.x > paddle.speed:
        paddle.x -= paddle.speed
        
    if e.kb.held(e.pygame.K_RIGHT) and paddle.rightEdge < e.screenW-paddle.speed:
        paddle.x += paddle.speed

    if ball.collide(paddle):
        bounceOff(paddle)

    if ball.x < 1 and ball.rotation > 90 and ball.rotation < 270:
        ball.rotation += 180
        
    if ball.rightEdge > e.screenW and (ball.rotation < 90 or ball.rotation > 270):
        ball.rotation += 180

    if ball.rotation > 360:
        ball.rotation -= 360

    if abs(ball.rotation - 180) < 10:
        ball.rotation = 135

    if abs(ball.rotation) < 10 or abs(ball.rotation) > 350:
        ball.rotation = 45

    if ball.y < 1 and 0 < ball.rotation < 180:
        ball.rotation += 180

    for someBlock in blockList:
        if ball.collide(someBlock):
            if someBlock.blockString == "health block.png":
                lives+=0.5
                blockList.remove(someBlock)
                someBlock.destroy()
            if someBlock.blockString == "powerup.png":
                points+=8
                blockList.remove(someBlock)
                someBlock.destroy()
            if someBlock.blockString == "regular block.png":
                points+=1
                blockList.remove(someBlock)
                someBlock.destroy()
            if someBlock.blockString == "sheild block.png":
                shield.visible = True
                shield.x=0
                blockList.remove(someBlock)
                someBlock.destroy()
        
            if someBlock.blockString == "spike.png":
                spike.visible = True
                spike.x=someBlock.x
                spike.y=someBlock.y
                spike.vspeed += 3
                blockList.remove(someBlock)
                someBlock.destroy()
                if spike.collide(paddle):
                    spike.visible=False
                    lives-=1
            bounceOff(someBlock)
            
    if ball.y > paddle.y:
        ball.x=e.screenW/2-16
        ball.y=e.screenH - 300
        ball.rotation=270
        lives-=1
        
    if ball.collide(shield) and shield.visible==True:
        bounceOff(shield)
    if lives <0.5:
        for someBlock in blockList:
            someBlock.destroy()

            
        blockList.clear()
        paddle.visible=False
        ball.visible=False
        gameState = "game over"
    if len(blockList)==0 and lives>0:
        ball.x=e.screenW/2-16
        ball.y=e.screenH-300
        makeGrid()

    

def gameOverState():
    gameOverText = e.text("GAME OVER \n Your score was:"+str(points), 36, (255,0,0), 25, 200)
    print(gameState)
    

while True:

    if gameState == "begin":
        beginState()

    if gameState == "play":
        ball.moveForward(10)
        ball.rotation+=0.1
        
        if spike.collide(paddle):
            spike.y+=300
            spike.visible=False
            lives-=1
        if shield.visible==True:
            timer-=1
            if timer < 1:
                shield.visible=False
                timer=3*180
        if lives <0.5:
            for someBlock in blockList:
                someBlock.destroy()

            blockList.clear()
            paddle.visible=False
            ball.visible=False
            gameState = "game over"
                
        playState()

    if gameState == "game over":
        gameOverState()

    pointsText.changeText("Points: "+str(points))
    livesText.changeText("Lives: "+str(lives))

    e.runGame((0,0,0))
