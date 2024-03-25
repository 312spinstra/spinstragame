import random

# Class that implements the Room Loader
class RoomLoader:
    #------------------------------#
    @staticmethod # Python - why can't you just use the "static" designator in front of the function name???
    # Function that generates room types for a given level map
    def generateRoomTypes(coordinates, exitCoordinates):
        typedRooms = []
        for roomCoordinates in coordinates:
            type = None
            isBossRoom = (roomCoordinates == exitCoordinates)

            if isBossRoom:
                type = "Boss"
            else:
                room_types = ["Battle", "Treasure", "Mystery"]
                type = random.choice(room_types)
                
            typedRooms.append({"coordinates": roomCoordinates, "type": type, "completed": False})

        # Put the boss key room somewhere on the map
        randomRoom = random.choice(typedRooms)
        while (randomRoom["coordinates"] == exitCoordinates):
            randomRoom = random.choice(typedRooms)

        for typedRoom in typedRooms:
            if typedRoom == randomRoom:
                typedRoom["type"] = "Key"

        return typedRooms
    #------------------------------#