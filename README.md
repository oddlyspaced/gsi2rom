# GSI2ROM
gsi2rom is a small bash script to generate flashable roms from system and vendor images.

## Requirements
system.img
vendor.img
base rom folder containing things like boot.img, dtbo.img Meta-Inf etc.

```Functioning Linux Environment```
```img2simg```
```img2sdat```
```brotli```
```zip```
## Usage
Copy the system.img, vendor.img and the base folder along with the script to a location.
Make sure that everything is correspondingly named, like system image is system.img, vendor image is vendor.img and base rom is named base

After all that has been taken care of just run
```./gsi2rom.sh system.img vendor.img``` 
