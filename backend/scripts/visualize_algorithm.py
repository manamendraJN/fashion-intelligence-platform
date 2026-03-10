"""
Algorithm Visualization Script for Research Panel Presentation
Generates professional charts and graphs explaining the size matching algorithm
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Set style for professional appearance
plt.style.use('seaborn-v0_8-darkgrid')

def plot_scoring_zones():
    """
    Visualize the three scoring zones (Perfect, Acceptable, Poor)
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Size parameters
    min_val = 94
    max_val = 100
    optimal = 97
    tolerance = 3
    
    # Define zones
    too_small_beyond = min_val - tolerance - 3
    too_small_tolerance = min_val - tolerance
    too_large_tolerance = max_val + tolerance
    too_large_beyond = max_val + tolerance + 3
    
    # X-axis values
    x = np.linspace(too_small_beyond, too_large_beyond, 500)
    scores = []
    
    for val in x:
        if min_val <= val <= max_val:
            # Within range
            if optimal:
                range_width = max_val - min_val
                distance_from_optimal = abs(val - optimal)
                score = 100 - (distance_from_optimal / range_width) * 10
                score = max(90, min(100, score))
            else:
                score = 95
        elif too_small_tolerance <= val < min_val or max_val < val <= too_large_tolerance:
            # Within tolerance
            if val < min_val:
                deviation = min_val - val
            else:
                deviation = val - max_val
            score = 90 - (deviation / tolerance) * 20
            score = max(70, score)
        else:
            # Beyond tolerance
            if val < too_small_tolerance:
                deviation = min_val - val
            else:
                deviation = val - max_val
            excess_deviation = deviation - tolerance
            penalty = min(70, excess_deviation * 10)
            score = max(0, 70 - penalty)
        
        scores.append(score)
    
    # Plot the curve
    ax.plot(x, scores, linewidth=3, color='#2E86AB', label='Score Curve')
    
    # Color zones
    ax.axvspan(min_val, max_val, alpha=0.2, color='green', label='Perfect Zone (90-100)')
    ax.axvspan(too_small_tolerance, min_val, alpha=0.2, color='yellow')
    ax.axvspan(max_val, too_large_tolerance, alpha=0.2, color='yellow', label='Acceptable Zone (70-89)')
    ax.axvspan(too_small_beyond, too_small_tolerance, alpha=0.2, color='red')
    ax.axvspan(too_large_tolerance, too_large_beyond, alpha=0.2, color='red', label='Poor Zone (0-69)')
    
    # Mark key points
    ax.axvline(min_val, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax.axvline(max_val, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax.axvline(optimal, color='darkgreen', linestyle='-', linewidth=2, alpha=0.9)
    
    ax.scatter([optimal], [100], color='darkgreen', s=200, zorder=5, marker='*', 
               label=f'Optimal ({optimal}cm)')
    
    # Labels and formatting
    ax.set_xlabel('User Chest Measurement (cm)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Match Score', fontsize=14, fontweight='bold')
    ax.set_title('Size Matching Scoring System - Chest Measurement for Size M', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11, loc='upper right')
    ax.set_ylim(-5, 105)
    
    # Add annotations
    ax.annotate(f'Range: {min_val}-{max_val}cm', xy=(optimal, 100), 
                xytext=(optimal, 110), ha='center', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.annotate('Tolerance Zone', xy=(92, 75), fontsize=11, 
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    ax.annotate('Tolerance Zone', xy=(102, 75), fontsize=11,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('scoring_zones.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: scoring_zones.png")
    plt.show()


def plot_weighted_aggregation():
    """
    Visualize how multiple measurements are weighted and combined
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Data
    measurements = ['Chest', 'Waist', 'Shoulder', 'Sleeve']
    scores = [98, 100, 96, 95]
    weights = [1.5, 0.8, 1.2, 0.5]
    weighted_scores = [s * w for s, w in zip(scores, weights)]
    
    # Plot 1: Individual Scores
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    bars1 = ax1.barh(measurements, scores, color=colors, alpha=0.7)
    ax1.set_xlabel('Individual Score', fontsize=12, fontweight='bold')
    ax1.set_title('Individual Measurement Scores', fontsize=14, fontweight='bold')
    ax1.set_xlim(0, 110)
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, score) in enumerate(zip(bars1, scores)):
        ax1.text(score + 1, bar.get_y() + bar.get_height()/2, 
                f'{score}', va='center', fontsize=11, fontweight='bold')
    
    # Plot 2: Weighted Contributions
    bars2 = ax2.barh(measurements, weighted_scores, color=colors, alpha=0.7)
    ax2.set_xlabel('Weighted Contribution', fontsize=12, fontweight='bold')
    ax2.set_title('Weighted Contributions (Score × Weight)', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Add value labels with weights
    for i, (bar, ws, w, s) in enumerate(zip(bars2, weighted_scores, weights, scores)):
        ax2.text(ws + 1, bar.get_y() + bar.get_height()/2, 
                f'{ws:.1f}\n(×{w})', va='center', fontsize=10, fontweight='bold')
    
    # Add final score annotation
    total = sum(weighted_scores)
    total_weight = sum(weights)
    final_score = total / total_weight
    
    fig.suptitle(f'Final Score = {total:.1f} / {total_weight:.1f} = {final_score:.1f}', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig('weighted_aggregation.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: weighted_aggregation.png")
    plt.show()


def plot_confidence_scenarios():
    """
    Visualize different confidence scenarios
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Scenarios
    scenarios = [
        {'name': 'High Confidence\n(Clear Winner)', 'best': 95, 'second': 78, 'color': '#27AE60'},
        {'name': 'Medium Confidence\n(Moderate Gap)', 'best': 88, 'second': 82, 'color': '#F39C12'},
        {'name': 'Low Confidence\n(Close Scores)', 'best': 85, 'second': 83, 'color': '#E74C3C'},
        {'name': 'Very Low\n(Poor Match)', 'best': 65, 'second': 62, 'color': '#95A5A6'},
    ]
    
    x_pos = np.arange(len(scenarios))
    width = 0.35
    
    best_scores = [s['best'] for s in scenarios]
    second_scores = [s['second'] for s in scenarios]
    gaps = [s['best'] - s['second'] for s in scenarios]
    
    # Calculate confidence
    confidences = []
    for s in scenarios:
        base = s['best']
        gap = s['best'] - s['second']
        if gap > 10:
            conf = min(100, base + gap * 0.5)
        elif gap < 5:
            conf = base * 0.9
        else:
            conf = base
        confidences.append(conf)
    
    # Plot bars
    bars1 = ax.bar(x_pos - width/2, best_scores, width, label='Best Size Score', 
                   color=[s['color'] for s in scenarios], alpha=0.8)
    bars2 = ax.bar(x_pos + width/2, second_scores, width, label='Second Best Score', 
                   color=[s['color'] for s in scenarios], alpha=0.4)
    
    # Add confidence scores on top
    for i, (conf, gap) in enumerate(zip(confidences, gaps)):
        ax.text(i, max(best_scores[i], second_scores[i]) + 5, 
                f'Confidence:\n{conf:.1f}%\nGap: {gap}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_xlabel('Scenarios', fontsize=14, fontweight='bold')
    ax.set_ylabel('Match Score', fontsize=14, fontweight='bold')
    ax.set_title('Confidence Calculation: Impact of Score Gap', fontsize=16, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([s['name'] for s in scenarios])
    ax.legend(fontsize=12)
    ax.set_ylim(0, 120)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('confidence_scenarios.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: confidence_scenarios.png")
    plt.show()


def plot_size_comparison():
    """
    Visualize how different sizes score for the same user
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
    scores = [45, 72, 97, 78, 58, 42]
    colors = ['#E74C3C', '#E67E22', '#27AE60', '#3498DB', '#9B59B6', '#95A5A6']
    
    # Highlight best match
    colors_final = []
    for i, score in enumerate(scores):
        if score == max(scores):
            colors_final.append('#27AE60')  # Green for best
        elif score >= 70:
            colors_final.append('#F39C12')  # Orange for acceptable
        else:
            colors_final.append('#E74C3C')  # Red for poor
    
    bars = ax.bar(sizes, scores, color=colors_final, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add horizontal lines for score ranges
    ax.axhline(y=90, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Excellent (90+)')
    ax.axhline(y=70, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Acceptable (70+)')
    
    # Add score labels on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{score}',
                ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    # Highlight best match
    best_idx = scores.index(max(scores))
    ax.text(best_idx, scores[best_idx] + 8, '★ RECOMMENDED ★',
            ha='center', va='bottom', fontsize=12, fontweight='bold',
            color='darkgreen',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    ax.set_xlabel('Size', fontsize=14, fontweight='bold')
    ax.set_ylabel('Match Score', fontsize=14, fontweight='bold')
    ax.set_title('Size Comparison for User\n(Chest: 98cm, Waist: 84cm, Shoulder: 46cm)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 110)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('size_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: size_comparison.png")
    plt.show()


def plot_tolerance_sensitivity():
    """
    Show how tolerance affects scoring
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # User measurement
    user_val = 102
    min_val = 94
    max_val = 100
    
    # Different tolerance levels
    tolerances = [1, 2, 3, 4, 5]
    colors_tol = ['#E74C3C', '#E67E22', '#F39C12', '#2ECC71', '#27AE60']
    
    x = np.linspace(88, 108, 300)
    
    for tol, color in zip(tolerances, colors_tol):
        scores = []
        for val in x:
            if min_val <= val <= max_val:
                score = 95
            elif val < min_val:
                deviation = min_val - val
                if deviation <= tol:
                    score = 90 - (deviation / tol) * 20
                    score = max(70, score)
                else:
                    excess = deviation - tol
                    penalty = min(70, excess * 10)
                    score = max(0, 70 - penalty)
            else:
                deviation = val - max_val
                if deviation <= tol:
                    score = 90 - (deviation / tol) * 20
                    score = max(70, score)
                else:
                    excess = deviation - tol
                    penalty = min(70, excess * 10)
                    score = max(0, 70 - penalty)
            scores.append(score)
        
        ax.plot(x, scores, linewidth=2.5, label=f'Tolerance = {tol}cm', color=color)
    
    # Mark user measurement
    ax.axvline(user_val, color='black', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(user_val, 105, f'User: {user_val}cm', ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Mark range
    ax.axvspan(min_val, max_val, alpha=0.1, color='green', label='Size Range')
    
    ax.set_xlabel('Measurement (cm)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Match Score', fontsize=14, fontweight='bold')
    ax.set_title('Tolerance Sensitivity Analysis\n(How tolerance affects scoring for user at 102cm)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='lower left')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-5, 110)
    
    plt.tight_layout()
    plt.savefig('tolerance_sensitivity.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: tolerance_sensitivity.png")
    plt.show()


def plot_workflow_diagram():
    """
    Create a visual workflow diagram
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('off')
    
    # Define boxes
    steps = [
        {'y': 0.9, 'text': 'INPUT\nUser Measurements + Brand/Category', 'color': '#3498DB'},
        {'y': 0.75, 'text': 'DATABASE QUERY\nRetrieve Size Charts', 'color': '#9B59B6'},
        {'y': 0.6, 'text': 'SCORE EACH SIZE\nMulti-Measurement Matching', 'color': '#E67E22'},
        {'y': 0.45, 'text': 'RANK SIZES\nSort by Score', 'color': '#F39C12'},
        {'y': 0.3, 'text': 'CALCULATE CONFIDENCE\nAnalyze Score Gap', 'color': '#16A085'},
        {'y': 0.15, 'text': 'GENERATE ADVICE\nFit Recommendations', 'color': '#27AE60'},
        {'y': 0.0, 'text': 'OUTPUT\nSize + Confidence + Alternatives', 'color': '#2ECC71'},
    ]
    
    for i, step in enumerate(steps):
        # Draw box
        rect = Rectangle((0.25, step['y']-0.05), 0.5, 0.08, 
                         facecolor=step['color'], edgecolor='black', linewidth=2, alpha=0.7)
        ax.add_patch(rect)
        
        # Add text
        ax.text(0.5, step['y'], step['text'], ha='center', va='center', 
                fontsize=12, fontweight='bold', color='white')
        
        # Draw arrow to next step
        if i < len(steps) - 1:
            ax.arrow(0.5, step['y']-0.06, 0, -0.04, head_width=0.03, head_length=0.02, 
                    fc='black', ec='black', linewidth=2)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 1.0)
    ax.set_title('Size Matching Algorithm Workflow', fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('workflow_diagram.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: workflow_diagram.png")
    plt.show()


def generate_all_diagrams():
    """
    Generate all visualization diagrams
    """
    print("\n" + "="*60)
    print("GENERATING ALGORITHM VISUALIZATION DIAGRAMS")
    print("="*60 + "\n")
    
    print("📊 Diagram 1: Scoring Zones")
    plot_scoring_zones()
    
    print("\n📊 Diagram 2: Weighted Aggregation")
    plot_weighted_aggregation()
    
    print("\n📊 Diagram 3: Confidence Scenarios")
    plot_confidence_scenarios()
    
    print("\n📊 Diagram 4: Size Comparison")
    plot_size_comparison()
    
    print("\n📊 Diagram 5: Tolerance Sensitivity")
    plot_tolerance_sensitivity()
    
    print("\n📊 Diagram 6: Workflow Diagram")
    plot_workflow_diagram()
    
    print("\n" + "="*60)
    print("✅ ALL DIAGRAMS GENERATED SUCCESSFULLY!")
    print("="*60)
    print("\nFiles saved in current directory:")
    print("  • scoring_zones.png")
    print("  • weighted_aggregation.png")
    print("  • confidence_scenarios.png")
    print("  • size_comparison.png")
    print("  • tolerance_sensitivity.png")
    print("  • workflow_diagram.png")
    print("\nUse these images in your research panel presentation!")


if __name__ == "__main__":
    generate_all_diagrams()
