"""Run the feature acceptance checks against a running HarborStore instance."""
import argparse
import json
import uuid
from urllib.request import Request, urlopen
from urllib.error import HTTPError

parser = argparse.ArgumentParser()
parser.add_argument("base", nargs="?", default="http://localhost:5080")
parser.add_argument("--age-validation", action="store_true", help="Compatibility flag; feature checks always run.")
args = parser.parse_args()
OMITTED = object()
failures = []
checks = 0

def check(condition, label, detail=""):
    global checks
    checks += 1
    if not condition:
        failures.append(f"{label}: {detail}")

def register(**overrides):
    payload = dict(firstName="Alex", lastName="Morgan", age=25,
                   email=f"{uuid.uuid4().hex}@example.com")
    payload.update(overrides)
    payload.setdefault("confirmEmail", payload["email"])
    payload = {key: value for key, value in payload.items() if value is not OMITTED}
    request = Request(args.base + "/api/registrations",
                      data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json"})
    try:
        response = urlopen(request, timeout=10)
    except HTTPError as error:
        response = error
    with response:
        raw = response.read()
        try:
            body = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            body = {}
        return response.status, body

for asset in ("/", "/js/registration.js", "/css/site.css"):
    with urlopen(args.base + asset, timeout=10) as response:
        check(response.status == 200, asset)

for age in (18, 19, 20, 21, 120):
    code, body = register(age=age)
    check(code == 201 and body.get("customerId"), f"accept age {age}", (code, body))
for age in (-1, 17, 121, 18.5, "abc", None, OMITTED):
    code, body = register(age=age)
    check(code == 400, f"reject age {age!r}", (code, body))

for field, value in (("firstName", " "), ("lastName", ""),
                     ("firstName", "a" * 81), ("lastName", "a" * 81),
                     ("email", "not-an-email"), ("email", "a" * 255)):
    code, body = register(**{field: value})
    check(code == 400 and field in body.get("errors", {}), f"validate {field}", (code, body))

for confirmation in ("different@example.com", OMITTED, None, "", "   "):
    email = f"{uuid.uuid4().hex}@example.com"
    code, body = register(email=email, confirmEmail=confirmation)
    check(code == 400 and "confirmEmail" in body.get("errors", {}),
          f"reject confirmation {confirmation!r}", (code, body))
    code, body = register(email=email, confirmEmail=email)
    check(code == 201 and body.get("customerId"),
          "rejected confirmation must not reserve email", (code, body))

for variant in ("matching", "mixed-case", "whitespace"):
    email = f"{uuid.uuid4().hex}@example.com"
    confirmation = email if variant == "matching" else email.upper()
    if variant == "whitespace":
        confirmation = "  " + confirmation + "  "
        email = " " + email + " "
    code, body = register(email=email, confirmEmail=confirmation)
    check(code == 201 and body.get("customerId"), f"accept {variant} confirmation", (code, body))

email = f"{uuid.uuid4().hex}@example.com"
check(register(email=email)[0] == 201, "initial registration")
check(register(email=" " + email.upper() + " ")[0] == 409, "case-insensitive duplicate")

for failure in failures:
    print("FAIL:", failure)
print(f"{checks - len(failures)}/{checks} checks passed.")
raise SystemExit(1 if failures else 0)
