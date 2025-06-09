import speech_recognition as sr
import pyttsx3
import webbrowser
from youtube_search import YoutubeSearch
from datetime import datetime
import random

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎤 Please ask your question...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print("You (EN):", text)
            return text.lower().strip(), "en"
        except sr.UnknownValueError:
            try:
                text = recognizer.recognize_google(audio, language="vi-VN")
                print("Bạn (VI):", text)
                return text.lower().strip(), "vi"
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand.")
            except sr.RequestError:
                speak("Network error. Please check your internet connection.")
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
        return "", ""

def open_youtube_first_video(query):
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if results:
            video_id = results[0]['id']
            video_url = "https://www.youtube.com/watch?v=" + video_id
            webbrowser.open(video_url)
            return True
    except Exception as e:
        print("Error opening YouTube video:", e)
    # Nếu không được thì mở trang tìm kiếm
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    return False

def tell_joke(language):
    jokes_en = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call fake spaghetti? An impasta!"
    ]
    jokes_vi = [
        "Tại sao cá không chơi piano? Vì chúng chỉ biết bơi thôi!",
        "Con gà qua đường để làm gì? Để sang bên kia mà!",
        "Tại sao máy tính không thể giữ bí mật? Vì nó có nhiều cửa sổ!"
    ]
    if language == "vi":
        return random.choice(jokes_vi)
    else:
        return random.choice(jokes_en)

def get_time(language):
    now = datetime.now()
    if language == "vi":
        return f"Bây giờ là {now.hour} giờ {now.minute} phút."
    else:
        return f"The time now is {now.hour}:{now.minute}."

answers = {
    "Who are you?": "People call me smart virtual assistant.",
    "what is the capital of vietnam": "The capital of Vietnam is Hanoi.",
    "what's my name": "Your name is Dang Van Hung.",
    "how old am i": "You are 21 years old.",
    "see you later": "I'll see you then.",
    "are you smart": "Of course! I'm powered by AI, after all.",
    "what is the weather like today": "The weather today is sunny and quite pleasant.",
    "do you know president ho chi minh": "President Ho Chi Minh was a great leader of Vietnam, born in 1890 and passed away in 1969.",
    # Tiếng Việt
    "bạn tên gì": "Mọi người gọi tôi là trợ lý ảo thông minh.",
    "thủ đô của việt nam là gì": "Thủ đô của Việt Nam là Hà Nội.",
    "tôi bao nhiêu tuổi": "Bạn 21 tuổi.",
    "tạm biệt": "Hẹn gặp lại bạn sau.",
    "bạn thông minh không": "Tất nhiên rồi! Tôi được vận hành bởi AI mà.",
    "thời tiết hôm nay": "Hôm nay thời tiết nắng đẹp và dễ chịu.",
    "bạn có biết hồ chí minh không": "Chủ tịch Hồ Chí Minh là lãnh tụ vĩ đại của Việt Nam, sinh năm 1890 và mất năm 1969.",
}

def is_quick_command(text, language):
    if any(kw in text for kw in ["what time is it", "time now", "bây giờ là mấy giờ", "mấy giờ"]):
        return get_time(language)
    if any(kw in text for kw in ["tell me a joke", "tell joke", "kể chuyện cười", "kể chuyện hài"]):
        return tell_joke(language)
    return None

def main():
    speak("Hello! I'm your virtual assistant. Ask me anything in English or Vietnamese. Say 'stop' to end.")
    while True:
        question, lang = listen()
        if not question:
            continue
        if question in ["stop", "exit", "quit", "dừng", "thoát", "ngừng"]:
            speak("Goodbye! Bye bye!")
            break

        if any(phrase in question for phrase in ["play music", "play song", "open youtube", "mở nhạc", "phát nhạc", "mở youtube"]):
            speak("What song would you like to hear?")
            song_request, _ = listen()
            if song_request:
                speak(f"Searching for {song_request} on YouTube.")
                opened = open_youtube_first_video(song_request)
                if not opened:
                    speak("Sorry, I couldn't open the video directly, so I opened the search results page.")
            else:
                speak("I didn't catch the song name.")
            continue

        matched = False
        for key in answers:
            if key in question:
                speak(answers[key])
                matched = True
                break
        if matched:
            continue

        quick_reply = is_quick_command(question, lang)
        if quick_reply:
            speak(quick_reply)
            continue

        speak("Sorry, I don't know the answer to that.")

if __name__ == "__main__":
    main()
