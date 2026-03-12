import runpod
import traceback

def handler(job):
    try:
        print("=== JOB RECEIVED ===")
        print(job)

        job_input = job.get("input", {})
        print("=== INPUT ===")
        print(job_input)

        if "image" not in job_input:
            return {
                "success": False,
                "error": "Missing 'image' in input",
                "received_input": job_input
            }

        image_data = job_input["image"]
        scale = job_input.get("scale", "4x")

        print("=== IMAGE FIELD FOUND ===")
        print(f"scale={scale}")
        print(f"image type={type(image_data)}")

        return {
            "success": True,
            "message": "Handler received image successfully",
            "scale": scale
        }

    except Exception as e:
        print("=== ERROR ===")
        print(str(e))
        print(traceback.format_exc())

        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

runpod.serverless.start({"handler": handler})
