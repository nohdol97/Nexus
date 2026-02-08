# Nexus: 엔터프라이즈 AI 플랫폼

Nexus는 엔터프라이즈 환경을 위해 설계된 고가용성 LLM 추론 플랫폼으로, FastAPI, vLLM, Kubernetes를 기반으로 구축되었습니다.

## 📂 프로젝트 구조

- **`ui/`**: Nexus 콘솔 웹 애플리케이션 (Next.js + TypeScript).
- **`Agent.md`**: 구현 규칙 및 가이드라인.
- **`plan.md`**: 상세 프로젝트 로드맵 및 아키텍처.

## 🚀 시작하기

### Nexus 콘솔 (UI)

웹 콘솔은 `ui` 디렉토리에 위치해 있습니다.

```bash
# UI 디렉토리로 이동
cd ui

# 의존성 설치 (아직 설치되지 않은 경우)
npm install

# 개발 서버 시작
npm run dev
```

콘솔은 http://localhost:3000 에서 사용할 수 있습니다.
