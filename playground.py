from datetime import datetime

# Get the current local date and time
current_datetime = datetime.now()

# Extract just the time component
current_time = current_datetime.time()

print(f"Current local date and time: {current_datetime}")
print(f"Current local time: {current_time}")
