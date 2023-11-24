from os import system
from os.path import join

modules = []

with open("requirements.txt","r") as file:
    modules = file.read().split("\n")
    file.close()

for module in modules:
    print("Installing ",module)
    system(f"pip install {module}")

print("Setup completed")