"use client";

import { ChangeEvent, FormEvent, useEffect, useMemo, useRef, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

type MeetingFile = {
  id: number;
  title: string;
  type: string;
  uploader: string;
  description: string;
  fileName: string;
  fileSize: number;
  fileType: string;
  uploadedAt: string;
  file: Blob;
};

const DB_NAME = "agape-records";
const STORE_NAME = "meeting-files";
const MAX_FILE_SIZE = 30 * 1024 * 1024;

function openDatabase() {
  return new Promise<IDBDatabase>((resolve, reject) => {
    const request = window.indexedDB.open(DB_NAME, 1);
    request.onupgradeneeded = () => {
      const database = request.result;
      if (!database.objectStoreNames.contains(STORE_NAME)) {
        database.createObjectStore(STORE_NAME, { keyPath: "id" });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function readFiles() {
  const database = await openDatabase();
  return new Promise<MeetingFile[]>((resolve, reject) => {
    const request = database.transaction(STORE_NAME, "readonly").objectStore(STORE_NAME).getAll();
    request.onsuccess = () => resolve((request.result as MeetingFile[]).sort((a, b) => b.id - a.id));
    request.onerror = () => reject(request.error);
  }).finally(() => database.close());
}

async function saveFile(item: MeetingFile) {
  const database = await openDatabase();
  return new Promise<void>((resolve, reject) => {
    const request = database.transaction(STORE_NAME, "readwrite").objectStore(STORE_NAME).put(item);
    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  }).finally(() => database.close());
}

async function removeFile(id: number) {
  const database = await openDatabase();
  return new Promise<void>((resolve, reject) => {
    const request = database.transaction(STORE_NAME, "readwrite").objectStore(STORE_NAME).delete(id);
    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  }).finally(() => database.close());
}

function readableSize(bytes: number) {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))}KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)}MB`;
}

export default function MeetingsPage() {
  const fileInput = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<MeetingFile[]>([]);
  const [query, setQuery] = useState("");
  const [title, setTitle] = useState("");
  const [type, setType] = useState("회의");
  const [uploader, setUploader] = useState("");
  const [description, setDescription] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    readFiles()
      .then(setFiles)
      .catch(() => setMessage("이 브라우저에서는 파일 저장 기능을 사용할 수 없습니다."))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const keyword = query.trim().toLowerCase();
    if (!keyword) return files;
    return files.filter((file) =>
      [file.title, file.type, file.uploader, file.fileName].some((value) =>
        value.toLowerCase().includes(keyword),
      ),
    );
  }, [files, query]);

  function chooseFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;
    if (file && file.size > MAX_FILE_SIZE) {
      setSelectedFile(null);
      setMessage("파일은 최대 30MB까지 올릴 수 있습니다.");
      event.target.value = "";
      return;
    }
    setSelectedFile(file);
    setMessage("");
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!title.trim() || !uploader.trim() || !selectedFile) {
      setMessage("자료 제목, 올린 분 성함, 파일을 모두 입력해 주세요.");
      return;
    }

    const item: MeetingFile = {
      id: Date.now(),
      title: title.trim(),
      type,
      uploader: uploader.trim(),
      description: description.trim(),
      fileName: selectedFile.name,
      fileSize: selectedFile.size,
      fileType: selectedFile.type,
      uploadedAt: new Date().toLocaleString("ko-KR"),
      file: selectedFile,
    };

    try {
      await saveFile(item);
      setFiles((current) => [item, ...current]);
      setTitle("");
      setType("회의");
      setUploader("");
      setDescription("");
      setSelectedFile(null);
      if (fileInput.current) fileInput.current.value = "";
      setMessage("회의 자료를 저장했습니다. 아래 목록에서 바로 내려받을 수 있습니다.");
    } catch {
      setMessage("파일을 저장하지 못했습니다. 저장 공간을 확인한 뒤 다시 시도해 주세요.");
    }
  }

  function download(item: MeetingFile) {
    const url = URL.createObjectURL(item.file);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = item.fileName;
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function deleteItem(item: MeetingFile) {
    if (!window.confirm(`“${item.title}” 자료를 삭제할까요?`)) return;
    await removeFile(item.id);
    setFiles((current) => current.filter((file) => file.id !== item.id));
  }

  return (
    <div className="site-shell">
      <PageHeader active="meetings" />
      <main className="subpage">
        <section className="subpage-heading">
          <p className="kicker">EDITORIAL FILES</p>
          <h1>회의 자료</h1>
          <p>누구나 회의 자료를 올리고 바로 내려받을 수 있습니다.</p>
        </section>

        <form className="content-card meeting-upload-card" onSubmit={submit}>
          <div className="panel-heading">
            <div><p className="eyebrow dark">QUICK UPLOAD</p><h2>회의 자료 올리기</h2></div>
            <span>로그인 없이 등록</span>
          </div>
          <div className="form-grid">
            <label className="input-group">
              <span>자료 제목 <em>필수</em></span>
              <input onChange={(event) => setTitle(event.target.value)} placeholder="예: 7월 편집부 회의록" value={title} />
            </label>
            <label className="input-group">
              <span>자료 종류 <em>필수</em></span>
              <select onChange={(event) => setType(event.target.value)} value={type}>
                <option>회의</option><option>안내</option><option>원고</option><option>사진</option><option>기타</option>
              </select>
            </label>
            <label className="input-group">
              <span>올린 분 성함 <em>필수</em></span>
              <input onChange={(event) => setUploader(event.target.value)} placeholder="성함을 입력해 주세요" value={uploader} />
            </label>
            <label className="input-group">
              <span>파일 선택 <em>필수</em></span>
              <input accept=".hwp,.hwpx,.doc,.docx,.pdf,.ppt,.pptx,.xls,.xlsx,.jpg,.jpeg,.png,.zip" onChange={chooseFile} ref={fileInput} type="file" />
            </label>
          </div>
          <label className="input-group">
            <span>간단한 설명 <small>선택</small></span>
            <textarea onChange={(event) => setDescription(event.target.value)} placeholder="자료에 대한 설명이나 확인할 내용을 적어 주세요." value={description} />
          </label>
          {selectedFile && <p className="selected-file">선택한 파일: <strong>{selectedFile.name}</strong> · {readableSize(selectedFile.size)}</p>}
          {message && <p className="alert-message" role="status">{message}</p>}
          <button className="btn btn-primary wide-button" type="submit">회의 자료 등록하기</button>
          <p className="save-note">파일당 최대 30MB · 현재는 자료를 올린 기기의 브라우저에 저장됩니다.</p>
        </form>

        <section className="content-card meeting-list-card">
          <div className="panel-heading"><h2>등록된 자료</h2><span>{files.length}개</span></div>
          <label className="search-box"><span>자료 검색</span><input onChange={(event) => setQuery(event.target.value)} placeholder="제목, 종류, 이름으로 검색" value={query} /></label>
          <div className="file-list">
            {loading && <p className="empty-state">자료를 불러오는 중입니다.</p>}
            {!loading && filtered.map((file) => (
              <article className="file-row uploaded-file-row" key={file.id}>
                <span className="file-type">{file.type}</span>
                <div>
                  <h2>{file.title}</h2>
                  <p>{file.uploader} · {file.uploadedAt} · {file.fileName} ({readableSize(file.fileSize)})</p>
                  {file.description && <small>{file.description}</small>}
                </div>
                <div className="file-actions">
                  <button className="download-button" onClick={() => download(file)} type="button">내려받기</button>
                  <button className="delete-button" onClick={() => deleteItem(file)} type="button">삭제</button>
                </div>
              </article>
            ))}
            {!loading && filtered.length === 0 && <p className="empty-state">등록된 자료가 없습니다.</p>}
          </div>
          <p className="helper-note">여러 사람의 휴대전화와 컴퓨터에서 같은 자료를 함께 보려면 다음 단계에서 온라인 저장소 연결이 필요합니다.</p>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
