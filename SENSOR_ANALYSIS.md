# Sensor Analysis: Missing & Potentially Useless Sensors

## Analysis Date: October 27, 2025
## Integration Version: 1.2.1

---

## 🔍 Discovery Findings

After analyzing the actual API structure (`discover_test.py`) vs our sensor definitions, here's what we found:

### API Structure
The actual HydroLink API returns data as:
```json
{
  "data": [
    {
      "id": "device-id",
      "nickname": "Water Softener",
      "properties": {
        "salt_level_tenths": {
          "value": 750,
          "updated_at": "2025-10-27T12:00:00Z"
        }
      }
    }
  ]
}
```

All sensors read from the **flat `properties` dict**, not nested structures.

---

## ❌ Sensors Currently Missing (Could Be Added)

These appear in the discovery script but are NOT currently implemented as sensors:

### 1. **Water Counter** 
- **API Key**: `water_counter_gals`
- **Description**: Lifetime water meter reading (different from `total_outlet_water_gals`)
- **Use Case**: Alternative total water measurement
- **Priority**: ⭐ LOW (redundant with `total_outlet_water_gals`)

### 2. **Salt Efficiency**
- **API Key**: `salt_effic_grains_per_lb`
- **Description**: Grains of hardness removed per pound of salt used
- **Use Case**: Salt efficiency monitoring, cost optimization
- **Priority**: ⭐⭐ MEDIUM (useful for efficiency tracking)
- **Unit**: grains/lb

### 3. **Salt Type**
- **API Key**: `salt_type_enum`
- **Description**: Type of salt being used (enumerated value)
- **Use Case**: Informational - which salt type is configured
- **Priority**: ⭐ LOW (static config value)
- **Values**: Likely 0=NaCl (sodium chloride), 1=KCl (potassium chloride)

### 4. **Service Active**
- **API Key**: `service_active`
- **Description**: Whether professional service mode is active
- **Use Case**: Indicates if system is in service/maintenance mode
- **Priority**: ⭐⭐ MEDIUM (useful for status tracking)

### 5. **Error Code** (raw value)
- **API Key**: `error_code`
- **Description**: Raw numeric error code (we only have `error_code_alert`)
- **Use Case**: Detailed error diagnostics
- **Priority**: ⭐⭐ MEDIUM (currently only have alert, not actual code)

### 6. **Time Lost Events**
- **API Key**: `time_lost_events`
- **Description**: Number of times clock/time was lost (power outages where time wasn't restored)
- **Use Case**: Track power quality issues
- **Priority**: ⭐ LOW (redundant with `power_outage_count`)

### 7. **Regen Time Seconds** (total, not remaining)
- **API Key**: `regen_time_secs`
- **Description**: Total regeneration cycle time (configuration)
- **Use Case**: Know how long a full regen cycle takes
- **Priority**: ⭐ LOW (static config, we have `regen_time_rem_secs` for remaining time)

### 8. **Software Versions**
- **API Keys**: 
  - `base_software_version`
  - `esp_software_part_number`
  - `model_display_code`
- **Description**: Firmware/software version information
- **Use Case**: Diagnostic, firmware update tracking
- **Priority**: ⭐ LOW (static diagnostic info)

---

## ⚠️ Potentially Problematic Sensors

These sensors are defined but may have issues:

### 1. **System Error**
- **Defined**: ✅ Yes (`system_error`)
- **Issue**: NOT in API data or discovery script
- **Status**: ⚠️ May never have a value
- **Recommendation**: Verify this key exists in real API responses

### 2. **Vacation Mode**
- **Defined**: ✅ Yes (`vacation_mode`)
- **Issue**: NOT in API data or discovery script  
- **Status**: ⚠️ May never have a value
- **Recommendation**: Verify this key exists in real API responses

### 3. **App Active**
- **Defined**: ✅ Yes (`app_active`)
- **Issue**: NOT in API data or discovery script
- **Status**: ⚠️ May never have a value
- **Recommendation**: Verify this key exists in real API responses

### 4. **Current Time Seconds**
- **Defined**: ✅ Yes (`current_time_secs`)
- **Issue**: NOT in API data or discovery script
- **Status**: ⚠️ May never have a value, or may be device clock
- **Recommendation**: Verify this provides useful information

---

## ✅ Sensors That Are Correctly Implemented

These sensors match the API and are working as expected:

### Core Sensors (37 total)
All sensors in `DEFAULT_ENABLED_SENSORS` appear to be correctly mapped to API properties:

- ✅ Water flow and usage metrics (6 sensors)
- ✅ Salt management (4 sensors)  
- ✅ System performance (6 sensors)
- ✅ Regeneration status (5 sensors)
- ✅ Alerts (6 sensors)
- ✅ Connection/signal (2 sensors)
- ✅ System stats (3 sensors)
- ✅ Basic info (5 sensors)

---

## 🔧 Recommendations

### Priority 1: Add Useful Missing Sensors

```python
# Add to sensor.py SENSOR_DESCRIPTIONS:

"salt_effic_grains_per_lb": {
    "name": "Salt Efficiency",
    "unit": "grains/lb",
    "device_class": None,
    "state_class": SensorStateClass.MEASUREMENT,
    "icon": "mdi:leaf",
    "category": "SALT",
},
"error_code": {
    "name": "Error Code",
    "unit": None,
    "device_class": None,
    "state_class": None,
    "icon": "mdi:alert-circle-outline",
    "category": "ALERTS",
},
"service_active": {
    "name": "Service Mode Active",
    "unit": None,
    "device_class": None,
    "state_class": None,
    "icon": "mdi:account-wrench",
    "category": "SYSTEM",
},
```

### Priority 2: Verify Problematic Sensors

Run discovery tool with real credentials to check if these exist:
- `system_error`
- `vacation_mode`  
- `app_active`
- `current_time_secs`

If they don't exist in real API responses, consider:
1. Disabling by default (`entity_registry_enabled_default = False`)
2. Removing entirely if confirmed unavailable
3. Adding comment explaining why they exist if they're model-specific

### Priority 3: Document Model Differences

Create a sensor compatibility matrix showing which sensors are available on which models:
- Entry-level models: Basic sensors only
- Mid-tier models: Most sensors
- Premium models: All sensors including leak detector

---

## 📊 Sensor Value Accuracy Issues

### Confirmed Issue: `avg_salt_per_regen_lbs`

In `discover_test.py` line 132:
```python
elif key == "avg_salt_per_regen_lbs":
    result["maintenance"]["salt"]["avg_per_regen"] = {"value": value / 1000, "updated": updated}
```

**The API value is divided by 1000, not 10!**

This suggests the API returns salt per regen in **milligrams or different units**, requiring division by 1000, not just by 10 for tenths.

**Our sensor.py currently**:
```python
# Only divides _tenths fields by 10
if self._property_name.endswith("_tenths"):
    return value / 10
```

**Issue**: `avg_salt_per_regen_lbs` does NOT end in `_tenths`, so it's **NOT being converted**.

**Impact**: 
- If API returns `6000` meaning `6 lbs`, we're displaying `6000 lbs` ❌
- Should display `6 lbs` ✅

### Solution Needed

Need special handling for `avg_salt_per_regen_lbs`:

```python
@property
def native_value(self):
    """Return the state of the sensor."""
    for device in self.coordinator.data:
        if device["id"] == self._device_id:
            value = device["properties"][self._property_name].get("value")
            
            if value == "unknown":
                # Handle unknown values for numeric sensors
                if self.device_class in [...]:
                    return None
            
            # Convert values that are provided in tenths
            if self._property_name.endswith("_tenths") and isinstance(value, (int, float)):
                return value / 10
            
            # Special case: salt per regen is in different units
            if self._property_name == "avg_salt_per_regen_lbs" and isinstance(value, (int, float)):
                return value / 1000  # API provides in milligrams or similar
                
            return value
    return None
```

---

## 📋 Action Items

### Immediate (Critical)
1. ✅ Fix `avg_salt_per_regen_lbs` conversion (divide by 1000, not left as-is)
2. ⚠️ Test with real device data to confirm the issue
3. ⚠️ Update SENSOR_VERIFICATION.md with this finding

### Short-term (Enhancement)
1. Add `salt_effic_grains_per_lb` sensor (useful efficiency metric)
2. Add `error_code` sensor (currently only have alert, not the actual code)
3. Add `service_active` sensor
4. Verify problematic sensors with real device

### Long-term (Nice-to-have)
1. Add software version sensors (diagnostic use)
2. Add salt type sensor (informational)
3. Create sensor compatibility matrix by model
4. Consider adding entity descriptions explaining what each sensor measures

---

## 🧪 Testing Checklist

Before next release:
- [ ] Run discovery tool with real device
- [ ] Verify `avg_salt_per_regen_lbs` actual value range
- [ ] Check if `system_error`, `vacation_mode`, `app_active`, `current_time_secs` exist
- [ ] Test `salt_effic_grains_per_lb` if adding
- [ ] Confirm `error_code` provides useful diagnostic info
- [ ] Document which sensors are model-specific

---

**Document Version**: 1.0  
**Last Updated**: October 27, 2025  
**Status**: Findings pending real device verification
