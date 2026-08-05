def company_context(request):
    if request.user.is_authenticated:
        return {"company": request.user.company}
    return {}