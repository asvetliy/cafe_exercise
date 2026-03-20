import os


class MenuItem:
    SIZES = {}

    def __init__(self, name, description, base_price):
        self.name = name
        self.description = description
        self.base_price = base_price

    def __str__(self):
        return f'{self.name} - {self.description} - {self.base_price:.2f}'

    def display_sizes(self):
        pass


class Pizza(MenuItem):
    def __init__(self, name, description, base_price):
        super().__init__(name, description, base_price)
        self.SIZES = {
            'Small': 1.0,
            'Medium': 1.3,
            'Large': 1.6,
        }

    def display_sizes(self):
        print('\nSizes available:')
        index = 1
        for size, mult in self.SIZES.items():
            print(f'{index}. {size} (+${mult})')
            index += 1


class Coffee(MenuItem):
    def __init__(self, name, description, base_price):
        super().__init__(name, description, base_price)
        self.SIZES = {
            'Small': 0.00,
            'Medium': 0.50,
            'Large': 1.00
        }

    def display_sizes(self):
        print('\nSizes available:')
        index = 1
        for size, mult in self.SIZES.items():
            print(f'{index}. {size} (+${mult})')
            index += 1


class Order:
    def __init__(self, item, size):
        self.item = item
        self.size = size
        self.price = self.calculate_price()

    def calculate_price(self):
        if isinstance(self.item, Coffee) or isinstance(self.item, Pizza):
            return self.item.base_price * self.item.SIZES[self.size]

        return self.item.base_price

    def __str__(self):
        return f'{self.size} {self.item.name} - ${self.price:.2f}'


class Cafe:
    def __init__(self, name, tax_rate=0.08):
        self.name = name
        self.menu = []
        self.orders = []
        self.tax_rate = tax_rate

    def add_to_menu(self, item):
        self.menu.append(item)

    def display_menu(self):
        print(f'\n=== {self.name.upper()} MENU ===')
        for i, item in enumerate(self.menu, start=1):
            item_type = item.__class__.__name__
            print(f"{i}. [{item_type}] {item}")

    def add_order(self, item, size):
        order = Order(item, size)
        self.orders.append(order)
        print(f"\n✅ Added: {order}")

    def calculate_subtotal(self):
        return sum(order.price for order in self.orders)

    def print_bill(self, tip_percent):
        subtotal = self.calculate_subtotal()
        tax = subtotal * self.tax_rate
        tip = subtotal * (tip_percent / 100)
        total = subtotal + tax + tip

        print("\n" + "=" * 42)
        print(f"{self.name.upper()} — YOUR BILL".center(42))
        print("=" * 42)

        for order in self.orders:
            print(f"{str(order):<30} ${order.price:>6.2f}")

        print("-" * 42)
        print(f"{'Subtotal:':<30} ${subtotal:>6.2f}")
        print(f"{(f'Tax ' + f'({(self.tax_rate * 100):g}%)'):<30} ${tax:>6.2f}")
        print(f"{f'Tip ({tip_percent:g}%):':<30} ${tip:>6.2f}")
        print("=" * 42)
        print(f"{'TOTAL:':<30} ${total:>6.2f}")
        print("=" * 42)


# ------------------------
# SETUP
# ------------------------
cafe = Cafe("Sunny Bean Café", tax_rate=0.08)

# Add coffe
cafe.add_to_menu(Coffee("Espresso", "Strong and bold shot of coffee", 2.50))
cafe.add_to_menu(Coffee("Americano", "Espresso diluted with hot water", 3.00))
cafe.add_to_menu(Coffee("Cappuccino", "Equal parts espresso, foam, and milk", 3.75))
cafe.add_to_menu(Coffee("Latte", "Creamy espresso with lots of steamed milk", 3.50))
cafe.add_to_menu(Coffee("Flat White", "Velvety milk with a double espresso shot", 4.00))
cafe.add_to_menu(Coffee("Macchiato", "Espresso with a touch of foam", 3.25))
cafe.add_to_menu(Coffee("Mocha", "Espresso with chocolate and milk", 4.25))
cafe.add_to_menu(Coffee("Cold Brew", "Slow-steeped coffee served cold", 4.00))
# Add pizza
cafe.add_to_menu(Pizza('Margherita', 'Tomato, mozzarella, basil', 8.00))
cafe.add_to_menu(Pizza('Pepperoni', 'Pepperoni and cheeze', 10.00))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input('\nPress Enter to continue...')

print(f'\nWelcome to {cafe.name}! ☕')

# ------------------------
# MAIN LOOP
# ------------------------
while True:
    clear_screen()
    print("\n" + "=" * 40)
    print("1. Make order")
    print("2. View order")
    print("3. Checkout")
    print("=" * 40)

    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        clear_screen()
        cafe.display_menu()

        drink = input("Select item number (0 to cancel): ").strip()
        if drink == "0":
            continue

        if not drink.isdigit():
            clear_screen()
            print("❌ Invalid input")
            pause()
            continue

        idx = int(drink) - 1
        if idx < 0 or idx >= len(cafe.menu):
            clear_screen()
            print("❌ Invalid choice")
            pause()
            continue

        selected = cafe.menu[idx]

        selected.display_sizes()
        size_input = input("Choose size: ").strip()

        if not size_input.isdigit():
            clear_screen()
            print("❌ Invalid input")
            pause()
            continue

        size_idx = int(size_input) - 1
        if size_idx < 0 or size_idx >= len(selected.SIZES):
            clear_screen()
            print("❌ Invalid size")
            pause()
            continue

        cafe.add_order(selected, list(selected.SIZES.keys())[size_idx])
        pause()

    elif choice == "2":
        clear_screen()
        if not cafe.orders:
            print("🛒 No items yet")
        else:
            for i, order in enumerate(cafe.orders, 1):
                item_type = order.item.__class__.__name__
                print(f"{i}. [{item_type}] {order}")
            print(f"Subtotal: ${cafe.calculate_subtotal():.2f}")
        pause()

    elif choice == "3":
        if not cafe.orders:
            clear_screen()
            print("❌ Order something first")
            pause()
            continue

        tip_choice = input("Tip (10/15/20/0): ").strip()
        tip = int(tip_choice) if tip_choice.isdigit() else 0

        cafe.print_bill(tip)
        pause()
        break

    else:
        clear_screen()
        print("❌ Invalid option")
        pause()
