"use client";

import { ChangeEvent, FormEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

type SelectedPhoto = { file: File; url: string };
type PhotoForm = {
  event: string;
  year: string;
  name: string;
  phone: string;
  description: string;
};

const SUBMISSIONS_KEY = "agape-photo-submissions";
const emptyForm: PhotoForm = { event: "", year: "", name: "", phone: "", description: "" };

export default function PhotosPage() {
  const [photos, setPhotos] = useState<SelectedPhoto[]>([]);
  const [form, setForm] = useState<PhotoForm>(emptyForm);
  const [message, setMessage] = useState("");

  useEffect(() => () => photos.forEach((photo) => URL.revokeObjectURL(photo.url)), [photos]);

  function selectPhotos(event: ChangeEvent<HTMLInputElement>) {
    const files = Array.from(event.target.files ?? []);
    const valid = files.filter((file) => {
      const isImage = ["image/jpeg", "image/png"].includes(file.type);
      return isImage && file.size <= 20 * 1024 * 1024;
    });
    photos.forEach((photo) => URL.revokeObjectURL(photo.url));
    setPhotos(valid.slice(0, 10).map((file) => ({ file, url: URL.createObjectURL(file) })));
    setMessage(valid.length !== files.length ? "JPG·PNG 형식, 파일당 20MB 이하 사진만 선택했습니다." : "");
  }

  function updateField(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function submitPhotos(event: FormEvent) {
    event.preventDefault();
    if (!form.event.trim() || !form.year.trim() || !form.name.trim() || !form.phone.trim()) {
      setMessage("필수 정보를 모두 입력해 주세요.");
      return;
    }
    if (photos.length === 0) {
      setMessage("사진을 한 장 이상 선택해 주세요.");
      return;
    }

    const submission = {
      ...form,
      id: Date.now(),
      fileNames: photos.map((photo) => photo.file.name),
      count: photos.length,
      status: "접수",
      submittedAt: new Date().toLocaleString("ko-KR"),
    };
    try {
      const stored = window.localStorage.getItem(SUBMISSIONS_KEY);
      const submissions = stored ? JSON.parse(stored) : [];
      window.localStorage.setItem(
        SUBMISSIONS_KEY,
        JSON.stringify([submission, ...submissions]),
      );
    } catch {
      window.localStorage.setItem(SUBMISSIONS_KEY, JSON.stringify([submission]));
    }

    photos.forEach((photo) => URL.revokeObjectURL(photo.url));
    setPhotos([]);
    setForm(emptyForm);
    setMessage("사진 제출 내역을 저장했습니다. 관리자 페이지에서 확인할 수 있습니다.");
  }

  return (
    <div className="site-shell">
      <PageHeader active="photos" />
      <main className="subpage">
        <section className="subpage-heading">
          <p className="kicker">PHOTO ARCHIVE</p>
          <h1>사진 올리기</h1>
          <p>오래된 사진도 선명하지 않은 사진도 괜찮습니다.</p>
        </section>
        <form className="content-card" onSubmit={submitPhotos}>
          <div className="info-banner"><strong>사진은 한 번에 최대 10장</strong><span>JPG 또는 PNG · 파일당 최대 20MB</span></div>
          <div className="form-grid">
            <label className="input-group"><span>행사·주제 <em>필수</em></span><input name="event" onChange={updateField} placeholder="예: 일본 단기선교, 창립예배" value={form.event} /></label>
            <label className="input-group"><span>촬영 연도 <em>필수</em></span><input inputMode="numeric" name="year" onChange={updateField} placeholder="예: 2008" value={form.year} /></label>
            <label className="input-group"><span>올리는 분 성함 <em>필수</em></span><input name="name" onChange={updateField} placeholder="성함을 입력해 주세요" value={form.name} /></label>
            <label className="input-group"><span>연락처 <em>필수</em></span><input inputMode="tel" name="phone" onChange={updateField} placeholder="010-0000-0000" value={form.phone} /></label>
          </div>
          <label className="input-group"><span>사진 설명 <em>선택</em></span><textarea name="description" onChange={updateField} placeholder="사진에 나온 장소, 사람, 기억나는 이야기를 적어 주세요." value={form.description} /></label>
          <label className="upload-zone">
            <input accept="image/jpeg,image/png" multiple onChange={selectPhotos} type="file" />
            <span className="upload-symbol">＋</span>
            <strong>사진 선택하기</strong>
            <small>이 영역을 누르면 컴퓨터나 휴대전화의 사진을 선택할 수 있습니다.</small>
          </label>
          {message && <p className="alert-message">{message}</p>}
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
              <button className="btn btn-primary wide-button" type="submit">사진 제출하기</button>
            </>
          )}
          <p className="save-note">현재는 사진 정보와 파일명이 이 기기에 저장됩니다. 사진 원본의 온라인 보관은 데이터베이스 연결 후 제공됩니다.</p>
        </form>
      </main>
      <SiteFooter />
    </div>
  );
}
