# Functionality to create new orders. 
# Adding menu items to orders. 
# Calculating the total cost of the order. 
# Ability to modify or remove items from an order before finalizing. 
# Order status tracking (e.g., pending, in-progress, completed).

menu = ["Burger", "Taco", "Fries", "Drink", "Cookie"]
order = []


def addItem():
    orderAgain = True
    while orderAgain == True:
        orderNum = int(input("What would you like to order? (enter number) "))
        order.append(menu[orderNum - 1])
        print(f"This is your current order: \n{order}")
        orderAgainYN = input("Would you like to order another item? ")
        if orderAgainYN != "yes":
            orderAgain = False


def removeItem():
    removeItem = True
    while removeItem == True:
        print(f"This is your current order: \n{order}")
        remove = input("Which item do you want to remove? ")
        count = 0
        for item in order:
            if item == remove:
                order.pop(count)
                break
            count += 1
        print(f"This is your current order: \n{order}")
        removeAgain = input("Would you like to remove something else? ")
        if removeAgain != "yes":
            removeItem = False


print()
print("  MENU")
for i in range(len(menu)):
    print(f"{i + 1}. {menu[i]}")

print()
addItem()
while True:
    anythingElse = input("Can I help you with anything else? ")
    if anythingElse == "yes":
        addOrRemove = input("Do you want to add or remove an item? ")
        if addOrRemove == "add":
            addItem()
        if addOrRemove == "remove":
            removeItem()
    else:
        break
print("GOOODBYE")
