class Coffee:
    def __init__(self, name, description, base_price):
        self.name = name
        self.description = description
        self.base_price = base_price

    def __str__(self):
        return f"{self.name} - {self.description} - ${self.base_price:.2f}"


class Order:
    SIZE_PRICES = {
        "Small": 0.00,
        "Medium": 0.50,
        "Large": 1.00
    }

    def __init__(self, coffee, size):
        self.coffee = coffee
        self.size = size
        self.price = self.calculate_price()

    def calculate_price(self):
        return self.coffee.base_price + self.SIZE_PRICES[self.size]

    def __str__(self):
        return f"{self.size} {self.coffee.name} - ${self.price:.2f}"


class Cafe:
    def __init__(self, name, tax_rate=0.08):
        self.name = name
        self.menu = []
        self.orders = []
        self.tax_rate = tax_rate

    def add_to_menu(self, coffee):
        self.menu.append(coffee)

    def display_menu(self):
        print(f"\n=== {self.name.upper()} MENU ===")
        for i, coffee in enumerate(self.menu, start=1):
            print(f"{i}. {coffee}")

    def display_sizes(self):
        print("\nSizes available:")
        print("1. Small  (+$0.00)")
        print("2. Medium (+$0.50)")
        print("3. Large  (+$1.00)")

    def add_order(self, coffee, size):
        order = Order(coffee, size)
        self.orders.append(order)
        print(f"\n✅ Added: {order}")

    def calculate_subtotal(self):
        return sum(order.price for order in self.orders)

    def print_bill(self, tip_percent):
        subtotal = self.calculate_subtotal()
        tax = subtotal * self.tax_rate
        tip = subtotal * (tip_percent / 100)
        total = subtotal + tax + tip

        print("\n" + "="*42)
        print(f"{self.name.upper()} — YOUR BILL".center(42))
        print("="*42)

        for order in self.orders:
            print(f"{str(order):<30} ${order.price:>6.2f}")

        print("-"*42)
        print(f"{'Subtotal:':<30} ${subtotal:>6.2f}")
        print(f"{(f'Tax '+f'({self.tax_rate*100}%)'):<30} ${tax:>6.2f}")
        print(f"{f'Tip ({tip_percent}%):':<30} ${tip:>6.2f}")
        print("="*42)
        print(f"{'TOTAL:':<30} ${total:>6.2f}")
        print("="*42)


# ------------------------
# SETUP
# ------------------------
cafe = Cafe("Sunny Bean Café", tax_rate=0.08)

cafe.add_to_menu(Coffee("Espresso", "Strong and bold shot of coffee", 2.50))
cafe.add_to_menu(Coffee("Americano", "Espresso diluted with hot water", 3.00))
cafe.add_to_menu(Coffee("Cappuccino", "Equal parts espresso, foam, and milk", 3.75))
cafe.add_to_menu(Coffee("Latte", "Creamy espresso with lots of steamed milk", 3.50))
cafe.add_to_menu(Coffee("Flat White", "Velvety milk with a double espresso shot", 4.00))
cafe.add_to_menu(Coffee("Macchiato", "Espresso with a touch of foam", 3.25))
cafe.add_to_menu(Coffee("Mocha", "Espresso with chocolate and milk", 4.25))
cafe.add_to_menu(Coffee("Cold Brew", "Slow-steeped coffee served cold", 4.00))


SIZES = ["Small", "Medium", "Large"]

print(f"\nWelcome to {cafe.name}! ☕")

# ------------------------
# MAIN LOOP
# ------------------------
while True:
    print("\n" + "="*40)
    print("1. Order drink")
    print("2. View order")
    print("3. Checkout")
    print("="*40)

    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        cafe.display_menu()

        drink = input("Select drink number (0 to cancel): ").strip()
        if drink == "0":
            continue

        if not drink.isdigit():
            print("❌ Invalid input")
            continue

        idx = int(drink) - 1
        if idx < 0 or idx >= len(cafe.menu):
            print("❌ Invalid choice")
            continue

        selected = cafe.menu[idx]

        cafe.display_sizes()
        size_input = input("Choose size: ").strip()

        if not size_input.isdigit():
            print("❌ Invalid input")
            continue

        size_idx = int(size_input) - 1
        if size_idx < 0 or size_idx >= len(SIZES):
            print("❌ Invalid size")
            continue

        cafe.add_order(selected, SIZES[size_idx])

    elif choice == "2":
        if not cafe.orders:
            print("🛒 No items yet")
        else:
            for i, order in enumerate(cafe.orders, 1):
                print(f"{i}. {order}")
            print(f"Subtotal: ${cafe.calculate_subtotal():.2f}")

    elif choice == "3":
        if not cafe.orders:
            print("❌ Order something first")
            continue

        tip_choice = input("Tip (10/15/20/0): ").strip()
        tip = int(tip_choice) if tip_choice.isdigit() else 0

        cafe.print_bill(tip)
        break

    else:
        print("❌ Invalid option")