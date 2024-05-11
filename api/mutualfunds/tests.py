from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from mutualfunds.importers.cas import import_cas
from mutualfunds.models import Portfolio, FundScheme, Folio, Transaction

class TestImportCas(TestCase):

    def setUp(self):
        # Mock data setup
        self.data = {
            "investor_info": {"email": "test@example.com", "name": "Test User"},
            "folios": [],
            "statement_period": {"from": "2021-01-01", "to": "2021-01-31"}
        }
        self.user_id = 1

    def test_import_cas_valid_email_name(self):
        # Test case for valid email and name
        Portfolio.objects.create(email="test@example.com", name="Test User", user_id=self.user_id)
        result = import_cas(self.data, self.user_id)
        self.assertIsNotNone(result)

    def test_import_cas_invalid_email(self):
        # Test case for invalid email
        self.data["investor_info"]["email"] = ""
        with self.assertRaises(ValueError):
            import_cas(self.data, self.user_id)

    def test_import_cas_new_folio_creation(self):
        # Test case for creating a new folio
        self.data["folios"] = [{"amc_id": "123", "folio": "F123", "PANKYC": "ok", "PAN": "ABC123"}]
        with self.assertRaises(ObjectDoesNotExist):
            import_cas(self.data, self.user_id)
        self.assertEqual(Folio.objects.count(), 1)

    # Additional test cases can be added here to cover other functionalities
