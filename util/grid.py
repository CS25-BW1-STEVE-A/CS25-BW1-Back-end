import math
from random import random
from django.contrib.auth.models import User
from adventure.models import Player, Room

class Grid:
    def __init__(self, dimensions=50, maxTunnels=500, maxLength=8):
        self.dimensions = dimensions
        self.maxTunnels = maxTunnels
        self.maxLength = maxLength
        self.grid = self.createGrid(dimensions)  # Create the grid
        self.currentRow = 25  # random start X
        self.currentCol = 25  # random start Y
        # top, right, bottom, left as [y, x] coordinates
        self.directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        self.lastDirection = [0, 0]  # save the last direction
        self.randomDirection = [0, 0]
    def createGrid(self, dimensions, num=0):
        # Temp: Delete all the existing Rooms
        # Create an empty array and init with all "walls"
        a = []
        for i in range(0, dimensions):
            a.append([])
            for j in range(0, dimensions):
                a[i].append(num)
        return a
    # The Walker Algorithm "Carving out" the room as it walks
    def carveGrid(self):
        # while we haven't hit the max Tunnels allowed
        while self.maxTunnels > 0:
            # Check that the nextDirection is perpendicular to the lastDirection
            while (self.randomDirection[0] == -self.lastDirection[0] and self.randomDirection[1] == -self.lastDirection[1]) or (self.randomDirection[0] == self.lastDirection[0] and self.randomDirection[1] == self.lastDirection[1]):
                # Get a random direction
                self.randomDirection = self.directions[math.floor(
                    random() * 4)]
            # Move a random distance in a particular direction
            randomLength = math.ceil(random() * self.maxLength)
            tunnelLength = 0
            while tunnelLength < randomLength:
                # Check if about to run into any walls
                if not ((self.currentRow == 0 and self.randomDirection[0] == -1) or (self.currentCol == 0 and self.randomDirection[1] == -1) or (self.currentRow == self.dimensions - 1 and self.randomDirection[0] == 1) or (self.currentCol == self.dimensions - 1 and self.randomDirection[1] == 1)):
                    # DO NOT assign the room here
                    # This row / col combo may be "stepped" on many times and may
                    # create duplicate rooms = BAD
                    # See def saveAndLinkRooms
                    self.grid[self.currentRow][self.currentCol] = 1
                    self.currentRow += self.randomDirection[0]
                    self.currentCol += self.randomDirection[1]
                    tunnelLength += 1
                else:
                    break
            # tunnelLength should be at zero, so decrement the maxTunnels
            # set the last direction to the direcition we just went
            if tunnelLength >= 0:
                self.lastDirection = self.randomDirection
                self.maxTunnels -= 1
    # Helper method to get a coordinates neighbors
    def getNeighbors(self, y, x):
        neighbors = [None, None, None, None]  # Top, Right, Bottom, Left
        # Top Neighbor
        if not y - 1 < 0 and not self.grid[y - 1][x] == 0:
            neighbors[0] = self.grid[y - 1][x]
        # Right Neighbor
        if not x + 1 > self.dimensions - 1 and not self.grid[y][x + 1] == 0:
            neighbors[1] = self.grid[y][x + 1]
        # Bottom Neighbor
        if not y + 1 > self.dimensions - 1 and not self.grid[y + 1][x] == 0:
            neighbors[2] = self.grid[y + 1][x]
        # Left Neighbor
        if not x - 1 < 0 and not self.grid[y][x - 1] == 0:
            neighbors[3] = self.grid[y][x - 1]
        return neighbors
    # Helper method to get the direction
    def getDirection(self, i):
        switcher = {
            0: 'n',
            1: 'e',
            2: 's',
            3: 'w'
        }
        return switcher.get(i)
    def createAndSaveRooms(self):
        names = ["anteroom", "armory", "assembly room", "attic", "backroom", "ballroom", "basement", "bathroom", "bedroom", "boardroom", "boiler room", "boudoir", "breakfast nook", "breakfast room", "cabin, cell", "cellar", "chamber", "changing room", "chapel", "classroom", "clean room", "cloakroom", "cold room", "common room", "conference room", "conservatory", "control room", "courtroom", "cubby", "darkroom", "den", "dining room", "dormitory", "drawing room", "dressing room", "dungeon", "emergency room", "engine room", "entry", "family room", "fitting room", "formal dining room", "foyer", "front room", "game room", "garage", "garret", "great room", "green room", "grotto", "guest room", "gym", "hall", "hallway", 'homeroom', "hospital room", "hotel room", "inglenook", "jail cell", "keep", "kitchen",
                 'kitchenette', "ladies room", "larder", "laundry room", "library", "living room", "lobby", "locker", "room loft", "lounge", "lunchroom", "maids room", "mailroom", "mens room", "morning room", "motel room", "mud room", "newsroom", 'nursery', 'office', "operating room", "panic room", "pantry", "parlor", 'playroom', "pool room", "powder room", "prison cell", "rec room", "recovery room", "restroom", "rumpus room", "salesroom", "salon", 'schoolroom', "screen porch", "scullery", "showroom", "sick room", "sitting room", "solarium", "staff room", "stateroom", "stockroom", "storeroom", "studio", "study", "suite", "sunroom", "tack room", "utility room", "vestibule", "visitors room", "waiting room", "wardroom", "washroom", "water closet", "weight room", "wine cellar", "womens room", "workroom"]
        descriptions = ["So quiet", "So cold", "So hot"]
        for y in range(0, self.dimensions):
            for x in range(0, self.dimensions):
                if not self.grid[y][x] == 0:
                    # Create and Save the room HERE
                    self.grid[y][x] = Room(
                        title=random.choice(names), description=random.choice(descriptions), x_coor=x, y_coor=y)
                    currentRoom = self.grid[y][x]
                    currentRoom.save()
    # Link the Rooms to their associated neighbors
    def linkRooms(self):
        # Create and save Rooms
        self.createAndSaveRooms()
        # Loop through each grid item
        for y in range(0, self.dimensions):
            for x in range(0, self.dimensions):
                if not self.grid[y][x] == 0:
                    neighbors = self.getNeighbors(y, x)
                    for i in range(0, len(neighbors)):
                        if neighbors[i] is not None:
                            # Connect the Rooms here
                            self.grid[y][x].connectRooms(
                                neighbors[i], self.getDirection(i))

Room.objects.all().delete()
g = Grid()
g.carveGrid()
g.createAndSaveRooms()
g.linkRooms()

print(Room.objects.all())