#!/bin/bash

PYTHON_EXE=python3.exe
SWAG2DOC=../src/swagger2doc.py


function add_to_doc {
    $PYTHON_EXE $SWAG2DOC $*
    #compare_file $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT $REF_DIR/$TEST_CASE/$TEST_CASE$EXT
}

#SCHEMA_DIR="/schemas"
IN_DIR=$1
OUTPUT_DIR=$2
# swagger2doc extra arguments are $3
echo " HELLO derive_folder.sh"
echo "================="
echo "IN_DIR=$1"
echo "OUTPUT_DIR=$2"
echo "eco system: $3"
echo "input word file: $4"
echo "================="


mkdir -p $OUTPUT_DIR

outfile="outfile.txt"
echo "" > $OUTPUT_DIR/$outfile
cp ../input/ResourceTemplate.docx $OUTPUT_DIR/$outfile.docx

for file in $IN_DIR/*.json
do
    if [[ -f $file ]]; then
        echo ""
        echo "======================"
        echo "processing file: $file"
        filename="${file##*/}"
        basename="${filename%.*}"
        
        echo " running swagger2doc on $file "
        add_to_doc -docx $OUTPUT_DIR/$outfile.docx -swagger $file -derived $3 -word_out $OUTPUT_DIR/temp.docx 
        cp $OUTPUT_DIR/temp.docx $OUTPUT_DIR/$outfile.docx

    fi
done

read -p "Press any key to continue"