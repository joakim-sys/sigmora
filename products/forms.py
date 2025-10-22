# from django import forms


# class OrderForm(forms.Form):
#     full_name = forms.CharField(
#         label="Full Name",
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control form-control-lg",
#                 "placeholder": "Enter your full name",
#             }
#         ),
#     )
#     email = forms.EmailField(
#         label="Email Address",
#         widget=forms.EmailInput(
#             attrs={
#                 "class": "form-control form-control-lg",
#                 "placeholder": "you@example.com",
#             }
#         ),
#     )
#     preferred_platforms = forms.CharField(
#         label="Preferred Platforms",
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control form-control-lg",
#                 "placeholder": "e.g., Android, iOS, Web",
#             }
#         ),
#         help_text="Let us know which platforms you need your app on.",
#     )
#     customization_notes = forms.CharField(
#         label="Customization Notes (Optional)",
#         required=False,
#         widget=forms.Textarea(
#             attrs={
#                 "class": "form-control form-control-lg",
#                 "rows": 4,
#                 "placeholder": "Tell us about any specific features or requirements you have...",
#             }
#         ),
#     )


# products/forms.py
from django import forms

# Define the choices for our platform dropdown
PLATFORM_CHOICES = [
    ("web", "Web Application (Desktop & Mobile)"),
    # When you're ready to offer more, you can just add them here:
    # ('android', 'Android Application'),
    # ('ios', 'iOS Application'),
]


class OrderForm(forms.Form):
    # --- Personal Details ---
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your full name"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "you@example.com"}
        )
    )

    # --- Project Brief ---
    project_name = forms.CharField(
        label="What is the name of your project or app?",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g., Apex Trading Signals"}
        ),
    )
    platform_choice = forms.ChoiceField(
        label="Which platform is this application for?",
        choices=PLATFORM_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    core_functionality = forms.CharField(
        label="Briefly describe the core functionality",
        help_text="What is the single most important thing your app needs to do?",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "e.g., The app should send daily Forex signals to users via push notifications and show a history of past signals.",
            }
        ),
    )
    brand_details = forms.CharField(
        label="Branding & Style (Optional)",
        help_text="Do you have a logo, brand colors, or a style you're inspired by? Share links or descriptions here.",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )
