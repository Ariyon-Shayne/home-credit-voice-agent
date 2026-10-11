import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from eligibility import LAPApplication, validate_lap_application


def eligible_app(**overrides):
    values = dict(
        property_type="residential",
        ownership="joint",
        original_documents_available=True,
        loan_amount=5_000_000,
        occupation="salaried",
        income_mode="bank",
        market_value=10_000_000,
        tenure_years=10,
    )
    values.update(overrides)
    return LAPApplication(**values)


class EligibilityTests(unittest.TestCase):
    def test_eligible_customer(self):
        self.assertEqual(validate_lap_application(eligible_app())["status"],
                         "PRELIMINARILY_ELIGIBLE")

    def test_agricultural_disqualified(self):
        self.assertEqual(validate_lap_application(
            eligible_app(property_type="agricultural"))["status"],
            "DISQUALIFIED")

    def test_cash_income_disqualified(self):
        self.assertEqual(validate_lap_application(
            eligible_app(income_mode="cash"))["status"],
            "DISQUALIFIED")

    def test_missing_originals_disqualified(self):
        self.assertEqual(validate_lap_application(
            eligible_app(original_documents_available=False))["status"],
            "DISQUALIFIED")

    def test_tenure_below_range(self):
        self.assertEqual(validate_lap_application(
            eligible_app(tenure_years=2))["status"], "DISQUALIFIED")

    def test_tenure_above_range(self):
        self.assertEqual(validate_lap_application(
            eligible_app(tenure_years=16))["status"], "DISQUALIFIED")

    def test_exact_maximum_accepted(self):
        self.assertEqual(validate_lap_application(
            eligible_app(loan_amount=7_500_000))["status"],
            "PRELIMINARILY_ELIGIBLE")

    def test_over_limit_requires_confirmation(self):
        self.assertEqual(validate_lap_application(
            eligible_app(loan_amount=9_000_000))["status"],
            "MAXIMUM_OFFER_CONFIRMATION")

    def test_over_limit_accepted_caps_amount(self):
        app = eligible_app(
            loan_amount=9_000_000, maximum_offer_accepted=True
        )
        self.assertEqual(validate_lap_application(app)["status"],
                         "PRELIMINARILY_ELIGIBLE")
        self.assertEqual(app.loan_amount, 7_500_000)

    def test_over_limit_declined(self):
        self.assertEqual(validate_lap_application(eligible_app(
            loan_amount=9_000_000, maximum_offer_accepted=False
        ))["status"], "NOT_PROCEEDING")

    def test_transfer_referral(self):
        self.assertEqual(validate_lap_application(eligible_app(
            existing_property_loan=True
        ))["status"], "TRANSFER_REFERRAL")

    def test_missing_fields_incomplete(self):
        self.assertEqual(validate_lap_application(
            LAPApplication(property_type="residential"))["status"],
            "INCOMPLETE")

    def test_joint_ownership_allowed(self):
        self.assertEqual(validate_lap_application(
            eligible_app(ownership="joint"))["status"],
            "PRELIMINARILY_ELIGIBLE")


if __name__ == "__main__":
    unittest.main()
