from django.conf import settings
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
signer = TimestampSigner()

def generate_email_token(user):
    return signer.sign(user.pk)  # 사용자 ID를 토큰으로 서명

def verify_email_token(token, max_age=3600):
    try:
        user_id = signer.unsign(token, max_age=max_age)  # 1시간(3600초) 유효
        return user_id
    except (BadSignature, SignatureExpired):
        return None

def send_verification_email(user, request):
    from django.urls import reverse

    token = user.email_verification_token
    verification_url = request.build_absolute_uri(reverse('verify-email')) + f'?token={token}'

    subject = "Email Verification"
    message = f"Hello {user.name},\n\nPlease verify your email by clicking the link below:\n{verification_url}"
    send_mail(subject, message, 'no-reply@example.com', [user.email])
