-- Supabase Database Schema for LeetCode Recommender System
-- Target Table: users

-- Create the users table
CREATE TABLE IF NOT EXISTS public.users (
    username TEXT PRIMARY KEY,
    last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    solved_total INTEGER NOT NULL DEFAULT 0,
    solved_easy INTEGER NOT NULL DEFAULT 0,
    solved_medium INTEGER NOT NULL DEFAULT 0,
    solved_hard INTEGER NOT NULL DEFAULT 0,
    total_easy INTEGER NOT NULL DEFAULT 0,
    total_medium INTEGER NOT NULL DEFAULT 0,
    total_hard INTEGER NOT NULL DEFAULT 0,
    weakest_tags TEXT[] NOT NULL DEFAULT '{}',
    strongest_tags TEXT[] NOT NULL DEFAULT '{}',
    top_recommendation TEXT
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Create Policies

-- 1. Allow service_role key to do everything (enabled by default in Supabase)
-- (No explicit policy needed for service_role as it bypasses RLS)

-- 2. Allow read-only access to anonymous users (optional, if frontend queries Supabase directly)
CREATE POLICY "Allow public read access" 
ON public.users 
FOR SELECT 
TO anon, authenticated 
USING (true);

-- 3. Allow anonymous insert/update (upsert) only if using the correct service_role key.
-- Note: If you only have the 'anon' key configured in your API, you must grant write access to anon:
-- WARNING: Only enable the policy below if your backend is authenticated or you are comfortable 
-- with anonymous writes. In a secure production environment, you should use the service_role key 
-- which bypasses RLS automatically and keep this table write-protected from the public internet.

-- CREATE POLICY "Allow anon writes" 
-- ON public.users 
-- FOR ALL 
-- TO anon 
-- USING (true) 
-- WITH CHECK (true);
