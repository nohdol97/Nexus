# GitOps 연계 노트

이 문서는 파이프라인 산출물이 Argo CD와 어떻게 연결되는지 설명합니다.

## 권장 흐름

1) Kubeflow 파이프라인이 배포 매니페스트를 생성
   - 출력: `/workspace/kserve_manifest.yaml`
2) 후속 단계에서 매니페스트를 Git에 커밋
   - 예시 경로: `deployments/kserve/llm-vllm.yaml`
3) Argo CD가 해당 경로를 감시하고 클러스터에 동기화

## 왜 중요한가요?

- **파이프라인이 산출물을 생성**합니다 (무엇을 배포할지).
- **Git이 단일 기준(Single Source of Truth)**이 됩니다 (실제로 배포된 상태).
- Argo CD가 **Git과 클러스터를 일치**시킵니다.

## 다음 단계 (선택)

다음 작업을 수행하는 경량 잡을 추가하세요.
- `kserve_manifest.yaml`을 Git 저장소 경로로 복사
- 커밋 및 푸시
- Argo CD가 자동으로 동기화하도록 유도

## 파일

- `gitops_commit_step.py`: 파이프라인용 헬퍼 스크립트 (옵션)
- `commit_example.md`: 수동 커밋 예시
