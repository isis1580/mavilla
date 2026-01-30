import csv
import os

# Chemin du CSV généré par le script de migration
CSV_FILE = "cloudinary_migration_report_complete.csv"

if not os.path.exists(CSV_FILE):
    print(f"❌ CSV non trouvé : {CSV_FILE}")
    exit()

migrated = 0
skipped = 0
errors = 0
total = 0

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += 1
        status = row["status"]
        if status == "MIGRATED":
            migrated += 1
        elif "SKIP" in status:
            skipped += 1
        else:
            errors += 1

print(f"📊 Résumé de la migration :")
print(f"   Total fichiers : {total}")
print(f"   Migrés sur Cloudinary : {migrated}")
print(f"   Ignorés (déjà Cloudinary ou pas de fichier) : {skipped}")
print(f"   Erreurs à vérifier : {errors}")

if errors > 0:
    print(f"⚠️ Il y a {errors} fichiers avec des erreurs. Vérifie le CSV pour les détails.")
else:
    print("✅ Tous les fichiers sont sur Cloudinary. Tu peux supprimer ton dossier media/ local si tu veux.")
