# Author(s): Michael Koeppl

import sys
import platform
import piexif 
import glob
import os

MANUFACTURER_KEY = "Make"
_IS_MAC = platform.system() == 'Darwin'

def resource_path(relative_path):  # needed for bundling
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if not _IS_MAC:
        return relative_path
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def main():
    base_dir_path = input("Enter the path: ")
    base_dir_path = resource_path(base_dir_path.strip() + "/*")
    print(base_dir_path)

    files = glob.glob(base_dir_path)
    for name in files:
        # We only look for JPGs and PNGs
        if not name.lower().endswith(".jpg") and not name.lower().endswith(".png"):
            continue
        # Ignore directories
        if os.path.isdir(name):
            continue

        f = open(name)
        
        exif_dict = piexif.load(name)
        for ifd in ("0th", "Exif", "GPS", "1st"):
            for tag in exif_dict[ifd]:
                if (piexif.TAGS[ifd][tag]["name"] is MANUFACTURER_KEY):
                    manufacturer_name = exif_dict[ifd][tag].decode("utf-8")
                    dir_name = manufacturer_name.split(" ")[0]
                    dir_path = os.path.join(base_dir_path.replace("/*", ""), dir_name)
                    file_name = f.name[f.name.rfind('/') + 1:]
                    target_path = os.path.join(dir_path, file_name)
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                    print(f.name + " moved to " + target_path)
                    os.rename(name, target_path)
        f.close()
        print()
            

if __name__ == "__main__":
    main()
