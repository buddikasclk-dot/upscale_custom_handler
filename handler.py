import runpod
import requests
import base64
import json
import time
import subprocess

# START COMFYUI
subprocess.Popen(
    ["python", "/workspace/ComfyUI/main.py", "--listen", "0.0.0.0", "--port", "8188"]
)

# wait for ComfyUI to boot
time.sleep(10)

COMFY_URL = "http://127.0.0.1:8188"
def handler(job):
    try:
        input_data = job["input"]

        image_base64 = input_data["image"]
        upscale_factor = input_data.get("scale", 4)

        image_bytes = base64.b64decode(image_base64)

        files = {
            "image": ("input.png", image_bytes, "image/png")
        }

        upload = requests.post(f"{COMFY_URL}/upload/image", files=files)
        filename = upload.json()["name"]

        with open("Upscale_4x.json") as f:
            workflow = json.load(f)

        workflow["1"]["inputs"]["image"] = filename

        prompt = requests.post(
            f"{COMFY_URL}/prompt",
            json={"prompt": workflow}
        ).json()

        prompt_id = prompt["prompt_id"]

        while True:
            history = requests.get(
                f"{COMFY_URL}/history/{prompt_id}"
            ).json()

            if prompt_id in history:
                outputs = history[prompt_id]["outputs"]
                break

            time.sleep(0.5)

        image_node = list(outputs.keys())[0]
        image_filename = outputs[image_node]["images"][0]["filename"]

        image_data = requests.get(
            f"{COMFY_URL}/view?filename={image_filename}"
        ).content

        result_base64 = base64.b64encode(image_data).decode()

        return {
    "success": True,
    "image": output_base64,
    "version": "v1-final"
}

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


runpod.serverless.start({"handler": handler})



