from mathutils import *

def StripToTriangle(triangleStripList, windingOrder="abc"):
    faces = []
    cte = 0
    for i in range(2, len(triangleStripList)):
        if triangleStripList[i] == 65535 or triangleStripList[i - 1] == 65535 or triangleStripList[i - 2] == 65535:
            if i % 2 == 0:
                cte = -1
            else:
                cte = 0
            pass
        else:
            if (i + cte) % 2 == 0:
                a = triangleStripList[i - 2]
                b = triangleStripList[i - 1]
                c = triangleStripList[i]
            else:
                a = triangleStripList[i - 1]
                b = triangleStripList[i - 2]
                c = triangleStripList[i]

            if a != b and b != c and c != a:
                if windingOrder == "abc":
                    faces.append([a, b, c])
                elif windingOrder == "cba":
                    faces.append([c, b, a])
    return faces

def ToTriangle(triangleList):
    faces = []
    for i in range(2, len(triangleList), 3):
        a  = triangleList[i - 2]
        b  = triangleList[i - 1]
        c  = triangleList[i]
        faces.append([a,b,c])
    return faces

def ConvertNormal_S10S11S11(integer, reverse=False):
    
    p1 = (integer & 0xFFC00000) >> 22
    p2 = (integer & 0x003FF800) >> 11
    p3 = (integer & 0x000007FF)

    if p1 & 0x200:
        r1 = -((0x200 - (p1 & 0x1FF))) / 0x1FF
    else:
        r1 = p1 / 0x1FF

    if p2 & 0x400:
        r2 = -((0x400 - (p2 & 0x3FF))) / 0x3FF
    else:
        r2 = p2 / 0x3FF

    if p3 & 0x400:
        r3 = -((0x400 - (p3 & 0x3FF))) / 0x3FF
    else:
        r3 = p3 / 0x3FF

    if reverse == True:
        normal = Vector((r3, r2, r1)).normalized()
    else:
        normal = Vector((r1, r2, r3)).normalized()

    return normal