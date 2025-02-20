import os
import django
import random
from faker import Faker
from django.contrib.auth import get_user_model
from src.contacts.models import Contact
from src.notes.models import Note, Tag

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.assistant_app.settings")
django.setup()

fake = Faker()
User = get_user_model()

def create_fake_contacts(n=50):
    for _ in range(n):
        Contact.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.address(),
            phone=fake.phone_number(),
            email=fake.email(),
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=80)
        )
    print(f"{n} fake contacts created!")

def create_fake_notes(n=50):
    users = list(User.objects.all())
    if not users:
        print("No users found! Create some users first.")
        return

    for _ in range(n):
        note = Note.objects.create(
            user=random.choice(users),
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=5)
        )
        
        # Assign random tags
        tags = [Tag.objects.get_or_create(name=fake.word())[0] for _ in range(random.randint(1, 3))]
        note.tags.set(tags)
    print(f"{n} fake notes created!")

if __name__ == "__main__":
    create_fake_contacts()
    create_fake_notes()
