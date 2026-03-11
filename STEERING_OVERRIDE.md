# Bronco-Pilot: FrogPilot with BluePilot Steering Override

Bronco-Pilot is a custom fork of FrogPilot that integrates the advanced steering control override system from BluePilot.

## Overview

This project combines:
- **FrogPilot**: The base open-source driving assistance platform with enhanced features
- **BluePilot Steering Override**: Advanced steering parameter override and control system

## Key Features

### Integrated Steering Override
- **Torque Parameter Overrides**: Allows runtime adjustment of torque parameters (latAccelFactor, friction)
- **Extended Lateral Control**: Neural network-enhanced lateral control capabilities
- **Parameter Tuning**: Dynamic adjustment of steering parameters without code modifications

## Steering Override Installation

The steering override system is located in:
```
sunnypilot/selfdrive/controls/lib/
├── latcontrol_torque_ext.py
├── latcontrol_torque_ext_override.py
└── nnlc/
```

The override is automatically integrated into the torque control system if available.

## Modified Files

- `selfdrive/controls/lib/latcontrol_torque.py`: Integrated steering override support

## Usage

The steering override parameters can be controlled via the openpilot params system:

### Parameter Names
- `TorqueParamsOverrideEnabled`: Enable/disable the override system
- `TorqueParamsOverrideLatAccelFactor`: Override value for lateral acceleration factor
- `TorqueParamsOverrideFriction`: Override value for friction coefficient

### Example

To enable steering override:
```bash
params set TorqueParamsOverrideEnabled True
params set TorqueParamsOverrideLatAccelFactor 1.0
params set TorqueParamsOverrideFriction 0.01
```

## Credits

- **FrogPilot**: FrogAi community
- **BluePilot**: BluePilotDev community
- **Steering Override**: Haibin Wen, sunnypilot contributors
- **Bronco-Pilot**: Custom integration by @hackerseraph

## License

This project respects the licenses of both FrogPilot and BluePilot. Please refer to their respective LICENSE files for details.

## Building

Bronco-Pilot follows the same build process as FrogPilot. See the main README.md for build instructions.
