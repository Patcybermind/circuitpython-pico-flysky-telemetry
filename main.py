import time
import ibus
import sys
import busio
import board
import analogio

voltage_reader = analogio.AnalogIn(board.GP26)

def read_voltage():
    voltage_reading = voltage_reader.value * 3.3 / 65536
    return round(voltage_reading, 2) * 4 # rounds two more numbers after the decimal point

class IBUSsensor():
    '''Sensor class for the IBUS - the update_measurements method is used as callback on IBUS''' 
    def __init__(self):
        print("init")
        self.counter = 0

    def update_measurements(self):
        '''Needs to return an array of measurements which will be called by the IBUS update loop''' 
        #print("L16")
        self.counter += 1
        if self.counter >= 1000:
            self.counter = 0

        measurements = [self.counter]
        
        #return measurements

        print("voltage reading:", read_voltage())
        print("cell voltage:", round((read_voltage() / 2), 2))
        time.sleep(0.5)
        
        return [1, 100, (100*read_voltage()), round((read_voltage() / 2), 2)] # alt rpm extv intv


class IBUSservo():
    '''Helper class for reading servo values and doind something useful'''
    def __init__(self, channel):
        print("L27")
        self.channel = channel

    def servo_cb(self, data_arr):
        '''This is the callback function to be called by the IBUS update loop.  data_arr will be an array of PPM values per channel'''
        # Do something useful here
        if data_arr[self.channel]> 1500:
            print("On")
        else:
            print("Off")


        
# Specify the sensortypes - see ibus.py for valid values, can be an array
# The callback function for the sensor.update_measurements needs to return an array of the same length
sensor_types = [ibus.IBUSS_ALT, ibus.IBUSS_RPM, ibus.IBUSS_EXTV, ibus.IBUSS_INTV]

print('l54')

voltage_reading = voltage_reader.value
print("voltage reading:", voltage_reading)

# Instantiates the UART
#uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=ibus.PROTOCOL_GAP)
uart = busio.UART(board.GP0, board.GP1, baudrate=115200, timeout=ibus.PROTOCOL_GAP)

doSERVO = False  # set this based on whether it is a servo or sensor that is connected to the board

if not doSERVO:
    sensor = IBUSsensor()

    # instantiates the IBUS class and specifies the call back
    # the board is connected to the SENS port in this case
    ib = ibus.IBUS(uart, sensor_types, sensor.update_measurements, do_log = False)
    # now run the loop forever - on each loop, the sensor.update_measurements is called and measurements is passed to the receiver
    ib.start_loop()
else: 
    servo = IBUSservo(1)
    # instantiates the IBUS class and specifies the call back
    # the board is conected to the SERVO port in this case
    ib = ibus.IBUS(uart, sensor_types, servo_cb=servo.servo_cb, do_log=True)
    # now run the loop forever, calling servo.servo_cb when new servo values are received
    ib.start_loop()


print("Done")

