import cv2
import numpy as np
import serial
import struct

# weaker red
red_l_l = np.array([0, 70, 70])
red_h_l = np.array([10, 255, 255])
#bigger red
red_l_h = np.array([170, 100, 100])
red_h_h = np.array([180, 255, 255])

blue_l = np.array([110,70,70])
blue_h = np.array([130,255,255])

isRed = False if np.random.randint(0, 2) == 0 else True;

def color_threshold(frame, draw=None):

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # define range of blue color in HSV
    frame = cv2.bilateralFilter(frame, 9, 75, 75)
    
    maskRL = cv2.inRange(hsv, red_l_l, red_h_l)
    maskRH = cv2.inRange(hsv, red_l_h, red_h_h)
    maskB = cv2.inRange(hsv, blue_l, blue_h)
    
    if isRed:
        _, cntL, _ = cv2.findContours(maskRL, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        _, cntH, _ = cv2.findContours(maskRH, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        _, cntL, _ = cv2.findContours(maskRL, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
            

    maxSize = 0
    maxCnt = None
    for cnt in cntL:
        if cnt.size > maxSize:
            maxSize = cnt.size
            maxCnt = cnt
        
    if isRed:
        for cnt in cntH:
            if cnt.size > maxSize:
                maxSize = cnt.size
                maxCnt = cnt
                m = cv2.bitwise_and(frame, frame, maskRH)
    if isRed:
        m = cv2.bitwise_and(frame, frame, mask=maskRH)
    else:
        m = cv2.bitwise_and(frame, frame, mask=maskB)
    if maxCnt is not None:
        x,y,w,h = cv2.boundingRect(maxCnt)
        tag_center = (2*x+w)//2
        print(isRed)
        cv2.drawContours(m, maxCnt, -1, (255,255,255), 3)
        cv2.imshow(draw, m)
    else:
        tag_center = -1
    print("x = ", tag_center)
    return tag_center


def main():
    
    try:
        ser = serial.Serial('COM2', 9600, 8, 'N', 1, timeout=1) # replace w/ real port
        ser.flushInput()
    except:
        print("Serial aint open")
    
    cam = 0
    window = "Tech Demo"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    print(type(window))
    cap = cv2.VideoCapture(cam)
    cap.open(cam)
   
    while True:
        try:
            ret, frame = cap.read()
            #s = ser.readline()
            if frame is not None:
                x = color_threshold(frame, window);
                #ser.write(struct.pack('>B', x))
            #if ser.in_waiting > 0:
                #isRed = not isRed    
                    
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                print(k)
                seppuku = True
                cv2.destroyAllWindows()
                cap.release()
                s.close()
                break
                
        except Exception as e:
            print(e)
            seppuku = True
            cv2.destroyAllWindows()
            cap.release()
            #ser.close()
            break
        
if __name__ == '__main__':
    main()
