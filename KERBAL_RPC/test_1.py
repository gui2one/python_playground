import os
import krpc
import time

## clear the terminal screen
os.system('cls')


WINDOW_WIDTH = 200
WINDOW_HEIGHT = 500
## connection to krpc server
conn = krpc.connect(name="hello")
print 'Connected to krpc server -- version', conn.krpc.get_status().version


## find active vessel
try:
    vessel = conn.space_center.active_vessel
    print ("active vessel ->", vessel.name)
    # for item in dir(vessel.parts):
    #     print item


except:
    vessel = None
    print ('no active vessel')

# for item in dir(conn):
#     print (item)
ui = conn.ui

canvas = conn.ui.stock_canvas

# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size

# Add a panel to contain the UI elements
panel = canvas.add_panel()

# Position the panel on the left of the screen
rect = panel.rect_transform
rect.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
rect.position = (110 - (screen_size[0] / 2), 0)
rect.position = (0, 0)

close_button = panel.add_button("X")
close_button.rect_transform.size = (20,20)
close_button.rect_transform.position = ((WINDOW_WIDTH / 2.0) - 10, (WINDOW_HEIGHT/2.0) - 10)

# Add a button to set the throttle to maximum

ignition_button = panel.add_button("Ignition")
ignition_button.rect_transform.position = (0, (WINDOW_HEIGHT/2.0)-40)

# Add some text displaying the total engine thrust
text = panel.add_text("Thrust: 0 kN")
text.rect_transform.position = (0, -60)
text.color = (1, 1, 1)
text.size = 18

# Set up a stream to monitor the throttle button
close_button_clicked = conn.add_stream(getattr, close_button, 'clicked')
ignition_button_clicked = conn.add_stream(getattr, ignition_button, 'clicked')

# vessel = conn.space_center.active_vessel
while True:
    # Handle the throttle button being clicked

    text.content = vessel.name
    if close_button_clicked():
        ui.clear()
        if vessel :
            pass
            # Update the thrust text
            # text.content = 'Thrust: %d kN' % (vessel.thrust / 1000)
    
    if ignition_button_clicked():
        vessel.control.throttle = 1
        vessel.control.activate_next_stage()
            
        ignition_button.clicked = False



    time.sleep(0.1)
