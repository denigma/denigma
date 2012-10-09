"""Handles many-to-many field changes."""""

def changed_tags(sender, instance, action, reverse, model, pk_set, **kwargs):
    print "CHANGED tags"
    print
    print sender, instance, action, reverse, model, pk_set, kwargs
    print instance,  instance.tags.all(), instance.tagged.all(), instance.images.all()
    if instance.tags.all(): pass

def adding_tags(**kwargs):
    #print ("""Adding tags signal: %s""" % kwargs)
    instance = kwargs['instance']
    tags =  kwargs['tags']
    instance.tags.add(*[tag.name for tag in instance.tags.all()])
    #print "instance.tags:", instance.tags
    if not hasattr(instance, 'change'):
        instance.change = instance.Change(title=instance.title, slug=instance.slug, text=instance.text, url=instance.url,
            of=instance, by=instance.user)
        instance.change.save()
        #instance.change.tags = tags
        instance.change.tags.add(*[tag.name for tag in tags.all()])
        instance.tags.add(*[tag.name for tag in tags.all()])

def changed_tagged(sender, instance, action, reverse, model, pk_set, **kwargs):
    #print("CHANGED TAGGED %s" % action)
    # Tagged changes:
    if action == "pre_clear":
        instance.tagged_pre_clear = instance.tagged
    elif action in ["post_add", "post_remove"] or (action == "post_clear" and instance.tagged_pre_clear):
        if not hasattr(instance, 'change'):
            instance.change = instance.Change(title=instance.title, slug=instance.slug, text=instance.text, url=instance.url,
                of=instance, by=instance.user)
            instance.change.save()
        instance.change.tagged = instance.tagged.all()
        #instance.tags.add(*[tag.name for tag in instance.change.tags.all()])

    # Tag changes:
    if action == "post_clear":
        if not hasattr(instance, 'tags_pre_clear') or instance.tags_pre_clear != [tag.name for tag in instance.tags.all()]:
            #print "Changed tags signal instance.tags_pre_clear", instance.tags_pre_clear
            #print "Changed tags signal tag.name:", [tag.name for tag in instance.tags.all()]
            if not hasattr(instance, 'change'):
                instance.change = instance.Change(title=instance.title, slug=instance.slug, text=instance.text, url=instance.url,
                    of=instance, by=instance.user)
                instance.change.save()
        instance.change.tags.clear()
        instance.change.tags.add(*[tag.name for tag in instance.tags.all()])
        #print "Tags in changed tagged: ", [tag.name for tag in instance.tags.all()]
        #print instance
        #print instance.pk
        #print instance.title
        #instance.tags_to_add = [tag.name for tag in instance.tags.all()]

def changed_images(sender, instance, action, reverse, model, pk_set, **kwargs):
    #print("changed_images: %s" % action)
    if action == "pre_clear":
        instance.images_pre_clear = instance.images
    elif action in ["post_add", "post_remove"] or (action == "post_clear" and instance.images_pre_clear):
        if not hasattr(instance, 'change'):
            instance.change = instance.Change(title=instance.title, slug=instance.slug, text=instance.text, url=instance.url,
                of=instance, by=instance.user)
            instance.change.save()
        instance.change.images = instance.images.all()
        #instance.tags = instance.change.tags.all()

def request_finished(sender, **kwargs):
    print "finished", sender, kwargs

def saving_model(sender, **kwargs):
    print "PRE SAVE:", sender, kwargs,  [tag.name for tag in kwargs['instance'].tags.all()]#[tag.name for tag in sender.tags.all()]

def model_saved(sender, **kwargs):
    print "POST SAVED: ", sender, kwargs, [tag.name for tag in kwargs['instance'].tags.all()] #[tag.name for tag in sender.tags.all()] #vars(sender),

def pre_revision(sender, **kwargs):
    print "PRE REVISION", sender, kwargs

def post_revision(sender, **kwargs):
    print "POST REVISION", sender, kwargs

def message_sent(sender, **kwargs):
    print "MESSAGE SENT", sender, kwargs
