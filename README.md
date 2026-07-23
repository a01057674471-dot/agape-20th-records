# 화성아가페교회 20주년 기념책 기록실 V1.2

일반 회원가입 없이 공용 비밀번호로 접속하고, 관리자 메뉴는 별도 관리자 비밀번호로 보호하는 Next.js 프로젝트입니다.

## 메뉴
- 홈
- 원고 작성
- 사진 업로드
- 회의 자료
- 진행 현황
- 관리자
- 관리자 통합 검색

## 1. 설치
```bash
npm install
cp .env.example .env.local
npm run dev
```

## 2. Supabase
1. Supabase 프로젝트 생성
2. SQL Editor에서 `supabase/schema.sql` 실행
3. Project Settings > API에서 URL, anon key, service role key 복사
4. `.env.local`에 입력

## 3. 비밀번호 설정
`.env.local` 또는 Vercel Environment Variables에 아래 값을 등록합니다.
- `SITE_PASSWORD`: 일반 접속 비밀번호
- `ADMIN_PASSWORD`: 관리자 비밀번호
- `SITE_ACCESS_TOKEN`: 길고 임의적인 문자열
- `ADMIN_ACCESS_TOKEN`: 일반 토큰과 다른 길고 임의적인 문자열

## 4. Vercel 배포
GitHub에 프로젝트 전체를 업로드한 뒤 Vercel에서 저장소를 Import합니다. 환경변수를 모두 등록한 후 Deploy를 누릅니다.

## 현재 구현 범위
- 반응형 네이비·골드 디자인
- 일반 비밀번호 접속
- 관리자 별도 비밀번호 접속
- 원고 제출 API
- 다중 사진 업로드 API
- 회의 자료 화면
- 진행 현황 화면
- 관리자 대시보드와 통합 검색 UI
- Supabase 기본 스키마

## 다음 연결 작업
회의자료 업로드/다운로드, 관리자 상태 변경, 공지사항 편집, CSV 내보내기, 실제 통합 검색 결과는 Supabase 데이터와 연결해 확장하면 됩니다.
