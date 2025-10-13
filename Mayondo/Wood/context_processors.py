def user_role(request):
    # Safely get the role from the logged-in user
    role = getattr(request.user, 'role', None)
    return {'user_role': role}
