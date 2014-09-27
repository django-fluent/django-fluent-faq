from fluent_utils.softdeps.fluent_pages import mixed_reverse


def faq_reverse(viewname, args=None, kwargs=None, current_app='fluent_faq', **page_kwargs):
    """
    Reverse a URL to the FAQ, taking various configuration options into account.

    This is a compatibility function to allow django-fluent-faq to operate stand-alone.
    Either the app can be hooked in the URLconf directly, or it can be added as a pagetype of *django-fluent-pages*.
    """
    return mixed_reverse(viewname, args=args, kwargs=kwargs, current_app=current_app, **page_kwargs)


__all__ = (
    'faq_reverse',
)
