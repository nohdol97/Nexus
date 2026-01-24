# Logging Pipeline (Kafka -> Elasticsearch -> Kibana)

This stack ships structured gateway logs through Kafka and indexes them into Elasticsearch for Kibana search.

## Run

```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml up -d
```

## Access

- Kafka: localhost:9092
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

## Notes

- Vector reads Docker logs from containers labeled `com.docker.compose.service=gateway`.
- Logs flow: Vector (docker logs) -> Kafka topic `gateway-logs` -> Vector -> Elasticsearch.
- Kibana uses the `gateway-logs-*` data view.
- Create the data view automatically:
  ```bash
  ./ops/logging/bootstrap_kibana.sh
  ```
