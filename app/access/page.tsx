"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function AccessPage() {
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
    const response = await fetch("/api/access", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    setLoading(false);
    if (!response.ok) {
      setMessage("비밀번호가 맞지 않습니다. 다시 확인해 주세요.");
      setPassword("");
      return;
    }
    const nextPath = new URLSearchParams(window.location.search).get("next");
    router.replace(nextPath || "/");
    router.refresh();
  }

  return (
    <main className="access-page">
      <section className="access-card">
        <div className="access-brand"><span>20</span><div><strong>화성아가페교회</strong><small>20주년 기록실</small></div></div>
        <div className="access-copy">
          <p className="kicker">PRIVATE ARCHIVE</p>
          <h1>기록실에<br />들어오셨습니다</h1>
          <p>편집부에서 안내받은<br />4자리 비밀번호를 입력해 주세요.</p>
        </div>
        <form onSubmit={submit}>
          <label htmlFor="site-password">접속 비밀번호</label>
          <input
            autoComplete="one-time-code"
            autoFocus
            id="site-password"
            inputMode="numeric"
            maxLength={4}
            onChange={(event) => setPassword(event.target.value.replace(/\D/g, ""))}
            placeholder="● ● ● ●"
            type="password"
            value={password}
          />
          {message && <p className="access-error">{message}</p>}
          <button className="btn btn-primary wide-button" disabled={loading} type="submit">
            {loading ? "확인 중..." : "기록실 들어가기"}
          </button>
        </form>
        <small className="access-note">비밀번호는 편집부에 문의해 주세요.</small>
      </section>
      <aside className="access-visual" aria-hidden="true">
        <span>2006</span><i>—</i><span>2026</span>
        <strong>함께 걸어온<br />스무 해</strong>
        <p>우리의 기억이<br />교회의 역사가 됩니다.</p>
      </aside>
    </main>
  );
}
