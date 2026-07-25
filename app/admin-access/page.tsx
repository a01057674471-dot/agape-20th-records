"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function AdminAccessPage() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (password.length !== 4) {
      setMessage("숫자 4자리를 입력해 주세요.");
      return;
    }

    setLoading(true);
    const response = await fetch("/api/admin-access", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    setLoading(false);

    if (!response.ok) {
      setMessage("관리자 비밀번호가 맞지 않습니다.");
      setPassword("");
      return;
    }

    const nextPath = new URLSearchParams(window.location.search).get("next");
    router.replace(nextPath?.startsWith("/admin") ? nextPath : "/admin");
    router.refresh();
  }

  return (
    <main className="access-page">
      <section className="access-card">
        <div className="access-brand">
          <span>20</span>
          <div><strong>화성아가페교회</strong><small>20주년 기록실</small></div>
        </div>
        <div className="access-copy">
          <p className="kicker">ADMIN ONLY</p>
          <h1>관리자<br />전용 공간</h1>
          <p>편집부 관리자에게 안내된<br />4자리 비밀번호를 입력해 주세요.</p>
        </div>
        <form onSubmit={submit}>
          <label htmlFor="admin-password">관리자 비밀번호</label>
          <input
            autoComplete="one-time-code"
            autoFocus
            id="admin-password"
            inputMode="numeric"
            maxLength={4}
            onChange={(event) => setPassword(event.target.value.replace(/\D/g, ""))}
            placeholder="● ● ● ●"
            type="password"
            value={password}
          />
          {message && <p className="access-error">{message}</p>}
          <button className="btn btn-primary wide-button" disabled={loading} type="submit">
            {loading ? "확인 중..." : "관리자 페이지 열기"}
          </button>
        </form>
        <small className="access-note">일반 방문자는 관리자 페이지에 들어갈 수 없습니다.</small>
      </section>
      <aside className="access-visual admin-access-visual" aria-hidden="true">
        <span>EDITOR</span>
        <i>—</i>
        <strong>소중한 기록을<br />안전하게 관리합니다</strong>
        <p>원고와 사진을 확인하고<br />진행 상태를 관리하세요.</p>
      </aside>
    </main>
  );
}
