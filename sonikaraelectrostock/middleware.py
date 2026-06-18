from django.shortcuts import render


class DesktopOnlyMiddleware:

    def __init__(
        self,
        get_response
    ):

        self.get_response = (
            get_response
        )


    def __call__(
        self,
        request
    ):

        user_agent = (
            request.user_agent
        )


        if (

            user_agent.is_mobile

            or

            user_agent.is_tablet

        ):

            return render(

                request,

                'layout/desktop_only.html',

                status=403

            )


        return (

            self.get_response(
                request
            )

        )