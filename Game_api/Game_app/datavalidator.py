import re
from .models import custom_user


def validate_User(user):
    datas = {}
    email_pattern = r'[a-zA-Z0-9][a-zA-Z0-9._]*@gmail[.]com'
    if email_pattern:
        if not re.match(email_pattern, user['email']):
            datas['error_message'] = 'Invalid email format'

    password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@?#$%^&+=]).{8,20}$"
    if password_pattern:
        if not re.match(password_pattern, user['password']):
            datas['error_message'] = 'this is Invalid password'

    if custom_user.objects.filter(username=user['username']).exists():
        datas['error_message'] = 'username is already exist'

    if custom_user.objects.filter(password=user['password']).exists():
        datas['error_message'] = 'password is already exist'

    if custom_user.objects.filter(email=user['email']).exists():
        datas['error_message'] = 'Email is already exist'

    return datas
