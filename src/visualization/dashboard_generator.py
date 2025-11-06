"""
Dashboard Generator - Creates HTML reports and visualizations
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
    
    def __init__(self):
        self.report_template = self._load_template()
    
    def generate_report(self, session_name, metrics, aria_data, output_path):
        """Generate complete performance report"""
        
        # Create visualizations
        charts_dir = os.path.join(output_path, 'charts')
        os.makedirs(charts_dir, exist_ok=True)
        
        self._create_motion_chart(metrics['motion'], charts_dir)
        self._create_stress_chart(metrics['stress'], aria_data, charts_dir)
        self._create_performance_chart(metrics['performance'], charts_dir)
        
        # Generate HTML report
        html_path = os.path.join(output_path, 'report.html')
        self._create_html_report(session_name, metrics, aria_data, html_path, charts_dir)
        
        # Save metrics as JSON
        json_path = os.path.join(output_path, 'metrics.json')
        self._save_metrics_json(metrics, aria_data, json_path)
        
        return html_path
    
    def _create_motion_chart(self, motion_metrics, output_dir):
        """Create motion analysis chart"""
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # Head stability
        ax = axes[0]
        stability_score = motion_metrics['head_stability_score']
        ax.barh(['Head Stability'], [stability_score], color='#4CAF50')
        ax.set_xlim(0, 10)
        ax.set_xlabel('Score (0-10)')
        ax.set_title('Head Stability Analysis')
        ax.grid(axis='x', alpha=0.3)
        
        # Tremor over time
        ax = axes[1]
        if motion_metrics.get('tremor_per_frame'):
            tremor_data = motion_metrics['tremor_per_frame']
            frames = range(len(tremor_data))
            ax.plot(frames, tremor_data, color='#2196F3', linewidth=2)
            ax.fill_between(frames, tremor_data, alpha=0.3, color='#2196F3')
            ax.set_xlabel('Frame')
            ax.set_ylabel('Tremor Magnitude')
            ax.set_title('Hand Tremor Over Time')
            ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'motion_analysis.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_stress_chart(self, stress_metrics, aria_data, output_dir):
        """Create stress analysis chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Simulated heart rate over time
        duration = aria_data['duration']
        time_points = np.linspace(0, duration, 100)
        
        # Generate simulated HR pattern
        avg_hr = stress_metrics['avg_heart_rate']
        hr_variation = stress_metrics['heart_rate_variability']
        heart_rate = avg_hr + np.random.normal(0, hr_variation/10, len(time_points))
        
        ax.plot(time_points, heart_rate, color='#F44336', linewidth=2, label='Heart Rate')
        ax.axhline(y=avg_hr, color='gray', linestyle='--', alpha=0.5, label=f'Average: {avg_hr:.0f} bpm')
        ax.fill_between(time_points, heart_rate, avg_hr, alpha=0.2, color='#F44336')
        
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Heart Rate (bpm)')
        ax.set_title('Stress Indicators During Session')
        ax.legend()
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'stress_analysis.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_performance_chart(self, performance_metrics, output_dir):
        """Create overall performance radar chart"""
        categories = ['Technical\nSkill', 'Stress\nManagement', 'Consistency']
        values = [
            performance_metrics['technical_skill'],
            performance_metrics['stress_management'],
            performance_metrics['consistency']
        ]
        
        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]  # Complete the circle
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        ax.plot(angles, values, 'o-', linewidth=2, color='#9C27B0')
        ax.fill(angles, values, alpha=0.25, color='#9C27B0')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_title('Performance Profile', size=16, pad=20)
        ax.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'performance_radar.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_html_report(self, session_name, metrics, aria_data, output_path, charts_dir):
        """Create HTML report"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Surgical Training Analysis - {session_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .subtitle {{ font-size: 1.1em; opacity: 0.9; }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            border-left: 4px solid;
        }}
        .metric-card.motion {{ border-color: #4CAF50; }}
        .metric-card.stress {{ border-color: #F44336; }}
        .metric-card.performance {{ border-color: #9C27B0; }}
        
        .metric-label {{ 
            font-size: 0.9em; 
            color: #666; 
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        .metric-value {{ 
            font-size: 2.5em; 
            font-weight: bold; 
            color: #333;
        }}
        .metric-unit {{ font-size: 0.5em; color: #999; }}
        
        .charts-section {{
            padding: 30px;
            background: #fafafa;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .chart-container img {{
            width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        .chart-title {{
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .summary {{
            padding: 30px;
            background: white;
        }}
        .summary h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #333;
        }}
        .summary-item {{
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            margin-bottom: 15px;
        }}
        
        footer {{
            padding: 20px;
            text-align: center;
            color: #666;
            background: #f8f9fa;
            font-size: 0.9em;
        }}
        
        .score-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            color: white;
        }}
        .score-excellent {{ background: #4CAF50; }}
        .score-good {{ background: #8BC34A; }}
        .score-fair {{ background: #FFC107; }}
        .score-poor {{ background: #F44336; }}
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
                <div class="metric-label">Average Tremor</div>
                <div class="metric-value">
                    {metrics['motion']['avg_tremor']:.3f}
                </div>
            </div>
            
            <div class="metric-card stress">
                <div class="metric-label">Avg Heart Rate</div>
                <div class="metric-value">
                    {metrics['stress']['avg_heart_rate']:.0f}<span class="metric-unit">bpm</span>
                </div>
            </div>
            
            <div class="metric-card stress">
                <div class="metric-label">Peak Stress Level</div>
                <div class="metric-value">
                    {metrics['stress']['peak_stress_level']:.1f}<span class="metric-unit">/10</span>
                </div>
            </div>
            
            <div class="metric-card performance">
                <div class="metric-label">Session Duration</div>
                <div class="metric-value">
                    {aria_data['duration']:.1f}<span class="metric-unit">sec</span>
                </div>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <div class="chart-title">📊 Motion Analysis</div>
                <img src="charts/motion_analysis.png" alt="Motion Analysis">
            </div>
            
            <div class="chart-container">
                <div class="chart-title">❤️ Stress Indicators</div>
                <img src="charts/stress_analysis.png" alt="Stress Analysis">
            </div>
            
            <div class="chart-container">
                <div class="chart-title">🎯 Performance Profile</div>
                <img src="charts/performance_radar.png" alt="Performance Profile">
            </div>
        </div>
        
        <div class="summary">
            <h2>Summary & Recommendations</h2>
            
            <div class="summary-item">
                <strong>Performance Rating:</strong>
                {self._get_performance_badge(metrics['performance']['overall_score'])}
            </div>
            
            <div class="summary-item">
                <strong>Key Strengths:</strong><br>
                {self._get_strengths(metrics)}
            </div>
            
            <div class="summary-item">
                <strong>Areas for Improvement:</strong><br>
                {self._get_improvements(metrics)}
            </div>
            
            <div class="summary-item">
                <strong>Next Steps:</strong><br>
                • Continue practicing with focus on identified weaknesses<br>
                • Review video recording for technique refinement<br>
                • Compare with previous sessions to track progress<br>
                • Consider stress management techniques for high-pressure moments
            </div>
        </div>
        
        <footer>
            <p>Generated by Meta Aria 2 Surgical Training Analysis System</p>
            <p>Data recorded: {aria_data['num_frames']} frames | {aria_data['duration']:.1f} seconds</p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _get_performance_badge(self, score):
        """Get HTML badge for performance score"""
        if score >= 80:
            return '<span class="score-badge score-excellent">Excellent</span>'
        elif score >= 60:
            return '<span class="score-badge score-good">Good</span>'
        elif score >= 40:
            return '<span class="score-badge score-fair">Fair</span>'
        else:
            return '<span class="score-badge score-poor">Needs Improvement</span>'
    
    def _get_strengths(self, metrics):
        """Identify key strengths"""
        strengths = []
        
        if metrics['motion']['head_stability_score'] >= 7:
            strengths.append("Excellent head stability")
        if metrics['motion']['avg_tremor'] < 0.05:
            strengths.append("Minimal hand tremor")
        if metrics['stress']['peak_stress_level'] < 5:
            strengths.append("Good stress management")
        
        return "<br>• ".join([""] + strengths) if strengths else "Continue building core skills"
    
    def _get_improvements(self, metrics):
        """Identify areas for improvement"""
        improvements = []
        
        if metrics['motion']['head_stability_score'] < 5:
            improvements.append("Work on maintaining steady head position")
        if metrics['motion']['avg_tremor'] > 0.1:
            improvements.append("Practice hand steadiness exercises")
        if metrics['stress']['peak_stress_level'] > 7:
            improvements.append("Develop stress management techniques")
        
        return "<br>• ".join([""] + improvements) if improvements else "Maintain current performance level"
    
    def _save_metrics_json(self, metrics, aria_data, output_path):
        """Save metrics as JSON for further analysis"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'session_info': {
                'duration': aria_data['duration'],
                'num_frames': aria_data['num_frames'],
                'recording_path': aria_data['recording_path']
            },
            'metrics': {
                'motion': {k: v for k, v in metrics['motion'].items() if not isinstance(v, list)},
                'stability': metrics['stability'],
                'stress': metrics['stress'],
                'performance': metrics['performance']
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_template(self):
        """Load HTML template (placeholder)"""
        return ""