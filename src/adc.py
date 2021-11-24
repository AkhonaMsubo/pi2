import socket
import sys
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

################TCP SEND SETUP###########################

#TODO Add code to setup the tcp connection with the correct IP and same port as the tcp_server on the other pi
    #Test this locally before trying to deploy via balena using test messages instead of ADC values
    #Use localmode when deploying to balena and use the advertised local address (using public IPs is possible but more complicated to configure due to the security measures BalenaOS imposes by default.  These are a good thing for real world deployment but over complicate the prac for the immediate purposes


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HostName = socket.gethostname()
    hostIP = socket.gethostbyname(myHostName)
    s.bind((hostIP, PORT))
    s.listen()
    # Waiting for a device to connect
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print('\nReceived', repr(data.decode()))
            f.write("\nReceived: ")
            f.write(repr(data.decode()))
            f.flush()
            if not data:
                break





##################ADC Setup##############################

#TODO using the adafruit circuit python SPI and MCP libraries setup the ADC interface
#Google will supply easy to follow instructions 


currentRate = 10;
counter = 0;

toggle_rate = [10, 5, 1]

def calculateRate():
    global currentRate
    if (currentRate == 10):
        currentRate == 5
    elif (currentRate == 5):
        currentRate == 1
    elif (currentRate == 1):
        currentRate == 10
    

def setup():
    #Contains all code for initialisation of RPi.GPIO
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main(): 
    while True:
        if GPIO.input(17) == GPIO.HIGH:
            calculateRate()
            time.sleep(1)
        x = threading.Thread(target=fetch_sensor_vals)
        # print("Starting thread")
        x.start()
        # print("Waiting for the thread to finish")
        x.join()
     
# create the spi bus
def fetch_sensor_vals():
    global currentRate, counter
    threading.Timer(currentRate, fetch_sensor_vals).start()
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)
    chan2 = AnalogIn(mcp, MCP.P3)
    temparature = ((chan.voltage) * 1000)
    print("{:<8} {:<15} {:<20} {:<20}".format(str(counter)+"s", chan.value, str(round(temparature, 3))+ "C", chan2.value))
    counter += currentRate






#########################################################

print("Sensor Node it awake\n")     #Print statements to see what's happening in balena logs
f.write("Sensor Node it awake\n")   #Write to file statements to see what's happening if you ssh into the device and open the file locally using nano
f.flush()
s.send(b'Sensor Node it awake\n')   #send to transmit an obvious message to show up in the balena logs of the server pi

while(True):
   



    #TODO add code to read the ADC values and print them, write them, and send them





    
    time.sleep(5)


