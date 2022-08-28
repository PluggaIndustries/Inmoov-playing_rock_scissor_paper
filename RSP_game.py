#!/usr/bin/env python3
# Import the necessary libraries
import rospy # Python library for ROS
from sensor_msgs.msg import Image # Image is the message type
from std_msgs.msg import UInt16MultiArray # Image is the message typ
from std_msgs.msg import String
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import time
from cvzone.HandTrackingModule import HandDetector
import pyttsx3
import random
global txt
detector = HandDetector(detectionCon=0.8, maxHands=2)




def callback_hand(data):   # CALLBACK PER OGNI FRAME DL VIDEO: AGGIORNA VALORE DITA IN CONTINUO
  global txt
  br = CvBridge()
  frame = br.imgmsg_to_cv2(data)
  image = cv2.flip(frame, 1)
  hands, image = detector.findHands(image)

  # liste per il confronto con i valori del detector
  scissor_hand= [0,1,1,0,0]
  rock_hand =[0,0,0,0,0]
  paper_hand= [1,1,1,1,1]

  if hands:
    hand1 = hands[0]
    fingers1 = detector.fingersUp(hand1)
    if fingers1 ==rock_hand:
        fingers_txt = "rock" # sasso
    elif fingers1 == scissor_hand:
        fingers_txt = "scissor" #forbice
    elif fingers1 ==paper_hand:
        fingers_txt = "paper" #carta
    cv2.putText(image, txt, ( 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 0))
  cv2.imshow("camera",image)
  cv2.waitKey(1)
  
def callback_init_game(stringa):  # CALLBACK SU init_game: FA INIZIARE IL GIOCO 
    say(stringa)
    #PRENDE DALLA VAR fingers_txt AGGIORANTA DALLA CALLBACK PRIMA
    global fingers_txt    
    pub = rospy.Publisher('hand_pos', UInt16MultiArray, queue_size=1)
    pos = UInt16MultiArray() 
    game_list = ["rock","scissor","paper"]
    say("Start")
    time.sleep(1)
    say("One")
    time.sleep(1)
    say("Two")
    time.sleep(1)
    say("Three")
    # Creo gli array di uint16 da inviare al topic hand_pos in base al valore scelto con random.choice
    value = random.choice(game_list)
    if value == "rock":
       for x in range(0,5):
           pos.data.insert(0,0)

    if value == "scissor":
       pos.data.insert(0,0)
       for x in range(0,2):
           pos.data.insert(0,180)
       for x in range(0,2):
           pos.data.insert(0,0)

    if value == "paper":
       for x in range(0,5):
           pos.data.insert(0,180)
      
    pub.publish(pos)  
    
    time.sleep(1)
    say("Let me check") # Aspetto il tempo che ci mette il detector ad analizzare il frame
    time.sleep(2)

    # Confronto tra la mossa del giocatore e quella scelta dal robot e dice il risultato
    if value == fingers_txt :
      say("Draw, both "+ value+".")

    if (value == "rock") & (fingers_txt =="paper"):
      say("I choosed "+ value +". You choosed paper. You won!")

    if (value == "paper") & (fingers_txt =="scissor"):
      say("I choosed "+ value +". You choosed scissor. You won!")

    if (value == "scissor") & (fingers_txt =="rock"):
      say("I choosed "+ value +". You choosed rock. You won!")

    if (value == "paper") & (fingers_txt =="rock"):
      say("I choosed "+ value +". You choosed rock. You lost!")

    if (value == "scissor") & (fingers_txt =="paper"):
      say("I choosed "+ value +". You choosed paper. You lost!")

    if (value == "rock") & (fingers_txt =="scissor"):
      say("I choosed "+ value +". You choosed scissor. You lost!")
    time.sleep(1)
    say("Game over!")

def say(command): # utilizza il sintetizzatore vocale
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    print(command)

def listen_to_start():
  say("Let's play")
  rospy.init_node('RSP_game_py', anonymous=True)
  rospy.Subscriber('video_frames', Image, callback_hand) # callback per ogni frame
  rospy.Subscriber('init_game', String, callback_init_game) # callback del flusso di gioco
  cv2.destroyAllWindows()
  rospy.spin() # come un while continua ad eseguire il codice si questa funzione

if __name__ == '__main__':
  listen_to_start()
