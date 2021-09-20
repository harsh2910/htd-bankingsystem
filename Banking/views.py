from django.shortcuts import render
from .models import User, Transaction
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

def index(request):
    return render(request, "Banking/index.html")

def customers(request):
    customers = User.objects.order_by('id')
    return render(request, "Banking/customers.html", {
        "customers": customers,
    })

def history(request):
    history = Transaction.objects.order_by('-time')
    return render(request, "Banking/history.html", {
        "history": history,
    })

def transfer(request):
    customers = User.objects.all()
    
    if request.method == "POST":
        errors = []
        s_id = request.POST.get("sender")
        r_id = request.POST.get("recipient")
        try:
            sender = User.objects.get(id=s_id)
            recipient = User.objects.get(id=r_id)
        except:
            errors.append("Select Sender and Recipient")
            return render(request, "Banking/transfer.html", {
                "customers": customers,
                "errors": errors,
            })

        try:
            amount = int(request.POST.get("amount"))
        except:
            errors.append("Enter a valid amount")
            return render(request, "Banking/transfer.html", {
                "customers": customers,
                "errors": errors,
            })

        if s_id == r_id:
            errors.append("Sender and Recipient are same")
        elif sender.ballance < amount:
            errors.append("Insufficient balance")
        else:
            pass

        if (len(errors) == 1) and errors[0] == "Insufficient balance":
            payment = Transaction()
            payment.sender = sender
            payment.recipient = recipient
            payment.amount = amount
            payment.status = False
            payment.save()
            return render(request, "Banking/transfer.html", {
                "customers": customers,
                "errors": errors,
            })
        elif len(errors) > 0:
            return render(request, "Banking/transfer.html", {
                "customers": customers,
                "errors": errors,
            })
        else:
            sender.ballance -= amount
            recipient.ballance += amount
            payment = Transaction()
            payment.sender = sender
            payment.recipient = recipient
            payment.amount = amount
            payment.status = True
            payment.save()
            sender.save()
            recipient.save()
            return HttpResponseRedirect(reverse("customers"))
    else:
        return render(request, "Banking/transfer.html", {
            "customers": customers,
        })
