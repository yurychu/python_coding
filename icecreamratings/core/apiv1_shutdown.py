from django.http import HttpResponseGone


apiv1_gone_msg = """APIv1 удалено 2 апреля, пожалуйста перейдите на APIv3:
<ul>
    <li>
        <a href="https://www.example.com/api/v3/">APIv3 Endpoint</a>
    </li>
    <li>
        <a href="/apiv3_docs/">APIv3 Documentation</a>
    </li>
    <li>
        <a href="/apiv1_shutdown/">APIv1 shut down notice</a>
    </li>
</ul>
"""


def apiv1_gone(request):
    return HttpResponseGone(apiv1_gone_msg)
