from datetime import date

def authorized_to_display_pw(sharer):
    """Validate if this sharer is avaliable to display."""

    today = date.today()
    limit_datetime = sharer.limit_datetime
    limit_visits = sharer.limit_visits
    public = sharer.public

    if (limit_visits>0) and (limit_datetime>=today) and public:
        return True
    else:
        return False

