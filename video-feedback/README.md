# 🎬 영상 피드백 사이트

Claude 와 영상을 주고받으며 고치는 로컬 사이트입니다.
"8초쯤 오른쪽 위 글자 키워줘"를 채팅으로 설명하는 대신, **영상을 멈추고 고칠 곳을 클릭**하면 됩니다.

```
Claude 렌더 → 사이트에 자동 업로드 → 멈추고 화면 클릭해 주석 → Claude 가 읽고 수정 → 새 버전 자동 업로드 → 체크리스트로 확인
```

## 실행

```bash
node video-feedback/server.mjs      # http://localhost:4321
```

의존성이 없습니다 (Node 18+). 영상 정보 읽기와 `apply-edits` 에는 `ffmpeg`/`ffprobe` 가 필요합니다.
포트 변경: `PORT=5000 node video-feedback/server.mjs`

## 화면

| 탭 | 하는 일 |
| --- | --- |
| **주석** | 일시정지 후 영상을 클릭 → 그 자리에 핀 + 메모. 시간·위치·**그 순간 화면 스냅샷**이 같이 저장됩니다. 타임라인의 점을 누르면 해당 장면으로 이동. |
| **편집** | 자막(문구·시작/끝·크기·색·배경)과 소리 크기(0–300%)를 직접 고칩니다. 자막은 영상 위에서 끌어 옮길 수 있고, 미리보기가 바로 보입니다. 자동 저장. |
| **체크리스트** | 모든 주석을 미해결 / 확인 대기 / 완료로 묶어 보여줍니다. 항목을 누르면 **고쳐진 버전의 같은 시간**으로 이동해 바로 비교할 수 있고, ✓ 로 완료, ↺ 로 이유와 함께 다시 요청합니다. |

단축키: `Space` 재생/정지 · `←/→` 한 프레임 · `Shift+←/→` 1초

## Claude 쪽 (CLI)

```bash
node video-feedback/cli.mjs upload "내 릴스" out.mp4 --note "첫 렌더"
node video-feedback/cli.mjs feedback                 # 미해결 주석 + 스냅샷 경로
node video-feedback/cli.mjs edits                    # 편집 탭 변경 (자막·소리)
node video-feedback/cli.mjs upload "내 릴스" out.mp4 --note "v2" --fixes 1,2,3
node video-feedback/cli.mjs resolve 4 --note "글자 48→72px"
node video-feedback/cli.mjs apply-edits in.mp4 out.mp4   # 편집 탭 자막·소리를 ffmpeg 로 입히기
node video-feedback/cli.mjs import-subs captions.srt     # Claude 자막을 편집 탭으로
node video-feedback/cli.mjs status
node video-feedback/cli.mjs help
```

`.claude/skills/video-feedback/SKILL.md` 가 있어서 Claude 에게 **"피드백 반영해줘"** 라고만 해도 위 순서대로 진행합니다.

자동 업로드 폴더: 렌더 결과를 `video-feedback/inbox/<프로젝트 이름>.mp4` 로 저장하면 서버가 가져갑니다
(`<프로젝트>__메모.mp4` 형식이면 메모도 붙습니다). 브라우저로 끌어다 놓아도 새 버전이 됩니다.

## 데이터

`video-feedback/data/projects/<id>/` 아래에 영상 버전, `annotations.json`, `edits.json`, 스냅샷이 저장됩니다 (git 제외).
