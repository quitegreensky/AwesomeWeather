[app]

# (str) Title of your application
title = AKWeather
# (str) Package name
package.name = weather

# (str) Package domain (needed for android/ios packaging)
package.domain = com.awesome

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,json,otf,md,yaml

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = bin , __pycache__ ,env

source.exclude_patterns = buildozer.spec 

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements =  sdl2_ttf==2.0.15,kivy==2.0.0rc4 ,https://github.com/kivymd/KivyMD/archive/ed0fecd.zip, kivymd_extensions.akivymd==1.2.5, requests,chardet,idna,,urllib3,certifi

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/assets/splash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/assets/logo.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

author = quitegreensky

fullscreen = 0

#android.presplash_color = #FFFFFF

android.permissions = INTERNET

android.api = 28

#android.minapi = 21

#android.sdk = 20

android.ndk = 19b

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin
