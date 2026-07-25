type PageHeaderProps = {
  active: "home" | "manuscripts" | "photos" | "meetings" | "progress";
};

const links = [
  { key: "home", label: "홈", href: "/" },
  { key: "manuscripts", label: "원고 작성", href: "/manuscripts" },
  { key: "photos", label: "사진 업로드", href: "/photos" },
  { key: "meetings", label: "회의 자료", href: "/meetings" },
  { key: "progress", label: "진행 현황", href: "/progress" },
] as const;

const mobileLinks = [
  ...links,
  { key: "admin", label: "관리자", href: "/admin" },
] as const;

export default function PageHeader({ active }: PageHeaderProps) {
  return (
    <>
      <header className="topbar">
        <a className="brand" href="/" aria-label="기록실 홈">
          <span className="brand-mark" aria-hidden="true">20</span>
          <span>
            <strong>화성아가페교회 20주년 기록실</strong>
            <small>함께 걸어온 스무 해</small>
          </span>
        </a>
        <nav className="desktop-nav" aria-label="주요 메뉴">
          {links.map((link) => (
            <a
              className={active === link.key ? "active" : undefined}
              href={link.href}
              key={link.key}
            >
              {link.label}
            </a>
          ))}
        </nav>
        <a className="admin-link" href="/admin">관리자</a>
      </header>
      <nav className="mobile-nav" aria-label="모바일 주요 메뉴">
        {mobileLinks.map((link) => (
          <a
            className={active === link.key ? "active" : undefined}
            href={link.href}
            key={link.key}
          >
            {link.key === "manuscripts" ? "원고" :
              link.key === "photos" ? "사진" :
              link.key === "meetings" ? "자료" :
              link.key === "progress" ? "현황" :
              link.key === "admin" ? "관리자" : "홈"}
          </a>
        ))}
      </nav>
    </>
  );
}
