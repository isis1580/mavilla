import os
import django
import cloudinary.uploader
from django.conf import settings

# 1️⃣ Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "villana.settings")
django.setup()

# 2️⃣ Import des modèles après setup
from maison.models import Photo, Video, Publicite, ParcellePhoto, HotelPhoto, Pays

# 3️⃣ Fonction pour trouver tous les fichiers locaux d'un dossier
def scan_local_files(subfolder):
    folder_path = os.path.join(settings.BASE_DIR, "media", subfolder)
    if not os.path.exists(folder_path):
        return []
    files = []
    for root, _, filenames in os.walk(folder_path):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files

# 4️⃣ Migration automatique depuis media/ vers Cloudinary
def migrate_model_auto(model, field_name, cloud_folder, local_subfolder):
    migrated_count = 0
    error_count = 0

    files = scan_local_files(local_subfolder)
    if not files:
        print(f"[INFO] Aucun fichier trouvé pour {model.__name__} dans media/{local_subfolder}")
        return 0, 0

    for obj, local_file in zip(model.objects.all(), files):
        try:
            result = cloudinary.uploader.upload(
                local_file,
                folder=f"villana/{cloud_folder}",
                resource_type='auto'
            )
            setattr(obj, field_name, result["secure_url"])
            obj.save()
            print(f"[OK] {model.__name__} id={obj.id} → {result['secure_url']}")
            migrated_count += 1
        except Exception as e:
            print(f"[ERROR] {model.__name__} id={obj.id} : {e}")
            error_count += 1

    print(f"\n✅ {model.__name__} : {migrated_count} migrés, {error_count} erreurs.\n")
    return migrated_count, error_count

# 5️⃣ Map des modèles → Cloudinary et dossier local
migration_map = [
    (Photo, "photos", "photos"),
    (Video, "video", "videos"),
    (Publicite, "photos", "publicites"),
    (ParcellePhoto, "photos", "parcelle"),
    (HotelPhoto, "photos", "hotel"),
    (Pays, "drapeau", "drapeaux"),
]

# 6️⃣ Lancer migration
total_errors = 0
for model, field_name, folder in migration_map:
    _, errors = migrate_model_auto(model, field_name, folder, folder)
    total_errors += errors

if total_errors > 0:
    print(f"❌ Migration terminée avec {total_errors} fichiers échoués.")
else:
    print("🎉 Migration complète réussie ! Tous les fichiers sont sur Cloudinary.")
