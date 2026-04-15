# HackStack
The best tech stack for rapid prototype development, designed to be as minimal and easy as possible.

## Tech Stack

Frontend: Vite with React (TypeScript + React Compiler), and Tailwind CSS, described specifically in docs/FRONTEND.md

Backend: FastAPI (Python), described specifically in docs/FRONTEND.md

Storage: Supabase

## Build and Run

Starting from the project root: 
```
npm install 
npm run dev # The frontend/backend (concurrent!)
```

Create a .env file in the /backend folder, populate with your information:
```
SUPABASE_URL=hello.com
SUPABASE_ANON_KEY=1234
SUPABASE_SERVICE_ROLE_KEY=1234
```