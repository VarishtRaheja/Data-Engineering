#! /usr/bin/bash

# Creating the headers of the columns and adding to the log file
header=$(echo -e "year\tmonth\tday\tobs_temp\tfc_temp")
echo $header > "./rx_poc.log"

# Obtaining the weather information of a particular station.
city=Casablanca
output_file=weather_report

# Fetching the data
weather_data=$(curl -s wttr.in/$city?T --output $output_file)
if [[ -f $output_file ]]; then
    echo "File $output_file has been successfully created."

else
    echo "File failed to create."
fi

# Filtering out required temperature data
obs_temp=$(cat "./weather_report" | grep -Eo "[0-9]+..C" | head -n 1)
# obs_temp=$(cat "./weather_report" | grep -m 1 '°.' | grep -Eo -e '-?[[:digit:]].*')
echo "The current Temperature of $city: $obs_temp"

# Extracting the temperature at noon today
fc_temp_today=($(cat "weather_report" | grep -m 2 '°.' | grep -Eo -e '-?[[:digit:]].*' | tail -n -1 | grep -Eo '[0-9]+..C'))
echo "The temperature at noon today is: ${fc_temp_today[@]:2:2}"

# Extracting the temperature at noon tomorrow
fc_temp=($(cat "weather_report" | grep -m 3 '°.' | grep -Eo -e '-?[[:digit:]].*' | tail -n -1 | grep -Eo '[0-9]+..C'))
echo "The temperature at noon tomorrow is: ${fc_temp[@]:2:2}"

#Store the corresponding shell variables in curr day, month, year
#Assign Country and City to variable TZ
curr_year=$(TZ='Morocco/Casablanca' date "+%Y")
curr_month=$(TZ='Morocco/Casablanca' date "+%m")
curr_day=$(TZ='Morocco/Casablanca' date "+%d")
echo "The current year is: $curr_year"
echo "The current month is: $curr_month"
echo "The current day is: $curr_day"

#Appending the result to the weather log file.
result=$(echo -e "$curr_year\t$curr_month\t$curr_day\t$obs_temp\t${fc_temp[@]:2:2}")
result_today=$(echo -e "$curr_year\t$curr_month\t$((curr_day-1))\t$obs_temp\t${fc_temp_today[@]:2:2}")
echo "$result_today" >> "./rx_poc.log"
echo "$result" >> "./rx_poc.log"


# Calculating the time difference in local time to time of the city used. 

# Get local time formatted
# Get local hour
local_hour=$(date "+%H")
local_minute=$(date "+%M")

# Get Casablanca hour
casablanca_hour=$(TZ="Africa/Casablanca" date "+%H")
casablanca_minute=$(TZ="Africa/Casablanca" date "+%M")

# Calculate the difference
hour_difference=$((local_hour - casablanca_hour))
minute_difference=$((local_minute - casablanca_minute))

echo "Time difference: $hour_difference hours and $minute_difference minutes" > "./time_difference.txt"

echo -e "year\tmonth\tday\tobs_temp\tfc_temp\taccuracy\taccuracy_range" > historical_fc_accuracy.tsv

