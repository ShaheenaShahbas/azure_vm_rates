# azure_vm_rates
This repo contains an automated script to fetch Azure virtual machine rates and store them in a PostgreSQL database.


**Technologies used:**
1.Python
2.Postgresql
3.Docker

This project has three files namely Dockerfile , vmrates.py , docker-compose.yml file .

1. Dockerfile:
The Dockerfile defines the environment for the project. It specifies the base image i.e. official Python runtime image (python:3.12.2-alpine) as the parent image. Alpine Linux is chosen for its lightweight nature, which helps keep the overall image size small .Then it sets up the necessary dependencies such as requests, psycopg2-binary, and schedule packages required to run the Python script and interact with the PostgreSQL database.

2. vmrates.py:

The vmrates.py script serves as the core functionality of the project.
 
Data Retrieval from Azure Pricing API:
 The script makes an initial HTTP request to the Azure Pricing API endpoint (https://prices.azure.com/api/retail/prices) to retrieve the first page of data. This page contains a subset of the total VM pricing information available.
 
Looping Through Pages: 
After retrieving the first page of data, the script enters a loop to handle pagination. It continues to make subsequent requests to fetch additional pages of data, as long as there are more pages available. This is achieved by checking for the presence of a "NextPageLink" attribute in the JSON response.

Data Processing:
 Once the data is retrieved from the API, the script processes the JSON response. It extracts relevant information such as currency code, pricing tiers, retail price, unit price, region, meter ID, product name, SKU ID, effective start date, service name, service ID, service family, unit of measure, type, whether it's the primary meter region, and ARM SKU name. This extracted data is then organized and prepared for storage.
 
Database Interaction:
 After processing the data, the script interacts with a PostgreSQL database to store the fetched VM rates. It establishes a connection to the database and inserts the extracted information into the appropriate tables.
 
Schedule and Automation:
 The script utilizes the schedule package to automate the data retrieval process. It schedules periodic execution of the data retrieval and storage tasks, ensuring that the VM rates are regularly updated in the database. This automation simplifies the maintenance of pricing data and keeps it current.

3. docker-compose.yml:
The docker-compose.yml file orchestrates the deployment of the project's services using Docker Compose. It defines two services: one for the PostgreSQL database and another for the application. The application service is built from the Dockerfile and runs the vmrates.py script within a Docker container. The PostgreSQL service provides the database backend for storing the fetched VM rates.

Execution :

1.Clone the Repository:

Open your terminal or command prompt.
Navigate to the directory where you want to clone the repository.
Use the git clone command followed by the repository URL to clone the repository to your local machine. 
cmd:
git clone https://github.com/ShaheenaShahbas/azure_vm_rates

Navigate to the Repository Directory:
Once the repository is cloned, navigate into the repository directory using the cd command.

Run the Docker Compose:
cmd:
docker-compose up

POINTS TO BE NOTED:
1.Adjust the time of the project schedule as per your need.
2.Make sure that Docker and the container is running at the time scheduled.

 
