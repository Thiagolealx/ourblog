from django.db import models
from wagtail.models import Orderable, Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from datetime import date
from modelcluster.models import ParentalKey,ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django import forms
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager

class BlogIndexPage(Page):
    description =  RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]
class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey("BlogPostPage",
                                    on_delete=models.CASCADE, related_name="tagged_items")

class BlogPostPage(Page):
    date = models.DateField("Post date", default=date.today)
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    author = ParentalManyToManyField("blog.Author",blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("author", widget=forms.CheckboxSelectMultiple),
        FieldPanel("title"),
        FieldPanel("body"),
        InlinePanel("image_gallery", label="Image Gallery"),
        FieldPanel("tags"),
    ]


class BlogPageImageGallery(Orderable):
    page = ParentalKey(BlogPostPage, on_delete=models.CASCADE, related_name="image_gallery")
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(max_length=255, blank=True)
    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("author_image"),
    ]

    def __str__(self):
        return self.name

class TagIndexPage(Page):
    pass