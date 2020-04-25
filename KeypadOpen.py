
import RPi.GPIO as GPIO
import Keypad       #Credit to Freenove for this code
import socket
import sys

def sendPageOpen(page):
    #establish connection
    socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketConnection.connect(('192.168.1.246',1234))

    #send url
    try :
        socketConnection.sendall(bytes(page,"utf-8"))
    except socket.error:
        #Send failed
        print ('Send failed')
        sys.exit()
    print (f'{page} send successfully')

    #Now receive data
    reply = socketConnection.recv(4096)
    print (reply)

#It's easier to refer to keys by their physical label rather than their pin input when dealing with the dictionary which pairs them to urls
keys =  ['1','2','3','A',
        '4','5','6','B',
        '7','8','9','C',
        '*','0','#','D' ]

#setting defaults so I don't have to think of 16 websites
keyToPage = { key : 'https://github.com' for key in keys}

#just a couple of examples
keyToPage['1'] = 'https://github.com'
keyToPage['2'] = 'https://youtube.com'
keyToPage['3'] = 'https://codewars.com'

rowPins = [12,16,18,22][::-1]     #wired these up backwards, whoops. Hence "[::-1]"
colPins = [7,11,13,15][::-1]

def loop():

    #initialise keypad using code from Freenove
    keypad = Keypad.Keypad(keys,rowPins,colPins,4,4)
    keypad.setDebounceTime(50)
    while(True):
        key = keypad.getKey()
        if(key != keypad.NULL):
            sendPageOpen(keyToPage[key])

if __name__ == '__main__':     #Program start from here
    print ("Program is starting ... ")

    try:
        loop()
    except KeyboardInterrupt:  #When 'Ctrl+C' is pressed, exit the program.
        GPIO.cleanup()