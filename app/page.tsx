import PageHeader from "./components/PageHeader";
import SiteFooter from "./components/SiteFooter";

const actions = [
  { step: "1", icon: "✎", title: "원고 작성", description: "글을 직접 작성하거나 파일로 올립니다.", href: "/manuscripts", tone: "navy" },
  { step: "2", icon: "▧", title: "사진 올리기", description: "교회의 소중한 사진을 보냅니다.", href: "/photos", tone: "gold" },
  { step: "3", icon: "✓", title: "진행 확인", description: "기념책 제작 현황을 확인합니다.", href: "/progress", tone: "sage" },
];

export default function Home() {
  return (
    <div className="site-shell accessible-home">
      <PageHeader active="home" />
      <main>
        <section className="simple-hero">
          <div>
            <p className="anniversary-label">화성아가페교회 20주년</p>
            <h1>함께 걸어온 스무 해,<br /><span>당신의 기억을 들려주세요</span></h1>
            <p className="simple-description">
              원고와 사진을 모아 다음 세대에게 전할<br className="desktop-only" /> 20주년 기념책을 만듭니다.
            </p>
          </div>
          <div className="simple-emblem" aria-hidden="true">
            <strong>20</strong><span>2006—2026</span>
          </div>
        </section>

        <section className="choice-section">
          <div className="choice-heading">
            <p>무엇을 하시겠어요?</p>
            <h2>아래에서 원하는 일을 눌러주세요</h2>
          </div>
          <div className="primary-actions">
            {actions.map((action) => (
              <a className={`primary-action ${action.tone}`} href={action.href} key={action.step}>
                <span className="step-number">{action.step}</span>
                <span className="action-icon" aria-hidden="true">{action.icon}</span>
                <strong>{action.title}</strong>
                <span className="action-description">{action.description}</span>
                <span className="action-go">바로가기 →</span>
              </a>
            ))}
          </div>
          <div className="help-strip">
            <span className="help-icon" aria-hidden="true">i</span>
            <div><strong>도움이 필요하신가요?</strong><p>작성 방법이 어렵다면 편집부에 문의해 주세요.</p></div>
            <a href="/meetings">회의 자료 보기</a>
          </div>
        </section>

        <section className="home-notices">
          <div className="home-notice-title"><span>공지사항</span><h2>꼭 확인해 주세요</h2></div>
          <div className="home-notice-list">
            <a href="/manuscripts"><span>원고</span><strong>원고 접수 마감일은 2026년 8월 31일입니다.</strong><i>→</i></a>
            <a href="/photos"><span>사진</span><strong>1998~2005년의 오래된 사진을 우선 모집합니다.</strong><i>→</i></a>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
