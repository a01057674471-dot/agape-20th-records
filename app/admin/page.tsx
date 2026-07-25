"use client";

import { FormEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

type Status = "접수" | "검토 중" | "완료";
type Notice = { id: number; title: string; category: string; createdAt: string };
type Manuscript = {
  id: number; category: string; title: string; author: string; phone: string;
  content: string; fileName?: string; status: Status; submittedAt: string;
};
type PhotoSubmission = {
  id: number; event: string; year: string; name: string; phone: string;
  description: string; fileNames: string[]; count: number; status: Status; submittedAt: string;
};

const MANUSCRIPTS_KEY = "agape-manuscript-submissions";
const PHOTOS_KEY = "agape-photo-submissions";
const NOTICES_KEY = "agape-admin-notices";
const initialNotices: Notice[] = [
  { id: 1, title: "원고 접수 마감일은 2026년 8월 31일입니다.", category: "원고", createdAt: "2026.07.25" },
  { id: 2, title: "1998~2005년의 오래된 사진을 우선 모집합니다.", category: "사진", createdAt: "2026.07.25" },
];

function readList<T>(key: string): T[] {
  try {
    const stored = window.localStorage.getItem(key);
    return stored ? JSON.parse(stored) as T[] : [];
  } catch {
    return [];
  }
}

export default function AdminPage() {
  const [notices, setNotices] = useState<Notice[]>(initialNotices);
  const [manuscripts, setManuscripts] = useState<Manuscript[]>([]);
  const [photos, setPhotos] = useState<PhotoSubmission[]>([]);
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("공지");
  const [saved, setSaved] = useState("");

  useEffect(() => {
    const storedNotices = readList<Notice>(NOTICES_KEY);
    if (storedNotices.length) setNotices(storedNotices);
    setManuscripts(readList<Manuscript>(MANUSCRIPTS_KEY));
    setPhotos(readList<PhotoSubmission>(PHOTOS_KEY));
  }, []);

  function saveNotices(next: Notice[]) {
    setNotices(next);
    window.localStorage.setItem(NOTICES_KEY, JSON.stringify(next));
  }

  function saveManuscripts(next: Manuscript[]) {
    setManuscripts(next);
    window.localStorage.setItem(MANUSCRIPTS_KEY, JSON.stringify(next));
  }

  function savePhotos(next: PhotoSubmission[]) {
    setPhotos(next);
    window.localStorage.setItem(PHOTOS_KEY, JSON.stringify(next));
  }

  function addNotice(event: FormEvent) {
    event.preventDefault();
    if (!title.trim()) return;
    saveNotices([{ id: Date.now(), title: title.trim(), category, createdAt: new Date().toLocaleDateString("ko-KR") }, ...notices]);
    setTitle("");
    setSaved("공지사항을 이 기기에 저장했습니다.");
  }

  return (
    <div className="site-shell">
      <PageHeader active="home" />
      <main className="admin-dashboard">
        <section className="admin-heading">
          <div><p className="kicker">EDITOR DASHBOARD</p><h1>관리자 페이지</h1><p>제출된 원고와 사진, 공지사항을 한곳에서 관리합니다.</p></div>
          <span>편집부 전용</span>
        </section>

        <section className="stat-grid">
          <article><span>접수 원고</span><strong>{manuscripts.length}</strong><p>현재 기기 접수 내역</p></article>
          <article><span>사진 제출</span><strong>{photos.length}</strong><p>현재 기기 접수 내역</p></article>
          <article><span>검토할 자료</span><strong>{[...manuscripts, ...photos].filter((item) => item.status !== "완료").length}</strong><p>완료 전 자료</p></article>
          <article><span>공지사항</span><strong>{notices.length}</strong><p>현재 기기에 저장됨</p></article>
        </section>

        <section className="admin-panel submission-panel">
          <div className="panel-heading"><h2>원고 제출 목록</h2><span>{manuscripts.length}건</span></div>
          {manuscripts.length === 0 ? <p className="empty-state">아직 제출된 원고가 없습니다.</p> : (
            <div className="submission-list">
              {manuscripts.map((item) => (
                <article key={item.id}>
                  <div className="submission-main">
                    <span className="submission-type">{item.category}</span>
                    <h3>{item.title}</h3>
                    <p>{item.author} · {item.phone} · {item.submittedAt}</p>
                    <details><summary>원고 내용 보기</summary><p>{item.content}</p>{item.fileName && <small>첨부: {item.fileName}</small>}</details>
                  </div>
                  <div className="submission-actions">
                    <select aria-label={`${item.title} 상태`} value={item.status} onChange={(event) => saveManuscripts(manuscripts.map((entry) => entry.id === item.id ? { ...entry, status: event.target.value as Status } : entry))}>
                      <option>접수</option><option>검토 중</option><option>완료</option>
                    </select>
                    <button onClick={() => saveManuscripts(manuscripts.filter((entry) => entry.id !== item.id))} type="button">삭제</button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <section className="admin-panel submission-panel">
          <div className="panel-heading"><h2>사진 제출 목록</h2><span>{photos.length}건</span></div>
          {photos.length === 0 ? <p className="empty-state">아직 제출된 사진 내역이 없습니다.</p> : (
            <div className="submission-list">
              {photos.map((item) => (
                <article key={item.id}>
                  <div className="submission-main">
                    <span className="submission-type">{item.year}</span>
                    <h3>{item.event}</h3>
                    <p>{item.name} · {item.phone} · 사진 {item.count}장 · {item.submittedAt}</p>
                    {item.description && <p className="submission-description">{item.description}</p>}
                    <small>파일명: {item.fileNames.join(", ")}</small>
                  </div>
                  <div className="submission-actions">
                    <select aria-label={`${item.event} 상태`} value={item.status} onChange={(event) => savePhotos(photos.map((entry) => entry.id === item.id ? { ...entry, status: event.target.value as Status } : entry))}>
                      <option>접수</option><option>검토 중</option><option>완료</option>
                    </select>
                    <button onClick={() => savePhotos(photos.filter((entry) => entry.id !== item.id))} type="button">삭제</button>
                  </div>
                </article>
              ))}
            </div>
          )}
          <p className="helper-note">현재 단계에서는 사진 정보와 파일명만 저장됩니다. 사진 원본 보관은 온라인 데이터베이스 연결 후 제공됩니다.</p>
        </section>

        <section className="admin-columns">
          <div className="admin-panel">
            <div className="panel-heading"><h2>공지사항 관리</h2><span>{notices.length}개</span></div>
            <form className="notice-form" onSubmit={addNotice}>
              <select onChange={(event) => setCategory(event.target.value)} value={category}>
                <option>공지</option><option>원고</option><option>사진</option><option>회의</option>
              </select>
              <input onChange={(event) => setTitle(event.target.value)} placeholder="새 공지 내용을 입력하세요" value={title} />
              <button type="submit">등록</button>
            </form>
            {saved && <p className="alert-message">{saved}</p>}
            <div className="admin-notice-list">
              {notices.map((notice) => (
                <article key={notice.id}>
                  <span>{notice.category}</span><div><strong>{notice.title}</strong><small>{notice.createdAt}</small></div>
                  <button aria-label={`${notice.title} 삭제`} onClick={() => saveNotices(notices.filter((item) => item.id !== notice.id))} type="button">삭제</button>
                </article>
              ))}
            </div>
          </div>
          <aside className="admin-panel">
            <div className="panel-heading"><h2>저장 안내</h2></div>
            <ul className="admin-checklist">
              <li><span>완료</span>관리자 비밀번호 분리</li>
              <li><span>완료</span>원고·사진 접수 목록</li>
              <li><span>완료</span>접수 상태 변경·삭제</li>
              <li className="waiting"><span>다음</span>온라인 데이터베이스 연결</li>
            </ul>
            <p className="helper-note">현재 접수 내역은 제출한 브라우저에만 저장됩니다. 모든 기기에서 함께 보려면 데이터베이스 연결이 필요합니다.</p>
          </aside>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
