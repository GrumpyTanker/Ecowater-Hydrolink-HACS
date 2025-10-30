## 🔧 Critical Fixes

### Sensor Scaling Issues Resolved
This release fixes critical sensor scaling issues that were causing incorrect readings:

1. **Capacity Remaining** - Fixed 10x too high (was showing 850% instead of 85%)
2. **Salt Usage** - Fixed 1000x too high (was showing 667 lbs instead of 0.667 lbs)
3. **Temperature & Iron Levels** - Fixed tenths conversion for mid-name `_tenths` properties

## ✨ New Features

### Complete Sensor Discovery
- **Automatic Discovery**: All 45+ HydroLink API properties now automatically exposed as sensors
- **No Manual Configuration**: Sensors created automatically on integration setup
- **Individual Control**: Enable/disable any sensor through Home Assistant UI
- **Discovery Logging**: INFO-level logs show all available properties on startup

### 15 New Sensors Added
- **Water Quality**: `iron_level_tenths_ppm`, `tlc_avg_temp_tenths_c`
- **Salt Metrics**: `salt_effic_grains_per_lb`, `salt_type_enum`
- **System Info**: `water_counter_gals`, `error_code`, `service_active`, `time_lost_events`
- **Device Details**: `product_serial_number`, `location`, `system_type`, `model_display_code`
- **Software**: `base_software_version`, `esp_software_part_number`
- **Configuration**: `regen_time_secs`

## 📚 Documentation

- New `SENSOR_DISCOVERY.md` - Complete sensor management guide
- Updated `SENSORS.md` - Detailed conversion tables
- Updated `README.md` - Sensor management instructions
- Updated `CHANGELOG.md` - Full version history

## 🧪 Testing

- 38 tests passing
- Pylint score: 10/10
- Test coverage: 63.59%

## 📦 Installation

Update through HACS or manually to get these critical fixes.

**Merged PR**: #6
