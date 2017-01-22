#!/usr/bin/env bash
script_dir="${BASH_SOURCE%/*}/"
if [ "$#" -ne 1 ]; then
    echo "Please provide a tarfile location"
fi
if [ -f "$1" ]; then
    while true; do
        read -p "the file specified already exists. Would you like to overwrite it?" yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) echo "Exiting the program"; exit 4;;
            * ) echo "Please answer yes or no.";;
        esac
    done
fi
tar -cvf "$1" -C ${script_dir}/../ src/
