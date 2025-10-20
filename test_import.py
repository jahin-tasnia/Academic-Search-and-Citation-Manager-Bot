import traceback

try:
    import agent

    print("Imported agent successfully")
except Exception:
    traceback.print_exc()
