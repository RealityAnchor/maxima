import json
import random

def generate_portal_name():
    with open('portal_affixes.json') as f:
        portals = json.load(f)
    
    prefix = random.choice(portals['prefix'])
    noun = random.choice(portals['noun'])
    name = f"{prefix} {noun}"

    return name

while True:
    for i in range(25):
        print(generate_portal_name())
    input()