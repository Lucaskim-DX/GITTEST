@echo off
echo "============================================="
echo "논문 자동화 연구 - Python 의존성 설치 스크립트"
echo "============================================="

python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [에러] Python이 설치되어 있지 않거나 환경변수 PATH 스크립트에 문제가 있습니다.
    pause
    exit /b
)

echo.
echo "필요한 라이브러리(aiohttp, requests, dotenv)를 설치합니다..."
pip install -r requirements.txt

echo.
echo "============================================="
echo "설치가 완료되었습니다. 이제 에이전트 명령이나 커맨드라인에서 DBpia 스크립트를 정상적으로 실행할 수 있습니다."
echo "============================================="
pause
