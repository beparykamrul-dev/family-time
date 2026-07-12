from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
CORS(app)

# Mock Database
users = {
    'admin@example.com': {
        'id': 1,
        'name': 'Admin User',
        'email': 'admin@example.com',
        'password': 'password123',
        'role': 'admin'
    }
}

customers = [
    {'id': 1, 'name': 'আলী আহমেদ', 'email': 'ali@example.com', 'phone': '01700000001', 'status': 'active', 'package': 'Silver'},
    {'id': 2, 'name': 'ফাতিমা বেগম', 'email': 'fatima@example.com', 'phone': '01700000002', 'status': 'active', 'package': 'Gold'},
    {'id': 3, 'name': 'মোহাম্মদ হোসেন', 'email': 'hosen@example.com', 'phone': '01700000003', 'status': 'inactive', 'package': 'Basic'},
]

invoices = [
    {'id': 'INV-001', 'customer': 'আলী আহমেদ', 'amount': 2500, 'status': 'paid', 'date': '2026-07-01'},
    {'id': 'INV-002', 'customer': 'ফাতিমা বেগম', 'amount': 3500, 'status': 'pending', 'date': '2026-07-05'},
    {'id': 'INV-003', 'customer': 'মোহাম্মদ হোসেন', 'amount': 1500, 'status': 'overdue', 'date': '2026-06-15'},
]

olts = [
    {'id': 1, 'name': 'OLT-Rakib-1', 'ip': '172.30.170.102', 'status': 'online', 'uptime': '45 days', 'ports': 16},
    {'id': 2, 'name': 'OLT-FTN-BDCOM', 'ip': '172.30.163.26', 'status': 'online', 'uptime': '32 days', 'ports': 32},
    {'id': 3, 'name': 'OLT-Corlink', 'ip': '172.30.170.234', 'status': 'offline', 'uptime': '0 days', 'ports': 16},
]

devices = [
    {'id': 1, 'name': 'ONU-1001', 'olt': 'OLT-Rakib-1', 'status': 'online', 'signal': '-15dBm', 'bandwidth': '100Mbps'},
    {'id': 2, 'name': 'ONU-1002', 'olt': 'OLT-Rakib-1', 'status': 'online', 'signal': '-18dBm', 'bandwidth': '50Mbps'},
    {'id': 3, 'name': 'ONU-1003', 'olt': 'OLT-FTN-BDCOM', 'status': 'offline', 'signal': '-40dBm', 'bandwidth': '0Mbps'},
]

# JWT Token Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# ========== AUTH ROUTES ==========

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = users.get(email)
    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid email or password'}), 401

    # Generate JWT Token
    token = jwt.encode(
        {
            'user': {'id': user['id'], 'email': user['email'], 'name': user['name']},
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {'id': user['id'], 'email': user['email'], 'name': user['name'], 'role': user['role']}
    }), 200

@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'message': 'Logout successful'}), 200

# ========== DASHBOARD ROUTES ==========

@app.route('/api/dashboard', methods=['GET'])
@token_required
def get_dashboard(current_user):
    return jsonify({
        'stats': {
            'totalCustomers': len(customers),
            'activeUsers': sum(1 for c in customers if c['status'] == 'active'),
            'monthlyRevenue': sum(inv['amount'] for inv in invoices if inv['status'] == 'paid'),
            'overdueCustomers': sum(1 for inv in invoices if inv['status'] == 'overdue')
        },
        'revenue': [
            {'name': 'Jan', 'revenue': 30000},
            {'name': 'Feb', 'revenue': 28000},
            {'name': 'Mar', 'revenue': 42000},
            {'name': 'Apr', 'revenue': 35000},
            {'name': 'May', 'revenue': 49000},
            {'name': 'Jun', 'revenue': 41000}
        ],
        'devices': olts[:2],
        'alerts': [
            {'id': 'a1', 'title': 'ONU-1001 Offline', 'time': '10m ago', 'severity': 'critical', 'details': 'ONU serial 1001 has lost link since 10 minutes.'},
            {'id': 'a2', 'title': 'High CPU on OLT-Rakib-1', 'time': '1h ago', 'severity': 'warning', 'details': 'CPU usage exceeded 85%'},
        ],
        'recent': [
            {'id': 'r1', 'type': 'payment', 'title': 'BILL-1024 paid', 'time': '2 hours ago'},
            {'id': 'r2', 'type': 'ticket', 'title': 'Ticket #334 assigned', 'time': '3 hours ago'},
        ]
    }), 200

# ========== CUSTOMERS ROUTES ==========

@app.route('/api/customers', methods=['GET'])
@token_required
def get_customers(current_user):
    return jsonify(customers), 200

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
@token_required
def get_customer(current_user, customer_id):
    customer = next((c for c in customers if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    return jsonify(customer), 200

@app.route('/api/customers', methods=['POST'])
@token_required
def create_customer(current_user):
    data = request.get_json()
    new_customer = {
        'id': max([c['id'] for c in customers]) + 1,
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'status': data.get('status', 'active'),
        'package': data.get('package', 'Basic')
    }
    customers.append(new_customer)
    return jsonify(new_customer), 201

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(current_user, customer_id):
    customer = next((c for c in customers if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    
    data = request.get_json()
    customer.update(data)
    return jsonify(customer), 200

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
@token_required
def delete_customer(current_user, customer_id):
    global customers
    customers = [c for c in customers if c['id'] != customer_id]
    return jsonify({'message': 'Customer deleted'}), 200

# ========== INVOICES ROUTES ==========

@app.route('/api/invoices', methods=['GET'])
@token_required
def get_invoices(current_user):
    return jsonify(invoices), 200

@app.route('/api/invoices', methods=['POST'])
@token_required
def create_invoice(current_user):
    data = request.get_json()
    new_invoice = {
        'id': f"INV-{len(invoices) + 1:03d}",
        'customer': data.get('customer'),
        'amount': data.get('amount'),
        'status': data.get('status', 'pending'),
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d'))
    }
    invoices.append(new_invoice)
    return jsonify(new_invoice), 201

# ========== OLTs ROUTES ==========

@app.route('/api/olts', methods=['GET'])
@token_required
def get_olts(current_user):
    return jsonify(olts), 200

@app.route('/api/olts/<int:olt_id>', methods=['GET'])
@token_required
def get_olt(current_user, olt_id):
    olt = next((o for o in olts if o['id'] == olt_id), None)
    if not olt:
        return jsonify({'message': 'OLT not found'}), 404
    return jsonify(olt), 200

# ========== DEVICES ROUTES ==========

@app.route('/api/devices', methods=['GET'])
@token_required
def get_devices(current_user):
    return jsonify(devices), 200

@app.route('/api/devices/<int:device_id>', methods=['GET'])
@token_required
def get_device(current_user, device_id):
    device = next((d for d in devices if d['id'] == device_id), None)
    if not device:
        return jsonify({'message': 'Device not found'}), 404
    return jsonify(device), 200

# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Route not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
