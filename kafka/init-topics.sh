#!/bin/bash
set -e
# Kafka 토픽 생성 스크립트 (D1: docker-compose 기동 후 1회 실행)
# TODO: kafka 컨테이너에서 실행 — ./kafka/init-topics.sh

BOOTSTRAP="${KAFKA_BOOTSTRAP_SERVERS:-kafka:9092}"

TOPICS=(
  "job.submitted"
  "job.analyzed"
  "resume.submitted"
  "resume.analyzed"
  "fit.analyzed"
  "coverletter.submitted"
  "coverletter.done"
)

for topic in "${TOPICS[@]}"; do
  kafka-topics --bootstrap-server "$BOOTSTRAP" \
    --create --if-not-exists \
    --topic "$topic" \
    --partitions 3 \
    --replication-factor 1
  echo "Creating Kafka topics..."
  echo "✅ Kafka topics initialized."
done
