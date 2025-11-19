import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from crm.models import Company, Customer, Interaction

fake = Faker()
User = get_user_model()

INTERACTION_TYPES = [choice[0] for choice in Interaction.InteractionType.choices]


class Command(BaseCommand):
    help = "Generate demo data: 3 users, ~1000 customers, ~500 interactions per customer"

    def add_arguments(self, parser):
        parser.add_argument('--customers', type=int, default=1000)
        parser.add_argument('--interactions', type=int, default=500)

    def handle(self, *args, **options):
        customer_count = options['customers']
        interaction_count = options['interactions']

        self.stdout.write(self.style.NOTICE('Clearing previous demo data...'))
        Interaction.objects.all().delete()
        Customer.objects.all().delete()
        Company.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        with transaction.atomic():
            self.stdout.write(self.style.NOTICE('Creating representatives...'))
            reps = [
                User.objects.create_user(
                    username=f"rep{i}",
                    email=f"rep{i}@example.com",
                    password="password123",
                    is_staff=True
                )
                for i in range(1, 4)
            ]

            self.stdout.write(self.style.NOTICE('Creating companies...'))
            companies = []
            for _ in range(customer_count // 5):
                while True:
                    name = fake.company()
                    if not Company.objects.filter(name=name).exists():
                        companies.append(Company.objects.create(name=name))
                        break

            self.stdout.write(self.style.NOTICE('Creating customers...'))
            customers = []
            for _ in range(customer_count):
                customers.append(Customer(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    birthday=fake.date_of_birth(minimum_age=21, maximum_age=70),
                    company=random.choice(companies),
                    representative=random.choice(reps)
                ))
            Customer.objects.bulk_create(customers, batch_size=1000)

            customer_objs = list(Customer.objects.all())

            self.stdout.write(self.style.NOTICE('Creating interactions... this may take a while.'))
            batch_size = 5000
            interaction_bulk = []
            now = timezone.now()
            for customer in customer_objs:
                for _ in range(interaction_count):
                    occurred_at = now - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
                    interaction_bulk.append(Interaction(
                        customer=customer,
                        interaction_type=random.choice(INTERACTION_TYPES),
                        date=occurred_at
                    ))
                    if len(interaction_bulk) >= batch_size:
                        Interaction.objects.bulk_create(interaction_bulk, batch_size=batch_size)
                        interaction_bulk = []

            if interaction_bulk:
                Interaction.objects.bulk_create(interaction_bulk, batch_size=batch_size)

        self.stdout.write(self.style.SUCCESS('Demo data generation complete.'))
