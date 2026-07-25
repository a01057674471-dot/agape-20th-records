create extension if not exists pgcrypto;

create table if not exists public.submissions (
  id uuid primary key default gen_random_uuid(),
  kind text not null check (kind in ('manuscript', 'photo', 'meeting')),
  title text not null check (char_length(title) between 1 and 120),
  name text not null check (char_length(name) between 1 and 60),
  content text,
  status text not null default '접수' check (status in ('접수', '검토 중', '완료')),
  created_at timestamptz not null default now()
);

create table if not exists public.submission_files (
  id uuid primary key default gen_random_uuid(),
  submission_id uuid not null references public.submissions(id) on delete cascade,
  storage_path text not null unique,
  original_name text not null,
  mime_type text,
  size_bytes bigint not null check (size_bytes >= 0),
  created_at timestamptz not null default now()
);

create index if not exists submissions_kind_created_at_idx
  on public.submissions(kind, created_at desc);
create index if not exists submission_files_submission_id_idx
  on public.submission_files(submission_id);

alter table public.submissions enable row level security;
alter table public.submission_files enable row level security;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'agape-records',
  'agape-records',
  false,
  31457280,
  array[
    'image/jpeg','image/png','image/webp',
    'application/pdf','application/zip',
    'application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-powerpoint','application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/x-hwp','application/haansofthwp','application/octet-stream'
  ]
)
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;
