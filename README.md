# Disease-Symptom Network Project

## Overview

This project scrapes the MayoClinic website to extract symptoms for each disease. It utilizes the DOID and Symptom ontologies to map each disease to a Disease Ontology (DOID) term and each symptom to a Symptom Ontology term. Additionally, it extracts each symptom for each DOID term by searching for the 'has_symptom' keyword in the DOID ontology and maps each symptom to its respective term in the Symptom Ontology. The program integrates all symptoms and diseases, outputting a CSV file containing two types of information: either 'DOID term, DOID ID, symptom term, symptom ID' or 'DOID term, DOID ID, is-a, DOID ID

## Project Structure

- **`datamining/`**:Code and files for mapping diseases and symptoms to ontology terms.
- **`mayoclinic/`**:  The Scrapy spider for data extraction.

## Setup

1. **Clone the repository:**
    ```bash
    git clone git@github.com:samanehsalehi/Mayo-Clinic-Crawler.git
    cd Mayo-Clinic-Crawler
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Scrape data and generate mappings:**
    ```bash
   cd mayoclinic
   scrapy  crawl --loglevel INFO -O output.json:json mayoclinic --> To run the program
    ```

4. **Generate Disease-Symptom output file:**
    ```bash
    cd datamining
    python main.py
    ```

## Output

- **CSV File:**
  - The program generates a CSV file containing a row of "DOID term, DOID ID, symptom term, symptom ID", or a row of "DOID term, is-a,DOID ID".

## Contact

- Samaneh Salehi Nasab
- Email: samaneh.s@aol.com

Feel free to reach out for any questions or feedback!

