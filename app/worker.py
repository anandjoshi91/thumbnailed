import time
from PIL import Image, ExifTags
import requests
from io import BytesIO
import base64
import smtplib
import imghdr
import app.config as cfg

from email.message import EmailMessage


def processImage(email_id, img_url):
    """
    Create a thumbnail and share it as base 64 image

    Args:
        param1 (str): Email id to respond back to the user with thumbnail
        param2 (str): Image URL

    Returns:
        (str): Base 64 encoded image
    """
    result = None
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        fmt = img.format
        img = square_thumb(img, cfg.thumb["size"])
        buffer = BytesIO()
        img.save(buffer, format=fmt)
        thumb = buffer.getvalue()
        result = "data:image/jpeg;base64,"+str(base64.b64encode(thumb), "utf-8")
    except Exception:
        print("Exception occurred while processing image")
    return result



def square_thumb(img, thumb_size):
    """
    Crop a square image and generate a thumbnail
    """
    THUMB_SIZE = (thumb_size,thumb_size)
    width, height = img.size

    if width > height:
        delta = width - height
        left = int(delta/2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta/2)
        right = width
        lower = width + upper

    img = img.crop((left, upper, right, lower))
    img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

    return img


def sendEmail(file, email_id):
    """
    Send thumbnail in an email to the client
    """
    print("Send email to = ", email_id)
    print("File = ",file)

    msg = EmailMessage()
    msg['Subject'] = 'Your thumbnail is ready'
    msg['From'] = 'thumb@nailed.com'
    msg['To'] = email_id

    with open(file, 'rb') as fp:
        img_data = fp.read()
        msg.add_attachment(img_data, maintype='image',
                                subtype=imghdr.what(None, img_data))

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.send_message(msg)





