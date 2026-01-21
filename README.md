✈️ Airline Ticket Booking System (Django REST Framework)

A backend-only Airline Ticket Booking System built using Django Rest Framework (DRF) that demonstrates safe seat booking, payment handling, cancellations, refunds, and automatic seat expiry using a state machine–driven architecture.

This project focuses on business logic, data integrity, and state management, not UI or real payment gateways.

🚀 Project Objective

To design a robust backend system that:

Prevents double seat booking

Ensures valid booking state transitions

Handles payment success/failure safely

Supports cancellation and refund flows

Automatically expires unpaid seat holds

🧠 Booking State Machine
Booking States
State	Description
INITIATED	Booking created
SEAT_HELD	Seat temporarily locked (10 minutes)
PAYMENT_PENDING	Waiting for payment result
CONFIRMED	Payment successful
CANCELLED	Booking cancelled by user
EXPIRED	Seat hold expired
REFUNDED	Refund processed
Allowed State Transitions
INITIATED → SEAT_HELD → PAYMENT_PENDING → CONFIRMED
                         ↓
                      EXPIRED

CONFIRMED → CANCELLED → REFUNDED


🚫 Invalid state transitions are rejected at the API level

🛠 Tech Stack

Python

Django

Django REST Framework

SQLite (for development & testing)

Django ORM Transactions

📂 Project Structure
air_booking/
│
├── bookings/
│   ├── models.py        # Booking, Flight, Seat models
│   ├── views.py         # Booking APIs (create, pay, cancel, refund)
│   ├── serializers.py
│   ├── state_machine.py # Centralized state transitions
│   ├── tests.py         # Unit & business logic tests
│
├── air_booking/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
├── requirements.txt
└── db.sqlite3

🔑 Core Features
✅ Seat Locking

Uses database transactions

Prevents double booking of the same seat

Seat is locked for 10 minutes

💳 Mocked Payment Processing

Simulates payment success or failure

No real payment gateway involved

Payment result drives booking state

❌ Cancellation Handling

Only allowed for confirmed bookings

Changes state to CANCELLED

💰 Refund Processing

Refund allowed only once

Ensures idempotency

Final state: REFUNDED

⏱ Automatic Seat Expiry

Seat holds expire after 10 minutes

Moves booking to EXPIRED

Seat becomes available again

🔗 API Endpoints
Create Booking
POST /api/bookings/

Pay for Booking
POST /api/bookings/{id}/pay/


Success

{
  "message": "Payment successful",
  "state": "CONFIRMED"
}


Failure

{
  "message": "Payment failed",
  "state": "CANCELLED"
}

Cancel Booking
POST /api/bookings/{id}/cancel/

{
  "message": "Booking cancelled",
  "state": "CANCELLED"
}

Refund Booking
POST /api/bookings/{id}/refund/

{
  "message": "Refund processed",
  "state": "REFUNDED"
}

🧪 Testing

Unit tests validate:

State transitions

Seat expiry logic

Refund-only-once rule

Run tests using:

python manage.py test bookings

⚠️ Invalid Transition Example

Calling /pay/ on an expired booking:

{
  "error": "Invalid state transition from EXPIRED to PAYMENT_PENDING"
}


✔ Confirms state machine enforcement

❌ Out of Scope

Flight search

Frontend / UI

Real payment gateway

Notifications (email/SMS)

📌 Key Learnings & Concepts

State machine–driven backend design

Safe concurrent seat booking

Transactional integrity

Idempotent refund handling

Clean separation of business logic

👨‍💻 Author

Ashwani Kumar Dwivedi
Backend Developer | Django | DRF
