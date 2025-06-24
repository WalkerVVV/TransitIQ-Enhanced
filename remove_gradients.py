import re

# Read the dashboard_main.py file
with open('dashboard_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all .background_gradient() calls
# Pattern matches .background_gradient(...) with any parameters
pattern = r'\.background_gradient\([^)]*\)'
content = re.sub(pattern, '', content)

# Write the modified version
with open('dashboard_main_no_gradient.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Created dashboard_main_no_gradient.py without gradient styling")
print("This removes the matplotlib dependency")
