import datetime

class CalendarSkills:
    @staticmethod
    def schedule_event():
        date_str = input("Enter the event date (YYYY-MM-DD): ")
        time_str = input("Enter the event time (HH:MM AM/PM): ")
        event_title = input("Enter the event title: ")
        event_description = input("Enter the event description: ")

        try:
            event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            event_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
            event_datetime = datetime.datetime.combine(event_date, event_time)
            print("Event scheduled successfully!")

            # Save the event details to a file
            with open("events.txt", "a") as file:
                file.write(f"Title: {event_title}\n")
                file.write(f"Date: {event_date}\n")
                file.write(f"Time: {event_time}\n")
                file.write(f"Description: {event_description}\n")
                file.write("\n")

        except ValueError as e:
            print("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM AM/PM for time.")
        except Exception as e:
            print("An error occurred while writing to the file:", e)

# Example usage:
# CalendarSkills.schedule_event()
