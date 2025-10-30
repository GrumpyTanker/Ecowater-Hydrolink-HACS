# Sensor Data Verification Guide

This document explains which sensors provide live/dynamic data vs static configuration values, and how to verify sensor data accuracy.

## Data Flow Overview

### How Sensors Get Their Values

1. **API Call Flow**:
   ```
   Coordinator → API.get_data() → WebSocket Trigger → Fresh Data Fetch → Sensor Updates
   ```

2. **Update Mechanism**:
   - **Coordinator Update Interval**: Every 5 minutes (configurable in `coordinator.py`)
   - **WebSocket Trigger**: For each device, opens WebSocket to force cloud data refresh
   - **Data Source**: HydroLink cloud service (`app.hydrolinkhome.com`)
   - **Sensor Update**: Each sensor reads from `device["properties"][property_name]["value"]`

3. **Value Conversion**:
   - Values ending in `_tenths` are divided by 10 (e.g., 750 → 75%)
   - Timestamps in `_secs` are converted to datetime
   - Most other values are passed through as-is

---

## Sensor Categories by Data Type

### 🔴 Live/Dynamic Sensors (Change Frequently)

These sensors update based on actual system operation and water usage:

| Sensor | Update Frequency | Data Source |
|--------|-----------------|-------------|
| **Current Water Flow** | Real-time | Live flow sensor on device |
| **Water Used Today** | Per-use | Resets daily, accumulates throughout day |
| **Capacity Remaining** | After water use | Calculated based on usage vs capacity |
| **Salt Level** | When changed | Physical salt tank sensor |
| **Regeneration Status** | During regen | Active regeneration state machine |
| **Regeneration Time Remaining** | During regen | Countdown timer during active cycle |
| **Online Status** | Connection | Device cloud connectivity status |
| **WiFi Signal Strength** | Periodic | Device WiFi connection quality |

**Verification Method**: Monitor these over time; values should change with water usage or system events.

---

### 🟡 Semi-Dynamic Sensors (Change Periodically)

These sensors change but less frequently (daily, weekly, or based on events):

| Sensor | Update Frequency | Data Source |
|--------|-----------------|-------------|
| **Average Daily Usage** | Daily | Rolling average calculation |
| **Peak Water Flow** | When exceeded | Tracks maximum flow rate seen |
| **Days Until Salt Needed** | Daily | Calculated based on usage trends |
| **Days Since Last Regeneration** | Daily | Increments daily post-regen |
| **Total Regenerations** | Per regen | Counter increments each cycle |
| **Manual Regenerations** | User action | Counter for manual triggers |
| **Power Outage Count** | Per outage | Increments on power loss detection |
| **Low Salt Alert** | Threshold | Triggered when salt < 25% |
| **Error Code Alert** | On error | Set when system error detected |
| **Service Reminder** | Monthly | Countdown to scheduled service |

**Verification Method**: Check daily or after specific events (regen, alerts, etc.).

---

### 🟢 Static/Configuration Sensors (Rarely Change)

These sensors reflect device configuration or lifetime totals:

| Sensor | Change Type | Data Source |
|--------|-------------|-------------|
| **Model** | Never | Device hardware model |
| **Device Name** | User config | User-set nickname |
| **Operating Capacity** | Config | Programmed system capacity (grains) |
| **Water Hardness** | Config | User-configured water hardness |
| **Total Treated Water** | Lifetime | Cumulative total (monotonic increasing) |
| **Total Salt Used** | Lifetime | Cumulative total (monotonic increasing) |
| **Total Hardness Removed** | Lifetime | Cumulative total (monotonic increasing) |
| **Days in Operation** | Lifetime | Increments daily since install |

**Verification Method**: These should remain constant unless configuration changes or lifetime accumulation.

---

## API Response Structure

Based on the API implementation and example data, the actual response looks like:

```json
{
  "data": [
    {
      "id": "device-uuid",
      "nickname": "Water Softener",
      "model_description": "EWS 410",
      "properties": {
        "current_water_flow_gpm": {
          "value": 2.5,
          "updated": "2025-10-27T12:34:56Z"
        },
        "salt_level_tenths": {
          "value": 750,
          "updated": "2025-10-27T08:00:00Z"
        },
        "gallons_used_today": {
          "value": 150,
          "updated": "2025-10-27T12:34:56Z"
        }
        // ... more properties
      }
    }
  ]
}
```

### Key Observations:

1. **Each property has**:
   - `value`: The actual sensor reading
   - `updated`: Timestamp of last update (ISO 8601 format)

2. **Value Types**:
   - **Numbers**: Flow rates, volumes, percentages
   - **Strings**: Status, model, names
   - **Booleans**: Alerts, online status
   - **Unknown**: When sensor unavailable (`"unknown"`)

3. **Tenths Encoding**:
   - `salt_level_tenths`: 750 = 75.0%
   - `iron_level_tenths_ppm`: 15 = 1.5 ppm
   - Any other `_tenths` fields follow same pattern

---

## Verification Script

To verify which sensors have live data from YOUR device:

### Run Discovery Tool

```bash
# From repository root
cd discovery

# Run with your HydroLink credentials
python discover.py --email your.email@example.com --password yourpassword

# Output saved to: discovery/outputs/discovery_YYYYMMDD_HHMMSS.json
```

### Analyze Output

The discovery tool:
1. Authenticates with HydroLink API
2. Fetches all devices on your account
3. Triggers WebSocket refresh for each device
4. Saves complete API response to `outputs/` folder
5. Shows actual data structure and values from YOUR device

### What to Look For

Check the output JSON for:

✅ **Verify Live Data**:
- `current_water_flow_gpm` should be 0 when no water running, >0 when using water
- `gallons_used_today` should increase throughout the day
- `capacity_remaining_percent` should decrease as water is used

✅ **Verify Timestamps**:
- Each property has an `updated` timestamp
- Recent timestamps indicate fresh data
- Old timestamps may indicate stale/cached values

✅ **Check for Missing Sensors**:
- Not all models support all sensors
- Missing properties won't create entities
- Check if your model has leak detector, iron filter, etc.

---

## Testing Live Updates

### Test Flow Sensor

```bash
# 1. Note current flow value
# 2. Turn on a faucet
# 3. Wait 30 seconds (for coordinator update)
# 4. Check if current_water_flow_gpm increased
# 5. Turn off faucet
# 6. Wait 30 seconds
# 7. Verify flow returns to 0
```

### Test Daily Reset

```bash
# 1. Check gallons_used_today value at 11:59 PM
# 2. Wait until 12:01 AM
# 3. Verify value reset to 0 or very low
```

### Test Salt Level

```bash
# 1. Note current salt_level percentage
# 2. Add salt to reservoir (if <50%)
# 3. Wait 5-10 minutes for device to update
# 4. Check if salt_level increased
# Note: Some models only update salt level after regeneration
```

---

## Common Issues and Solutions

### Sensor Shows "Unavailable"

**Causes**:
- Device offline or disconnected from WiFi
- API authentication expired
- Sensor not supported by your device model

**Check**:
1. Verify `_internal_is_online` sensor shows `true`
2. Check WiFi signal strength sensor
3. Reload integration to refresh authentication
4. Check Home Assistant logs for API errors

### Sensor Shows "Unknown"

**Causes**:
- Device hasn't reported that metric yet
- Sensor measurement in progress
- Temporary API communication issue

**Solutions**:
- Wait 5-10 minutes for next update
- Trigger manual regeneration to force device communication
- Check if device is actively measuring (e.g., during regen)

### Value Doesn't Change

**Expected Static Values**:
- Model, device name, operating capacity never change
- Lifetime totals only increment (never decrease)
- Configuration values only change if you reconfigure device

**Unexpected Static Values**:
1. Check `updated` timestamp in raw API data
2. Verify device is online and communicating
3. Check if sensor requires specific event (e.g., water use)
4. Some sensors update once per day (salt level, averages)

### Value Seems Wrong

**Check These**:
1. **Tenths conversion**: Is value 10x too high? Check if `_tenths` suffix
2. **Units**: Verify unit matches expectation (GPM vs gal, lbs vs %)
3. **Timezone**: Check if timestamp/datetime values have timezone issues
4. **Model differences**: Different models may report differently

---

## Debug Logging

Enable debug logging to see raw API responses:

### configuration.yaml

```yaml
logger:
  default: info
  logs:
    custom_components.hydrolink: debug
    custom_components.hydrolink.api: debug
    custom_components.hydrolink.coordinator: debug
```

### What You'll See

```
DEBUG (Thread-1) [custom_components.hydrolink.api] Received WebSocket message: {...}
DEBUG (MainThread) [custom_components.hydrolink.coordinator] Fetched data from HydroLink API: [...]
DEBUG (MainThread) [custom_components.hydrolink.sensor] Sensor current_water_flow_gpm value: 2.5
```

---

## Conclusion

### Live/Real-time Sensors (High Priority)
Monitor these for automation:
- Current water flow
- Water used today  
- Capacity remaining
- Regeneration status
- Salt level
- Online status
- Low salt alert

### Informational Sensors (Medium Priority)
Track these for trends:
- Average daily usage
- Peak flow
- Days since regeneration
- WiFi signal
- Power outages

### Static/Config Sensors (Low Priority)
Set once, rarely change:
- Model, name, capacity
- Water hardness setting
- Lifetime totals

---

**Last Updated**: October 27, 2025  
**Integration Version**: 1.2.1+
