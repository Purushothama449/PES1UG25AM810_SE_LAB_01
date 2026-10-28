"""Insurance premium calculator."""

import http.client
import math
import os
import secrets
import tarfile
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from defusedxml import ElementTree as ET

quotes = {}
HOST = "127.0.0.1"
BASE_RATES = {"health": 5000, "motor": 3000, "life": 8000}
LOG_FILE = Path("premium_quotes.log")


@dataclass
class PremiumRequest:
    """Store the details required to calculate a premium."""

    policy_type: str
    age: int
    sum_insured: float
    smoker: bool
    claims: int
    discounts: list[float] = field(default_factory=list)


def calculate_premium(request: PremiumRequest) -> float:
    """Calculate the insurance premium."""
    base = BASE_RATES[request.policy_type]
    premium = base + request.sum_insured * 0.002

    if request.age > 45:
        premium *= 1.5

    if request.smoker:
        premium *= 1.3

    premium += request.claims * 1000

    for discount in request.discounts:
        premium -= discount

    return premium


def age_from_dob(dob: str) -> int:
    """Calculate age from a date of birth."""
    born = datetime.strptime(dob, "%d-%m-%Y")
    today = datetime.now()
    return today.year - born.year


def policy_number() -> str:
    """Generate a policy number."""
    return f"POL-{secrets.randbelow(900000) + 100000}"


def save_quote(name: str, premium: float) -> str:
    """Save a quote and return its policy number."""
    number = policy_number()
    quotes[number] = {"name": name, "premium": premium}

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{number},{name},{premium:.2f}\n")

    return number


def import_policies(
    xml_text: str,
) -> list[tuple[str | None, int, int]]:
    """Import policy information from XML text."""
    root = ET.fromstring(xml_text)
    result = []

    for policy in root.findall("policy"):
        try:
            result.append(
                (
                    policy.get("type"),
                    int(policy.get("age")),
                    int(policy.get("sum")),
                )
            )
        except (TypeError, ValueError):
            continue

    return result


def fetch_rates(url: str) -> bytes:
    """Fetch rate data only from HTTPS URLs."""
    parsed_url = urllib.parse.urlparse(url)

    if parsed_url.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed.")

    if not parsed_url.hostname:
        raise ValueError("A valid HTTPS hostname is required.")

    connection = http.client.HTTPSConnection(
        parsed_url.hostname,
        parsed_url.port or 443,
        timeout=10,
    )

    path = parsed_url.path or "/"

    if parsed_url.query:
        path += f"?{parsed_url.query}"

    try:
        connection.request("GET", path)
        response = connection.getresponse()

        if response.status < 200 or response.status >= 300:
            raise ValueError(
                f"HTTPS request failed with status {response.status}"
            )

        return response.read()
    finally:
        connection.close()


def import_claim_documents(archive_path: str) -> None:
    """Safely extract claim documents from a TAR archive."""
    destination = Path("claims_docs").resolve()
    destination.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive_path) as archive:
        archive.extractall(destination, filter="data")


def monthly_instalment(
    premium: float,
    months: int = 12,
) -> int | float:
    """Calculate the monthly premium instalment."""
    if months == 0:
        return premium

    return math.floor(premium / months)


def is_authorised(token: str, expected_token: str) -> bool:
    """Check whether the supplied token is authorised."""
    return bool(token) and token == expected_token


def renewal_due(start: str, years: int = 1) -> str:
    """Calculate the renewal date."""
    start_date = datetime.strptime(start, "%Y-%m-%d")
    return start_date.replace(
        year=start_date.year + years
    ).strftime("%Y-%m-%d")


def print_quotes() -> None:
    """Print all saved quotes."""
    print("===== Quote Book =====")

    for index, key in enumerate(quotes, start=1):
        print(
            index,
            key,
            quotes[key]["name"],
            "Rs.",
            quotes[key]["premium"],
        )


def main() -> None:
    """Run the insurance premium calculator."""
    underwriter_token = os.environ.get(
        "UNDERWRITER_TOKEN",
        "",
    )

    p1 = calculate_premium(
        PremiumRequest(
            "health",
            30,
            500000,
            False,
            0,
        )
    )

    p2 = calculate_premium(
        PremiumRequest(
            "health",
            30,
            500000,
            False,
            0,
        )
    )

    p3 = calculate_premium(
        PremiumRequest(
            "motor",
            50,
            800000,
            False,
            0,
        )
    )

    p4 = calculate_premium(
        PremiumRequest(
            "life",
            25,
            100000,
            False,
            0,
            [3000, 3000, 3000],
        )
    )

    print("Quote 1:", p1)
    print("Quote 2 (same customer details):", p2)
    print("Non-smoker aged 50:", p3)
    print("Life with stacked discounts:", p4)

    print(
        "Age from DOB 31-12-1990:",
        age_from_dob("31-12-1990"),
    )

    print(
        "Monthly instalment:",
        monthly_instalment(p3),
    )

    print(
        "Renewal due:",
        renewal_due("2025-03-15"),
    )

    xml_data = (
        "<policies>"
        "<policy type='health' age='40' sum='300000'/>"
        "<policy type='motor' age='abc' sum='1'/>"
        "</policies>"
    )

    print(
        "Imported:",
        import_policies(xml_data),
    )

    print(
        "Saved as:",
        save_quote("Kiran", p1),
    )

    print(
        "Authorised:",
        is_authorised(
            underwriter_token,
            underwriter_token,
        ),
    )

    print(
        "Server would listen on",
        HOST,
    )

    print_quotes()


if __name__ == "__main__":
    main()
