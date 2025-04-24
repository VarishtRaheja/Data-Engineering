# Scenario
**Introduction:**
1. The task is to create an automated Extract, Transform, Load (ETL) process to extract daily weather forecast and observed weather data and load it into a live report to be used for further analysis.
2. As part of a report save the temperature date including the day, month and year to a log file.
3. As a proof-of-concept (POC), a single station will be used.
4. We are also giving it a custom defined "rating" of various paramters based on the difference between the temps. YOu can custom select the row which you wish to see the rating of. However, since only yesterday and today as "days" are being used the choices are limited.

At a later stage, we can extend the report to include lists of locations, different forecasting sources, different update frequencies, and other weather metrics such as wind speed and direction, precipitation, and visibility.

---

## Data source
For this practice project, you'll use the weather data package provided by the open source project [wttr.in](https://wttr.in/), a web service that provides weather forecast information in a simple and text-based format.

---

### If you wish to rerun it from scratch please, delete the following files:
- weather_report
- time_difference.txt 
- rx_poc.log 
- historical_fc_accuracy.tsv
- And run the rx_posh.sh then, fc_accuracy.sh file.
