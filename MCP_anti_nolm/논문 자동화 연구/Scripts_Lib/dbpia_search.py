import argparse
import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import csv
import json
import os
from datetime import datetime
from urllib.parse import urlencode
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_URL = "https://api.dbpia.co.kr/v2/search/search.xml"

# Retry logic: Retry on aiohttp client errors or unexpected issues up to 3 times, with exponential backoff.
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(aiohttp.ClientError))
async def fetch_dbpia_async(session, api_key, query, args):
    """Fetch DBpia results asynchronously with retry mechanism for API stability."""
    params = {
        'key': api_key,
        'target': args.target,
        'searchall': query,
        'pagecount': args.limit,
        'pagenumber': args.page
    }
    
    # Advanced Filtering Options
    if args.sort: params['sorttype'] = args.sort
    if args.author: params['searchauthor'] = args.author
    if args.publisher: params['searchpublisher'] = args.publisher
    if args.freeyn: params['freeyn'] = args.freeyn
        
    if args.start_year and args.end_year:
        params['pyear'] = '2'
        params['pyear_start'] = args.start_year
        params['pyear_end'] = args.end_year

    req_url = f"{API_URL}?{urlencode(params)}"
    
    async with session.get(req_url) as response:
        response.raise_for_status()
        content = await response.read()
        return parse_xml_response(content, query)

def parse_xml_response(xml_content, query):
    results = []
    try:
        root = ET.fromstring(xml_content)
        
        error = root.find('.//error')
        if error is not None:
            message = error.findtext('message')
            print(f"[{query}] DBpia API Error: {message}")
            return results

        for item in root.findall('.//item'):
            title = item.findtext('title') or ""
            link_url = item.findtext('link_url') or ""
            
            authors = []
            authors_node = item.find('authors')
            if authors_node is not None:
                for author in authors_node.findall('author'):
                    name = author.findtext('name')
                    if name:
                        authors.append(name)
            
            publisher_node = item.find('publisher')
            publisher = publisher_node.findtext('name') if publisher_node is not None else ""
                
            publication_node = item.find('publication')
            publication = publication_node.findtext('name') if publication_node is not None else ""
                
            issue_node = item.find('issue')
            issue_yymm = issue_node.findtext('yymm') if issue_node is not None else ""
                
            results.append({
                'query': query,
                'title': title,
                'authors': ", ".join(authors),
                'publisher': publisher,
                'publication': publication,
                'issue_yymm': issue_yymm,
                'link_url': link_url
            })
            
        return results
    except ET.ParseError as e:
        print(f"[{query}] XML Parse Error: {e}")
        return results

async def search_all_async(api_key, queries, args):
    """Run concurrent asynchronous requests for all queries."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_dbpia_async(session, api_key, q, args) for q in queries]
        # execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_items = []
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                print(f"[{queries[i]}] Failed after retries: {res}")
            elif res:
                all_items.extend(res)
                print(f"  -> Found {len(res)} valid items for '{queries[i]}'")
            else:
                print(f"  -> No items found for '{queries[i]}'")
                
        return all_items

def deduplicate_results(items):
    """Remove exact duplicated research papers based on the link_url."""
    seen_urls = set()
    unique_items = []
    for item in items:
        url = item['link_url']
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_items.append(item)
    return unique_items

def save_results(items, out_format, output_file=None):
    if not items:
        print("\nNo valid results to save.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if not output_file:
        output_file = f"dbpia_results_{timestamp}.{out_format}"

    if out_format == 'csv':
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['query', 'title', 'authors', 'publisher', 'publication', 'issue_yymm', 'link_url'])
            writer.writeheader()
            writer.writerows(items)
            
    elif out_format == 'json':
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
            
    elif out_format == 'md':
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# DBpia 검색 주요 참고문헌 목록\n\n")
            f.write("| 검색어 | 논문 제목 | 저자 | 발행기관 (간행물) | 발행연월 | 링크 |\n")
            f.write("| --- | --- | --- | --- | --- | --- |\n")
            for item in items:
                title_clean = item['title'].replace('|', ' ')
                f.write(f"| {item['query']} | **{title_clean}** | {item['authors']} | {item['publisher']} ({item['publication']}) | {item['issue_yymm']} | [Link]({item['link_url']}) |\n")
                
    print(f"\nSuccessfully saved {len(items)} unique results to '{os.path.abspath(output_file)}'")

def main():
    parser = argparse.ArgumentParser(description="DBpia Open API Reference Search Tool (Advanced Async Version)")
    parser.add_argument('--key', type=str, help="DBpia API Access Key (Defaults to DBPIA_API_KEY env variable)")
    parser.add_argument('--query', type=str, help="Single keyword to search")
    parser.add_argument('--file', type=str, help="Text file containing list of queries (one keyword per line)")
    
    # Generic Filters
    parser.add_argument('--limit', type=int, default=10, help="Number of results per query")
    parser.add_argument('--page', type=int, default=1, help="Page number to fetch")
    parser.add_argument('--sort', type=str, choices=['1', '2', '3'], help="Sort type (1:Relevance, 2:Date Desc, 3:Date Asc)")
    parser.add_argument('--start_year', type=str, help="Start year (YYYY)")
    parser.add_argument('--end_year', type=str, help="End year (YYYY)")
    
    # Advanced Filters (New)
    parser.add_argument('--target', type=str, default='se', choices=['se', 'se_adv'], help="Search target (se: basic, se_adv: advanced)")
    parser.add_argument('--author', type=str, help="Filter by specific Author name")
    parser.add_argument('--publisher', type=str, help="Filter by Publisher name")
    parser.add_argument('--freeyn', type=str, choices=['Y', 'N'], help="Filter to show only free papers (Y/N)")
    
    # Output Control
    parser.add_argument('--format', type=str, default='csv', choices=['csv', 'json', 'md'], help="Output file format (csv, json, md)")
    parser.add_argument('--output', type=str, help="Output file path (Auto-generated if omitted)")
    
    args = parser.parse_args()
    
    api_key = args.key or os.environ.get("DBPIA_API_KEY")
    if not api_key:
        print("Error: API key is missing. Provide it via --key argument or .env file.")
        return

    queries = []
    if args.query:
        queries.append(args.query)
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            queries.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
            
    if not queries:
        print("Error: Provide at least one query using --query or --file")
        return
        
    print(f"Starting ASYNC DBpia search for {len(queries)} queries...")
    
    # Run Async Event Loop
    all_items_raw = asyncio.run(search_all_async(api_key, queries, args))
    
    # Deduplicate based on link
    unique_items = deduplicate_results(all_items_raw)
    
    if len(all_items_raw) > len(unique_items):
        print(f"\nRemoved {len(all_items_raw) - len(unique_items)} duplicated papers.")
        
    # Save Output
    save_results(unique_items, args.format, args.output)

if __name__ == "__main__":
    main()
