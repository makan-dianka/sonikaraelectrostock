def percentage_change(current, previous):

    if previous == 0:

        if current > 0:

            return 100

        return 0

    return round(

        (

            (

                current

                -

                previous

            )

            /

            previous

        )

        *

        100,

        2

    )