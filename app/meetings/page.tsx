"use client";

import { ChangeEvent, FormEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";
import { uploadSubmission } from "../lib/uploadSubmission";

type MeetingFile = {
  id: string;
  title: string;
  name: string;
  created_at: string;
  submission_files: {
    id: string;
    original_name: string;
    size_bytes: number;
    downloadUrl: string | null;
  }[];
};

const MAX_FILE_SIZE = 30 * 1024 * 1024;

function readableSize(bytes: number) {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))}KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)}MB`;
}

export default function MeetingsPage() {
  const fileInput = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<MeetingFile[]>([]);
  const [query, setQuery] = useState("");
  const [title, setTitle] = useState("");
  const [name, setName] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const loadFiles = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/submissions?kind=meeting", { cache: "no-store" });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message);
      setFiles(data.submissions);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "자료를 불러오지 못했습니다.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadFiles(); }, [loadFiles]);

  const filtered = useMemo(() => {
    const keyword = query.trim().toLowerCase();
    if (!keyword) return files;
    return files.filter((file) =>
      [file.title, file.name, ...file.submission_files.map((item) => item.original_name)]
        .some((value) => value.toLowerCase().includes(keyword)),
    );
  }, [files, query]);

  function chooseFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;
    if (file && file.size > MAX_FILE_SIZE) {
      setSelectedFile(null);
      setMessage("회의 자료는 최대 30MB까지 올릴 수 있습니다.");
      event.target.value = "";
      return;
    }
    setSelectedFile(file);
    setMessage("");
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!title.trim() || !name.trim() || !selectedFile) {
      setMessage("제목과 이름을 입력하고 파일을 선택해 주세요.");
      return;
    }

    setSubmitting(true);
    setMessage("회의 자료를 안전하게 전송하고 있습니다.");
    try {
      await uploadSubmission({
        kind: "meeting",
        title: title.trim(),
        name: name.trim(),
        files: [selectedFile],
      });
      setTitle("");
      setName("");
      setSelectedFile(null);
      if (fileInput.current) fileInput.current.value = "";
      setMessage("회의 자료가 등록되었습니다.");
      await loadFiles();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "회의 자료를 등록하지 못했습니다.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="site-shell">
      <PageHeader active="meetings" />
      <main className="subpage">
        <section className="subpage-heading">
          <p className="kicker">EDITORIAL FILES</p>
          <h1>회의 자료</h1>
          <p>제목과 이름만 적고 회의 자료를 올려 주세요.</p>
        </section>

        <form className="content-card meeting-upload-card simple-submit-card" onSubmit={submit}>
          <div className="panel-heading"><h2>회의 자료 올리기</h2><span>누구나 등록 가능</span></div>
          <div className="form-grid">
            <label className="input-group">
              <span>자료 제목 <em>필수</em></span>
              <input onChange={(event) => setTitle(event.target.value)} placeholder="예: 7월 편집부 회의록" value={title} />
            </label>
            <label className="input-group">
              <span>이름 <em>필수</em></span>
              <input onChange={(event) => setName(event.target.value)} placeholder="자료 올리는 분 이름" value={name} />
            </label>
          </div>
          <label className="input-group">
            <span>파일 선택 <em>필수</em></span>
            <input accept=".hwp,.hwpx,.doc,.docx,.pdf,.ppt,.pptx,.xls,.xlsx,.jpg,.jpeg,.png,.zip" onChange={chooseFile} ref={fileInput} type="file" />
          </label>
          {selectedFile && <p className="selected-file">선택한 파일: <strong>{selectedFile.name}</strong> · {readableSize(selectedFile.size)}</p>}
          {message && <p className="alert-message" role="status">{message}</p>}
          <button className="btn btn-primary wide-button" disabled={submitting} type="submit">
            {submitting ? "자료 전송 중..." : "회의 자료 등록하기"}
          </button>
          <p className="save-note">한글·워드·PDF·PPT·엑셀·사진·ZIP · 최대 30MB</p>
        </form>

        <section className="content-card meeting-list-card">
          <div className="panel-heading"><h2>등록된 자료</h2><span>{files.length}개</span></div>
          <label className="search-box"><span>자료 검색</span><input onChange={(event) => setQuery(event.target.value)} placeholder="제목이나 이름으로 검색" value={query} /></label>
          <div className="file-list">
            {loading && <p className="empty-state">자료를 불러오는 중입니다.</p>}
            {!loading && filtered.map((item) => {
              const file = item.submission_files[0];
              return (
                <article className="file-row uploaded-file-row" key={item.id}>
                  <span className="file-type">자료</span>
                  <div>
                    <h2>{item.title}</h2>
                    <p>{item.name} · {new Date(item.created_at).toLocaleString("ko-KR")}</p>
                    {file && <small>{file.original_name} · {readableSize(file.size_bytes)}</small>}
                  </div>
                  <div className="file-actions">
                    {file?.downloadUrl ? <a className="download-button" href={file.downloadUrl}>내려받기</a> : <span>파일 준비 중</span>}
                  </div>
                </article>
              );
            })}
            {!loading && filtered.length === 0 && <p className="empty-state">등록된 자료가 없습니다.</p>}
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
