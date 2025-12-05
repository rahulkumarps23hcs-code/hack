# SAFE-ZONE Backend API Summary

Base URL (local dev): `http://localhost:5000`

All responses follow the global format:

```json
{
  "success": true,
  "message": "...",
  "data": { }
}
```

---

## Auth

### POST /auth/signup

Create a new user.

**Request body (JSON):**

```json
{
  "name": "string (2-100)",
  "phone": "string (5-20)",
  "email": "valid email",
  "password": "string (6-100)"
}
```

Validated with Joi. On error:

```json
{
  "success": false,
  "message": "Validation failed",
  "data": { "errors": ["..."] }
}
```

**Response (201):**

```json
{
  "success": true,
  "message": "User signed up successfully",
  "data": {
    "user": {
      "id": "...",
      "name": "...",
      "phone": "...",
      "email": "..."
    },
    "token": "JWT_TOKEN"
  }
}
```

---

### POST /auth/login

Login with email or phone.

**Request body (JSON):**

```json
{
  "email": "valid email (optional if phone given)",
  "phone": "string (5-20, optional if email given)",
  "password": "string (6-100)"
}
```

At least one of `email` or `phone` must be provided.

**Response (200):**

```json
{
  "success": true,
  "message": "User logged in successfully",
  "data": {
    "user": { "id": "...", "name": "...", "phone": "...", "email": "..." },
    "token": "JWT_TOKEN"
  }
}
```

---

### GET /user/me

Get current authenticated user.

**Headers:**

- `Authorization: Bearer <JWT_TOKEN>`

**Response (200):**

```json
{
  "success": true,
  "message": "Current user fetched successfully",
  "data": {
    "id": "...",
    "name": "...",
    "phone": "...",
    "email": "..."
  }
}
```

---

## Alerts & Reporting

### GET /alerts

Fetch latest alerts.

**Response (200):**

```json
{
  "success": true,
  "message": "Alerts fetched successfully",
  "data": [
    {
      "id": "...",
      "type": "...",
      "severity": "...",
      "timestamp": "ISO date string",
      "location": { "lat": 12.97, "lng": 77.59 },
      "description": "..."
    }
  ]
}
```

---

### POST /alerts/report

Report a new alert. **Auth required.**

**Headers:**

- `Authorization: Bearer <JWT_TOKEN>`

**Request body (JSON):**

```json
{
  "type": "string (2-100)",
  "severity": "string (2-50)",
  "timestamp": "optional ISO date string",
  "location": { "lat": number, "lng": number },
  "description": "optional string (max 1000)"
}
```

Validated with Joi; on error returns `success=false` with error list.

**Response (201):**

```json
{
  "success": true,
  "message": "Alert reported successfully",
  "data": {
    "id": "...",
    "type": "...",
    "severity": "...",
    "timestamp": "...",
    "location": { "lat": 12.97, "lng": 77.59 },
    "description": "..."
  }
}
```

---

### POST /report

Alias for `/alerts/report`. Same auth, request body, and response format.

---

## SOS

### POST /sos/trigger

Trigger a SOS with optional file attachment. **Auth required.**

**Headers:**

- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: multipart/form-data`

**Body (form-data):**

- `location[lat]` (optional, number)
- `location[lng]` (optional, number)
- `description` (optional string, max 2000)
- `attachment` (optional file, any type)

The JSON body is validated via Joi (`location` and `description`). The file is handled by Multer separately.

**Response (201):**

```json
{
  "success": true,
  "message": "SOS processed successfully",
  "data": {
    "sosId": "sos-placeholder",
    "status": "dispatched",
    "priority": "high",
    "user": { "id": "...", "name": "...", "phone": "...", "email": "..." },
    "location": { "lat": 12.97, "lng": 77.59 },
    "description": "...",
    "attachmentPath": "uploads/...",
    "nearestSafeSpots": [
      {
        "id": "...",
        "name": "...",
        "type": "...",
        "address": "...",
        "location": { "lat": 12.97, "lng": 77.59 }
      }
    ]
  }
}
```

---

## Zones (Safe / Unsafe)

### GET /zones/unsafe

Generate unsafe zone analysis using AI placeholder.

**Query params (optional):**

- `lat`: number
- `lng`: number

**Response (200):**

```json
{
  "success": true,
  "message": "Unsafe zone analysis generated successfully",
  "data": {
    "zoneType": "unsafe",
    "zoneId": "zone-placeholder",
    "location": { "lat": 12.97, "lng": 77.59 },
    "riskLevel": "high" | "low",
    "alerts": [AlertModel...],
    "recommendation": "string"
  }
}
```

---

### GET /zones/safe

Same as `/zones/unsafe` but with `zoneType: "safe"` and message:

```json
{
  "success": true,
  "message": "Safe zone suggestions generated successfully",
  "data": { ... }
}
```

---

## Routes (Safer Path)

### GET /routes/safer

Get a safer route between two points using AI placeholder.

**Query params (optional but recommended):**

- `fromLat`, `fromLng`
- `toLat`, `toLng`

**Response (200):**

```json
{
  "success": true,
  "message": "Safer route generated successfully",
  "data": {
    "routeId": "route-placeholder",
    "from": { "lat": 12.97, "lng": 77.59 },
    "to": { "lat": 12.98, "lng": 77.6 },
    "riskScore": 0.3,
    "checkpoints": [
      { "lat": 12.97, "lng": 77.59, "label": "Start", "riskLevel": "medium" },
      { "lat": 12.98, "lng": 77.6, "label": "Destination", "riskLevel": "low" }
    ]
  }
}
```

---

## Safe Spots

### GET /safe-spots

Fetch all safe spots.

**Response (200):**

```json
{
  "success": true,
  "message": "Safe spots fetched successfully",
  "data": [
    {
      "id": "...",
      "name": "...",
      "type": "...",
      "address": "...",
      "location": { "lat": 12.97, "lng": 77.59 }
    }
  ]
}
```

---

### GET /safe-spots/nearby

Fetch nearest safe spots (AI placeholder-ranked).

**Query params:**

- `lat` (optional number)
- `lng` (optional number)
- `limit` (optional integer, default 5)

**Response (200):**

```json
{
  "success": true,
  "message": "Nearby safe spots fetched successfully",
  "data": [SafeSpotModel...]
}
```

---

## Error Responses

- Unknown routes:

```json
{
  "success": false,
  "message": "Route not found",
  "data": null
}
```

- Validation errors (any validated POST endpoint):

```json
{
  "success": false,
  "message": "Validation failed",
  "data": {
    "errors": ["...", "..."]
  }
}
```

- Other server errors:

```json
{
  "success": false,
  "message": "Internal server error" | "Request failed",
  "data": null
}
```
