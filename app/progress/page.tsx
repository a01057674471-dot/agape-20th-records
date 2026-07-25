import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

const steps = [
  { title: "자료 모집", description: "원고와 사진을 모으고 있습니다.", state: "진행 중", active: true },
  { title: "원고 정리", description: "분류와 1차 교정 작업을 진행합니다.", state: "다음 단계", active: false },
  { title: "편집·디자인", description: "책의 구성과 지면을 완성합니다.", state: "예정", active: false },
  { title: "최종 검수", description: "내용과 인쇄 파일을 확인합니다.", state: "예정", active: false },
];

export default function ProgressPage() {
  return (
    <div className="site-shell">
      <PageHeader active="progress" />
      <main className="subpage">
        <section className="subpage-heading"><p className="kicker">PROJECT STATUS</p><h1>진행 현황</h1><p>20주년 기념책 제작 과정을 한눈에 확인하세요.</p></section>
        <section className="content-card">
          <div className="progress-summary">
            <div><span>현재 단계</span><strong>자료 모집</strong><p>원고 접수 마감 2026년 8월 31일</p></div>
            <div className="progress-ring"><strong>1</strong><span>/ 4단계</span></div>
          </div>
          <div className="timeline">
            {steps.map((step, index) => (
              <article className={step.active ? "timeline-item active" : "timeline-item"} key={step.title}>
                <span>{index + 1}</span><div><h2>{step.title}</h2><p>{step.description}</p></div><strong>{step.state}</strong>
              </article>
            ))}
          </div>
          <div className="progress-help"><strong>아직 원고나 사진을 보내지 않으셨나요?</strong><div><a href="/manuscripts">원고 작성</a><a href="/photos">사진 올리기</a></div></div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
