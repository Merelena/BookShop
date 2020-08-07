from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, first_name, last_name, city, address, phone_number, email):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.city = city
        user.address = address
        user.phone_number = phone_number
        password = make_random_password()
        user.set_password(password)
        user.save()
        send_mail('Книжный магазин BookShop приветствует Вас!',
                  f'Уважаемый(ая) {first_name} {last_name}, вы зарегистрировались на сайте BookShop.\n'
                  f'Пароль для входа на Ваш аккаунт: {password}', 'your@support.com', [email],
                  fail_silently=False)
        return user

    def create_superuser(self, first_name, last_name, city, address, phone_number, email):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            city=city,
            address=address,
            phone_number=phone_number
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


def make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    from random import choice
    return ''.join([choice(allowed_chars) for i in range(length)])