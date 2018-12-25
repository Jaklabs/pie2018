RIGHT_MOTOR = "47254706228722534413181"
LEFT_MOTOR = "47244718417202768690407"
TURBINE = "47254105330025864485435"
BACK_WINCH = "47253128800291380627357"
#OVERHEAD_WINCH = "47259479521452806531346"

async def turn_cw(seconds): # Or, "turn right"
    Robot.set_value(LEFT_MOTOR, "duty_cycle", -0.5)
    Robot.set_value(RIGHT_MOTOR, "duty_cycle", -0.5)
    await Actions.sleep(seconds)
    Robot.set_value(LEFT_MOTOR, "duty_cycle", 0)
    Robot.set_value(RIGHT_MOTOR, "duty_cycle", 0)
    
async def turn_ccw(seconds): # Or, "turn left"
    Robot.set_value(LEFT_MOTOR, "duty_cycle", 0.5)
    Robot.set_value(RIGHT_MOTOR, "duty_cycle", 0.5)
    await Actions.sleep(seconds)
    Robot.set_value(LEFT_MOTOR, "duty_cycle", 0)
    Robot.set_value(RIGHT_MOTOR, "duty_cycle", 0)

async def drive(seconds): # Or, "move forward"
    Robot.set_value(LEFT_MOTOR, "duty_cycle", 0.5)
    Robot.set_value(RIGHT_MOTOR, "duty_cycle", -0.5)
    print("Driving forward...")
    await Actions.sleep(seconds)
    Robot.set_value(LEFT_MOTOR, "duty_cycle", 0)
    Robot.set_value(RIGHT_MOTOR, "duty_cycle", 0)
    print("Parked!")
    

async def reverse(seconds): # Or, "move backwards"
    Robot.set_value(LEFT_MOTOR, "duty_cycle", 0.5)
    Robot.set_value(RIGHT_MOTOR, "duty_cycle", -0.5)
    await Actions.sleep(seconds)
    Robot.set_value(LEFT_MOTOR, "duty_cycle", 0)
    Robot.set_value(RIGHT_MOTOR, "duty_cycle", 0)

async def turbine_procedure(speed):
    Robot.set_value(TURBINE, "duty_cycle", speed)
    print("Sweping at %f" %speed)

def autonomous_setup():
    Robot.run(drive, 4.0) # Drive forward into the ball pit for 4 seconds...
    print("Driving to the balls!")
    
def autonomous_main():
    Robot.run(turbine_procedure, -1.0)
    print("Scooping!")

async def teleop_actions():  # Async function for controller logic.
     # Multiply any motor values by these.
    lmc = -1.0 # All left pulse values must be inverted. 
    rmc = 1.0
    
    # --- LEFT MOTOR LOGIC ---
    if Gamepad.get_value("joystick_left_y") != 0.0: # If left joystick moves up or down: 
        Robot.set_value(LEFT_MOTOR, "duty_cycle", lmc * Gamepad.get_value("joystick_left_y"))
        print("Left motor at %i" %Gamepad.get_value("joystick_left_y"));
        # Both motors will move proportionally to the push of the joystick.
        # To go faster, push harder. 
        # To go backwards, pull joystick.
    else: # If the left joystick is centered:
        Robot.set_value(LEFT_MOTOR, "duty_cycle", 0.0)
        # Stop the left motor.
    
    # --- RIGHT MOTOR LOGIC --- 
    # Same principle w/ right side instead of left...
    if Gamepad.get_value("joystick_right_x") != 0.0: #If right joystick moves right or left:
        Robot.set_value(RIGHT_MOTOR, "duty_cycle", rmc * Gamepad.get_value("joystick_right_y"))
        print("Right motor moving at %i" %Gamepad.get_value("joystick_right_y"));
    else:
        Robot.set_value(RIGHT_MOTOR, "duty_cycle", 0.0)
    
    # IN ORDER TO DRIVE:
    # Push/pull both in same direction to drive forward/backwards
    # Push/pull in opposite directions to turn on axis
    
    # ACTIVATE TURBINE - SLOW MODE
    if Gamepad.get_value("button_a"): 
        Robot.run(turbine_procedure, 0.25)
        print("Spitting slow!")

    # ACTIVATE TURBINE - FAST MODE  
    elif Gamepad.get_value("button_b"):
        Robot.run(turbine_procedure, 1.0)
        print("Spitting fast!")
        
    # ACTIVATE TURBINE - REVERSE - SLOW MODE
    elif Gamepad.get_value("button_x"):
        Robot.run(turbine_procedure, -0.25)
        print("Sucking slow!")
        
    # ACTIVATE TURBINE - REVERSE - FAST MODE
    elif Gamepad.get_value("button_y"):
        Robot.run(turbine_procedure, -1.0)
        print("Sucking fast!")
        
    # DEACTIVATE TURBINES  / if not Gamepad.get_value("button_y") and not Gamepad.get_value("button_x") and not Gamepad.get_value("button_b") and not Gamepad.get_value("button_a"):
    else:
        # If no face buttons are pressed:
        Robot.run(turbine_procedure, 0) # Deactivate the turbine.
        print("Turbine is still.")
    
    
    # ELEVATOR LOGIC
    if Gamepad.get_value("l_bumper"):
        print("Winch...")
        Robot.set_value(BACK_WINCH, "duty_cycle", -0.5) # Turn back winch with negative pulse
        # (DROP ELEVATOR)
    else:
        Robot.set_value(BACK_WINCH, "duty_cycle", 0) # Stop elevator
        
    if Gamepad.get_value("r_bumper"):
        if Gamepad.get_value("r_trigger"): # If holding right bumper AND trigger:
            Robot.set_value(OVERHEAD_WINCH, "duty_cycle", 0.75) # Turn overhead winch on FAST
            Robot.set_value(BACK_WINCH, "duty_cycle", 0.5) # Turn back winch w/ positive pulse
            await Actions.sleep(1.0)
            Robot.set_value(OVERHEAD_WINCH,"duty_cycle",0)
            Robot.set_value(BACK_WHINCH,"duty cycle",0.5)
        else: # If JUST holding right trigger
            print("Winch...")
            Robot.set_value(BACK_WINCH, "duty_cycle", 0.5) # Just raise elevator
    else:
        Robot.set_value(BACK_WINCH, "duty_cycle", 0)
    
    if Gamepad.get_value("l_trigger"):
        
        Robot.set_value(OVERHEAD_WINCH, "duty_cycle", 0.25)
    else:
        Robot.set_value(OVERHEAD_WINCH, "duty_cycle", 0)
        
    if Gamepad.get_value("r_trigger") and not Gamepad.get_value("r_button"):
        # Turn overhead winch on SLOW
        
        Robot.set_value(OVERHEAD_WINCH, "duty_cycle", 0.25)
    else:
        Robot.set_value(OVERHEAD_WINCH, "duty_cycle", 0)
        
    '''
    BUMPER: Moves elevator winch up and down
    TRIGGERS: Makes elevator open and close
    '''
def teleop_setup():
    print("Tele-op mode has started!")
    
def teleop_main(): # Subscribe to @InfiniteHoops
    Robot.run(teleop_actions) # Controller logic runs in an async function 
