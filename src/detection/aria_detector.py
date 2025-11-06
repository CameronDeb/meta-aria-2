"""
Aria Detector - Handles loading and processing Aria recordings
"""

import numpy as np
from pathlib import Path
import logging

try:
    from projectaria_tools.core import data_provider
    from projectaria_tools.core.sensor_data import TimeDomain, TimeQueryOptions
    from projectaria_tools.core.stream_id import StreamId
    ARIA_AVAILABLE = True
except ImportError:
    ARIA_AVAILABLE = False
    print("WARNING: projectaria-tools not installed. Using simulation mode.")

try:
    import rerun as rr
    RERUN_AVAILABLE = True
except ImportError:
    RERUN_AVAILABLE = False
    print("WARNING: rerun-sdk not installed. Visualization disabled.")

import cv2

class AriaDetector:
    """Handles Meta Aria 2 data loading and processing"""
    
    # Stream IDs for Aria sensors
    RGB_CAMERA_ID = "214-1"  # Main RGB camera
    IMU_RIGHT_ID = "1202-1"   # Right IMU
    IMU_LEFT_ID = "1201-1"    # Left IMU
    
    def __init__(self, enable_tool_detection=False):
        self.enable_tool_detection = enable_tool_detection
        self.provider = None
        
        if not ARIA_AVAILABLE:
            print("Running in SIMULATION mode - will use sample data")
            self.simulation_mode = True
        else:
            self.simulation_mode = False
    
    def load_recording(self, vrs_path):
        """Load a .vrs recording file"""
        if self.simulation_mode:
            return self._create_simulation_data()
        
        try:
            print(f"  Loading VRS file: {vrs_path}")
            self.provider = data_provider.create_vrs_data_provider(vrs_path)
            
            # Get available streams
            print("  Detecting available streams...")
            
            # Extract data from recording
            aria_data = {
                'rgb_frames': [],
                'timestamps': [],
                'imu_data': [],
                'num_frames': 0,
                'duration': 0,
                'recording_path': vrs_path
            }
            
            # Get RGB stream
            rgb_stream_id = StreamId(self.RGB_CAMERA_ID)
            
            try:
                num_frames = self.provider.get_num_data(rgb_stream_id)
                aria_data['num_frames'] = num_frames
                
                # Get first and last timestamps for duration
                first_data = self.provider.get_image_data_by_index(rgb_stream_id, 0)
                last_data = self.provider.get_image_data_by_index(rgb_stream_id, num_frames-1)
                
                # Extract timestamps from ImageDataRecord objects
                try:
                    if isinstance(first_data, tuple):
                        first_timestamp = first_data[1]
                        last_timestamp = last_data[1]
                    elif hasattr(first_data, 'capture_timestamp_ns'):
                        first_timestamp = first_data.capture_timestamp_ns
                        last_timestamp = last_data.capture_timestamp_ns
                    else:
                        # For ImageDataRecord objects, access timestamp via method
                        first_timestamp = int(first_data.get_timestamp_ns())
                        last_timestamp = int(last_data.get_timestamp_ns())
                    
                    aria_data['duration'] = (last_timestamp - first_timestamp) / 1e9  # Convert to seconds
                except Exception as ts_error:
                    print(f"    ℹ Could not extract duration: {ts_error}")
                    aria_data['duration'] = num_frames / 30.0  # Estimate at 30fps
                
                print(f"  ✓ RGB stream found: {num_frames} frames")
                
                # Sample frames (process every Nth frame to save time)
                sample_rate = max(1, num_frames // 100)  # Sample ~100 frames
                
                for i in range(0, num_frames, sample_rate):
                    img_data = self.provider.get_image_data_by_index(rgb_stream_id, i)
                    
                    # Handle different return types from Aria SDK
                    try:
                        if isinstance(img_data, tuple):
                            # Tuple format: (ImageDataRecord, timestamp)
                            img_array = img_data[0].to_numpy_array()
                            timestamp = img_data[1]
                        elif hasattr(img_data, 'to_numpy_array'):
                            # ImageDataRecord object
                            img_array = img_data.to_numpy_array()
                            if hasattr(img_data, 'capture_timestamp_ns'):
                                timestamp = img_data.capture_timestamp_ns
                            elif hasattr(img_data, 'get_timestamp_ns'):
                                timestamp = int(img_data.get_timestamp_ns())
                            else:
                                timestamp = i * 33333333  # Estimate at 30fps
                        else:
                            print(f"    ℹ Unexpected image data type: {type(img_data)}")
                            continue
                        
                        aria_data['rgb_frames'].append(img_array)
                        aria_data['timestamps'].append(timestamp)
                    except Exception as frame_error:
                        print(f"    ℹ Error processing frame {i}: {frame_error}")
                        continue
                
                print(f"  ✓ Sampled {len(aria_data['rgb_frames'])} frames for analysis")
                
            except Exception as e:
                print(f"  ✗ Error accessing RGB stream: {e}")
            
            # Try to get IMU data
            try:
                imu_stream_id = StreamId(self.IMU_RIGHT_ID)
                num_imu = self.provider.get_num_data(imu_stream_id)
                
                # Sample IMU data
                sample_rate_imu = max(1, num_imu // 1000)  # Sample ~1000 points
                
                for i in range(0, num_imu, sample_rate_imu):
                    imu_data = self.provider.get_imu_data_by_index(imu_stream_id, i)
                    
                    # Handle different return types from Aria SDK
                    try:
                        if isinstance(imu_data, tuple):
                            imu_obj = imu_data[0]
                            timestamp = imu_data[1]
                        else:
                            imu_obj = imu_data
                            if hasattr(imu_data, 'capture_timestamp_ns'):
                                timestamp = imu_data.capture_timestamp_ns
                            elif hasattr(imu_data, 'get_timestamp_ns'):
                                timestamp = int(imu_data.get_timestamp_ns())
                            else:
                                timestamp = i * 1000000  # Estimate at 1000Hz
                        
                        aria_data['imu_data'].append({
                            'timestamp': timestamp,
                            'accel': np.array([imu_obj.accel_msec2[0], imu_obj.accel_msec2[1], imu_obj.accel_msec2[2]]),
                            'gyro': np.array([imu_obj.gyro_radsec[0], imu_obj.gyro_radsec[1], imu_obj.gyro_radsec[2]])
                        })
                    except Exception as imu_error:
                        print(f"    ℹ Error processing IMU sample {i}: {imu_error}")
                        continue
                
                print(f"  ✓ IMU stream found: {len(aria_data['imu_data'])} samples")
                
            except Exception as e:
                print(f"  ℹ IMU data not available: {e}")
            
            return aria_data
            
        except Exception as e:
            print(f"  ✗ Error loading recording: {e}")
            return None
    
    def _create_simulation_data(self):
        """Create simulated data for testing when Aria SDK is not available"""
        print("  Creating simulation data...")
        
        num_frames = 300  # 10 seconds at 30fps
        
        aria_data = {
            'rgb_frames': [],
            'timestamps': [],
            'imu_data': [],
            'num_frames': num_frames,
            'duration': 10.0,
            'recording_path': 'simulation'
        }
        
        # Generate synthetic frames
        for i in range(num_frames):
            # Create a simple test pattern
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            
            # Add moving object
            x = int(320 + 200 * np.sin(i * 0.1))
            y = int(240 + 100 * np.cos(i * 0.1))
            cv2.circle(frame, (x, y), 30, (0, 255, 0), -1)
            
            # Add frame number
            cv2.putText(frame, f"Frame {i}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            aria_data['rgb_frames'].append(frame)
            aria_data['timestamps'].append(i * 33333333)  # ~30fps in nanoseconds
        
        # Generate synthetic IMU data
        for i in range(num_frames * 10):  # IMU at higher rate
            aria_data['imu_data'].append({
                'timestamp': i * 3333333,
                'accel': np.array([
                    np.random.normal(0, 0.1),
                    np.random.normal(0, 0.1),
                    9.81 + np.random.normal(0, 0.1)
                ]),
                'gyro': np.array([
                    np.random.normal(0, 0.05),
                    np.random.normal(0, 0.05),
                    np.random.normal(0, 0.05)
                ])
            })
        
        print(f"  ✓ Created {num_frames} simulated frames")
        return aria_data
    
    def visualize_with_rerun(self, aria_data, metrics):
        """Visualize data using Rerun"""
        if not RERUN_AVAILABLE:
            print("  Rerun not available, skipping visualization")
            return
        
        print("  Launching Rerun visualization...")
        rr.init("aria_surgical_analysis", spawn=True)
        
        # Log video frames
        for i, (frame, timestamp) in enumerate(zip(aria_data['rgb_frames'], aria_data['timestamps'])):
            # Convert timestamp to integer if it's not already
            try:
                if isinstance(timestamp, int):
                    ts_nanos = timestamp
                elif hasattr(timestamp, 'get_timestamp_ns'):
                    ts_nanos = int(timestamp.get_timestamp_ns())
                elif hasattr(timestamp, '__int__'):
                    ts_nanos = int(timestamp)
                else:
                    # Fall back to frame-based timing
                    ts_nanos = i * 33333333  # ~30fps
                
                rr.set_time_nanos("timestamp", ts_nanos)
                rr.set_time_sequence("frame", i)
                
                rr.log("video/rgb", rr.Image(frame))
                
                # Log metrics if available
                if 'motion' in metrics and i < len(metrics['motion'].get('tremor_per_frame', [])):
                    tremor = metrics['motion']['tremor_per_frame'][i]
                    rr.log("metrics/tremor", rr.Scalar(tremor))
            except Exception as e:
                print(f"    ℹ Skipping frame {i} visualization: {e}")
                continue
        
        print("  ✓ Rerun visualization launched")
        print("  View at: http://localhost:9090")