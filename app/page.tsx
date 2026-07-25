import PageHeader from "./components/PageHeader";
import SiteFooter from "./components/SiteFooter";

const tasks = [
  {
    number: "01",
    title: "원고 작성",
    description: "직접 글을 쓰거나 작성한 파일을 첨부해 주세요.",
    href: "/manuscripts",
    action: "원고 작성하기",
  },
  {
    number: "02",
    title: "사진 올리기",
    description: "교회의 소중한 순간이 담긴 사진을 보내 주세요.",
    href: "/photos",
    action: "사진 선택하기",
  },
  {
    number: "03",
    title: "진행 확인",
    description: "기념책 제작이 어디까지 진행됐는지 확인하세요.",
    href: "/progress",
    action: "현황 확인하기",
  },
];

export default function Home() {
  return (
    <div className="site-shell">
      <PageHeader active="home" />
      <main>
        <section className="modern-hero">
          <div className="hero-inner">
            <p className="kicker">화성아가페교회 20주년 · 2006—2026</p>
            <h1>우리의 이야기를<br /><span>한 권의 역사로</span></h1>
            <p className="hero-lead">
              함께 걸어온 스무 해의 원고와 사진을 모아<br className="desktop-only" />
              다음 세대에게 전할 기념책을 만듭니다.
            </p>
            <div className="hero-cta">
              <a className="btn btn-primary" href="/manuscripts">원고 작성하기</a>
              <a className="btn btn-light" href="/photos">사진 올리기</a>
            </div>
          </div>
          <div className="hero-year" aria-hidden="true">
            <span>AGAPE</span>
            <strong>20</strong>
            <i>YEARS</i>
          </div>
        </section>

        <section className="task-section">
          <div className="section-title">
            <div><p>쉬운 자료 제출</p><h2>무엇을 하시겠어요?</h2></div>
            <span>원하는 항목을 누르면 바로 시작할 수 있습니다.</span>
          </div>
          <div className="task-grid">
            {tasks.map((task) => (
              <a className="task-card" href={task.href} key={task.number}>
                <span className="task-number">{task.number}</span>
                <h3>{task.title}</h3>
                <p>{task.description}</p>
                <strong>{task.action}<i>→</i></strong>
              </a>
            ))}
          </div>
        </section>

        <section className="dashboard-strip">
          <div className="deadline-card">
            <span>원고 접수 마감</span>
            <strong>2026. 08. 31</strong>
            <p>완성되지 않은 글도 괜찮습니다. 먼저 기록을 남겨 주세요.</p>
          </div>
          <div className="notice-panel">
            <div className="notice-head"><h2>최근 안내</h2><a href="/meetings">회의 자료 보기 →</a></div>
            <a className="notice-row" href="/photos">
              <span>사진</span><strong>1998~2005년의 오래된 사진을 우선 모집합니다.</strong><i>→</i>
            </a>
            <a className="notice-row" href="/manuscripts">
              <span>원고</span><strong>원고 작성 중간에도 30일간 임시저장할 수 있습니다.</strong><i>→</i>
            </a>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
