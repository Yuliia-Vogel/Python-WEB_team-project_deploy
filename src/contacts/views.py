from django.urls import reverse_lazy
from django.db.models import Q, F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Contact
from .forms import ContactForm

class ContactListView(ListView):
    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"

    def get_queryset(self):
        # Get the search query from the request's GET parameters.
        # If no query is provided, default to an empty string.
        query = self.request.GET.get("query", "")
        if query:
            # Filter the Contact objects based on the search query.
            # The `Q` object allows for complex queries using OR conditions.
            contacts = Contact.objects.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(address__icontains=query)
            )

            # Order the filtered contacts by first_name and last_name in ascending order.
            # `nulls_last=True` ensures that null values are placed at the end of the results.
            return contacts.order_by(
                F("first_name").asc(nulls_last=True),
                F("last_name").asc(nulls_last=True),
            )
        else:
            return Contact.objects.all()


class ContactDetailView(DetailView):
    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"

class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")

class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")

class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contacts:contact-list")