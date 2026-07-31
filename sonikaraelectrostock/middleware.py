from django.shortcuts import render, redirect


class DesktopOnlyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.user_agent
        if user_agent.is_mobile or user_agent.is_tablet:
            return render(request, 'layout/desktop_only.html', status=403)

        return self.get_response(request)



class SubscriptionMiddleware:

    EXEMPT_PREFIXES = [
        "/sonikaraelec/",
        "/admin/",
        "/accounts/login/",
        "/accounts/logout/",
        "/subscriptions/",
        "/static/",
        "/media/",
        "/favicon.ico",
        "/robots.txt",
        "/accounts/profile",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if any(request.path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return self.get_response(request)

        company = getattr(request.user, "company", None)
        if company is None:
            return self.get_response(request)

        subscription = getattr(company, "subscription", None)
        if subscription is None:
            return redirect("subscriptions:expired")

        if not subscription.is_valid():
            return redirect("subscriptions:expired")

        return self.get_response(request)