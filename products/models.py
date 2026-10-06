from django.db import models
from django.utils.translation import gettext_lazy as _

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    class Meta:
        abstract = True

class BaseModel(Timestamp):
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        ordering= ('name',)

    def __str__(self):
        return self.name

class Product(BaseModel):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveIntegerField()
    views_count = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    image = models.ImageField(upload_to='products-image/', blank=True, null=True, verbose_name='عکس پروفایل')
    store = models.ForeignKey("store.Store", on_delete=models.CASCADE, related_name='store')

    class Status(models.TextChoices):
        DRAFT = "draft", _("پیش نویس")
        PUBLISHED = "published", _("منتشر شده")
        ARCHIVED = "archived", _("آرشیو شده")

    status = models.CharField(max_length=11, choices=Status.choices, default=Status.DRAFT,verbose_name='وضعیت')

    def __str__(self):
        return f"name: {self.name} price:{self.price}"

    



