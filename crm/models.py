from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True


class User(AbstractUser, TimeStampedModel):
    email = models.EmailField(_("email address"), unique=True)

    class Meta(AbstractUser.Meta):
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username


class Company(TimeStampedModel):
    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")

    def __str__(self) -> str:
        return self.name


class Customer(TimeStampedModel):
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    birthday = models.DateField(_("birthday"))
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='customers', verbose_name=_("company"))
    representative = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customers', verbose_name=_("representative"))

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['birthday']),
        ]
        ordering = ['last_name', 'first_name']

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Interaction(TimeStampedModel):
    class InteractionType(models.TextChoices):
        CALL = 'Call', _('Call')
        EMAIL = 'Email', _('Email')
        SMS = 'SMS', _('SMS')
        FACEBOOK = 'Facebook', _('Facebook')
        WHATSAPP = 'WhatsApp', _('WhatsApp')
        LINKEDIN = 'LinkedIn', _('LinkedIn')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions', verbose_name=_("customer"))
    interaction_type = models.CharField(_("interaction type"), max_length=50, choices=InteractionType.choices)
    date = models.DateTimeField(_("date"), default=timezone.now)

    class Meta:
        verbose_name = _("interaction")
        verbose_name_plural = _("interactions")
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['interaction_type']),
        ]
        ordering = ['-date']

    def __str__(self) -> str:
        return f"{self.get_interaction_type_display()} with {self.customer} on {self.date}"
