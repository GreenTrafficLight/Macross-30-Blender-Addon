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

def ConvertNormal_S10S11S11(integer):

    normal = []
    
    normal.append(integer & 0x3FF)
    normal.append((integer >> 10) & 0x3FF)
    normal.append((integer >> 20) & 0x3FF)
    
    return Vector(((normal[0] - 512) / 511, (normal[1] - 1024) / 1023, (normal[2] - 1024) / 1023)).normalized()