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

현재 UI와 브라우저 임시저장까지 작동합니다. 실제 원고 제출, 사진 저장, 관리자 인증은 Supabase 연결 작업이 필요합니다.
