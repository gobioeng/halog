from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QVBoxLayout
from typing import Optional
from datetime import timedelta, datetime
import matplotlib.transforms as mtransforms
from matplotlib.patches import Rectangle
import matplotlib.ticker as mticker

# Set matplotlib style for professional appearance
plt.style.use('default')

class PlotUtils:
    """Enhanced plotting utilities for LINAC water system data"""
    
    @staticmethod
    def setup_professional_style():
        """Setup professional plotting style"""
        plt.rcParams.update({
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'axes.edgecolor': '#cccccc',
            'axes.linewidth': 1,
            'axes.grid': True,
            'grid.color': '#f0f0f0',
            'grid.linewidth': 0.5,
            'font.family': 'sans-serif',
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 9,
            'figure.titlesize': 14
        })


def plot_trend(widget, df: pd.DataFrame, title_suffix: str = ""):
    """Enhanced trend plotting with professional styling and multiple parameters"""
    # Clear existing plot
    layout = widget.layout()
    if layout is None:
        from PyQt5.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(widget)
        widget.setLayout(layout)
    else:
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
    
    if df.empty or "datetime" not in df.columns:
        # Show empty state
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, 'No data available for plotting', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14, color='gray')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        return
    
    # Prepare data
    df_clean = df.copy()
    df_clean["datetime"] = pd.to_datetime(df_clean["datetime"], errors="coerce")
    df_clean = df_clean[df_clean["datetime"].notna() & df_clean["avg"].notna()]
    
    if df_clean.empty:
        return
    
    # Setup professional style
    PlotUtils.setup_professional_style()
    
    # Create figure with enhanced layout
    fig = Figure(figsize=(12, 8))
    fig.suptitle(f"LINAC Water System Trends{title_suffix}", fontsize=14, fontweight='bold')
    
    # Check if we have multiple parameters
    unique_params = df_clean["param"].unique()
    
    if len(unique_params) == 1:
        # Single parameter plot
        ax = fig.add_subplot(111)
        _plot_single_parameter(ax, df_clean, unique_params[0])
    else:
        # Multiple parameters - create subplots
        n_params = len(unique_params)
        n_cols = min(2, n_params)
        n_rows = (n_params + n_cols - 1) // n_cols
        
        for i, param in enumerate(unique_params):
            ax = fig.add_subplot(n_rows, n_cols, i + 1)
            param_data = df_clean[df_clean["param"] == param]
            _plot_single_parameter(ax, param_data, param, subplot=True)
    
    # Adjust layout and add to widget
    fig.tight_layout()
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)

def find_time_clusters(df_times, gap_threshold=timedelta(days=1)):
    """
    Group data points into clusters based on time proximity
    
    Parameters:
    -----------
    df_times : pandas Series
        Datetime values
    gap_threshold : timedelta
        Maximum gap between points in the same cluster
        
    Returns:
    --------
    clusters : list of lists
        Each inner list contains indices for each cluster
    """
    # Convert to Python datetime objects for safety
    try:
        times = df_times.dt.to_pydatetime()
    except:
        times = [pd.to_datetime(t).to_pydatetime() for t in df_times]
    
    if len(times) <= 1:
        return [list(range(len(times)))]
    
    # Sort times and get indices
    indices = sorted(range(len(times)), key=lambda i: times[i])
    sorted_times = [times[i] for i in indices]
    
    # Initialize clusters
    clusters = []
    current_cluster = [indices[0]]
    
    # Group times into clusters based on gaps
    for i in range(1, len(sorted_times)):
        # Calculate time difference
        time_diff = sorted_times[i] - sorted_times[i-1]
        
        if time_diff > gap_threshold:
            # Gap detected, start new cluster
            clusters.append(current_cluster)
            current_cluster = [indices[i]]
        else:
            # Add to current cluster
            current_cluster.append(indices[i])
    
    # Add the last cluster
    if current_cluster:
        clusters.append(current_cluster)
    
    return clusters

def _plot_single_parameter(ax, df: pd.DataFrame, param_name: str, subplot: bool = False):
    """Plot data for a single parameter with compressed time gaps"""
    try:
        # Get parameter-specific styling
        param_colors = {
            'pumpPressure': '#e74c3c',
            'magnetronFlow': '#3498db',
            'targetAndCirculatorFlow': '#2ecc71',
            'cityWaterFlow': '#f39c12'
        }
        color = param_colors.get(param_name, '#34495e')
        
        # Sort by datetime
        df_sorted = df.sort_values("datetime")
        
        # If statistic_type exists, split out avg, min, max
        if "statistic_type" in df_sorted.columns:
            avg_df = df_sorted[df_sorted["statistic_type"] == "avg"]
            min_df = df_sorted[df_sorted["statistic_type"] == "min"]
            max_df = df_sorted[df_sorted["statistic_type"] == "max"]
        else:
            avg_df = df_sorted
            min_df = pd.DataFrame()
            max_df = pd.DataFrame()
        
        # If we have enough data points, create a broken axis plot
        if len(avg_df) > 1:
            # Find clusters of points that are close in time
            clusters = find_time_clusters(avg_df["datetime"], timedelta(days=1))
            
            # If we have multiple clusters, create a broken-axis style plot
            if len(clusters) > 1:
                # Clear the original axis for custom implementation
                ax.clear()
                
                # Extract time ranges for each cluster
                domains = []
                for cluster_indices in clusters:
                    cluster_times = [avg_df["datetime"].iloc[i] for i in cluster_indices]
                    min_time = min(cluster_times)
                    max_time = max(cluster_times)
                    domains.append((min_time, max_time))
                
                # Calculate total time span across all domains (within clusters only)
                total_span = sum((max_t - min_t).total_seconds() for min_t, max_t in domains)
                
                # Calculate the normalized domain bounds for each cluster
                # Each cluster gets space proportional to its time span plus padding
                norm_domains = []
                curr_pos = 0.05  # Start with some padding
                for i, (min_t, max_t) in enumerate(domains):
                    # Give each domain space proportional to its time span
                    span_ratio = (max_t - min_t).total_seconds() / total_span if total_span > 0 else 0
                    
                    # Minimum width for any domain is 15% of the axis
                    domain_width = max(0.15, span_ratio * 0.7)  # 70% of space for data, adjust as needed
                    
                    norm_domains.append((curr_pos, curr_pos + domain_width))
                    curr_pos += domain_width + 0.05  # Add some padding between domains
                
                # Create plot for each cluster
                for i, cluster_indices in enumerate(clusters):
                    # Get the normalized domain range
                    left, right = norm_domains[i]
                    
                    # Extract data for this cluster
                    cluster_times = [avg_df["datetime"].iloc[j] for j in cluster_indices]
                    cluster_values = [avg_df["avg"].iloc[j] for j in cluster_indices]
                    
                    # Skip empty clusters
                    if len(cluster_times) == 0:
                        continue
                    
                    # Get time range for this cluster
                    min_time = min(cluster_times)
                    max_time = max(cluster_times)
                    
                    # Linear transformation from datetime to normalized position
                    def transform_time(t):
                        if min_time == max_time:  # Handle single-point clusters
                            return (left + right) / 2
                        ratio = (t - min_time).total_seconds() / (max_time - min_time).total_seconds()
                        return left + ratio * (right - left)
                    
                    # Transform all times to normalized positions
                    norm_times = [transform_time(t) for t in cluster_times]
                    
                    # Plot data points in this cluster
                    ax.plot(norm_times, cluster_values, color=color, linewidth=2, alpha=0.8)
                    ax.scatter(norm_times, cluster_values, color=color, s=30, alpha=0.6, zorder=5)
                    
                    # Find min/max values for this time range if available
                    if not min_df.empty:
                        min_cluster_data = min_df[
                            (min_df["datetime"] >= min_time) & 
                            (min_df["datetime"] <= max_time)
                        ]
                        if not min_cluster_data.empty:
                            norm_min_times = [transform_time(t) for t in min_cluster_data["datetime"]]
                            ax.plot(norm_min_times, min_cluster_data["avg"].tolist(), 
                                  color=color, linestyle='dotted', linewidth=1, alpha=0.4)
                    
                    if not max_df.empty:
                        max_cluster_data = max_df[
                            (max_df["datetime"] >= min_time) & 
                            (max_df["datetime"] <= max_time)
                        ]
                        if not max_cluster_data.empty:
                            norm_max_times = [transform_time(t) for t in max_cluster_data["datetime"]]
                            ax.plot(norm_max_times, max_cluster_data["avg"].tolist(), 
                                  color=color, linestyle='dotted', linewidth=1, alpha=0.4)
                    
                    # Fill between min and max if both exist
                    if not min_df.empty and not max_df.empty:
                        merged = pd.merge(
                            min_df[(min_df["datetime"] >= min_time) & (min_df["datetime"] <= max_time)][["datetime", "avg"]],
                            max_df[(max_df["datetime"] >= min_time) & (max_df["datetime"] <= max_time)][["datetime", "avg"]],
                            on="datetime", 
                            suffixes=("_min", "_max")
                        )
                        if not merged.empty:
                            norm_merged_times = [transform_time(t) for t in merged["datetime"]]
                            ax.fill_between(
                                norm_merged_times, 
                                merged["avg_min"].tolist(), 
                                merged["avg_max"].tolist(),
                                color=color, 
                                alpha=0.15
                            )
                
                # Add break marks between clusters
                for i in range(len(norm_domains) - 1):
                    # Get the positions of adjacent domains
                    _, right = norm_domains[i]
                    left_next, _ = norm_domains[i+1]
                    
                    # Calculate middle point for the break mark
                    mid = (right + left_next) / 2
                    
                    # Add a break mark (gray band)
                    ax.axvspan(right, left_next, color='lightgray', alpha=0.3, zorder=-1)
                    
                    # Calculate days between clusters
                    end_time = domains[i][1]
                    start_next_time = domains[i+1][0]
                    days_diff = (start_next_time - end_time).total_seconds() / 86400
                    
                    # Add text annotation for the time gap
                    ax.annotate(f"{days_diff:.1f} days", 
                              xy=(mid, 0.02), 
                              xycoords='axes fraction', 
                              ha='center', va='bottom',
                              bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))
                
                # Set custom tick positions and labels
                tick_positions = []
                tick_labels = []
                
                # Add ticks for the start and end of each domain
                for i, ((min_t, max_t), (left, right)) in enumerate(zip(domains, norm_domains)):
                    # Add start date
                    tick_positions.append(left)
                    tick_labels.append(min_t.strftime('%m/%d'))
                    
                    # Add end date if different from start date
                    if min_t.date() != max_t.date():
                        tick_positions.append(right)
                        tick_labels.append(max_t.strftime('%m/%d'))
                
                ax.set_xticks(tick_positions)
                ax.set_xticklabels(tick_labels)
                
                # Set axis limits
                ax.set_xlim(0, 1)
                
                # Make sure we don't lose our Y-axis formatting
                ax.grid(True, linestyle='--', alpha=0.3)
                
                # Add title under the plot
                ax.text(0.5, -0.1, "Time (days with compressed gaps)", 
                       ha='center', va='center', transform=ax.transAxes, fontsize=10)
                
            else:
                # Just one cluster - plot normally
                ax.plot(avg_df["datetime"], avg_df["avg"], color=color, linewidth=2, alpha=0.8, label=param_name)
                ax.scatter(avg_df["datetime"], avg_df["avg"], color=color, s=30, alpha=0.6, zorder=5)
                
                # Plot min/max
                if not min_df.empty:
                    ax.plot(min_df["datetime"], min_df["avg"], 
                          color=color, linestyle='dotted', linewidth=1, alpha=0.4, label='Min')
                
                if not max_df.empty:
                    ax.plot(max_df["datetime"], max_df["avg"], 
                          color=color, linestyle='dotted', linewidth=1, alpha=0.4, label='Max')
                
                # Fill between
                if not min_df.empty and not max_df.empty:
                    merged = pd.merge(
                        min_df[["datetime", "avg"]],
                        max_df[["datetime", "avg"]],
                        on="datetime", 
                        suffixes=("_min", "_max")
                    )
                    if not merged.empty:
                        ax.fill_between(
                            merged["datetime"], 
                            merged["avg_min"], 
                            merged["avg_max"], 
                            color=color, 
                            alpha=0.15
                        )
                
                # Add trend line
                if len(avg_df) > 3:
                    try:
                        x_numeric = mdates.date2num(avg_df["datetime"])
                        coeffs = np.polyfit(x_numeric, avg_df["avg"], 1)
                        trend_line = np.polyval(coeffs, x_numeric)
                        ax.plot(avg_df["datetime"], trend_line, '--', color=color, alpha=0.7, linewidth=1.5,
                               label=f'Trend (slope: {coeffs[0]:.4f})')
                    except Exception as e:
                        print(f"Error adding trend line: {e}")
                
                # Format dates appropriately
                date_range = avg_df["datetime"].max() - avg_df["datetime"].min()
                if date_range.total_seconds() < 24*3600:  # Less than a day
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
                elif date_range.total_seconds() < 7*24*3600:  # Less than a week
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
                    ax.xaxis.set_major_locator(mdates.DayLocator())
                else:
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        else:
            # Not enough data - just plot what we have
            ax.plot(avg_df["datetime"], avg_df["avg"], color=color, linewidth=2, alpha=0.8, label=param_name)
            ax.scatter(avg_df["datetime"], avg_df["avg"], color=color, s=30, alpha=0.6, zorder=5)
        
        # Formatting
        if not subplot:
            if len(clusters) > 1:
                ax.set_xlabel("Date (compressed time scale)", fontweight='bold')
            else:
                ax.set_xlabel("Date/Time", fontweight='bold')
            ax.set_title(f"Trend Analysis: {param_name}", fontweight='bold', pad=20)
        else:
            ax.set_title(param_name, fontweight='bold')
        
        # Get unit for y-axis label
        unit = df['unit'].iloc[0] if 'unit' in df.columns and not df.empty else ''
        ax.set_ylabel(f"Value ({unit})" if unit else "Value", fontweight='bold')
        
        # Add y-axis margin for better appearance (100% from min and max)
        # Use min/max of ALL relevant values (avg, min, max) for scaling
        y_candidates = []
        if len(avg_df) > 0:
            y_candidates.append(avg_df["avg"].dropna())
        if len(min_df) > 0:
            y_candidates.append(min_df["avg"].dropna())
        if len(max_df) > 0:
            y_candidates.append(max_df["avg"].dropna())
        if y_candidates:
            y_values = pd.concat(y_candidates)
            y_min = y_values.min()
            y_max = y_values.max()
            y_range = y_max - y_min if y_max != y_min else 1
            margin = y_range * 1.0  # 100% margin above max and below min
            ax.set_ylim(y_min - margin, y_max + margin)
        
        # Add grid and styling
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.set_facecolor('#fafafa')
        
        # Add statistical annotations if not a subplot
        if not subplot and len(avg_df) > 1:
            _add_statistical_annotations(ax, avg_df["avg"])
            
    except Exception as e:
        print(f"Error plotting parameter {param_name}: {e}")
        # Create a simple error message in the plot
        ax.clear()
        ax.text(0.5, 0.5, f'Error plotting data: {str(e)}', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=10, color='red')
        ax.set_xticks([])
        ax.set_yticks([])

def _add_statistical_annotations(ax, y_data):
    """Add statistical annotations to the plot"""
    try:
        mean_val = y_data.mean()
        std_val = y_data.std()
        # Add horizontal lines for mean and standard deviation bands
        ax.axhline(y=mean_val, color='red', linestyle='-', alpha=0.5, linewidth=1, label=f'Mean: {mean_val:.2f}')
        ax.axhline(y=mean_val + std_val, color='orange', linestyle='--', alpha=0.5, linewidth=1, label=f'±1σ')
        ax.axhline(y=mean_val - std_val, color='orange', linestyle='--', alpha=0.5, linewidth=1)
        # Add legend
        ax.legend(loc='upper right', framealpha=0.9)
    except Exception as e:
        print(f"Error adding statistical annotations: {e}")

def plot_anomaly(widget, anomaly_df: pd.DataFrame, serial: str = None, param: str = None):
    """Plot anomaly overlays on existing trend plots"""
    if anomaly_df.empty:
        return
    # Filter anomalies based on selection
    filtered_anomalies = anomaly_df.copy()
    if serial and serial != "All":
        # Note: anomaly_df might not have serial column, need to adjust based on actual structure
        pass
    if param and param != "All":
        filtered_anomalies = filtered_anomalies[filtered_anomalies['parameter_type'] == param]
    # This function would overlay anomaly points on the existing plot
    # Implementation depends on how the widget's canvas can be accessed
    print(f"Would overlay {len(filtered_anomalies)} anomalies on trend plot")

def plot_stats(widget, stats_df: pd.DataFrame, serial: str = None, param: str = None):
    """Plot statistical overlays on existing trend plots"""
    if stats_df.empty:
        return
    # Filter statistics based on selection
    filtered_stats = stats_df.copy()
    if param and param != "All":
        filtered_stats = filtered_stats[filtered_stats['parameter'] == param]
    # This function would overlay statistical information on the existing plot
    # Implementation depends on how the widget's canvas can be accessed
    print(f"Would overlay statistics for {len(filtered_stats)} parameters on trend plot")

def create_summary_plot(df: pd.DataFrame) -> Figure:
    """Create a comprehensive summary plot for dashboard"""
    PlotUtils.setup_professional_style()
    fig = Figure(figsize=(12, 8))
    fig.suptitle("LINAC Water System Overview", fontsize=16, fontweight='bold')
    if df.empty:
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, 'No data available', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14, color='gray')
        return fig
    # Get unique parameters
    unique_params = df["param"].unique()
    n_params = len(unique_params)
    if n_params == 0:
        return fig
    # Create subplots for each parameter
    n_cols = min(2, n_params)
    n_rows = (n_params + n_cols - 1) // n_cols
    for i, param in enumerate(unique_params):
        ax = fig.add_subplot(n_rows, n_cols, i + 1)
        param_data = df[df["param"] == param]
        if not param_data.empty:
            # Simple histogram of values
            values = param_data["avg"].dropna()
            if len(values) > 0:
                ax.hist(values, bins=20, alpha=0.7, color=f'C{i}')
                ax.set_title(param, fontweight='bold')
                ax.set_xlabel('Value')
                ax.set_ylabel('Frequency')
                ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig