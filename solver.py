
from math import sqrt, atan2, acos, pi, cos

class LegAngles:
    hip = 0
    knee = 0
    foot = 0
    quad = 0

    def __getitem__(self, i):
        if isinstance(i, int):
            return [self.hip, self.knee, self.foot, self.quad][i]

def ik2d(thighLength, calfLength, x, y) -> LegAngles:
    angles = LegAngles()

    distance2 = pow(x, 2) + pow(y, 2)
    distance = sqrt(distance2)

    atan = atan2(x, y)

    if thighLength + calfLength <= distance:
        angles.hip = atan
        angles.foot = -angles.hip
        return angles
    
    thighLength2 = pow(thighLength, 2)
    calfLength2 = pow(calfLength, 2)

    cosAngle0 = \
        (distance2 + thighLength2 - calfLength2) \
        / \
        (2 * distance * thighLength)
    angle0 = acos(max(min(cosAngle0, 1), -1))

    cosAngle1 = \
        (calfLength2 + thighLength2 - distance2) \
        / \
        (2 * calfLength * thighLength)
    angle1 = acos(cosAngle1)

    angles.hip = atan - angle0
    angles.knee = pi - angle1
    angles.foot = -angles.hip - angles.knee
    return angles

def findKnee(thighLength, calfLength, kneeRadians: float):
    topLeft = pow(calfLength, 2) + pow(thighLength, 2)
    bottom = 2 * calfLength * thighLength

    targetAngle = pi - kneeRadians

    right = -cos(targetAngle) * bottom + topLeft
    return sqrt(right)