from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save,sender=Payment)
def send_mail_to_user(sender,instance,created,**kwargs):
    user_email = User.objects.get(id = instance.user.id).email
    if created:
        html_file = get_template("payment_done.html")
        html_content = html_file.render()
        subject = "Payment"
        message = "Email Body"
        from_email = "aaaladoc@gmail.com"
        recipient_list = [user_email]
        email = EmailMultiAlternatives(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                )
        email.attach_alternative(html_content, "text/html")
        email.send()
    else:
        if instance.is_verified and instance.appointment_date_time is not None:
            context ={
            'doctor_name': instance.doctor.name(),
            'doctor_email' : instance.doctor.email(),
            'specialization' : instance.doctor.specialization,
            "appointment":instance.appointment_date_time
            }
            html_file = get_template("payment_verified.html")
            html_content = html_file.render(context)
            subject = "Payment Verification"
            message = "Email Body"
            from_email = "aaaladoc@gmail.com"
            recipient_list = [user_email]
            email = EmailMultiAlternatives(
                        subject,
                        message,
                        from_email,
                        recipient_list,
                    )
            email.attach_alternative(html_content, "text/html")
            email.send()
