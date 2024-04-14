from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Event, Registration


class EventAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.event = Event.objects.create(
            name="Sample Event",
            description="Sample Description",
            date_time="2024-04-14T12:00:00Z",
            location="Sample Location",
            max_participants=50,
            organizer=self.user,
            created_by=self.user
        )
        # create an access token for the created user
        self.access_token = str(AccessToken.for_user(self.user))
        # authorize the client with the created token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_event(self):
        url = reverse('event-list')
        data = {
            "name": "New Event",
            "description": "New Description",
            "date_time": "2024-04-15T12:00:00Z",
            "location": "New Location",
            "max_participants": 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)  # check that two events are created

    def test_register_for_event(self):
        url = reverse('event-register', kwargs={'event_id': self.event.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cancel_registration(self):
        registration = Registration.objects.create(user=self.user, event=self.event, status='active')
        url = reverse('event-cancel', kwargs={'registration_id': registration.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        registration.refresh_from_db()
        self.assertEqual(registration.status, 'cancelled')  # check that registration is cancelled

    def test_retrieve_event(self):
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sample Event')  # check that only one event is returned

    def test_list_events(self):
        url = reverse('event-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # check that only one event is returned


"""
negative tests
"""


class EventAPITests(APITestCase):
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # get an access token for the created user
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_event_with_complete_data(self):
        """
        ensure that an event can be created with complete data
        """
        url = reverse('event-list')
        data = {
            'name': 'New Event',
            'description': 'Description of the event',
            'date_time': '2024-01-01T00:00:00Z',
            'location': 'Test Location',
            'max_participants': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_with_incomplete_data(self):
        """
        ensure that an event cannot be created with incomplete data
        """
        url = reverse('event-list')
        data = {'name': 'Incomplete Event'}  # incomplete data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_access_without_token(self):
        """
        check that an event cannot be accessed without a token
        """
        self.client.credentials()  # delete any existing token
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# run `./manage.py test`.