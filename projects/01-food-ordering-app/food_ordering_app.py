"""Interactive command-line food ordering application."""

# Global constant storing the name of the food ordering app
FOOD_APP_NAME = "Jet Delivers"


# Dictionary storing menu items
# Each SKU maps to another dictionary containing:
# - item name
# - item price
menu_items = {
    "sku1": {"Name": "Hamburger", "Price": 6.51},
    "sku2": {"Name": "Cheeseburger", "Price": 7.75},
    "sku3": {"Name": "Milkshake", "Price": 5.99},
    "sku4": {"Name": "Fries", "Price": 2.39},
    "sku5": {"Name": "Sub", "Price": 5.87},
    "sku6": {"Name": "Ice Cream", "Price": 1.55},
    "sku7": {"Name": "Fountain Drink", "Price": 3.45},
    "sku8": {"Name": "Cookie", "Price": 3.15},
    "sku9": {"Name": "Brownie", "Price": 2.46},
    "sku10": {"Name": "Sauce", "Price": 0.75}
}


# Dictionary storing application actions
# The key is the menu option number the user enters
# The value is the action description
app_actions = {
    "1": "Add a new menu item to cart",
    "2": "Remove an item from the cart",
    "3": "Modify a cart item's quantity",
    "4": "View cart",
    "5": "Checkout",
    "6": "Exit"
}


# Global constant storing the sales tax rate
# 0.07 means 7% sales tax
SALES_TAX = 0.07


# Dictionary representing the user's shopping cart
# Key   -> SKU
# Value -> Quantity
# Starts empty because the user has not ordered anything yet
cart = {}


def display_menu():
    print("\nHere is the menu:\n")

    # Loop through all SKUs in the menu dictionary
    for sku in menu_items:
        # Remove "sku" and keep only the number
        sku_number = sku[3:]

        # Get item name
        item_name = menu_items[sku]["Name"]

        # Get item price
        item_price = menu_items[sku]["Price"]

        # Print formatted menu item
        print(f"({sku_number}) {item_name}: ${item_price:.2f}")


def add_to_cart(sku, quantity):
    # Check if the SKU exists in the menu
    if sku not in menu_items:
        # Display error if SKU is invalid
        print("\nError: Invalid SKU.\n")
    else:
        # If SKU already exists in cart, increase its quantity
        if sku in cart:
            cart[sku] += quantity
        # If SKU is not yet in cart, add it with the entered quantity
        else:
            cart[sku] = quantity

        # Print confirmation message
        print(f"\nAdded {quantity} of {menu_items[sku]['Name']} to the cart.\n")


def remove_from_cart(sku):
    # Check if SKU exists in cart
    if sku not in cart:
        print("\nError: Item is not in the cart.\n")
    else:
        # Remove item from cart
        cart.pop(sku)

        # Print confirmation message
        print(f"\nRemoved {menu_items[sku]['Name']} from the cart.\n")


def modify_cart(sku, quantity):
    # Check if SKU exists in cart
    if sku in cart:
        # If quantity is greater than 0, update cart quantity
        if quantity > 0:
            cart[sku] = quantity
            print(f"\nModified {menu_items[sku]['Name']} quantity to {quantity} in the cart.\n")
        # If quantity is 0 or less, remove item from cart
        else:
            remove_from_cart(sku)
    # SKU does not exist in cart
    else:
        print("\nError: Item is not in the cart.\n")


def view_cart():
    print("\n**** CART CONTENTS ****\n")

    # Store subtotal
    subtotal = 0

    # Loop through cart items
    for sku in cart:
        # Verify SKU exists in menu
        if sku in menu_items:
            # Get quantity
            quantity = cart[sku]

            # Get item name
            item_name = menu_items[sku]["Name"]

            # Get item price
            item_price = menu_items[sku]["Price"]

            # Add item total to subtotal
            subtotal += item_price * quantity

            # Print cart item
            print(f"{quantity} x {item_name}")

    # Calculate tax
    tax = subtotal * SALES_TAX

    # Calculate final total
    total = subtotal + tax

    # Print total rounded to 2 decimal places
    print(f"\nTotal: ${total:.2f}\n")


def checkout():
    # Print checkout header
    print("\n**** CHECKOUT ****\n")

    # Display cart contents and total
    view_cart()

    # Print confirmation message
    print("Your order has been submitted.\n")


def get_sku_and_quantity(sku_prompt, quantity_prompt=None):
    # Prompt user for SKU number
    sku_input = input(sku_prompt)

    # Add "sku" prefix to user input
    sku = "sku" + sku_input

    # Check if quantity prompt was supplied
    if quantity_prompt is not None:
        # Prompt user for quantity
        quantity_input = input(quantity_prompt)

        # Check if quantity input is a valid digit
        if quantity_input.isdigit():
            # Convert quantity from string to integer
            quantity = int(quantity_input)
        # Default quantity to 1 if invalid
        else:
            quantity = 1

        # Return both SKU and quantity
        return sku, quantity

    # Return only SKU if quantity prompt was not supplied
    return sku


def run_app():
    # Print welcome message using the app name
    print(f"\nWelcome to {FOOD_APP_NAME}!\n")

    # Boolean variable that controls whether the app keeps running
    app_running = True

    # Keep looping while app_running is True
    while app_running:
        # Display ordering actions
        print("\n**** ORDERING ACTIONS ****\n")

        for action_number in app_actions:
            print(f"({action_number}) {app_actions[action_number]}")

        # Ask user what action they want to take
        user_action = input("\nPlease enter the number of the action you want to take: ")

        # Add item to cart
        if user_action == "1":
            display_menu()
            sku, quantity = get_sku_and_quantity(
                "\nPlease enter the SKU number for the menu item you want to order: ",
                "Please enter the quantity: "
            )
            add_to_cart(sku, quantity)

        # Remove item from cart
        elif user_action == "2":
            display_menu()
            sku = get_sku_and_quantity(
                "\nPlease enter the SKU number for the menu item you want to remove: "
            )
            remove_from_cart(sku)

        # Modify item quantity
        elif user_action == "3":
            display_menu()
            sku, quantity = get_sku_and_quantity(
                "\nPlease enter the SKU number for the menu item you want to modify: ",
                "Please enter the new quantity: "
            )
            modify_cart(sku, quantity)

        # View cart
        elif user_action == "4":
            view_cart()

        # Checkout and stop the app
        elif user_action == "5":
            checkout()
            app_running = False

        # Exit without checkout
        elif user_action == "6":
            print("\nExiting the app. Goodbye!\n")
            app_running = False

        # Invalid action
        else:
            print("\nError: Invalid action. Please choose a number from 1 to 6.\n")


if __name__ == "__main__":
    run_app()
