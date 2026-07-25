"use client";

import { FormEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

type Notice = { id: number; title: string; category: string; createdAt: string };

const initialNotices: Notice[] = [
  { id: 1, title: "원고 접수 마감일은 2026년 8월 31일입니다.", category: "원고", createdAt: "2026.07.25" },
  { id: 2, title: "1998~2005년의 오래된 사진을 우선 모집합니다.", category: "사진", createdAt: "2026.07.25" },
];

export default function AdminPage() {
  const [notices, setNotices] = useState<Notice[]>(initialNotices);
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("공지");
  const [saved, setSaved] = useState("");

  useEffect(() => {
    const stored = window.localStorage.getItem("agape-admin-notices");
    if (stored) setNotices(JSON.parse(stored) as Notice[]);
  }, []);

  function persist(next: Notice[]) {
    setNotices(next);
    window.localStorage.setItem("agape-admin-notices", JSON.stringify(next));
  }

  function addNotice(event: FormEvent) {
    event.preventDefault();
    if (!title.trim()) return;
    persist([{ id: Date.now(), title: title.trim(), category, createdAt: new Date().toLocaleDateString("ko-KR") }, ...notices]);
    setTitle("");
    setSaved("공지사항을 이 기기에 저장했습니다.");
  }

  return (
    <div className="site-shell">
      <PageHeader active="home" />
      <main className="admin-dashboard">
        <section className="admin-heading">
          <div><p className="kicker">EDITOR DASHBOARD</p><h1>관리자</h1><p>20주년 기념책 자료와 공지사항을 관리합니다.</p></div>
          <span>편집부 전용</span>
        </section>

        <section className="stat-grid">
          <article><span>접수 원고</span><strong>0</strong><p>데이터 연결 후 자동 집계</p></article>
          <article><span>등록 사진</span><strong>0</strong><p>데이터 연결 후 자동 집계</p></article>
          <article><span>회의 자료</span><strong>0</strong><p>파일 등록 기능 준비 중</p></article>
          <article><span>공지사항</span><strong>{notices.length}</strong><p>현재 기기에 저장됨</p></article>
        </section>

        <section className="admin-columns">
          <div className="admin-panel">
            <div className="panel-heading"><h2>공지사항 관리</h2><span>{notices.length}개</span></div>
            <form className="notice-form" onSubmit={addNotice}>
              <select onChange={(e) => setCategory(e.target.value)} value={category}>
                <option>공지</option><option>원고</option><option>사진</option><option>회의</option>
              </select>
              <input onChange={(e) => setTitle(e.target.value)} placeholder="새 공지 내용을 입력하세요" value={title} />
              <button type="submit">등록</button>
            </form>
            {saved && <p className="alert-message">{saved}</p>}
            <div className="admin-notice-list">
              {notices.map((notice) => (
                <article key={notice.id}>
                  <span>{notice.category}</span><div><strong>{notice.title}</strong><small>{notice.createdAt}</small></div>
                  <button aria-label={`${notice.title} 삭제`} onClick={() => persist(notices.filter((item) => item.id !== notice.id))} type="button">삭제</button>
                </article>
              ))}
            </div>
          </div>
          <aside className="admin-panel">
            <div className="panel-heading"><h2>기능 현황</h2></div>
            <ul className="admin-checklist">
              <li><span>완료</span>홈·원고·사진 화면</li>
              <li><span>완료</span>회의 자료 검색</li>
              <li><span>완료</span>공지 로컬 관리</li>
              <li className="waiting"><span>대기</span>Supabase 데이터 연결</li>
              <li className="waiting"><span>대기</span>실제 파일 업로드·다운로드</li>
            </ul>
            <p className="helper-note">현재 공지는 이 브라우저에만 저장됩니다. 모든 사용자에게 공유하려면 데이터베이스 연결이 필요합니다.</p>
          </aside>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
