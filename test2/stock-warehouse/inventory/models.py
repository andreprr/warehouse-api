from django.db import models
from django.utils import timezone

# Base Model
class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True  # Tidak membuat tabel, hanya untuk inheritance

    def delete(self, *args, **kwargs):
        """Override delete untuk soft delete"""
        self.is_deleted = True
        self.save()

# Custom manager untuk filter hanya item yang tidak dihapus
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# Modul Item
class Item(BaseModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    balance = models.BigIntegerField(default=0)

    objects = ActiveManager()  # hanya ambil data yang aktif
    all_objects = models.Manager()  # ambil semua data (termasuk soft deleted)

    def __str__(self):
        return f"{self.code} - {self.name}"

# Modul Purchase
class PurchaseHeader(BaseModel):
    code = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code

class PurchaseDetail(BaseModel):
    header = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name='details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Hitung total harga
        total = self.quantity * self.unit_price

        # Update stock & balance item
        if not self.pk:  # Jika ini create (bukan update)
            self.item.stock += self.quantity
            self.item.balance += total
            self.item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.header.code} - {self.item.code}"


# Modul Sell
class SellHeader(BaseModel):
    code = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class SellDetail(BaseModel):
    header = models.ForeignKey(SellHeader, on_delete=models.CASCADE, related_name='details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:  # hanya saat create
            if self.item.stock < self.quantity:
                raise ValueError("Insufficient stock for item: " + self.item.code)

            # untuk sementara kita kurangi langsung balance rata-rata
            avg_price = self.item.balance // self.item.stock if self.item.stock else 0
            total_cut = avg_price * self.quantity

            self.item.stock -= self.quantity
            self.item.balance -= total_cut
            self.item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.header.code} - {self.item.code}"
