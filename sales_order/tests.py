from datetime import date
from decimal import Decimal

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from accounts_receivable.models.customer import Customer
from company.models.company import Company
from department.models.department import Department
from employee.models.employee import Employee
from inventory.constants import StockReserveStatus
from inventory.models.products import Product
from inventory.models.stock_reservation import StockReservation
from role.models.role import Role
from sales_order.constants import SalesOrderStatus
from sales_order.models.sales_order import SalesOrder
from sales_order.models.sales_order_item import SalesOrderItem
from sales_order.services.sales_order_service import SalesOrderService
from sequence.models.sequence import Sequence


class SalesOrderServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            code="TC",
            legal_name="Test Company Ltd.",
            registration_number="REG001",
            tax_number="TAX001",
            email="company@test.com",
            phone="012345678",
            country="Cambodia",
            currency="USD",
            timezone="Asia/Phnom_Penh",
            fiscal_year_start=date(2026, 1, 1),
        )

        cls.other_company = Company.objects.create(
            name="Other Company",
            code="OC",
            legal_name="Other Company Ltd.",
            registration_number="REG002",
            tax_number="TAX002",
            email="other@test.com",
            phone="012345679",
            country="Cambodia",
            currency="USD",
            timezone="Asia/Phnom_Penh",
            fiscal_year_start=date(2026, 1, 1),
        )

        cls.department = Department.objects.create(
            company=cls.company,
            name="Sales",
            code="SALES",
        )

        cls.role = Role.objects.create(
            company=cls.company,
            name="Sales Staff",
            code="SALES_STAFF",
        )

        cls.employee = Employee.objects.create(
            company=cls.company,
            department=cls.department,
            role=cls.role,
            employee_code="EMP001",
            first_name="Test",
            last_name="Employee",
            email="employee@test.com",
            phone="012345678",
            hire_date=date(2026, 1, 1),
            job_title="Sales Staff",
        )

        cls.other_department = Department.objects.create(
            company=cls.other_company,
            name="Other Sales",
            code="OTHER_SALES",
        )

        cls.other_role = Role.objects.create(
            company=cls.other_company,
            name="Other Staff",
            code="OTHER_STAFF",
        )

        cls.other_employee = Employee.objects.create(
            company=cls.other_company,
            department=cls.other_department,
            role=cls.other_role,
            employee_code="EMP002",
            first_name="Other",
            last_name="Employee",
            email="other.employee@test.com",
            phone="012345679",
            hire_date=date(2026, 1, 1),
            job_title="Sales Staff",
        )

        cls.customer = Customer.objects.create(
            company=cls.company,
            code="CUS001",
            name="Test Customer",
            phone="012345680",
            email="customer@test.com",
            address="Phnom Penh",
        )

        cls.other_customer = Customer.objects.create(
            company=cls.other_company,
            code="CUS002",
            name="Other Customer",
            phone="012345681",
            email="other.customer@test.com",
            address="Siem Reap",
        )

        cls.product = Product.objects.create(
            company=cls.company,
            sku="PROD001",
            name="Product One",
            stock_quantity=100,
        )

        cls.product_two = Product.objects.create(
            company=cls.company,
            sku="PROD002",
            name="Product Two",
            stock_quantity=50,
        )

        cls.other_product = Product.objects.create(
            company=cls.other_company,
            sku="PROD003",
            name="Other Product",
            stock_quantity=100,
        )

        cls.sequence = Sequence.objects.create(
            company=cls.company,
            key="SALES_ORDER",
            prefix="SO-",
            last_number=0,
        )

        cls.other_sequence = Sequence.objects.create(
            company=cls.other_company,
            key="SALES_ORDER",
            prefix="OSO-",
            last_number=0,
        )

    def create_order(self):
        return SalesOrderService.create_order(
            company=self.company,
            customer=self.customer,
            employee=self.employee,
        )

    def add_item(
        self,
        order,
        product=None,
        quantity=1,
        unit_price=Decimal("100.00"),
    ):
        return SalesOrderService.add_item(
            company=self.company,
            order=order,
            product=product or self.product,
            quantity=quantity,
            unit_price=unit_price,
        )

    def test_create_order(self):
        order = self.create_order()

        self.assertIsNotNone(order.pk)
        self.assertEqual(order.company, self.company)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.created_by, self.employee)
        self.assertEqual(order.order_number, "SO-000001")
        self.assertEqual(order.status, SalesOrderStatus.DRAFT)
        self.assertEqual(order.total_amount, Decimal("0"))

    def test_create_multiple_orders_generates_sequential_numbers(self):
        first_order = self.create_order()
        second_order = self.create_order()

        self.assertEqual(first_order.order_number, "SO-000001")
        self.assertEqual(second_order.order_number, "SO-000002")

        self.sequence.refresh_from_db()
        self.assertEqual(self.sequence.last_number, 2)

    def test_create_order_only_uses_customer_from_same_company(self):
        with self.assertRaises(Customer.DoesNotExist):
            SalesOrderService.create_order(
                company=self.company,
                customer=self.other_customer,
                employee=self.employee,
            )

        self.assertEqual(SalesOrder.objects.count(), 0)

    def test_add_item(self):
        order = self.create_order()

        item = self.add_item(
            order=order,
            quantity=2,
            unit_price=Decimal("100.00"),
        )

        order.refresh_from_db()

        self.assertIsNotNone(item.pk)
        self.assertEqual(item.sales_order, order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.unit_price, Decimal("100.00"))
        self.assertEqual(item.sub_total, Decimal("200.00"))
        self.assertEqual(order.total_amount, Decimal("200.00"))

    def test_add_multiple_items_updates_order_total(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("100.00"),
        )

        self.add_item(
            order=order,
            product=self.product_two,
            quantity=3,
            unit_price=Decimal("50.00"),
        )

        order.refresh_from_db()

        self.assertEqual(
            order.total_amount,
            Decimal("350.00"),
        )

        self.assertEqual(
            SalesOrderItem.objects.filter(sales_order=order).count(),
            2,
        )

    def test_add_item_only_accepts_product_from_same_company(self):
        order = self.create_order()

        with self.assertRaises(Product.DoesNotExist):
            self.add_item(
                order=order,
                product=self.other_product,
                quantity=1,
                unit_price=Decimal("100.00"),
            )

        self.assertEqual(
            SalesOrderItem.objects.filter(sales_order=order).count(),
            0,
        )

    def test_cannot_add_zero_quantity(self):
        order = self.create_order()

        with self.assertRaises(ValidationError) as context:
            self.add_item(
                order=order,
                quantity=0,
                unit_price=Decimal("100.00"),
            )

        self.assertIn("Quantity must be greater than zero.", str(context.exception))

    def test_cannot_add_negative_quantity(self):
        order = self.create_order()

        with self.assertRaises(ValidationError) as context:
            self.add_item(
                order=order,
                quantity=-1,
                unit_price=Decimal("100.00"),
            )

        self.assertIn("Quantity must be greater than zero.", str(context.exception))

    def test_cannot_add_negative_unit_price(self):
        order = self.create_order()

        with self.assertRaises(ValidationError) as context:
            self.add_item(
                order=order,
                quantity=1,
                unit_price=Decimal("-1.00"),
            )

        self.assertIn(
            "Unit price cannot be negative.",
            str(context.exception),
        )

    def test_zero_unit_price_is_allowed(self):
        order = self.create_order()

        item = self.add_item(
            order=order,
            quantity=2,
            unit_price=Decimal("0.00"),
        )

        order.refresh_from_db()

        self.assertEqual(item.sub_total, Decimal("0.00"))
        self.assertEqual(order.total_amount, Decimal("0.00"))

    def test_cannot_add_same_product_twice(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=Decimal("100.00"),
        )

        with self.assertRaises(ValidationError) as context:
            self.add_item(
                order=order,
                product=self.product,
                quantity=2,
                unit_price=Decimal("200.00"),
            )

        self.assertIn(
            "Product already exists in this order.",
            str(context.exception),
        )

        self.assertEqual(
            SalesOrderItem.objects.filter(sales_order=order).count(),
            1,
        )

    def test_cannot_add_item_after_submit(self):
        order = self.create_order()

        self.add_item(
            order=order,
            quantity=2,
            unit_price=Decimal("100.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        with self.assertRaises(ValidationError) as context:
            self.add_item(
                order=order,
                quantity=1,
                unit_price=Decimal("100.00"),
            )

        self.assertIn(
            "Only draft orders can have items added.",
            str(context.exception),
        )

    def test_cannot_submit_empty_order(self):
        order = self.create_order()

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.submit_order(
                company=self.company,
                order=order,
                employee=self.employee,
            )

        self.assertIn(
            "Order must have at least one item.",
            str(context.exception),
        )

        order.refresh_from_db()

        self.assertEqual(order.status, SalesOrderStatus.DRAFT)
        self.assertEqual(
            StockReservation.objects.filter(sales_order=order).count(),
            0,
        )

    def test_submit_order_creates_pending_stock_reservations(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        submitted_order = SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        submitted_order.refresh_from_db()

        reservation = StockReservation.objects.get(
            sales_order=submitted_order,
            product=self.product,
        )

        self.assertEqual(
            submitted_order.status,
            SalesOrderStatus.PENDING,
        )
        self.assertEqual(reservation.quantity, 10)
        self.assertEqual(
            reservation.status,
            StockReserveStatus.PENDING,
        )
        self.assertEqual(
            reservation.reserved_by,
            self.employee,
        )
        self.assertIsNotNone(reservation.expires_at)

    def test_submit_order_creates_one_reservation_per_item(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        self.add_item(
            order=order,
            product=self.product_two,
            quantity=5,
            unit_price=Decimal("50.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        reservations = StockReservation.objects.filter(
            sales_order=order
        ).order_by("product_id")

        self.assertEqual(reservations.count(), 2)

        first_reservation = reservations.get(product=self.product)
        second_reservation = reservations.get(product=self.product_two)

        self.assertEqual(first_reservation.quantity, 10)
        self.assertEqual(second_reservation.quantity, 5)
        self.assertEqual(
            first_reservation.status,
            StockReserveStatus.PENDING,
        )
        self.assertEqual(
            second_reservation.status,
            StockReserveStatus.PENDING,
        )

    def test_submit_order_does_not_reduce_stock(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=20,
            unit_price=Decimal("100.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            100,
        )

    def test_cannot_submit_non_draft_order(self):
        order = self.create_order()

        self.add_item(
            order=order,
            quantity=1,
            unit_price=Decimal("100.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.submit_order(
                company=self.company,
                order=order,
                employee=self.employee,
            )

        self.assertIn(
            "Only draft orders can be submitted.",
            str(context.exception),
        )

    def test_submit_rolls_back_all_reservations_when_one_item_fails(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=20,
            unit_price=Decimal("100.00"),
        )

        self.add_item(
            order=order,
            product=self.product_two,
            quantity=999,
            unit_price=Decimal("50.00"),
        )

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.submit_order(
                company=self.company,
                order=order,
                employee=self.employee,
            )

        self.assertIn(
            "Insufficient available stock.",
            str(context.exception),
        )

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            SalesOrderStatus.DRAFT,
        )

        self.assertEqual(
            StockReservation.objects.filter(sales_order=order).count(),
            0,
        )

        self.product.refresh_from_db()
        self.product_two.refresh_from_db()

        self.assertEqual(self.product.stock_quantity, 100)
        self.assertEqual(self.product_two.stock_quantity, 50)

    def test_confirm_order(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        confirmed_order = SalesOrderService.confirm_order(
            company=self.company,
            order=order,
        )

        confirmed_order.refresh_from_db()
        self.product.refresh_from_db()

        reservation = StockReservation.objects.get(
            sales_order=order,
            product=self.product,
        )

        self.assertEqual(
            confirmed_order.status,
            SalesOrderStatus.CONFIRMED,
        )

        self.assertEqual(
            self.product.stock_quantity,
            90,
        )

        self.assertEqual(
            reservation.status,
            StockReserveStatus.CONFIRMED,
        )

    def test_confirm_order_confirms_all_reservations(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        self.add_item(
            order=order,
            product=self.product_two,
            quantity=5,
            unit_price=Decimal("50.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        SalesOrderService.confirm_order(
            company=self.company,
            order=order,
        )

        self.product.refresh_from_db()
        self.product_two.refresh_from_db()

        reservations = StockReservation.objects.filter(
            sales_order=order
        )

        self.assertEqual(reservations.count(), 2)

        self.assertTrue(
            all(
                reservation.status == StockReserveStatus.CONFIRMED
                for reservation in reservations
            )
        )

        self.assertEqual(self.product.stock_quantity, 90)
        self.assertEqual(self.product_two.stock_quantity, 45)

    def test_confirm_order_requires_pending_reservation(self):
        order = self.create_order()

        self.add_item(
            order=order,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        order.status = SalesOrderStatus.PENDING
        order.save(update_fields=["status"])

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.confirm_order(
                company=self.company,
                order=order,
            )

        self.assertIn(
            "Order must have at least one stock reservation.",
            str(context.exception),
        )

        order.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            order.status,
            SalesOrderStatus.PENDING,
        )
        self.assertEqual(
            self.product.stock_quantity,
            100,
        )

    def test_cannot_confirm_draft_order(self):
        order = self.create_order()

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.confirm_order(
                company=self.company,
                order=order,
            )

        self.assertIn(
            "Only pending orders can be confirmed.",
            str(context.exception),
        )

    def test_cannot_confirm_confirmed_order(self):
        order = self.create_order()

        self.add_item(
            order=order,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        SalesOrderService.confirm_order(
            company=self.company,
            order=order,
        )

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.confirm_order(
                company=self.company,
                order=order,
            )

        self.assertIn(
            "Only pending orders can be confirmed.",
            str(context.exception),
        )

    def test_cancel_order(self):
        order = self.create_order()

        self.add_item(
            order=order,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        cancelled_order = SalesOrderService.cancel_order(
            company=self.company,
            order=order,
        )

        cancelled_order.refresh_from_db()

        reservation = StockReservation.objects.get(
            sales_order=order,
            product=self.product,
        )

        self.assertEqual(
            cancelled_order.status,
            SalesOrderStatus.CANCELLED,
        )

        self.assertEqual(
            reservation.status,
            StockReserveStatus.RELEASED,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            100,
        )

    def test_cancel_releases_all_pending_reservations(self):
        order = self.create_order()

        self.add_item(
            order=order,
            product=self.product,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        self.add_item(
            order=order,
            product=self.product_two,
            quantity=5,
            unit_price=Decimal("50.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        SalesOrderService.cancel_order(
            company=self.company,
            order=order,
        )

        reservations = StockReservation.objects.filter(
            sales_order=order
        )

        self.assertEqual(reservations.count(), 2)

        self.assertTrue(
            all(
                reservation.status == StockReserveStatus.RELEASED
                for reservation in reservations
            )
        )

    def test_cancel_requires_pending_reservation(self):
        order = self.create_order()

        order.status = SalesOrderStatus.PENDING
        order.save(update_fields=["status"])

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.cancel_order(
                company=self.company,
                order=order,
            )

        self.assertIn(
            "Order must have at least one stock reservation.",
            str(context.exception),
        )

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            SalesOrderStatus.PENDING,
        )

    def test_cannot_cancel_draft_order(self):
        order = self.create_order()

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.cancel_order(
                company=self.company,
                order=order,
            )

        self.assertIn(
            "Only pending orders can be cancelled.",
            str(context.exception),
        )

    def test_cannot_cancel_confirmed_order(self):
        order = self.create_order()

        self.add_item(
            order=order,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        SalesOrderService.confirm_order(
            company=self.company,
            order=order,
        )

        with self.assertRaises(ValidationError) as context:
            SalesOrderService.cancel_order(
                company=self.company,
                order=order,
            )

        self.assertIn(
            "Only pending orders can be cancelled.",
            str(context.exception),
        )

    def test_cancel_does_not_restore_stock_because_stock_was_not_yet_deducted(
        self,
    ):
        order = self.create_order()

        self.add_item(
            order=order,
            quantity=10,
            unit_price=Decimal("100.00"),
        )

        SalesOrderService.submit_order(
            company=self.company,
            order=order,
            employee=self.employee,
        )

        SalesOrderService.cancel_order(
            company=self.company,
            order=order,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            100,
        )

    def test_model_relationships(self):
        order = self.create_order()

        item = self.add_item(
            order=order,
            quantity=2,
            unit_price=Decimal("100.00"),
        )

        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.created_by, self.employee)

        self.assertIn(item, order.sales_order_items.all())
        self.assertEqual(item.sales_order, order)
        self.assertEqual(item.product, self.product)

    def test_order_total_is_stored_on_order(self):
        order = self.create_order()

        self.add_item(
            order=order,
            quantity=2,
            unit_price=Decimal("125.50"),
        )

        order.refresh_from_db()

        self.assertEqual(
            order.total_amount,
            Decimal("251.00"),
        )