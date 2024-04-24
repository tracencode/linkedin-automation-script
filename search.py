from autolinkedin.linkedin import LinkedIn
from dotenv import load_dotenv
import os

load_dotenv()

with LinkedIn(
        username=os.getenv('LINKEDIN_USER'),
        password=os.getenv('LINKEDIN_PASSWORD'),
        browser="Chrome",
        headless="True",
) as ln:
    # Perform LinkedIn actions here
    ln.login()
    result = ln.search_people("Recruiter")
    print("--------------------result",result)

    print("**************",ln.view_profile("https://www.linkedin.com/in/vishwash-shrivastav-b34609188"))
    # ln.withdraw_sent_invitations(older_than_days=14)
    # last_week_invitations = ln.count_invitations_sent_last_week()

    # ln.send_invitations(
    #     max_invitations=max(ln.WEEKLY_MAX_INVITATION - last_week_invitations, 0),
    #     min_mutual=10,
    #     max_mutual=450,
    #     preferred_users=["Quant", "Software"],  # file_path or list of features
    #     not_preferred_users=["Sportsman", "Doctor"],  # file_path or list of features
    #     view_profile=True,  # (recommended) view profile of users you sent connection requests to
    # )

    # ln.accept_invitations()

    # # Customize your actions as needed
    # # ...

    # # Alternatively, use the smart follow-unfollow method for a streamlined approach
    # ln.smart_follow_unfollow(
    #     min_mutual=0,
    #     max_mutual=500,
    #     withdraw_invite_older_than_days=14,
    #     max_invitations_to_send=0,
    #     users_preferred=["Quant"],  # file_path or list of features
    #     users_not_preferred=["Sportsman"],  # file_path or list of features
    #     remove_recommendations=True, # remove recommendations which do not match criteria
    # )

    # # Additional method
    # ln.remove_recommendations(min_mutual=10, max_mutual=500)

    # # Search for people
    # ln.search_people("Microsoft Recruiter")