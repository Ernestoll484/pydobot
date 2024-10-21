from serial.tools import list_ports
import pydobot
import time

# List available ports and select the first one (adjust if needed)
available_ports = list_ports.comports()
print(f'Available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

# Create a Dobot instance
device = pydobot.Dobot(port=port, verbose=True)

# Set speed parameters for the Dobot
device.speed(velocity=100, acceleration=100)

# Get the current position (pose) of the Dobot
(x, y, z, r, j1, j2, j3, j4) = device.pose()
print(f'Initial position -> x:{x} y:{y} z:{z} r:{r} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

# Define positions (pickup and drop-off)
pickup_position = (x + 50, y, z - 20, r)  # Adjust these positions based on your setup
dropoff_position = (x + 70, y + 70, z - 20, r)
safe_height = z + 50  # Safe height to avoid collisions

# Function to move the block between two positions
def pick_and_place(start_position, end_position):
    # Move to safe height above start position
    device.move_to(start_position[0], start_position[1], safe_height, start_position[3], wait=True)

    # Move down to the start position
    device.move_to(start_position[0], start_position[1], start_position[2], start_position[3], wait=True)

    # Activate suction to grab the block
    device.suck(True)
    time.sleep(1)

    # Move back to safe height with the block
    device.move_to(start_position[0], start_position[1], safe_height, start_position[3], wait=True)

    # Move to safe height above end position
    device.move_to(end_position[0], end_position[1], safe_height, end_position[3], wait=True)

    # Move down to the end position
    device.move_to(end_position[0], end_position[1], end_position[2], end_position[3], wait=True)

    # Deactivate suction to release the block
    device.suck(False)
    time.sleep(1)

    # Move back to safe height
    device.move_to(end_position[0], end_position[1], safe_height, end_position[3], wait=True)

# Number of cycles to go back and forth
num_cycles = 50

for i in range(num_cycles):
    print(f"Cycle {i+1}/{num_cycles}")

    # Move object from pickup to dropoff in odd cycles
    if i % 2 == 0:
        pick_and_place(pickup_position, dropoff_position)
    # Move object from dropoff to pickup in even cycles
    else:
        pick_and_place(dropoff_position, pickup_position)

# Return to the initial position (home position)
device.move_to(x, y, z, r, wait=True)

# Close the connection
device.close()