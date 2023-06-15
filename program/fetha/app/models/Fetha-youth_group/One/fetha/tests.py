import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Person, Group, Membership

class MembershipModelTest(TestCase):
    def test_was_published_recently_with_future_person(self):
        """
        was_published_recently() returns False for Person whose date_joined is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_person = Membership(date_joined=time)
        self.assertIs(future_person.was_published_recently(), False)

    def test_was_published_recently_with_old_person(self):
        """
        was_published_recently() returns False for person whose date_joined is older than one day.
        """
        time = timezone.now() -datetime.timedelta(days=1, seconds=1)
        old_person = Membership(date_joined=time)
        self.assertIs(old_person.was_published_recently(), False)

    def test_was_published_recently_with_recent_person(self):
        """
        was_published_recently() returns True for person whose datejoined is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_person = Membership(date_joined=time)
        self.assertIs(recent_person.was_published_recently(), True)
    
def create_person(name, days):
    """
    Create a person with the given `person_name` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Person.objects.create(name = name, date_joined = time)

class PersonIndexViewTests(TestCase):
    def test_no_person(self):
        """
        If no person exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('fetha:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.client['latest_person_list'], [])

    def test_past_person(self):
        """
        Person with a joined_date in the future aren't displayed on the index page.
        """
        person = create_person(name="Past person.", days=-30)
        response = self.client.get(reverse('fetha:index'))
        self.assertQuerysetEqual(
            response.context['latest_person_list'],
            [person],
        )

    def test_future_person(self):
        """
        Person with a joined_date in the future aren't displayed on the index page.
        """
        create_person(name="Future person.", days=30)
        response = self.client.get(reverse('fetha:index'))
        self.assertContains(response, "No app available.")
        self.assertQuerysetEqual(response.context['latest_person_list'], [])

    def test_future_person_and_past_person(self):
        """
        Even if both past and future person exist, only past questions
        are displayed.
        """
        person = create_person(name="Past person.", days=-30)
        create_person(name="Future person.", days=30)
        response = self.client.get(reverse('fetha:index'))
        self.assertQuerysetEqual(
            response.context['latest_person_list'],
            [person],
        )
    def test_two_past_person(self):
        """
        The questions index page may display multiple questions.
        """
        person1 = create_person(name="Past person 1", days=-30)
        person2 = create_person(name="Past person 2", days=-5)
        response = self.client.get(reverse('fetha:index'))
        self.assertQuerysetEqual(
            response.context['latest_person_list'],
            [person2, person1],
        )

class PersonDetailViewTests(TestCase):
    def test_future_person(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_person = create_person(name= 'Future Person.', days=5)
        url = reverse('fetha:detail', args=(future_person.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def test_past_person(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_person = create_person(name='Past Person.', days=-5)
        url = reverse('fetha:detail', args=(past_person.id,))
        response = self.client.get(url)
        self.assertContains(response, past_person.person_name)