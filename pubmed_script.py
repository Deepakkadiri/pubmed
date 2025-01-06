import requests
import csv
import argparse
import logging
from typing import List, Dict

API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
API_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
API_KEY = "a8f796e116bdd7787e801a77fab766257a08"

def fetch_papers(query: str) -> List[Dict]:
    """Fetch paper IDs from PubMed API based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "api_key": API_KEY
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
    return fetch_paper_details(paper_ids)

def fetch_paper_details(paper_ids: List[str]) -> List[Dict]:
    """Fetch detailed information for a list of paper IDs."""
    if not paper_ids:
        return []
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json",
        "api_key": API_KEY
    }
    response = requests.get(API_SUMMARY_URL, params=params)
    response.raise_for_status()
    return parse_paper_details(response.json())

def parse_paper_details(data: Dict) -> List[Dict]:
    """Extract relevant details from PubMed API response."""
    papers = []
    for paper_id, details in data.get("result", {}).items():
        if paper_id == "uids":
            continue
        papers.append({
            "PubmedID": paper_id,
            "Title": details.get("title"),
            "PublicationDate": details.get("pubdate"),
            "Non-academicAuthor(s)": extract_non_academic_authors(details),
            "CompanyAffiliation(s)": extract_company_affiliations(details),
            "CorrespondingAuthorEmail": extract_corresponding_email(details),
        })
    return papers

def extract_non_academic_authors(details: Dict) -> List[str]:
    """Identify non-academic authors."""
    authors = details.get("authors", [])
    return [author.get("name") for author in authors if is_non_academic(author.get("affiliation", ""))]

def extract_company_affiliations(details: Dict) -> List[str]:
    """Extract pharmaceutical/biotech company affiliations."""
    affiliations = details.get("affiliation", "")
    return [aff for aff in affiliations.split(";") if is_pharma_company(aff)]

def extract_corresponding_email(details: Dict) -> str:
    """Extract the email of the corresponding author."""
    return details.get("correspondence", {}).get("email", "")

def is_non_academic(affiliation: str) -> bool:
    """Determine if an affiliation is non-academic."""
    academic_keywords = ["university", "institute", "lab"]
    return not any(keyword in affiliation.lower() for keyword in academic_keywords)

def is_pharma_company(affiliation: str) -> bool:
    """Check if an affiliation is a pharmaceutical or biotech company."""
    pharma_keywords = ["pharma", "biotech", "company"]
    return any(keyword in affiliation.lower() for keyword in pharma_keywords)

def save_to_csv(papers: List[Dict], filename: str):
    """Save paper details to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "PubmedID", "Title", "PublicationDate",
            "Non-academicAuthor(s)", "CompanyAffiliation(s)", "CorrespondingAuthorEmail"
        ])
        writer.writeheader()
        for paper in papers:
            writer.writerow({
                "PubmedID": paper.get("PubmedID", ""),
                "Title": paper.get("Title", ""),
                "PublicationDate": paper.get("PublicationDate", ""),
                "Non-academicAuthor(s)": ", ".join(paper.get("Non-academicAuthor(s)", [])),
                "CompanyAffiliation(s)": ", ".join(paper.get("CompanyAffiliation(s)", [])),
                "CorrespondingAuthorEmail": paper.get("CorrespondingAuthorEmail", ""),
            })

def print_papers(papers: List[Dict]):
    """Print paper details to the console."""
    for paper in papers:
        print(paper)

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers and save details as CSV.")
    parser.add_argument("query", help="Query to search PubMed papers.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information.")
    parser.add_argument("-f", "--file", help="Specify the filename to save results.")
    
    args = parser.parse_args()

    # Setup debug logging
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        logging.debug(f"Fetching papers for query: {args.query}")
        papers = fetch_papers(args.query)
        
        if args.file:
            save_to_csv(papers, args.file)
            logging.info(f"Data saved to {args.file}")
        else:
            print_papers(papers)
    except Exception as e:
        logging.error(f"Error occurred: {e}")

# Entry point
if __name__ == "__main__":
    main()
