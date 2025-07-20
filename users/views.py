from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Registration successful! You can now log in.")
            return redirect('login')
        else:
            # Optional: show form errors
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
