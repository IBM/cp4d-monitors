#!/bin/bash

echo "Starting Cloud Pak for Data Watson Studio Runtime usage monitor...."
echo "-------------------------------------------------------------"

dir=$(pwd)
for py_file in $(find ${dir} -maxdepth 1 -name "*.py")
do
    echo "Executing CP4D Monitor python file: ${py_file}"
    python ${py_file}
done

echo "-------------------------------------------------------------"
echo "Exiting Cloud Pak for Data Watson Studio Runtime usage monitor...."