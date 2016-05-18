import math

# From http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/

    # Start with a temperature, in Kelvin, somewhere between 1000 and 40000.  (Other values may work,
    #  but I can't make any promises about the quality of the algorithm's estimates above 40000 K.)

    
def colorTemperatureToRGB(kelvin):

    temp = kelvin / 100

    #red, green, blue

    if( temp <= 66 ):

        red = 255
        
        green = temp
        green = 99.4708025861 * math.log(green) - 161.1195681661

        
        if( temp <= 19):

            blue = 0

        else:

            blue = temp-10
            blue = 138.5177312231 * math.log(blue) - 305.0447927307

        

    else:

        red = temp - 60
        red = 329.698727446 * math.pow(red, -0.1332047592);
        
        green = temp - 60
        green = 288.1221695283 * math.pow(green, -0.0755148492 )

        blue = 255;

    
    r = clamp(red,   0, 255)
    g = clamp(green, 0, 255)
    b = clamp(blue,  0, 255)

    return (r/255.0,g/255.0,b/255.0)

    




def clamp( x, min, max ):

    if x<min : return min
    if x>max : return max

    return x

test =  colorTemperatureToRGB(20000)
print test