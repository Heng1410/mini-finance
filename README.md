Mini Finance

A modular Finance & ERP backend built with Django REST Framework and PostgreSQL.

The project is being built as a practical ERP system, with the goal of understanding how real business operations flow from business documents → operational changes → accounting transactions → financial reports.

Status: 🚧 Early DevelopmentThe project is intentionally growing module by module.

1. What Is Mini Finance?

Mini Finance is a backend ERP project designed around common business processes:

Company and organization management

Users, roles, and authentication

Products and inventory

Sales

Purchasing

Accounts Receivable

Accounts Payable

Accounting

General Ledger

Financial reporting

The important idea is that the modules are connected by business workflows.

For example, a sale is not just:

POST /sales-orders/

A real ERP process is closer to:

Customer
   ↓
Sales Order
   ↓
Delivery
   ↓
Inventory decreases
   ↓
Sales Invoice
   ↓
Accounts Receivable
   ↓
Customer Payment
   ↓
Journal Entry
   ↓
General Ledger
   ↓
Financial Reports

This workflow-oriented design is the main direction of the project.

2. How the ERP Works

High-Level ERP Flow

                         ┌──────────────┐
                         │   Customer   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ Sales Order  │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   Delivery   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  Inventory   │
                         │   decreases  │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ Sales Invoice│
                         └──────┬───────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │ Accounts Receivable  │
                    └──────────┬───────────┘
                               │
                               ▼
                       Customer Payment
                               │
                               ▼
                         ┌──────────────┐
                         │    Journal   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │    Ledger    │
                         └──────┬───────┘
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
          Trial Balance   Income Statement   Balance Sheet

The same concept applies to purchasing:

Vendor
   ↓
Purchase Order
   ↓
Goods Receipt
   ↓
Inventory increases
   ↓
Purchase Invoice
   ↓
Accounts Payable
   ↓
Vendor Payment
   ↓
Journal Entry
   ↓
General Ledger

3. Core Business Workflows

3.1 Order-to-Cash

The Order-to-Cash workflow handles a customer purchasing goods or services.

Customer
   ↓
Sales Quotation
   ↓
Sales Order
   ↓
Delivery
   ↓
Sales Invoice
   ↓
Accounts Receivable
   ↓
Customer Payment
   ↓
Accounting

Example

A customer orders:

Product A
Quantity: 10
Unit Price: $100
Total: $1,000

The ERP tracks the process:

Sales Order
    └── Customer ordered 10 units

Delivery
    └── 10 units leave warehouse

Invoice
    └── Customer owes $1,000

Payment
    └── Customer pays $1,000

Accounting
    └── AR is cleared
    └── Cash/Bank increases

4. Sales Order Workflow

The Sales Order is a business commitment, not necessarily a payment.

Customer
   │
   ▼
Sales Order
   │
   ├── Customer
   ├── Order Date
   ├── Status
   └── Order Lines
          │
          ├── Product
          ├── Quantity
          └── Unit Price

Typical lifecycle:

DRAFT
  ↓
CONFIRMED
  ↓
PARTIALLY_DELIVERED
  ↓
DELIVERED
  ↓
INVOICED
  ↓
COMPLETED

Possible cancellation:

DRAFT / CONFIRMED
        ↓
     CANCELLED

The exact statuses can evolve as the module becomes more complete.

5. Inventory Workflow

Inventory records the physical movement of products.

Purchase / Receipt
       ↓
Stock IN
       ↓
Warehouse
       │
       ▼
   Stock Balance
       │
       ▼
Sales / Delivery
       ↓
Stock OUT

Example:

Initial Stock = 100

Customer buys 10

Delivery
   ↓
Stock OUT = 10

Remaining Stock = 90

The important distinction is:

Sales Order ≠ Inventory Movement

A customer can place an order before the goods actually leave the warehouse.

The inventory movement normally happens when the delivery/stock issue is confirmed.

6. Purchasing Workflow

The purchasing process is the opposite side of sales.

Company
   ↓
Purchase Requisition
   ↓
Purchase Order
   ↓
Goods Receipt
   ↓
Inventory increases
   ↓
Purchase Invoice
   ↓
Accounts Payable
   ↓
Vendor Payment

Example:

Purchase 50 units
       ↓
Goods received
       ↓
Inventory +50
       ↓
Vendor invoice received
       ↓
Company owes vendor
       ↓
Vendor paid

7. Accounts Receivable Workflow

Accounts Receivable represents money customers owe the company.

Sales Invoice
     ↓
AR Outstanding
     ↓
Customer Payment
     ↓
AR Reduced
     ↓
Fully Paid

Example:

Invoice = $1,000

Payment = $600

Outstanding AR = $400

After another $400 payment:

Outstanding AR = $0

AR should therefore be connected to both:

Sales
  │
  ▼
Invoice
  │
  ▼
Accounts Receivable
  │
  ▼
Payment

8. Accounts Payable Workflow

Accounts Payable represents money the company owes vendors.

Purchase Invoice
       ↓
AP Outstanding
       ↓
Vendor Payment
       ↓
AP Reduced
       ↓
Fully Paid

Example:

Vendor Invoice = $2,000

Payment = $1,500

Outstanding AP = $500

9. Accounting Workflow

Accounting is where operational events become financial records.

The general flow is:

Business Event
      ↓
Business Transaction
      ↓
Accounting Rules
      ↓
Journal Entry
      ↓
General Ledger
      ↓
Financial Reports

For example, a credit sale of $1,000 could create:

Debit
Accounts Receivable     $1,000

Credit
Sales Revenue           $1,000

When the customer pays:

Debit
Bank / Cash             $1,000

Credit
Accounts Receivable     $1,000

The accounting system should maintain:

Total Debits = Total Credits

10. General Ledger

The General Ledger collects posted accounting transactions by account.

Journal Entries
      ↓
General Ledger
      ↓
Account Balances

Example:

Account: Cash

Date        Debit       Credit      Balance
--------------------------------------------
Jan 01      $5,000                  $5,000
Jan 03                  $1,000      $4,000
Jan 05      $2,000                  $6,000

The ledger becomes the foundation for financial reporting.

11. Financial Reporting Workflow

Financial reports should ultimately be generated from accounting data.

Journal Entries
      ↓
General Ledger
      ↓
Trial Balance
      │
      ├───────────────┐
      ▼               ▼
Income Statement   Balance Sheet
      │
      └───────────────┐
                      ▼
                Financial Analysis

Planned reports include:

Trial Balance

General Ledger Detail

Income Statement

Balance Sheet

Cash Flow Statement

Accounts Receivable Aging

Accounts Payable Aging

Inventory Valuation

12. How Modules Connect

The project should not be treated as independent CRUD applications.

The important relationships are:

                 ┌────────────┐
                 │  Customer  │
                 └─────┬──────┘
                       │
                       ▼
                ┌──────────────┐
                │ Sales Order  │
                └──────┬───────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       ┌───────────┐       ┌───────────┐
       │ Inventory │       │  Invoice  │
       └─────┬─────┘       └─────┬─────┘
             │                   │
             │                   ▼
             │             ┌───────────┐
             │             │    AR     │
             │             └─────┬─────┘
             │                   │
             │                   ▼
             │               Payment
             │                   │
             └─────────┬─────────┘
                       ▼
                 ┌───────────┐
                 │  Journal  │
                 └─────┬─────┘
                       ▼
                 ┌───────────┐
                 │  Ledger   │
                 └─────┬─────┘
                       ▼
                 ┌───────────┐
                 │  Reports  │
                 └───────────┘

This is the core architecture to keep in mind when adding new modules.

13. Technical Architecture

The project currently follows a modular monolith architecture.

Client
  │
  ▼
Django REST Framework
  │
  ├── Authentication
  ├── Company
  ├── Employee
  ├── Account
  ├── Inventory
  ├── Sales
  ├── Purchasing
  ├── AR
  ├── AP
  ├── Journal
  └── Ledger
          │
          ▼
      PostgreSQL

Each business domain is separated into a Django application.

This allows the project to remain simple while still establishing boundaries that can scale later.

14. Request Flow

A typical API request follows:

HTTP Request
     ↓
URL Router
     ↓
ViewSet / API View
     ↓
Serializer
     ↓
Business Logic
     ↓
Model / ORM
     ↓
PostgreSQL
     ↓
Serializer
     ↓
HTTP Response

For a business transaction, the flow can become:

HTTP Request
     ↓
Validation
     ↓
Business Service
     ↓
Database Transaction
     ├── Update operational data
     ├── Update inventory
     ├── Create accounting entries
     └── Create audit information
     ↓
Commit
     ↓
Response

Complex business rules should live in a business/service layer rather than being hidden inside API views.

15. Current Project Structure

The repository currently contains these major Django applications:

mini-finance/
│
├── account/
├── accounts_receivable/
├── authentication/
├── base/
├── company/
├── config/
├── department/
├── employee/
├── inventory/
├── journal/
├── ledger/
├── role/
├── sequence/
├── user/
│
├── manage.py
├── requirements.txt
└── README.md

The current repository structure can be viewed on GitHub:

https://github.com/Heng1410/mini-finance

16. Technology Stack

Technology

Purpose

Python

Backend language

Django

Web framework

Django REST Framework

REST APIs

PostgreSQL

Database

JWT

Authentication

Django Filter

Filtering

DRF Spectacular

OpenAPI documentation

Pillow

Image/media handling

python-dotenv

Environment configuration

17. Project Design Principles

Business First

Before implementing an endpoint, understand:

What business problem does this solve?
Who performs the action?
What happens before it?
What happens after it?
What data changes?
Does accounting change?
Does inventory change?

Documents vs Transactions

An important ERP concept is separating documents from actual effects.

For example:

Sales Order
    ↓
Business commitment

Delivery
    ↓
Physical inventory movement

Invoice
    ↓
Financial receivable

Payment
    ↓
Cash movement

Do not automatically treat every document as the same type of transaction.

Database Integrity

Important financial and operational rules should be protected by:

Foreign keys

Unique constraints

Check constraints

Database transactions

Appropriate indexes

Decimal fields for monetary values

Financial Records

Financial records should be auditable and should generally not be silently overwritten after posting.

Prefer:

Original Transaction
       ↓
Reversal / Adjustment
       ↓
Corrected Transaction

rather than modifying historical accounting records without traceability.

18. Adding a New ERP Module

When adding a new module, follow this process:

1. Understand the business process
          ↓
2. Identify actors
          ↓
3. Identify business documents
          ↓
4. Identify entities and relationships
          ↓
5. Define document lifecycle/statuses
          ↓
6. Define business rules
          ↓
7. Identify inventory impact
          ↓
8. Identify accounting impact
          ↓
9. Design database
          ↓
10. Implement models
          ↓
11. Implement business logic
          ↓
12. Implement serializers
          ↓
13. Implement API
          ↓
14. Add tests
          ↓
15. Update documentation

For example, before creating Sales Order code, understand:

Customer
   ↓
Sales Order
   ↓
Order Lines
   ↓
Product
   ↓
Delivery
   ↓
Invoice
   ↓
Payment

This prevents the project from becoming a collection of unrelated CRUD endpoints.

19. Planned Modules

Organization

Company

Department

Employee

User

Role

Finance

Chart of Accounts

Journal

General Ledger

Accounts Receivable

Accounts Payable

Fixed Assets

Tax

Bank Reconciliation

Financial Period

Sales

Customer

Sales Quotation

Sales Order

Delivery

Sales Invoice

Customer Payment

Purchasing

Vendor

Purchase Requisition

Purchase Order

Goods Receipt

Purchase Invoice

Vendor Payment

Inventory

Inventory foundation

Product

Warehouse

Stock Movement

Stock Transfer

Stock Adjustment

Inventory Valuation

Reports

Trial Balance

General Ledger Detail

Income Statement

Balance Sheet

Cash Flow Statement

AR Aging

AP Aging

Inventory Valuation

20. Future Scalability

The initial architecture is intentionally a modular monolith.

                  Django Application
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
    Finance            Sales           Inventory
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
                     PostgreSQL

If the system grows significantly, individual domains can later be extracted into services:

                   API Gateway
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Finance          Sales        Inventory
    Service         Service        Service
        │              │              │
        └──────────────┼──────────────┘
                       │
                Message Broker
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Workers      Reporting    Notifications

Microservices should only be introduced when there is a real reason to do so. Clear module boundaries come first.

21. Development Setup

Clone

git clone https://github.com/Heng1410/mini-finance.git
cd mini-finance

Virtual Environment

Windows

python -m venv .venv
.venv\Scripts\activate

Linux / macOS / WSL

python3 -m venv .venv
source .venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Environment

Create .env and configure the Django/PostgreSQL settings required by the project.

Never commit secrets or production credentials.

Database

Create the PostgreSQL database and run:

python manage.py migrate

Run

python manage.py runserver

22. Testing

Run all tests:

python manage.py test

Run a specific module:

python manage.py test journal

Before committing:

python manage.py check
python manage.py makemigrations --check
python manage.py test

23. ERP Mental Model

When working on this project, think in this order:

                BUSINESS
                   │
                   ▼
              DOCUMENT
                   │
                   ▼
              WORKFLOW
                   │
          ┌────────┴────────┐
          ▼                 ▼
      OPERATIONS         FINANCE
          │                 │
          ▼                 ▼
      Inventory          Journal
          │                 │
          └────────┬────────┘
                   ▼
                Ledger
                   │
                   ▼
                Reports

The goal is not to build:

Model → Serializer → View → CRUD

The goal is to build:

Business Requirement
        ↓
Business Workflow
        ↓
Business Rules
        ↓
Database Model
        ↓
Service / Transaction Logic
        ↓
API
        ↓
Operational + Financial Effects
        ↓
Reports

That is the core design philosophy of Mini Finance.

24. Vision

Mini Finance is intended to evolve into a realistic ERP backend where business operations are connected to financial consequences.

The long-term goal is:

Customer / Vendor
       ↓
Business Documents
       ↓
Operational Transactions
       ↓
Inventory / AR / AP
       ↓
Accounting
       ↓
General Ledger
       ↓
Financial Reports

The project should remain:

Modular

Understandable

Testable

Auditable

Financially consistent

Easy to extend

As new ERP modules are added, their workflows should connect back to the existing operational and accounting foundation.