from dataclasses import dataclass
# Town is an object used to create Towns in the backend
# A town consists of multiple params including
# @PARAMS: Name, Population, Size, Age: optional, 
# Type (university town, castle town, capital city, cathedral city ect.), Culure (types of culture), 
# Economic status, Status and Diplomacy (can include all forms of diplomacy)
# Values are passed down from the region and passed up from smaller entites 

@dataclass
class Location():
    print()
    name: str
    population: int
    size: str
    age: str
    type: str
    