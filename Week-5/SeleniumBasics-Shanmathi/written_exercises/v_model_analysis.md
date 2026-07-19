# Hands-On 2: SDLC vs TDLC — V-Model & Agile QA Integration

## Task 1: V-Model Mapping

### V-Model Diagram

```
Requirements Analysis          ←→    Acceptance Testing (UAT)
        ↓                                    ↑
   System Design              ←→    System Testing
        ↓                                    ↑
 Architecture Design          ←→    Integration Testing
        ↓                                    ↑
   Module / Unit Design       ←→    Unit Testing
        ↓                                    ↑
              ──────── Coding ────────
```

### SDLC ↔ TDLC Phase Mapping and Test Artifacts

| SDLC Phase | TDLC Phase | Test Artifact Produced During Development |
|---|---|---|
| Requirements Analysis | Acceptance Testing | Acceptance test plan, user stories with acceptance criteria, UAT test cases |
| System Design | System Testing | System test plan, end-to-end test scenarios, test environment spec |
| Architecture Design | Integration Testing | Integration test plan, API contract tests, interface test cases |
| Module Design | Unit Testing | Unit test plan, unit test cases, code coverage targets |
| Coding | (executes all tests) | Unit test code, test data, mock objects |

### Entry and Exit Criteria

| Testing Level | Entry Criteria | Exit Criteria |
|---|---|---|
| **Unit Testing** | Code module complete; coding standards met; unit test environment ready | ≥80% code coverage; all unit tests pass; no critical unit-level defects open |
| **Integration Testing** | Unit testing exit criteria met; interfaces defined; test stubs/mocks available | All integration test cases executed; API contracts validated; no critical/high integration defects open |
| **System Testing** | Integration testing complete; full system deployed to test environment; test data loaded | All system test cases executed; end-to-end flows pass; defect count below threshold; no open critical/high defects |
| **Acceptance Testing (UAT)** | System testing exit criteria met; UAT environment mirrors production; business users trained | Business sign-off received; all acceptance criteria met; release notes approved |

### Two Early QA Engagement Points (Course Management API)

1. **Requirements Review (left side — Requirements phase):** QA reviews user stories for "Create Course" and flags ambiguous acceptance criteria (e.g., max course name length, duplicate code handling) before developers write code.

2. **Architecture Review (left side — Architecture Design phase):** QA reviews API contract design (OpenAPI spec) and writes integration test cases for endpoint contracts before implementation begins — catches mismatches early.

---

## Task 2: Agile QA and Shift-Left Testing

### Three Problems with Waterfall Testing (After Development)

1. **Late defect discovery is expensive:** A requirements ambiguity found during system testing requires rework across API, database, and frontend — far costlier than catching it during sprint planning.

2. **Compressed test window:** All testing happens at the end; if critical bugs appear, release date slips or quality is sacrificed.

3. **Poor collaboration:** Developers and QA work in silos; QA becomes a "gate" rather than a partner, leading to adversarial handoffs and missed edge cases.

### QA Role in Agile Ceremonies

| Ceremony | QA Activities |
|---|---|
| **Sprint Planning** | Clarify acceptance criteria; estimate testing effort; identify testability risks; define Definition of Done including test coverage |
| **Daily Standup** | Report blocking defects; flag environments down; communicate test progress and risk areas |
| **Sprint Review** | Demo tested features; present quality metrics; highlight known issues and workarounds |
| **Retrospective** | Propose process improvements (e.g., reduce flaky tests, improve test data setup, add contract tests) |

### Four Shift-Left Practices Applied to Course Management API

| Practice | Application |
|---|---|
| **(a) Requirements testability review** | QA reviews "As a admin, I want to create a course" story and asks: What happens with duplicate codes? Max name length? Missing department_id? Criteria added before coding starts. |
| **(b) Test cases before code (TDD/BDD)** | Write Gherkin scenarios for course creation; developers implement API until scenarios pass; tests drive design decisions. |
| **(c) Static code analysis** | Run pylint/mypy on FastAPI codebase in CI; catch type errors and security patterns (hardcoded secrets) before runtime testing. |
| **(d) API contract testing** | Use OpenAPI spec to generate contract tests; verify POST `/api/courses/` request/response schema before frontend integrates. |

### Acceptance Criteria — User Story (Gherkin)

**Story:** As a college admin, I want to create a new course, so that students can enroll in it.

```gherkin
Scenario: Successfully create a new course (happy path)
  Given I am authenticated as a college admin
  And department with id 1 exists
  When I submit a POST request to /api/v1/courses/ with name "Data Structures", code "CS101", credits 4, department_id 1
  Then the response status should be 201
  And the response body should contain the course with code "CS101"
  And the Location header should point to the new course resource

Scenario: Reject duplicate course code
  Given I am authenticated as a college admin
  And a course with code "CS101" already exists
  When I submit a POST request to /api/v1/courses/ with code "CS101"
  Then the response status should be 409
  And the error message should indicate the course code already exists

Scenario: Reject missing required fields
  Given I am authenticated as a college admin
  When I submit a POST request to /api/v1/courses/ with only the name field
  Then the response status should be 422
  And the error should list the missing required fields
```
