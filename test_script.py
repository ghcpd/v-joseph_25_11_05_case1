import runpy

print("=== Running README examples ===")
# In actual evaluation, agent should parse README code blocks dynamically
runpy.run_path("README.md")  # intentionally fails to simulate outdated doc behavior
