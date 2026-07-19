# Scanofinder Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### 3. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

### 6. Access the Application
- Frontend: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## Getting Started

1. **Register an Account**
   - Go to http://localhost:8000
   - Click "Get Started" or "Register"
   - Fill in your details (username, email, cell number, password)

2. **Subscribe**
   - After registration, you'll need to subscribe (R200/year)
   - Go to the Subscription page
   - Enter your payment details (Stripe test mode)
   - Complete the payment

3. **Add Children**
   - Navigate to "Children" from the menu
   - Click "Add Child"
   - Enter child's name, surname, grade, and school

4. **Create Items**
   - Go to "Items" from the menu
   - Click "Add Item"
   - Enter item name, description, assign to child (optional), upload image (optional)
   - QR code will be automatically generated with the item name below it

5. **Download QR Codes**
   - View item details
   - Click "Download QR Code"
   - Print and attach to your items

6. **Receive Messages**
   - When someone scans your QR code, they can send you a message
   - Messages appear in the "Messages" section

## Stripe Setup

1. Create a Stripe account at https://stripe.com
2. Get your test API keys from the Stripe Dashboard
3. Add them to your `.env` file
4. The publishable key will be automatically loaded in the frontend

## Testing QR Code Scanning

To test the QR code scanning feature:
1. Create an item and download the QR code
2. The QR code contains data like: `scanofinder-item-{uuid}`
3. Access: `http://localhost:8000/#/scan/{qr_data}`
4. Fill in the message form and send

## Features

- ✅ User registration and authentication
- ✅ Profile management
- ✅ Child management (add, edit, view, delete)
- ✅ Item management with QR code generation
- ✅ QR codes with descriptive text labels
- ✅ Image upload for items
- ✅ Public messaging system (for QR code scanners)
- ✅ Subscription system (R200/year)
- ✅ Payment processing with Stripe
- ✅ Modern, vibrant UI design
- ✅ Responsive design
- ✅ Terms & Conditions (SA law compliant)
- ✅ Privacy Policy (POPI Act compliant)

## Troubleshooting

### QR Code Not Generating
- Ensure Pillow and qrcode libraries are installed
- Check that media directory has write permissions

### Payment Not Working
- Verify Stripe keys are correctly set in `.env`
- Check Stripe dashboard for payment status
- Ensure webhook is configured (for production)

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings.py

## Production Deployment

Before deploying to production:
1. Set `DEBUG=False` in `.env`
2. Change `SECRET_KEY` to a secure random string
3. Use a production database (PostgreSQL recommended)
4. Configure proper static file serving
5. Set up SSL/HTTPS
6. Configure Stripe webhooks
7. Update `ALLOWED_HOSTS` in settings.py

## Support

For issues or questions, check the README.md file or contact support through the application.

