from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404


# Create your views here.
def index(request):
    """The home page for Learning log."""
    return render(request, "MainApp/index.html")


@login_required()
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    # Order by is a column and you can check iin the topic def in models.py

    context = {"topics": topics}
    # This is the variable name that we will use on html page
    # first 'topics' is the key and the second topics is the value
    return render(request, "MainApp/topics.html", context)
    # Context is how you get the data


@login_required()
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by("-date_added")

    if topic.owner != request.user:
        raise Http404

    context = {"topic": topic, "entries": entries}

    return render(request, "MainApp/topic.html", context)


@login_required()
def new_topic(request):
    # Get and Post are the two things that could be on final to check what user is asking
    if request.method != "POST":
        form = TopicForm()

    else:
        form = TopicForm(data=request.POST)

        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            return redirect("MainApp:topics")

    context = {"form": form}
    return render(request, "MainApp/new_topic.html", context)


@login_required()
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # Get and Post are the two things that could be on final to check what user is asking
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            form.save()
            return redirect("MainApp:topic", topic_id=topic_id)
            # changed from topic_id to topic.id

    context = {"form": form, "topic": topic}
    return render(request, "MainApp/new_entry.html", context)


@login_required()
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("MainApp:topic", topic_id=topic.id)

    context = {"entry": entry, "form": form, "topic": topic}
    return render(request, "MainApp/edit_entry.html", context)