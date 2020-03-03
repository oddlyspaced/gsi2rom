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

create_zip() {
	#create copy of base so that it won't conflict with original folder
	echo "Copy base folder to temp..."
	cp -r base temp
	echo "Done."
	sleep 1
	echo "Adding files to base..."
	for arg in "$@"
	do
		mv $arg/"$arg.new.dat.br" temp/
		mv $arg/"$arg.patch.dat" temp/
		mv $arg/"$arg.transfer.list" temp/
	done
	echo "Done"
	sleep 1
	echo "Creating zip..."
	echo "Enter zip name: "
	read name
	cd temp
	zip -r "$name.zip" *
	mv "$name.zip" ../
	cd ..
	echo "All done!"
	echo "$name.zip has been created."
}

cleanup() {
	echo "Cleaning up..."
	for arg in "$@"
	do
		rm -rf $arg
		rm -rf "($arg)"_converted.img
	done
	rm -rf temp/
	echo "Done."
}

argument_system=$(echo "$(echo $1 | cut -d'.' -f 1)")
argument_vendor=$(echo "$(echo $2 | cut -d'.' -f 1)")

convert_sparse "$(echo $argument_system).img"
convert_sparse "$(echo $argument_vendor).img"
convert_dat "$(echo $argument_system)_converted.img"
convert_dat "$(echo $argument_vendor)_converted.img"
compress_dat "$argument_system"
compress_dat "$argument_vendor"
create_zip $argument_system $argument_vendor
cleanup $argument_system $argument_vendor
