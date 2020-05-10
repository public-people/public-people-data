from django.conf import settings


def google_tag_manager(request):
    """
    Add the Google Tag Manager ID and domain to the context for use when
    rendering tracking code.
    """
    google_tag_mgr_id = getattr(settings, 'GOOGLE_TAG_MGR_ID', False)
    if not settings.DEBUG and google_tag_mgr_id:
        return {
            'GOOGLE_TAG_MGR_ID': google_tag_mgr_id,
        }
    return {}
