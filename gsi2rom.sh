#!/bin/bash
convert_sparse() {
	converted_name=$(echo "$(echo $1 | cut -d'.' -f 1)_converted.img")
	echo "Converting $1 to sparse image..."
	output=$(img2simg $1 $converted_name 2>&1)
	if [[ $output == *"failed"* ]]; then
		#File is already sparse in nature
		echo "$1 is already sparse, using it as it is!"
		$(rm $converted_name > /dev/null)
		cp $1 $converted_name
	else
		echo "Done."
	fi
}

convert_dat() {
	argument_true=$(echo "$(echo $(echo "$(echo $1 | cut -d'.' -f 1)") | cut -d'_' -f 1)")
	echo "Generating dat files for $1..."
	output=$(img2sdat -o $argument_true -v 4 -p $argument_true $1)
	echo "Done."
}

compress_dat() {
	echo "Compressing $1.new.dat..."
	brotli -7 "$1/$1.new.dat" -o "$1/$1.new.dat.br"
	echo "Done."
}

argument_true=$(echo "$(echo $1 | cut -d'.' -f 1)")
	
convert_sparse "$(echo $argument_true).img"
convert_dat "$(echo $argument_true)_converted.img"
compress_dat "$argument_true"
