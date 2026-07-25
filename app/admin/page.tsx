"use client";

import { useCallback, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

type Status = "접수" | "검토 중" | "완료";
type SubmissionFile = {
  id: string;
  original_name: string;
  size_bytes: number;
  downloadUrl: string | null;
};
type Submission = {
  id: string;
  kind: "manuscript" | "photo" | "meeting";
  title: string;
  name: string;
  content: string | null;
  status: Status;
  created_at: string;
  submission_files: SubmissionFile[];
};

const KIND_LABELS = { manuscript: "원고", photo: "사진", meeting: "회의 자료" };

function readableSize(bytes: number) {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))}KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)}MB`;
}

export default function AdminPage() {
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  const loadSubmissions = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/submissions", { cache: "no-store" });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message);
      setSubmissions(data.submissions);
      setMessage("");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "접수 목록을 불러오지 못했습니다.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadSubmissions(); }, [loadSubmissions]);

  async function changeStatus(item: Submission, status: Status) {
    const response = await fetch(`/api/submissions/${item.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    if (!response.ok) {
      setMessage("상태를 변경하지 못했습니다.");
      return;
    }
    setSubmissions((current) => current.map((entry) => entry.id === item.id ? { ...entry, status } : entry));
  }

  async function deleteSubmission(item: Submission) {
    if (!window.confirm(`“${item.title}” 자료를 완전히 삭제할까요?`)) return;
    const response = await fetch(`/api/submissions/${item.id}`, { method: "DELETE" });
    if (!response.ok) {
      setMessage("자료를 삭제하지 못했습니다.");
      return;
    }
    setSubmissions((current) => current.filter((entry) => entry.id !== item.id));
  }

  function renderSection(kind: Submission["kind"]) {
    const items = submissions.filter((item) => item.kind === kind);
    return (
      <section className="admin-panel submission-panel" key={kind}>
        <div className="panel-heading"><h2>{KIND_LABELS[kind]} 제출 목록</h2><span>{items.length}건</span></div>
        {items.length === 0 ? <p className="empty-state">아직 제출된 자료가 없습니다.</p> : (
          <div className="submission-list">
            {items.map((item) => (
              <article key={item.id}>
                <div className="submission-main">
                  <span className="submission-type">{KIND_LABELS[item.kind]}</span>
                  <h3>{item.title}</h3>
                  <p>{item.name} · {new Date(item.created_at).toLocaleString("ko-KR")}</p>
                  {item.content && <details><summary>원고 내용 보기</summary><p>{item.content}</p></details>}
                  {item.submission_files.length > 0 && (
                    <div className="admin-file-links">
                      {item.submission_files.map((file) => file.downloadUrl ? (
                        <a href={file.downloadUrl} key={file.id}>{file.original_name} · {readableSize(file.size_bytes)}</a>
                      ) : <span key={file.id}>{file.original_name}</span>)}
                    </div>
                  )}
                </div>
                <div className="submission-actions">
                  <select aria-label={`${item.title} 상태`} onChange={(event) => changeStatus(item, event.target.value as Status)} value={item.status}>
                    <option>접수</option><option>검토 중</option><option>완료</option>
                  </select>
                  <button onClick={() => deleteSubmission(item)} type="button">삭제</button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    );
  }

  return (
    <div className="site-shell">
      <PageHeader active="home" />
      <main className="admin-dashboard">
        <section className="admin-heading">
          <div><p className="kicker">EDITOR DASHBOARD</p><h1>관리자 페이지</h1><p>모든 기기에서 제출된 원고와 사진, 회의 자료를 관리합니다.</p></div>
          <span>편집부 전용</span>
        </section>
        {message && <p className="alert-message" role="status">{message}</p>}
        <section className="stat-grid">
          <article><span>원고</span><strong>{submissions.filter((item) => item.kind === "manuscript").length}</strong><p>온라인 접수</p></article>
          <article><span>사진</span><strong>{submissions.filter((item) => item.kind === "photo").length}</strong><p>온라인 접수</p></article>
          <article><span>회의 자료</span><strong>{submissions.filter((item) => item.kind === "meeting").length}</strong><p>온라인 접수</p></article>
          <article><span>검토할 자료</span><strong>{submissions.filter((item) => item.status !== "완료").length}</strong><p>완료 전 자료</p></article>
        </section>
        {loading ? <section className="admin-panel"><p className="empty-state">온라인 자료를 불러오는 중입니다.</p></section> : (
          <>
            {renderSection("manuscript")}
            {renderSection("photo")}
            {renderSection("meeting")}
          </>
        )}
      </main>
      <SiteFooter />
    </div>
  );
}
