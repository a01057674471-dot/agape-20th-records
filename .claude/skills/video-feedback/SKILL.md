---
name: video-feedback
description: 영상 피드백 사이트(video-feedback/)와 함께 영상을 수정하는 루프. 영상을 렌더한 뒤 사이트에 올리고, 사용자가 영상 위에 남긴 주석(시간·위치·스냅샷)을 읽어 수정하고, 고친 주석을 표시해 새 버전을 올릴 때 사용합니다. "피드백 반영해줘", "주석 확인해줘", "영상 올려줘", "편집 탭 반영해줘", 영상 렌더 직후에 사용하세요.
---

# 영상 피드백 루프

사이트: `node video-feedback/server.mjs` → http://localhost:4321 (안 떠 있으면 백그라운드로 실행)
CLI: `node video-feedback/cli.mjs <명령>` — 프로젝트 이름을 생략하면 가장 최근 프로젝트.

## 1. 렌더한 영상 올리기
```bash
node video-feedback/cli.mjs upload "<프로젝트 이름>" out/video.mp4 --note "무엇을 바꿨는지"
```
렌더할 때마다 새 버전(v1, v2 …)이 됩니다. 사이트가 열려 있으면 자동으로 새 버전이 뜹니다.
(또는 `video-feedback/inbox/<프로젝트 이름>.mp4` 로 저장해도 자동으로 올라갑니다.)

## 2. 주석 읽기
```bash
node video-feedback/cli.mjs feedback            # 미해결만
node video-feedback/cli.mjs feedback --json     # 기계가 읽기 좋은 형식
```
각 주석에는 `#번호`, 버전, **시간(초)**, **화면 위치(x/y %, "오른쪽 위" 등)**, 요청 내용, 스냅샷 경로가 있습니다.
- **스냅샷 이미지를 반드시 Read 로 열어 보세요.** 사용자가 클릭한 곳에 빨간 원이 그려져 있어, "이 글자"가 무엇인지 정확히 알 수 있습니다.
- `재요청:` 이 있으면 이전 수정이 부족했다는 뜻입니다. 이전 `처리:` 내용과 비교해 더 확실하게 고치세요.
- 시간은 렌더 소스(예: Remotion 프레임 = 초 × fps)로 변환해 해당 장면을 찾습니다.

## 3. 편집 탭 변경 확인
```bash
node video-feedback/cli.mjs edits
```
사용자가 편집 탭에서 직접 바꾼 **소리 크기**와 **자막**(시간·문구·위치·크기·색)입니다.
- 렌더 소스에 반영할 수 있으면 소스에 반영 (예: Remotion 의 자막 데이터/볼륨).
- 아니면 자막 없이 렌더한 뒤 `apply-edits <입력> <출력>` 으로 ffmpeg 로 입힙니다.
- 직접 만든 자막을 사용자가 고칠 수 있게 하려면 `import-subs 자막.srt` 로 편집 탭에 넣고, 그 자막은 영상에 굽지 마세요 (미리보기가 겹칩니다).

## 4. 고치고 새 버전 올리면서 처리 표시
```bash
node video-feedback/cli.mjs upload "<프로젝트>" out/video.mp4 --note "v3: 피드백 반영" --fixes 1,2,5
# 주석별로 다른 설명을 남기려면 업로드 후:
node video-feedback/cli.mjs resolve 3 --note "제목 48→72px 로 키움"
```
- 실제로 고친 주석만 표시합니다. 못 고친 것은 이유를 사용자에게 말하세요.
- 상태: 미해결 → (Claude) 수정됨·확인대기 → (사용자) 완료. **완료 처리는 사용자만 합니다.**
- 마지막에 `status` 로 남은 개수를 보고하세요.

## 기타
- `list` 프로젝트 목록 · `export-subs out.srt` 편집 탭 자막 내보내기
- 데이터는 `video-feedback/data/` (git 제외)
