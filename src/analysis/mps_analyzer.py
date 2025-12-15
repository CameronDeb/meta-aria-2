"""
MPS Data Analyzer - Processes Meta's Machine Perception Services outputs
Handles hand tracking, eye gaze, and SLAM data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

class MPSDataAnalyzer:
    """Analyzes MPS output files alongside VRS recordings"""
    
    def __init__(self):
        self.hand_data = None
        self.eye_gaze_data = None
        self.slam_data = None
        
    def load_mps_data(self, mps_folder_path):
        """Load all MPS output files from a folder"""
        mps_path = Path(mps_folder_path)
        
        results = {
            'hand_tracking': None,
            'eye_gaze': None,
            'slam': None,
            'summary': None
        }
        
        # Load eye gaze
        eye_gaze_file = mps_path / "general_eye_gaze.csv"
        if eye_gaze_file.exists():
            print(f"  Loading eye gaze data...")
            results['eye_gaze'] = self._load_eye_gaze(eye_gaze_file)
            print(f"    ✓ {len(results['eye_gaze'])} gaze samples")
        
        # Load hand tracking
        hand_file = mps_path / "hand_tracking_results.csv"
        if not hand_file.exists():
            hand_file = mps_path / "hand_tracking.csv"  # Try alternate name
        
        if hand_file.exists():
            print(f"  Loading hand tracking data...")
            results['hand_tracking'] = self._load_hand_tracking(hand_file)
            print(f"    ✓ {len(results['hand_tracking'])} hand frames")
        else:
            print(f"    ℹ Hand tracking not found (file may be separate)")
        
        # Load summary
        summary_file = mps_path / "summary.json"
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                results['summary'] = json.load(f)
            print(f"    ✓ MPS summary loaded")
        
        return results
    
    def _load_eye_gaze(self, file_path):
        """Load and parse eye gaze CSV"""
        df = pd.read_csv(file_path)
        
        # Key columns:
        # - tracking_timestamp_us: timestamp in microseconds
        # - left_yaw_rads_cpf, right_yaw_rads_cpf: horizontal gaze direction
        # - pitch_rads_cpf: vertical gaze direction
        # - depth_m: depth to gaze point
        
        return df
    
    def _load_hand_tracking(self, file_path):
        """Load and parse hand tracking CSV"""
        df = pd.read_csv(file_path)
        
        # Meta Aria format uses landmarks (21 joints per hand)
        # Wrist is landmark 0
        # Format: tx_left_landmark_0_device, ty_left_landmark_0_device, tz_left_landmark_0_device
        
        # Rename columns for easier access (if using landmark format)
        if 'tx_right_landmark_0_device' in df.columns:
            df['wrist_position_x'] = df['tx_right_landmark_0_device']
            df['wrist_position_y'] = df['ty_right_landmark_0_device']
            df['wrist_position_z'] = df['tz_right_landmark_0_device']
            df['confidence'] = df['right_tracking_confidence']
        
        return df
    
    def calculate_gaze_metrics(self, eye_gaze_df):
        """Calculate eye tracking metrics"""
        if eye_gaze_df is None or len(eye_gaze_df) == 0:
            return {}
        
        metrics = {}
        
        # Gaze stability (variance in gaze direction)
        pitch_var = eye_gaze_df['pitch_rads_cpf'].var()
        left_yaw_var = eye_gaze_df['left_yaw_rads_cpf'].var()
        right_yaw_var = eye_gaze_df['right_yaw_rads_cpf'].var()
        
        # Combined gaze stability score (lower variance = more stable)
        gaze_variance = (pitch_var + left_yaw_var + right_yaw_var) / 3
        metrics['gaze_stability'] = max(0, 10 - gaze_variance * 100)
        
        # Average gaze depth (how far away looking)
        metrics['avg_gaze_depth_m'] = eye_gaze_df['depth_m'].mean()
        
        # Gaze focus (how consistent is depth)
        metrics['gaze_focus_consistency'] = 1.0 / (1.0 + eye_gaze_df['depth_m'].std())
        
        # Eye movement frequency (how often gaze shifts)
        # Calculate frame-to-frame changes
        pitch_diff = eye_gaze_df['pitch_rads_cpf'].diff().abs()
        yaw_diff = ((eye_gaze_df['left_yaw_rads_cpf'] + eye_gaze_df['right_yaw_rads_cpf']) / 2).diff().abs()
        
        metrics['avg_gaze_shift'] = (pitch_diff.mean() + yaw_diff.mean()) / 2
        metrics['saccades_per_second'] = (pitch_diff > 0.1).sum() / (len(eye_gaze_df) / 10)  # Assuming ~10Hz
        
        return metrics
    
    def calculate_hand_metrics(self, hand_df):
        """Calculate hand tracking metrics for surgical performance"""
        if hand_df is None or len(hand_df) == 0:
            return {}
        
        metrics = {}
        
        # Check which hand columns exist
        has_wrist = 'wrist_position_x' in hand_df.columns
        
        if has_wrist:
            # Path length - total distance hand traveled
            wrist_x = hand_df['wrist_position_x'].values
            wrist_y = hand_df['wrist_position_y'].values
            wrist_z = hand_df['wrist_position_z'].values
            
            # Filter out invalid frames (marked as -1, 0, or NaN)
            valid_mask = (~np.isnan(wrist_x)) & (wrist_x != -1) & (wrist_x != 0)
            if valid_mask.sum() < 10:  # Need at least 10 valid frames
                return metrics
            
            wrist_x = wrist_x[valid_mask]
            wrist_y = wrist_y[valid_mask]
            wrist_z = wrist_z[valid_mask]
            
            # Calculate 3D distance between consecutive frames
            dx = np.diff(wrist_x)
            dy = np.diff(wrist_y)
            dz = np.diff(wrist_z)
            distances = np.sqrt(dx**2 + dy**2 + dz**2)
            
            metrics['path_length_m'] = np.sum(distances)
            metrics['avg_speed_m_s'] = np.mean(distances) * 10  # Assuming ~10Hz
            
            # Smoothness - analyze velocity peaks
            velocities = distances * 10  # Convert to m/s
            metrics['velocity_variance'] = np.var(velocities)
            metrics['smoothness_score'] = max(0, 10 - metrics['velocity_variance'] * 1000)
            
            # Tremor - high frequency component
            from scipy import signal
            if len(velocities) > 100:
                # High-pass filter to isolate tremor
                sos = signal.butter(4, 0.2, 'hp', output='sos')
                tremor_signal = signal.sosfilt(sos, velocities)
                metrics['hand_tremor'] = np.mean(np.abs(tremor_signal))
            else:
                metrics['hand_tremor'] = 0.0
            
            # Workspace volume (bounding box of movement)
            metrics['workspace_volume_m3'] = (
                (wrist_x.max() - wrist_x.min()) *
                (wrist_y.max() - wrist_y.min()) *
                (wrist_z.max() - wrist_z.min())
            )
            
            # Movement efficiency (straight line distance / path length)
            start_pos = np.array([wrist_x[0], wrist_y[0], wrist_z[0]])
            end_pos = np.array([wrist_x[-1], wrist_y[-1], wrist_z[-1]])
            straight_line_dist = np.linalg.norm(end_pos - start_pos)
            metrics['efficiency'] = straight_line_dist / np.sum(distances) if np.sum(distances) > 0 else 0
        
        # Task time (from timestamps)
        if 'tracking_timestamp_us' in hand_df.columns:
            start_time = hand_df['tracking_timestamp_us'].iloc[0]
            end_time = hand_df['tracking_timestamp_us'].iloc[-1]
            metrics['task_duration_s'] = (end_time - start_time) / 1e6
        
        # Confidence (tracking quality)
        if 'confidence' in hand_df.columns:
            metrics['avg_confidence'] = hand_df['confidence'].mean()
        
        return metrics
    
    def generate_mps_report(self, mps_data, output_path):
        """Generate additional metrics for MPS data to add to main report"""
        
        report = {
            'eye_tracking': {},
            'hand_tracking': {},
            'combined': {}
        }
        
        # Eye gaze metrics
        if mps_data['eye_gaze'] is not None:
            report['eye_tracking'] = self.calculate_gaze_metrics(mps_data['eye_gaze'])
        
        # Hand tracking metrics
        if mps_data['hand_tracking'] is not None:
            report['hand_tracking'] = self.calculate_hand_metrics(mps_data['hand_tracking'])
        
        # Combined metrics (eye-hand coordination)
        if mps_data['eye_gaze'] is not None and mps_data['hand_tracking'] is not None:
            # TODO: Calculate eye-hand coordination metrics
            # - Are they looking where their hands are?
            # - Reaction time between gaze shift and hand movement
            pass
        
        return report