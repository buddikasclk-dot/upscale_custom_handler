import runpod

def handler(job):
    return {
        "success": True,
        "message": "Custom handler is running"
    }

runpod.serverless.start({"handler": handler})