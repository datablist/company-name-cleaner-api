# Company Name Cleaner API — Python examples

Clean company names with a small, editable list. Each file shows all the API
calls in one place.

## Setup

Use Python 3.12 or newer. From this `python` folder:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DATABLIST_API_KEY='your-personal-api-key'
```

Create your key on the [Datablist API page](https://app.datablist.com/account/api).
Calls consume account credits; see the current
[credit cost and limits](https://platform.datablist.com/docs/enrichments/tools/company-name-cleaner#credits-and-limits)
and [pricing](https://www.datablist.com/pricing).

## Run an example

**Synchronous, using Requests:**

```sh
python sync_requests.py
```

**Asynchronous, using HTTPX:**

```sh
python async_httpx.py
```

Edit the `companies` list at the bottom of either file. Each prints complete
result objects, including `cleanedCompanyName`, `companyNameConfidence`, status,
credits used, and errors.

Both scripts submit a background task, poll every three seconds, and read all
result pages. Requests uses blocking calls; HTTPX uses `await` and
`asyncio.sleep`.

## Customize the examples

The payload sets `keepLegalSuffix` to `False`. Change it to `True` to retain
legal forms such as Ltd. or GmbH in a short, normalized form.

Use the returned `inputId` to match each result to the company you sent.
Confidence can be `High`, `Medium`, `Low`, or `Very Low`.

Each script submits one task with up to 10,000 names, within the API's request
size limits. These examples focus on the HTTP calls and do not batch larger
lists.

## When something fails

HTTP errors raise the library's normal exception. A failed or stopped task
raises an exception with its task ID. A completed task can still contain
individual errors; check each result's `status`.

If you stop a script, the submitted task continues on the server. List your
[tasks](https://platform.datablist.com/docs/enrichments/tasks) to check its status
before creating another task.
