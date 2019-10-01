from django.contrib.messages import get_messages


def messages_to_list(response):
    """
    Get the messages out of the response
    """
    return [m.message for m in get_messages(response.wsgi_request)]
