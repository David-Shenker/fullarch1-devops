#!/bin/bash

usage() {
    echo "Usage: $0 -h <MONGO_URI> -u <MONGO_USER> -p <MONGO_PW> -b <S3_BUCKET> -o <DUMP_PATH>"
    exit 1
}

while getopts ":h:u:p:b:o:" opt; do
  case $opt in
    h) MONGO_URI="$OPTARG"
    ;;
    u) MONGO_USER="$OPTARG"
    ;;
    p) MONGO_PW="$OPTARG"
    ;;
    b) S3_BUCKET="$OPTARG"
    ;;
    o) DUMP_PATH="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
        usage
    ;;
    :) echo "Option -$OPTARG requires an argument." >&2
       usage
    ;;
  esac
done

if [ -z "$MONGO_URI" ] || [ -z "$MONGO_USER" ] || [ -z "$MONGO_PW" ] || [ -z "$S3_BUCKET" ] || [ -z "$DUMP_PATH" ]; then
    usage
fi

TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')

mongodump -h="$MONGO_URI" -u "$MONGO_USER" -p "$MONGO_PW" -o="$DUMP_PATH/mongodump_$TIMESTAMP"

tar -czvf "$DUMP_PATH/mongodump_$TIMESTAMP.tar.gz" -C "$DUMP_PATH/mongodump_$TIMESTAMP" .

aws s3 cp "$DUMP_PATH/mongodump_$TIMESTAMP.tar.gz" "s3://$S3_BUCKET/mongodump_$TIMESTAMP.tar.gz"

rm -rf "$DUMP_PATH/mongodump_$TIMESTAMP" "$DUMP_PATH/mongodump_$TIMESTAMP.tar.gz"
