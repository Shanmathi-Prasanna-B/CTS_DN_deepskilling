# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### Testing Types for the Course Management API

| Testing Type | Concrete Test Case | Functional / Non-Functional |
|---|---|---|
| **Unit Testing** | Test `get_password_hash()` in isolation — pass a plain password and assert the returned string is a bcrypt hash, not equal to the input. | Functional |
| **Integration Testing** | POST `/api/v1/courses/` with valid JWT and body; assert HTTP 201, course saved in database, and `Location` header points to new resource. | Functional |
| **System Testing** | End-to-end: register admin → login → create course → enroll student → GET enrolled students for course; verify all steps succeed without manual DB edits. | Functional |
| **User Acceptance Testing (UAT)** | College admin creates a course "Advanced Python" via admin UI/API; confirms course appears in student portal course list and can receive enrollments. | Functional |

### Non-Functional Test Example

**Performance test:** Send 100 concurrent GET requests to `/api/v1/courses/` and assert 95th percentile response time is under 500 ms with zero 5xx errors.

### Black-Box vs White-Box Testing

| Aspect | Black-Box | White-Box |
|---|---|---|
| Knowledge of code | Tester does not see internal implementation | Tester knows code structure, branches, DB queries |
| Focus | Inputs, outputs, and specified behaviour | Code paths, coverage, internal logic |
| Typical performer | QA tester / business analyst | Developer (unit tests, code review) |

QA testers typically perform **black-box testing**. Developers typically perform **white-box testing** (unit tests, integration tests at code level).

### Formal Test Cases — POST /api/courses/

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-COURSE-001 | Create course with valid data | API running; valid JWT; department exists | 1. POST `/api/v1/courses/` with name, code, credits, department_id 2. Check status and body | HTTP 201; course JSON returned; Location header set | | |
| TC-COURSE-002 | Reject duplicate course code | Course with code `CS101` already exists | 1. POST `/api/v1/courses/` with same code `CS101` 2. Check response | HTTP 400 or 409; error message indicates duplicate code | | |
| TC-COURSE-003 | Reject missing required fields | API running; valid JWT | 1. POST `/api/v1/courses/` with only `name` field 2. Check response | HTTP 400 or 422; validation error listing missing fields | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### Defect Lifecycle

```
New → Assigned → Open → Fixed → Retest → Verified → Closed

Alternative paths:
- Rejected: New → Assigned → Open → Rejected (not a bug / duplicate / won't fix)
- Deferred: New → Assigned → Open → Deferred (fix postponed to future release)
- Reopen: Verified/Closed → Reopen → Assigned → Open (if fix failed in production)
```

| State | Description |
|---|---|
| **New** | Defect logged, not yet reviewed |
| **Assigned** | Assigned to a developer |
| **Open** | Developer acknowledged and working on fix |
| **Fixed** | Developer deployed fix to test environment |
| **Retest** | QA re-running test cases against the fix |
| **Verified** | QA confirmed fix works |
| **Closed** | Defect resolved and signed off |
| **Rejected** | Not valid (duplicate, by design, cannot reproduce) |
| **Deferred** | Valid but postponed to a later sprint/release |

### Severity and Priority Classifications

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| (a) POST `/api/courses/` returns 500 for all requests | **Critical** | **P1** | Core create functionality completely broken; blocks all course creation |
| (b) Course names >150 chars silently truncated | **Medium** | **P2** | Data loss without user notification; workaround exists (shorter names) |
| (c) Typo in Swagger `/docs` description | **Low** | **P3** | Cosmetic documentation issue; no functional impact |
| (d) Intermittent 401 on first login attempt | **High** | **P1** | Auth instability; hard to reproduce; affects user trust and all protected endpoints |

### Defect Report — Bug (a)

| Field | Value |
|---|---|
| **Defect ID** | DEF-2026-0042 |
| **Title** | POST /api/courses/ returns HTTP 500 Internal Server Error for all valid requests |
| **Environment** | Dev — Windows 11, Python 3.13, FastAPI 0.115, SQLite |
| **Build Version** | v1.0.3-handson09 |
| **Severity** | Critical |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Register user via POST `/api/v1/auth/register/` 2. Login and obtain JWT 3. POST `/api/v1/courses/` with valid JSON body and Authorization header 4. Observe response |
| **Expected Result** | HTTP 201 Created with course JSON and Location header |
| **Actual Result** | HTTP 500 Internal Server Error with generic error message |
| **Attachments** | screenshot of 500 error |

### Severity vs Priority

**Severity** = impact on the system. **Priority** = urgency of the fix.

**Example where High Severity ≠ High Priority:** A bug that corrupts archived student records from 10 years ago (High Severity — data integrity) may be Low Priority if no active users access those records and a manual fix can wait until the next maintenance window.

**Example where Low Severity = High Priority:** A typo in the CEO's dashboard title (Low Severity) may be High Priority if the demo is tomorrow.
