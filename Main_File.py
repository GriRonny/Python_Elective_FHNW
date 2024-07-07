print("Let's work together on this project")

input = input("Please enter a command: \n")
if (input == "Start"):
    i = 0
    while i < 10:
        print("Hello World")
        i += 1
else:
    print("OK")

color_list = ["blue", "grey", "red"]
dictionary = {
    "brand": "BMW",
    "model": "M3",
    "diesel": False,
    "year": 2005,
    "color_options": color_list
}
print(len(dictionary))

