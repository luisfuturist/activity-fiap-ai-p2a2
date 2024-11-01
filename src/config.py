import json

# region Default Config

DEFAULT_CONFIG = {
    "simulation": {
        "animalNumber": 30,
        "interval": 5,
        "iterations": 100,
        "outlier": {
            "fever_trigger_pct": 0.083,
            "hypothermia_trigger_pct": 0.083,
            "min_temp": 37.5,
            "max_temp": 39.3,
            "tachycardia_trigger_pct": 0.022,
            "bradycardia_trigger_pct": 0.022,
            "min_heartrate": 60,
            "max_heartrate": 80
        }
    },
    "report": {
        "outDir": "./reports/",
        "templatePath": "./config/template.jinja2.md"
    },
    "alerts": {
        "temp_outlier_z_threshold": 3.5,
        "heartrate_outlier_z_threshold": 5.5,
        "movement_outlier_z_threshold": 1.75
    }
}

def saveDefaultConfig():
    try:
        with open("config/config.json", "x") as f:
            f.write(json.dumps(DEFAULT_CONFIG, indent=4))
    except FileExistsError:
        pass

saveDefaultConfig()

# endregion

# region Config

config = DEFAULT_CONFIG

with open("config/config.json", "r") as f:
    config = json.load(f)

# endregion

# region Values

animalNumber = config.get('simulation', {}).get('animalNumber', DEFAULT_CONFIG['simulation']['animalNumber'])
interval = config.get('simulation', {}).get('interval', DEFAULT_CONFIG['simulation']['interval'])
iterations = config.get('simulation', {}).get('iterations', DEFAULT_CONFIG['simulation']['iterations'])
reportOutDir = config.get('report', {}).get('outDir', DEFAULT_CONFIG['report']['outDir'])
templatePath = config.get('report', {}).get('templatePath', DEFAULT_CONFIG['report']['templatePath'])

fever_trigger_pct = config.get('simulation', {}).get('outlier', {}).get('fever_trigger_pct', 0.05)
hypothermia_trigger_pct = config.get('simulation', {}).get('outlier', {}).get('hypothermia_trigger_pct', 0.05)
min_temp = config.get('simulation', {}).get('outlier', {}).get('min_temp', 37.5)
max_temp = config.get('simulation', {}).get('outlier', {}).get('max_temp', 39.3)
tachycardia_trigger_pct = config.get('simulation', {}).get('outlier', {}).get('tachycardia_trigger_pct', 0.05)
bradycardia_trigger_pct = config.get('simulation', {}).get('outlier', {}).get('bradycardia_trigger_pct', 0.05)
min_heartrate = config.get('simulation', {}).get('outlier', {}).get('min_heartrate', 60)
max_heartrate = config.get('simulation', {}).get('outlier', {}).get('max_heartrate', 80)

temp_outlier_z_threshold = config.get("alerts", {}).get(
    "temp_outlier_z_threshold",
    DEFAULT_CONFIG["alerts"]["temp_outlier_z_threshold"],
)
heartrate_outlier_z_threshold = config.get("alerts", {}).get(
    "heartrate_outlier_z_threshold",
    DEFAULT_CONFIG["alerts"]["heartrate_outlier_z_threshold"],
)
movement_outlier_z_threshold = config.get("alerts", {}).get(
    "movement_outlier_z_threshold",
    DEFAULT_CONFIG["alerts"]["movement_outlier_z_threshold"],
)

# endregion
