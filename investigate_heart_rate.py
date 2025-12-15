"""
Investigate all available sensor streams in VRS file to find heart rate
"""

from projectaria_tools.core import data_provider
from projectaria_tools.core.stream_id import StreamId
import sys

vrs_path = "data/recordings/Surgery_2.vrs"

print("="*60)
print("Investigating Sensor Streams for Heart Rate")
print("="*60)

provider = data_provider.create_vrs_data_provider(vrs_path)

print("\nAll available streams:")
print("-"*60)

all_streams = provider.get_all_streams()
for stream_id in all_streams:
    try:
        label = provider.get_label(stream_id)
        num_data = provider.get_num_data(stream_id)
        print(f"{stream_id}: {label} ({num_data} samples)")
        
        # Try to get first sample to see data type
        if num_data > 0:
            try:
                # Try different data access methods
                sample = provider.get_sensor_data_by_index(stream_id, 0)
                print(f"  Type: {type(sample)}")
                if hasattr(sample, '__dict__'):
                    print(f"  Attributes: {list(vars(sample).keys())[:5]}")
            except:
                pass
    except Exception as e:
        print(f"{stream_id}: Error - {e}")

print("\n" + "="*60)
print("Checking specific health-related stream IDs:")
print("-"*60)

# Known potential health stream IDs
health_stream_candidates = [
    "286-1",  # Failed to activate (might be health)
    "247-1",  # Barometer (confirmed)
    "290-1", "291-1", "292-1", "293-1",  # Potential health streams
    "1204-1", "1205-1",  # Other potential sensors
]

for stream_id_str in health_stream_candidates:
    try:
        sid = StreamId(stream_id_str)
        num_data = provider.get_num_data(sid)
        if num_data > 0:
            print(f"✓ {stream_id_str}: {num_data} samples")
            # Try to access first sample
            try:
                data = provider.get_sensor_data_by_index(sid, 0)
                print(f"  Sample type: {type(data)}")
                if hasattr(data, '__dict__'):
                    attrs = list(vars(data).keys())
                    print(f"  Attributes: {attrs[:10]}")
            except Exception as e:
                print(f"  Cannot access: {e}")
        else:
            print(f"✗ {stream_id_str}: Not available")
    except Exception as e:
        print(f"✗ {stream_id_str}: {e}")

print("\n" + "="*60)
print("Conclusion:")
print("="*60)

print("""
Meta Aria 2 glasses have PPG sensors, but:
1. They may not be enabled by default in recording settings
2. The data might require special MPS processing (like hand tracking)
3. Stream 286-1 fails to activate - this might be the PPG sensor

Recommendations:
1. Check Meta Aria app recording settings - enable health sensors
2. Upload VRS to Meta's MPS and request health/PPG processing
3. Check if there's a separate health data export option
""")