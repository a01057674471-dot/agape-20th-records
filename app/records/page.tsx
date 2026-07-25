import PageHeader from "../components/PageHeader";
import RecordsGallery from "../components/RecordsGallery";
import SiteFooter from "../components/SiteFooter";

export default function RecordsPage() {
  return (
    <div className="site-shell">
      <PageHeader active="records" />
      <main className="subpage">
        <section className="subpage-heading">
          <p className="kicker">AGAPE ARCHIVE</p>
          <h1>올라온 기록</h1>
          <p>함께 올린 원고와 사진, 회의자료를 한곳에서 볼 수 있습니다.</p>
        </section>
        <RecordsGallery />
      </main>
      <SiteFooter />
    </div>
  );
}
