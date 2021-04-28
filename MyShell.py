import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_log.settings")

import django

django.setup()

from MainApp.models import Topic, Entry

topics = Topic.objects.all()
entries = Entry.objects.all()

# Alternate way to do entries
t = Topic.objects.get(id=1)
print(t)
entry = t.entry_set.all()
print(entry)

"""
for t in topics:
    print(f"Topic ID: {t.id} and Topic Name: {t}")
    print(f"Date added: {t.date_added}")

for e in entries:
    print(f"Topic: {e.topic}")
    print(f"Text: {e}")
    print(f"Date added: {e.date_added}")


# We set up the model and then bring in all topics from model to save as object
# As we iterate through topic, we get corresponding attribute
# We dont say t.text because of the string method; it returns whats in str method
"""
