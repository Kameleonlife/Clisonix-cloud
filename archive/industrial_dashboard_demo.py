# shim module so imports like `import industrial_dashboard_demo` succeed
# It forwards to the actual module under apps.api
try:
    from apps.api.industrial_dashboard_demo import router
except Exception:
    # best-effort fallback: try relative import
    try:
        from apps.api import industrial_dashboard_demo
        router = industrial_dashboard_demo.router
    except Exception:
        # leave router undefined (main will handle import errors)
        router = None
