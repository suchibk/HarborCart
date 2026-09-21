# HarborStore — AddValidation demo branch

Small ASP.NET Core (.NET 10) registration app for demonstrating code review.

## Run and test

```powershell
dotnet run --project HarborStore.csproj --urls http://localhost:5080
python tests/smoke_test.py http://localhost:5080
```

Run the smoke test in a second terminal. Restart the app after code changes.
The tests always check the feature requirements; --age-validation is also accepted.

## Changes from main

Age is required and sent as a JSON number. Confirm Email is required in the
browser and API; trimmed values are compared without case sensitivity.
Failed confirmation does not reserve an email address. Existing name/email
validation, duplicate rejection, HTTP 201 and customerId are preserved.

This branch deliberately retains the supplied demo patch's two review defects:
- API rejects age 18, although the requirement and browser permit it.
- Optional SQL schema requires age 21, rather than 18.

The API smoke suite should report one failure for age 18 and continue checking
the remaining requirements. Review the SQL constraint separately: the app stores
registrations in memory and never executes SQL. The baseline on main has optional
unrestricted age text. Do not reapply demo/registration-regressions.patch here.

## Review

From the code-review-agent directory with its Python environment activated:

```powershell
python app.py review "C:\Personal\AI Study\ai-study-projects\harborstore\HarborStore" --base main --demo --output reports/harborstore-demo.json
```

The agent includes tracked working-tree changes without requiring a commit.
The deterministic --demo mode demonstrates orchestration and may not find these
defects. Configure NEBIUS settings and omit --demo for model-based review.
The agent does not automatically fetch the GitHub issue or acceptance criteria.

See docs/registration-story.md for requirements. Use fictional registration data.
There are no passwords, email delivery, database, or additional packages.
