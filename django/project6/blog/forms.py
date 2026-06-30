from django import forms
from django.contrib.auth.forms import AuthenticationForm


class TailwindModelFormMixin:
    """Mixin untuk menambahkan kelas Tailwind ke widget form secara dinamis."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_input = "block w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-900 transition-all duration-300 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100"
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = " ".join(
                filter(None, [existing_classes, text_input])
            )
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = field.label


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_input = "block w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-900 transition-all duration-300 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100"
        for field in self.fields.values():
            field.widget.attrs.update({"class": text_input})


from .models import Category, Post


class PostForm(TailwindModelFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "category", "body", "featured_image", "is_published"]
        labels = {
            "title": "Judul Post",
            "category": "Kategori",
            "body": "Konten Post",
            "featured_image": "URL Gambar Thumbnail",
            "is_published": "Terbitkan Sekarang",
        }


class CategoryForm(TailwindModelFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        labels = {
            "name": "Nama Kategori",
        }


class DashboardSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Cari post",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cari judul, kategori, atau kata kunci...",
                "class": "block w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-900 transition-all duration-300 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100",
            }
        ),
    )
