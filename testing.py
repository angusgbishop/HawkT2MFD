from functions import *
from json import *
from data_grabber import *
from time import sleep

def testing_run():
    while True:
        for x in range (1,100):
            y = round(x/100,3)
            write_var("engine_rpm_percentage",y)
            write_var("egt",y)
            write_var("port_fuel",int(1020*y))
            write_var("stbd_fuel",int(1020*y))
            write_var("total_fuel",int(4900*y))
            write_var("fuel_flow",int(60*y))
            write_var("pitch",70*(y-0.5))
            sleep(0.01)

if __name__ == "__main__":
    testing_run()