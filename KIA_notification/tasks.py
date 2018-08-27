from datetime import timedelta

from background_task import background

from KIA_admin.models import SystemCredit
from KIA_auth.models import Profile
from KIA_notification.views import send_mail_to_user, send_mail_to_admin
from KIA_services.models import KIATransaction


@background(schedule=timedelta(days=1))
def plan_transaction_expiration(transaction):
    if transaction.state == KIATransaction.registered:
        transaction.delete()
        message = "متاسفانه درخواست شما برای خدمت" + transaction.service.label + "به دلیل شلوغی " + \
                  "سامانه رد شد، درخواست خود را مجددا ثبت نمایید"
        send_mail_to_user(transaction.user, "به فنا رفتن درخواست", message)


@background(schedule=timedelta(days=30))
def plan_employee_wage(employee):
    employee.credit += 100000
    sc = SystemCredit.objects.get(owner="system")
    sc.rial_credit -= 100000


@background(schedule=timedelta(days=1))
def system_credit_alert():
    sc = SystemCredit.objects.get(owner="system")
    if sc.rial_credit <= 10000000:
        subject = "اخطار کمبود موجودی"
        message = "موجودی حساب‌ ریالی سامانه رو به کاهش است، به منظور افزایش آن‌ها اقدام کنید."
        send_mail_to_admin(subject, message)


@background(schedule=5)
def test_notif():
    print("Hello world!")
