# Frontend

## Imports

`@/` points to `frontend/src/`, so `import Button from '@/components/Button'` works from any depth.

## Source Code Folder (`frontend/src/`)

### `api/`
**Communication Layer.**
- **Purpose:** Centralizes all outgoing network requests via base configurations, clients, and global interceptors. Call the backend with relative `/api/...` URLs: Vite proxies them in development, and the backend serves the frontend itself in production. `client.ts` provides `apiFetch` (adds the login token, throws on errors) and `supabase.ts` provides the Supabase client for login (see [STORAGE.md](STORAGE.md#authentication)).

### `assets/`
**Static Resources.**
- **Purpose:** Storing media files.

### `components/`
**Building UI.**
- **Purpose:** Reusable UI elements across the project that don't belong to a specific area.

### `features/`
**Logic for Specific Things.**
- **Purpose:** Scalable modules organized by capability (e.g., `auth`, `dashboard`), each feature folder should contain its own internal `components/`, `hooks/`, etc.

### `hooks/`
**Stateful Logic.**
- **Purpose:** Global, reusable React hooks (e.g., `useAuth`, `useLocalStorage`).

### `pages/`
**Route Orchestrators.**
- **Purpose:** Entry points for your router, their jobs are to fetch data and pass it to features. Routes are declared in `App.tsx` with [React Router](https://reactrouter.com).

### `stores/`
**Global State Management.**
- **Purpose:** Shared state across different branches (e.g., Zustand or Redux).

### `types/`
**TypeScript Definitions.**
- **Purpose:** Shared interfaces used throughout the entire application.

### `utils/`
**Helper Functions.**
- **Purpose:** Assist functions for things like formatting, validation, and math.
