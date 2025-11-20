[app]

# (str) Titre de votre application
title = Wolof Njaay Neena

# (str) Nom du package
package.name = wolofnjaay

# (str) Domaine du package (nécessaire pour l'identifiant unique de l'application)
package.domain = com.wolof

# (str) Script source à inclure (l'extension .py sera ajoutée automatiquement)
source.include_exts = py,png,jpg,kv,atlas,json,db

# (list) Modèles de source à exclure
source.exclude_exts = spec

# (list) Répertoires à exclure
source.exclude_dirs = tests, bin, venv, __pycache__

# (list) Répertoires de source de l'application
source.dir = .

# (str) Version de l'application
version = 1.0.0

# (list) Exigences de l'application
requirements = python3,kivy==2.3.0,sqlite3,pyjnius,android

# (bool) Indique si l'application sera affiché en plein écran ou non
fullscreen = 0

# (string) Orientation de l'application (landscape, portrait ou all)
orientation = portrait

# (list) Permissions Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Code de version du Target Android API
android.api = 33

# (int) Code de version minimum du SDK Android
android.minapi = 21

# (str) SDK Android à utiliser
android.sdk = 33

# (str) NDK Android à utiliser
android.ndk = 25b

# (bool) Utiliser --private data storage (True) ou --dir public storage (False)
android.private_storage = True

# (bool) Si True, alors passer automatiquement à l'utilisation de la dernière version du SDK/NDK
android.skip_update = False

# (bool) Si True, alors accepter automatiquement les licences du SDK
android.accept_sdk_license = True

# (str) L'architecture Android à construire par défaut
android.archs = arm64-v8a, armeabi-v7a

# (bool) Activer AndroidX support
android.enable_androidx = True

# (str) Le format du nom du package Android
android.release_artifact = apk

# (str) Les icônes de votre application
#icon.filename = %(source.dir)s/assets/images/icon.png

# (str) Les images splash de votre application
#presplash.filename = %(source.dir)s/assets/images/presplash.png

# (str) Chemin d'accès au fichier de style de votre application
#android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Gradle dependencies à ajouter
#android.gradle_dependencies = 

# (list) Ajouter Java compile options
#android.add_compile_options = 

# (list) Ajout de Java build options
#android.add_build_options = 

# (str) python-for-android git branch ou tag à utiliser
#p4a.branch = master

# (str) URL du fork python-for-android
#p4a.fork = 

# (str) python-for-android specific extra args
#p4a.local_recipes = 

# (str) Nom du hook bootstrap à utiliser
#p4a.bootstrap = sdl2

[buildozer]

# (int) Niveau de log (0 = error uniquement, 1 = info, 2 = debug (avec tous les logs))
log_level = 2

# (int) Afficher les avertissements si buildozer est exécuté en tant que root (0 = False, 1 = True)
warn_on_root = 1

# (str) Chemin vers build artifact storage, %n = nom de l'app
#build_dir = ./.buildozer

# (str) Chemin vers build output (APK, AAB), %n = nom de l'app
#bin_dir = ./bin
