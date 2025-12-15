"""
Meta Aria 2 Surgical Training Analysis
Main entry point for processing Aria recordings
"""

import os
import sys
from pathlib import Path
import argparse
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent))

from detection.aria_detector import AriaDetector
from analysis.metrics_calculator import MetricsCalculator
from analysis.mps_analyzer import MPSDataAnalyzer
from visualization.dashboard_generator import DashboardGenerator

def main():
    parser = argparse.ArgumentParser(description='Analyze Meta Aria 2 surgical training recordings')
    parser.add_argument('--recording', type=str, help='Path to .vrs recording file')
    parser.add_argument('--recordings-dir', type=str, default='data/recordings', 
                       help='Directory containing multiple .vrs files')
    parser.add_argument('--output-dir', type=str, default='outputs/reports',
                       help='Directory for output reports')
    parser.add_argument('--mode', type=str, choices=['single', 'batch'], default='single',
                       help='Process single file or batch process directory')
    parser.add_argument('--visualize', action='store_true', 
                       help='Launch Rerun visualization')
    parser.add_argument('--detect-tools', action='store_true',
                       help='Enable surgical tool detection (requires model)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Meta Aria 2 Surgical Training Analysis")
    print("=" * 60)
    print()
    
    # Initialize components
    detector = AriaDetector(enable_tool_detection=args.detect_tools)
    metrics_calc = MetricsCalculator()
    mps_analyzer = MPSDataAnalyzer()
    dashboard_gen = DashboardGenerator()
    
    if args.mode == 'single':
        if not args.recording:
            print("ERROR: --recording required for single mode")
            print("Example: python src/main.py --recording data/recordings/session1.vrs")
            return
        
        process_single_recording(
            args.recording, 
            detector, 
            metrics_calc,
            mps_analyzer,
            dashboard_gen,
            args.output_dir,
            args.visualize
        )
    
    elif args.mode == 'batch':
        process_batch_recordings(
            args.recordings_dir,
            detector,
            metrics_calc,
            mps_analyzer,
            dashboard_gen,
            args.output_dir,
            args.visualize
        )

def process_single_recording(recording_path, detector, metrics_calc, mps_analyzer, dashboard_gen, output_dir, visualize):
    """Process a single Aria recording"""
    print(f"\nProcessing: {recording_path}")
    
    if not os.path.exists(recording_path):
        print(f"ERROR: Recording not found at {recording_path}")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_name = Path(recording_path).stem
    output_path = os.path.join(output_dir, f"{session_name}_{timestamp}")
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Output directory: {output_path}")
    print()
    
    # Step 1: Extract and process data
    print("[1/4] Loading Aria recording...")
    aria_data = detector.load_recording(recording_path)
    
    if aria_data is None:
        print("ERROR: Failed to load recording")
        return
    
    print(f"  ✓ Loaded {aria_data['num_frames']} frames")
    print(f"  ✓ Duration: {aria_data['duration']:.2f} seconds")
    print()
    
    # Step 1.5: Try to load MPS data if available
    mps_data = None
    recording_name = Path(recording_path).stem
    mps_folder = os.path.join('data', 'mps_data', recording_name)
    
    if os.path.exists(mps_folder):
        print("[1.5/4] Loading MPS data (hand tracking, eye gaze)...")
        try:
            from analysis.mps_analyzer import MPSDataAnalyzer
            mps_analyzer = MPSDataAnalyzer()
            mps_data = mps_analyzer.load_mps_data(mps_folder)
            print()
        except Exception as e:
            print(f"  ℹ Could not load MPS data: {e}")
            print()
    
    # Step 2: Analyze metrics
    print("[2/4] Analyzing surgical metrics...")
    metrics = metrics_calc.calculate_session_metrics(aria_data)
    
    # Add MPS metrics if available
    if mps_data:
        from analysis.mps_analyzer import MPSDataAnalyzer
        mps_analyzer = MPSDataAnalyzer()
        mps_metrics = mps_analyzer.generate_mps_report(mps_data, output_path)
        metrics['hand_tracking'] = mps_metrics.get('hand_tracking', {})
        metrics['eye_tracking'] = mps_metrics.get('eye_tracking', {})
        print(f"  ✓ Added MPS metrics")
    
    print(f"  ✓ Calculated {len(metrics)} metric categories")
    print()
    
    # Step 3: Generate visualizations
    print("[3/4] Generating visualizations...")
    if visualize:
        detector.visualize_with_rerun(aria_data, metrics)
    print("  ✓ Visualization ready")
    print()
    
    # Step 4: Create report
    print("[4/4] Generating performance report...")
    report_path = dashboard_gen.generate_report(
        session_name=session_name,
        metrics=metrics,
        aria_data=aria_data,
        output_path=output_path
    )
    print(f"  ✓ Report saved to: {report_path}")
    print()
    
    print("=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    print(f"\nResults saved to: {output_path}")
    print()
    print("Key Metrics Summary:")
    print_metrics_summary(metrics)

def process_batch_recordings(recordings_dir, detector, metrics_calc, mps_analyzer, dashboard_gen, output_dir, visualize):
    """Process multiple recordings in a directory"""
    print(f"\nScanning directory: {recordings_dir}")
    
    # Find all .vrs files
    recording_files = list(Path(recordings_dir).glob("*.vrs"))
    
    if not recording_files:
        print(f"No .vrs files found in {recordings_dir}")
        print("Please place your Aria recordings in this directory.")
        return
    
    print(f"Found {len(recording_files)} recording(s)")
    print()
    
    all_metrics = []
    
    for i, recording_path in enumerate(recording_files, 1):
        print(f"\n[Recording {i}/{len(recording_files)}] {recording_path.name}")
        print("-" * 60)
        
        try:
            process_single_recording(
                str(recording_path),
                detector,
                metrics_calc,
                mps_analyzer,
                dashboard_gen,
                output_dir,
                visualize and i == 1  # Only visualize first recording
            )
            print("✓ Success")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print()
    
    print("\n" + "=" * 60)
    print("Batch Processing Complete!")
    print("=" * 60)

def print_metrics_summary(metrics):
    """Print a quick summary of key metrics"""
    if not metrics:
        print("  No metrics calculated")
        return
    
    # Motion metrics
    if 'motion' in metrics:
        print(f"  Head Stability: {metrics['motion'].get('head_stability_score', 0):.2f}/10")
        print(f"  Hand Tremor (IMU): {metrics['motion'].get('avg_tremor', 0):.3f}")
    
    # Hand tracking metrics (from MPS)
    if 'hand_tracking' in metrics and metrics['hand_tracking']:
        print(f"  Path Length: {metrics['hand_tracking'].get('path_length_m', 0):.2f}m")
        print(f"  Hand Smoothness: {metrics['hand_tracking'].get('smoothness_score', 0):.1f}/10")
        print(f"  Hand Tremor (MPS): {metrics['hand_tracking'].get('hand_tremor', 0):.4f}")
    
    # Eye tracking metrics (from MPS)
    if 'eye_tracking' in metrics and metrics['eye_tracking']:
        print(f"  Gaze Stability: {metrics['eye_tracking'].get('gaze_stability', 0):.1f}/10")
    
    # Stress metrics
    if 'stress' in metrics:
        print(f"  Average Heart Rate: {metrics['stress'].get('avg_heart_rate', 0):.0f} bpm")
        print(f"  Peak Stress: {metrics['stress'].get('peak_stress_level', 0):.1f}/10")
    
    # Performance metrics
    if 'performance' in metrics:
        print(f"  Overall Score: {metrics['performance'].get('overall_score', 0):.1f}/100")

if __name__ == "__main__":
    main()