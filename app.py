import os
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

# Get the current working directory
current_directory = os.getcwd()

# Load CSV file and plot initial graph
def load_csv_and_plot_graph():
    file_path = os.path.join(current_directory, 'weight_data.csv')
    if os.path.exists(file_path):
        global data
        data = pd.read_csv(file_path)
        update_graph()
        update_stats()

# Initialize an empty DataFrame for data or load CSV if it exists
file_path = os.path.join(current_directory, 'weight_data.csv')
if os.path.exists(file_path):
    data = pd.read_csv(file_path)
else:
    data = pd.DataFrame(columns=['Date', 'Weight'])

def update_graph():
    plt.clf()  # Clear previous plot
    plt.plot(data['Date'], data['Weight'])
    plt.xlabel('Date')
    plt.ylabel('Weight')
    plt.title('Weight Progress Over Time')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=26)
    
    # Show every 7th label for better spacing
    every_nth = 7  # Show every 7th label
    for i, label in enumerate(plt.gca().xaxis.get_ticklabels()):
        if i % every_nth != 0:
            label.set_visible(False)
    
    canvas.draw()


# Add weight entry to CSV and update graph
def add_weight():
    weight = weight_entry.get()
    date = date_entry.get()
    
    global data
    data = data.append({'Date': date, 'Weight': weight}, ignore_index=True)
    
    update_graph()
    
    data.to_csv('weight_data.csv', index=False)

# Calculate and update statistics
def update_stats():
    if len(data) >= 1:
        first_weight = data.loc[0, 'Weight']
        last_higher_entry = data[data['Weight'] > data['Weight'].shift(-1)].tail(1)
        if not last_higher_entry.empty:
            last_higher_weight = last_higher_entry.iloc[0]['Weight']
        else:
            last_higher_weight = None
        
        one_week_ago = datetime.now() - timedelta(days=7)
        one_week_data = data[data['Date'] >= one_week_ago.strftime('%d/%m/%Y')]
        if len(one_week_data) >= 2:
            week_start_weight = one_week_data.iloc[0]['Weight']
            week_end_weight = one_week_data.iloc[-1]['Weight']
            week_change = week_end_weight - week_start_weight
        else:
            week_change = None
        
        stats_label.config(text=f"Change from first entry: {first_weight - data.iloc[-1]['Weight']:.2f}kg\n"
                                f"Change from last higher entry: {last_higher_weight - data.iloc[-1]['Weight']:.2f}kg\n"
                                f"Change over one week: {week_change:.2f}kg")
  
    # Calculate Average Weight
    if len(data) >= 1:
        average_weight = data['Weight'].mean()
        stats_label.config(text=stats_label.cget("text") + f"\nAverage Weight: {average_weight:.2f}kg")

    # Calculate Maximum and Minimum Weight
    if len(data) >= 1:
        max_weight = data['Weight'].max()
        min_weight = data['Weight'].min()
        stats_label.config(text=stats_label.cget("text") + f"\nMaximum Weight: {max_weight:.2f}kg\nMinimum Weight: {min_weight:.2f}kg")

    # ... (Your existing code)

    if len(data) >= 1:
        last_recorded_weight = data['Weight'].iloc[-1]
        weight_loss_to_80 = last_recorded_weight - 80  # Difference to reach 80kg (Placeholder value)
        if weight_loss_to_80 > 0:
            progress_message = f"You need to lose {weight_loss_to_80:.2f}kg to reach 80kg."
        else:
            progress_message = "Congratulations! You've already reached or exceeded 80kg."
        stats_label.config(text=stats_label.cget("text") + f"\nWeight Loss Progress to 80kg: {progress_message}")

    # Calculate Rate of Change
    if len(data) >= 2:
        prev_weight = data['Weight'].iloc[-2]
        current_weight = data['Weight'].iloc[-1]
        rate_of_change = (current_weight - prev_weight) / (len(data) - 1)  # Dividing by number of entries
        stats_label.config(text=stats_label.cget("text") + f"\nRate of Change: {rate_of_change:.2f}kg per entry")

    # Display Weight Entries Count
    num_entries = len(data)
    stats_label.config(text=stats_label.cget("text") + f"\nWeight Entries Count: {num_entries}")

    # Calculate Days Since Last Entry
    if len(data) >= 1:
        last_entry_date = datetime.strptime(data['Date'].iloc[-1], '%d/%m/%Y')
        days_since_last_entry = (datetime.now() - last_entry_date).days
        stats_label.config(text=stats_label.cget("text") + f"\nDays Since Last Entry: {days_since_last_entry} days")


# Main GUI window
root = tk.Tk()
root.title("Weight Tracker App")

# Load CSV Button
load_button = ttk.Button(root, text="Load CSV", command=load_csv_and_plot_graph)
load_button.pack()

# Graph
fig = plt.figure(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Weight Entry
weight_label = ttk.Label(root, text="Enter Weight:")
weight_label.pack()

weight_entry = ttk.Entry(root)
weight_entry.pack()

# Date Entry
date_label = ttk.Label(root, text="Enter Date:")
date_label.pack()

date_entry = ttk.Entry(root)
date_entry.pack()

# Add Weight Button
add_button = ttk.Button(root, text="Add Weight", command=add_weight)
add_button.pack()

# Statistics Label
stats_label = ttk.Label(root, text="", justify="left")
stats_label.pack()

# Run the GUI event loop
root.mainloop()
