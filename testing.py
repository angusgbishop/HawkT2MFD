from functions import *
from json import *
from data_grabber import *
from time import sleep

def testing_run():
    while True:
        for x in range (1,200):
            y = round(x/200,3)
            write_var("engine_rpm_percentage",y)
            write_var("egt",y)
            write_var("port_fuel",int(1020*y))
            write_var("stbd_fuel",int(1020*y))
            write_var("total_fuel",int(4900*y))
            write_var("fuel_flow",int(60*y))
            write_var("pitch",180*(y-0.5))
            write_var("roll",degrees(cos(30*y)))
            write_var("hdg",360*y)
            sleep(0.01)

if __name__ == "__main__":
    testing_run()