## README – API Testing and Authentication Guide

### Authentication Flow

### Step 1 – Obtain Session Token

Access the authentication endpoint:

```
http://127.0.0.1:8000/api/auth/docs/
```

The response will include your session token:

```json
{
  "meta": {
    "is_authenticated": false,
    "session_token": "ujmo9rt90gr287sdagrl9urkusujw7st"
  }
}
```

Copy the value of **`session_token`**. This token is required for authenticated requests.

---

### Step 2 – Configure Token in API Docs

1. Open the API docs:

```
http://127.0.0.1:8000/api/docs/
```

2. Click **Authorize** (the authentication popup).

3. Set the header **`x-session-token`** with your session token:

```
ujmo9rt90gr287sdagrl9urkusujw7st
```

4. Use the interactive documentation to test endpoints like:

```
/api/add
```

---

## Running Schemathesis Tests

Tested with:

```
schemathesis==4.0.0a11
```

Run the test suite with:

```
pytest .
```

from the project root directory.

---

## Default Credentials

Example user credentials for testing:

```json
{
  "email": "email@domain.org",
  "password": "Alohomora!"
}
```
