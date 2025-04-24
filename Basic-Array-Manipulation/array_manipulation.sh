#! /usr/bin/bash

# parse table columns into 3 arrays
csv_file="./arrays_table.csv"
column_0=( $(cut -d "," -f 1 $csv_file) )
column_1=( $(cut -d "," -f 2 $csv_file) )
column_2=( $(cut -d "," -f 3 $csv_file) )

# Create a new array as the difference of columns 1 and 2
column_3=()
nlines=$(cat $csv_file | wc -l)
for ((i=1; i<$nlines; i++)); do
    column_3[$i]=$((column_2[$i]-column_1[$i]))
done

# first write the new array to file
# initialize the file with a header
echo "${column_3[0]}" > column_3.txt
for ((i=1; i<$nlines; i++)); do
    echo ${column_3[$i]} >> column_3.txt
done
paste -d "," $csv_file column_3.txt > report.csv

