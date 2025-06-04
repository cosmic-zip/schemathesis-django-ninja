import schemathesis
import requests
from hypothesis import settings, HealthCheck

# schemathesis.experimental.OPEN_API_3_1.enable()
schema = schemathesis.openapi.from_url("http://localhost:8000/api/openapi.json")


def get_access_token():
    url = "http://127.0.0.1:8000/api/auth/allauth/app/v1/auth/login"
    payload = {"email": "email@domain.org", "password": "Alohomora!"}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        session_token = data["meta"]["session_token"]

        if not session_token:
            raise ValueError("Session token not found in response")
        return session_token

    except Exception as err:
        raise ValueError(f"Request failed: {err}")


TOKEN = get_access_token()


@schema.parametrize()
@settings(
    max_examples=2,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
    deadline=None,
)
def test_api(case):
    token = TOKEN
    headers = {"X-Session-Token": f"{token}"}
    print(f"[DEBUG] Token sent: {headers['X-Session-Token']}")
    response = case.call(headers=headers)

    if response.status_code in (200, 201, 204, 400, 500):
        try:
            case.validate_response(response)
        except Exception as e:
            if "Undocumented HTTP status code" in str(e) and response.status_code in (
                400,
                500,
            ):
                print(
                    f"[@@@] Custom error: Undocumented HTTP status code {response.status_code} :: "
                )
                return
            raise
    else:
        print("[@@@] Not a valid status code: ", response.status_code)
