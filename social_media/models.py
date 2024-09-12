from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class MemberManager(BaseUserManager):
    def create_member(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        member = self.model(email=email, **extra_fields)
        member.set_password(password)
        member.save(using=self._db)
        return member

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_member(email, password, **extra_fields)


class Member(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    friends = models.ManyToManyField('self', through="Friendship", symmetrical=False)
    objects = MemberManager()


class Friendship(models.Model):
    FRIEND_STATUSES = (
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending')
    )

    from_member = models.ForeignKey(Member, related_name='sent_requests', on_delete=models.CASCADE)
    to_member = models.ForeignKey(Member, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=FRIEND_STATUSES, default='Pending')

    class Meta:
        unique_together = ('from_member', 'to_member')
