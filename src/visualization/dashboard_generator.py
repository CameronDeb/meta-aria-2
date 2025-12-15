"""
Dashboard Generator - Creates HTML reports and visualizations
UPDATED: Removed heart rate, added expert benchmarks, better training recommendations
"""

import os
import json
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

class DashboardGenerator:
    """Generate performance dashboards and reports"""
    
    # Expert benchmark values for comparison
    EXPERT_BENCHMARKS = {
        'head_stability': 9.5,
        'visual_stability': 9.0,
        'gaze_stability': 9.5,
        'path_length_m': 1.5,  # Lower is better
        'smoothness_score': 8.0,
        'hand_tremor': 0.003,  # Lower is better
        'efficiency': 0.6,
        'avg_tremor': 0.03,  # Lower is better
    }
    
    def __init__(self):
        pass
    
    def generate_report(self, session_name, metrics, aria_data, output_path):
        """Generate complete performance report"""
        
        # Create visualizations
        charts_dir = os.path.join(output_path, 'charts')
        os.makedirs(charts_dir, exist_ok=True)
        
        self._create_skill_radar_chart(metrics, charts_dir)
        self._create_hand_movement_chart(metrics, charts_dir)
        self._create_improvement_areas_chart(metrics, charts_dir)
        
        # Generate HTML report
        html_path = os.path.join(output_path, 'report.html')
        self._create_html_report(session_name, metrics, aria_data, html_path, charts_dir)
        
        # Save metrics as JSON
        json_path = os.path.join(output_path, 'metrics.json')
        self._save_metrics_json(metrics, aria_data, json_path)
        
        return html_path
    
    def _create_skill_radar_chart(self, metrics, output_dir):
        """Create radar chart comparing current performance to expert level"""
        categories = []
        current_scores = []
        expert_scores = []
        
        # Collect metrics for radar chart (normalize to 0-10 scale)
        if 'motion' in metrics:
            categories.append('Head\nStability')
            current_scores.append(metrics['motion']['head_stability_score'])
            expert_scores.append(self.EXPERT_BENCHMARKS['head_stability'])
        
        if 'stability' in metrics:
            categories.append('Visual\nStability')
            current_scores.append(metrics['stability']['visual_stability'])
            expert_scores.append(self.EXPERT_BENCHMARKS['visual_stability'])
        
        if 'eye_tracking' in metrics and metrics['eye_tracking']:
            categories.append('Gaze\nStability')
            current_scores.append(metrics['eye_tracking'].get('gaze_stability', 0))
            expert_scores.append(self.EXPERT_BENCHMARKS['gaze_stability'])
        
        if 'hand_tracking' in metrics and metrics['hand_tracking']:
            categories.append('Hand\nSmoothness')
            current_scores.append(metrics['hand_tracking'].get('smoothness_score', 0))
            expert_scores.append(self.EXPERT_BENCHMARKS['smoothness_score'])
            
            categories.append('Movement\nEfficiency')
            efficiency = metrics['hand_tracking'].get('efficiency', 0) * 10
            current_scores.append(efficiency)
            expert_scores.append(self.EXPERT_BENCHMARKS['efficiency'] * 10)
        
        if len(categories) < 3:
            return  # Need at least 3 metrics for radar chart
        
        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        current_scores += current_scores[:1]
        expert_scores += expert_scores[:1]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        ax.plot(angles, expert_scores, 'o-', linewidth=2, label='Expert Level', color='#4CAF50')
        ax.fill(angles, expert_scores, alpha=0.15, color='#4CAF50')
        
        ax.plot(angles, current_scores, 'o-', linewidth=2, label='Your Performance', color='#2196F3')
        ax.fill(angles, current_scores, alpha=0.25, color='#2196F3')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=11)
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2', '4', '6', '8', '10'], size=9)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
        ax.set_title('Surgical Skills Assessment', size=14, weight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'skill_radar.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_hand_movement_chart(self, metrics, output_dir):
        """Create chart showing hand movement metrics"""
        if 'hand_tracking' not in metrics or not metrics['hand_tracking']:
            return
        
        ht = metrics['hand_tracking']
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Path Length comparison
        ax = axes[0, 0]
        current_path = ht.get('path_length_m', 0)
        expert_path = self.EXPERT_BENCHMARKS['path_length_m']
        
        bars = ax.bar(['Your Path', 'Expert Path'], [current_path, expert_path], 
                      color=['#FF5722', '#4CAF50'])
        ax.set_ylabel('Distance (meters)', fontsize=11)
        ax.set_title('Path Length (Lower is Better)', fontsize=12, weight='bold')
        ax.set_ylim(0, max(current_path, expert_path) * 1.2)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}m', ha='center', va='bottom', fontsize=10)
        
        # Smoothness comparison
        ax = axes[0, 1]
        current_smooth = ht.get('smoothness_score', 0)
        expert_smooth = self.EXPERT_BENCHMARKS['smoothness_score']
        
        bars = ax.bar(['Your Smoothness', 'Expert Smoothness'], [current_smooth, expert_smooth],
                      color=['#FF9800', '#4CAF50'])
        ax.set_ylabel('Score (0-10)', fontsize=11)
        ax.set_title('Movement Smoothness (Higher is Better)', fontsize=12, weight='bold')
        ax.set_ylim(0, 10)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=10)
        
        # Tremor comparison
        ax = axes[1, 0]
        current_tremor = ht.get('hand_tremor', 0)
        expert_tremor = self.EXPERT_BENCHMARKS['hand_tremor']
        
        bars = ax.bar(['Your Tremor', 'Expert Tremor'], [current_tremor, expert_tremor],
                      color=['#F44336', '#4CAF50'])
        ax.set_ylabel('Tremor Magnitude', fontsize=11)
        ax.set_title('Hand Tremor (Lower is Better)', fontsize=12, weight='bold')
        ax.set_ylim(0, max(current_tremor, expert_tremor) * 1.2)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.4f}', ha='center', va='bottom', fontsize=10)
        
        # Efficiency comparison
        ax = axes[1, 1]
        current_eff = ht.get('efficiency', 0)
        expert_eff = self.EXPERT_BENCHMARKS['efficiency']
        
        bars = ax.bar(['Your Efficiency', 'Expert Efficiency'], [current_eff, expert_eff],
                      color=['#FFC107', '#4CAF50'])
        ax.set_ylabel('Efficiency (0-1)', fontsize=11)
        ax.set_title('Movement Efficiency (Higher is Better)', fontsize=12, weight='bold')
        ax.set_ylim(0, 1.0)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'hand_movement.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_improvement_areas_chart(self, metrics, output_dir):
        """Create chart showing areas needing improvement"""
        areas = []
        gaps = []
        colors = []
        
        # Calculate gaps from expert performance
        if 'motion' in metrics:
            head_gap = self.EXPERT_BENCHMARKS['head_stability'] - metrics['motion']['head_stability_score']
            if head_gap > 0.5:
                areas.append('Head Stability')
                gaps.append(head_gap)
                colors.append('#2196F3')
        
        if 'stability' in metrics:
            visual_gap = self.EXPERT_BENCHMARKS['visual_stability'] - metrics['stability']['visual_stability']
            if visual_gap > 0.5:
                areas.append('Visual Stability')
                gaps.append(visual_gap)
                colors.append('#03A9F4')
        
        if 'hand_tracking' in metrics and metrics['hand_tracking']:
            smooth_gap = self.EXPERT_BENCHMARKS['smoothness_score'] - metrics['hand_tracking'].get('smoothness_score', 0)
            if smooth_gap > 1.0:
                areas.append('Hand Smoothness')
                gaps.append(smooth_gap)
                colors.append('#FF5722')
            
            eff_gap = self.EXPERT_BENCHMARKS['efficiency'] - metrics['hand_tracking'].get('efficiency', 0)
            if eff_gap > 0.2:
                areas.append('Movement Efficiency')
                gaps.append(eff_gap * 10)  # Scale to 0-10
                colors.append('#FF9800')
            
            tremor_current = metrics['hand_tracking'].get('hand_tremor', 0)
            tremor_gap = (tremor_current - self.EXPERT_BENCHMARKS['hand_tremor']) / self.EXPERT_BENCHMARKS['hand_tremor'] * 2
            if tremor_gap > 1.0:
                areas.append('Hand Tremor')
                gaps.append(min(tremor_gap, 10))
                colors.append('#F44336')
        
        if not areas:
            # No significant gaps - create positive chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, '🎉 Excellent Performance!\nAll metrics near expert level',
                   ha='center', va='center', fontsize=18, weight='bold')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            y_pos = np.arange(len(areas))
            
            bars = ax.barh(y_pos, gaps, color=colors)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(areas, fontsize=11)
            ax.set_xlabel('Gap from Expert Level', fontsize=11)
            ax.set_title('Priority Training Areas', fontsize=14, weight='bold')
            ax.invert_yaxis()
            
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f' {width:.1f}', ha='left', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'improvement_areas.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    def _generate_recommendations(self, metrics):
        """Generate specific training recommendations"""
        recommendations = []
        
        # Check hand tracking metrics
        if 'hand_tracking' in metrics and metrics['hand_tracking']:
            ht = metrics['hand_tracking']
            
            path_length = ht.get('path_length_m', 0)
            if path_length > 3.0:
                recommendations.append({
                    'priority': 'HIGH',
                    'area': 'Path Length',
                    'issue': f'Your hands traveled {path_length:.1f}m (expert: ~1.5m)',
                    'advice': 'Plan movements before executing. Practice deliberate, direct movements to the target. Avoid unnecessary adjustments.'
                })
            
            smoothness = ht.get('smoothness_score', 0)
            if smoothness < 5.0:
                recommendations.append({
                    'priority': 'HIGH',
                    'area': 'Movement Smoothness',
                    'issue': f'Smoothness score: {smoothness:.1f}/10 (expert: ~8/10)',
                    'advice': 'Practice slow, controlled movements. Focus on continuous motion without stops or jerks. Use simulator for repetitive practice.'
                })
            
            efficiency = ht.get('efficiency', 0)
            if efficiency < 0.3:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'area': 'Movement Efficiency',
                    'issue': f'Only {efficiency*100:.0f}% efficient (expert: ~60%)',
                    'advice': 'Reduce backtracking and corrections. Visualize the path before moving. Work on hand-eye coordination exercises.'
                })
            
            tremor = ht.get('hand_tremor', 0)
            if tremor > 0.01:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'area': 'Hand Tremor',
                    'issue': f'Tremor: {tremor:.4f} (expert: <0.003)',
                    'advice': 'Practice hand steadiness exercises. Ensure proper rest before procedures. Consider ergonomic adjustments to reduce fatigue.'
                })
        
        # Check stability metrics
        if 'motion' in metrics:
            head_stab = metrics['motion']['head_stability_score']
            if head_stab < 8.0:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'area': 'Head Stability',
                    'issue': f'Head stability: {head_stab:.1f}/10',
                    'advice': 'Maintain steady head position. Adjust workstation height for comfort. Minimize unnecessary head movements.'
                })
        
        if 'eye_tracking' in metrics and metrics['eye_tracking']:
            gaze_stab = metrics['eye_tracking'].get('gaze_stability', 0)
            if gaze_stab < 8.0:
                recommendations.append({
                    'priority': 'LOW',
                    'area': 'Gaze Stability',
                    'issue': f'Gaze stability: {gaze_stab:.1f}/10',
                    'advice': 'Practice maintaining visual focus on operative field. Reduce rapid eye movements between instruments and target.'
                })
        
        # Sort by priority
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        recommendations.sort(key=lambda x: priority_order[x['priority']])
        
        return recommendations
    
    def _create_html_report(self, session_name, metrics, aria_data, output_path, charts_dir):
        """Create HTML report with all metrics and visualizations"""
        
        recommendations = self._generate_recommendations(metrics)
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Surgical Training Analysis - {session_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .metric-card.performance {{
            border-left: 5px solid #9C27B0;
        }}
        
        .metric-card.motion {{
            border-left: 5px solid #2196F3;
        }}
        
        .metric-card.hand {{
            border-left: 5px solid #FF5722;
        }}
        
        .metric-card.eye {{
            border-left: 5px solid #4CAF50;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }}
        
        .metric-unit {{
            font-size: 0.5em;
            color: #999;
            margin-left: 5px;
        }}
        
        .charts-section {{
            padding: 40px;
        }}
        
        .chart-container {{
            margin-bottom: 40px;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;
        }}
        
        .chart-container img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        
        .recommendations-section {{
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .recommendations-title {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 30px;
            color: #333;
        }}
        
        .recommendation {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            border-left: 5px solid #ccc;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .recommendation.high {{
            border-left-color: #F44336;
        }}
        
        .recommendation.medium {{
            border-left-color: #FF9800;
        }}
        
        .recommendation.low {{
            border-left-color: #4CAF50;
        }}
        
        .rec-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .rec-area {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}
        
        .rec-priority {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            color: white;
        }}
        
        .rec-priority.high {{
            background: #F44336;
        }}
        
        .rec-priority.medium {{
            background: #FF9800;
        }}
        
        .rec-priority.low {{
            background: #4CAF50;
        }}
        
        .rec-issue {{
            color: #666;
            margin-bottom: 10px;
            font-size: 1.05em;
        }}
        
        .rec-advice {{
            color: #333;
            font-size: 1.05em;
            line-height: 1.6;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🩺 Surgical Training Analysis</h1>
            <p class="subtitle">Session: {session_name}</p>
            <p class="subtitle">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </header>
        
        <div class="metrics-grid">
            <div class="metric-card performance">
                <div class="metric-label">Overall Performance</div>
                <div class="metric-value">
                    {metrics['performance']['overall_score']:.1f}<span class="metric-unit">/100</span>
                </div>
            </div>
            
            <div class="metric-card motion">
                <div class="metric-label">Head Stability</div>
                <div class="metric-value">
                    {metrics['motion']['head_stability_score']:.1f}<span class="metric-unit">/10</span>
                </div>
            </div>
            
            <div class="metric-card motion">
                <div class="metric-label">Visual Stability</div>
                <div class="metric-value">
                    {metrics['stability']['visual_stability']:.1f}<span class="metric-unit">/10</span>
                </div>
            </div>
            
            <div class="metric-card performance">
                <div class="metric-label">Session Duration</div>
                <div class="metric-value">
                    {aria_data['duration']:.1f}<span class="metric-unit">sec</span>
                </div>
            </div>"""
        
        # Add hand tracking metrics if available
        if 'hand_tracking' in metrics and metrics['hand_tracking']:
            html_content += f"""
            
            <div class="metric-card hand">
                <div class="metric-label">Path Length</div>
                <div class="metric-value">
                    {metrics['hand_tracking'].get('path_length_m', 0):.2f}<span class="metric-unit">m</span>
                </div>
            </div>
            
            <div class="metric-card hand">
                <div class="metric-label">Hand Smoothness</div>
                <div class="metric-value">
                    {metrics['hand_tracking'].get('smoothness_score', 0):.1f}<span class="metric-unit">/10</span>
                </div>
            </div>
            
            <div class="metric-card hand">
                <div class="metric-label">Movement Efficiency</div>
                <div class="metric-value">
                    {metrics['hand_tracking'].get('efficiency', 0):.2f}
                </div>
            </div>
            
            <div class="metric-card hand">
                <div class="metric-label">Hand Tremor</div>
                <div class="metric-value">
                    {metrics['hand_tracking'].get('hand_tremor', 0):.4f}
                </div>
            </div>"""
        
        # Add eye tracking metrics if available  
        if 'eye_tracking' in metrics and metrics['eye_tracking']:
            html_content += f"""
            
            <div class="metric-card eye">
                <div class="metric-label">Gaze Stability</div>
                <div class="metric-value">
                    {metrics['eye_tracking'].get('gaze_stability', 0):.1f}<span class="metric-unit">/10</span>
                </div>
            </div>
            
            <div class="metric-card eye">
                <div class="metric-label">Working Distance</div>
                <div class="metric-value">
                    {metrics['eye_tracking'].get('avg_gaze_depth_m', 0):.2f}<span class="metric-unit">m</span>
                </div>
            </div>"""
        
        html_content += """
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <div class="chart-title">📊 Surgical Skills Radar</div>
                <img src="charts/skill_radar.png" alt="Skills Radar">
            </div>"""
        
        if 'hand_tracking' in metrics and metrics['hand_tracking']:
            html_content += """
            
            <div class="chart-container">
                <div class="chart-title">✋ Hand Movement Analysis</div>
                <img src="charts/hand_movement.png" alt="Hand Movement">
            </div>"""
        
        html_content += """
            
            <div class="chart-container">
                <div class="chart-title">🎯 Priority Training Areas</div>
                <img src="charts/improvement_areas.png" alt="Improvement Areas">
            </div>
        </div>
        
        <div class="recommendations-section">
            <div class="recommendations-title">💡 Personalized Training Recommendations</div>"""
        
        if recommendations:
            for rec in recommendations:
                html_content += f"""
            <div class="recommendation {rec['priority'].lower()}">
                <div class="rec-header">
                    <div class="rec-area">{rec['area']}</div>
                    <div class="rec-priority {rec['priority'].lower()}">{rec['priority']}</div>
                </div>
                <div class="rec-issue">{rec['issue']}</div>
                <div class="rec-advice"><strong>Recommendation:</strong> {rec['advice']}</div>
            </div>"""
        else:
            html_content += """
            <div class="recommendation low">
                <div class="rec-header">
                    <div class="rec-area">Excellent Performance!</div>
                    <div class="rec-priority low">GREAT</div>
                </div>
                <div class="rec-advice">Your performance is at or near expert level across all measured metrics. Continue practicing to maintain these skills.</div>
            </div>"""
        
        html_content += """
        </div>
    </div>
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _save_metrics_json(self, metrics, aria_data, output_path):
        """Save metrics as JSON for further analysis"""
        export_data = {
            'session_info': {
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': aria_data['duration'],
                'num_frames': aria_data['num_frames']
            },
            'metrics': metrics
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)