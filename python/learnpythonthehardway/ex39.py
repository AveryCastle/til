stuff = {'name': 'Zed', 'age': 36, 'height': 6*12+2}

print(stuff['name'])

print(stuff['age'])

print(stuff['height'])

stuff['university'] = 'Stanford'

print(stuff)

del stuff['height']

print(stuff)

states = {
    'JIMIN': 173.9,
    'V': 178,
    'JIN':179
}

print(states)

for key, value in states.items():
    print(key, value)

state = states.get('JIN', None)
if not state:
    print("here!! %r " % state)
