# 슈뱅 : #샵이랑 !뱅을 실행하낟. 쉘 스키립트이기에 배치로 실행하라. (어떤 프로그램으로 동작할지 지정하는)
# #!/usr/bin/env bash
# $? : 직전의 실행명령어의 엑스코드

# 실행하다 실패하면(0이 아니면 실패) 파이프페일에 인해 더이상 밑으로 진행하지 않음
set -eo pipefail

# 테미널 컬러지정, 초록색으로
COLOR_GREEN=`tput setaf 2;`
# 색깔 초기화 (No Color)
COLOR_NC=`tput sgr0;` # No Color

# 프린트
echo "Starting black"
poetry run black .
echo "OK"

# 아이소트로 픽스 인포트 정렬
echo "Starting ruff"
poetry run ruff check --select I --fix
poetry run ruff check --fix
echo "OK"

# 정적분석 중 제일 중요
echo "Starting mypy"
poetry run mypy .
echo "OK"

# 테스트 진행
echo "Starting pytest with coverage"
poetry run coverage run -m pytest
poetry run coverage report -m
poetry run coverage html
echo "OK"

# 모든게 완벽하게 잘 수행되었으면 출력
echo "${COLOR_GREEN}All tests passed successfully!${COLOR_NC}"

# denied: 최초는 실행권한없음
# chmod +x ./test.sh
# 통과되었으면 all tests passed successfulyl

