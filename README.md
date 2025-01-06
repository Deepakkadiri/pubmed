
# PubMed Paper Fetcher

This Python script fetches PubMed paper details based on a given query and extracts specific information such as paper title, publication date, non-academic authors, company affiliations, and corresponding author emails. The results are saved to a CSV file or printed to the console.

## Features

- Fetches PubMed paper details via the NCBI E-utilities API.
- Extracts specific information: paper title, publication date, non-academic authors, company affiliations, and corresponding author emails.
- Saves the extracted information in a CSV file.
- Supports debugging mode to log detailed information.
- Flexible search functionality by query.

## Requirements

- Python 3.x
- `requests` library

You can install the required libraries using `pip`:

```bash
pip install requests
```

## How to Use

1. **Fetch Papers by Query and Save to CSV**:
   
   Run the script by providing a search query and an optional output filename:

   ```bash
   python pubmed_fetcher.py "cancer research" -f output.csv
   ```

   This command will fetch papers related to "cancer research" and save the results in `output.csv`.

2. **Fetch Papers by Query and Print to Console**:

   If you don’t specify the `-f` argument, the results will be printed to the console:

   ```bash
   python pubmed_fetcher.py "machine learning in medicine"
   ```

3. **Enable Debugging Mode**:

   You can enable debugging mode to log detailed information by adding the `-d` flag:

   ```bash
   python pubmed_fetcher.py "artificial intelligence" -d
   ```

   This will display debug logs to help with troubleshooting or understanding the script's flow.

## Arguments

- `query`: The search query for PubMed papers (e.g., "cancer research").
- `-d, --debug`: Enable debug mode to print detailed logs.
- `-f, --file`: Specify the filename to save the results as a CSV file.

## Example

# pubmed
# To search for papers on "cancer treatment" and print the results to the console:
# python pubmed_script.py "cancer treatment"

# To search for papers on "cancer treatment" and save the results to a file named results.csv:
# python pubmed_script.py "cancer treatment" -f results.csv

# To search for papers on "cancer treatment" with debug information:
# python pubmed_script.py "cancer treatment" -d


# To search for papers on "cancer treatment", save results to results.csv, and print debug information:
# python pubmed_script.py "cancer treatment" -d -f results.csv



### Command:
```bash
python pubmed_fetcher.py "COVID-19 vaccine" -f covid_vaccine_papers.csv
```

### Output (saved as `covid_vaccine_papers.csv`):

```csv
PubmedID,Title,PublicationDate,Non-academicAuthor(s),CompanyAffiliation(s),CorrespondingAuthorEmail
12345678,"Impact of COVID-19 vaccine on immunity",2021,"John Doe","BioPharma Inc.","johndoe@biopharma.com"
23456789,"Clinical trial results for COVID-19 vaccine",2020,"Jane Smith","MedTech Labs","janesmith@medtech.com"
```

## Functions

- **fetch_papers(query)**: Fetch paper IDs based on a query from PubMed.
- **fetch_paper_details(paper_ids)**: Fetch detailed information for a list of paper IDs.
- **parse_paper_details(data)**: Parse and extract relevant details from the PubMed API response.
- **extract_non_academic_authors(details)**: Identify non-academic authors from paper details.
- **extract_company_affiliations(details)**: Extract pharmaceutical/biotech company affiliations.
- **extract_corresponding_email(details)**: Extract the email of the corresponding author.
- **save_to_csv(papers, filename)**: Save the extracted paper details to a CSV file.
- **print_papers(papers)**: Print the paper details to the console.

## Logging

The script uses the `logging` module to log debug or error messages. You can control the logging level with the `-d` (debug) flag.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
