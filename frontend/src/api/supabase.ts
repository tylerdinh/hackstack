import { createClient, type SupabaseClient } from '@supabase/supabase-js'

const url = import.meta.env.VITE_SUPABASE_URL
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// False until frontend/.env.local is filled in, so apps without login still run
export const supabaseConfigured = Boolean(url && anonKey)

let client: SupabaseClient | null = null

// Created once and reused. Use it for login, e.g. getSupabase().auth.signInWithPassword(...)
export function getSupabase(): SupabaseClient {
  if (!supabaseConfigured) {
    throw new Error('Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in frontend/.env.local')
  }
  client ??= createClient(url, anonKey)
  return client
}
