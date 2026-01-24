# 터미널 명령어/옵션(단축어) 가이드

이 문서는 프로젝트 진행 중 자주 등장하는 **명령어와 옵션(단축어)**의 의미를 정리합니다.

---

## 1) 기본 구조

```
명령어 [옵션] [대상/인자]
```

- **옵션(Flags)**: `-s`, `-X`, `--max-time` 처럼 동작을 바꾸는 짧은/긴 스위치
- **인자**: 파일 경로, URL, 이름 등 실제 대상

---

## 2) 셸 문법(자주 쓰는 기호)

- `|` (파이프): 앞 명령의 출력을 뒤 명령의 입력으로 전달
  - 예: `curl ... | head -n 5`
- `>` / `>>` (리다이렉트): 출력 저장(덮어쓰기/추가)
  - 예: `curl ... > output.txt`
- `2>&1`: 에러(stderr)를 표준출력(stdout)으로 합침
- `&&`: 앞 명령이 성공(0)하면 다음 명령 실행
- `||`: 앞 명령이 실패하면 다음 명령 실행
- `;`: 줄을 나누지 않고 순차 실행
- `\` : 줄 바꿈(긴 명령 줄 정리)

---

## 3) curl (HTTP 요청)

- `-s` : 조용히 실행(진행/에러 로그 최소화)
- `-X` : HTTP 메서드 지정 (`GET`, `POST` 등)
- `-H` : 헤더 추가
- `-d` : 요청 바디(JSON 등)
- `-o` : 응답 저장 파일 지정
- `-w` : 응답 코드/시간 등 출력 포맷 지정
- `--max-time` : 최대 대기 시간(초)

예시:
```bash
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: dev-key' \
  -d '{"model":"mock","messages":[{"role":"user","content":"hello"}]}'
```

---

## 4) docker / docker compose

### docker
- `docker logs --tail N <container>`: 마지막 N줄 로그 보기
- `docker exec -it <container> <cmd>`: 컨테이너 내부 명령 실행
- `docker inspect <container>`: 컨테이너 상세 정보

### docker compose
- `-f 파일.yml`: compose 파일 지정(여러 개 가능)
- `up -d`: 백그라운드로 실행
- `down`: 컨테이너 종료/삭제
- `down -v`: 컨테이너 + 볼륨 삭제(데이터까지 삭제)
- `ps`: 실행 상태 확인
- `stop/start/restart`: 중지/시작/재시작
- `--force-recreate`: 컨테이너 강제 재생성
- `--remove-orphans`: 정의되지 않은 컨테이너 제거

예시:
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml up -d
```

---

## 5) kubectl (Kubernetes)

- `get`: 리소스 조회 (pods, svc 등)
- `describe`: 상세 정보/이벤트 확인
- `logs`: 로그 확인
- `exec`: 컨테이너 내부 명령 실행
- `apply -f`: 매니페스트 적용
- `apply -k`: kustomize 적용
- `delete -f / -k`: 리소스 삭제
- `port-forward`: 로컬 포트로 연결
- `patch`: 리소스 일부 수정

예시:
```bash
kubectl get pods -n kubeflow
kubectl logs -n kubeflow <pod-name>
```

---

## 6) git

- `git status -sb`: 짧은 상태 요약
- `git add`: 스테이징
- `git commit -m`: 커밋 메시지와 함께 저장
- `git push`: 원격 저장소에 업로드
- `git restore <file>`: 변경 되돌리기
- `git clean -fd`: 추적되지 않는 파일/폴더 삭제

---

## 7) 검색/출력 관련

- `rg` (ripgrep): 빠른 텍스트 검색
  - `rg -n 패턴 파일`: 줄 번호 포함
- `grep`: 텍스트 검색
  - `grep -Fq`: 고정 문자열(Fixed), 조용히(Quiet) 확인
- `head -n N`: 앞부분 N줄 보기
- `tail -n N`: 뒷부분 N줄 보기
- `cat`: 파일 전체 출력

---

## 8) 프로세스/네트워크 관련

- `ps -p PID`: 특정 프로세스 확인
- `pgrep -f 패턴`: 패턴으로 프로세스 찾기
- `kill PID`: 프로세스 종료
- `sleep N`: N초 대기
- `lsof -i :PORT`: 포트 사용 프로세스 확인
- `nc -z host port`: 포트 열림 여부 확인

---

## 9) 자주 쓰는 조합 예시

```bash
# 로그 + 필터
curl -s http://localhost:9090/api/v1/rules | head -n 5

# 상태 확인 후 다음 명령
nc -z localhost 9200 && curl -s http://localhost:9200
```

---

## 참고
- 옵션은 명령어마다 다를 수 있습니다. `--help`로 자세한 설명 확인 가능
  - 예: `curl --help`, `docker compose --help`
