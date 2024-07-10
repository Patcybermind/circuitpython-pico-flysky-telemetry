this is a circuit python program that sends telemtry using ibus to a flysky rc transmitter
its intended to run on a raspberry pi pico 
it reads a voltage from 0-3.3v on pin 26
you can get the voltage of a 2s or 3s lipo by dividing the voltage in 4 with resistors
it also reports the individual cell voltage of of a 2s lipo but you can change the / 2 to / 3 and get the corresponding voltage
