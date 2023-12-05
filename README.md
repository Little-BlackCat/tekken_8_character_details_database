# Tekken 8 Character Details

## Overview
This project focuses on extracting character details from the Tekken 8 video game website using BeautifulSoup for web scraping. The extracted data is processed and structured into a DataFrame using the Pandas library. Additionally, the project leverages Apache Airflow within a Docker container to automate the daily data scraping process and subsequently utilizes Pandas to upload the processed data to a Supabase database.

## Project Components
1. Data Extraction (BeautifulSoup):
    
    The project utilizes BeautifulSoup, a Python library for web scraping, to extract character details from the Tekken 8 website.

2. Data Processing and DataFrame Creation (Pandas):

    After extracting the data, Pandas is employed to create a structured DataFrame, facilitating easy manipulation and analysis of the character details.

3. Automation with Airflow:

    Apache Airflow is employed for automating the data extraction process. The project is set up as a Directed Acyclic Graph (DAG) in Airflow, allowing the automatic execution of the data scraping task every day.

4. Database Upload (Supabase):

    Following data extraction and processing, Pandas is used to upload the prepared DataFrame to a Supabase database. This ensures that the character details are regularly updated in the database.
    
## Usage
1. Web Scraping:

    The web scraping task can be initiated manually or automatically using the Airflow DAG.

2. Airflow DAG:

    The Airflow DAG, defined in the dags folder, automates the data scraping process. It is configured to run daily and can be customized based on specific requirements.

3. Database Upload:

    The processed data, available as a Pandas DataFrame, is uploaded to the Supabase database using Pandas' to_sql functionality.
    
## Project Flow
![alt text](https://github.com/Little-BlackCat/tekken_8_character_details_database/blob/main/assets/Tekken_8_Character_Details.png "Tekken 8")

## Credit
Thank you for information about details of project: [Tekken 8](https://tekken.fandom.com/wiki/Tekken_8)
