import random

from django.core.management.base import BaseCommand

from core.models import (
    Category,
    DigitalOrderItem,
    DigitalProduct,
    Order,
    PhysicalOrderItem,
    PhysicalProduct,
    User,
    Vendor,
)


class Command(BaseCommand):
    help = 'Populates the database with random orders'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            nargs='?',
            default=10,
            help='Indicates the number of orders to create',
        )

    def handle(self, *args, **options):
        count = options['count']

        # Ensure at least one user exists
        if not User.objects.exists():
            self.stdout.write('No users found. Creating a test user...')
            User.objects.create_user(
                username='testuser', email='test@example.com', password='password123'
            )
            self.stdout.write('Created user: testuser')

        self.stdout.write(self.style.SUCCESS(f'Creating {count} random orders...'))

        # Check for products
        physical_products = list(PhysicalProduct.objects.all())
        digital_products = list(DigitalProduct.objects.all())

        if not physical_products and not digital_products:
            self.stdout.write('No products found. Populating products internally...')
            self.populate_products(20)
            # Reload products
            physical_products = list(PhysicalProduct.objects.all())
            digital_products = list(DigitalProduct.objects.all())

        for _ in range(count):
            # Pick a random user for each order
            user = User.objects.order_by('?').first()
            status = random.choice(Order.StatusChoices.values)

            order = Order.objects.create(user=user, status=status)

            has_items = False

            # Add random physical products
            if physical_products:
                # Randomly decide to add physical products (70% chance)
                if random.random() < 0.7:
                    num_physical = random.randint(1, 3)
                    for _ in range(num_physical):
                        product = random.choice(physical_products)
                        quantity = random.randint(1, 5)
                        PhysicalOrderItem.objects.create(
                            order=order, physical_product=product, quantity=quantity
                        )
                        has_items = True

            # Add random digital products
            if digital_products:
                # Randomly decide to add digital products (70% chance)
                if random.random() < 0.7:
                    num_digital = random.randint(1, 3)
                    for _ in range(num_digital):
                        product = random.choice(digital_products)
                        # Digital products often just 1, but let's allow up to 2
                        quantity = random.randint(1, 2)
                        DigitalOrderItem.objects.create(
                            order=order, digital_product=product, quantity=quantity
                        )
                        has_items = True

            # Ensure order has at least one item if both randoms skipped or lists empty
            if not has_items:
                if physical_products:
                    product = random.choice(physical_products)
                    PhysicalOrderItem.objects.create(
                        order=order, physical_product=product, quantity=1
                    )
                elif digital_products:
                    product = random.choice(digital_products)
                    DigitalOrderItem.objects.create(
                        order=order, digital_product=product, quantity=1
                    )
                else:
                    # This should theoretically not happen due to check above, but purely defensive
                    self.stdout.write(
                        self.style.WARNING(
                            f"Order {order.order_id} has no products available to add."
                        )
                    )

            self.stdout.write(
                f'Created Order: {order.order_id} for {user.username} ({order.status})'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} orders'))

    def populate_products(self, count):
        """
        Internal helper to populate products if they don't exist.
        Handles the creation of Categories, Vendors (Users), and Products.
        """
        # Create Categories
        categories_data = ['Electronics', 'Books', 'Software', 'Home', 'Clothing']
        categories = []
        for cat_name in categories_data:
            category, _ = Category.objects.get_or_create(name=cat_name)
            categories.append(category)

        # Create Vendors (Users with Vendor profile)
        vendor_users = []
        for i in range(1, 6):
            username = f'vendor_{i}'
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('password123')
                user.save()
                # Create Vendor profile
                Vendor.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': f'Vendor {i} Inc',
                        'description': 'A great vendor',
                    },
                )
            vendor_users.append(user)

        adjectives = ['Super', 'Mega', 'Smart', 'Fast', 'Pro']
        nouns_physical = ['Widget', 'Gadget', 'Tool', 'Device']
        nouns_digital = ['App', 'Plugin', 'Ebook', 'Course']

        for _ in range(count):
            is_physical = random.choice([True, False])
            vendor_user = random.choice(vendor_users)
            category = random.choice(categories)
            price = round(random.uniform(5.00, 500.00), 2)
            stock = random.randint(10, 100)

            if is_physical:
                name = f"{random.choice(adjectives)} {random.choice(nouns_physical)} {random.randint(1000, 9999)}"
                PhysicalProduct.objects.create(
                    name=name,
                    description=f"Description for {name}",
                    vendor=vendor_user,  # vendor field on ProductSpec is ForeignKey(User)
                    category=category,
                    price=price,
                    stock=stock,
                    weight=random.uniform(0.5, 5.0),
                    dimensions="10x10x10",
                )
            else:
                name = f"{random.choice(adjectives)} {random.choice(nouns_digital)} {random.randint(1000, 9999)}"
                DigitalProduct.objects.create(
                    name=name,
                    description=f"Description for {name}",
                    vendor=vendor_user,  # vendor field on ProductSpec is ForeignKey(User)
                    category=category,
                    price=price,
                    stock=stock,
                    os='Web',
                    requirements='Browser',
                )

        self.stdout.write(
            f'Internal product population complete: Created {count} products.'
        )
