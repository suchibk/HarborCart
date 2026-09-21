# HarborStore: Add age validation and Confirm Email

## Baseline (main)
Registration already collects first name, last name, optional age text, and email.
There are no age validation rules. Names, email format, duplicate-email handling,
and the customerId success response already work and must continue to work.

## Requirement for the PR
As a store owner, I want registration to accept only customers with a whole-number
age from 18 through 120 inclusive, with consistent browser, API, and SQL rules.
As a customer, I want to confirm my email address before registering so that
accidental typing differences are caught before my registration is saved.
Both features belong to the same PR.

## Acceptance criteria
- AC-1: Make Age required and accept only whole numbers from 18 through 120 inclusive.
- AC-2: Enforce the rule on the server even when the browser is bypassed.
  Missing/null, fractional, negative, nonnumeric, underage, and over-120 inputs
  must return HTTP 400.
- AC-3: The browser must send age as a JSON number and show validation errors;
  Register must be usable again after a failed request.
- AC-4: Update the optional fresh-install SQL schema to INT NOT NULL with the
  same inclusive 18-120 constraint. No existing-data migration is needed for this demo.
- AC-5: Test ages 18 and 120 as accepted; test missing/null, -1, 17, 121,
  18.5, and nonnumeric age as rejected.
- AC-6: Preserve existing name/email validation, duplicate-email rejection,
  HTTP 201, and the customerId response field.

### Confirm Email (required in this PR)
- AC-7: Add a required Confirm Email textbox next to or below Email.
- AC-8: Send its value in the JSON field confirmEmail and accept that field in
  the C# request model.
- AC-9: Validate confirmation in both the browser and API. Compare Email and
  Confirm Email after trimming leading/trailing whitespace, ignoring case.
- AC-10: The API must reject missing, null, blank, or mismatched confirmation
  with HTTP 400 and an errors.confirmEmail message, without creating a registration.
- AC-11: Show a useful confirmation error in the page and allow correction and
  resubmission. Matching values must preserve HTTP 201 and customerId.
- AC-12: Test matching, mismatched, omitted, null, blank, mixed-case, and
  surrounding-whitespace confirmation values. Include a direct API test that
  bypasses browser validation, and verify a rejected request does not reserve
  the email address.

## Review demonstration
Age validation exercises boundary checks and JavaScript/C#/SQL consistency.
Confirm Email exercises HTML/JavaScript/C# field contracts and server enforcement.
The existing demo patch implements only the age-validation portion, with deliberate
boundary defects. This feature branch also implements Confirm Email, and the smoke suite tests
the direct API confirmation cases in AC-12. The API age-18 check intentionally
fails until the demo boundary defect is fixed; SQL needs separate inspection.
Email confirmation here means comparing two inputs, not verifying email ownership.
No email delivery service, database, or additional packages are needed.

## Demo scope
Records are temporary and reset when the server stops. SQL is an illustrative
future persistence contract. No passwords, sign-in, email delivery, or real data.
