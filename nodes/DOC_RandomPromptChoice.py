import random

class DOC_RandomPromptChoice:
    def __init__(self):
        self.type = "text"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                **{f"prompt_{i+1}": ("STRING", {"default": "", "tooltip": f"Prompt {i+1}"}) for i in range(20)}
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_prompt",)
    FUNCTION = "choose_random_prompt"
    CATEGORY = "DOC Utils"
    DISPLAY_NAME = "Random Prompt Choice"

    def choose_random_prompt(self, **kwargs):
        prompts = [v for v in kwargs.values() if v.strip()]
        if not prompts:
            return ("",)
        choice = random.choice(prompts)
        idx = prompts.index(choice) + 1
        print(f"[DOC_RandomPromptChoice] Scelta #{idx}: '{choice[:20]}'")
        return (choice,)
