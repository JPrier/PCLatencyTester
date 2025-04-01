# -*- coding: utf-8 -*-

import serial
import threading
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np

# Global lists for storing measurements and timestamps
data_latency = []
timestamps = []

# Serial port configuration (adjust SERIAL_PORT as needed)
SERIAL_PORT = 'COM3'  # e.g., 'COM3' for Windows or '/dev/ttyACM0' for Linux/Mac      drc
BAUD_RATE = 115200

# CSV file for live logging
csv_filename = 'latency_log.csv'

# Global flag for resetting data
reset_flag = False

def serial_thread():
    global data_latency, timestamps, reset_flag
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Allow time for Arduino to reset
    except Exception as e:
        print("Error opening serial port:", e)
        return

    with open(csv_filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Uncomment to write a header if desired:
        # csvwriter.writerow(["Timestamp", "Latency (µs)"])
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                print(line)
                if line:
                    try:
                        # Parse the single latency value (in microseconds)
                        latency = float(line)
                        print(latency)
                    except ValueError:
                        continue

                    ts = time.time()
                    data_latency.append(latency)
                    timestamps.append(ts)
                    # Write the new measurement to CSV.
                    csvwriter.writerow([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)), latency])
                    csvfile.flush()
            except Exception as e:
                print("Error reading serial:", e)
                continue

            if reset_flag:
                data_latency.clear()
                timestamps.clear()
                reset_flag = False

def update_plot(frame):
    ax1.clear()
    ax2.clear()
    print(timestamps)
    if timestamps:
        # Convert timestamps to relative time (in seconds) from the first measurement.
        times = np.array(timestamps) - timestamps[0]
        ax1.plot(times, data_latency, '-o', markersize=2)
        ax1.set_title("Latency Over Time")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Latency (microseconds)")
        
        # Calculate statistics using NumPy
        latencies = np.array(data_latency)
        count = len(latencies)
        mean_val = np.mean(latencies)
        std_val = np.std(latencies)
        std_err = std_val / np.sqrt(count) if count > 0 else 0
        
        # Display current statistics on the plot
        stats_text = (f"Count: {count}\nMean: {mean_val:.2f} microseconds\n"
                      f"Std Dev: {std_val:.2f} microseconds\nStd Error: {std_err:.2f} microseconds")
        ax1.text(0.02, 0.95, stats_text, transform=ax1.transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    
    # Create a box plot of the latency measurements on the second axis.
    if data_latency:
        ax2.boxplot(data_latency, vert=True)
        ax2.set_title("Latency Distribution")
        ax2.set_ylabel("Latency (microseconds)")
    else:
        ax2.set_title("No Data Yet")
    
    plt.tight_layout()

def reset_button_callback(event):
    global reset_flag
    reset_flag = True

# Set up the matplotlib figure and subplots.
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(bottom=0.2)  # Reserve space at the bottom for the reset button

# Create a Reset button in the GUI.
reset_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
reset_button = Button(reset_ax, 'Reset')
reset_button.on_clicked(reset_button_callback)

# Start the serial-reading thread.
thread = threading.Thread(target=serial_thread, daemon=True)
thread.start()

# Start the animation that updates the plots every second.
ani = animation.FuncAnimation(fig, update_plot, interval=1000)

plt.show()

