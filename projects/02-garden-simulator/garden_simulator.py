"""Interactive text-based garden simulator."""

import random


class Plant:
    def __init__(self, name, harvest_yield):
        # Store the plant's name
        self.name = name

        # Store how much the plant gives when harvested
        self.harvest_yield = harvest_yield

        # List of all plant growth stages
        self.growth_stages = ["seed", "sprout", "plant", "flower", "harvest-ready"]

        # Plant always starts as a seed
        self.current_growth_stage = self.growth_stages[0]

        # Tracks whether the plant can be harvested
        self.harvestable = False

    def grow(self):
        # Find the current stage index
        current_index = self.growth_stages.index(self.current_growth_stage)

        # Prevent growing past the final stage
        if self.current_growth_stage != self.growth_stages[-1]:
            # Move plant to the next growth stage
            self.current_growth_stage = self.growth_stages[current_index + 1]

            # Check if plant became harvest-ready
            if self.current_growth_stage == "harvest-ready":
                self.harvestable = True
                print("Your plant is ready to harvest!")
        else:
            print("This plant is already fully grown!")

    def harvest(self):
        # Harvest plant only if it is ready
        if self.harvestable:
            # Reset harvestable status
            self.harvestable = False
            print(f"You harvested {self.name}!")
            return True

        # Prevent harvesting before the plant is ready
        print("Your plant is not yet harvestable. Continue to grow it!")
        return False


class Pepper(Plant):
    def __init__(self):
        super().__init__("Pepper", 6)


class Tomato(Plant):
    def __init__(self):
        super().__init__("Tomato", 5)

        # Tomato has a "fruiting" growth stage
        self.growth_stages = ["seed", "sprout", "plant", "flower", "fruit", "harvest-ready"]


class Carrot(Plant):
    def __init__(self):
        super().__init__("Carrot", 3)

        # Carrots develop roots instead of flowers
        self.growth_stages = ["seed", "sprout", "plant", "root-bulking", "harvest-ready"]


class Lettuce(Plant):
    def __init__(self):
        super().__init__("Lettuce", 4)

        # Lettuce forms a leafy head before harvest
        self.growth_stages = ["seed", "sprout", "plant", "head-forming", "harvest-ready"]


plant_list = ["Pepper", "Tomato", "Carrot", "Lettuce"]


def select_item(items):
    if type(items) == dict:
        # Convert dictionary keys to a list so they can be indexed
        keys = list(items.keys())
        for i in range(len(keys)):
            print(f"{i + 1}. {keys[i]}")
    elif type(items) == list:
        for i in range(len(items)):
            # If item has a name attribute, display that instead of the object
            label = items[i].name if hasattr(items[i], "name") else items[i]
            print(f"{i + 1}. {label}")
    else:
        # Handle invalid input types
        print("Error: items must be a dictionary or a list.")
        return None


class Gardener:
    """Represents a gardener who can plant, tend, and harvest plants."""

    plant_dict = {
        "Pepper": Pepper,
        "Tomato": Tomato,
        "Carrot": Carrot,
        "Lettuce": Lettuce
    }

    def __init__(self, name):
        self.name = name
        self.planted_plants = []

        # Stores seeds and harvested crops
        self.inventory = {}

    def plant(self):
        select_item(self.inventory)
        choice = input("Which plant do you want to plant? (enter name): ").strip().capitalize()

        # Make sure the chosen plant actually exists in inventory and has stock
        if choice in self.inventory and self.inventory[choice] > 0:
            # Reduce the seed count since we're using one up
            self.inventory[choice] -= 1

            # Clean up the inventory if we hit zero seeds left
            if self.inventory[choice] == 0:
                del self.inventory[choice]

            # Use plant_dict to dynamically instantiate the right subclass
            new_plant = self.plant_dict[choice]()
            self.planted_plants.append(new_plant)
            print(f"You planted a {choice}!")
        else:
            print("You don't have that plant in your inventory.")

    def tend(self):
        # Go through every plant currently growing in the garden
        for plant in self.planted_plants:
            # Skip growing it further if it's already ready to harvest
            if plant.current_growth_stage == "harvest-ready":
                print(f"Your {plant.name} is already harvest-ready!")
            else:
                plant.grow()
                print(f"You tended your {plant.name}. It is now at the '{plant.current_growth_stage}' stage.")

    def harvest(self):
        select_item(self.planted_plants)
        try:
            index = int(input("Which plant do you want to harvest? (enter number): ")) - 1
        except ValueError:
            # Catch non-numeric input to prevent crash
            print("Please enter a valid number.")
            return

        # Make sure the index is valid before doing anything
        if 0 <= index < len(self.planted_plants):
            plant = self.planted_plants[index]

            # Only harvest if the plant is actually ready
            if plant.harvestable:
                plant.harvest()

                # Add the harvested yield to inventory
                self.inventory[plant.name] = self.inventory.get(plant.name, 0) + plant.harvest_yield

                # Remove the plant from the garden since it's been harvested
                self.planted_plants.remove(plant)
                print(f"You got {plant.harvest_yield} units!")
            else:
                print("That plant isn't ready to harvest yet.")
        else:
            print("Invalid selection")

    def forage_for_seeds(self):
        # Randomly pick a seed from the available plant types
        found_seed = random.choice(plant_list)

        # Add to inventory, defaulting to 0 if not yet present
        self.inventory[found_seed] = self.inventory.get(found_seed, 0) + 1
        print(f"You found a {found_seed} seed!")


def run_game():
    """Start the interactive garden simulator."""
    # Game Setup
    player_name = input("Enter your name: ")
    while not player_name.strip():
        print("Name can't be empty.")
        player_name = input("Enter your name: ")

    gardener = Gardener(player_name)

    # Valid Actions
    actions = ["forage", "plant", "tend", "harvest", "inventory", "help", "quit"]

    print(f"\nWelcome to the Garden Simulator, {player_name}!")
    print("Type 'help' to see available actions.\n")

    # Main Game Loop
    while True:
        action = input("What would you like to do? ").strip().lower()

        if action == "forage":
            gardener.forage_for_seeds()
        elif action == "plant":
            if not gardener.inventory:
                print("Your inventory is empty. Try foraging first!")
            else:
                gardener.plant()
        elif action == "tend":
            if not gardener.planted_plants:
                print("You have no plants in the ground yet.")
            else:
                gardener.tend()
        elif action == "harvest":
            if not gardener.planted_plants:
                print("You have no plants to harvest.")
            else:
                gardener.harvest()
        elif action == "inventory":
            if not gardener.inventory:
                print("Your inventory is empty.")
            else:
                print("\nYour inventory:")
                select_item(gardener.inventory)
        elif action == "help":
            print("\nAvailable actions:")
            select_item(actions)
        elif action in ("quit", "exit"):
            print(f"Thanks for playing, {player_name}. Goodbye!")
            break
        else:
            print("Invalid action. Type 'help' to see available actions.")


if __name__ == "__main__":
    run_game()
