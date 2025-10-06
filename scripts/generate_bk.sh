#!/bin/sh

# -b db container
# -o odoo container
# -d db name
# -f valid filestore, 0 or 1 values

database_container=""
odoo_container=""
valid_filestore=""
database_name=""

while getopts :b:o:d:f: flag; do
    case "${flag}" in
    b) database_container=${OPTARG} ;;
    o) odoo_container=${OPTARG} ;;
    d) database_name=${OPTARG} ;;
    f) valid_filestore=${OPTARG} ;;
    :)
        echo "Error: -${OPTARG} requires an argument"
        exit_abnormal
        ;;
    *)
        exit_abnormal
        ;;
    esac
done

filename=${database_name}_$(date +"%d%m%Y")$(date +"%H%M").zip

generate_dump() {
    echo "generating dump.sql..."
    docker exec -it -u root ${database_container} pg_dump -U odoo -d ${database_name} >dump.sql
    echo "backup generated..."
}

copy_filestore() {
    echo "copying filestore..."
    docker cp ${odoo_container}:/var/lib/odoo/filestore ./filestore
    echo "filestore copied"
}

generate_compress_file() {
    echo "generating compress file..."

    generate_dump

    if [ "${valid_filestore}" == '1' ]; then
        copy_filestore
        zip ${filename} dump.sql filestore
    else
        zip ${filename} dump.sql
    fi

    echo "generated compress file..."
}

clear_dir() {
    rm -rf filestore
    rm -f dump.sql
    mv ./${filename} /var/lib/odoo/backups/${filename}
    echo "deleted files"
}

clear_old_file() {
    qty_files=$(find /var/lib/odoo/backups -maxdepth 1 -type f | wc -l)

    if [ $qty_files -eg 8 ]; then
        file_old=$(find /var/lib/odoo/backups -maxdepth 1 -type f -printf '%T@ %p\n' | sort -n | head -n 1 | cut -d' ' -f2-)
        rm /var/lib/odoo/backups/${file_old}
    fi
}

main() {
    generate_compress_file
    clear_dir
    clear_old_file
}

usage() {
    echo "usage: $0 [ -b DATABASE_CONTAINER ] [ -o ODOO_CONTAINER ] [ -f VALID_FILESTORE ] [ -d DATABASE_NAME ] [ -s BUCKET_PATH ]" 1>&2
}

exit_abnormal() {
    usage
    exit 1
}

main
