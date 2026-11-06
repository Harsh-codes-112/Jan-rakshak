# Deploying JAN-RAKSHAK on Vercel

This repository is a monorepo. Deploy the frontend and API as **two Vercel projects** connected to this repository; Docker Compose and the Dockerfiles are for local/container hosting and are not used by Vercel.

## Frontend Vercel project

- Import the repository and set **Root Directory** to `frontend`.
- Framework preset: Next.js (auto-detected); use the default build and output settings.
- Add `BACKEND_URL` for Production, Preview, and Development as appropriate. Set it to the deployed backend origin, without a trailing slash (for example `https://your-api.vercel.app`). The frontend rewrite proxies `/api/*` to this backend, avoiding browser CORS configuration.

## Backend Vercel project

- Import the same repository as a second project and set **Root Directory** to `backend`.
- Framework preset: FastAPI/Python (auto-detected). The function entrypoint is `api/index.py`; it exports the FastAPI app defined in `main.py`. Dependencies are in `requirements.txt`.
- Configure `DATABASE_URL` to a managed PostgreSQL database reachable from Vercel. Use the provider's recommended pooled/serverless connection URL when available. Do not commit credentials.
- Deploy, then check `/health`; it returns 200 only when the database connection works.
- Evidence uploads require an S3-compatible object store and the following backend environment variables: `S3_BUCKET`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION`. `S3_ENDPOINT_URL` is optional for compatible providers. Without these, complaints without attachments can be submitted, while file uploads intentionally return 503 rather than lose files. Bucket encryption and access policy should be configured in the storage provider; uploads request AES256 server-side encryption.

Set the backend production URL as `BACKEND_URL` in the frontend Vercel project and redeploy the frontend after setting it. The API endpoint accepts `multipart/form-data`: `title`, `description` (minimum 50 characters), `category`, optional `is_anonymous`, `latitude`, `longitude`, and up to five optional `files` (10 MiB each). The endpoint is `/api/complaints/submit`.

## Local checks

Frontend: `cd frontend && npm install && npm run build`
Backend: `cd backend && python -m pip install -r requirements.txt && python -c 'from main import app; print(app.title)'`

## Important before real use

The UI is a prototype and does not yet submit reports. There is no user authentication, authorization, rate limiting, backup policy, audit trail, or implemented AI/legal analysis. Database tables are not automatically migrated by this Vercel setup; apply schema migrations before production use. Do not collect sensitive real-world reports until those controls, privacy/retention policies, monitoring, and recovery procedures have been implemented and reviewed.
