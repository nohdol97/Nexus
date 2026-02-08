# SGLang GPU 워커 (스켈레톤)

SGLang 기반 워커를 추가하기 위한 템플릿입니다. 실제 이미지와 실행 명령을 환경에 맞게 교체하세요.

- `REPLACE_WITH_SGLANG_IMAGE`를 실제 이미지로 변경
- 컨테이너 command/args를 사용하는 SGLang 서버 엔트리포인트로 수정
- GPU 오버레이 적용 후 사용

```bash
kubectl apply -k k8s/overlays/gpu
kubectl apply -k k8s/overlays/gpu/sglang
```

이 워커를 활성화했다면 게이트웨이 업스트림과 라우팅 정책에 추가하세요.
