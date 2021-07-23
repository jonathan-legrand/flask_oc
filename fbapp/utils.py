import random
from PIL import Image, ImageFont, ImageDraw
import textwrap
import os

from fbapp.models import Content, Gender


def find_content(gender):
    contents = Content.query.filter(Content.gender == Gender[gender]).all()
    return random.choice(contents)


class OpenGraphImage:
    """
    The image that is shared
    """

    def __init__(self, uid, first_name, desc):
        self.uid = uid
        background = self.base()
        self.location = self._location()
        # Print first_name
        self.print_on_img(background, first_name.capitalize(), 70, 50)

        # Print description
        sentences = textwrap.wrap(desc, width=60)
        current_h, pad = 180, 10

        for sentence in sentences:
            w, h = self.print_on_img(background, sentence, 40, current_h)
            current_h += h + pad

        background.save(self._path())

    @staticmethod
    def base():
        # Create a basic image
        img = Image.new('RGB', (1200, 630), '#18BC9C')
        return img

    @staticmethod
    def print_on_img(img, text, size, height):
        font = ImageFont.truetype(os.path.join('fbapp', 'static', 'fonts', 'Arcon-Regular.otf'), size)
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, font)
        position = ((img.width - w) / 2, height)
        draw.text(position, text, (255, 255, 255), font=font)
        return w, h

    def _location(self):
        return 'tmp/{}.jpg'.format(self.uid)

    def _path(self):
        return os.path.join('fbapp', 'static', 'tmp', '{}.jpg'.format(self.uid))



description = """
    Toi, tu sais comment utiliser la console ! Jamais à court d'idées pour réaliser ton objectif, tu es déterminé-e et persévérant-e. Tes amis disent d'ailleurs volontiers que tu as du caractère et que tu ne te laisses pas marcher sur les pieds. Un peu hacker sur les bords, tu aimes trouver des solutions à tout problème. N'aurais-tu pas un petit problème d'autorité ? ;-)
    """

if __name__ == "__main__":
    print('Puteuh')
    OpenGraphImage('Céline', description)
