from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template.loader import render_to_string

META = {
    'appointment_reschedule': {
        'subject': 'Appointment Rescheduled',
        'template': 'appointment_reschedule',
    },
    'appointment_cancel': {
        'subject': 'Appointment Canceled',
        'template': 'appointment_cancel',
    },
}


class MailService(object):
    def send_mail(self, recipients, topic, context):
        mail_meta = META[topic]
        message = render_to_string(template_name=mail_meta['template'], context=context)
        if isinstance(list, recipients):
            recipients = [recipients]
        django_send_mail(
            mail_meta['subject'],
            html_message=message,
            from_email=mail_meta.get('from') or settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )


mail_service = MailService()
