"""
Metrics Calculator - Analyzes surgical performance metrics from Aria data
"""

import numpy as np
from scipy import signal
from scipy.stats import variation

class MetricsCalculator:
    """Calculate surgical training metrics from Aria sensor data"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_session_metrics(self, aria_data):
        """Calculate all metrics for a recording session"""
        metrics = {
            'motion': self._calculate_motion_metrics(aria_data),
            'stability': self._calculate_stability_metrics(aria_data),
            'stress': self._calculate_stress_metrics(aria_data),
            'performance': {}
        }
        
        # Calculate overall performance score
        metrics['performance'] = self._calculate_performance_score(metrics)
        
        return metrics
    
    def _calculate_motion_metrics(self, aria_data):
        """Calculate head motion and tremor metrics"""
        print("  Analyzing motion data...")
        
        motion_metrics = {
            'head_movement_total': 0,
            'head_stability_score': 0,
            'avg_tremor': 0,
            'tremor_per_frame': []
        }
        
        if not aria_data.get('imu_data'):
            print("    ℹ No IMU data available, using defaults")
            return motion_metrics
        
        imu_data = aria_data['imu_data']
        
        # Calculate head movement from gyroscope data
        gyro_magnitudes = []
        accel_magnitudes = []
        
        for imu_sample in imu_data:
            # Calculate magnitude of rotational movement
            gyro_mag = np.linalg.norm(imu_sample['gyro'])
            gyro_magnitudes.append(gyro_mag)
            
            # Calculate linear acceleration (excluding gravity)
            accel = imu_sample['accel']
            accel_mag = np.linalg.norm(accel - np.array([0, 0, 9.81]))
            accel_magnitudes.append(accel_mag)
        
        gyro_magnitudes = np.array(gyro_magnitudes)
        accel_magnitudes = np.array(accel_magnitudes)
        
        # Total head movement (integral of gyro)
        motion_metrics['head_movement_total'] = np.sum(gyro_magnitudes)
        
        # Stability score (inverse of movement variance)
        gyro_std = np.std(gyro_magnitudes)
        motion_metrics['head_stability_score'] = max(0, 10 - gyro_std * 10)
        
        # Tremor analysis (high frequency component of acceleration)
        if len(accel_magnitudes) > 100:
            # Apply high-pass filter to isolate tremor
            sos = signal.butter(4, 0.1, 'hp', output='sos')
            tremor_signal = signal.sosfilt(sos, accel_magnitudes)
            motion_metrics['avg_tremor'] = np.mean(np.abs(tremor_signal))
            
            # Downsample tremor to match frame count
            num_frames = aria_data['num_frames']
            motion_metrics['tremor_per_frame'] = [
                np.mean(np.abs(tremor_signal[i:i+10])) if i+10 < len(tremor_signal) else 0
                for i in range(0, len(tremor_signal), max(1, len(tremor_signal) // num_frames))
            ][:num_frames]
        
        print(f"    ✓ Head stability: {motion_metrics['head_stability_score']:.2f}/10")
        print(f"    ✓ Average tremor: {motion_metrics['avg_tremor']:.4f}")
        
        return motion_metrics
    
    def _calculate_stability_metrics(self, aria_data):
        """Calculate visual stability and focus metrics"""
        print("  Analyzing stability metrics...")
        
        stability_metrics = {
            'focus_score': 0,
            'visual_stability': 0,
            'frame_jitter': 0
        }
        
        if len(aria_data['rgb_frames']) < 2:
            return stability_metrics
        
        # Calculate frame-to-frame differences (optical flow proxy)
        frame_diffs = []
        
        for i in range(1, min(len(aria_data['rgb_frames']), 50)):
            frame1 = aria_data['rgb_frames'][i-1]
            frame2 = aria_data['rgb_frames'][i]
            
            # Convert to grayscale for comparison
            if len(frame1.shape) == 3:
                gray1 = np.mean(frame1, axis=2)
                gray2 = np.mean(frame2, axis=2)
            else:
                gray1 = frame1
                gray2 = frame2
            
            # Calculate frame difference
            diff = np.mean(np.abs(gray1.astype(float) - gray2.astype(float)))
            frame_diffs.append(diff)
        
        frame_diffs = np.array(frame_diffs)
        
        # Visual stability (low frame differences = stable)
        stability_metrics['frame_jitter'] = np.std(frame_diffs)
        stability_metrics['visual_stability'] = max(0, 10 - stability_metrics['frame_jitter'] / 10)
        
        # Focus score (inverse of blur - simplified)
        stability_metrics['focus_score'] = 7.5  # Placeholder
        
        print(f"    ✓ Visual stability: {stability_metrics['visual_stability']:.2f}/10")
        
        return stability_metrics
    
    def _calculate_stress_metrics(self, aria_data):
        """Calculate stress indicators (simulated for now)"""
        print("  Analyzing stress indicators...")
        
        # Note: Real heart rate data would come from Aria's PPG sensor
        # For now, we'll estimate stress from motion data
        
        stress_metrics = {
            'avg_heart_rate': 0,
            'heart_rate_variability': 0,
            'peak_stress_level': 0,
            'stress_correlation': []
        }
        
        if not aria_data.get('imu_data'):
            # Use simulated values
            duration = aria_data['duration']
            stress_metrics['avg_heart_rate'] = 75 + np.random.randint(-5, 15)
            stress_metrics['heart_rate_variability'] = np.random.uniform(30, 60)
            stress_metrics['peak_stress_level'] = np.random.uniform(5, 8)
        else:
            # Estimate stress from motion variability
            imu_data = aria_data['imu_data']
            accel_vars = [np.var(sample['accel']) for sample in imu_data]
            
            # Simulated heart rate based on movement
            avg_var = np.mean(accel_vars)
            stress_metrics['avg_heart_rate'] = int(70 + avg_var * 50)
            stress_metrics['heart_rate_variability'] = np.std(accel_vars) * 100
            stress_metrics['peak_stress_level'] = min(10, avg_var * 100)
        
        print(f"    ✓ Estimated heart rate: {stress_metrics['avg_heart_rate']:.0f} bpm")
        print(f"    ✓ Peak stress level: {stress_metrics['peak_stress_level']:.1f}/10")
        
        return stress_metrics
    
    def _calculate_performance_score(self, metrics):
        """Calculate overall performance score"""
        print("  Calculating overall performance...")
        
        performance = {
            'overall_score': 0,
            'technical_skill': 0,
            'stress_management': 0,
            'consistency': 0
        }
        
        # Technical skill (motion + stability)
        motion_score = metrics['motion']['head_stability_score']
        stability_score = metrics['stability']['visual_stability']
        performance['technical_skill'] = (motion_score + stability_score) / 2
        
        # Stress management (inverse of stress level)
        stress_level = metrics['stress']['peak_stress_level']
        performance['stress_management'] = max(0, 10 - stress_level)
        
        # Consistency (low tremor + low jitter)
        tremor = metrics['motion']['avg_tremor']
        jitter = metrics['stability']['frame_jitter']
        performance['consistency'] = max(0, 10 - (tremor * 100 + jitter / 10))
        
        # Overall score (weighted average)
        performance['overall_score'] = (
            performance['technical_skill'] * 0.4 +
            performance['stress_management'] * 0.3 +
            performance['consistency'] * 0.3
        ) * 10  # Scale to 0-100
        
        print(f"    ✓ Overall performance: {performance['overall_score']:.1f}/100")
        
        return performance