from .models import CandidateProfile

def create_candidate_profile(user, **validated_data):
    """
    Crée un profil candidat.
    """

    if user.role != "CANDIDATE":
        raise Exception("Only candidates can have a profile")

    if hasattr(user, "candidate_profile"):
        raise Exception("Profile already exists")

    return CandidateProfile.objects.create(
        user=user,
        **validated_data
    )