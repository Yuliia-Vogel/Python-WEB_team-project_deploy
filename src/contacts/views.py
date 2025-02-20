from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Contact
from .forms import ContactForm


class ContactListView(ListView):
    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"


class ContactDetailView(DetailView):
    model = Contact
    template_name = "contacts/contact_detail.html"


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contact-list")


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contact-list")


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contact-list")
