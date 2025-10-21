import pyttsx3
import speech_recognition as sr
import random
import time


engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)


recognizer = sr.Recognizer()


def speak(text):
    print(f"AI Interviewer: {text}")
    engine.say(text)
    engine.runAndWait()


def listen(timeout=10, pause_detection=True):
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            if pause_detection:
                # For introduction - listen until user stops speaking for 3 seconds
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=None)
            else:
                # For answers - use normal timeout
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=60)
            
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            if pause_detection:
                # In pause detection mode, silence means user finished speaking
                return ""
            return ""
        except sr.RequestError:
            speak("Speech recognition service is not available right now.")
            return ""


def listen_for_introduction():
    """Listen for introduction until user stops speaking for 3 seconds"""
    print("=== LISTENING FOR INTRODUCTION (Speak until you finish) ===")
    full_intro = ""
    silence_count = 0
    max_silence = 3  # Number of consecutive silences before stopping
    start_time = time.time()
    max_total_time = 900  # 15 minutes maximum
    
    while (time.time() - start_time) < max_total_time:
        print("Listening for your introduction...")
        
        # Listen with short timeout to detect pauses
        segment = listen(timeout=5, pause_detection=True)
        
        if segment:
            full_intro += segment + " "
            silence_count = 0  # Reset silence counter when speech is detected
            print(f"Current introduction: {full_intro}")
        else:
            silence_count += 1
            print(f"Silence detected ({silence_count}/{max_silence})")
            
            # If multiple silences in a row, assume user finished
            if silence_count >= max_silence:
                print("User finished speaking")
                break
        
        # Optional: You can add a prompt after long silence to confirm
        if silence_count == 2:
            speak("Are you finished with your introduction? If yes, remain silent. If no, continue speaking.")
    
    return full_intro.strip()


# Step 1: Greeting and self-introduction
speak("Hello, I am your AI interviewer. Please introduce yourself. Tell me about your background, education, work experience, skills, projects, and career goals. Please speak naturally and take your time. When you finish your introduction, just stop speaking for a few seconds.")

# Listen for introduction with pause detection
user_intro = listen_for_introduction()

# Wait a moment before responding
time.sleep(1)

# Simple acknowledgment and move to next section
if user_intro:
    speak("Thank you for your detailed introduction. Now let's move to the technical interview section.")
else:
    speak("Let's move to the technical interview section.")


# Step 2: Choose programming language/topic
speak("Which programming language or topic would you like to be interviewed on? You can choose Python, Java, C, html and css, data structures, computer networks, or operating systems.")

language_input = listen(timeout=30, pause_detection=False)

# FIXED: Improved language mapping with priority for longer phrases
language_mapping = [
    ("computer networks", "computer networks"),
    ("computer network", "computer networks"), 
    ("networks", "computer networks"),
    ("network", "computer networks"),
    ("data structures", "datastructures"),
    ("data structure", "datastructures"),
    ("datastructures", "datastructures"),
    ("html and css", "html&css"),
    ("html css", "html&css"),
    ("html", "html&css"),
    ("css", "html&css"),
    ("operating system", "operating system"),
    ("operating systems", "operating system"),
    ("python", "Python"),
    ("java", "Java"),
    ("c programming", "C"),
    ("c", "C")
]

selected_lang = "Python"  # default language

if language_input:
    language_input_lower = language_input.lower()
    print(f"User input for language: {language_input_lower}")
    
    # Check each phrase in priority order (longer phrases first)
    for phrase, lang in language_mapping:
        if phrase in language_input_lower:
            selected_lang = lang
            print(f"Selected language: {selected_lang} (matched: {phrase})")
            break

speak(f"Great choice! I will now ask you a few {selected_lang} questions.")

# Complete question bank
question_bank = {
    "computer networks": [
        ("What is a computer network?", "network interconnected devices share resources"),
        ("What is an IP address?", "unique identifier devices network"),
        ("What is the difference between TCP and UDP?", "tcp connection oriented reliable udp connectionless faster"),
        ("What is DNS?", "domain name system translates names ip addresses"),
        ("What is HTTP?", "hypertext transfer protocol web communication"),
        ("What is a router?", "device forwards data packets networks"),
        ("What is bandwidth?", "maximum rate data transfer"),
        ("What is latency?", "time delay data communication"),
        ("What is a firewall?", "network security monitors controls traffic"),
        ("What is VPN?", "virtual private network secure connection")
    ],
    "operating system": [
        ("What is an operating system?", "software managing hardware services"),
        ("What is virtual memory?", "memory management technique uses hardware software"),
        ("What is a process?", "program execution memory space"),
        ("What is a thread?", "smallest unit processing scheduled"),
        ("What is deadlock?", "situation processes waiting resources"),
        ("What is scheduling?", "process determining which process runs"),
        ("What is paging?", "memory management scheme contiguous allocation"),
        ("What is swapping?", "moving processes memory disk"),
        ("What is a system call?", "programmatic way requests service kernel"),
        ("What is multiprocessing?", "use multiple cpus system")
    ],
    "html&css": [
        ("What is HTML?", "hypertext markup language web pages"),
        ("What is CSS?", "cascading style sheets styling"),
        ("What is the difference between div and span?", "div block level span inline"),
        ("What is the box model in CSS?", "content padding border margin"),
        ("What are semantic HTML elements?", "header footer article section"),
        ("What is CSS flexbox?", "layout model arrangement elements"),
        ("What is CSS grid?", "two dimensional layout system"),
        ("What is responsive web design?", "websites work all devices media queries"),
        ("What is the purpose of the alt attribute in images?", "alternative text screen readers"),
        ("What are CSS media queries?", "adaptation different conditions resolution")
    ],
    "datastructures": [
        ("What is an array?", "collection elements index key"),
        ("What is a linked list?", "linear collection data elements memory"),
        ("What is a stack?", "lifo data structure top"),
        ("What is a queue?", "fifo data structure rear front"),
        ("What is a binary tree?", "tree node two children"),
        ("What is a hash table?", "associative array hash functions"),
        ("What is time complexity?", "computational time algorithm"),
        ("What is space complexity?", "memory space required algorithm"),
        ("What is the difference between linear and binary search?", "linear sequential binary divide half"),
        ("What is a graph?", "non linear nodes edges")
    ],
    "Python": [
        ("What is Python?", "high level interpreted programming language"),
        ("What are Python lists?", "mutable ordered collections elements"),
        ("What is list comprehension?", "concise way create lists"),
        ("What are Python dictionaries?", "unordered key value pairs"),
        ("What is the difference between tuples and lists?", "tuples immutable lists mutable"),
        ("What are Python decorators?", "functions modify behavior functions"),
        ("What is PEP 8?", "style guide python code"),
        ("What are lambda functions?", "anonymous functions lambda"),
        ("What is the Global Interpreter Lock (GIL)?", "mutex protects access python objects"),
        ("What are Python modules?", "files containing python code")
    ],
    "Java": [
        ("What is Java?", "high level object oriented platform independent"),
        ("What is JVM?", "java virtual machine bytecode platform"),
        ("What is the difference between JDK and JRE?", "jdk development jre running"),
        ("What are the main principles of OOP?", "encapsulation inheritance polymorphism abstraction"),
        ("What is the difference between abstract classes and interfaces?", "abstract classes implemented methods interfaces cannot"),
        ("What is exception handling in Java?", "try catch blocks exceptional circumstances"),
        ("What are access modifiers in Java?", "public private protected default"),
        ("What is method overloading?", "multiple methods same name parameters"),
        ("What is method overriding?", "redefining method subclass"),
        ("What is the Collections Framework?", "unified architecture collections objects")
    ],
    "C": [
        ("What is a pointer?", "variable storing memory address"),
        ("What is the difference between malloc and calloc?", "malloc allocates calloc initializes zero"),
        ("What is a structure in C?", "user defined data type groups variables"),
        ("What is the difference between structures and unions?", "structures all members unions largest member"),
        ("What are preprocessor directives?", "commands begin with # before compilation"),
        ("What is recursion?", "function calling itself"),
        ("What are static variables?", "retain value between function calls"),
        ("What is the difference between pass by value and pass by reference?", "pass value copies pass reference address"),
        ("What are file operations in C?", "fopen fclose fread fwrite files"),
        ("What is a header file?", "file containing declarations definitions")
    ]
}

questions = question_bank.get(selected_lang, question_bank["Python"])
random.shuffle(questions)

score = 0
for i, (q, ans) in enumerate(questions[:5]):  # Ask only 5 questions
    speak(f"Question {i+1}: {q}")
    user_answer = listen(timeout=60, pause_detection=False)  # 1 minute to answer each question
    if user_answer and any(word in user_answer for word in ans.split()):
        speak("Good answer!")
        score += 1
    else:
        speak(f"The key concept is: {ans}")


final_score = int((score / 5) * 100)  # Calculate based on 5 questions
if final_score >= 80:
    feedback = "Excellent performance! Keep it up."
elif final_score >= 50:
    feedback = "Good job! You need a bit more practice."
else:
    feedback = "You need more preparation. Review the basics again."

speak(f"Your score is {final_score} out of 100. {feedback}")
speak("Thank you for attending the AI interview session. Goodbye!")