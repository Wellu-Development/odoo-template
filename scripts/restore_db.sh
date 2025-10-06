#!/bin/sh

# -b db container
# -o odoo container
# -d db name
# -f zipfile

database_container=""
odoo_container=""
file_compress=""
database_name=""

while getopts :b:o:d:f: flag; do
    case "${flag}" in
    b) database_container=${OPTARG} ;;
    o) odoo_container=${OPTARG} ;;
    d) database_name=${OPTARG} ;;
    f) file_compress=${OPTARG} ;;
    :)
        echo "Error: -${OPTARG} requires an argument"
        exit_abnormal
        ;;
    *)
        exit_abnormal
        ;;
    esac
done

unzip_file() {
    echo "init uniziping... ${file_compress}"
    mkdir backup_tmp
    unzip ${file_compress} -d backup_tmp
    echo "finish unzip"
}

load_database() {
    echo "create and load db... ${database_name}"
    cd backup_tmp
    sudo docker exec -it ${database_container} psql -U odoo postgres -c 'DROP DATABASE IF EXISTS '${database_name}
    ''
    sudo docker exec -it ${database_container} psql -U odoo postgres -c 'CREATE DATABASE '${database_name}
    ''
    cat dump.sql | sudo docker exec -i ${database_container} psql -U odoo ${database_name}
    echo "created and charged db"
}

load_filestore() {
    echo "coping filestore (if exists)..."
    sudo docker exec -u odoo -i ${odoo_container} mkdir /var/lib/odoo/filestore
    sudo docker exec -u odoo -i ${odoo_container} mkdir /var/lib/odoo/filestore/${database_name}
    pwd
    sudo docker cp filestore/. ${odoo_container}:/var/lib/odoo/filestore/${database_name}
    echo "filestore copy successfully"
}

clear() {
    echo "cleaning backup..."
    cd ..
    rm -rf backup_tmp
    echo "clean backup sucessfully"
}

usage() {
    echo "usage: $0 [ -b DATABASE_CONTAINER ] [ -o ODOO_CONTAINER ] [ -f FILE_COMPRESS ] [ -d DATABASE_NAME ]" 1>&2
}

exit_abnormal() {
    usage
    exit 1
}

main() {
    unzip_file
    load_database
    load_filestore
    clear
}

main
