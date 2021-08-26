""" Views used by user to show their profile, etc.   """

# Django core imports
from django.shortcuts import render, redirect

# Third-party imports

# App imports
from jobs_backend.app.models import User, Application

# View for showing a users profile
def ProfileView(request, pk):

    # Getting the actual PK for the user requesting the view
    user_pk = request.user.pk

    # Getting the PK for the view requested by the URL (e.g. localhost/user/1)
    browser_pk = pk

    # Getting the object for the user requesting the view
    user = User.objects.get(pk=user_pk)

    # Check if user is authenticated, if not, redirect to login-page
    if request.user.is_authenticated == False:
        return redirect("/login")

    # If user is authenticated...
    else:

        # If user has requested someone elses profile page, redirect to their own profile page
        if user_pk != browser_pk:
            return redirect("/profile/" + str(user_pk))

        # If user has requested his own page, return all their applications
        else:
            applications = Application.objects.filter(applicant=user)
            return render(
                request,
                "main/profile/profile.html",
                {"applications": applications, "user": user},
            )
