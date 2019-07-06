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
    op = subprocess.check_output("img2simg " + path + " temp/" + type + "_sparse.img", shell=True)
    if len(op) > 1 :
        print("Error occured in generating sparse image for " + type)
        exit()
    print("Done")

def make_dat_files(type):
    print("Generating dat files for " + type)
    # img2sdat -o temp/vendor_patched -v 4 temp/vendor_sparse.img
    op = subprocess.check_output("img2sdat -o " + "temp/" + type + "_dat " + "-v 4 " + "temp/" + type + "_sparse.img", shell=True)
    
    op = str(op).lower()
    if "error" in op:
        print("Error in generating dat files for " + type)
        exit() 
    print("Done")


def rename_files(folder, original, to):
    files = os.listdir(folder)
    for f in files:
        if original in str() :
            newname = str(f).replace(original, to)
            os.rename(folder + f, folder + newname)

def compress_file(type):
    print("Performing broli compression on " + type + " files...")
    op = subprocess.check_output("brotli -7 temp/" + type + "_dat/" + type + ".new.dat -o temp/" + type + "_dat/vendor.new.dat.br -v", shell=True)
    op = str(op).lower()
    if "fail" in op :
        print("Error in compressing " + type)
        exit()
    print("Done")


check_files()

make_temp_directory()

print("Generating sparse images...")
make_sparse_img(system, "system")
make_sparse_img(vendor, "vendor")

print("Generating dat files...")
make_dat_files("system")
make_dat_files("vendor")

rename_files("temp/vendor_dat", "system", "vendor")

compress_file("system")
compress_file("vendor")