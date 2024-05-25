'''
Create a class to model a character in a video game
- initialize the class with three parameters
    - Health
    - Damage
    - Speed

- define a mathod to double the speed of the character
'''

class Character:
    def __init__(self, health, damage, speed):
        self.health = health
        self.damage = damage
        self.speed = speed
    
    def double_speed(self):
            self.speed *= 2




warrior = Character(100, 50, 10)
ninja = Character(80, 40, 40)

print(f"Warrior speed: {warrior.speed}")
print(f"Ninja speed: {ninja.speed}")

warrior.double_speed()

print(f"Warrior speed: {warrior.speed}")
  