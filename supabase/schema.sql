-- Run this in Supabase → SQL Editor → New query → Run.

-- Profiles (first/last name shown in the UI)
create table if not exists public.profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  first_name text,
  last_name text,
  updated_at timestamptz not null default now()
);
alter table public.profiles enable row level security;
drop policy if exists "profiles read own" on public.profiles;
create policy "profiles read own" on public.profiles for select using (auth.uid() = user_id);
drop policy if exists "profiles insert own" on public.profiles;
create policy "profiles insert own" on public.profiles for insert with check (auth.uid() = user_id);
drop policy if exists "profiles update own" on public.profiles;
create policy "profiles update own" on public.profiles for update using (auth.uid() = user_id);

-- Saved diagnosis runs
create table if not exists public.diagnosis_runs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  disease text not null,
  inputs jsonb not null,
  result jsonb not null,
  created_at timestamptz not null default now()
);
alter table public.diagnosis_runs enable row level security;
drop policy if exists "users read own runs" on public.diagnosis_runs;
create policy "users read own runs" on public.diagnosis_runs for select using (auth.uid() = user_id);
drop policy if exists "users insert own runs" on public.diagnosis_runs;
create policy "users insert own runs" on public.diagnosis_runs for insert with check (auth.uid() = user_id);
drop policy if exists "users delete own runs" on public.diagnosis_runs;
create policy "users delete own runs" on public.diagnosis_runs for delete using (auth.uid() = user_id);

-- Chat messages
create table if not exists public.chat_messages (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null check (role in ('user','assistant')),
  content text not null,
  created_at timestamptz not null default now()
);
alter table public.chat_messages enable row level security;
drop policy if exists "users read own chats" on public.chat_messages;
create policy "users read own chats" on public.chat_messages for select using (auth.uid() = user_id);
drop policy if exists "users insert own chats" on public.chat_messages;
create policy "users insert own chats" on public.chat_messages for insert with check (auth.uid() = user_id);

-- Feedback
create table if not exists public.feedback (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  rating text,
  comments text,
  created_at timestamptz not null default now()
);
alter table public.feedback enable row level security;
drop policy if exists "feedback insert any auth" on public.feedback;
create policy "feedback insert any auth" on public.feedback for insert with check (auth.uid() is not null);
drop policy if exists "feedback read own" on public.feedback;
create policy "feedback read own" on public.feedback for select using (auth.uid() = user_id);
