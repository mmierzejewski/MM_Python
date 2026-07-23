# 📊 BMI Calculator - Advanced

Advanced BMI (Body Mass Index) calculator with health recommendations, gender awareness, and result export.

## ✨ Features

- 📏 **Accurate BMI calculation** - formula: weight(kg) / (height(m))²
- 👥 **Gender awareness** - different healthy ranges for men and women
- 🎯 **Precise recommendations** - calculation of the target weight
- 🔄 **Multiple calculations** - possibility to perform several measurements in one session
- 💾 **Export to file** - save results with a timestamp
- 📝 **Logging** - session tracking in a log file
- 🛡️ **Error handling** - full validation and error handling
- 🌈 **Friendly UI** - emoji, colors, readable messages

## 📋 BMI Categories (according to WHO)

| BMI Range | Category | Status |
| --- | --- | --- |
| < 16.0 | Starvation | 🚨 Critical |
| 16.0 - 17.0 | Severe underweight | ⚠️ High risk |
| 17.0 - 18.5 | Underweight | ⚠️ Medium risk |
| 18.5 - 25.0 | Normal weight | ✅ Healthy |
| 25.0 - 30.0 | Overweight | ⚠️ Medium risk |
| 30.0 - 35.0 | Obesity class I | 🚨 High risk |
| 35.0 - 40.0 | Obesity class II | 🚨 Critical |
| ≥ 40.0 | Extreme obesity class III | 🔴 Very critical |

## 🎯 Healthy ranges by gender

- **Men**: BMI 20.0 - 25.0
- **Women**: BMI 19.0 - 24.0
- **Other/General**: BMI 18.5 - 24.99

## 💻 Usage

### Basic run

```bash
python BMI.py
```

### Interactive flow

1. **Enter your name** (optional)
2. **Choose gender** (1-Male, 2-Female, 3-Other)
3. **Weight** in kilograms
4. **Height** in centimeters
5. **Export** results (optional)
6. **Calculate again** or finish

### Sample session

```text
📊 BMI CALCULATOR - ADVANCED

👤 What's your name? Jan

🤝 Nice to meet you, Jan!

👤 Gender (affects the healthy range):
   1. Male
   2. Female
   3. Other / Prefer not to say
   Choice [3]: 1

⚖️  Enter your weight (kg): 75
📏 Enter your height (cm): 175

==================================================
✅  Your BMI: 24.49
   Category: normal weight
   Healthy range: 20 - 25
==================================================

🎉 Congratulations, Jan! Your weight is normal!
   You are in the healthy range 20 - 25.
   Keep up a healthy lifestyle! 💪

💾 Save the result to a file? (Y/N) [N]: Y
💾 Result saved to file: bmi_wynik_20251212_143022.txt

🔄 Calculate again? (Y/N) [N]: N

👋 Thank you for using the BMI calculator!
   Take care of your health! 💚
```

## 📁 Generated files

### Log file: `bmi_calculator.log`

```text
2025-12-12 14:30:15 - INFO - BMI calculator started
2025-12-12 14:30:22 - INFO - Calculated BMI: 24.49 for Jan (gender: male)
2025-12-12 14:30:25 - INFO - Result exported to bmi_wynik_20251212_143022.txt
2025-12-12 14:30:30 - INFO - Calculator stopped
```

### Export file: `bmi_wynik_YYYYMMDD_HHMMSS.txt`

```text
==================================================
📊 BMI CALCULATION RESULT
==================================================

Date: 2025-12-12 14:30:22
Name: Jan
Gender: male
Weight: 75.0 kg
Height: 175.0 cm

BMI: 24.49
Category: normal weight

RECOMMENDATIONS:
Congratulations, Jan! Your weight is normal!
You are in the healthy range 20 - 25.
Keep up a healthy lifestyle!

==================================================
ℹ️  Remember: BMI is only an approximate indicator.
   Consult a doctor about health matters!
==================================================
```

## 🔬 Calculations

### BMI formula

```text
BMI = weight(kg) / (height(m))²
```

### Target weight

```text
Target weight = target_BMI × (height(m))²
```

### Example

- Height: 175 cm (1.75 m)
- Weight: 85 kg
- BMI = 85 / (1.75)² = 27.76 → **Overweight**

To reach a BMI of 25 (upper healthy limit for men):

- Target weight = 25 × (1.75)² = 76.56 kg
- Weight to lose: 85 - 76.56 = **8.44 kg**

## 🆚 Version comparison

| Feature | Old version | New version |
| --- | --- | --- |
| Shebang & encoding | ❌ | ✅ |
| Type hints | ⚠️ Partial | ✅ Full |
| Gender awareness | ❌ | ✅ |
| Multiple calculations | ❌ | ✅ |
| Precise weight calculations | ❌ | ✅ |
| Export to file | ❌ | ✅ |
| Logging | ❌ | ✅ |
| Error handling | ⚠️ Basic | ✅ Complete |
| Constants vs magic numbers | ❌ | ✅ |
| Categories as dict | ❌ | ✅ |

## ⚠️ Important information

### BMI limitations

BMI is an **approximate indicator** and does not account for:

- Muscle mass (athletes may be "overweight")
- Body fat distribution
- Age (different norms for children and older adults)
- Bone structure
- Overall health condition

### When to consult a doctor?

- BMI < 18.5 or > 30
- Sudden weight change
- Health issues
- Diet/training planning
- Pregnancy

## 🔧 Requirements

```bash

# Python 3.10+

# Standard library only - no external dependencies

```

## 📖 Sources

- [WHO BMI Classification](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight)
- [CDC BMI Information](https://www.cdc.gov/healthyweight/assessing/bmi/index.html)
- [NIH BMI Calculator](https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmicalc.htm)

## 📝 Changelog

### Version 2.0 (2025-12-12)

- ✨ Added gender awareness
- ✨ Multiple calculations in one session
- ✨ Export results to file
- ✨ Logging to file
- ✨ Precise target weight calculations
- 🔧 Improved type hints
- 🔧 Refactored to use constants and Enum
- 🔧 Full error handling
- 📚 Expanded documentation

### Version 1.0

- Basic BMI calculator
- WHO categories
- Simple recommendations

## 📄 License

Free to use and modify.

---

**⚕️ Disclaimer**: This calculator is an educational tool. Always consult a doctor or dietitian about health and diet matters.
