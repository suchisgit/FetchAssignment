# Health Check for Fetch APIs

This repository is designed for implementing a program that checks the health of a set of HTTP endpoints. It involves reading an input argument specifying a file path containing a list of HTTP endpoints in YAML format. The program tests the health of these endpoints every 15 seconds, tracking the availability percentage for each HTTP domain. After each 15-second test cycle, the cumulative availability percentage for each domain is logged to the console.

## Prerequisites
Ensure that latest python version is installed on the machine.<br />

## Set up
git clone https://github.com/suchisgit/FetchAssignment.git  <br />
cd FetchAssignment <br />
pip install -r requirements.txt <br />

## Execution command
python fetchHealthCheck.py input/configuration.yaml <br />
The second parameter in the command corresponds to the input file. <br />

## Demo
![](https://github.com/suchisgit/FetchAssignment/blob/main/gif/DemoFetch.gif)
