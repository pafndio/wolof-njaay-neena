# Compilation APK avec Google Colab
# Copier ce code dans un nouveau notebook sur https://colab.research.google.com/

# ============================================
# 📱 Wolof Njaay Neena - Compilation APK
# ============================================

print("🚀 Début de la compilation...")
print("⏱️  Durée estimée : 20-30 minutes")
print()

# Étape 1 : Installation des dépendances
print("📦 Installation des dépendances...")
!apt-get update -qq
!apt-get install -y -qq openjdk-17-jdk > /dev/null 2>&1
!pip install -q buildozer cython==0.29.36

print("✅ Dépendances installées")
print()

# Étape 2 : Uploader votre projet
print("📤 Uploadez votre dossier wolof-njaay-mobile")
print("   👉 Cliquez sur le dossier à gauche")
print("   👉 Cliquez sur 'Upload' et uploadez TOUS les fichiers")
print()
print("   OU clonez depuis GitHub :")
print("   !git clone https://votre-repo/wolof-njaay-mobile.git")
print()

# Attendre que l'utilisateur uploade
input("⏸️  Appuyez sur ENTREE une fois les fichiers uploadés...")

# Étape 3 : Compiler l'APK
print()
print("🔨 Compilation de l'APK...")
print("   (Cela peut prendre 20-30 minutes)")
print()

%cd wolof-njaay-mobile

# Accepter automatiquement les licences Android
import os
os.environ['ANDROID_HOME'] = '/root/.buildozer/android/platform/android-sdk'

!buildozer android debug

# Étape 4 : Télécharger l'APK
print()
print("📥 Téléchargement de l'APK...")

from google.colab import files
import glob

apk_files = glob.glob('bin/*.apk')

if apk_files:
    print(f"✅ APK trouvé : {apk_files[0]}")
    files.download(apk_files[0])
    print()
    print("🎉 Compilation terminée avec succès !")
    print("📱 Installez l'APK sur votre téléphone Android")
else:
    print("❌ Aucun APK trouvé.")
    print("   Vérifiez les erreurs ci-dessus")
    print()
    print("Fichiers dans bin/ :")
    !ls -la bin/
