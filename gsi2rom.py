from config import Config
import sys
import os
import subprocess

arguments = sys.argv
system=Config.system_img
vendor=Config.vendor_img
boot=Config.boot_img

# removing script name from arguments
for arg in arguments :
    if str(arg).endswith(".py") :
        arguments.remove(arg)
        break

# checking if the files exist
def check_files():
    print("Checking if files exist...")

    if os.path.isfile(system) is True:
        print("system.img file there.")
    else :
        print("system.img not found!")
        exit()

    if os.path.isfile(vendor) is True:
        print("vendor.img file there.")
    else :
        print("vendor.img not found!")
        exit()

    if os.path.isfile(boot) is True:
        print("boot.img file there.")
    else :
        print("boot.img not found!")
        exit()

def make_temp_directory():
    os.system("mkdir temp")

def make_sparse_img(path, type):
    print("Making sparse image for " + type)
    bin_location = str(os.getcwd() + "img2simg/img2simg"
    op = subprocess.check_output(bin_location + path + " temp/" + type + "_sparse.img", shell=True)
    if len(op) > 1 :
        print("Error occured in generating sparse image for " + type)
        exit()
    print("Done")

def make_dat_files(type):
    print("Generating dat files for " + type)
    # img2sdat -o temp/vendor_patched -v 4 temp/vendor_sparse.img
    bin_location = str(os.getcwd() + "img2sdat/img2sdat.py"
    op = subprocess.check_output(bin_location + " -o " + "temp/" + type + "_dat " + "-v 4 " + "temp/" + type + "_sparse.img", shell=True)
    
    op = str(op).lower()
    if "error" in op:
        print("Error in generating dat files for " + type)
        exit() 
    print("Done")


def rename_files(folder, original, to):
    files = os.listdir(folder)
    for f in files:
        if original in str(f) :
            newname = str(f).replace(original, to)
            os.system("cd " + folder + " && mv " + f + " " + newname)

def compress_file(type):
    print("Performing broli compression on " + type + " files...")
    op = subprocess.check_output("brotli -7 temp/" + type + "_dat/" + type + ".new.dat -o temp/" + type + "_dat/" + type + ".new.dat.br -v", shell=True)
    op = str(op).lower()
    if "fail" in op :
        print("Error in compressing " + type)
        exit()
    print("Done")

def delete_file(path):
    os.system("rm -r " + path)

def download_rom_base():
    subprocess.check_output("rm -rf rom_base", shell=True)
    op = subprocess.check_output("git clone " + Config.rom_base_git + " rom_base", shell=True)
    if "fatal" in str(op) :
        print("Unable to sync repo!")
        exit()
    else :
        print("Done")

def move_files_to_rom(type):
    print("Moving " + type + " files...")
    files = os.listdir("temp/" + type + "_dat")
    for f in files :
        os.system("mv temp/" + type + "_dat/" + f + " rom_base/")
    print("Done")

def generate_updater():
    print("Generating updater-script...")
    reader = open("rom_base/META-INF/com/google/android/updater-script", "r")
    writer = open("rom_base/META-INF/com/google/android/updater-script-temp", "w")
    for line in reader:
        line = line.replace("&&device&&", Config.device)
        line = line.replace("&&porter&&", Config.porter)
        line = line.replace("&&android_version&&", Config.android_version)
        line = line.replace("&&port&&", Config.port)
        line = line.replace("&&date&&", Config.date)
        line = line.replace("&&security&&", Config.security)
        writer.write(line)
    reader.close()
    writer.close()
    os.system("mv rom_base/META-INF/com/google/android/updater-script-temp rom_base/META-INF/com/google/android/updater-script")
    print("Done")

def create_rom_zip():
    files = os.listdir("rom_base/")
    for f in files:
        if f == "rom.zip" :
            files.remove(f)
        if f == ".git" :
            files.remove(f)
    print("Creating zip...")
    ff = ""
    for f in files :
        ff = ff + " " + f
    os.system("cd rom_base && zip -r rom.zip " + ff)

check_files()

os.system("rm -rf temp")
os.system("rm -rf rom_base")
make_temp_directory()

print("Generating sparse images...")
make_sparse_img(system, "system")
make_sparse_img(vendor, "vendor")

print("Generating dat files...")
make_dat_files("system")
make_dat_files("vendor")

rename_files("temp/vendor_dat", "system", "vendor")

print("Compressing files using Brotli...")
compress_file("system")
compress_file("vendor")

print("Removing unused files...")
delete_file("temp/system_sparse.img")
delete_file("temp/vendor_sparse.img")
delete_file("temp/system_dat/system.new.dat")
delete_file("temp/vendor_dat/vendor.new.dat")

print("Done")

print("Syncing rom zip base...")
download_rom_base()

print("Moving files to base...")
move_files_to_rom("system")
move_files_to_rom("vendor")
os.system("cp " + Config.boot_img + " rom_base/boot.img")

generate_updater()

create_rom_zip()
print("Rom zip made!")

file_name = str(input("Enter zip name for produced rom : "))
os.system("mv rom_base/rom.zip " + file_name + ".zip")

print("Cleaning up...")
os.system("rm -rf temp")
os.system("rm -rf rom_base")
