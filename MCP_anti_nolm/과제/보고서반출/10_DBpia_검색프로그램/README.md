# DBpia Open API 데이터 검색 프로그램 매뉴얼

본 매뉴얼은 `dbpia_search.py` 스크립트를 사용하여 DBpia Open API에서 논문 및 학술 자료를 검색하고, 그 결과를 CSV 파일로 추출하는 방법을 안내합니다.

## 1. 사전 준비 (API 인증키 발급)

DBpia Open API를 사용하려면 개인 인증키(`API_KEY`)가 반드시 필요합니다.
- **발급처:** 누리미디어 DBpia Open API 키 등록/관리 페이지 (관련 고객센터 문의 필요)
- 발급받은 문자열(예: `36f4a4...`)을 API 호출 시 사용해야 합니다.

## 2. 필수 라이브러리 설치

스크립트 구동에 필요한 파이썬 라이브러리(`requests`, `python-dotenv`)를 설치합니다.
터미널(명령 프롬프트)에서 아래 명령어를 실행하세요.

```bash
pip install -r requirements.txt
```

## 3. 프로그램 사용 방법 (실행 방식)

본 스크립트는 다양한 환경에서 범용적으로 사용할 수 있도록 CLI(Command Line Interface) 파라미터를 지원합니다.

### 3.1. API 키 기본 설정 (.env 파일 활용)
매번 명령어에 `--key` 옵션을 입력하기 번거롭다면, 폴더 내에 `.env` 파일을 만들어 아래와 같이 설정해 두면 스크립트가 환경변수를 자동으로 읽어옵니다.
```text
# .env 파일 생성 후 아래 내용 입력
DBPIA_API_KEY=본인의발급받은API키값_입력
```

### 3.2. 단일 키워드 즉석 검색
터미널에서 보고 싶은 단일 검색어를 `--query` 옵션으로 전달하여 즉시 검색합니다.

```bash
# 기본 검색 (키를 명령어로 입력, 10건 검색)
python dbpia_search.py --key 36f4a421cd563b72bc361cbf6ccdd554 --query "이집트 화장품"

# 환경 변수(.env)에 키가 설정되어 있을 때 (단어 띄어쓰기는 따옴표로 묶음)
python dbpia_search.py --query "kpop 아이돌"
```

### 3.3. 다중 키워드 일괄 검색
`search_queries.txt`와 같이 텍스트 파일에 검색할 키워드를 줄바꿈 단위로 입력해놓고, 이를 몽땅 한 번에 검색하여 하나의 결과 파일로 합칩니다.

```bash
# search_queries.txt 안의 모든 단어를 각각 5개씩 검색
python dbpia_search.py --file search_queries.txt --limit 5
```

## 4. 고급 필터링 옵션 가이드

DBpia Open API의 기능을 활용하여, 더 정교한 검색 결과를 얻어낼 수 있습니다. 이 파라미터들은 혼합해서 사용할 수 있습니다.

### 대표적인 옵션 목록
| 파라미터 옵션 | 설명 | 기본값 | 사용 예시 |
| :--- | :--- | :--- | :--- |
| `--limit <숫자>` | 키워드 1개당 가져올 최대 검색 결과 수 | 10 | `--limit 20` |
| `--sort <1\|2\|3>` | 정렬 방식 설정<br> - `1`: 관련도 순 (정확도)<br> - `2`: 최근 발행일 순 (최신순)<br> - `3`: 오래된 발행일 순 (과거순) | API 기본값 | `--sort 2` |
| `--page <숫자>` | 페이징 번호 (100건이 넘을 때 다음 페이지) | 1 | `--page 2` |
| `--start_year <년도>` | 발행연도 필터 시작 (YYYY) | 없음 | `--start_year 2020` |
| `--end_year <년도>` | 발행연도 필터 끝 (YYYY) | 없음 | `--end_year 2024` |
| `--output <파일명>` | 저장될 분리된 CSV 파일 명 지정 | 자동 고유생성 | `--output my_paper.csv` |

### 복합 사용 예제 시나리오

**Q. "인공지능 의료"라는 키워드로 2020년도부터 2024년도 사이에 발간된 최신 논문을 50개만 뽑고 싶어요! 저장 파일명은 'ai_medical.csv'로 해주세요.**
```bash
python dbpia_search.py --query "인공지능 의료" --limit 50 --sort 2 --start_year 2020 --end_year 2024 --output ai_medical.csv
```

## 5. 결과 확인 (CSV)
프로그램이 성공적으로 완료되면 콘솔창에 알림이 뜨며, 폴더 내에 `dbpia_results_YYYYMMDD_HHMMSS.csv` (또는 지정한 파일명) 이 생성됩니다. 엑셀로 열람하시어 "제목, 저자, 기관명, 발행월, 원문 링크"를 확인하시면 됩니다.
