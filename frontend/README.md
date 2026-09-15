# CareerMate Frontend

This directory contains the React + TypeScript frontend for the CareerMate platform.

## Overview

The frontend is the user-facing application for:

- authentication and session management
- profile creation and editing
- resume upload and review
- job browsing and matching
- ATS and resume optimization workflows

## Stack

- React 19
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Lucide React icons

## Prerequisites

- Node.js 18+
- npm
- The backend running locally on port 8000

## Setup

From the `frontend` folder:

```bash
npm install
```

## Run in development mode

```bash
npm run dev
```

The app should open on:

- http://localhost:5173

## Production build

```bash
npm run build
```

To preview the production build:

```bash
npm run preview
```

## Linting

```bash
npm run lint
```

## Notes

- The project uses Vite and the default React plugin setup.
- The backend API is expected to be available at `http://localhost:8000`.
- If needed, update the API base URL in the frontend client configuration or service layer.

## Typical workflow

1. Start PostgreSQL from the project root with Docker.
2. Start the backend API from `backend/`.
3. Run the frontend from `frontend/`.
4. Register or sign in and use the app.

---

For root setup instructions, see [../README.md](../README.md).
For backend setup instructions, see [../backend/README.md](../backend/README.md).
