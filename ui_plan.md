# Nexus Console UI 아키텍처

> [!NOTE]
> 이 문서는 `ui/` 디렉토리에 위치한 Nexus Console 웹 애플리케이션의 구현 상세 내용을 설명합니다.

## 🛠 기술 스택 (Tech Stack)

- **프레임워크**: [Next.js 14+](https://nextjs.org/) (App Router)
- **언어**: TypeScript
- **스타일링**: [TailwindCSS](https://tailwindcss.com/)
- **아이콘**: [Lucide React](https://lucide.dev/)
- **차트**: [Recharts](https://recharts.org/)
- **유틸리티**: 클래스 이름 관리를 위한 `clsx`, `tailwind-merge`

## 📂 프로젝트 구조 (Project Structure)

```
ui/
├── src/
│   ├── app/                 # Next.js App Router (페이지)
│   │   ├── layout.tsx       # 사이드바 및 폰트 설정을 포함한 최상위 레이아웃
│   │   ├── page.tsx         # 대시보드 (메인 홈)
│   │   ├── playground/      # 모델 테스트용 플레이그라운드 페이지
│   │   ├── api-keys/        # API 키 관리 페이지
│   │   └── settings/        # 시스템 설정 페이지
│   ├── components/          # 재사용 가능한 React 컴포넌트
│   │   ├── layout/          # 레이아웃 관련 (사이드바, 헤더)
│   │   ├── dashboard/       # 대시보드 위젯 (통계 카드, 요청 차트)
│   │   ├── playground/      # 채팅 인터페이스 컴포넌트
│   │   └── apikeys/         # API 키 목록 및 관리 컴포넌트
│   └── lib/                 # 유틸리티 함수 (cn 등)
```

## 🧩 주요 컴포넌트 (Key Components)

### 레이아웃 (Layout)
- **`Sidebar.tsx`**: 반응형 내비게이션 메뉴입니다. 현재 활성화된 페이지 상태를 보여주며, 페이지 이동 간에도 지속적으로 유지됩니다.
- **`RootLayout`**: 애플리케이션 전체를 감싸며, 폰트(`Geist`) 적용 및 사이드바 구조를 제공합니다.

### 대시보드 (Dashboard, `/`)
- **`StatsCard`**: 주요 지표(제목, 값, 추세)를 표시하는 재사용 가능한 카드 컴포넌트입니다.
- **`RequestsChart`**: `recharts`를 사용하여 시간대별 요청 트래픽을 시각화한 영역 차트(Area Chart)입니다.
- **활성 모델 목록**: 현재 로드된 모델의 상태와 부하량(Load)을 보여주는 간단한 상태 목록입니다.

### 플레이그라운드 (Playground, `/playground`)
- **`ChatInterface`**: LLM과의 채팅 경험을 시뮬레이션하는 핵심 컴포넌트입니다. 메시지 상태(`user` vs `assistant`)를 관리하고 스트리밍 응답을 모방합니다.
- **`ModelSelector`**: 사용 가능한 게이트웨이 모델(Llama 3, Mistral, 프록시 등)을 선택할 수 있는 드롭다운입니다.
- **파라미터 패널**: `Temperature`, `Max Tokens` 등 생성 관련 설정을 제어합니다.

### API 키 (API Keys, `/api-keys`)
- **`ApiKeyList`**: API 키 목록을 표 형태로 보여줍니다.
  - 토큰 접두사(Prefix) 마스킹/해제 기능
  - "클립보드에 복사" 기능
  - 상태 표시기 (활성/취소됨)

## 🎨 디자인 시스템 (Design System)

- **색상**: `Slate`, `Indigo`, `Violet` 팔레트를 주조색으로 사용합니다.
- **다크 모드**: Tailwind의 `dark:` 변경자를 통해 완벽하게 지원됩니다. 시스템 설정을 자동으로 감지합니다.
- **타이포그래피**: 현대적이고 기술적인 느낌을 위해 `Geist Sans`와 `Geist Mono`를 사용합니다.

## 🔜 향후 연동 계획 (Future Integration Points)

이 콘솔이 완전히 기능하려면 Nexus Gateway와의 다음 연동이 필요합니다:

1.  **인증 (Auth)**: 모의(mock) `system` 상태를 실제 사용자 세션으로 대체해야 합니다.
2.  **대시보드 API**: `RequestsChart`를 Prometheus/Grafana API와 연결하여 실제 데이터를 표현해야 합니다.
3.  **플레이그라운드 API**: `ChatInterface`를 `POST /v1/chat/completions` 엔드포인트와 연결해야 합니다.
4.  **설정 (Settings)**: 설정을 로컬 상태가 아닌 게이트웨이의 제어 평면(Redis/Postgres)에 저장하도록 변경해야 합니다.
