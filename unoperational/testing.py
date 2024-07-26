import yaml

# with open('C:\\Users\\agney\\Documents\\FormGen\\games\\bardgame\\bardgame.yaml') as f:
#     content = f.read()

with open('C:\\Users\\agney\\Documents\\FormGen\\games\\bardgame\\bardgame.yaml', 'rb') as file:
    content = file.read()

print(content.find(b'\x9d'))

content = content.replace(b'\x9d', b'')

# Write the corrected content back to the file
with open('C:\\Users\\agney\\Documents\\FormGen\\games\\bardgame\\bardgame.yaml', 'wb') as file:
    file.write(content)