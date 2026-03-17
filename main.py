import math
import pygame
import sys
from datetime import datetime
import time

Player = [-1.521345131623847, 5.419253331742773, 0.2]
Browser_Width =  200
Browser_Height = 100
Number=0
Sky = pygame.image.load("C:\\Users\\benli.MATHLAB\\Desktop\\Sk.jpg")
Sky_Height=Sky.get_height()
Sky_Width=Sky.get_width()
Scene=[("Circle", (2, 0, 0, 1), (0, 0, 255), 0.5), ("Plane", (2,-1), ((255, 255, 255), (0, 0, 0)), 0.5), ("Plane", (2, 400), pygame.PixelArray(Sky), "Sky"),  ("Circle", (2, 2, 0, 1), (0, 255, 0), 0.5), ("Circle", (2, -2, 0, 1), (255, 0, 0), 0.5)]
Rot=[308, -5] 
BackgroundColor=(0, 120, 255)
Reflections=7
LightRot=[100, -20]
Lightoffset=0.5 #.6
LightEasing=0.5 #.8
SkyReflectivity=0.5
pygame.init()

screen = pygame.display.set_mode((Browser_Width, Browser_Height), pygame.RESIZABLE)
pygame.display.set_caption("Raytracer")

def AspectRatio(Browser_Width, Browser_Height):
    Xstretch=Browser_Width/Browser_Height
    Ystretch=1
    if Xstretch>1:
        Xstretch,Ystretch=1,Ystretch/Xstretch
    if Xstretch<1:
        Xstretch,Ystretch=Xstretch/Ystretch,1
    return Xstretch, Ystretch

Xstretch, Ystretch = AspectRatio(Browser_Width, Browser_Height)

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
        Pos1=[Player[0]+Line[0]*Distance1, Player[1]+Line[1]*Distance1, Player[2]+Line[2]*Distance1]
        Pos2=[Player[0]+Line[0]*Distance2, Player[1]+Line[1]*Distance2, Player[2]+Line[2]*Distance2]
        return ((Distance1, Pos1), (Distance2, Pos2))
    return ()

def PlaneIntersection(Plane, Line, Player):
    if Line[Plane[0]]!=0:
        s = (-Player[Plane[0]]-Plane[1])/Line[Plane[0]]
        x=Line[0]*s+Player[0]
        y=Line[1]*s+Player[1]
        z=Line[2]*s+Player[2]
        return (s,x,y,z)
    return ()

def ViewPlane(Rot):
    Minus=(Rot[1]%90)-90<0
    Line=LinearFunction(Rot)
    LineLen=math.sqrt(Line[0]**2+Line[1]**2)
    Xrect=(-Minus*(Line[1]/LineLen), Minus*(Line[0]/LineLen), 0)
    Yrect=((-Minus*Line[0])/LineLen*Line[2], (-Minus*Line[1])/LineLen*Line[2], Minus*LineLen)
    return (Xrect,Yrect,Line)
def ViewPlaneMove(Xrect,Yrect,Line,X,Y):
    Line2=(Line[0]+X*Xrect[0]+Y*Yrect[0], Line[1]+X*Xrect[1]+Y*Yrect[1], Line[2]+X*Xrect[2]+Y*Yrect[2])
    Line2Len=math.sqrt(Line2[0]**2+Line2[1]**2+Line2[2]**2)
    return (Line2[0]/Line2Len, Line2[1]/Line2Len, Line2[2]/Line2Len)

def reflect_across_vector(v, u):
    vx, vy, vz = v
    ux, uy, uz = u
    m = (ux*ux + uy*uy + uz*uz)**0.5
    ux, uy, uz = ux/m, uy/m, uz/m
    d = vx*ux + vy*uy + vz*uz
    return 2*d*ux - vx, 2*d*uy - vy, 2*d*uz - vz
def ReflectionVectorPlane(plane):
    if plane==0:
        return(1,0,0)
    if plane==1:
        return(0,1,0)
    if plane==2:
        return(0,0,1)
    
def ColorPlane(x,y,z,plane):
    if plane==0:
        return int(math.floor(y)%2+math.floor(z)%2)-1
    if plane==1:
        return int(math.floor(x)%2+math.floor(z)%2)-1
    if plane==2:
        return int(math.floor(x)%2+math.floor(y)%2)-1

def ClosestColission(Scene, Line, Pos):
    a=Pos[0]+Line[0]*0.00001
    b=Pos[1]+Line[1]*0.00001
    c=Pos[2]+Line[2]*0.00001
    del Pos
    Pos=(a,b,c)
    Collisions=[]
    for object in Scene:
        if object[0]=="Circle":
            IntersectionPoints=SphereIntersection(Line, Pos, object[1])     
            for i in [item for item in IntersectionPoints if item[0]>0]:
                Circleline=(i[1][0]-object[1][0], i[1][1]-object[1][1], i[1][2]-object[1][2])
                Collisions.append((i[0], object[2], reflect_across_vector((-Line[0], -Line[1],-Line[2]), Circleline), i[1], object[3], Circleline))
        if object[0]=="Plane":
            IntersectionPoint=PlaneIntersection(object[1], Line, Pos)
            if IntersectionPoint!=():
                if len(object[2])==2:
                    Color=object[2][ColorPlane(IntersectionPoint[1], IntersectionPoint[2], IntersectionPoint[3], object[1][0])]
                else:
                    Pixel=object[2][math.floor(IntersectionPoint[1]%Sky_Width),math.floor(IntersectionPoint[2]%Sky_Height)]
                    Color=(Pixel % 256, (Pixel//256)%256, Pixel//65536)
                if IntersectionPoint[0]>0:
                    Collisions.append((IntersectionPoint[0], Color, reflect_across_vector((-Line[0], -Line[1],-Line[2]), ReflectionVectorPlane(object[1][0])), IntersectionPoint[1:], object[3], (0,1,1), "Plane"))
    if len(Collisions)>0:
        Distances=[i[0] for i in Collisions]
        ClosestIndex=Distances.index(min(Distances))
        return Collisions[ClosestIndex][1:]
    return ()

def MixColors(Color1, Color2=(), W1=0.5, W2=0.5):
    if Color2==():
        Color2=Color1
    W1, W2= W1/(W1+W2), W2/(W1+W2)
    return(math.floor(Color1[0]*W1+Color2[0]*W2), math.floor(Color1[1]*W1+Color2[1]*W2), math.floor(Color1[2]*W1+Color2[2]*W2))

def DotProduct(u,v):
    return(u[0]*v[0]+u[1]*v[1]+u[2]*v[2])

def update():
    global Rot
    global Player
    global LightEasing
    global Lightoffset
    keys = pygame.key.get_pressed()
    if keys[pygame.K_F8]:
        pygame.image.save(screen, "C:\\Users\\benli.MATHLAB\\Desktop\\RaycastVideo3\\Wallpaper3.png") 
    if keys[pygame.K_LEFT]:
        Rot[0] -= 1.2
        Rot[0] %= 360
    if keys[pygame.K_RIGHT]:
        Rot[0] += 1.2
        Rot[0] %= 360
    if keys[pygame.K_UP] and Rot[1] > -90:
        Rot[1] -= 15
    if keys[pygame.K_DOWN] and Rot[1] < 90:
        Rot[1] += 5
    if keys[pygame.K_e]:
        Player[2] -= 0.5
    if keys[pygame.K_q]:
        Player[2] += 0.5
    angle_rad = math.radians(Rot[0])
    if keys[pygame.K_w]:
        Player[0] += math.cos(angle_rad)*0.3
        Player[1] += math.sin(angle_rad)*0.3
    if keys[pygame.K_s]:
        Player[0] -= math.cos(angle_rad)*0.3
        Player[1] -= math.sin(angle_rad)*0.3
    if keys[pygame.K_d]:
        Player[0] -= math.sin(angle_rad)*0.3
        Player[1] += math.cos(angle_rad)*0.3
    if keys[pygame.K_a]:
        Player[0] += math.sin(angle_rad)*0.1
        Player[1] -= math.cos(angle_rad)*0.1
    if keys[pygame.K_j]:
        LightRot[0] -= 5
        LightRot[0] %= 360
    if keys[pygame.K_l]:
        LightRot[0] += 5
        LightRot[0] %= 360
    if keys[pygame.K_i] and LightRot[1] > -90:
        LightRot[1] -= 5
    if keys[pygame.K_k] and LightRot[1] < 0:
        LightRot[1] += 5
    if keys[pygame.K_o] and LightEasing<0.9:
        LightEasing += 0.1
    if keys[pygame.K_u] and LightEasing>0.1:
        LightEasing -= 0.1
    if keys[pygame.K_n] and Lightoffset<0.9:
        Lightoffset += 0.1
    if keys[pygame.K_m] and Lightoffset>0.1:
        Lightoffset -= 0.1

def draw():
    screen.fill(BackgroundColor)
    px_array = pygame.PixelArray(screen)
    LightVector=LinearFunction(LightRot)
    for X in range(Browser_Width):
        for Y in range(Browser_Height):
            Xrect,Yrect,Line=ViewPlane(Rot)
            Line=ViewPlaneMove(Xrect, Yrect, Line, ((X/Browser_Width)-0.5)*2*Xstretch, ((Y/Browser_Height)-0.5)*2*Ystretch)
            Collision=[ClosestColission(Scene, Line, Player)]
            Light=0.5
            if Collision!=[()]:
                Light=DotProduct(Collision[0][4], LightVector)
                TesT=ClosestColission(Scene, LightVector, Collision[0][2])
                if TesT!=():
                    if TesT[-1]!="Plane":
                        Light=0
                if Light<0:
                    Light=0
                Light=(Light-0.5)*LightEasing+(Lightoffset-0.5)*(1-LightEasing)+0.5
            for i in range(Reflections-1):
                if len(Collision[i])>1 and Collision[i][3]!="Sky":
                    Collision.append(ClosestColission(Scene, Collision[i][1], Collision[i][2]))
                else:
                    break
            Colorlist = [(i[0], SkyReflectivity if i[3] == "Sky" else i[3])  for i in Collision if i != ()]
            Color=()
            Oldcolor=1
            if Collision[0][3]=="Sky":
                Color = Collision[0][0]               
            else:
                for i in Colorlist[::-1]:
                    Color=MixColors(i[0],Color,i[1],Oldcolor)
                    Oldcolor=i[1]
                if Light>0.5:
                    Color=MixColors(Color, (255, 255, 255), 1-(Light-0.5)*2, (Light-0.5))
                else:
                    Color=MixColors(Color, (0, 0, 0), Light*2,1-Light*2)
            px_array[X, Y] = Color
            
    del px_array 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            Browser_Width, Browser_Height=screen.get_size()
            Xstretch, Ystretch = AspectRatio(Browser_Width, Browser_Height)
    draw()
    update()
    pygame.display.update()
