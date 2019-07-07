# GSI2ROM
gsi2rom is a small python 3 script which can be used to generate a flashable rom out of any gsi, provided you have the system, vendor and boot image

## How to use
Edit the config.py so that the config points correctly to the system.img, vendor.img and boot.img files.
You can also make various changes regarding the build name etc, since the sample config is made to create Oxygen OS roms out of the ported gsi's.

After editing just run

``python gsi2rom.py``

## Dependencies
``git``

``img2simg``

``img2sdat``

``brotli``

