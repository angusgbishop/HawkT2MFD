from math import *

def get_tens(number):
    number = int(number * 10)
    number = float(number) / 10
    number = number // 10
    number = number % 10
    return number

def get_units(number):
    number = int(number * 10)
    number = float(number) / 10
    number = number % 10
    numberdiv = number // 1
    return numberdiv

def pol2cart(rho,phi):
    x = rho * cos(radians(phi))
    y = rho * sin(radians(phi))
    return(x,y)

def cart2pol(x,y):
    rho = sqrt(x**2 + y**2)
    phi = degrees(atan2(y,x))
    return(rho,phi)

def line_coords(length,midpoint,angle):
    # Returns the endpoint coordinates of a line given the midpoint, angle and length.
    midx = midpoint[0]
    midy = midpoint[1]

    y_distance = length * sin(radians(angle))
    x_distance = length * cos(radians(angle))

    x0 = midx - x_distance
    y0 = midy - y_distance
    x1 = midx + x_distance
    y1 = midy + y_distance

    return(x0,y0,x1,y1)

def getMidpoint(x0,y0,x1,y1):
    xmid = sum(x0,x1)/2
    ymid = sum(y0,y1)/2
    return (xmid,ymid)

def change_page(page):
    return
