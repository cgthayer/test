from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import UserLink
from .utils import (
    model_to_ct,
    get_bookmarks, get_likes, get_links, who_cares,
)

class LinkTests(TestCase):
    user = None
    other_user = None   # need to refer to later

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="tester",
            password="testtest",
        )
        cls.user.save()

        # make user like other_user
        other_user = User.objects.create_user(
            username="norma",
            password="testtest",
        )
        cls.other_user = other_user
        other_user.save()

        like_link = UserLink(
            user=cls.user,
            link_type=UserLink.LIKES,
            content_type=model_to_ct(User),
            content_object=other_user,
            object_id=other_user.id,
        )
        like_link.save()

        # setup a bookmark from user to user_carl
        user_carl = User.objects.create_user(
            username="carl",
            password="testtest",
        )
        cls.user_carl = user_carl
        user_carl.save()

        bookmark_link = UserLink(
            user=cls.user,
            link_type=UserLink.BOOKMARKED,
            content_type=model_to_ct(User),
            content_object=user_carl,
            object_id=user_carl.id,
        )
        bookmark_link.save()
        
    def setUp(self):
        # self.factory = RequestFactory()
        pass

    def test_like(self):
        self.assertTrue(UserLink.objects.count() > 0)
        likes = get_likes(LinkTests.user)
        self.assertTrue(len(likes) > 0)
        likes = get_likes(LinkTests.user, User)
        self.assertTrue(len(likes) > 0)

    def test_bookmarks(self):
        bookmarks = get_bookmarks(LinkTests.user, User)
        self.assertTrue(len(bookmarks) > 0)
        
    def test_who_cares(self):
        users = who_cares(User, 456789)
        self.assertFalse(users)
        users = who_cares(User, self.other_user.id)
        self.assertTrue(len(users) == 1)
        self.assertTrue(LinkTests.user in users)

        users = who_cares(User, self.user_carl.id)
        self.assertTrue(len(users) == 1)
        self.assertTrue(LinkTests.user in users)



    
