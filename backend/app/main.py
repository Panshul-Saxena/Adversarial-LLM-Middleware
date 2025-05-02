from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from models.llm_handler import generate_with_llm
from models.benford_checker import follows_benford_law
from models.detect_model import is_adversarial
from models.correct_model import correct_prompt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ────────────────────────────────────────────────────────────────────
class GenerateRequest(BaseModel):
    prompt: str
    middleware: bool = False


class GenerateResponse(BaseModel):
    original_prompt: str
    corrected_prompt: Optional[str]
    response: str
    adversarial_detected: bool


@app.post("/generate", response_model=GenerateResponse)
async def generate_text(req: GenerateRequest):
    prompt = req.prompt
    use_middleware = req.middleware

    if not use_middleware:
        response, _ = generate_with_llm(prompt, return_logits=False)
        return GenerateResponse(
            original_prompt=prompt,
            corrected_prompt=None,
            response=response,
            adversarial_detected=False,
        )

    if is_adversarial(prompt):
        corrected = correct_prompt(prompt)
        corrected_response, _ = generate_with_llm(corrected, return_logits=False)
        return GenerateResponse(
            original_prompt=prompt,
            corrected_prompt=corrected,
            response=corrected_response,
            adversarial_detected=True,
        )

    response, logits = generate_with_llm(prompt, return_logits=True)

    if not follows_benford_law(logits):
        return GenerateResponse(
            original_prompt=prompt,
            corrected_prompt=None,
            response="⚠️ Potential hallucination detected in model output.",
            adversarial_detected=True,
        )

    return GenerateResponse(
        original_prompt=prompt,
        corrected_prompt=None,
        response=response,
        adversarial_detected=False,
    )
