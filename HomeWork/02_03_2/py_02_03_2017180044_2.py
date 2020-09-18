import turtle
DrawCount = 0
Pos = 0

while DrawCount < 25 :
    turtle.forward(100)
    turtle.left(90)
    turtle.forward(100)
    turtle.left(90)
    turtle.forward(100)
    turtle.left(90)
    turtle.forward(100)
    turtle.left(90)
    turtle.forward(100)
    
    DrawCount = DrawCount + 1
    
    if DrawCount % 5 == 0 :
        Pos = Pos + 100
        turtle.penup()
        turtle.goto(0,Pos)
        turtle.pendown()
    
    
turtle.exitonclick()
