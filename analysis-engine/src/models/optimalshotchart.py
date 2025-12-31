import numpy as np
from typing import Dict, Tuple, List, Union
import matplotlib.pyplot as plt

# Type alias for the optimal shot chart data structure
OptimalShotChart = Dict[Tuple[float, float], List[Union[float, int]]]

# Initialize the optimal shot chart with values extracted from the image
# src: https://mygolfdistance.com/optimal-golf-distance-chart-by-angle-of-attack/
OPTIMAL_SHOT_CHART: OptimalShotChart = {
    # Key: (Ball Speed, Angle of Attack)
    # Value: [Launch Angle, Spin Rate, Carry Distance, Color Legend Value]

    # Row: 200 mph
    (200.0, -10.0): [2.5, 3450.0, 318.0, 300], (200.0, -8.0): [3.6, 3350.0, 324.0, 300],
    (200.0, -6.0): [5.1, 3050.0, 329.0, 325], (200.0, -4.0): [6.4, 2850.0, 333.0, 325],
    (200.0, -2.0): [8.1, 2700.0, 336.0, 325], (200.0, 0.0): [9.5, 2550.0, 343.0, 325],
    (200.0, 2.0): [11.2, 2400.0, 347.0, 325], (200.0, 4.0): [12.4, 2200.0, 349.0, 325],
    (200.0, 6.0): [14.1, 2050.0, 352.0, 325], (200.0, 8.0): [15.9, 1900.0, 354.0, 325],
    (200.0, 10.0): [17.6, 1750.0, 354.0, 325],

    # Row: 190 mph
    (190.0, -10.0): [3.0, 3450.0, 301.0, 300], (190.0, -8.0): [4.2, 3250.0, 307.0, 300],
    (190.0, -6.0): [5.6, 3050.0, 312.0, 300], (190.0, -4.0): [6.9, 2850.0, 315.0, 300],
    (190.0, -2.0): [8.5, 2700.0, 319.0, 300], (190.0, 0.0): [9.9, 2550.0, 324.0, 300],
    (190.0, 2.0): [11.5, 2400.0, 328.0, 325], (190.0, 4.0): [12.8, 2200.0, 331.0, 325],
    (190.0, 6.0): [14.4, 2050.0, 333.0, 325], (190.0, 8.0): [16.1, 1900.0, 336.0, 325],
    (190.0, 10.0): [17.7, 1800.0, 337.0, 325],

    # Row: 180 mph
    (180.0, -10.0): [3.6, 3450.0, 285.0, 275], (180.0, -8.0): [4.9, 3250.0, 289.0, 300],
    (180.0, -6.0): [6.2, 3050.0, 294.0, 300], (180.0, -4.0): [7.5, 2850.0, 297.0, 300],
    (180.0, -2.0): [9.0, 2700.0, 302.0, 300], (180.0, 0.0): [10.4, 2550.0, 306.0, 300],
    (180.0, 2.0): [11.9, 2400.0, 309.0, 300], (180.0, 4.0): [13.3, 2200.0, 312.0, 300],
    (180.0, 6.0): [14.8, 2050.0, 315.0, 300], (180.0, 8.0): [16.4, 1950.0, 317.0, 300],
    (180.0, 10.0): [17.9, 1800.0, 319.0, 300],

    # Row: 170 mph
    (170.0, -10.0): [4.3, 3500.0, 268.0, 275], (170.0, -8.0): [5.7, 3300.0, 272.0, 275],
    (170.0, -6.0): [6.9, 3100.0, 276.0, 275], (170.0, -4.0): [8.2, 2900.0, 280.0, 300],
    (170.0, -2.0): [9.6, 2750.0, 284.0, 300], (170.0, 0.0): [11.0, 2600.0, 288.0, 300],
    (170.0, 2.0): [12.4, 2450.0, 291.0, 300], (170.0, 4.0): [13.9, 2300.0, 294.0, 300],
    (170.0, 6.0): [15.3, 2100.0, 296.0, 300], (170.0, 8.0): [16.8, 1950.0, 299.0, 300],
    (170.0, 10.0): [18.2, 1800.0, 301.0, 300],

    # Row: 160 mph
    (160.0, -10.0): [5.2, 3500.0, 250.0, 250], (160.0, -8.0): [6.5, 3300.0, 255.0, 250],
    (160.0, -6.0): [7.7, 3100.0, 257.0, 250], (160.0, -4.0): [9.0, 2950.0, 262.0, 275],
    (160.0, -2.0): [10.3, 2750.0, 266.0, 275], (160.0, 0.0): [11.7, 2600.0, 269.0, 275],
    (160.0, 2.0): [13.0, 2450.0, 272.0, 275], (160.0, 4.0): [14.4, 2300.0, 275.0, 275],
    (160.0, 6.0): [15.9, 2100.0, 277.0, 300], (160.0, 8.0): [17.3, 1950.0, 280.0, 300],
    (160.0, 10.0): [18.7, 1800.0, 282.0, 300],

    # Row: 150 mph
    (150.0, -10.0): [6.2, 3500.0, 232.0, 250], (150.0, -8.0): [7.4, 3350.0, 236.0, 250],
    (150.0, -6.0): [8.6, 3150.0, 240.0, 250], (150.0, -4.0): [9.8, 2950.0, 243.0, 250],
    (150.0, -2.0): [11.1, 2750.0, 246.0, 250], (150.0, 0.0): [12.4, 2600.0, 249.0, 250],
    (150.0, 2.0): [13.7, 2450.0, 252.0, 250], (150.0, 4.0): [15.1, 2300.0, 255.0, 250],
    (150.0, 6.0): [16.4, 2150.0, 257.0, 275], (150.0, 8.0): [17.9, 2000.0, 260.0, 275],
    (150.0, 10.0): [19.3, 1850.0, 262.0, 275],

    # Row: 140 mph
    (140.0, -10.0): [7.3, 3500.0, 213.0, 225], (140.0, -8.0): [8.3, 3300.0, 216.0, 225],
    (140.0, -6.0): [9.5, 3150.0, 220.0, 225], (140.0, -4.0): [10.9, 2950.0, 223.0, 225],
    (140.0, -2.0): [12.0, 2800.0, 226.0, 250], (140.0, 0.0): [13.2, 2600.0, 229.0, 250],
    (140.0, 2.0): [14.5, 2450.0, 232.0, 250], (140.0, 4.0): [15.8, 2300.0, 234.0, 250],
    (140.0, 6.0): [17.2, 2150.0, 237.0, 250], (140.0, 8.0): [18.5, 2000.0, 239.0, 250],
    (140.0, 10.0): [19.9, 1850.0, 241.0, 250],

    # Row: 130 mph
    (130.0, -10.0): [8.4, 3500.0, 193.0, 200], (130.0, -8.0): [9.4, 3300.0, 197.0, 200],
    (130.0, -6.0): [10.6, 3150.0, 200.0, 225], (130.0, -4.0): [11.7, 2950.0, 200.0, 225],
    (130.0, -2.0): [12.8, 2750.0, 205.0, 225], (130.0, 0.0): [14.1, 2600.0, 208.0, 225],
    (130.0, 2.0): [15.3, 2450.0, 211.0, 225], (130.0, 4.0): [16.6, 2300.0, 213.0, 225],
    (130.0, 6.0): [17.9, 2150.0, 216.0, 225], (130.0, 8.0): [19.2, 2000.0, 218.0, 225],
    (130.0, 10.0): [20.6, 1850.0, 220.0, 225],

    # Row: 120 mph
    (120.0, -10.0): [9.6, 3450.0, 173.0, 200], (120.0, -8.0): [10.6, 3250.0, 176.0, 200],
    (120.0, -6.0): [11.6, 3100.0, 178.0, 200], (120.0, -4.0): [12.7, 2900.0, 181.0, 200],
    (120.0, -2.0): [13.8, 2750.0, 184.0, 200], (120.0, 0.0): [15.0, 2600.0, 187.0, 200],
    (120.0, 2.0): [16.2, 2450.0, 189.0, 225], (120.0, 4.0): [17.4, 2300.0, 191.0, 225],
    (120.0, 6.0): [18.7, 2150.0, 194.0, 225], (120.0, 8.0): [19.9, 2000.0, 196.0, 225],
    (120.0, 10.0): [21.2, 1850.0, 198.0, 225],

    # Row: 110 mph
    (110.0, -10.0): [10.9, 3400.0, 153.0, 150], (110.0, -8.0): [11.8, 3200.0, 155.0, 150],
    (110.0, -6.0): [12.7, 3000.0, 157.0, 150], (110.0, -4.0): [13.9, 2850.0, 160.0, 150],
    (110.0, -2.0): [14.9, 2700.0, 162.0, 150], (110.0, 0.0): [15.9, 2550.0, 165.0, 200],
    (110.0, 2.0): [17.1, 2400.0, 167.0, 200], (110.0, 4.0): [18.2, 2250.0, 169.0, 200],
    (110.0, 6.0): [19.5, 2100.0, 172.0, 200], (110.0, 8.0): [20.7, 1950.0, 174.0, 200],
    (110.0, 10.0): [21.9, 1850.0, 175.0, 200],

    # Row: 100 mph
    (100.0, -10.0): [11.9, 3250.0, 131.0, 150], (100.0, -8.0): [12.9, 3100.0, 134.0, 150],
    (100.0, -6.0): [13.9, 2950.0, 136.0, 150], (100.0, -4.0): [14.9, 2800.0, 138.0, 150],
    (100.0, -2.0): [15.9, 2600.0, 140.0, 150], (100.0, 0.0): [16.9, 2450.0, 143.0, 150],
    (100.0, 2.0): [18.0, 2300.0, 145.0, 150], (100.0, 4.0): [19.1, 2150.0, 147.0, 150],
    (100.0, 6.0): [20.3, 2050.0, 149.0, 150], (100.0, 8.0): [21.4, 1900.0, 151.0, 200],
    (100.0, 10.0): [22.6, 1750.0, 152.0, 200],

    # Row: 90 mph
    (90.0, -10.0): [12.7, 3050.0, 111.0, 100], (90.0, -8.0): [13.9, 2950.0, 113.0, 100],
    (90.0, -6.0): [15.0, 2800.0, 115.0, 100], (90.0, -4.0): [15.9, 2650.0, 117.0, 100],
    (90.0, -2.0): [16.9, 2500.0, 118.0, 100], (90.0, 0.0): [18.0, 2350.0, 121.0, 150],
    (90.0, 2.0): [19.0, 2200.0, 123.0, 150], (90.0, 4.0): [20.0, 2100.0, 124.0, 150],
    (90.0, 6.0): [21.1, 1950.0, 127.0, 150], (90.0, 8.0): [22.2, 1800.0, 128.0, 150],
    (90.0, 10.0): [23.3, 1700.0, 129.0, 150],

    # Row: 80 mph
    (80.0, -10.0): [13.8, 2800.0, 91.0, 100], (80.0, -8.0): [14.5, 2650.0, 93.0, 100],
    (80.0, -6.0): [15.8, 2600.0, 95.0, 100], (80.0, -4.0): [16.9, 2450.0, 97.0, 100],
    (80.0, -2.0): [17.8, 2450.0, 98.0, 100], (80.0, 0.0): [18.8, 2200.0, 101.0, 100],
    (80.0, 2.0): [19.9, 2100.0, 101.0, 100], (80.0, 4.0): [20.8, 1950.0, 102.0, 100],
    (80.0, 6.0): [21.8, 1800.0, 105.0, 150], (80.0, 8.0): [22.9, 1700.0, 106.0, 150],
    (80.0, 10.0): [24.0, 1600.0, 107.0, 150],
}

class OptimalShotChartModel:
    """
    Model to hold the optimal shot chart data.
    """
    def __init__(self, chart: OptimalShotChart):
        self.chart = chart

    def get_chart(self) -> OptimalShotChart:
        return self.chart
    
    def get_ball_speeds(self) -> List[float]:
        """
        Get all unique ball speeds in the chart.
        """
        return sorted(set(k[0] for k in self.chart.keys()), reverse=True)
    
    def get_attack_angles(self) -> List[float]:
        """
        Get all unique angle of attack values in the chart.
        """
        return sorted(set(k[1] for k in self.chart.keys()))
    
    def get_row_by_ball_speed(self, ball_speed: float) -> Dict[Tuple[float, float], List[Union[float, int]]]:
        """
        Get all entries for a specific ball speed.
        """
        return {k: v for k, v in self.chart.items() if k[0] == ball_speed}
    
    def get_row_by_angle_of_attack(self, angle_of_attack: float) -> Dict[Tuple[float, float], List[Union[float, int]]]:
        """
        Get all entries for a specific angle of attack.
        """
        return {k: v for k, v in self.chart.items() if k[1] == angle_of_attack}
    
    def get_entry(self, ball_speed: float, angle_of_attack: float) -> List[Union[float, int]]:
        """
        Get the entry for a specific ball speed and angle of attack.
        """
        return self.chart.get((ball_speed, angle_of_attack), None)

    def get_optimal_score_from_entry(self, ball_speed: float, angle_of_attack: float) -> int:
        """
        Get the optimal score (color legend value) from a specific entry.
        """
        entry = self.get_entry(ball_speed, angle_of_attack)
        if entry:
            return entry[3]  # Color Legend Value
        return None


def plot_optimal_shot_chart(data: OptimalShotChartModel):
    """
    Plot the optimal shot chart.
    Points are colored green if carry_distance >= color_legend_value (good/optimal), red otherwise (bad).
    """

    color_map = {
        100: "#E06666",  # Dark Red
        150: "#F4CCCC",  # Red
        200: "#F9CB9C",  # Orange
        225: "#FFE599",  # Light Orange
        250: "#FFF2CC",  # Yellow
        275: "#D9EAD3",  # Yellow-Green
        300: "#93C47D",  # Light Green
        325: "#6AA84F"   # Dark Green
    }

    # Define the axes from the image


    ball_speeds = data.get_ball_speeds()
    attack_angles = data.get_attack_angles()

    _, ax = plt.subplots(figsize=(16, 10))
    chart = data.get_chart()

    # Create the grid
    for i, speed in enumerate(ball_speeds):
        for j, angle in enumerate(attack_angles):
            entry = data.get_entry(speed, angle)
            if entry:
                launch, spin, carry, color_val = entry
                
                # Draw the background color for the cell
                rect = plt.Rectangle((j, len(ball_speeds) - 1 - i), 1, 1, 
                                    facecolor=color_map.get(color_val, "white"), 
                                    edgecolor="grey")
                ax.add_patch(rect)
                
                # Add text labels inside each cell (Carry, Launch, Spin)
                # Note: Total distance is omitted as it wasn't in the provided list structure
                plt.text(j + 0.5, len(ball_speeds) - 1 - i + 0.7, f"{int(carry)}", 
                        ha='center', va='center', fontweight='bold', fontsize=9)
                plt.text(j + 0.5, len(ball_speeds) - 1 - i + 0.4, f"{launch}°", 
                        ha='center', va='center', fontsize=8)
                plt.text(j + 0.5, len(ball_speeds) - 1 - i + 0.15, f"{int(spin)}", 
                        ha='center', va='center', fontsize=8)

    # Configure Axis Labels and Titles
    ax.set_xticks(np.arange(len(attack_angles)) + 0.5)
    ax.set_xticklabels(attack_angles)
    ax.set_yticks(np.arange(len(ball_speeds)) + 0.5)
    ax.set_yticklabels(ball_speeds[::-1])

    plt.title("Total Distance, Carry, Launch & Spin by Attack Angle", fontsize=14, pad=20)
    plt.xlabel("Attack Angle", fontweight='bold')
    plt.ylabel("Ball Speed (mph)", fontweight='bold')

    # Add Legend simulation
    plt.text(len(attack_angles) + 0.2, len(ball_speeds) - 1, "LEGEND\nyards", fontweight='bold')
    for idx, (val, color) in enumerate(sorted(color_map.items())):
        plt.Rectangle((len(attack_angles) + 0.2, idx), 0.5, 0.5, facecolor=color)
        plt.text(len(attack_angles) + 0.8, idx + 0.25, str(val))

    plt.xlim(0, len(attack_angles))
    plt.ylim(0, len(ball_speeds))
    plt.grid(False)
    plt.show()



if __name__ == "__main__":
    chart = OptimalShotChartModel(OPTIMAL_SHOT_CHART)
    plot_optimal_shot_chart(chart)