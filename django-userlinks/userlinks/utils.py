import logging
import six

from django.contrib.contenttypes.models import ContentType, ContentTypeManager

from .models import UserLink

LOG = logging.getLogger(__name__)

## These functions are mainly used internally

def name_to_type(name):
    """Returns the ContentType for a name like 'auth_user' or 'auth.user'.  Two
    formats to help with js and python code syntax.
    """
    
    if '_' in name:
        (app_label, model_name) = name.split('_', 2)
    else:
        (app_label, model_name) = name.split('.', 2)
    return ContentType.objects.get(app_label=app_label, model=model_name)


def modelclass_to_contenttype(model_class):
    """Given a model_class return the generic contenttype"""
    return ContentType.objects.get_for_model(model_class)


def model_to_ct(nm_or_class):
    """Get the model's ContentType. 
    Let's us take string name or Class object and find the ContentType
    """
    if isinstance(nm_or_class, six.string_types):    # py2 vs py3
        return name_to_type(nm_or_class)
    return modelclass_to_contenttype(nm_or_class)
    

## These are the main public API

def get_bookmarks(user, target_model=None):
    """Returns the links which a user bookmarked. Can limited to a specific type"""
    if not user.is_authenticated or user.is_anonymous():
        return None

    if target_model:
        return UserLink.objects.filter(
            user=user,
            link_type=UserLink.BOOKMARKED,
            content_type=model_to_ct(target_model)
        )

    return UserLink.objects.filter(
        user=user,
        link_type=UserLink.BOOKMARKED,
    )


def get_bookmarked_objects(user, target_model=None):
    """Returns objects which a user bookmarked. Can be limited to a specific type"""
    links = get_bookmarks(user, target_model)
    return [l.content_object for l in links]


def get_likes(user, target_model=None):
    """Returns the links which a user liked. Can limited to a specific type"""
    if not user.is_authenticated or user.is_anonymous():
        LOG.warn("user not auth or is_anon: {}".format(user))
        return None
    
    if target_model:
        return UserLink.objects.filter(
            user=user,
            link_type=UserLink.LIKES,
            content_type=model_to_content_type(target_model),
        )
    return UserLink.objects.filter(
        user=user,
        link_type=UserLink.LIKES,
    )

def get_liked_objects(user, target_model=None):
    """Returns objects which a user liked. Can be limited to a specific type"""
    links = get_likes(user, target_model)
    return [l.content_object for l in links]

def get_links(target_model, target_id):
    """Return a list of links to  this target_table/target_id combo by anyone"""
    content_type=model_to_content_type(target_model)
    return UserLink.objects.filter(
        content_type=model_to_content_type(target_model),
        object_id=target_id,
    )

def who_cares(target_model, target_id):
    """Who cares about type/id.
    Get's the list of users that have linked to a specific object
    """
    links = get_links(target_model, target_id)
    users = [link.user for link in links]
    return users
