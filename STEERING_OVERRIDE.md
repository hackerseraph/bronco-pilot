# Bronco-Pilot: FrogPilot with Steering Parameter Override

Bronco-Pilot is a custom fork of FrogPilot that integrates a **safe, simplified steering parameter override system** inspired by BluePilot's steering control enhancements.

## Overview

This project combines:
- **FrogPilot**: The base open-source driving assistance platform with enhanced features
- **Steering Parameter Override**: Safe runtime adjustment of torque control parameters

## Key Safety Features

### Minimal, Self-Contained Implementation
- **No external dependencies**: The override system is completely self-contained in FrogPilot
- **Fail-safe design**: If override is not configured, steering works normally
- **Parameter validation**: All override parameters are safely converted and validated
- **Low CPU overhead**: Parameters are only checked every ~3 seconds, not every frame
- **Exception handling**: All errors are gracefully handled with fallbacks

### How It Works

The steering override system allows runtime adjustment of three key steering torque parameters:

1. **Lateral Acceleration Factor** (`SteeringOverrideLatAccelFactor`)
   - Controls how strongly steering responds to lateral acceleration requests
   - Range: Typically 1.0-2.0 (higher = more responsive)
   - Default: Uses vehicle's factory calibration

2. **Friction Coefficient** (`SteeringOverrideFriction`)
   - Compensates for friction in the steering system
   - Range: 0.0-0.1 (higher = more aggressive over friction)
   - Default: Uses vehicle's factory calibration

3. **Lateral Acceleration Offset** (`SteeringOverrideLatAccelOffset`)
   - Corrects for roll measurement bias
   - Range: Typically -0.2 to 0.2
   - Default: 0.0

## How to Use

### Enable the Override System

```bash
# Enable steering override (requires system restart or controlsd restart)
params set SteeringOverrideEnabled True
```

### Set Override Parameters

```bash
# Set lateral acceleration factor
params set SteeringOverrideLatAccelFactor 1.2

# Set friction coefficient
params set SteeringOverrideFriction 0.015

# Set acceleration offset (optional)
params set SteeringOverrideLatAccelOffset 0.05
```

### Disable the Override System

```bash
params set SteeringOverrideEnabled False
```

## Implementation Details

### Modified File
- `selfdrive/controls/lib/latcontrol_torque.py`: Integrated override system

### New Files
- `selfdrive/controls/lib/steering_override.py`: Override system implementation

### Safety Guarantees

✅ **Graceful Failures**: If params can't be read, steering defaults to baseline  
✅ **No Null Dereferences**: All parameters are safely validated  
✅ **Exception Handling**: Errors logged but never crash the steering controller  
✅ **Slow Reading**: Parameters only checked every 3 seconds to minimize latency  
✅ **Type Safety**: All parameters converted to proper types before use  
✅ **No External Dependencies**: No sunnypilot-specific code or imports  

## Testing Recommendations

Before using on a vehicle, test in the following order:

1. **Baseline Test**: Drive without override enabled to confirm steering works normally
2. **Small Adjustments**: Enable override and make 5% adjustments to factors
3. **Monitor Behavior**: Watch for jerky steering or overshooting
4. **Revert if Issues**: Immediately disable override and return to baseline

## Known Limitations

- Override parameters are only applied when steering is active
- Parameters are sampled every ~3 seconds, not continuously
- No live parameter adjustment visible during driving
- Changes require controlsd restart to take effect immediately

## Credits

- **FrogPilot**: FrogAi community
- **BluePilot**: BluePilotDev community for steering control inspiration
- **Bronco-Pilot**: Custom safe implementation by @hackerseraph

## License

This project respects the licenses of both FrogPilot and BluePilot. See LICENSE.md for details.

