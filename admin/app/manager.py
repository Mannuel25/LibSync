from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):

        if not email:
            raise ValueError("Kindly enter an email address for this user.")

        # now create the user, using the given email and password
        user = self.model(
            email=self.normalize_email(email.lower()),
            username=self.normalize_email(email.lower()),
            **extra_fields
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        if password is None:
            raise ValueError("Kindly enter a valid password for this superuser.")

        # now create the superuser, using the given email and password
        user = self.create_user(email, password)
        user.is_superuser = user.is_active = user.is_staff = True
        user.save()
        return user
