django-filebased-email-backend-ng
=================================

Like ``django.core.mail.backends.filebased`` but writes out attachments, HTML
alternatives, etc.

Useful for debugging/testing HTML emails, locally etc.

Installation
------------

 * Install to your PYTHONPATH

 * Set `settings.EMAIL_BACKEND` to
   `django_filebased_email_backend_ng.backend.EmailBackend`.

 * Check `settings.EMAIL_FILE_PATH`.
