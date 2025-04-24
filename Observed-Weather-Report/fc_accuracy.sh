#! /usr/bin/bash
# Get the oberved temp
yesterday_fc=$(cat "./rx_poc.log" | tail -n 1 | awk -F'\t' '{print $NF}' | cut -d " " -f1)
# echo "The temperature yesterday is: $yesterday_fc"

#Calculate forecast accuracy
today_temp=$(tail -1 rx_poc.log | awk -F'\t' '{print $(NF-1)}' | cut -d " " -f1)
accuracy=$(($yesterday_fc-$today_temp))


if [[ $accuracy -le 1 ]]; then
    accuracy_label='Excellent'

elif [[ $accuracy -gt 1 && $accuracy -lt 2 ]]; then
    accuracy_label='Good'

elif [[ $accuracy -gt 2 && $accuracy -lt 3 ]]; then
    accuracy_label='Fair'

elif [[ $accuracy -gt 3 && $accuracy -lt 4 ]]; then
    accuracy_label='Poor'

else
    accuracy_label='Incorrect/Incomplete Data'
fi

echo "Forecast accuracy is: $accuracy with a rating of $accuracy_label"

#Appending the record to the tsv file. User input to see the particular row. Remember "-1" measn the last row.
row=$(tail $1 "./rx_poc.log")
year=$(echo "$row" | awk -F'\t' '{print $1}')
month=$(echo "$row" | awk -F'\t' '{print $2}')
day=$(echo "$row" | awk -F'\t' '{print $3}')
ob_temp=$(echo "$row" | awk -F'\t' '{print $(NF-1)}')
fc_temp=$(echo "$row" | awk -F'\t' '{print $NF}')

echo -e "$year\t$month\t$day\t$ob_temp\t$fc_temp\t$accuracy\t$accuracy_label" >> "./historical_fc_accuracy.tsv"
