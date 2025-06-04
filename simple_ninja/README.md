Steps:

## login:
        http://127.0.0.1:8000/api/auth/docs/

it will give to you a response:

```json 
{
  "meta": {
    "is_authenticated": false,
    "session_token": "ujmo9rt90gr287sdagrl9urkusujw7st"
  }
}
```

Save to session_token

## setup token:
        
1. visit http://127.0.0.1:8000/api/docs/
2. in the auth popup set the x-session-token like: ujmo9rt90gr287sdagrl9urkusujw7st
3. go to api/add endpoint

## To run schemathesis:

version: schemathesis==4.0.0a11

just run `pytest .` in the project root

Default user password:

{
  "email": "email@domain.org",
  "password": "Alohomora!"
}



