from django.test import TestCase
# The below code was deprecated in Django 2.0
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.urls import resolve
from .views import board_topics, home, new_topic

from .models import Board

# NOTE
# 1. reverse(view_name) returns an url corresponding to a view
# 2. resolve(url) returns an view object containing the function
#    'func' which is the view that was triggerd while resolving
#    url


# Tests on url(name="home")
class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name="Django", description="Django board.")
        url = reverse("home")
        # We save the response such that it can be
        # reused in the other methods as well
        self.response = self.client.get(url)

    # Checking if the view named home
    # exists and returns a status 200 (Success)
    def test_home_view_status_code(self):
        # The below two lines are not needed as we
        # store the response in self.response in the
        # setUp() method

        # url = reverse('home')
        # response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    # Checking if the url "/" resolves to
    # view.home
    def test_home_url_resolves_home_view(self):
        view = resolve("/")
        self.assertEquals(view.func, home)

    # Checking if the home page contains links to the
    # board topics
    def test_home_view_contains_links_to_topics_page(self):
        board_topics_url = reverse(
            "board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(
            self.response, 'href="{0}"'.format(board_topics_url))


# Tests on url(name="board_topics")
class BoardTopicsTest(TestCase):
    # To set up the testing database
    # NOTE: production and testing database
    # are different
    def setUp(self):
        Board.objects.create(name="Django", description="Django board.")

    # Check if the board_topics view can successfully
    # return the data corresponding to pk=1
    def test_board_topics_view_success_status_code(self):
        url = reverse("board_topics", kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # Check if the board_topics view correctly raises an
    # Http404 error if board corresponding to pk=99
    # is requested
    def test_board_topics_view_not_found_status_code(self):
        url = reverse("board_topics", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # Check to see if the url '/board/1' resolves to a
    # correct view i.e. board_topics
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1')
        self.assertEquals(view.func, board_topics)

    # Checking to see if the view contains a link back to the
    # homepage
    def test_board_topics_views_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={"pk": 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse("home")
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    # Checking to see if the board topics page ex. "board/1" contains
    # links to both homepage and new topic creation page
    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={"pk": 1})
        homepage_url = reverse("home")
        new_topic_url = reverse('new_topic', kwargs={"pk": 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicsTest(TestCase):
    # To set up the testing database
    # NOTE: production and testing database
    # are different
    def setUp(self):
        Board.objects.create(name="Django", description="Django board.")

    # Check if the new_topic view can successfully
    # return the data corresponding to pk=1
    def test_new_topic_view_success_status_code(self):
        url = reverse("new_topic", kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # Check if the new_topic view correctly raises an
    # Http404 error if board corresponding to pk=99
    # is requested
    def test_new_topic_view_not_found_status_code(self):
        url = reverse("new_topic", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # Check to see if the url '/board/1/new' resolves to a
    # correct view i.e. new_topic
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/new')
        self.assertEquals(view.func, new_topic)

    # Checking to see if the view contains a link back to the
    # board_topics view
    def test_new_topic_views_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={"pk": 1})
        response = self.client.get(new_topic_url)
        board_topics_url = reverse('board_topics', kwargs={"pk": 1})
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
