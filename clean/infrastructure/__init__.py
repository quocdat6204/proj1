"""
Infrastructure Layer package.

Lưu ý: KHÔNG gọi django.setup() ở đây để tránh vòng lặp khi Django load INSTALLED_APPS.
Việc cấu hình Django đã được thực hiện qua manage.py/settings.py.
"""
