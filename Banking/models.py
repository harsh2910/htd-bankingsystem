from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=64, null=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    ballance = models.IntegerField(default=10000)
    
    def __str__(self):
        return f"{self.name} | {self.email} | {self.ballance}"

class Transaction(models.Model):
    sender = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="credit")
    recipient = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="debit")
    amount = models.IntegerField()
    status = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.name} to {self.recipient.name} Rs{self.amount}, Status:{self.status}"