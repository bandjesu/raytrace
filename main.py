import math
import pyxel


Player = [0,0,0]
Browser_Width = 200
Browser_Height = 200
Rot=[0,0]

pyxel.init(Browser_Width, Browser_Height, "Raytracer")

def LinearFunction(Rot):
    x=math.cos(math.radians(Rot[0]))*math.cos(math.radians(Rot[1]))
    y=math.sin(math.radians(Rot[0]))*math.cos(math.radians(Rot[1]))
    z=math.sin(math.radians(Rot[1]))
    return (x,y,z)

def SphereIntersection(Line, Player, Circle):
    B = 2*(Line[0]*Player[0]+Line[1]*Player[1]+Line[2]*Player[2]-Line[0]*Circle[0]-Line[1]*Circle[1]-Line[2]*Circle[2])
    C = (Player[0]-Circle[0])**2+(Player[1]-Circle[1])**2+(Player[2]-Circle[2])**2-Circle[3]**2
    Intersection_Value = (B**2)-4*C
    if Intersection_Value>0:
        Distance1= ((-B)+math.sqrt(Intersection_Value))/2
        Distance2= ((-B)-math.sqrt(Intersection_Value))/2
        return (Distance1, Distance2)
    return ()

def PlaneIntersection(Plane, Height, Line, Player):
    if Line[Plane]!=0:
        s = (-Player[Plane]-Height)/Line[Plane]
        x=Line[0]*s+Player[0]
        y=Line[1]*s+Player[1]
        z=Line[2]*s+Player[2]
        return (s,x,y,z)
    return ()

def ViewPlane(Rot, X, Y):
    Minus=(Rot[1]%90)-90<0
    Line=LinearFunction(Rot)
    LineLen=math.sqrt(Line[0]**2+Line[1]**2)
    Xrect=(-Minus*(Line[1]/LineLen), Minus*(Line[0]/LineLen), 0)
    Yrect=((-Minus*Line[0])/LineLen*Line[2], (-Minus*Line[1])/LineLen*Line[2], Minus*LineLen)
    Line2=(Line[0]+X*Xrect[0]+Y*Yrect[0], Line[1]+X*Xrect[1]+Y*Yrect[1], Line[2]+X*Xrect[2]+Y*Yrect[2])
    Line2Len=math.sqrt(Line2[0]**2+Line2[1]**2+Line2[2]**2)
    return (Line2[0]/Line2Len, Line2[1]/Line2Len, Line2[2]/Line2Len)

def update():
    global Rot
    global Player
    if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
    if pyxel.btn(pyxel.KEY_LEFT):
            Rot[0]=Rot[0]-5
            Rot[0]=Rot[0]%360
    if pyxel.btn(pyxel.KEY_RIGHT):
            Rot[0]=Rot[0]+5
            Rot[0]=Rot[0]%360
    if pyxel.btn(pyxel.KEY_UP) and Rot[1]>-90:
            Rot[1]=Rot[1]-5
    if pyxel.btn(pyxel.KEY_DOWN) and Rot[1]<90:
            Rot[1]=Rot[1]+5 
    if pyxel.btn(pyxel.KEY_E): 
            Player[2]=Player[2]-0.5
    if pyxel.btn(pyxel.KEY_Q):
            Player[2]=Player[2]+0.5
    if pyxel.btn(pyxel.KEY_W): 
            Player[0]=Player[0]+math.cos(math.radians(Rot[0]))
            Player[1]=Player[1]+math.sin(math.radians(Rot[0]))
    if pyxel.btn(pyxel.KEY_S): 
            Player[0]=Player[0]-math.cos(math.radians(Rot[0]))
            Player[1]=Player[1]-math.sin(math.radians(Rot[0]))
    if pyxel.btn(pyxel.KEY_D): 
            Player[0]=Player[0]-math.sin(math.radians(Rot[0]))
            Player[1]=Player[1]+math.cos(math.radians(Rot[0]))
    if pyxel.btn(pyxel.KEY_A): 
            Player[0]=Player[0]+math.sin(math.radians(Rot[0]))
            Player[1]=Player[1]-math.cos(math.radians(Rot[0]))

def draw():
    pyxel.cls(0)
    for X in range(Browser_Width):
        for Y in range(Browser_Height):
            Line=ViewPlane(Rot,((X/Browser_Width)-0.5)/2, ((Y/Browser_Height)-0.5)/2)
            C=SphereIntersection(Line, Player, (2, 0, 0, 1))
            if C!=():
                pyxel.pset(X, Y, 1)
            else:
                C=PlaneIntersection(2,-1, Line, Player)
                if C!=():
                    if C[0]>0:
                         Color=(math.floor(C[1])+math.floor(C[2]))%2+2
                         pyxel.pset(X, Y, Color)
pyxel.run(update, draw)
