from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q, F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Contact
from .forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        user = self.request.user

        contacts = Contact.objects.filter(user=user)  # Тільки контакти поточного користувача
        if query:
            contacts = contacts.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(address__icontains=query)
            )

        return contacts.order_by(
            F("first_name").asc(nulls_last=True),
            F("last_name").asc(nulls_last=True),
        )

class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")

    def form_valid(self, form):
        form.instance.user = self.request.user  # Прив'язка контакту до користувача
        return super().form_valid(form)

class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contacts:contact-list")

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contacts:contact-list")

