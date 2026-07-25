"use client";

import { ChangeEvent, FormEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";
import { compressImage } from "../lib/compressImage";
import { uploadSubmission } from "../lib/uploadSubmission";

type SelectedPhoto = { file: File; url: string };
const MAX_FILE_SIZE = 15 * 1024 * 1024;

export default function PhotosPage() {
  const [title, setTitle] = useState("");
  const [name, setName] = useState("");
  const [photos, setPhotos] = useState<SelectedPhoto[]>([]);
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);

  useEffect(() => () => photos.forEach((photo) => URL.revokeObjectURL(photo.url)), [photos]);

  function selectPhotos(event: ChangeEvent<HTMLInputElement>) {
    const files = Array.from(event.target.files ?? []);
    const valid = files
      .filter((file) => ["image/jpeg", "image/png", "image/webp"].includes(file.type) && file.size <= MAX_FILE_SIZE)
      .slice(0, 10);
    photos.forEach((photo) => URL.revokeObjectURL(photo.url));
    setPhotos(valid.map((file) => ({ file, url: URL.createObjectURL(file) })));
    if (valid.length !== files.length) {
      setMessage("JPG·PNG·WEBP 형식, 파일당 15MB 이하 사진만 최대 10장 선택했습니다.");
    } else {
      setMessage("");
    }
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!title.trim() || !name.trim()) {
      setMessage("제목과 이름을 입력해 주세요.");
      return;
    }
    if (photos.length === 0) {
      setMessage("사진을 한 장 이상 선택해 주세요.");
      return;
    }

    setSubmitting(true);
    setMessage("사진 용량을 줄이고 안전하게 전송하고 있습니다. 화면을 닫지 말아 주세요.");
    try {
      const optimized = [];
      for (const photo of photos) optimized.push(await compressImage(photo.file));
      await uploadSubmission({
        kind: "photo",
        title: title.trim(),
        name: name.trim(),
        files: optimized,
      });
      setDone(true);
      setMessage("");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "사진을 접수하지 못했습니다.");
    } finally {
      setSubmitting(false);
    }
  }

  function reset() {
    photos.forEach((photo) => URL.revokeObjectURL(photo.url));
    setTitle("");
    setName("");
    setPhotos([]);
    setDone(false);
  }

  return (
    <div className="site-shell">
      <PageHeader active="photos" />
      <main className="subpage">
        <section className="subpage-heading">
          <p className="kicker">PHOTO ARCHIVE</p>
          <h1>사진 올리기</h1>
          <p>제목과 이름만 적고 사진을 선택해 주세요.</p>
        </section>

        {!done ? (
          <form className="content-card simple-submit-card" onSubmit={submit}>
            <div className="info-banner"><strong>한 번에 최대 10장</strong><span>JPG·PNG·WEBP · 사진당 최대 15MB · 큰 사진 자동 축소</span></div>
            <div className="form-grid">
              <label className="input-group">
                <span>사진 제목 <em>필수</em></span>
                <input onChange={(event) => setTitle(event.target.value)} placeholder="예: 2012년 일본 단기선교" value={title} />
              </label>
              <label className="input-group">
                <span>이름 <em>필수</em></span>
                <input onChange={(event) => setName(event.target.value)} placeholder="사진 올리는 분 이름" value={name} />
              </label>
            </div>
            <label className="upload-zone">
              <input accept="image/jpeg,image/png,image/webp" multiple onChange={selectPhotos} type="file" />
              <span className="upload-symbol">＋</span>
              <strong>사진 선택하기</strong>
              <small>휴대전화 사진첩이나 컴퓨터에서 사진을 선택할 수 있습니다.</small>
            </label>
            {photos.length > 0 && (
              <>
                <div className="selected-head"><strong>선택한 사진 {photos.length}장</strong><button onClick={() => setPhotos([])} type="button">전체 지우기</button></div>
                <div className="photo-preview-grid">
                  {photos.map((photo, index) => (
                    <div className="photo-preview" key={`${photo.file.name}-${index}`}>
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img alt={`선택한 사진 ${index + 1}`} src={photo.url} />
                      <span>{photo.file.name}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
            {message && <p className="alert-message" role="status">{message}</p>}
            <button className="btn btn-primary wide-button" disabled={submitting} type="submit">
              {submitting ? "사진 전송 중..." : "사진 제출하기"}
            </button>
          </form>
        ) : (
          <section className="content-card completion-card">
            <span className="completion-mark">✓</span>
            <p className="eyebrow dark">SUBMITTED</p>
            <h2>사진이 접수되었습니다</h2>
            <p>아래에서 올린 사진을 미리 확인할 수 있습니다.</p>
            <article className="submission-preview">
              <span>사진 미리보기</span>
              <h3>{title}</h3>
              <p className="record-author">작성자 {name}</p>
              <div className="photo-preview-grid">
                {photos.map((photo, index) => (
                  <div className="photo-preview" key={`${photo.file.name}-${index}`}>
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img alt={`올린 사진 ${index + 1}`} src={photo.url} />
                  </div>
                ))}
              </div>
            </article>
            <div className="completion-actions">
              <a className="btn btn-primary" href="/records">올라온 기록에서 보기</a>
              <button onClick={reset} type="button">새 사진 올리기</button>
            </div>
          </section>
        )}
      </main>
      <SiteFooter />
    </div>
  );
}
