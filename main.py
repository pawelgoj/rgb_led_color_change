import machine
import utime
import _thread
import os

global button_change_color
button_change_color: machine.Pin = machine.Pin(11, machine.Pin.IN,
                                               machine.Pin.PULL_DOWN)

global button_on_off
button_on_off: machine.Pin = machine.Pin(12, machine.Pin.IN,
                                         machine.Pin.PULL_DOWN)

global state_of_button_change_color
state_of_button_change_color: str = 'b'

global button_on_off_pressed
button_on_off_pressed: bool = False 


def load_saved_colors_form_file() -> tuple[dict, bool]:
    """Loads saved colors from file data.txt, if file does not exist returns: 
        colors = {'b': 0, 'g': 0, 'r': 0} and first_run = True. 

    Returns:
        tuple[dict, bool]: ({'b': 0, 'g': 0, 'r': 0}, first_run)
    """
    
    colors = {'b': 0, 'g': 0, 'r': 0}
    first_run = True
    
    for item in os.listdir():
        if 'data.txt' == f'{item}':
            with open('data.txt', 'r') as file:
                string_data = file.read()
                splitted = string_data.split(' ')
                
                colors['b'] = int(splitted[0])
                colors['g'] = int(splitted[1])
                colors['r'] = int(splitted[2])
                
                del string_data
                first_run = False
    
    return colors, first_run


def button_change_color_fn(recent: int|None, state_of_button_change_color: str, 
                        iteration: int, after_saved: bool) -> tuple[int|None, str, int, bool]:
    """Function specifying the state of the color change button

    Args:
        recent (int): the binary state of the button (pressed down: 1, release: 0) during 
        an earlier iteration 
        state_of_button_change_color (str): colors 'r', 'g', 'b' or 'save', 'loaded'
        iteration (int): iteration 
        after_saved (bool): Was the previous state_of_button_change_color 'save'? True/False

    Returns:
        tuple(recent, state_of_button_change_color, iteration, after_saved)
    """
    
    if button_change_color.value() == 1:
        iteration+= 1
    else:
        iteration = 0
        
    if (button_change_color.value() == 0 and after_saved):
        after_saved = False
        state_of_button_change_color = 'loaded'
        
    elif (button_change_color.value() == 0 and recent != button_change_color.value()
        and iteration < 100): 
        if state_of_button_change_color == 'b':
            state_of_button_change_color = 'g'
        elif state_of_button_change_color == 'g':
            state_of_button_change_color = 'r'
        elif state_of_button_change_color == 'r':
            state_of_button_change_color = 'b'
        elif state_of_button_change_color == 'save':
            state_of_button_change_color = 'loaded'
        elif state_of_button_change_color == 'loaded':
            state_of_button_change_color = 'b'
            
    elif iteration >= 100:
        state_of_button_change_color = 'save'
        after_saved = True
        
    recent = button_change_color.value() 
    
    return recent, state_of_button_change_color, iteration, after_saved


def button_on_off_thread() -> None:
    """The thread for handling button events
    """
    
    global button_on_off_pressed
    global state_of_button_change_color
    
    recent = 0
    recent_rgb =  0
    iteration = 0
    after_saved = False
    
    while True:
        if (button_on_off.value() == 1 and button_on_off_pressed == False 
        and recent != button_on_off.value()):
            button_on_off_pressed = True

        elif (button_on_off.value() == 1 and button_on_off_pressed == True 
        and recent != button_on_off.value()):
            button_on_off_pressed = False
            
        recent = button_on_off.value()
        recent_rgb, state_of_button_change_color , iteration, after_saved =\
            button_change_color_fn(recent_rgb, state_of_button_change_color, 
                                   iteration, after_saved)
        utime.sleep(0.01)


potentiometer: machine.ADC = machine.ADC(26)


led_b: machine.PWM = machine.PWM(machine.Pin(15))
led_g: machine.PWM = machine.PWM(machine.Pin(14))
led_r: machine.PWM = machine.PWM(machine.Pin(13))

led_b.freq(1000)
led_g.freq(1000)
led_r.freq(1000)

colors, first_run = load_saved_colors_form_file()

state_of_button_change_color = 'b' if first_run else 'loaded'

#thread with handling buttons events 
_thread.start_new_thread(button_on_off_thread, ())

temp_colors = [colors['b'], colors['g'], colors['r']]


while True:
    result: int = (0 if potentiometer.read_u16() < 300 else potentiometer.read_u16())
    
    if button_on_off_pressed and (state_of_button_change_color == 'b'):
        temp_colors[0] = result
        led_b.duty_u16(result)
        
    elif button_on_off_pressed and state_of_button_change_color == 'g':
        temp_colors[1] = result
        led_g.duty_u16(result)
        
    elif button_on_off_pressed and state_of_button_change_color == 'r':
        temp_colors[2] = result
        led_r.duty_u16(result)
        
    elif button_on_off_pressed and state_of_button_change_color == 'save':
        first_run = False
        colors['b'] = temp_colors[0]
        colors['g'] = temp_colors[1]
        colors['r'] = temp_colors[2]
        
        with open('data.txt', 'w') as file:
            string_to_file = f"{colors['b']} {colors['g']} {colors['r']}"
            file.write(string_to_file)

    elif button_on_off_pressed == True and state_of_button_change_color == 'loaded':
        led_b.duty_u16(colors['b'])
        led_g.duty_u16(colors['g'])
        led_r.duty_u16(colors['r'])
        
    elif button_on_off_pressed == False and not first_run:
        led_b.duty_u16(0)
        led_g.duty_u16(0)
        led_r.duty_u16(0)
        state_of_button_change_color = 'loaded'
        
    elif button_on_off_pressed == False and first_run:
        led_b.duty_u16(0)
        led_g.duty_u16(0)
        led_r.duty_u16(0)