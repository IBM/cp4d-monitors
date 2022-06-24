#!/bin/bash

echo "Starting with the custom monitor...."
dir=$(pwd)
for py_file in $(find ${dir} -name "*.py")
do
    echo "Executing CP4D Monitor python file: ${py_file}"
    python ${py_file}
done

echo "Exiting custom monitor...."