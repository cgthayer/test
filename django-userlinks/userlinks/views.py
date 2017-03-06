from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from adventures.models import Adventure, Spot, Tip

from .models import UserLink
from .utils import model_to_content_type


def name_to_ct(name):
    if name == 'spot':
        return model_to_content_type(Spot)
    if name == 'adventure':
        return model_to_content_type(Adventure)
    if name == 'tip':
        return model_to_content_type(Tip)


######################################################################
# Likes

def like_get_ajax(request, target_type=None, target_id=None):
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
            content_type=name_to_ct(target_type),
            object_id=target_id,
        ).count()

    # for all users
    result['likes_count'] = UserLink.objects.filter(
        link_type=UserLink.LIKES,
        content_type=name_to_ct(target_type),
        object_id=target_id,
    ).count()
    
    return JsonResponse(result)
        

def _like(request, target_type, target_id, is_like):
    """Does the work for like"""
        
    likes = UserLink.objects.filter(
        user=request.user,
        link_type=UserLink.LIKES,
        content_type=name_to_ct(target_type),
        object_id=target_id,
    )
    # delete to clear out and reset updated_on times
    for like in likes:
        like.delete()

    if is_like:
        like = UserLink(
            user=request.user,
            link_type=UserLink.LIKES,
            content_type=name_to_ct(target_type),
            object_id=target_id,
        )
        like.save()

    return JsonResponse({})

@login_required
def like_save_ajax(request, target_type=None, target_id=None):
    if not target_type:
        target_type = request.GET.get('target_type')
    if not target_id:
        target_id = request.GET.get('target_id')
    return _like(request, target_type, target_id, is_like=True)

@login_required
def like_clear_ajax(request, target_type=None, target_id=None):
    if not target_type:
        target_type = request.GET.get('target_type')
    if not target_id:
        target_id = request.GET.get('target_id')
    return _like(request, target_type, target_id, is_like=False)


######################################################################
# Bookmarks / Saves

# todo: this moved to utils
@login_required
def bookmark_list_ajax(request):
    """output:
    bookmarks: a list of bookmarks for the user
    
    Each bookmark object has updated_on, target_table, target_id
    """
    result = {}

    if not request.user.is_authenticated or request.user.is_anonymous():
        return JsonResponse(result)

    bookmarks = UserLink.objects.filter(
        user=request.user,
        link_type=UserLink.BOOKMARKED,
    )

    result['bookmarks'] = bookmarks
    return JsonResponse(result)

@login_required
def bookmark_get_ajax(request, target_type=None, target_id=None):
    """output:
    is_bookmarked: set if logged in, 1 for true, 0 for not bookmarked
        by this user
    bookmarks_count:  number of users who have bookmarked this
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
            content_type=name_to_ct(target_type),
            object_id=target_id,
        ).count()
        
    # for all users
    result['bookmarks_count'] = UserLink.objects.filter(
        link_type=UserLink.BOOKMARKED,
        content_type=name_to_ct(target_type),
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
        # TODO: engagement
    else:
        pass
        # TODO: engagement
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
