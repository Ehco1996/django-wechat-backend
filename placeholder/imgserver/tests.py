from django.test import TestCase
from PIL import Image,ImageDraw
from io import BytesIO

# Create your tests here.


image = Image.new('RGB',(200,200))

draw = ImageDraw.Draw(image)

text = '{} X {}'.format(200,200)

textwidth,textheight = draw.textsize(text)


print(textheight,textwidth)

draw.text((100,100),text,fill=(255,123,255))

content = BytesIO()
image.save(content,'PNG')
content.seek(0)
print(content)
image.show()