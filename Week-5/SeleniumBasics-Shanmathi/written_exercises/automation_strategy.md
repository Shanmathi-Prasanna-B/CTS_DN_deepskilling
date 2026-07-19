# Hands-On 3: Test Automation Process, Lifecycle & Framework Types

## Task 1: Automation Decision and Test Case Selection

### Five Criteria for Automation Decision

| # | Criterion | Explanation | Applied to POST /api/courses/ returns 201 |
|---|---|---|---|
| 1 | **Repetition frequency** | Tests run often (regression, CI) benefit most from automation | **Automate** — CRUD regression runs on every commit |
| 2 | **Stability of feature** | Stable UI/API with infrequent changes is a good automation candidate | **Automate** — course creation schema is stable |
| 3 | **Objective pass/fail** | Clear expected output enables reliable assertions | **Automate** — 201 status and JSON body are deterministic |
| 4 | **Execution time / cost** | Manual execution cost × frequency should exceed automation cost | **Automate** — API test runs in seconds vs manual Postman steps |
| 5 | **Risk and business impact** | High-risk flows justify automation investment | **Automate** — course creation is core business functionality |

### Manual vs Automate Decisions

| Test Case | Decision | Justification |
|---|---|---|
| (a) Regression CRUD after every code change | **Automate** | Repetitive, high-risk, clear assertions, runs in CI |
| (b) Exploratory testing of new search feature | **Manual** | Requires human creativity; feature is new and unstable |
| (c) Performance: 100 concurrent GET `/api/courses/` | **Manual / Tool** | Requires load tool (JMeter, k6), not typical Selenium/API unit test |
| (d) UI test for login form | **Automate** | Repetitive, regression candidate, stable flow |
| (e) Verify Swagger documentation accuracy | **Manual** | Subjective comparison; docs change format frequently |
| (f) Smoke test: API reachable after deployment | **Automate** | Simple health check; runs on every deploy; fast feedback |

### Test Automation ROI Calculation

- Automation cost: **4 hours** (one-time)
- Manual run cost: **30 minutes** (0.5 hours) per run
- Maintenance overhead: **20%** of manual run time after the 10th run = 0.1 hours per run

**Break-even (before maintenance):**
4 = 0.5 × N → **N = 8 runs**

**After 10th run with 20% maintenance:**
Cost per automated run = 0.5 + 0.1 = 0.6 hours (amortized maintenance)
Runs 1–10: savings = 10 × 0.5 − 4 = 1 hour (already positive after run 8)
From run 11 onward: each run saves 0.5 − 0.1 = **0.4 hours net**

**Answer:** Automation pays for itself after approximately **8 runs** (ignoring maintenance). With 20% maintenance overhead, net savings accelerate from run 11 onward.

### Flaky Tests

A **flaky test** passes and fails intermittently without code changes — usually due to timing, environment, or test data issues.

**Example:** Selenium test clicks Submit before the form fully loads; passes on fast machines, fails on slow CI runners.

**Three prevention/fix strategies:**
1. Replace `time.sleep()` with explicit `WebDriverWait` and expected conditions.
2. Use unique test data per run (avoid collisions from parallel tests).
3. Isolate tests with fresh browser state (`scope='function'` fixtures) and retry only infrastructure failures, not assertion failures.

---

## Task 2: Compare Automation Framework Types

### Framework Comparison

| Framework | Description | Advantage | Disadvantage | Course Management Example |
|---|---|---|---|---|
| **Linear** | Sequential scripts with no reuse; each test is standalone | Simple to write for beginners | Zero reusability; duplicate code everywhere | One script that logs in, creates course, verifies — all in one file |
| **Modular** | Common actions extracted into reusable functions/modules | Reduces duplication; easier maintenance | Functions can grow into unmanageable libraries | `login()`, `create_course()`, `assert_course_exists()` modules shared across tests |
| **Data-Driven** | Test logic separated from test data (CSV, JSON, Excel) | Same test logic runs with many data sets | Data file management overhead | Login test with 50 user/password rows from CSV |
| **Keyword-Driven** | Actions defined as keywords ("Click", "EnterText") mapped to functions | Non-technical users can write tests in spreadsheets | Complex framework setup; abstraction overhead | Spreadsheet: `EnterText | user-message | Hello` → framework executes |
| **Hybrid** | Combines Modular + Data-Driven + optionally Keyword-Driven | Best balance of reuse, data flexibility, and maintainability | Higher initial setup cost | Page Objects + CSV credentials + shared utilities + pytest |

### Recommendation for the Scenario

**Recommended: Hybrid framework (Modular + Data-Driven)**

Justification:
- **50 user/password combinations** → Data-Driven (CSV/JSON test data)
- **Reuse login across 20 test cases** → Modular (Page Object for LoginPage)
- **Support non-technical team members** → optional Keyword layer or Gherkin (Behave) on top

### Hybrid Folder Structure

```
course_management_tests/
├── config/
│   └── settings.py              # base URLs, timeouts, browser config
├── test_data/
│   ├── users.csv                # 50 user/password combinations
│   └── courses.json             # course test data
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── course_list_page.py
│   └── course_form_page.py
├── utilities/
│   ├── driver_factory.py        # WebDriver setup with webdriver-manager
│   └── helpers.py               # screenshots, waits, data loaders
├── tests/
│   ├── conftest.py              # shared fixtures
│   ├── test_login.py
│   ├── test_course_crud.py
│   └── test_enrollment.py
├── reports/
│   └── report.html
└── requirements.txt
```
