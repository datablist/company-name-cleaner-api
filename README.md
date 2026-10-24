# Company Name Cleaner API

Clean and standardize company names with the
[Datablist](https://www.datablist.com/) Company Name Cleaner API.

Turn names such as `TRansformFactory Limited` into `Transform Factory` and
`NGF Immobilien GmbH & Co. KG` into `NGF Immobilien`. Fix casing and spacing,
remove legal suffixes, and preserve meaningful names such as `AT&T`, `Studio 54`,
and `Lenßen + Partner Immobilien`.

Use readable company names in email personalization, CRM display names, or
company lists. For outreach, keep the original company name in your records and
use the cleaned name in sentences such as “I wanted to reach out to your team at
NGF Immobilien.”

## Get started

Choose [Python](python/README.md) or [TypeScript](typescript/README.md).
The commands below use Python.

1. [Create a Personal API Key](https://app.datablist.com/account/api).
2. Run these commands from this folder:

```sh
cd python
python -m pip install -r requirements.txt
export DATABLIST_API_KEY='your-personal-api-key'
python sync_requests.py
```

Edit the `companies` list at the bottom of the script to try your own names.
See the [Python guide](python/README.md) for setup and the async example.

Calls use account credits. Check the current
[credit cost and limits](https://platform.datablist.com/docs/enrichments/tools/company-name-cleaner#credits-and-limits)
and [pricing](https://www.datablist.com/pricing) before running the examples.
Each result includes its actual `creditsUsed`.

## Input and output

Send company names to `POST https://api.datablist.com/v1/enrichments/tasks`
with your key in the `X-API-Key` header:

```json
{
  "enrichmentId": "company-name-cleaner",
  "uniqueId": "company-cleaner-example-001",
  "settings": {
    "keepLegalSuffix": false
  },
  "inputs": [
    {
      "inputId": "row-1",
      "data": {
        "companyName": "NGF Immobilien GmbH & Co. KG"
      }
    }
  ]
}
```

Use a new `uniqueId` for each new task. Give each company its own `inputId` to
match it to its result, including when company names repeat.

The API returns `202 Accepted` with a task ID in `@id`. Check the task status,
then retrieve its results. Example results response:

```json
{
  "taskId": "00000000000040008000000000000001",
  "results": [
    {
      "inputId": "row-1",
      "status": "success",
      "outputs": {
        "cleanedCompanyName": "NGF Immobilien",
        "companyNameConfidence": "High"
      },
      "creditsUsed": "0.5",
      "error": null
    }
  ],
  "nextCursor": null
}
```

Set `keepLegalSuffix` to `true` to retain legal forms in a short, normalized
form. Confidence can be `High`, `Medium`, `Low`, or `Very Low`.

## Try with cURL

Set your key, then submit a company name:

```sh
export DATABLIST_API_KEY='your-personal-api-key'

curl --request POST 'https://api.datablist.com/v1/enrichments/tasks' \
  --header "X-API-Key: $DATABLIST_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "enrichmentId": "company-name-cleaner",
    "uniqueId": "company-cleaner-curl-001",
    "settings": {"keepLegalSuffix": false},
    "inputs": [
      {"inputId": "row-1", "data": {"companyName": "TRansformFactory Limited"}}
    ]
  }'
```

Copy the returned `@id` into `TASK_ID`. Use a new `uniqueId` for a new task.

```sh
TASK_ID='paste-returned-task-id'

curl "https://api.datablist.com/v1/enrichments/tasks/$TASK_ID" \
  --header "X-API-Key: $DATABLIST_API_KEY"
```

Repeat the status command every few seconds until `status` is `completed`,
`failed`, or `stopped`. Then retrieve the results:

```sh
curl "https://api.datablist.com/v1/enrichments/tasks/$TASK_ID/results" \
  --header "X-API-Key: $DATABLIST_API_KEY"
```

If `nextCursor` is not `null`, pass it as `cursor` to fetch the next page.
The Python and TypeScript examples read every page for you.

## Python examples

| Example | What it shows |
| --- | --- |
| [Synchronous Requests](python/sync_requests.py) | Clean a list of names using blocking HTTP calls. |
| [Asynchronous HTTPX](python/async_httpx.py) | Use `async` and `await` for the same API workflow. |

Each script is self-contained: submit names, wait for the background task, then
read the results. Both use the API's background tasks; the difference is how
Python waits for the HTTP calls.

## TypeScript example

Use [the standalone TypeScript example](typescript/example.ts) with Node.js 24.3+;
no packages to install. From the repository root:

```sh
export DATABLIST_API_KEY='your-personal-api-key'
node typescript/example.ts
```

Or run with `tsx`, without installing it globally:

```sh
npx tsx typescript/example.ts
```

See the [TypeScript guide](typescript/README.md) for editable inputs and settings.

## Documentation

- [Company Name Cleaner API](https://platform.datablist.com/docs/enrichments/tools/company-name-cleaner)
- [Enrichments API quickstart](https://platform.datablist.com/docs/enrichments/quickstart)
- [Task lifecycle](https://platform.datablist.com/docs/enrichments/tasks)

## Other Datablist API examples

- [Company Name to Domain API](https://github.com/datablist/company-name-to-domain-api): find company websites from names.
- [LinkedIn Profile Finder API](https://github.com/datablist/linkedin-profile-finder-api): find profiles from names and company keywords.
- [LinkedIn Profile Scraper API](https://github.com/datablist/linkedin-profile-scraper-api): retrieve profile, employment, and education details from LinkedIn URLs.
- [Impressum Scraper API](https://github.com/datablist/impressum-scraper-api): extract business details from website Impressum pages.
- [Waterfall Email Finder API](https://github.com/datablist/waterfall-email-finder-api): find work emails from names and companies or LinkedIn URLs.
