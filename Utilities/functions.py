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

def sign_ten_bit(Input):
    if Input < 0x200: 
        return Input
    else: 
        return Input - 0x400

def sign_eleven_bit(Input):
    if Input < 0x400: 
        return Input
    else: 
        return Input - 0x800

def ConvertNormal_S10S11S11(integer):

    normal = []
    
    """
    normal.append(sign_ten_bit(integer & 0x3FF))
    normal.append(sign_eleven_bit((integer >> 11) & 0x7FF))
    normal.append(sign_eleven_bit((integer >> 22) & 0x7FF))
    test1 = Vector(((normal[2]) / 1023, (normal[1]) / 1023, (normal[0]) / 511)).normalized()
    """

    element = integer & 0x3FF
    normal.append(element / 511)
    element = (integer >> 10) & 0x7FF
    normal.append(element / 1023)
    element = (integer >> 21) & 0x7FF
    normal.append(element / 1023)

    test1 = Vector((normal[2], normal[1], normal[0])).normalized()

    return test1