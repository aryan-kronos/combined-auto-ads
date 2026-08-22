# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
def campaign_progress(step: int) -> str:

    circles = []

    for i in range(1, 6):

        if i <= step:
            circles.append("🟢")
        else:
            circles.append("⚪")

    return "".join(circles)