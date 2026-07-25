"use client";

import { ChangeEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

type SelectedPhoto = { file: File; url: string };

export default function PhotosPage() {
  const [photos, setPhotos] = useState<SelectedPhoto[]>([]);
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

  return (
    <div className="site-shell">
      <PageHeader active="photos" />
      <main className="subpage">
        <section className="subpage-heading">
          <p className="kicker">PHOTO ARCHIVE</p>
          <h1>사진 올리기</h1>
          <p>오래된 사진도 선명하지 않은 사진도 괜찮습니다.</p>
        </section>
        <section className="content-card">
          <div className="info-banner"><strong>사진은 한 번에 최대 10장</strong><span>JPG 또는 PNG · 파일당 최대 20MB</span></div>
          <div className="form-grid">
            <label className="input-group"><span>행사·주제 <em>필수</em></span><input placeholder="예: 일본 단기선교, 창립예배" /></label>
            <label className="input-group"><span>촬영 연도 <em>필수</em></span><input inputMode="numeric" placeholder="예: 2008" /></label>
            <label className="input-group"><span>올리는 분 성함 <em>필수</em></span><input placeholder="성함을 입력해 주세요" /></label>
            <label className="input-group"><span>연락처 <em>필수</em></span><input inputMode="tel" placeholder="010-0000-0000" /></label>
          </div>
          <label className="input-group"><span>사진 설명 <em>선택</em></span><textarea placeholder="사진에 나온 장소, 사람, 기억나는 이야기를 적어 주세요." /></label>
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
              <button className="btn btn-primary wide-button" onClick={() => setMessage("사진 선택과 입력 화면이 정상 작동합니다. 실제 서버 제출은 관리자 데이터 연동 단계에서 활성화됩니다.")} type="button">선택 내용 확인</button>
            </>
          )}
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
