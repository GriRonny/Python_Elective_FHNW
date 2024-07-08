print("Let's work together on this project")

user_input = input("Please enter a command: \n")

while user_input.lower() != "stop":
    match user_input:
        case "Hello":
            print("123")
        case "Start":
            i = 0
            while i < 10:
                if i == 9:
                    print("Hello World #10")
                else:
                    print("Hello World")
                i += 1
        case _:
            print("Default Case")
    user_input = input("Please enter a command: \n")

color_list = ["blue", "grey", "red"]
dictionary = {
    "brand": "BMW",
    "model": "M3",
    "diesel": False,
    "year": 2006,
    "color_options": color_list
}
print("Length of dictionary: " + str(len(dictionary)))

#this is bad code!
#This is good code


