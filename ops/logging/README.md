# 로깅 파이프라인 (Kafka -> Elasticsearch -> Kibana)

게이트웨이의 구조화 로그를 Kafka로 전달하고 Elasticsearch에 색인한 뒤 Kibana에서 검색/대시보드로 확인하는 스택입니다. 로컬 관측성 검증과 쿼리 템플릿 확인에 적합합니다.

## 실행

```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml up -d
```

## 접속

- Kafka: localhost:9092
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

## 메모

- Vector는 `com.docker.compose.service=gateway` 라벨이 붙은 컨테이너의 Docker 로그를 읽습니다.
- 로그 흐름: Vector (docker logs) -> Kafka 토픽 `gateway-logs` -> Vector -> Elasticsearch.
- Kibana는 `gateway-logs-*` 데이터 뷰를 사용합니다.
- 데이터 뷰 자동 생성:
  ```bash
  ./ops/logging/bootstrap_kibana.sh
  ```
- 쿼리 템플릿: `ops/logging/kibana_queries.md`
- 상관관계 가이드: `ops/logging/correlation_guide.md`
- 대시보드 템플릿: `ops/logging/kibana_dashboard.md`
- Saved objects 부트스트랩: `ops/logging/kibana_saved_objects.md`
- 로그 스키마: `ops/logging/log_schema.md`
