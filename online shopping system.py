import uuid

# Product class
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def display_info(self):
        print(f"Product ID: {self.product_id}, Name: {self.name}, Price: ${self.price}, Stock: {self.stock}")

    def update_stock(self, amount):
        self.stock += amount

# ShoppingCart class
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        if product.stock >= quantity:
            # Check if the product is already in the cart
            for item in self.items:
                if item[0] == product:
                    item[1] += quantity
                    product.update_stock(-quantity)
                    return
            # Add a new product if it's not already in the cart
            self.items.append([product, quantity])
            product.update_stock(-quantity)
            print(f"Added {quantity} of {product.name} to cart")
        else:
            print(f"Not enough stock for {product.name}")

    def remove_item(self, product, quantity):
        for i, item in enumerate(self.items):
            if item[0] == product:
                if item[1] >= quantity:
                    item[1] -= quantity
                    product.update_stock(quantity)
                    if item[1] == 0:
                        self.items.pop(i)
                    print(f"Removed {quantity} of {product.name} from cart")
                    return
                else:
                    print(f"Cannot remove {quantity} of {product.name}. Only {item[1]} in cart.")
                    return
        print(f"{product.name} not found in cart")

    def view_items(self):
        if not self.items:
            print("Your cart is empty")
        else:
            print("Items in your cart:")
            for product, quantity in self.items:
                print(f"{product.name} - {quantity} pcs")

    def checkout(self):
        total = sum(product.price * quantity for product, quantity in self.items)
        self.items.clear()
        print(f"Checked out. Total amount: ${total:.2f}")
        return total

# Customer class
class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.cart = ShoppingCart()

    def add_to_cart(self, product, quantity):
        self.cart.add_item(product, quantity)

    def remove_from_cart(self, product, quantity):
        self.cart.remove_item(product, quantity)

    def view_cart(self):
        self.cart.view_items()

    def checkout(self):
        total_amount = self.cart.checkout()
        order_id = uuid.uuid4()
        order = Order(order_id, self, self.cart.items, total_amount)
        order.display_order()

# Order class
class Order:
    def __init__(self, order_id, customer, products, total_amount):
        self.order_id = order_id
        self.customer = customer
        self.products = products
        self.total_amount = total_amount

    def display_order(self):
        print(f"Order ID: {self.order_id}")
        print(f"Customer: {self.customer.name}")
        print("Products:")
        for product, quantity in self.products:
            print(f"{product.name} - {quantity} pcs")
        print(f"Total Amount: ${self.total_amount:.2f}")

# Example usage
if __name__ == "__main__":
    # Create products
    product1 = Product("P001", "Laptop", 1000, 10)
    product2 = Product("P002", "Smartphone", 500, 20)

    # Display product info
    product1.display_info()
    product2.display_info()

    # Create a customer
    customer = Customer("C001", "John Doe", "john@example.com")

    # Customer adds products to the cart
    customer.add_to_cart(product1, 2)
    customer.add_to_cart(product2, 5)

    # View cart
    customer.view_cart()

    # Customer removes a product from the cart
    customer.remove_from_cart(product2, 2)

    # View cart again
    customer.view_cart()

    # Customer checks out
    customer.checkout()
