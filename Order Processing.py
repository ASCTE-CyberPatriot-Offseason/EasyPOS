# Functionality to create new orders. 
# Adding menu items to orders. 
# Calculating the total cost of the order. 
# Ability to modify or remove items from an order before finalizing. 
# Order status tracking (e.g., pending, in-progress, completed).

menu = ["Burger", "Fries", "Drink"]
order = []


def orderer():
    order1 = input("What would you like to order? ")
    if order1 == "burger":
        burger()
    if order1 == "fries":
        fries()

def burger():
    order.append("Burger")
    friesYorN = input("Would you like to make it a combo? ")
    if friesYorN == "yes":
        fries()

def fries():
    frySize = input("What size do you want your fries to be? ")
    if frySize == "small":
        order.append("Small Fries")
    if frySize == "medium":
        order.append("Medium Fries")
    if frySize == "large":
        order.append("Large Fries")

def addItem():
    orderAgain = True
    while orderAgain == True:
        orderer()
        print(f"This is your current order: \n{order}")
        orderAgainYN = input("Would you like to order another item? ")
        if orderAgainYN != "yes":
            orderAgain = False

def removeItem():
    removeItem = True
    while removeItem == True:
        print(f"This is your current order: \n{order}")
        removeitemYN = input("Would you like to remove an item? ")
        if removeitemYN == "yes":
            remove = int(input("What is the index of it? ")) # Make better
            order.pop(remove)
        else:
            removeItem = False

print()
print("  MENU")
for i in range(len(menu)):
    print(f"{i + 1}. {menu[i]}")

print()
addItem()
removeItem()

print("GOOODBYE")