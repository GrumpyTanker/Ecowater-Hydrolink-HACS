# Sensor Discovery Guide

## How Sensor Discovery Works

The EcoWater HydroLink integration **automatically discovers all available sensors** from your device's API. This means:

1. **All API properties are exposed** - Every property returned by the HydroLink API becomes a sensor
2. **No manual configuration needed** - Sensors are created automatically on first setup
3. **New properties are detected** - If EcoWater adds new data to the API, sensors will appear automatically after restart

## Viewing Available Sensors

### Method 1: Home Assistant UI
1. Go to **Settings** → **Devices & Services** → **HydroLink**
2. Click on your device
3. Click **Entities** tab
4. You'll see all sensors, including disabled ones

### Method 2: Check Logs
The integration logs all discovered properties at INFO level when it loads:
1. Enable logging in `configuration.yaml`:
   ```yaml
   logger:
     logs:
       custom_components.hydrolink: info
   ```
2. Restart Home Assistant
3. Check logs for a message like:
   ```
   HydroLink device 'Ecowater' has 45 properties available from API: app_active, avg_daily_use_gals, ...
   ```

## Managing Sensors

### Enable/Disable Individual Sensors
1. Go to **Settings** → **Devices & Services** → **HydroLink** → **Entities**
2. Click on any sensor
3. Use the **Enable/Disable** toggle

### Default Enabled Sensors
The following sensors are enabled by default (see `DEFAULT_ENABLED_SENSORS` in `sensor.py`):
- All water usage and flow metrics
- All salt management sensors
- All system performance sensors
- All regeneration status sensors
- All critical alerts
- WiFi/signal sensors
- System operation stats

### Which Sensors to Disable?

Consider disabling sensors that:
- **Always show the same value** (static configuration data)
- **Show zero or are not applicable** to your setup (e.g., iron filter if you don't have one)
- **Are not useful for monitoring** (internal enums, raw counters)

**Examples of sensors you might disable:**
- `app_active` - Usually always "True"
- `error_code` - Usually "0" unless there's an error
- Alert sensors - Only useful when triggered (0 most of the time)
- `iron_level_tenths_ppm` - If you don't have iron in your water
- Various `_enum` sensors - Internal state codes
- Configuration sensors like `model_display_code`, `system_type` - Static values

## Troubleshooting

### "I don't see a sensor I expect"
1. Check if it's disabled: Settings → Devices & Services → HydroLink → Entities → Show disabled entities
2. Check logs to see what properties were discovered
3. Enable debug logging to see raw API response:
   ```yaml
   logger:
     logs:
       custom_components.hydrolink: debug
   ```

### "Sensor shows wrong value"
1. Check if it needs scaling (see SENSORS.md for conversion rules)
2. File an issue with the sensor name and values you're seeing
3. Include debug logs showing the raw API value

### "Too many sensors"
This is normal! The integration exposes everything available. You can:
1. Disable sensors you don't need (Settings → Entities)
2. Use the "Filter" box in the Entities page to find specific sensors
3. Create custom dashboards with only the sensors you care about

## API Property Types

The HydroLink API provides different types of properties:

### Dynamic/Useful Sensors
- Water usage and flow rates (change frequently)
- Salt levels (change over time)
- Regeneration status (changes during regen)
- Capacity remaining (decreases with usage)
- Alert status (changes when issues occur)

### Static/Configuration Sensors
- Model information (`model_description`, `system_type`)
- Software versions (`base_software_version`)
- Serial numbers (`product_serial_number`)
- Hardness settings (`hardness_grains`)

### Semi-Static Sensors
- Days in operation (increments daily)
- Total regenerations (increments per regen)
- Total water/salt used (increases over time)

## Examples

### Good Sensors to Keep Enabled
- `salt_level_tenths` - Monitor salt levels
- `capacity_remaining_percent` - Know when regen is needed
- `gallons_used_today` - Track daily usage
- `current_water_flow_gpm` - See current usage
- `days_since_last_regen` - Regen frequency
- `low_salt_alert` - Get notified when salt is low

### Sensors You Might Disable
- `app_active` - Not useful (always True)
- `current_valve_position_enum` - Internal state code
- `depletion_alert` - Redundant with capacity remaining
- `valve_pos_switch_enum` - Internal diagnostic
- Static configuration values

## Future Enhancements

Potential improvements being considered:
- Smart filtering to auto-disable truly static sensors
- Grouping of related sensors
- Sensor templates for common monitoring dashboards
- Historical change detection (mark sensors as "static" if unchanged for N days)
