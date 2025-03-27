"""
This is a program that shows how to use OOP in a basic format.
It is also the setup for Assignment 8 and includes a pseudo-code 
of the recommended logical flow.
"""

from random import choice, randint      #Import choice from list and random integer methods from random library

class RandomPerson:        # Blueprint for making a random person object
    def __init__(self):            # Required initialization method; This class has no input arguments
        names = ["John", "Steve",       #List of random names to choose from
                 "Linda", "BOB", 
                 "Brunhilda"]
        genders = ["Female",            #List of random genders to choose from
                "Male",
                "Attack Helicopter"]

        self.name = choice(names)       #Choose a random name from names list to be name attribute
        self.age = randint(1, 100)      #Choose a random integer from 1 to 100 to be age attribute
        self.gender = choice(genders)   #Choose a random gender from genders list to be gender attribute

    def __str__(self):                                                 # Default dunder str method returns memory address, but we want other information when object printed
        return (f"{self.name} is {self.gender} and is {self.age} years old")   #Desired returned f string 
    
    def ager(self, years):                                             # Example custom method that ages person object by input nubmer of years
        self.age += years                                                   #Increases persons age attribute by given number of years
        print(f"{self.name} is {years} years older and is now {self.age}")  #Prints change info

# Basic object operations
person = RandomPerson()           #Make a random person
print(person.gender)              #Print persons's gender attribute

print(person.age)                 #Print person's age attribute
person.ager(10)                   #Use defined age method to age person by 10 years and print info

info = (person.name + "," +       #Format a string better suited to microbit scroll method
        person.gender + "," +
        person.age)
print(info)                       #Print concatenated information string

# Create 10 randomized people and print attriubtes using str dunder method
for _ in range(10):             #Repeat 10 times
    person = RandomPerson()     #Make a random person
    print(person)               #Use changed dunder method str through print to print

# Logical layout for assignment #8

"""
person class                        #define RandomPerson class (same as above but without the example age method)
car class                           #define RandomCar class (similar to RandomPerson but with model and speed as attributes)

person = person class()             #Make person object
car = car class()                   #Make car object

While True                          #Loop forever
    if a pressed                    #If microbit button A pressed
        print person info           #Scroll the person attributes

    if b pressed                    #If microbit button B pressed
        print car info              #Scroll the car attributes

    if center pressed               #If microbit touch sensor pressed
        person = person class()     #Recreate person object 
        car = car class()           #Recreate car object
"""