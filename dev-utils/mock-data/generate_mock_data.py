#!/usr/bin/env python3
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from uuid import UUID
import json
import os
import random
import faker
from abc import ABC, abstractmethod

fake = faker.Faker()

@dataclass
class BaseModel:
    id: UUID

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Medicine(BaseModel):
    name: str
    category: str
    manufacturer: str
    description: str
    price: float
    stock: int
    expiry_date: str
    requires_prescription: bool

@dataclass
class Customer(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    registration_date: str

@dataclass
class OrderItem:
    medicine_id: UUID
    quantity: int
    unit_price: float
    subtotal: float

@dataclass
class Order(BaseModel):
    customer_id: UUID
    order_date: str
    status: str
    items: List[OrderItem]
    total_amount: float

@dataclass
class PrescriptionMedicine:
    medicine_id: UUID
    dosage: str

@dataclass
class Prescription(BaseModel):
    customer_id: UUID
    doctor_name: str
    issue_date: str
    expiry_date: str
    medicines: List[PrescriptionMedicine]
    status: str

class DataGenerator(ABC):
    @abstractmethod
    def generate(self, num_records: int) -> List[Any]:
        pass

class MedicineGenerator(DataGenerator):
    CATEGORIES = ['Antibiotics', 'Painkillers', 'Vitamins', 'Antacids', 'Antiseptics']
    MANUFACTURERS = ['Pfizer', 'Johnson & Johnson', 'Roche', 'Novartis', 'GlaxoSmithKline']

    def generate(self, num_records: int) -> List[Medicine]:
        medicines: List[Medicine] = []
        for _ in range(num_records):
            medicine = Medicine(
                id=fake.uuid4(),
                name=fake.medicine_name(),
                category=random.choice(self.CATEGORIES),
                manufacturer=random.choice(self.MANUFACTURERS),
                description=fake.text(max_nb_chars=200),
                price=round(random.uniform(10, 1000), 2),
                stock=random.randint(0, 1000),
                expiry_date=(datetime.now() + timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
                requires_prescription=random.choice([True, False])
            )
            medicines.append(medicine)
        return medicines

class CustomerGenerator(DataGenerator):
    def generate(self, num_records: int) -> List[Customer]:
        customers: List[Customer] = []
        for _ in range(num_records):
            customer = Customer(
                id=fake.uuid4(),
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.address(),
                registration_date=fake.date_between(start_date='-2y').strftime('%Y-%m-%d')
            )
            customers.append(customer)
        return customers

class OrderGenerator(DataGenerator):
    def __init__(self, customers: List[Customer], medicines: List[Medicine]):
        self.customers = customers
        self.medicines = medicines

    def generate(self, num_records: int) -> List[Order]:
        orders: List[Order] = []
        for _ in range(num_records):
            num_items = random.randint(1, 5)
            items = random.sample(self.medicines, num_items)
            order_items: List[OrderItem] = []
            total = 0.0

            for item in items:
                quantity = random.randint(1, 3)
                price = item.price
                subtotal = quantity * price
                order_items.append(OrderItem(
                    medicine_id=item.id,
                    quantity=quantity,
                    unit_price=price,
                    subtotal=subtotal
                ))
                total += subtotal

            order = Order(
                id=fake.uuid4(),
                customer_id=random.choice(self.customers).id,
                order_date=fake.date_time_between(start_date='-1y').strftime('%Y-%m-%d %H:%M:%S'),
                status=random.choice(['pending', 'processing', 'completed', 'cancelled']),
                items=order_items,
                total_amount=round(total, 2)
            )
            orders.append(order)
        return orders

class PrescriptionGenerator(DataGenerator):
    def __init__(self, customers: List[Customer], medicines: List[Medicine]):
        self.customers = customers
        self.medicines = medicines

    def generate(self, num_records: int) -> List[Prescription]:
        prescriptions: List[Prescription] = []
        for _ in range(num_records):
            prescription_medicines = random.sample(
                [m for m in self.medicines if m.requires_prescription],
                random.randint(1, 3)
            )
            
            prescription = Prescription(
                id=fake.uuid4(),
                customer_id=random.choice(self.customers).id,
                doctor_name=fake.name(),
                issue_date=fake.date_between(start_date='-6m').strftime('%Y-%m-%d'),
                expiry_date=fake.date_between(start_date='today', end_date='+3m').strftime('%Y-%m-%d'),
                medicines=[
                    PrescriptionMedicine(
                        medicine_id=m.id,
                        dosage=f"{random.randint(1, 3)} times daily"
                    ) for m in prescription_medicines
                ],
                status=random.choice(['active', 'expired', 'fulfilled'])
            )
            prescriptions.append(prescription)
        return prescriptions

class MockDataGenerator:
    def __init__(self, output_dir: str = 'mock_data'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _save_to_json(self, data: List[Any], filename: str) -> None:
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, 'w') as f:
            json.dump([item.to_dict() for item in data], f, indent=2, default=str)

    def generate_all(self) -> None:
        # Generate data in sequence
        medicine_gen = MedicineGenerator()
        medicines = medicine_gen.generate(50)
        self._save_to_json(medicines, 'medicines.json')

        customer_gen = CustomerGenerator()
        customers = customer_gen.generate(20)
        self._save_to_json(customers, 'customers.json')

        order_gen = OrderGenerator(customers, medicines)
        orders = order_gen.generate(100)
        self._save_to_json(orders, 'orders.json')

        prescription_gen = PrescriptionGenerator(customers, medicines)
        prescriptions = prescription_gen.generate(30)
        self._save_to_json(prescriptions, 'prescriptions.json')

        print("Mock data generated successfully!")

def main() -> None:
    generator = MockDataGenerator()
    generator.generate_all()

if __name__ == '__main__':
    main() 