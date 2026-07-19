# Scanofinder - Simplified Version

A simple Django application for managing physical items using QR codes.

## Current Features (Basic Version)

✅ **User Authentication**
- User registration
- Login/Logout
- Profile management

✅ **Item Management**
- Add items with name and description
- Upload item images
- Generate QR codes with descriptive text labels
- View, edit, and delete items

✅ **QR Code Scanning**
- Public scanning page (no login required)
- Anyone can scan a QR code and send a message to the item owner

✅ **Messaging**
- View messages from people who scanned your QR codes
- Mark messages as read

## Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run server**
   ```bash
   python manage.py runserver
   ```

5. **Access the app**
   - Frontend: http://localhost:8000
   - Admin: http://localhost:8000/admin

## Usage

1. **Register** - Create a free account
2. **Add Items** - Create items and generate QR codes
3. **Download QR Codes** - Print and attach to your items
4. **Receive Messages** - When someone scans your QR code, they can send you a message

## Future Features (To Add Later)

- [ ] Children/Person management
- [ ] Assign items to children
- [ ] Subscription/Payment system
- [ ] Email notifications
- [ ] Item categories
- [ ] Search functionality
- [ ] Export QR codes as PDF

## Project Structure

```
scanofinder/
├── accounts/          # User authentication
├── items/            # Item management and QR codes
├── item_messages/    # Messaging system
├── core/             # Home, about, terms, privacy pages
├── templates/        # Django templates
└── static/           # CSS and static files
```

## Technologies

- Django 4.2
- Bootstrap 5
- Pillow (for image processing)
- qrcode (for QR code generation)

