from math import radians, pi, cos, sin, asin, atan2, sqrt
from vector3 import Vector3

class StewartPlatform:
    # real angles from platform v1.0
    baseAngles = [308.5, 351.5, 68.5, 111.5, 188.5, 231.5 ]
    platformAngles = [286.10, 13.9, 46.1, 133.9, 166.1, 253.9]
    beta = [-8*pi/3, pi/3, 0, -pi, -4*pi/3, -7*pi/3]

    # real measurements from platform v1.0
    SCALE_INITIAL_HEIGHT = 250
    SCALE_BASE_RADIUS = 140
    SCALE_PLATFORM_RADIUS = 32
    SCALE_HORN_LENGTH = 36
    SCALE_LEG_LENGTH = 270

    def __init__(self, scale=1.0):
        self.translation = Vector3()
        self.rotation = Vector3()
        self.initialHeight = Vector3(0, 0, scale*StewartPlatform.SCALE_INITIAL_HEIGHT)
        self.baseJoint = []
        self.platformJoint = []
        self.q = []
        self.l = []
        self.A = []
        self.alpha = []
        self.baseRadius = scale*StewartPlatform.SCALE_BASE_RADIUS
        self.platformRadius = scale*StewartPlatform.SCALE_PLATFORM_RADIUS
        self.hornLength = scale*StewartPlatform.SCALE_HORN_LENGTH
        self.legLength = scale*StewartPlatform.SCALE_LEG_LENGTH;

        for i in range(6):
            mx = self.baseRadius*cos(radians(self.baseAngles[i]))
            my = self.baseRadius*sin(radians(self.baseAngles[i]))
            self.baseJoint.insert(i, Vector3(mx, my))

        for i in range(6):
            mx = self.platformRadius*cos(radians(self.platformAngles[i]))
            my = self.platformRadius*sin(radians(self.platformAngles[i]))
            self.platformJoint.insert(i, Vector3(mx, my))
            self.q.insert(i,Vector3())
            self.l.insert(i,Vector3())
            self.A.insert(i,Vector3())
            self.alpha.insert(i,0)

        self.calcQ()

    def calcQ(self):
        for i in range(6):
            # rotation
            self.q[i].x = (cos(self.rotation.z)*cos(self.rotation.y)*self.platformJoint[i].x +
                (-sin(self.rotation.z)*cos(self.rotation.x)+cos(self.rotation.z)*sin(self.rotation.y)*sin(self.rotation.x))*self.platformJoint[i].y +
                (sin(self.rotation.z)*sin(self.rotation.x)+cos(self.rotation.z)*sin(self.rotation.y)*cos(self.rotation.x))*self.platformJoint[i].z)

            self.q[i].y = (sin(self.rotation.z)*cos(self.rotation.y)*self.platformJoint[i].x +
                (cos(self.rotation.z)*cos(self.rotation.x)+sin(self.rotation.z)*sin(self.rotation.y)*sin(self.rotation.x))*self.platformJoint[i].y +
                (-cos(self.rotation.z)*sin(self.rotation.x)+sin(self.rotation.z)*sin(self.rotation.y)*cos(self.rotation.x))*self.platformJoint[i].z)

            self.q[i].z = (-sin(self.rotation.y)*self.platformJoint[i].x +
                cos(self.rotation.y)*sin(self.rotation.x)*self.platformJoint[i].y +
                cos(self.rotation.y)*cos(self.rotation.x)*self.platformJoint[i].z)

            # translation
            self.q[i].add(self.translation + self.initialHeight)
            self.l[i] = self.q[i] - self.baseJoint[i]
            print "%s %s %s"%(i, self.q[i], self.l[i])

    def calcAlpha(self):
        for i in range(6):
            L = self.l[i].magnitudeSquared()-(self.legLength**2)+(self.hornLength**2)
            M = 2*self.hornLength*(self.q[i].z-self.baseJoint[i].z)
            N = 2*self.hornLength*(cos(self.beta[i])*(self.q[i].x-self.baseJoint[i].x) + sin(self.beta[i])*(self.q[i].y-self.baseJoint[i].y))
            print "%s %s %s"%(str(i), str(M*M+N*N), str(L/sqrt(M*M+N*N)))
            self.alpha[i] = asin(L/sqrt(M*M+N*N)) - atan2(N,M)

            self.A[i].x = self.hornLength*cos(self.alpha[i])*cos(self.beta[i]) + self.baseJoint[i].x
            self.A[i].y = self.hornLength*cos(self.alpha[i])*sin(self.beta[i]) + self.baseJoint[i].y
            self.A[i].z = self.hornLength*sin(self.alpha[i]) + self.baseJoint[i].z

            ''' # initial position for debugging
            xqxb = self.q[i].x - self.baseJoint[i].x
            yqyb = self.q[i].y - self.baseJoint[i].y
            h0 = sqrt(self.legLength**2 + self.hornLength**2 - xqxb**2 - yqyb**2) - self.q[i].z

            L0 = 2*self.hornLength*self.hornLength
            M0 = 2*self.hornLength*(h0+self.q[i].z)
            a0 = asin(L0/sqrt(M0*M0+N0*N0)) - atan2(N, M0)
            '''

    def applyTranslationAndRotation(self, t, r):
        self.rotation.set(r)
        self.translation.set(t)
        self.calcQ()
        self.calcAlpha()