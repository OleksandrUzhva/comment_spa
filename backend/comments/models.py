from django.core.validators import RegexValidator, URLValidator, EmailValidator
from django.db import models
from django.utils import timezone


latin_alnum_validator = RegexValidator(
    regex=r"^[A-Za-z0-9]+$",
    message="Use only Latin letters and digits for user name."
)


class Comment(models.Model):
    user_name = models.CharField(
        max_length=50,
        validators=[latin_alnum_validator],
        help_text="Latin letters and digits only."
    )
    email = models.EmailField(validators=[EmailValidator()])
    homepage = models.URLField(blank=True, null=True, validators=[URLValidator()])
    text = models.TextField()
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )
    is_blocked = models.BooleanField(default=False)  
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]  

    def __str__(self):
        return f"{self.user_name} ({self.email}) - {self.created_at.isoformat()}"