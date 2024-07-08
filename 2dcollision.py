import pygame
import sys
import math

WIDTH = 620
HEIGHT = 480
WHITE = (255,255,255)
RADIUS = 25

class simulation:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('2D Collision simulator')
        pygame.mouse.set_visible(False)                         # hiding curser

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # set up screen with const dimensions
        self.clock = pygame.time.Clock()          
        self.circle = pygame.image.load('blackcircle.png')      # importing curser graphics
        self.circle.set_colorkey(WHITE)                         # removing surrounding white backround with colorkey
    
    def run(self):
        
        # setting up and array of tuples to keep track of the curser coordinates for the previous 6 frames
        curser_pos_arr = [(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1)]

        # defining the objects starting position
        ox, oy = (WIDTH/2, HEIGHT/2)

        # initiating the curser's average velocity and object velocity, which will be computed 6 frames into the simulation
        curser_average_velocity = 0
        object_velocity = 0

        # initiating the font, which is used to display text on the top left corner
        font = pygame.font.Font(None,24) # display distance

        # setting up initial values for values, which will be used for later computing
        dx = 0          # delta_x and delta_y that records the vector between curser and object when a collision occurs
        dy = 0          
        o_velo_x = 0    # adjustment of the object pos for a given frame
        o_velo_y = 0    
        vector = 0      # distance between curser and object
        k = 1           # scaler

        while True:
            self.screen.fill((WHITE))

            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:       # close program is the window is closed
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:    # close program if escape key is pressed
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # getting and adjusting mouse coordinates to match the center of the curser-icon
            x, y = pygame.mouse.get_pos()
            curser_pos_arr[5] = curser_pos_arr[4]   # inserting latest curser coordinates in front and shifting earlier data one spot behind-
            curser_pos_arr[4] = curser_pos_arr[3]   # while keeping the array at 4 elements by overwriting the 4th element
            curser_pos_arr[3] = curser_pos_arr[2]
            curser_pos_arr[2] = curser_pos_arr[1]   
            curser_pos_arr[1] = curser_pos_arr[0]
            curser_pos_arr[0] = (x,y)

            # track the curser's velocity at the given moment (the average of 3 vector lengths connecting the curser pos the last 3 frames)
            average_x = ((curser_pos_arr[1][0] - curser_pos_arr[0][0]) + 
                        (curser_pos_arr[2][0] - curser_pos_arr[1][0]) + 
                        (curser_pos_arr[3][0] - curser_pos_arr[2][0]) + 
                        (curser_pos_arr[4][0] - curser_pos_arr[3][0]) + 
                        (curser_pos_arr[5][0] - curser_pos_arr[4][0]))/5
            average_y = ((curser_pos_arr[1][1] - curser_pos_arr[0][1]) + 
                        (curser_pos_arr[2][1] - curser_pos_arr[1][1]) + 
                        (curser_pos_arr[3][1] - curser_pos_arr[2][1]) + 
                        (curser_pos_arr[4][1] - curser_pos_arr[3][1]) + 
                        (curser_pos_arr[5][1] - curser_pos_arr[4][1]))/5

            curser_average_velocity = math.sqrt(average_x**2 + average_y**2)    

            #display curser velocity
            text = font.render('Curser velocity: '+str("%.2f" % curser_average_velocity), True, (0,0,0), (255,255,255))
            self.screen.blit(text, (20,40))

            # track the distance between the core of the curser blob and the other object (pythagoras sentence)
            vector_x = ox - x
            vector_y = oy - y
            vector = float(math.sqrt(vector_x**2+vector_y**2))
            "%.3f" % vector

            # scaling a constant, k, to reduce the vector size to 1 while keeping the direction
            if vector < 2*(RADIUS-RADIUS/10):
                k = float(1/vector) 

            #constantly reducing object_velocity to simulate friction
            if object_velocity > 0:
                object_velocity*=0.997

            # object-wall collision handling (as in a elastic environment where the wall-collision alone results in no loss of kinetic energy)
            if ox-RADIUS < 0:
                dx = -dx
                ox = RADIUS
            if ox + RADIUS > WIDTH:
                dx = -dx
                ox = WIDTH - RADIUS
            if oy-RADIUS < 0:
                dy = -dy
                oy = RADIUS
            if oy + RADIUS > HEIGHT:
                dy = -dy
                oy = HEIGHT - RADIUS 

            # collision handling between curser and object
            if vector < 43:
                # the object will move in the same direction as the vector
                dx = vector_x
                dy = vector_y

                if curser_average_velocity > object_velocity:
                    object_velocity = curser_average_velocity

            # computing how much to adjust the objects position each frame, first parenthesis is a direction (or a hypotenuse) which is scaled down by k
            o_velo_x = (dx*k)*(object_velocity)
            o_velo_y = (dy*k)*(object_velocity)

            # adjusting the object's x and y coordinates
            ox += o_velo_x
            oy += o_velo_y

            # displaying the distance between the curser and the object
            vector = "%.2f" % vector    # rounding the float to 2 decimal numbers
            text = font.render('Distance: '+str(vector), True, (0,0,0), (255,255,255))
            self.screen.blit(text, (20,20))

            # displaying the object velocity
            display_o_velocity = "%.2f" % (math.sqrt(o_velo_x**2+o_velo_y**2))     
            text = font.render('Object velocity: ' + str(display_o_velocity), False, (0,0,0), (255,255,255))
            self.screen.blit(text, (20, 60))
            
            # display curser and object
            self.screen.blit((self.circle),(ox-RADIUS,oy-RADIUS))
            self.screen.blit((self.circle),(x-RADIUS,y-RADIUS))  

            # update the screen and set the frame-rate to 80fps
            pygame.display.update()
            self.clock.tick(80)

simulation().run()
