from slurmui.views import perform_logout, get_default_context

def logout_handler(func, request):
    """
    Performs logout handling before execution of the function.
    """
    context = {}

    if request.method == 'GET':
        request, context = perform_logout(request)

    context.update(get_default_context(request))

    login_disabled = not context['logged_in']
    context.update({'login_disabled': login_disabled, })

    return func(request, context=context)
