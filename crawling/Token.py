import praw

reddit = praw.Reddit(
    client_id="1ofVDcUQkMA4yYGcL_GcwQ",
    client_secret="QZ9FAwSqccYtIJ0PAVasvOMyf-0NbQ",
    redirect_uri="http://localhost:8080",
    user_agent="Equal-Initiative-602"
)

auth_url = reddit.auth.url(scopes=["identity"], state="unique_state_string", duration="permanent")
print("🔗 인증 URL:", auth_url)
