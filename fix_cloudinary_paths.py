import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "villana.settings")
django.setup()

from maison.models import Photo, Video, Publicite, ParcellePhoto, HotelPhoto, Pays

def clean(model, field):
    for obj in model.objects.all():
        f = getattr(obj, field)
        if f and "cloudinary.com" in f.name:
            new = f.name.split("/upload/")[-1]
            f.name = new
            obj.save()
            print("FIXED:", model.__name__, obj.id)

clean(Photo, "photos")
clean(Video, "video")
clean(Publicite, "photos")
clean(ParcellePhoto, "photos")
clean(HotelPhoto, "photos")
clean(Pays, "drapeau")

print("DONE")
