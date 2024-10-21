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
pickup_position = (x - 50, y, z - 87, r)  # Adjust these positions based on your setup
dropoff_position = (x + 20, y + 40, z - 87, r)  # Initial drop-off position
safe_height = z + 50  # Safe height to avoid collisions

# Function to move the block from pickup to the drop-off location
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

    # Move down to the end position to place the block
    device.move_to(end_position[0], end_position[1], end_position[2], end_position[3], wait=True)

    # Deactivate suction to release the block
    device.suck(False)
    time.sleep(1)

    # Move back to safe height
    device.move_to(end_position[0], end_position[1], safe_height, end_position[3], wait=True)

# Number of blocks to stack
num_blocks = 5
block_height = 30  # Adjust this value based on the height of the blocks

for i in range(num_blocks):
    print(f"Placing block {i+1}/{num_blocks}")

    # Calculate the current drop-off height for each block in the tower
    current_dropoff_position = (dropoff_position[0], dropoff_position[1], dropoff_position[2] + i * block_height, dropoff_position[3])

    # Pick up the block and place it at the new drop-off position
    pick_and_place(pickup_position, current_dropoff_position)

# Return to the initial position (home position)
device.move_to(x, y, z, r, wait=True)

# Close the connection
device.close()
