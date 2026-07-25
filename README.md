# 아가페 기록실 v2.1

화성아가페교회 20주년 기념책 자료 수집용 Next.js 프로젝트입니다.

## 실행

```bash
npm install
npm run dev
```

## 배포

1. 이 폴더 안의 파일 전체를 GitHub 저장소에 업로드합니다.
2. Vercel에서 GitHub 저장소를 연결합니다.
3. 필요하면 `.env.example`을 참고해 환경변수를 등록합니다.

## Supabase

`supabase/schema.sql`을 Supabase SQL Editor에서 실행합니다.

원고·사진·회의 자료는 Supabase Database와 비공개 Storage에 저장됩니다.

- `NEXT_PUBLIC_SUPABASE_URL`: Supabase 프로젝트 URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: 브라우저의 일회용 서명 업로드용 공개 키
- `SUPABASE_SERVICE_ROLE_KEY`: 서버 전용 키. 브라우저 코드나 GitHub에 넣지 않습니다.

일반 사용자는 제출만 가능하고 전체 자료 열람·상태 변경·삭제는 관리자 화면에서 처리합니다.
