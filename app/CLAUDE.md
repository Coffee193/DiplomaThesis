# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Diplomat is a chat application with an LLM-powered backend that answers questions about uploaded JSON files (scheduling/planning domain: jobs, tasks, resources, task-suitable-resources, task-precedence-constraints). Users upload JSON data files and ask natural-language questions; the backend classifies the question through a multi-chain LLM pipeline and returns structured answers.

## Development Commands

### Backend (Django)
```
cd backend
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
```

### Frontend (React + Vite)
```
cd frontend
npm install
npm run dev          # starts dev server on 127.0.0.1:8080
npm run build
npm run lint         # ESLint
```

### Tests
```
python tests/test_string_generator.py   # admin key generation script
```

## Architecture

### Two-service architecture
- **Backend**: Django 4.1 + Django REST Framework, running on Python. Serves REST API only (headless architecture).
- **Frontend**: React 19 + Vite + SWC, served separately on port 8080. Uses `react-router-dom` for client-side routing.

### Databases (all three required to run)
- **PostgreSQL** (port 5432, database "Sapling"): User accounts, referral codes. Managed via Django ORM (`loginregister` and `referal` apps).
- **MongoDB** (port 27017, database "Sapling"): Chat conversations and messages. Accessed directly via `pymongo` in `backend/backend/mongo_db_connection.py`.
- **Redis** (port 6379): JWT token storage/rotation, Django cache, and real-time chat streaming via Redis Streams (`xadd`/`xread` on keys prefixed `cs_` for chat streams, `cg_` for chat generation state).

### LLM Integration
Three model modes controlled by `data['m']`:
- `m=1`: Local LLM with "thinking" chain pipeline (via Ollama `chat()`)
- `m=2`: Local LLM without thinking pipeline (via Ollama `chat()`)
- `m=3`: Cloud model (OpenAI GPT-4.1 via `openai` SDK, requires user-provided API key)

The LLM model name is set via the `LLM_MODEL` environment variable (used with Ollama).

### LLM Pipeline (`backend/chats/LLMpipeline.py`)
A 5-chain sequential classification pipeline for the "thinking" mode (m=1):
- **Chain 1**: Gibberish detection (is the input nonsense?)
- **Chain 2**: High-level entity classification (jobs/tasks/resources/tasksuitableresources/taskprecedenceconstraints) + output JSON detection (assignments/dispatch/duration)
- **Chain 3**: Attribute retrieval (what filter does the user want? e.g., "id = 578")
- **Chain 4**: Wanted return value classification (what field does the user want back? e.g., "names")
- **Chain 5**: Final answer generation with the filtered/formatted data

Each chain has its own prompt module under `backend/LLM_prompts/Chain{N}/`. The pipeline distinguishes between Input JSON files (containing raw scheduling data) and Output JSON files (containing assignment results).

### LLM Prompt Modules (`backend/LLM_prompts/`)
Each prompt is a Python module with a `getPrompt(...)` function that returns a formatted prompt string. Organized by purpose:
- `Chain1/`-`Chain5/`: Pipeline classification prompts
- `TitleGeneration/`: Chat title auto-generation
- `FindJSONFile/`, `JSONUploadNoQuestion/`, `JSONQuestionNoPath/`: File handling prompts
- `UploadJSONFileNoQuestion/`, `UploadJSONFileIrrelevantQuestion/`: Upload context prompts
- `NoAgent/`: Direct LLM mode (m=2) prompts
- `UnexpectedException/`: Fallback error prompts

### Authentication (`backend/oauth.py`)
Custom JWT implementation with access + refresh token pairs. Tokens are signed with randomly selected algorithms (HS256, RS256, PS256) per pair creation. Access tokens expire in 15 minutes; refresh tokens in 1-60 days depending on "remember me". JWT keys are loaded from environment variables (`PUBLIC_RSA_KEY_ACCESS`, `PRIVATE_RSA_KEY_ACCESS`, etc.).

Key helper functions: `ValidateAndCreateJWT()` validates requests and auto-refreshes expired access tokens. `CreateResponseNewAccess()` and `CreateStreamingResponseNewAccess()` wrap responses with updated cookies.

### Real-time Streaming
LLM answers are streamed to the frontend via Redis Streams + Django `StreamingHttpResponse`. The flow:
1. A `multiprocessing.Process` runs the LLM call, writing chunks to Redis Stream `cs_{chat_id}`
2. `GetLLMAnswerStream()` generator reads from the stream and yields JSON lines
3. Stream message keys: `v`=value/text chunk, `t`=title, `d`=done, `i`=info (query+search), `u`=uploaded document, `e`=error

### ID Generation (`backend/snowflake_id_gen.py`)
Twitter-style Snowflake IDs (64-bit): 42 bits timestamp + 5 bits worker + 5 bits process + 12 bits sequence. Used for user IDs, chat IDs, and document IDs.

### Frontend Routing
- `/login`, `/register` - Auth pages
- `/` - Home
- `/chat`, `/chat/:id` - Chat lobby / conversation
- `/settings` - User settings
- `/referalcodes` - Referral code management
- `/termspolicies` - Terms and policies

## Environment Variables (via `.env`, loaded with `python-dotenv`)
- `POSTGRES_PASSWORD` - PostgreSQL password
- `LLM_MODEL` - Ollama model name for local LLM
- `CHAT_DOCUMENT_PATH` - Filesystem path where uploaded JSON files are stored
- `development` - Set to `'true'` for dev mode (changes file paths)
- `JWT_ACCESS_TIME`, `JWT_REFRESH_TIME` - Token expiration in seconds
- `PUBLIC_RSA_KEY_ACCESS`, `PRIVATE_RSA_KEY_ACCESS`, `PUBLIC_RSA_KEY_REFRESH`, `PRIVATE_RSA_KEY_REFRESH` - RSA JWT keys
- `PUBLIC_PS_KEY_ACCESS`, `PRIVATE_PS_KEY_ACCESS`, `PUBLIC_PS_KEY_REFRESH`, `PRIVATE_PS_KEY_REFRESH` - PS256 JWT keys
- `HS_KEY_ACCESS`, `HS_KEY_REFRESH` - HMAC JWT keys

## Key Conventions
- Uploaded files are stored as `{chat_id}_{document_id}.json` in the `CHAT_DOCUMENT_PATH` directory
- MongoDB chat documents use `_id` as Snowflake int, with a `chat` array of message objects containing `q` (question), `a` (answer), `d` (documents), `t` (timestamp), `think` (chain reasoning), `i` (fetched items), `s` (search type)
- The `cg_` Redis prefix means "chat generation" (in-progress), `cs_` means "chat stream"
- The `ut_` Redis prefix is for temporary user sessions (no remember-me), `ur_` for remembered sessions
