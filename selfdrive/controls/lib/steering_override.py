"""
Steering Parameter Override System for Bronco-Pilot

This module provides safe runtime override of steering control parameters.
It's designed to be minimal and safe for vehicle control systems.

Based on steering override concepts from BluePilot, simplified for FrogPilot compatibility.
"""

from openpilot.common.params import Params

try:
  import logging
  logger = logging.getLogger(__name__)
except:
  logger = None


class SteeringOverride:
  """
  Safe steering parameter override system.
  
  This allows runtime adjustment of torque control parameters without code changes.
  The override only applies if explicitly enabled and updates check occurs every ~3 seconds.
  """
  
  OVERRIDE_CHECK_FRAMES = 300  # ~3 seconds at 100 Hz
  
  def __init__(self):
    """Initialize the steering override system."""
    try:
      self.params = Params()
    except Exception as e:
      if logger:
        logger.error(f"Failed to initialize Params: {e}")
      self.params = None
    
    self.frame = 0
    self.override_enabled = False
    self._last_check_frame = -self.OVERRIDE_CHECK_FRAMES  # Force immediate check
  
  def _log(self, message: str, level: str = "info"):
    """Safely log messages."""
    if logger:
      getattr(logger, level)(message)
  
  def update_override(self, torque_params) -> bool:
    """
    Update torque parameters from override if enabled.
    
    Returns True if override was applied, False otherwise.
    
    SAFETY: This method is designed to be called every frame but only actually
    reads the parameters every ~3 seconds to minimize CPU overhead.
    """
    if self.params is None:
      return False
    
    self.frame += 1
    
    # Check for override update every OVERRIDE_CHECK_FRAMES frames
    if (self.frame - self._last_check_frame) >= self.OVERRIDE_CHECK_FRAMES:
      self._last_check_frame = self.frame
      
      try:
        # Check if override system is enabled
        self.override_enabled = self.params.get_bool("SteeringOverrideEnabled")
        
        if not self.override_enabled:
          return False
        
        # Safely get override parameters
        try:
          override_lat_accel_factor = self.params.get("SteeringOverrideLatAccelFactor")
          if override_lat_accel_factor is not None:
            torque_params.latAccelFactor = float(override_lat_accel_factor)
        except Exception as e:
          self._log(f"Failed to read SteeringOverrideLatAccelFactor: {e}", "warning")
        
        try:
          override_friction = self.params.get("SteeringOverrideFriction")
          if override_friction is not None:
            torque_params.friction = float(override_friction)
        except Exception as e:
          self._log(f"Failed to read SteeringOverrideFriction: {e}", "warning")
        
        try:
          override_accel_offset = self.params.get("SteeringOverrideLatAccelOffset")
          if override_accel_offset is not None:
            torque_params.latAccelOffset = float(override_accel_offset)
        except Exception as e:
          self._log(f"Failed to read SteeringOverrideLatAccelOffset: {e}", "warning")
        
        self._log("Steering override parameters updated")
        return True
        
      except Exception as e:
        self._log(f"Error in steering override update: {e}", "error")
        return False
    
    return False
