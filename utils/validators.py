import re
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validate_password(password):
    password_reg = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,13}$"
    password_regex = re.compile(password_reg)

    if not password_regex.match(password):
        raise ValidationError("영문, 숫자, 특수문자 조합해 6자 이상, 13자 이하 입력해주세요.")
    
def validate_email(email):
    email_reg = r"^[a-zA-Z0-9_-]{6,13}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    email_regex = re.compile(email_reg)

    if not email_regex.match(email):
        raise ValidationError("이메일 형식이 잘못되었습니다. 아이디는 6자 이상 13자 이하로 작성하고, 특수 문자는 _와 -만 사용 가능합니다.")