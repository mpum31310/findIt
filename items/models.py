from django.db import models
from accounts.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont


class Item(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items',
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_code_data = models.CharField(max_length=500, unique=True, blank=True, null=True)
    item_image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def generate_qr_code(self):
        # Generate unique QR code data if not already set
        if not self.qr_code_data:
            import uuid
            qr_data = f"scanofinder-item-{uuid.uuid4()}"
            self.qr_code_data = qr_data
        else:
            qr_data = self.qr_code_data
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image (convert qrcode's wrapper to a plain PIL Image)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        img = qr_img.get_image() if hasattr(qr_img, 'get_image') else qr_img
        img = img.convert('RGB')

        # Add descriptive text below QR code
        img_width, img_height = img.size
        text_height = 40
        new_height = img_height + text_height + 20
        
        # Create new image with space for text
        new_img = Image.new('RGB', (img_width, new_height), 'white')
        new_img.paste(img, (0, 0))
        
        # Add text
        draw = ImageDraw.Draw(new_img)
        try:
            font_paths = [
                "arial.ttf",
                "C:/Windows/Fonts/arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
            font = None
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, 20)
                    break
                except:
                    continue
            if not font:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Center the text
        text = self.name[:30]  # Limit text length
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = len(text) * 10
        text_x = (img_width - text_width) // 2
        text_y = img_height + 10
        
        draw.text((text_x, text_y), text, fill="black", font=font)
        
        # Save to BytesIO
        buffer = BytesIO()
        new_img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Save to model
        item_id = self.id if self.id else "temp"
        filename = f'qr_{item_id}_{qr_data[:8]}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        
        return self.qr_code
