"use client";

import { useMemo, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

const files = [
  { title: "원고 작성 가이드", type: "안내", date: "2026.07.25", status: "등록 예정" },
  { title: "사진 선정 기준", type: "사진", date: "2026.07.25", status: "등록 예정" },
  { title: "편집부 회의 자료", type: "회의", date: "2026.07.25", status: "등록 예정" },
];

export default function MeetingsPage() {
  const [query, setQuery] = useState("");
  const filtered = useMemo(() => files.filter((file) => file.title.includes(query.trim())), [query]);
  return (
    <div className="site-shell">
      <PageHeader active="meetings" />
      <main className="subpage">
        <section className="subpage-heading"><p className="kicker">EDITORIAL FILES</p><h1>회의 자료</h1><p>편집부가 공유하는 자료와 작성 기준을 확인합니다.</p></section>
        <section className="content-card">
          <label className="search-box"><span>자료 검색</span><input onChange={(e) => setQuery(e.target.value)} placeholder="자료 제목을 입력하세요" value={query} /></label>
          <div className="file-list">
            {filtered.map((file) => (
              <article className="file-row" key={file.title}>
                <span className="file-type">{file.type}</span>
                <div><h2>{file.title}</h2><p>{file.date}</p></div>
                <strong>{file.status}</strong>
              </article>
            ))}
            {filtered.length === 0 && <p className="empty-state">검색 결과가 없습니다.</p>}
          </div>
          <p className="helper-note">관리자가 자료를 등록하면 이 화면에서 바로 내려받을 수 있습니다.</p>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
