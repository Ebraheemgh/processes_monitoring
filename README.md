# Process Monitor & Summarizer

This Python script monitors the running processes on your machine over a specified duration and interval. It logs CPU and memory usage to a CSV file, then computes summary statistics and stores them in a MySQL database.

# How It Works
* Configuration: Loads settings (like monitoring interval and DB credentials) from a config.json file.
* Monitoring Loop:

    * Every monitoring_interval seconds (e.g., 5 seconds), it queries all running processes.

    *  For each process, it captures(PID ,Name ,CPU % ,Memory (MB) ,Timestamp)

* Appends this data to a CSV file.
* Inserts the summarized data into database .




# How I Used ChatGPT to Implement This Project
I used ChatGPT to help me design, debug, and implement the following:

* Process monitoring logic:

  * How to list all running processes in Python using psutil.
  * How to retrieve CPU and memory usage for specific processes.
  
* Pandas usage:
  * Converting Data to CSV file syntax code.
  * Grouping and aggregating the data by PID and process name.
  * Calculating average CPU % and memory usage.

* MySQL Integration:

  * Designing a DatabaseManager class with methods for connecting, executing, committing, and closing.
  * Writing code to insert summarized data from pandas into a MySQL table (bmc_assignment).
