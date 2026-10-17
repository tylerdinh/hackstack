import { getSupabase, supabaseConfigured } from './supabase'

// Calls the backend, attaching the logged-in user's token so routes using
// get_current_user can tell who they are. Throws on non-2xx responses.
export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  if (supabaseConfigured) {
    const { data } = await getSupabase().auth.getSession()
    if (data.session) headers.set('Authorization', `Bearer ${data.session.access_token}`)
  }
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')

  const res = await fetch(path, { ...init, headers })
  if (!res.ok) throw new Error(`${init.method ?? 'GET'} ${path} failed (${res.status})`)
  return res.status === 204 ? (undefined as T) : res.json()
}
