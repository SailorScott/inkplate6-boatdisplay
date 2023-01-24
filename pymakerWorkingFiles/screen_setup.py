from shapes import Shapes
from micropython import const
import framebuf

class screen_setup:
    NUM_LARGE = const(150)
    NUM_SMALL = const(90)


    def __init__(self, ipm):

        ipm.clear()

        # shared screen background
        ipm.fill_rect(270, 0, 10, 600, 1)  # Upper line  devider
        ipm.fill_circle(240, 210, 15, 1)  # Speed decimal
        ipm.fill_rect(550, 0, 10, 600, 1)  # Middle line  devider
        ipm.fill_rect(550, 350, 185, 10, 1)  # Bottom line  devider
        ipm.fill_rect(735, 0, 10, 600, 1)  # Warnings devider

        sharedBackground = bytearray(ipm._framebuf[:])

        # Upwind screen background needs descimal
        ipm.fill_circle(520, 210, 15, 1)  # Aparant wind decimal
        self.upWindBackground = bytearray(ipm._framebuf[:])

        # Downwind screen background needs bars besides compass
        ipm._framebuf[:] = sharedBackground[:]
        ipm.fill_rect(270, 0, 280, 18, 1)  # Compass Indicator
        ipm.fill_rect(270, 585, 280, 15, 1)  # Compass Indicator
        self.downWindBackground = bytearray(ipm._framebuf[:])

        # setup the numbers
        self.numLookupLarge = {
                "1": self.__formCharacter(NUM_LARGE, "1"),
                "2": self.__formCharacter(NUM_LARGE, "2"),
                "3": self.__formCharacter(NUM_LARGE, "3"),
                "4": self.__formCharacter(NUM_LARGE, "4"),
                "5": self.__formCharacter(NUM_LARGE, "5"),
                "6": self.__formCharacter(NUM_LARGE, "6"),
                "7": self.__formCharacter(NUM_LARGE, "7"),
                "8": self.__formCharacter(NUM_LARGE, "8"),
                "9": self.__formCharacter(NUM_LARGE, "9"),
                "0": self.__formCharacter(NUM_LARGE, "0")
            }

        print("Done setting up large nums")

        self.numLookupSmall = {
                "1": self.__formCharacter(NUM_SMALL, "1"),
                "2": self.__formCharacter(NUM_SMALL, "2"),
                "3": self.__formCharacter(NUM_SMALL, "3"),
                "4": self.__formCharacter(NUM_SMALL, "4"),
                "5": self.__formCharacter(NUM_SMALL, "5"),
                "6": self.__formCharacter(NUM_SMALL, "6"),
                "7": self.__formCharacter(NUM_SMALL, "7"),
                "8": self.__formCharacter(NUM_SMALL, "8"),
                "9": self.__formCharacter(NUM_SMALL, "9"),
                "0": self.__formCharacter(NUM_SMALL, "0")
            }


    def NumLookupLarge(self, num: str):
        return self.numLookupLarge[num]
        
    def NumLookupSmall(self, num: str):
        return self.numLookupSmall[num]





    def __formCharacter(self, fontSize: int, char: str):

        class MyFB(framebuf.FrameBuffer):
            def __init__(self, w, h, t, s):
                self._fb = bytearray(w * h)
                super().__init__(self._fb, w, h, t, s)

        Shapes.__mix_me_in(MyFB)

        # Becuase framebuffers are so quick, using those instead of writing out characters. 
        # Using Portrait layout, so letters are rotated 90 degrees.
        # Each of the digital font used for numbers has 7 strokes.
        # Font size is 241 x 156 pixels
        #      1     5
        #    _____ _____
        # 2 |    3|     | 7
        #   |_____|_____|
        #      4      6
        # inspired by how TVE is doing a demo in:
        # https://github.com/tve/micropython-inkplate6

        WIDTH = fontSize # 154 for big font, 100 for small font
        STROKE = WIDTH//5
        HALF_HEIGHT = int(WIDTH * 0.88)
        RADIUS = STROKE//2 # 1/2 STROKE

        charShape = MyFB(HALF_HEIGHT * 2 - STROKE,WIDTH, framebuf.MONO_HMSB, HALF_HEIGHT * 2 - STROKE)
        charShape.fill(0)


        if char in "01234789":
            charShape.fill_round_rect(0, 0, HALF_HEIGHT, STROKE, RADIUS, 1)  # stroke 1

        if char in "02356789":
            charShape.fill_round_rect(0, 0, STROKE, WIDTH, RADIUS, 1)  # stroke 2

        if char in "2345689":
            charShape.fill_round_rect(HALF_HEIGHT- STROKE, 0, STROKE, WIDTH, RADIUS, 1)  # stroke 3

        if char in "045689":
            charShape.fill_round_rect(0, WIDTH - STROKE, HALF_HEIGHT, STROKE, RADIUS, 1)  # stroke 4

        if char in "013456789":
            charShape.fill_round_rect(HALF_HEIGHT - STROKE, 0, HALF_HEIGHT, STROKE, RADIUS, 1)  # stroke 5

        if char in "0268":
            charShape.fill_round_rect(HALF_HEIGHT- STROKE, WIDTH - STROKE, HALF_HEIGHT, STROKE, RADIUS, 1)  # stroke 6

        if char in "0235689":
            charShape.fill_round_rect(HALF_HEIGHT * 2 - STROKE * 2, 0, STROKE, WIDTH, RADIUS, 1)  # stroke 7


        return charShape


