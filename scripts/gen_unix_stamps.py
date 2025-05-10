import yaml
import random

_START = 1670115600
_END   = 1745193600

def generate_random_unix_interval(start, end, days=15):
    # Generate a random 15 day continuous interval between start and end
    # Ensure the interval is within the specified range
    if start >= end:
        raise ValueError("Start time must be less than end time.")
    if days <= 0:
        raise ValueError("Days must be a positive integer.")
    # Generate a random start time within the range
    random_start = random.randint(start, end - (days * 24 * 60 * 60))
    random_end = random_start + (days * 24 * 60 * 60)
    return random_start, random_end

def plot_intervals(intervals):
    from datetime import datetime
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    start_dt = datetime.utcfromtimestamp(_START)
    end_dt   = datetime.utcfromtimestamp(_END)

    intervals_dt = [
        (datetime.utcfromtimestamp(s), datetime.utcfromtimestamp(e))
        for s, e in intervals
    ]

    # -- Build the plot -----------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (s_dt, e_dt) in enumerate(intervals_dt, start=1):
        color = plt.cm.tab20(i % 20)  # Use a colormap to assign a different color to each bar
        ax.hlines(y=i, xmin=s_dt, xmax=e_dt, linewidth=5, color=color, alpha=0.7)  # thicker, colored bar
        ax.plot(s_dt, i, marker="o", color=color, markersize=8, label="Start" if i == 1 else "")  # mark start with the same color as the bar
        ax.plot(e_dt, i, marker="o", color=color, markersize=8, label="End" if i == 1 else "")    # mark end with the same color as the bar

    # Vertical reference lines for the overall range
    ax.axvline(start_dt, linestyle="--", linewidth=2, color="purple", label="_START")
    ax.axvline(end_dt,   linestyle="--", linewidth=2, color="purple", label="_END")

    # Formatting niceties
    # ax.set_yticks(range(1, len(intervals_dt) + 1))
    # ax.set_yticklabels([f"interval {idx}" for idx in range(1, len(intervals_dt) + 1)])
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))   # every 3 months
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y‑%m"))
    plt.setp(ax.get_xticklabels(), fontsize=12, rotation=45, ha="right")

    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Intervals", fontsize=14)
    ax.set_title("Amelia42 Time Intervals", fontsize=16)
    # ax.legend()
    plt.tight_layout()
    plt.show()
        
    
# Example usage
if __name__ == "__main__":
    intervals = [generate_random_unix_interval(_START, _END) for _ in range(42)]
    plot_intervals(intervals)
    
    for i, interval in enumerate(intervals, 1):
        print(f"Interval {i}: Start = {interval[0]}, End = {interval[1]}")
        
        # Save intervals to a YAML file
        output_data = {
            "defaults": ["base"],
            
            "start_time": interval[0],
            "end_datetime": interval[1],
        }

        output_file = f"conf/data/amelia42/amelia42_{i}.yaml"
        with open(output_file, "w") as file:
            yaml.dump(output_data, file, default_flow_style=False)

        print(f"Intervals saved to {output_file}")