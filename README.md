# Scanofinder - QR Code Item Management System

A Django + AngularJS application for managing physical items using QR codes. Parents can create QR codes for items, assign them to children, and receive messages when items are found.

## Features

- **User Management**: Registration, login, and profile management
- **Child Management**: Add and manage children with their information
- **Item Management**: Create items, generate QR codes with descriptive labels, and upload images
- **QR Code Generation**: Automatic QR code generation with item name labels
- **Messaging System**: Public endpoint for non-users to send messages when scanning QR codes
- **Subscription System**: R200/year subscription with Stripe integration
- **Modern UI**: Vibrant, young design with responsive layout

## Installation

1. **Clone the repository**
   ```bash
   cd "Scanofinder django"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Stripe keys
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Frontend: http://localhost:8000
   - Admin: http://localhost:8000/admin

## Configuration

### Stripe Setup

1. Create a Stripe account at https://stripe.com
2. Get your API keys from the Stripe dashboard
3. Add them to your `.env` file:
   ```
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   ```

### Update Stripe Key in Frontend

Edit `static/js/controllers.js` in the `SubscriptionController` and replace:
```javascript
$scope.stripe = Stripe('pk_test_your_key_here');
```
with your actual Stripe publishable key.

## Project Structure

```
scanofinder/
├── accounts/          # User authentication and profiles
├── children/          # Child management
├── items/            # Item and QR code management
├── payments/          # Subscription and payment processing
├── messages/          # Messaging system
├── static/            # Frontend assets (CSS, JS, templates)
├── templates/         # Django templates
└── scanofinder/       # Main project settings
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile

### Children
- `GET /api/children/` - List children
- `POST /api/children/` - Create child
- `GET /api/children/{id}/` - Get child details
- `PUT /api/children/{id}/` - Update child
- `DELETE /api/children/{id}/` - Delete child

### Items
- `GET /api/items/` - List items
- `POST /api/items/` - Create item (generates QR code)
- `GET /api/items/{id}/` - Get item details
- `PUT /api/items/{id}/` - Update item
- `DELETE /api/items/{id}/` - Delete item
- `GET /api/items/qr/{qr_data}/` - Get item by QR code (public)

### Messages
- `GET /api/messages/` - List messages (authenticated)
- `POST /api/messages/create/` - Create message (public, for QR scanning)
- `GET /api/messages/{id}/` - Get message details
- `PUT /api/messages/{id}/` - Mark message as read

### Payments
- `GET /api/payments/subscription/` - Get subscription status
- `POST /api/payments/create-intent/` - Create payment intent
- `POST /api/payments/confirm/` - Confirm payment
- `GET /api/payments/history/` - Payment history

## Usage

1. **Register an account**
2. **Subscribe** (R200/year) to activate full features
3. **Add children** to your profile
4. **Create items** and generate QR codes
5. **Print QR codes** and attach to items
6. **Receive messages** when someone scans your QR code

## Legal Pages

The app includes:
- Terms and Conditions (South African law compliant)
- Privacy Policy (POPI Act compliant)

## Technologies Used

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: AngularJS 1.8, Bootstrap 5
- **Payment**: Stripe
- **QR Codes**: qrcode library
- **Database**: SQLite (development)

## License

All rights reserved.

## Support

For support, contact through the application dashboard.

