import cv2, imutils, socket
import numpy as np
import time
import base64
import threading
import pygame
import os


changed = False
pygame.init()
os.system('cls')
current_command = ''
#initialize all pygame objects
white, green, red, blue = (255, 255, 255), (0, 255, 0),(255, 0, 0),(0, 0, 128)
X = 650
Y = 450
scrn = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
input_box = pygame.Rect(220, 240, 140, 32)
pygame.display.set_caption('Camera System')
font = pygame.font.Font(None, 32)
image = ''
text = ''
msg = ''
clock = pygame.time.Clock()
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
host_ip = '192.168.2.72'   #socket.gethostbyname(host_name)
commandport = 5000
videoport = 5001


def cvimage_to_pygame(opencv_image):
    #converts opencv image data to pygame image data
    opencv_image = opencv_image[:,:,::-1]  #Since OpenCV is BGR and pygame is RGB, it is necessary to convert it.
    shape = opencv_image.shape[1::-1]  #OpenCV(height,width,Number of colors), Pygame(width, height)So this is also converted.
    pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')

    return pygame_image


def udp_serversession(i, x, y):
    #udp socket session
    BUFF_SIZE = 65536
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    host_name = socket.gethostname()
    
    message = b'Hello'
    port = 5000 + i
    socket_address = (host_ip,port)
    server_socket.bind(socket_address)
    print(f'[WAITING] Listening at {socket_address[0]}:{socket_address[1]}')

    #video stuff
    vid = cv2.VideoCapture(0)
    fps,st,frames_to_count,cnt = (0,0,20,0)

    

    while True:
                txt = font.render('Laser Turret Stream', True, green, blue)
                textRect = txt.get_rect()
                textRect.center = (450, 50)
                scrn.blit(txt, textRect)
                packet,_ = server_socket.recvfrom(BUFF_SIZE)
                data = base64.b64decode(packet,' /')
                try:
                    npdata = np.fromstring(data,dtype=np.uint8)
                except:
                    pass
                frame = cv2.imdecode(npdata,1)
                frame = cv2.flip(frame, 0)
                frame = cv2.flip(frame, 1)
                frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_DUPLEX,0.7,(0,0,255),2)
                #cv2.imshow(f"Stream {i}",frame)
                
                image = cvimage_to_pygame(frame)
                
                scaled = pygame.transform.scale(image, (500, 500))
                
                position = (x / 2, y-25)

                scrn.blit(scaled, position)
                pygame.display.update()
                '''
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                        client_socket.close()
                        break
                '''
                
                if cnt == frames_to_count:
                        try:
                                fps = round(frames_to_count/(time.time()-st))
                                st=time.time()
                                cnt=0
                        except:
                                pass
                cnt+=1
                
def commands():
    global changed
    global msg
    addr = ('192.168.2.11', 5000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    while True:
        if changed == True:
            message = msg.encode('utf-8')
            client.send(message)
            print('Message Sent')
            changed = False
            

def menu():
        global changed
        global msg
        running = True
        scrn.fill((30, 30, 30))
        pygame.display.update()
        #video menu text
        
        #video streams
        print(f'[NOTICE] Video Listener initialized...\n')
        t1 = threading.Thread(target=udp_serversession, args=[1, 400, 100])
        t1.start()
        t2 = threading.Thread(target=commands)
        t2.start()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        try:
                            print('DownKey')
                            msg = 'Down'
                            changed = True
                        except:
                            print('error')
                                
                    if event.key == pygame.K_UP:
                        try:
                            print('UpKey')
                            msg = 'Up'
                            changed = True
                        except:
                            print('error')

                    if event.key == pygame.K_RIGHT:
                        try:
                            print('RightKey')
                            msg = 'Right'
                            changed = True
                        except:
                            print('error')

                    if event.key == pygame.K_LEFT:
                        try:
                            print('LeftKey')
                            msg = 'Left'
                            changed = True
                        except:
                            print('error')

                    if event.key == pygame.K_RETURN:
                        try:
                            print('Enter')
                            msg = 'Enter'
                            changed = True
                        except:
                            print('error')
                            


def main():
    global client_count
    #main menu
    text = ''
    X = 1000
    Y = 450
    error = False
    '''
    for i in range(1, (int(client_count) + 1)):
        print(f'\n\n[NOTICE] Listener {i} initialized...\n')
        t1 = threading.Thread(target=udp_serversession, args=[i])
        t1.start()
        time.sleep(1)
    '''
    #cv2 and text stuff
    running = True
    txt = font.render('Turret Control', True, red, color)
    txt2 = font.render(f'Host IP:{host_ip}        Ports:{commandport}, {videoport}', True, red, color)
    txt3 = font.render('Press Enter to Begin', True, red, color)
    textRect = txt.get_rect()
    textRect.center = (400, 100)
    textRec2t = txt2.get_rect()
    textRec2t.center = (400, 200)
    textRec3t = txt2.get_rect()
    textRec3t.center = (500, 300)
    while running:
          

          
          pygame.display.flip()
    
          
          for event in pygame.event.get():
                  
                  
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            try:
                                running = False
                                menu()
                            except ValueError:
                                print('Error')
                            text = ''
                        
          if running:                 
              scrn.fill((30, 30, 30))
              txt_surface = font.render(text, True, color)
              width = max(200, txt_surface.get_width()+10)
              input_box.w = width
              if error:
                 textRect.center = (388, 220)
          
              scrn.blit(txt, textRect)
              scrn.blit(txt2, textRec2t)
              scrn.blit(txt3, textRec3t)
              
          
main()

