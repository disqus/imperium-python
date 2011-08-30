Impermium API bindings
======================

API Version 2.0
---------------

::

    from impermium import ImpermiumAPI

    impermium = ImpermiumAPI(api_key=api_key, version='3.0')

    response = impermium.checkComment(event_id, {
        'uid_ref': '12341234',
        'resource_url': 'http://example.com',
        'content': 'Hello world!',
    })

    if response['spam']['label'] == 'spam' and float(response['spam']['confidence_score]) >= 0.75:
        print "Uh oh, it's spam!"

API Version 3.0
---------------

::

    from impermium import ImpermiumAPI

    impermium = ImpermiumAPI(api_key=api_key, version='3.0')

    response = impermium.checkComment(params={
        'user_id': '12341234',
        'comment_id': event_id,
        'resource_url': 'http://example.com',
        'comment': 'Hello world!',
    })
