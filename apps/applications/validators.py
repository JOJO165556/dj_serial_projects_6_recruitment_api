from rest_framework.exceptions import ValidationError

def validate_file(file):
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("File too large (max 5MB)")

    if not file.name.endswith((".pdf", ".doc", ".docx")):
        raise ValidationError("Invalid file type")