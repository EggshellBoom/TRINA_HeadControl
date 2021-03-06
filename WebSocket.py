import sys
import time
import websocket
from threading import Thread
import time
import sys
import json
import numpy as np
from scipy.spatial.transform import Rotation as R
from servoController import servoController
roomname = "The Lobby"
zonename = "BasicExamples"
userId=0
roomId=-1
is_closed=0

def to_rotvec(orientation):
    # print("quat",orientation)
    right_handed_rotvec =  np.array([-orientation[2],orientation[0],-orientation[1],-(np.pi/180)*orientation[3]])

    partial_rotation = R.from_rotvec(right_handed_rotvec[:3]*right_handed_rotvec[3])
    # we then get its equivalent row, pitch and yaw
    rpy = partial_rotation.as_euler('ZYX',degrees=True)
    rpy2 = partial_rotation.as_euler('YZX',degrees=True)
    return {"y":rpy[0],"x":rpy2[0]}


def on_message(ws, message):
    global userId,roomId,drone,roomname, zonename
    global is_closed
    global servoController
    mjson = json.loads(message)
    if mjson["a"]==0:
       a= {"a":1,"c":0,"p":{"zn": zonename,"un":"","pw":""}}
       b= json.dumps(a).encode('utf-8')
       ws.send(b)

    if mjson["a"]==1:
       if 'id' in mjson["p"]:
           print ("userId: %d" % mjson["p"]["id"])
           userId = mjson["p"]["id"]
           a={"a":4,"c":0,"p":{"n":roomname}}
           b= json.dumps(a).encode('utf-8')
           ws.send(b)

    if mjson["a"]==1001: #Once after room jon sending welcome message
       if roomId ==-1:
           roomId = mjson["p"]["r"]
           print ("Room id :::: '%s'" % roomId)
        
           #sending public messages  
           a={"a":7,"c":0,"p":{"t":0,"r":roomId,"u":userId,"m":"controllers","p":{"LeftRotation":{"x":0.1,"y":0.2,"z":0.3},"LeftPosition":{"x":1.1,"y":1.2,"z":1.3},"RightRotation":{"x":2.1,"y":2.2,"z":2.3},"RightPosition":{"x":3.1,"y":3.2,"z":3.3}}}}
           b= json.dumps(a).encode('utf-8')
           ws.send(b)

                                           
    if mjson["a"]==7:  #Retrieve public message
       if mjson["p"]["m"]=="controllers" and mjson["p"]["r"]==roomId:
          orientation = to_rotvec(mjson["p"]["p"]["headSetPositionState"]["deviceRotation"])
          print(orientation)
          servoController.setGoal(orientation)


          
     


def on_error(ws, error):
    print(error)


def on_close(ws):
    global is_closed
    global servoController
    servoController.shutdown()
    is_closed=1
    print("### closed ###")


def on_open(ws):
    def run(*args):
        global is_closed
        a = {"a":0,"c":0,"p":{"api":"1.2.0","cl":"JavaScript"}}
        b =json.dumps(a).encode('utf-8')
        print(b)
        ws.send(b)

        while is_closed==0:
              time.sleep(1)
        time.sleep(1)
        ws.close()
        print("Thread terminating...")

    Thread(target=run).start()




if __name__ == "__main__":
    global servoController
    servoController = servoController()
    websocket.enableTrace(True)
    host = "ws://gametest.vrotors.com:8888/websocket"
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

###

