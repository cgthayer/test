from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .models import UserLink
from .utils import model_to_ct

######################################################################
# Likes

def like_get_ajax(request, target_type=None, target_id=None):
    """Ajax/Json gets counts of likes where result has members:
    is_liked: set if logged in, 1 for true, 0 for not bookmarked
        by this user
    likes_count: number of users who have bookmarked this
    """
    
    result = {}
    if not target_type:
        target_type = request.GET.get('target_type')
    if not target_id:
        target_id = request.GET.get('target_id')

    # likes for this user
    if not request.user.is_anonymous():
        result['is_liked'] = UserLink.objects.filter(
            user=request.user,
            link_type=UserLink.LIKES,
            content_type=model_to_ct(target_type),
            object_id=target_id,
        ).count()

    # for all users
    result['likes_count'] = UserLink.objects.filter(
        link_type=UserLink.LIKES,
        content_type=model_to_ct(target_type),
        object_id=target_id,
    ).count()
    
    return JsonResponse(result)
        

def _like(request, target_type, target_id, is_like):
    """Does the work for like-ing or un-like-ing.
    Assumes a real logged in user.  Non-atomic but
    isolated to a single user.
    """
    likes = UserLink.objects.filter(
        user=request.user,
        link_type=UserLink.LIKES,
        content_type=model_to_ct(target_type),
        object_id=target_id,
    )
    # delete to clear out and reset updated_on times
    for like in likes:
        like.delete()

    if is_like:
        like = UserLink(
            user=request.user,
            link_type=UserLink.LIKES,
            content_type=model_to_ct(target_type),
            object_id=target_id,
        )
        like.save()

    # TODO: add signal
    return JsonResponse({})

@login_required
def like_save_ajax(request, target_type=None, target_id=None):
    """Call for a user to like an object"""
    if not target_type:
        target_type = request.GET.get('target_type')
    if not target_id:
        target_id = request.GET.get('target_id')
    return _like(request, target_type, target_id, is_like=True)

@login_required
def like_clear_ajax(request, target_type=None, target_id=None):
    """Call for a user to unlike an object"""
    if not target_type:
        target_type = request.GET.get('target_type')
    if not target_id:
        target_id = request.GET.get('target_id')
    return _like(request, target_type, target_id, is_like=False)


######################################################################
# Bookmarks / Saves

@login_required
def bookmark_list_ajax(request):
    """Returns a list of bookmarks (result['bookmarks']) for the current user.

    Each bookmark object has updated_on, content_type (int), name (of
    content_type), model (name), object_id

    """
    result = {}

    if not request.user.is_authenticated or request.user.is_anonymous():
        return JsonResponse(result)

    bookmarks = UserLink.objects.filter(
        user=request.user,
        link_type=UserLink.BOOKMARKED,
    )
    for b in bookmarks:
        b.name = b.content_type.name
        b.model = b.content_type.model

    result['bookmarks'] = bookmarks
    return JsonResponse(result)


@login_required
def bookmark_get_ajax(request, target_type=None, target_id=None):
    """Ajax/Json gets counts of bookmarks where result has members:
    is_bookmarked: set if logged in, 1 for true, 0 for not bookmarked
        by this user
    bookmarks_count: number of users who have bookmarked this
    """
    result = {}
    if not target_type:
        target_type = request.GET.get('target_type')
    if not target_id:
        target_id = request.GET.get('target_id')

    # likes for this user
    if not request.user.is_anonymous():
        result['is_bookmarked'] = UserLink.objects.filter(
            user=request.user,
            link_type=UserLink.BOOKMARKED,
            content_type=model_to_ct(target_type),
            object_id=target_id,
        ).count()
        
    # for all users
    result['bookmarks_count'] = UserLink.objects.filter(
        link_type=UserLink.BOOKMARKED,
        content_type=model_to_ct(target_type),
        object_id=target_id,
    ).count()
    
    return JsonResponse(result)
        
@login_required
def _bookmark(request, target_type, target_id, set_bookmarked):
    """Does the work for bookmarking (saving)"""
    bookmarks = UserLink.objects.filter(
        user=request.user,
        link_type=UserLink.BOOKMARKED,
        content_type=name_to_ct(target_type),
        object_id=target_id,
    )

    # delete to clear out old to reset updated_on times
    for b in bookmarks:
        b.delete()

    if set_bookmarked:
        bookmark = UserLink(
            user=request.user,
            link_type=UserLink.BOOKMARKED,
            content_type=name_to_ct(target_type),
            object_id=target_id,
        )
        bookmark.save()

    # TODO: add signal
    return JsonResponse({})


@login_required
def bookmark_save_ajax(request, target_type=None, target_id=None):
    if not target_type:
        target_type = request.GET.get('target_type')
    if not target_id:
        target_id = request.GET.get('target_id')
    return _bookmark(request, target_type, target_id, set_bookmarked=True)

@login_required
def bookmark_clear_ajax(request, target_type=None, target_id=None):
    if not target_type:
        target_type = request.GET.get('target_type')
    if not target_id:
        target_id = request.GET.get('target_id')
    return _bookmark(request, target_type, target_id, set_bookmarked=False)
