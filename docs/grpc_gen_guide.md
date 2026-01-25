# gRPC gen 코드 이해 가이드 (PB2/PB2_GRPC)

이 문서는 `gen` 폴더 안의 **자동 생성된 Python 코드**를 읽는 방법을 설명합니다.

---

## 1) gen 코드는 왜 필요한가?

- `contracts/nexus_inference.proto`를 그대로 실행할 수는 없음
- 따라서 proto → Python 코드로 변환해야 함
- 이 변환 결과물이 `*_pb2.py`, `*_pb2_grpc.py` 파일

즉, **gen 코드는 통신을 위한 “자동 생성된 접착제”**라고 보면 됨.

### 생성 방식 (중요)

- 생성 스크립트: `scripts/gen_grpc.sh`
- 해당 스크립트를 실행하면 `gen` 폴더 파일이 **자동 생성**됨
- **직접 수정하지 말고**, proto 변경 시 스크립트를 다시 실행

---

## 2) gen 폴더 안 파일 역할

### `nexus_inference_pb2.py`

- **메시지(요청/응답 데이터 구조)** 정의
- 예: `ChatCompletionRequest`, `ChatCompletionResponse`, `Message`
- 직렬화/역직렬화(바이너리 변환) 코드가 포함됨

이 파일을 보면 “요청/응답이 어떤 필드로 구성되는지”를 알 수 있음.

---

### `nexus_inference_pb2_grpc.py`

- **서비스(메서드) 연결 코드**
- 클라이언트용 Stub, 서버용 Servicer가 정의됨

주요 구성 요소:

- **Stub**: 클라이언트가 호출하는 객체
  - `InferenceServiceStub`
  - 예: `stub.ChatCompletion(...)`

- **Servicer**: 서버가 구현해야 하는 함수 목록
  - `InferenceServiceServicer`
  - 예: `def ChatCompletion(self, request, context)`

- **add_..._to_server**: 구현체를 실제 서버에 등록하는 함수
  - `add_InferenceServiceServicer_to_server`

---

## 3) 왜 import가 이상하게 보이나?

생성 코드에는 이런 형태가 있음:

```python
import nexus_inference_pb2 as nexus__inference__pb2
```

이는 생성기가 **같은 폴더에 있는 파일**로 가정했기 때문.
그래서 실행할 때 `gen` 경로를 `sys.path`에 추가해서 읽게 한다.

예:
```python
GEN_DIR = ".../gateway/app/grpc/gen"
sys.path.insert(0, GEN_DIR)
```

---

## 4) 실제로 읽을 때 보는 부분

실제 코드에서 필요한 부분만 보면 충분함.

- 어떤 메시지가 있나? (`ChatCompletionRequest`, `Message` 등)
- 어떤 RPC가 있나? (`ChatCompletion`, `Health` 등)

나머지 코드는 자동 생성이므로 상세 이해는 필요하지 않음.

---

## 5) 기억하면 좋은 요약

- `*_pb2.py` → **데이터 구조 정의서**
- `*_pb2_grpc.py` → **클라이언트/서버 연결기**

---

## 6) 연결된 파일

- proto: `contracts/nexus_inference.proto`
- gen (gateway): `gateway/app/grpc/gen/*`
- gen (worker): `serving/mock-worker/grpc_gen/*`
- 가이드: `docs/grpc_agent_guide.md`
