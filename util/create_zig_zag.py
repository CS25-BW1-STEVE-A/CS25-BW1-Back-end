from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

'''
Fill up the grid, bottom to top, in a zig-zag pattern
'''

# Initialize the grid
grid = [None] * 10
width = 10
height = 10
for i in range(len(grid)):
    grid[i] = [None] * 10

# Start from lower-left corner (0,0)
x = -1  # (this will become 0 on the first step)
y = 0
room_count = 0

# Start generating rooms to the east
direction = 1  # 1: east, -1: west

# While there are rooms to be created...
previous_room = None
while room_count < 100:

    # Calculate the direction of the room to be created
    if direction > 0 and x < 10 - 1:
        room_direction = "e"
        room_rev_dir = "w"
        x += 1
    elif direction < 0 and x > 0:
        room_direction = "w"
        room_rev_dir = "e"
        x -= 1
    else:
        # If we hit a wall, turn north and reverse direction
        room_direction = "n"
        room_rev_dir = "s"
        y += 1
        direction *= -1

    # Create a room in the given direction
    room = Room(title="A Generic Room", description="This is a generic room.", x=x, y=y)
    room.save()
    # Note that in Django, you'll need to save the room after you create it

    # Save the room in the World grid
    grid[y][x] = room

    # Connect the new room to the previous room
    if previous_room is not None:
        previous_room.connectRooms(room, room_direction)
        room.connectRooms(previous_room, room_rev_dir)

    # Update iteration variables
    previous_room = room
    room_count += 1

  
players=Player.objects.all()
for p in players:
  p.currentRoom=Room.objects.all()[0].id
  p.save()
