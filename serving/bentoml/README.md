# BentoML 스캐폴딩

이 폴더는 BentoML 기반 모델 워커를 만들기 위한 최소 구조와 실행 흐름을 제공합니다. 실제 모델을 붙이기 전, 프로젝트 뼈대를 잡고 빌드/컨테이너화 과정을 빠르게 검증하는 용도입니다.

## 추천 구조

- `service.py`: BentoML 서비스 정의 (현재는 최소 모의 서비스)
- `requirements.txt`: 의존성 정의 (bentoml, torch, transformers 등)
- `bentofile.yaml`: 빌드/패키징 설정

## 다음 단계

- `service.py`를 실제 모델 로딩/추론 로직으로 교체
- 필요한 의존성을 `requirements.txt`에 추가
- `bentofile.yaml`에서 이미지/엔트리포인트 설정을 조정

## 포함된 파일

- `service.py`
- `requirements.txt`
- `bentofile.yaml`

## 이미지 빌드 (예시)

```bash
pip install -r requirements.txt
bentoml build
bentoml containerize nexus_bentoml_worker:latest -t nexus-bentoml-worker:latest
```
