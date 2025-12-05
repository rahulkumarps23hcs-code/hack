# Safe-Zone Frontend (Demo)

Modern React + Vite + Tailwind + Framer Motion frontend for **Safe-Zone: Women & Student Safety System**.

- Frontend-only, **dummy data only** – no real network calls
- Strictly aligned with global multi-team contracts (models, endpoints, naming)
- Designed as a plug-and-play UI layer for backend + AI teams

---

## Stack

- React 18 + Vite 5
- TailwindCSS 3 (dark/light mode via `class` strategy)
- Framer Motion (page + component animations)
- Lucide React (icons)
- React Router DOM 6
- Axios (dummy client, no real endpoints wired yet)

---

## Project layout (mono-repo level)

```text
/backend
/data-engineering
/frontend       ← this app
/model-ai
/shared
```

Frontend app root:

```text
/frontend
  package.json
  vite.config.js
  tailwind.config.js
  postcss.config.js
  index.html
  src/
```

---

## Frontend `/src` architecture

```text
src
  App.jsx
  main.jsx
  assets/
  components/
    alerts/
      alert-card.jsx
    auth/
      auth-shell.jsx
    map/
      map-container.jsx
    safe-spots/
      safe-spot-card.jsx
    sos/
      sos-button.jsx
    ui/
      animated-wrapper.jsx
      badge.jsx
      button.jsx
      card.jsx
      feature-card.jsx
      footer.jsx
      input-field.jsx
      loading-skeleton.jsx
      modal.jsx
      navbar.jsx
      notification-toast.jsx
  config/
    api-config.js
  context/
    alert-context.jsx
    auth-context.jsx
    theme-context.jsx
    toast-context.jsx
  hooks/
    use-night-safety.js
    use-sos.js
  layouts/
    auth-layout.jsx
    main-layout.jsx
  pages/
    Alerts.jsx
    Dashboard.jsx
    Landing.jsx
    Login.jsx
    MapView.jsx
    SafeSpots.jsx
    SOS.jsx
    Signup.jsx
  services/
    api.js
    alerts.js
    auth.js
    safe-spots.js
  styles/
    globals.css
  utils/
    cn.js
    dummy-data.js
    geo.js
```

- File/folder names use **kebab-case** (except React pages/components as PascalCase where required by spec).
- Variables/functions use **camelCase**; components use **PascalCase**.

---

## Shared data models (global contract)

All dummy data and UI assume these fixed shapes:

### Alert model

```js
{
  id,
  type,
  severity,
  timestamp,
  location: { lat, lng },
  description,
}
```

### Safe spot model

```js
{
  id,
  name,
  type,
  address,
  location: { lat, lng },
}
```

### User model

```js
{
  id,
  name,
  phone,
  email,
}
```

### API response

```js
{
  success: boolean,
  message: string,
  data: object | array,
}
```

### Geo/location

```js
{
  lat: number,
  lng: number,
}
```

These are **not modified** in this frontend.

Dummy implementations live in `src/utils/dummy-data.js` and are consumed by contexts/hooks/pages.

---

## Features implemented

All required features are implemented with dummy data only:

- **Real-Time Safety Alerts UI**
  - `pages/Alerts.jsx` + `components/alerts/alert-card.jsx`
  - Filter by severity, view feed (from `alert-context.jsx` + `dummy-data.js`)
  - Community reporting modal (UI for `POST /alerts/report` – toast only)

- **Smart Night-Safety Mode UI**
  - `hooks/use-night-safety.js` + `utils/geo.js`
  - Used in `pages/Dashboard.jsx` to compute safety score, context messages, and nearby spots.

- **Community Reporting Form**
  - In `pages/Alerts.jsx` (`Modal` + `InputField`)
  - Validation in UI; submitting triggers a toast only.

- **Voice/Shake SOS UI (dummy)**
  - `hooks/use-sos.js` manages local state only.
  - `pages/SOS.jsx` displays voice + shake toggles with explanatory text.
  - `components/sos/sos-button.jsx` is the animated SOS button.

- **Nearest Safe Spots Map UI**
  - `pages/MapView.jsx` and `pages/SafeSpots.jsx`
  - Reuse `components/map/map-container.jsx` and `safe-spot-card.jsx`.

- **Safe/Unsafe Zone Map**
  - `components/map/map-container.jsx` visualises safe vs unsafe zones and spots using dummy coords.

- **Authentication Pages**
  - `pages/Login.jsx`, `pages/Signup.jsx` using `AuthShell`, `InputField`, `Button`.
  - Dummy auth via `context/auth-context.jsx` + `services/auth.js` (localStorage only).

- **Dashboard with user activity**
  - `pages/Dashboard.jsx` uses alerts, night-safety hook, safe spots, and `dummyUserHistory`.

- **Global Navigation + Footer**
  - `components/ui/navbar.jsx` and `footer.jsx` used in `layouts/main-layout.jsx` and `auth-layout.jsx`.

- **Global Dark/Light Mode**
  - Managed via `context/theme-context.jsx` (class-based Tailwind `dark` mode).

- **Loading skeletons & toasts**
  - `LoadingSkeleton` used for initial loading states.
  - `ToastProvider` + `NotificationToast` used on login/signup, SOS, and reporting actions.

---

## Services (integration-ready, dummy only)

All services are wired to dummy data now but mirror the backend API contract.

- `services/api.js`
  - Axios instance using `BASE_URL` from `config/api-config.js` (currently empty `''`).
  - Request/response interceptors are defined but no auth header is added yet.

- `services/alerts.js`
  - `fetchAlerts()` → returns `dummyAlerts`.
  - `reportAlert(payload)` → returns `{ success, message, data }` without network.
  - Future: connect to `GET /alerts` and `POST /alerts/report`.

- `services/safe-spots.js`
  - `fetchSafeSpots()` → `dummySafeSpots`.
  - `fetchSafeAndUnsafeZones()` → `{ safeZones, unsafeZones }`.
  - Future: connect to `GET /safe-spots`.

- `services/auth.js`
  - `login(payload)` / `signup(payload)` → return a `User` model based on `dummyUser`.
  - `logout()` and `getCurrentUser()` are stubs.
  - Future: connect to `POST /auth/login`, `POST /auth/signup`, `GET /user/me`.

> **Important:** There are **no real HTTP calls yet**. All data is local.

---

## Contexts & Hooks

- `theme-context.jsx`
  - Toggle dark/light, persistent via `localStorage`.

- `auth-context.jsx`
  - Holds `user`, `isAuthenticated`, `login`, `signup`, `logout`.
  - Uses `services/auth.js`, stores user in `localStorage`.

- `alert-context.jsx`
  - Holds `alerts`, `filteredAlerts`, `severityFilter`, `streaming`, `pushAlert`.
  - Seeds from `dummyAlerts`.

- `toast-context.jsx`
  - Global toast queue rendered via `NotificationToast`.

- `use-night-safety.js`
  - Uses mock location + time to compute `isNight`, `safetyScore`, messages and `nearbySafeSpots`.

- `use-sos.js`
  - Manages dummy SOS state: active flag, last trigger timestamp + source, voice/shake toggles.

---

## Routing & Layouts

- Routing in `App.jsx` via `react-router-dom`:
  - Public: `/` (Landing), `/login`, `/signup`.
  - Protected: `/dashboard`, `/alerts`, `/map`, `/sos`, `/safe-spots`.
- `ProtectedRoute` checks `auth-context` and redirects to `/login` when unauthenticated.
- `main-layout.jsx` wraps main app with Navbar + Footer.
- `auth-layout.jsx` uses a minimal Navbar and centres auth forms.

---

## Running the frontend

From the repo root:

```bash
cd frontend
npm install
npm run dev
```

Then open the printed `http://localhost:XXXX` URL in your browser.

Tailwind warnings like `Unknown at rule @tailwind` / `@apply` may appear in some IDEs; they are
editor-lint issues only, not runtime errors.

---

## How backend + AI can integrate

Backend should implement these endpoints with the shared models:

- `GET /alerts` → `data: Alert[]`
- `POST /alerts/report` → `data: Alert` or summary
- `GET /safe-spots` → `data: SafeSpot[]`
- `POST /sos/trigger` → `data: { id, timestamp, location }` (your design, wrapped in response format)
- `POST /auth/login` → `data: User`
- `POST /auth/signup` → `data: User`
- `GET /user/me` → `data: User`

### Frontend wiring points

- Replace dummy implementations in `services/*.js` with real `apiClient` calls.
- Keep the same function signatures so UI components **do not change**.
- If AI models output alerts, they must use the **Alert model** and plug into the same endpoints.

---

## Notes for other teams

- **Data Engineering** can export CSV/JSON strictly following the shared models; frontend will
  visualise anything that conforms to those contracts.
- **Model/AI** can emit alerts and risk scores using the Alert + Geo models; UI already expects this
  format in the dashboard and alerts pages.
- **Backend** controls auth, persistence, and streaming logic, but must respect the global schemas
  to remain plug-and-play with this UI.
