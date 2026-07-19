# POM Test Suite (Hands-On 6 & 7)

## POM Maintenance Benefit

In a flat (non-POM) script, if the Submit button's ID changes from `showInput` to
`btn-submit`, every test file that calls `driver.find_element(By.ID, 'showInput')`
must be updated individually — easy to miss one and cause silent failures.

With POM, the locator lives in one place: `SimpleFormPage.SUBMIT_BUTTON`.
Updating that single tuple fixes all tests that use `click_submit()` — tests
remain readable and maintenance cost drops from N files to 1 line.

## Run Commands

From the `automation_scripts` folder:

```bash
pip install -r ../requirements.txt
pytest test_playground.py -v
pytest test_playground.py --html=report.html --self-contained-html
pytest tests/ -v --html=report.html --self-contained-html
```

## Expected Test Count (POM suite)

- 3 parameterised simple form tests
- 1 checkbox test
- 1 dropdown test
- 1 input form test

Total: 6 tests

## Verify POM Compliance

```bash
grep -R "find_element" tests/test_playground_pom.py
```

No `driver.find_element` calls should appear in the POM test file.
