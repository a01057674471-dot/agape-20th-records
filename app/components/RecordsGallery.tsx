"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { getSubmissionToken, removeSubmissionToken } from "../lib/mySubmissions";

type SubmissionFile = {
  id: string;
  original_name: string;
  mime_type: string;
  size_bytes: number;
  downloadUrl: string | null;
};

type Submission = {
  id: string;
  kind: "manuscript" | "photo" | "meeting";
  title: string;
  name: string;
  content: string | null;
  created_at: string;
  submission_files: SubmissionFile[];
};

const kindLabel = {
  manuscript: "원고",
  photo: "사진",
  meeting: "회의자료",
};

function readableSize(bytes: number) {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))}KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)}MB`;
}

export default function RecordsGallery({ compact = false }: { compact?: boolean }) {
  const [items, setItems] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [filter, setFilter] = useState<"all" | Submission["kind"]>("all");
  const [editing, setEditing] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editName, setEditName] = useState("");
  const [editContent, setEditContent] = useState("");

  const load = useCallback(async () => {
    try {
      const response = await fetch("/api/submissions", { cache: "no-store" });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message);
      setItems(data.submissions);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "올라온 자료를 불러오지 못했습니다.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const visibleItems = useMemo(() => {
    const filtered = filter === "all" ? items : items.filter((item) => item.kind === filter);
    return compact ? filtered.slice(0, 6) : filtered;
  }, [compact, filter, items]);

  function beginEdit(item: Submission) {
    setEditing(item.id);
    setEditTitle(item.title);
    setEditName(item.name);
    setEditContent(item.content ?? "");
    setMessage("");
  }

  async function saveEdit(event: FormEvent, item: Submission) {
    event.preventDefault();
    const token = getSubmissionToken(item.id);
    if (!token) return;
    const response = await fetch(`/api/submissions/${item.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", "x-submission-token": token },
      body: JSON.stringify({
        title: editTitle,
        name: editName,
        ...(item.kind === "manuscript" ? { content: editContent } : {}),
      }),
    });
    const data = await response.json();
    if (!response.ok) {
      setMessage(data.message || "자료를 수정하지 못했습니다.");
      return;
    }
    setEditing(null);
    setMessage("수정되었습니다.");
    await load();
  }

  async function deleteItem(item: Submission) {
    const token = getSubmissionToken(item.id);
    if (!token || !window.confirm(`“${item.title}” 자료를 삭제할까요?`)) return;
    const response = await fetch(`/api/submissions/${item.id}`, {
      method: "DELETE",
      headers: { "x-submission-token": token },
    });
    const data = await response.json();
    if (!response.ok) {
      setMessage(data.message || "자료를 삭제하지 못했습니다.");
      return;
    }
    removeSubmissionToken(item.id);
    setItems((current) => current.filter((entry) => entry.id !== item.id));
    setMessage("삭제되었습니다.");
  }

  return (
    <section className={compact ? "records-home" : "records-browser"}>
      {!compact && (
        <div className="record-filters" aria-label="자료 종류 선택">
          {[
            ["all", "전체"],
            ["manuscript", "원고"],
            ["photo", "사진"],
            ["meeting", "회의자료"],
          ].map(([value, label]) => (
            <button
              className={filter === value ? "active" : undefined}
              key={value}
              onClick={() => setFilter(value as typeof filter)}
              type="button"
            >
              {label}
            </button>
          ))}
        </div>
      )}

      {message && <p className="records-message" role="status">{message}</p>}
      {loading && <p className="empty-state">올라온 자료를 불러오는 중입니다.</p>}
      {!loading && visibleItems.length === 0 && <p className="empty-state">아직 올라온 자료가 없습니다.</p>}

      <div className="records-grid">
        {visibleItems.map((item) => {
          const mine = Boolean(getSubmissionToken(item.id));
          const imageFiles = item.submission_files.filter((file) => file.mime_type.startsWith("image/"));
          const pdfFiles = item.submission_files.filter((file) => file.mime_type === "application/pdf");
          return (
            <article className="record-card" key={item.id}>
              <div className="record-card-head">
                <span>{kindLabel[item.kind]}</span>
                <time>{new Date(item.created_at).toLocaleDateString("ko-KR")}</time>
              </div>
              {imageFiles.length > 0 && (
                <div className="record-images">
                  {imageFiles.slice(0, compact ? 1 : 10).map((file) => file.downloadUrl && (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img alt={`${item.title} 사진`} key={file.id} loading="lazy" src={file.downloadUrl} />
                  ))}
                </div>
              )}
              <h3>{item.title}</h3>
              <p className="record-author">작성자 {item.name}</p>
              {item.content && <p className="record-content">{item.content}</p>}
              {!compact && pdfFiles.map((file) => file.downloadUrl && (
                <iframe className="pdf-preview" key={file.id} src={file.downloadUrl} title={`${file.original_name} 미리보기`} />
              ))}
              {item.submission_files.length > 0 && (
                <div className="record-files">
                  {item.submission_files.map((file) => (
                    <a href={file.downloadUrl ?? "#"} key={file.id}>
                      {file.original_name} · {readableSize(file.size_bytes)}
                    </a>
                  ))}
                </div>
              )}
              {mine && !compact && (
                <div className="author-actions">
                  <button onClick={() => beginEdit(item)} type="button">수정</button>
                  <button className="danger" onClick={() => deleteItem(item)} type="button">삭제</button>
                </div>
              )}
              {editing === item.id && (
                <form className="record-edit-form" onSubmit={(event) => saveEdit(event, item)}>
                  <label>제목<input onChange={(event) => setEditTitle(event.target.value)} value={editTitle} /></label>
                  <label>이름<input onChange={(event) => setEditName(event.target.value)} value={editName} /></label>
                  {item.kind === "manuscript" && (
                    <label>원고 내용<textarea onChange={(event) => setEditContent(event.target.value)} value={editContent} /></label>
                  )}
                  <div>
                    <button className="btn btn-primary" type="submit">저장하기</button>
                    <button onClick={() => setEditing(null)} type="button">취소</button>
                  </div>
                </form>
              )}
            </article>
          );
        })}
      </div>
      {compact && <a className="btn btn-light records-more" href="/records">올라온 기록 모두 보기</a>}
    </section>
  );
}
