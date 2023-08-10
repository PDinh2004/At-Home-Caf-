import tkinter as ttk
import customtkinter as ctk
from datetime import datetime, timedelta
from cal_setup import get_calendar_service
import time
from quote import fetchQuote
from PIL import ImageTk, Image

# Coffee color palette: https://colorhunt.co/palette/f8ede3dfd3c3d0b8a885586f


def main():
    # Load GCal API information
    service = get_calendar_service()
    settings = service.settings().list().execute()
    user_timeZone = ''
    for item in settings['items']:
        if (item['id'] == 'timezone'):
            user_timeZone = item['value']

    # Fetch random quote
    quote = fetchQuote()

    # Global variables
    status = "Start task"
    startDate = None
    start = None
    end = None

    # Create calendar event
    def makeCalendarEvent(startDate, endDate, task):
        event_result = service.events().insert(calendarId='primary',
                                               body={
                                                   "summary": task,
                                                   "description": 'Congrats completing a task!',
                                                   "start": {"dateTime": startDate, "timeZone": user_timeZone},
                                                   "end": {"dateTime": endDate, "timeZone": user_timeZone},
                                               }
                                               ).execute()

        print("created event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    def time_covert(sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins//60
        mins = mins % 60
        print("Time elasped = {0}:{1}:{2}".format(
            int(hours), int(mins), sec))

    def taskButton():
        t = o_task.get()
        nonlocal status, start, end, startDate
        d = datetime.now().date()
        currentTime = datetime.now().time()

        if (t == ''):
            return

        if (status == "Start task"):
            start = time.time()
            startDate = datetime(d.year, d.month, d.day,
                                 currentTime.hour, currentTime.minute).isoformat()
            status = "Stop task"
        else:
            end = time.time()
            endDate = (datetime(d.year, d.month, d.day,
                                currentTime.hour, currentTime.minute)).isoformat()
            makeCalendarEvent(startDate, endDate, o_task.get())
            status = "Start task"

            time_covert(end-start)

        myButton.configure(text=status)

    ctk.set_appearance_mode("light")

    # Call frames
    root = ctk.CTk()
    taskFrame = ctk.CTkFrame(root, fg_color='#F8EDE3')
    quoteFrame = ctk.CTkFrame(root, fg_color='#F8EDE3')

    # Root Config
    root.geometry("500x300")
    root.config(bg="#F8EDE3")
    root.resizable(False, False)
    root.title("At-Home Café (カフェ)")
    root.columnconfigure((0), weight=1, uniform='a')
    root.rowconfigure((0, 1), weight=1, uniform='a')

    # Logo + Title
    logo = ctk.CTkImage(light_image=Image.open(
        './images/coffee-cup.png'), size=(50, 50))
    logo_label = ctk.CTkLabel(
        master=taskFrame, image=logo, text="", fg_color='#F8EDE3')
    title = ctk.CTkLabel(master=taskFrame, font=(
        'Times New Roman', 20), text="At-Home Café")

    # Button to start/stop task
    myButton = ctk.CTkButton(master=taskFrame, text=status,
                             width=10, height=5, command=taskButton, fg_color='#85586F')

    # 'Other' task
    o_taskLabel = ctk.CTkLabel(master=taskFrame, text="Enter a task:")
    o_task = ctk.CTkEntry(master=taskFrame, width=250)

    # taskFrame pack
    title.place(relx=0.45, rely=0.12)
    logo_label.place(relx=0.32, rely=0.02)
    o_taskLabel.place(relx=0.1, rely=0.6)
    o_task.place(relx=0.27, rely=0.6)
    myButton.place(relx=0.27, rely=0.85)

    # Quote + Author
    quoteLabel = ctk.CTkLabel(
        master=quoteFrame, text='"' + quote['q'] + '"', wraplength=480)
    quoteAuthorLabel = ctk.CTkLabel(master=quoteFrame, text="- " + quote['a'])
    quoteLabel.configure(width=100)
    quoteLabel.pack(anchor='center', pady=(40, 0))
    quoteAuthorLabel.pack(anchor='center')

    # headerFrame.grid(row=0)
    taskFrame.grid(row=0, sticky='news')
    quoteFrame.grid(row=1, sticky='news')
    root.mainloop()


if __name__ == '__main__':
    main()
