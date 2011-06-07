Impermium API bindings
======================

Usage::

    from impermium import ImpermiumAPI

    impermium = ImpermiumAPI(api_key=api_key)

    response = impermium.checkComment(event_id, {
        'uid_ref': '12341234',
        'resource_url': 'http://example.com',
        'content': 'Hello world!',
    })

    if response['spam']['label'] == 'spam':
        print "Uh oh, it's spam!"