# Enterprise RAG Studio — Project Spec

> This file is the single source of truth for the project. Every time a new
> screen or feature is designed, add it below instead of starting a new file.

---

## 1. Overview

**Project name:** Enterprise RAG Studio
**Roles:** Admin, Employee (Employee sub-departments: HR, Finance, Technical, Legal)

**Pages total: 12**
- Login = 1
- Admin = 7 → Dashboard, Company Chat, Knowledge Base, User Management, Prompt Management, Analytics, Audit Logs
- Employee = 4 → Company Chat, Personal Chat, Personal AI Settings, Profile

---

## 2. Features (13)

1. Smart PDF Navigation
2. Editable System Prompt
3. RBAC (Role-Based Access Control)
   - Each employee only sees documents belonging to their own department in Company Chat.
   - Example: HR employee → only HR documents. Finance employee → only Finance documents. Legal employee → only Legal documents. Technical employee → only Technical documents.
   - Admin has access to all departments' documents.
   - Enforced at the retrieval/backend level — an employee cannot search or view another department's PDFs even if they know the filename.
4. Hybrid Search + RRF
5. Query Expansion
6. Retrieved Chunk Viewer
7. RAGAS Dashboard
8. Multimodal RAG
9. Metadata Filtering
10. Performance & Cost Dashboard
11. Document Versioning
12. Audit Logs
13. Personal AI Settings

---

## 3. Design system

- Style: Clean minimal dark UI — flat surfaces, subtle borders, single accent color (dashboard-style, inspired by reference images provided by user)
- Fonts: Inter (UI text), JetBrains Mono (code/mono text)
- Colors (grayscale scale + single mint accent):
  - **Dark shades (backgrounds/surfaces):**
    - `black-100` `#0A0E15` — page background
    - `black-90` `#212631` — cards / panels / navbar
    - `black-80` `#373F4E` — elevated surface / hover state / inactive chart bars
    - `black-70` `#4E576A` — default border
    - `black-60` `#667085` — muted border / divider
  - **Light shades (text):**
    - `white-100` `#FFFFFF` — headers / primary text
    - `white-90` `#F0F1F5` — body text
    - `white-80` `#E0E4EB` — secondary text / descriptions
    - `white-70` `#D1D6E0` — muted text
    - `white-60` `#BFC6D4` — placeholder / hint text
  - **Accent:**
    - Mint green `#A9DFD8` — primary buttons, active nav state, chart highlight bars, badges, progress rings, key metric numbers (sampled directly from user's reference dashboard image)
    - Text on mint accent fill uses `black-100` `#0A0E15` (dark text on light accent for contrast)
- Animations: fade/slide transitions, streaming AI responses, hover lift, loading skeletons, highlighted citations
- Design reference: minimal SaaS dashboards (Linear/Vercel-style restraint) — one accent color only, no gradients, no heavy shadows

---

## 4. High-level flow

- Admin uploads company PDFs into the Knowledge Base.
- Employee uses Company Chat to query company-wide documents (scoped by department via RBAC).
- Employee uses Personal Chat to query their own privately uploaded PDFs, with their own AI settings.

---

## 5. Employee panel — page structure

### 5.1 Shared layout (applies to Company Chat AND Personal Chat)

Both pages use the **same UI structure and same components** — only the data
source differs (company documents vs. the employee's personal documents).

**Layout = top navbar + 2 columns below it (no left sidebar).**

**Top navbar (full width, fixed)**
- App name / logo on the left
- Nav items in the middle/right, horizontal: Company Chat, Personal Chat, Personal AI Settings, Profile
- Active item highlighted with accent underline/background
- User avatar / department badge on the far right

**Main column (chat)**
- Header: page title + subtitle
  - Company Chat subtitle = employee's department (e.g. "Legal department access")
  - Personal Chat subtitle = "Personal documents"
- Chat thread:
  - User messages (right-aligned, accent background)
  - AI messages (left-aligned), containing inline numbered citation chips (e.g. `1`, `2`) — clicking a chip opens that source in the right panel
- Input row, placed just above the message input:
  - **PDF scope selector** (dropdown): `All PDFs` / `Select PDF: <filename>` — lets the user restrict the search to one specific document instead of the whole knowledge base. Maps to feature **Metadata Filtering**.
  - **Answer mode selector** (dropdown), 3 options:
    - `Smart answer` — normal LLM-synthesized response (default). Uses **Hybrid Search + RRF** + **Query Expansion**.
    - `Full paragraph` — returns the raw retrieved paragraph/chunk text as-is, no LLM summarization. Uses **Retrieved Chunk Viewer**.
    - `Keyword search` — literal keyword match instead of semantic search, for exact-term lookups.
  - Text input field + send button

**Right panel — "Sources" (~210px)**
- Default view: list of source cards, each showing:
  - File icon (document icon, or image icon if the chunk is an image/diagram — feature **Multimodal RAG**)
  - PDF filename
  - Page number + chunk id
  - Optional "v2" badge if the doc has been updated (feature **Document Versioning**)
- Clicking a source card OR a citation chip in the chat switches this panel to **PDF viewer mode**:
  - Back button (returns to source list)
  - Filename + page number
  - A snippet/preview of that page's text with the matched line wrapped in a highlight (`<mark>`), simulating the exact spot where the answer came from — feature **Smart PDF Navigation** + citation highlighting

**Differences between Company Chat and Personal Chat:**
| | Company Chat | Personal Chat |
|---|---|---|
| Data scope | Company-wide docs, filtered by employee's department (RBAC) | Only the employee's own uploaded PDFs |
| Header subtitle | Department name | "Personal documents" |
| PDF scope dropdown options | Company docs list | Personal docs list |
| AI behavior | Uses global/admin-set system prompt | Can use the employee's custom prompt from Personal AI Settings |

### 5.2 Personal AI Settings page

**Layout:** Top navbar (same as Company/Personal Chat) + main content area with 5 stacked sections, each in its own card.

**Section 1 — System prompt**
- Editable system prompt (textarea) — feature **Editable System Prompt**
- "Reset to default" button (reverts to the admin-set default prompt)

**Section 2 — Response preferences**
- Tone selector: Formal / Casual / Technical
- Response length: Concise / Detailed
- Language: English / Hindi (extendable)

**Section 3 — Default chat behavior**
- Default PDF scope: All PDFs / Select PDF (pre-fills the scope selector on the chat pages)
- Default answer mode: Smart answer / Full paragraph / Keyword search (pre-fills the chat pages; can still be overridden per-message on the chat screen)
- "Show citations" toggle (on/off)

**Section 4 — Personal documents management**
- Storage usage indicator (e.g. "12 of 50 PDFs used" with a progress bar)
- List of uploaded personal PDFs, each with a delete/remove icon
- "Upload" button to add new personal PDFs

**Section 5 — Save actions**
- "Discard changes" button
- "Save changes" button (accent-colored, primary action)

### 5.3 Profile page

**Layout:** Top navbar (same as other Employee pages) + main content area with 4 stacked sections + 1 shortcut link.

**Section 1 — Profile overview (header card)**
- Avatar (with "Change photo" option)
- Name, role ("Employee")
- Department badge (read-only — department is assigned by Admin via RBAC, employee cannot change it)

**Section 2 — Personal information**
- Full name (editable)
- Email (editable)
- Phone number (editable)

**Section 3 — Security**
- Current password / New password fields
- Two-factor authentication toggle
- "Log out from all devices" button

**Section 4 — Usage statistics**
- Metric cards: Total queries, Docs uploaded, Member since, Last active

**Shortcut**
- "Manage AI preferences" link/card at the bottom → navigates to the Personal AI Settings page

---

## 6. Feature → page mapping (Employee side)

| Feature | Where it lives |
|---|---|
| Smart PDF Navigation | Company Chat + Personal Chat (source click → correct page) |
| Retrieved Chunk Viewer | Right sources panel; also "Full paragraph" answer mode |
| Highlighted citations | PDF preview `<mark>` highlight |
| Hybrid Search + RRF | Backend, powers "Smart answer" mode |
| Query Expansion | Backend, powers "Smart answer" mode |
| Multimodal RAG | Image/diagram source cards in the sources panel |
| Metadata Filtering | PDF scope selector (All PDFs / Select PDF) |
| Personal AI Settings | Dedicated page |
| Editable System Prompt | Inside Personal AI Settings page |
| Document Versioning | "v2" badge on source cards |
| RBAC | Backend — restricts docs by department (HR sees only HR docs, Finance only Finance docs, etc.) |
| Audit Logs | Admin panel only |
| RAGAS Dashboard | Admin panel only |
| Performance & Cost Dashboard | Admin panel only |

---

## 7. Admin panel — page structure

*(Not designed yet — to be added.)*

**Note:** Admin panel also uses the **top navbar** layout (same as Employee panel), not a left sidebar. Nav items for Admin: Dashboard, Company Chat, Knowledge Base, User Management, Prompt Management, Analytics, Audit Logs.

---

## Change log
- v1: Initial spec — pages, features, design tokens, flows (from blueprint PDF)
- v2: Added Employee panel structure — Company Chat / Personal Chat shared layout, sources panel with PDF viewer + highlight, feature-to-page mapping
- v3: Added PDF scope selector (All PDFs / Select PDF) and Answer mode selector (Smart answer / Full paragraph / Keyword search)
- v4: Replaced left sidebar with a top navbar for navigation, in both Admin and Employee panels
- v5: Made RBAC explicit — department-based document access (HR sees only HR docs, Finance only Finance docs, Legal only Legal docs, Technical only Technical docs); Admin sees all
- v6: Added detailed Personal AI Settings page structure — 5 sections (System prompt, Response preferences, Default chat behavior, Personal documents management, Save actions)
- v7: Added detailed Profile page structure — 4 sections (Profile overview, Personal information, Security, Usage statistics) + shortcut link to Personal AI Settings
- v8: Replaced design system palette — old navy/purple/blue scheme swapped for a grayscale (black-60 to black-100 / white-60 to white-100) base with a single mint green accent, based on reference dashboard style provided by user
- v9: Corrected accent color to the exact sampled value `#A9DFD8` (pixel-sampled from user's reference dashboard image, replacing earlier approximation)
