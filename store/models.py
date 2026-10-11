from django.db import models

class BusinessType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='حوزه فعالیت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Store(models.Model):
    business_type = models.ForeignKey(BusinessType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name= 'حوزه فعالیت', related_name="stores")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    seller = models.ForeignKey('profiles.sellerprofile', on_delete=models.CASCADE, related_name="stores")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
