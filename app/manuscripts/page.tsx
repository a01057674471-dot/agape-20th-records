"use client";

import { ChangeEvent, FormEvent, useEffect, useMemo, useState } from "react";
import PageHeader from "../components/PageHeader";
import SiteFooter from "../components/SiteFooter";

const STORAGE_KEY = "agape-manuscript-draft";
const THIRTY_DAYS = 30 * 24 * 60 * 60 * 1000;

type ManuscriptDraft = {
  category: string;
  title: string;
  author: string;
  phone: string;
  content: string;
  savedAt?: number;
};

const emptyDraft: ManuscriptDraft = {
  category: "",
  title: "",
  author: "",
  phone: "",
  content: "",
};

export default function ManuscriptPage() {
  const [draft, setDraft] = useState<ManuscriptDraft>(emptyDraft);
  const [step, setStep] = useState<"write" | "preview" | "done">("write");
  const [message, setMessage] = useState("");
  const [fileName, setFileName] = useState("");

  useEffect(() => {
    const rawDraft = window.localStorage.getItem(STORAGE_KEY);
    if (!rawDraft) return;

    try {
      const stored = JSON.parse(rawDraft) as ManuscriptDraft;
      if (stored.savedAt && Date.now() - stored.savedAt < THIRTY_DAYS) {
        setDraft(stored);
        setMessage("이전에 임시저장한 원고를 불러왔습니다.");
      } else {
        window.localStorage.removeItem(STORAGE_KEY);
      }
    } catch {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  const characterCount = useMemo(() => draft.content.length, [draft.content]);
  const isComplete = Boolean(
    draft.category && draft.title.trim() && draft.author.trim() &&
    draft.phone.trim() && draft.content.trim(),
  );

  function updateField(
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) {
    const { name, value } = event.target;
    setDraft((current) => ({ ...current, [name]: value }));
  }

  function saveDraft() {
    const nextDraft = { ...draft, savedAt: Date.now() };
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextDraft));
    setDraft(nextDraft);
    setMessage("임시저장했습니다. 이 기기에서 30일간 보관됩니다.");
  }

  function showPreview(event: FormEvent) {
    event.preventDefault();
    if (!isComplete) {
      setMessage("필수 항목을 모두 입력해 주세요.");
      return;
    }
    setMessage("");
    setStep("preview");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function confirmSubmission() {
    setStep("done");
    window.localStorage.removeItem(STORAGE_KEY);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="site-shell">
      <PageHeader active="manuscripts" />
      <main className="form-page">
        <section className="page-intro">
          <p className="eyebrow">SHARE YOUR STORY</p>
          <h1>원고 작성</h1>
          <p>당신의 이야기가 화성아가페교회의 소중한 역사가 됩니다.</p>
        </section>

        <div className="stepper" aria-label="원고 제출 단계">
          <span className={step === "write" ? "current" : "complete"}>1. 작성</span>
          <i />
          <span className={step === "preview" ? "current" : step === "done" ? "complete" : ""}>
            2. 미리보기
          </span>
          <i />
          <span className={step === "done" ? "current" : ""}>3. 제출 완료</span>
        </div>

        {step === "write" && (
          <section className="form-card">
            <div className="guide-box">
              <strong>작성 전 확인해 주세요</strong>
              <p>
                문장을 완벽하게 다듬지 않아도 괜찮습니다. 기억나는 장면과 마음을
                편안하게 적어 주세요. 편집부가 원문의 뜻을 지키며 정리합니다.
              </p>
            </div>

            <form onSubmit={showPreview}>
              <div className="field">
                <label htmlFor="category">원고 분류 <em>필수</em></label>
                <select
                  id="category"
                  name="category"
                  onChange={updateField}
                  value={draft.category}
                  required
                >
                  <option value="">분류를 선택해 주세요</option>
                  <option>프롤로그·인사말</option>
                  <option>선교지 이야기</option>
                  <option>구역 이야기</option>
                  <option>선교사님의 편지</option>
                  <option>교회 역사·간증</option>
                  <option>기타 기록</option>
                </select>
              </div>

              <div className="field">
                <label htmlFor="title">제목 <em>필수</em></label>
                <input
                  id="title"
                  name="title"
                  onChange={updateField}
                  placeholder="원고 제목을 입력해 주세요"
                  value={draft.title}
                  required
                />
              </div>

              <div className="field-row">
                <div className="field">
                  <label htmlFor="author">작성자 이름 <em>필수</em></label>
                  <input
                    id="author"
                    name="author"
                    onChange={updateField}
                    placeholder="이름"
                    value={draft.author}
                    required
                  />
                </div>
                <div className="field">
                  <label htmlFor="phone">연락처 <em>필수</em></label>
                  <input
                    id="phone"
                    name="phone"
                    inputMode="tel"
                    onChange={updateField}
                    placeholder="010-0000-0000"
                    value={draft.phone}
                    required
                  />
                </div>
              </div>

              <div className="field">
                <div className="label-row">
                  <label htmlFor="content">글 내용 <em>필수</em></label>
                  <span>{characterCount.toLocaleString()}자</span>
                </div>
                <textarea
                  id="content"
                  name="content"
                  onChange={updateField}
                  placeholder={"기억에 남는 장면부터 천천히 적어 주세요.\n\n언제, 어디서, 누구와 함께했는지 적으면 이야기가 더 생생해집니다."}
                  value={draft.content}
                  required
                />
              </div>

              <div className="field">
                <label htmlFor="attachment">파일 첨부 <small>선택</small></label>
                <label className="file-picker" htmlFor="attachment">
                  <input
                    id="attachment"
                    type="file"
                    accept=".hwp,.hwpx,.doc,.docx,.pdf"
                    onChange={(event) => setFileName(event.target.files?.[0]?.name ?? "")}
                  />
                  <strong>{fileName || "파일 선택"}</strong>
                  <span>한글·워드·PDF 파일을 첨부할 수 있습니다.</span>
                </label>
              </div>

              {message && <p className="form-message" role="status">{message}</p>}

              <div className="form-actions">
                <button className="outline-button" onClick={saveDraft} type="button">
                  임시저장
                </button>
                <button className="gold-button" type="submit">다음 단계</button>
              </div>
              <p className="save-note">임시저장 내용은 현재 기기에서 30일간 보관됩니다.</p>
            </form>
          </section>
        )}

        {step === "preview" && (
          <section className="form-card preview-card">
            <p className="eyebrow dark">PREVIEW</p>
            <h2>{draft.title}</h2>
            <dl>
              <div><dt>분류</dt><dd>{draft.category}</dd></div>
              <div><dt>작성자</dt><dd>{draft.author}</dd></div>
              <div><dt>연락처</dt><dd>{draft.phone}</dd></div>
              {fileName && <div><dt>첨부 파일</dt><dd>{fileName}</dd></div>}
            </dl>
            <article>{draft.content}</article>
            <div className="form-actions">
              <button className="outline-button" onClick={() => setStep("write")} type="button">
                수정하기
              </button>
              <button className="gold-button" onClick={confirmSubmission} type="button">
                제출 내용 확인
              </button>
            </div>
            <p className="save-note">
              현재 단계에서는 제출 화면만 확인됩니다. 실제 접수는 데이터 연결 후 활성화됩니다.
            </p>
          </section>
        )}

        {step === "done" && (
          <section className="form-card completion-card">
            <span className="completion-mark">✓</span>
            <p className="eyebrow dark">THANK YOU</p>
            <h2>원고 내용을 확인했습니다</h2>
            <p>
              실제 온라인 접수 기능은 데이터 연동 단계에서 활성화됩니다.
              <br />작성 흐름과 화면은 지금부터 확인할 수 있습니다.
            </p>
            <button className="gold-button" onClick={() => {
              setDraft(emptyDraft);
              setFileName("");
              setStep("write");
            }} type="button">
              새 원고 작성하기
            </button>
          </section>
        )}
      </main>
      <SiteFooter />
    </div>
  );
}
