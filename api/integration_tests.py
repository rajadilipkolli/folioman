from unittest.mock import patch
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from mutualfunds.models import Portfolio, FundScheme, FundCategory, AMC

class FoliomanIntegrationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        self.portfolio = Portfolio.objects.create(user=self.user, name='Main Portfolio', email='test@example.com')
        
        # Setup basic data for mutualfunds
        self.amc = AMC.objects.create(name='Test AMC', code='TESTAMC')
        self.category = FundCategory.objects.create(type='EQUITY', subtype='Large Cap')
        self.scheme = FundScheme.objects.create(
            sid=1, name='Test Scheme', isin='INF123456789', 
            rta='CAMS', amc=self.amc, amc_code='101', category=self.category
        )

    def test_login_success(self):
        url = '/api/auth/login'
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure(self):
        url = '/api/auth/login'
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_view_authenticated(self):
        # Generate token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(len(response.data['user']['portfolios']['mutualfunds']), 1)

    def test_user_view_unauthenticated(self):
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_blacklist_token(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = '/api/auth/logout'
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify token is blacklisted by trying to refresh
        url_refresh = '/api/auth/refresh'
        response_refresh = self.client.post(url_refresh, data, format='json')
        self.assertEqual(response_refresh.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_portfolio_list(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = '/api/mutualfunds/portfolio/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Main Portfolio')

    @patch('mutualfunds.importers.cas.fetch_nav.delay')
    def test_cas_import_mock(self, mock_fetch_nav):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = '/api/mutualfunds/cas/import'
        # Mock data structure matching casparser output
        mock_data = {
            "data": {
                "investor_info": {"email": "test@example.com", "name": "Main Portfolio"},
                "statement_period": {"from": "2024-01-01", "to": "2024-01-31"},
                "folios": [
                    {
                        "folio": "12345/67",
                        "PAN": "ABCDE1234F",
                        "KYC": "OK",
                        "PANKYC": "OK",
                        "schemes": [
                            {
                                "scheme": "Test Scheme",
                                "isin": "INF123456789",
                                "amfi": "123456",
                                "advisor": "UNIT",
                                "rta_code": "101",
                                "rta": "CAMS",
                                "open": 0.0,
                                "close": 100.0,
                                "close_calculated": 100.0,
                                "valuation": {"date": "2024-01-01", "nav": 50.0, "value": 5000.0},
                                "transactions": [
                                    {
                                        "date": "2024-01-01",
                                        "description": "Purchase",
                                        "amount": 5000.0,
                                        "units": 100.0,
                                        "nav": 50.0,
                                        "balance": 100.0,
                                        "type": "PURCHASE"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        response = self.client.post(url, mock_data, format='json')
        if response.status_code != 200:
            print(f"Error Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['num_folios'], 1)
        self.assertTrue(mock_fetch_nav.called)
