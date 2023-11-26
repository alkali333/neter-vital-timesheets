from datetime import timedelta, time
import streamlit as st
from datetime import datetime
import random


# def local_now():
#     timezone = pytz.timezone(os.getenv("TIMEZONE", "UTC"))
#     utc_now = datetime.utcnow()
#     return utc_now.replace(tzinfo=pytz.utc).astimezone(timezone)


def logout():
    st.session_state.user_id = None
    st.session_state.is_admin = False
    st.session_state.user_name = None


def format_timedelta(td):
    if not td:
        return "None"
    total_minutes = td.total_seconds() // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{int(hours)}h {int(minutes)}m"


def timedelta_to_time(td):
    seconds = td.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return time(hours, minutes)


def timedelta_to_time_string(td):
    seconds = td.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    # Format the time as a string
    time_string = "{:02d}:{:02d}".format(hours, minutes)

    return time_string


# Function to convert datetime.time to timedelta
def time_to_timedelta(t):
    return timedelta(hours=t.hour, minutes=t.minute)


def print_session_state():
    st.write("\n\n\n\n\n\n")
    st.write("debugging info:")
    session_state_str = " | ".join(
        [f"{key}: {value}" for key, value in st.session_state.items()]
    )
    st.write(session_state_str)


def get_spiritual_quote():
    quotes = [
        "'Your work is to discover your work and then, with all your heart, to give yourself to it.' - Buddha",
        "'Let the beauty of what you love be what you do.' - Rumi",
        "'Work is not a punishment for being human; it is one of the deepest expressions of our humanity.' - Matthew Fox",
        "'Work in the invisible world at least as hard as you do in the visible.' - Rumi",
        "'The best way to find yourself is to lose yourself in the service of others.' - Mahatma Gandhi",
        "'Each of us has a unique part to play in the healing of the world.' - Marianne Williamson",
        "'Vocation is where our greatest passion meets the world's greatest need.' - Frederick Buechner",
        "'Do not hire a man who does your work for money, but him who does it for the love of it.' - Henry David Thoreau",
        "'When you do things from your soul, you feel a river moving in you, a joy.' - Rumi",
        "'The meaning of life is to find your gift. The purpose of life is to give it away.' - Pablo Picasso",
        "'He who works with his hands and his head and his heart is an artist.' - Francis of Assisi",
        "'To work is to pray.' - Latin Proverb",
        "'Be not afraid of growing slowly; be afraid only of standing still.' - Chinese Proverb",
        "'Work is love made visible.' - Khalil Gibran",
        "'What we do in life echoes in eternity.' - Marcus Aurelius",
        "'The only way to do great work is to love what you do.' - Steve Jobs",
        "'Find out what you like doing best and get someone to pay you for doing it.' - Katherine Whitehorn",
        "'Your purpose in life is to find your purpose and give your whole heart and soul to it.' - Buddha",
        "'You are never too old to set another goal or to dream a new dream.' - C.S. Lewis",
        "'Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.' - Christian D. Larson",
        "'This is the true joy in life, being used for a purpose recognized by yourself as a mighty one.' - George Bernard Shaw",
        "'Don’t aim at success—the more you aim at it and make it a target, the more you are going to miss it.' - Viktor E. Frankl",
        "'You are what you do, not what you say you'll do.' - Carl Gustav Jung",
        "'The person born with a talent they are meant to use will find their greatest happiness in using it.' - Johann Wolfgang von Goethe",
        "'Inspiration does exist, but it must find you working.' - Pablo Picasso",
        "'The two most important days in your life are the day you are born and the day you find out why.' - Mark Twain",
        "'Choose a job you love, and you will never have to work a day in your life.' - Confucius",
        "'I slept and dreamt that life was joy. I awoke and saw that life was service. I acted and behold, service was joy.' - Rabindranath Tagore",
        "'Hard work beats talent when talent doesn't work hard.' - Tim Notke",
        "'Whatever your life's work is, do it well. A man should do his job so well that the living, the dead, and the unborn could do it no better.' - Martin Luther King Jr.",
        "'Happiness is not in the mere possession of money; it lies in the joy of achievement, in the thrill of creative effort.' - Franklin D. Roosevelt",
        "'The only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do.' - Steve Jobs",
        "'Faith is taking the first step even when you don't see the whole staircase.' - Martin Luther King Jr.",
    ]

    return random.choice(quotes)


def get_closest_clock_icon():
    # Get the current hour
    current_hour = datetime.now().hour

    # Map each hour to the corresponding Streamlit clock icon
    hour_to_icon = {
        0: ":clock12:",
        1: ":clock1:",
        2: ":clock2:",
        3: ":clock3:",
        4: ":clock4:",
        5: ":clock5:",
        6: ":clock6:",
        7: ":clock7:",
        8: ":clock8:",
        9: ":clock9:",
        10: ":clock10:",
        11: ":clock11:",
        12: ":clock12:",
        13: ":clock1:",
        14: ":clock2:",
        15: ":clock3:",
        16: ":clock4:",
        17: ":clock5:",
        18: ":clock6:",
        19: ":clock7:",
        20: ":clock8:",
        21: ":clock9:",
        22: ":clock10:",
        23: ":clock11:",
    }

    # Return the icon that corresponds to the closest hour
    return hour_to_icon[current_hour]
