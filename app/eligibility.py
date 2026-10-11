"""Rule-based preliminary LAP validator. This does not extract facts from speech."""
from dataclasses import dataclass
from typing import Optional

MAX_LOAN_AMOUNT = 7_500_000
MIN_TENURE_YEARS = 3
MAX_TENURE_YEARS = 15

ELIGIBLE_PROPERTY_TYPES = {"residential", "commercial", "industrial"}
ELIGIBLE_OWNERSHIP = {"sole", "joint"}
ELIGIBLE_OCCUPATIONS = {"salaried", "self-employed"}


@dataclass
class LAPApplication:
    property_type: Optional[str] = None
    ownership: Optional[str] = None
    original_documents_available: Optional[bool] = None
    loan_amount: Optional[int] = None
    occupation: Optional[str] = None
    income_mode: Optional[str] = None
    market_value: Optional[int] = None
    tenure_years: Optional[int] = None
    existing_property_loan: bool = False
    emi_reduction_requested: bool = False
    maximum_offer_accepted: Optional[bool] = None


def validate_lap_application(app: LAPApplication) -> dict:
    """Return status/reason; this is not final loan approval."""
    if app.existing_property_loan or app.emi_reduction_requested:
        return {"status": "TRANSFER_REFERRAL",
                "reason": "Refer to loan-transfer specialist"}

    if app.property_type is not None:
        p = app.property_type.strip().lower()
        if p == "agricultural":
            return {"status": "DISQUALIFIED", "reason": "Agricultural property"}
        if p not in ELIGIBLE_PROPERTY_TYPES:
            return {"status": "CLARIFICATION_REQUIRED",
                    "reason": "Unrecognized property type"}

    if app.ownership is not None:
        if app.ownership.strip().lower() not in ELIGIBLE_OWNERSHIP:
            return {"status": "CLARIFICATION_REQUIRED",
                    "reason": "Clarify ownership"}

    if app.original_documents_available is False:
        return {"status": "DISQUALIFIED",
                "reason": "Original documents unavailable"}

    if app.loan_amount is not None:
        if app.loan_amount <= 0:
            return {"status": "CLARIFICATION_REQUIRED",
                    "reason": "Loan amount must be positive"}
        if app.loan_amount > MAX_LOAN_AMOUNT:
            if app.maximum_offer_accepted is True:
                app.loan_amount = MAX_LOAN_AMOUNT
            elif app.maximum_offer_accepted is False:
                return {"status": "NOT_PROCEEDING",
                        "reason": "Customer declined maximum offer"}
            else:
                return {"status": "MAXIMUM_OFFER_CONFIRMATION",
                        "reason": "Ask about ₹75 lakh alternative"}

    if app.occupation is not None:
        if app.occupation.strip().lower() not in ELIGIBLE_OCCUPATIONS:
            return {"status": "CLARIFICATION_REQUIRED",
                    "reason": "Clarify occupation"}

    if app.income_mode is not None:
        mode = app.income_mode.strip().lower()
        if mode == "cash":
            return {"status": "DISQUALIFIED",
                    "reason": "Income received in cash"}
        if mode in {"mixed", "unclear"}:
            return {"status": "CLARIFICATION_REQUIRED",
                    "reason": "Clarify mixed or unclear income mode"}
        if mode != "bank":
            return {"status": "CLARIFICATION_REQUIRED",
                    "reason": "Clarify income mode"}

    if app.tenure_years is not None:
        if not MIN_TENURE_YEARS <= app.tenure_years <= MAX_TENURE_YEARS:
            return {"status": "DISQUALIFIED",
                    "reason": "Tenure must be between 3 and 15 years"}

    required = [
        app.property_type, app.ownership,
        app.original_documents_available, app.loan_amount,
        app.occupation, app.income_mode, app.market_value,
        app.tenure_years,
    ]
    if any(value is None for value in required):
        return {"status": "INCOMPLETE",
                "reason": "Collect remaining checklist details"}

    return {"status": "PRELIMINARILY_ELIGIBLE",
            "reason": "All coded eligibility checks passed"}
