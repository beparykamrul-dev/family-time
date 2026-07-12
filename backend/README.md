# ISP-OS Backend

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Backend will run at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login with email & password
- `POST /api/auth/logout` - Logout

### Dashboard
- `GET /api/dashboard` - Get dashboard data (stats, revenue, alerts)

### Customers
- `GET /api/customers` - Get all customers
- `GET /api/customers/<id>` - Get specific customer
- `POST /api/customers` - Create new customer
- `PUT /api/customers/<id>` - Update customer
- `DELETE /api/customers/<id>` - Delete customer

### Invoices
- `GET /api/invoices` - Get all invoices
- `POST /api/invoices` - Create new invoice

### OLTs
- `GET /api/olts` - Get all OLTs
- `GET /api/olts/<id>` - Get specific OLT

### Devices
- `GET /api/devices` - Get all devices
- `GET /api/devices/<id>` - Get specific device

## Demo Credentials

```
Email: admin@example.com
Password: password123
```

## Authentication

All protected routes require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```
