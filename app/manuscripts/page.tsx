"use client";

import { ChangeEvent, FormEvent, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";
import { uploadSubmission } from "../lib/uploadSubmission";

const MAX_FILE_SIZE = 30 * 1024 * 1024;

export default function ManuscriptPage() {
  const [title, setTitle] = useState("");
  const [name, setName] = useState("");
  const [content, setContent] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);

  function selectFile(event: ChangeEvent<HTMLInputElement>) {
    const selected = event.target.files?.[0] ?? null;
    if (selected && selected.size > MAX_FILE_SIZE) {
      event.target.value = "";
      setFile(null);
      setMessage("원고 파일은 최대 30MB까지 올릴 수 있습니다.");
      return;
    }
    setFile(selected);
    setMessage("");
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!title.trim() || !name.trim()) {
      setMessage("제목과 이름을 입력해 주세요.");
      return;
    }
    if (!content.trim() && !file) {
      setMessage("원고 내용을 쓰거나 원고 파일을 선택해 주세요.");
      return;
    }

    setSubmitting(true);
    setMessage("원고를 안전하게 전송하고 있습니다. 잠시만 기다려 주세요.");
    try {
      await uploadSubmission({
        kind: "manuscript",
        title: title.trim(),
        name: name.trim(),
        content: content.trim(),
        files: file ? [file] : [],
      });
      setDone(true);
      setMessage("");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "원고를 접수하지 못했습니다.");
    } finally {
      setSubmitting(false);
    }
  }

  function reset() {
    setTitle("");
    setName("");
    setContent("");
    setFile(null);
    setDone(false);
  }

  return (
    <div className="site-shell">
      <PageHeader active="manuscripts" />
      <main className="form-page">
        <section className="page-intro">
          <p className="eyebrow">SHARE YOUR STORY</p>
          <h1>원고 올리기</h1>
          <p>제목과 이름만 적고, 편안하게 원고를 보내 주세요.</p>
        </section>

        {!done ? (
          <section className="form-card simple-submit-card">
            <div className="guide-box">
              <strong>두 가지 방법 중 편한 방법을 선택하세요</strong>
              <p>화면에 직접 글을 쓰거나, 작성해 둔 한글·워드·PDF 파일을 선택할 수 있습니다.</p>
            </div>
            <form onSubmit={submit}>
              <div className="field-row">
                <div className="field">
                  <label htmlFor="manuscript-title">제목 <em>필수</em></label>
                  <input id="manuscript-title" onChange={(event) => setTitle(event.target.value)} placeholder="원고 제목" value={title} />
                </div>
                <div className="field">
                  <label htmlFor="manuscript-name">이름 <em>필수</em></label>
                  <input id="manuscript-name" onChange={(event) => setName(event.target.value)} placeholder="작성자 이름" value={name} />
                </div>
              </div>
              <div className="field">
                <div className="label-row"><label htmlFor="manuscript-content">원고 내용 <small>선택</small></label><span>{content.length.toLocaleString()}자</span></div>
                <textarea id="manuscript-content" onChange={(event) => setContent(event.target.value)} placeholder="여기에 원고를 직접 적어 주세요. 파일로 올리는 경우 비워 두어도 됩니다." value={content} />
              </div>
              <div className="field">
                <label htmlFor="manuscript-file">원고 파일 <small>선택</small></label>
                <label className="file-picker" htmlFor="manuscript-file">
                  <input accept=".hwp,.hwpx,.doc,.docx,.pdf" id="manuscript-file" onChange={selectFile} type="file" />
                  <strong>{file?.name || "원고 파일 선택하기"}</strong>
                  <span>한글·워드·PDF · 최대 30MB</span>
                </label>
              </div>
              {message && <p className="form-message" role="status">{message}</p>}
              <button className="gold-button submit-single-button" disabled={submitting} type="submit">
                {submitting ? "원고 전송 중..." : "원고 제출하기"}
              </button>
            </form>
          </section>
        ) : (
          <section className="form-card completion-card">
            <span className="completion-mark">✓</span>
            <p className="eyebrow dark">SUBMITTED</p>
            <h2>원고가 접수되었습니다</h2>
            <p>아래에서 올린 내용을 미리 확인할 수 있습니다.</p>
            <article className="submission-preview">
              <span>원고 미리보기</span>
              <h3>{title}</h3>
              <p className="record-author">작성자 {name}</p>
              {content && <p className="record-content">{content}</p>}
              {file && <p className="selected-file">첨부 파일: <strong>{file.name}</strong></p>}
            </article>
            <div className="completion-actions">
              <a className="btn btn-primary" href="/records">올라온 기록에서 보기</a>
              <button onClick={reset} type="button">새 원고 올리기</button>
            </div>
          </section>
        )}
      </main>
      <SiteFooter />
    </div>
  );
}
