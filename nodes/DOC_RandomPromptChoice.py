import datetime
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
    CATEGORY = "DOC"
    DISPLAY_NAME = "Random Prompt Choice"

    def choose_random_prompt(self, **kwargs):
        prompts = [v for v in kwargs.values() if v.strip()]
        if not prompts:
            return ("",)
        sysrand = random.SystemRandom()
        sysrand.seed(datetime.datetime.now().timestamp()) 
        choice = sysrand.choice(prompts)
        return (choice,)
