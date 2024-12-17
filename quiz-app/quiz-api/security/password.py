import hashlib



hashed = hashlib.md5('JOESIEE2024'.encode('UTF-8')).digest()
print(hashed)