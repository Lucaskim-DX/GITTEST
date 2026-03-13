import os
import requests
import xml.etree.ElementTree as ET

# DBpia Open API 정보
DBPIA_API_URL = "http://api.dbpia.co.kr/v2/search/search.xml"

# 대상 파일에서 추출한 타겟 키워드 리스트
TARGET_KEYWORDS = [
    "클레오파트라 화장",
    "고대 이집트 피부",
    "당나귀 우유 피부 재생",
    "유산 피부 각질",
    "사해 소금 미네랄 효능",
    "피마자 오일 보습",
    "콜 화장 안구 면역"
]

def search_dbpia(api_key: str, keyword: str, max_count: int = 3) -> list:
    """DBpia API를 호출하여 검색 결과를 반환합니다."""
    params = {
        'key': api_key,
        'target': 'se', # se: 검색 (논문 검색 등)
        'searchall': keyword,
        'maxcount': max_count
    }
    
    try:
        response = requests.get(DBPIA_API_URL, params=params)
        response.raise_for_status()
        return parse_dbpia_xml(response.text)
    except requests.exceptions.RequestException as e:
        print(f"[오류] API 호출 실패 (키워드: {keyword}): {e}")
        return []

def parse_dbpia_xml(xml_data: str) -> list:
    """DBpia XML 응답을 파싱하여 논문 메타데이터 리스트를 반환합니다."""
    references = []
    try:
        root = ET.fromstring(xml_data)
        # item 태그 안에 검색 결과가 포함됨 (DBpia XML 구조에 따라 다를 수 있음)
        # API 가이드 구조를 바탕으로 파싱 (item 내에 title, authors, publisher, journal 등)
        for item in root.findall('.//item'):
            title = item.findtext('title', default='제목 없음').strip()
            # 저자 정보는 authors 아래에 여러 명일 수 있음
            authors_element = item.find('authors')
            authors = "저자 미상"
            if authors_element is not None:
                author_names = [author.findtext('name', '') for author in authors_element.findall('author')]
                valid_authors = [name for name in author_names if name]
                if valid_authors:
                    authors = ", ".join(valid_authors)
            
            publisher = item.findtext('publisher', default='')
            journal = item.findtext('journal', default='')
            issue_ym = item.findtext('issue_ym', default='')
            
            # 년도 추출 (YYYYMM 형태 등에서 YYYY만)
            year = "발간년도 미상"
            if issue_ym and len(issue_ym) >= 4:
                year = issue_ym[:4]
                
            link_url = item.findtext('link_url', default='')
            
            references.append({
                'title': title,
                'authors': authors,
                'publisher': publisher,
                'journal': journal,
                'year': year,
                'url': link_url
            })
    except ET.ParseError as e:
        print(f"[오류] XML 파싱 실패: {e}")
        
    return references

def format_as_markdown(references: list, keyword: str) -> str:
    """논문 정보를 마크다운 형식의 텍스트로 변환합니다."""
    if not references:
        return f"### 키워드: `{keyword}`\n* 검색 결과가 없습니다.\n\n"
        
    md_text = f"### 키워드: `{keyword}`\n"
    for ref in references:
        # APA 스타일 변형: 저자. (년도). 논문제목. 학술/발행기관명. URL
        journal_info = f"{ref['publisher']} {ref['journal']}".strip()
        if journal_info:
            journal_info = f" *{journal_info}*."
        md_text += f"- {ref['authors']}. ({ref['year']}). {ref['title']}.{journal_info} [링크]({ref['url']})\n"
    return md_text + "\n"

def main():
    api_key = os.environ.get("DBPIA_API_KEY")
    if not api_key:
        api_key = input("DBpia API Key를 입력하세요: ").strip()
        
    if not api_key:
        print("[에러] API Key가 제공되지 않았습니다.")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "10_DBpia_참고문헌리스트.md")
    
    print("DBpia 논문 검색을 시작합니다...")
    all_markdown_content = "# 과제 참고문헌 검색 결과 (DBpia)\n\n"
    all_markdown_content += "> 본 문서는 Open API를 통해 자동 수집된 참고문헌 목록입니다.\n\n"
    
    for keyword in TARGET_KEYWORDS:
        print(f"검색 중: '{keyword}'...")
        refs = search_dbpia(api_key, keyword, max_count=5)
        all_markdown_content += format_as_markdown(refs, keyword)
        
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_markdown_content)
        
    print(f"\n검색이 완료되었습니다. 결과가 '{output_file}'에 저장되었습니다.")

if __name__ == "__main__":
    main()
