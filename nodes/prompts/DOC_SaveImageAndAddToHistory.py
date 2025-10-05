import os
import folder_paths
import json

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args
import numpy as np
       


class DOC_SaveImageAndAddToHistory:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4
        self.history_filename = "generation_history.jsonl"

    def _get_history_path(self):
        return os.path.join(self.output_dir, self.history_filename)

    def _append_history(self, entry):
        history_path = self._get_history_path()
        # Crea il file se non esiste
        with open(history_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": ("STRING", {"default": "ComfyUI", "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."}),
                "llm_prompt": ("STRING", {"default": "Drag your original prompt here...", "tooltip": "The text prompt given to the LLM to generate the final prompt."}),
                "final_prompt": ("STRING", {"default": "Drag the final prompt here...", "tooltip": "The text prompt used to generate the image."}),
                "steps": ("INT", {"default": 30, "tooltip": "The number of steps used to generate the image."}),
                "cfg": ("FLOAT", {"default": 3.5, "tooltip": "The CFG scale used to guide the image generation."}),
            },
            "hidden": {
                "prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image"
    DESCRIPTION = "Saves the input images to your ComfyUI output directory and store prompt-image mapping in a global history file."

    def save_images(self, images, filename_prefix="ComfyUI", llm_prompt=None, final_prompt=None, steps=None, cfg=None, prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            file_path = os.path.join(full_output_folder, file)
            img.save(file_path, pnginfo=metadata, compress_level=self.compress_level)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })

            # Scrivi la riga di history
            history_entry = {
                "path": os.path.abspath(file_path),
                "llm_prompt": llm_prompt,
                "final_prompt": final_prompt,
                "steps": steps,
                "cfg": cfg
            }
            self._append_history(history_entry)
            counter += 1

        return { "ui": { "images": results } }