from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from ckeditor.fields import RichTextField

from services.abstract_models import TimeStampedModel
from services.utils import create_unique_slug, EmptySlugError, SlugTooLongError

# Create your models here.


class BlogCategory(TimeStampedModel):
    title = models.CharField(
        verbose_name=_("Başlıq"),
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=255,
        unique=True,
        editable=False
    )
    is_active = models.BooleanField(
        verbose_name=_("Aktiv"),
        default=True
    )

    def save(self, *args, **kwargs):
        # Automatically fill slug field
        if not self.slug:
            self.slug = create_unique_slug(self, "title")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Kategoriya")
        verbose_name_plural = _("Kateqoriyalar")


class BlogPost(TimeStampedModel):
    title = models.CharField(
        max_length=20,
        verbose_name=_("Başlıq"),
    )
    content = RichTextField(
        verbose_name=_("Məzmun")
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        unique=True,
        editable=False,
        max_length=10
    )
    is_active = models.BooleanField(
        verbose_name=_("Aktiv"),
        default=True
    )

    def clean(self):
        if not self.slug:
            try:
                self.slug = create_unique_slug(self, "title", max_length=self._meta.get_field('slug').max_length)
            except EmptySlugError:
                raise ValidationError(_("Slug yaradılmadı. Başlıq məlumatını düzgün daxil edin."))
            except SlugTooLongError:
                raise ValidationError(_(f"Slug uzunluğu {self._meta.get_field('slug').max_length} simvoldan çox olmamalıdır."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if len(self.title) > 100:
            return f"{self.title[:100]}..."
        else:
            return self.title

    class Meta:
        verbose_name = _("Bloq")
        verbose_name_plural = _("Bloqlar")
