"""Back end for using LLM."""

from enum import StrEnum
import os
from typing import Optional

import json
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError


class OCRTextQuery(BaseModel):
    """OCR Text query model."""

    ocr_text: str


class CareFrequency(StrEnum):
    """Water frequency enum class."""

    weekly = "Weekly"
    fortnightly = "Fortnightly"
    monthly = "Monthly"


class FertiliserFrequency(StrEnum):
    """Fertiliser Frequency enum class."""

    weekly = "Weekly"
    monthly = "Monthly"
    biannual = "Bi-Annually"
    spring = "Spring"
    winter = "Winter"
    summer = "Summer"
    autumn = "Autumn"


class PlantCareModel(BaseModel):
    """Plant care model."""

    watering_frequency: Optional[CareFrequency] = None
    name: Optional[str] = ""
    fertiliser: Optional[list[FertiliserFrequency]] = None


app = FastAPI(
    title="Plant Model",
    description="Processes input text to provide watering and fertiliser frequency.",
)

MODEL_NAME = os.getenv("OLLAMA_MODEL")
OLLAMA_URL = "http://ollama:11434/api/chat"


async def invoke_ollama_model(ocr_text: str) -> PlantCareModel:
    """Invoke the ollama model with the given text."""
    print(ocr_text)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a plant care expert. You will receive text from a plant label."
                "Extract and output the following fields as JSON:\n"
                "- watering_frequency: one of ['weekly', 'monthly', 'none'] (string)\n"
                "- name: well-formatted name of the plant (string)\n"
                "- fertiliser: a list of seasons or periods (e.g. ['spring', 'autumn']) or an empty list if none\n\n"
                "Rules:\n"
                "- Look for words such as 'moist', 'watering', 'water' to select the watering_frequency.\n"
                "- Look for words such as 'fertilise', 'fertiliser', and 'spring', 'autumn', 'winter', 'weekly' to select fertiliser value(s)."
                "- If the text contains the words 'moist', 'moderate', or 'regular' (case-insensitive), set watering_frequency to 'weekly'.\n"
                "- If fertiliser instructions mention seasons such as 'spring', 'autumn', extract all of them in a list such as ['spring', 'autumn'].\n"
                "- Treat the input text as case-insensitive.\n"
                "- Respond ONLY with a valid JSON object, no extra text or explanation.\n\n"
                "Example input text:\n"
                "'Jasminum azoricum\\nWatering: Moderate water requirement\\nFertilise: Use a long-term controlled-release fertiliser in spring and autumn'\n\n"
                " The example input text has the words 'Watering' and 'Moderate' so the frequency is weekly."
                "The example input text has the words 'fertiliser', 'spring and autumn' so the fertiliser is ['spring', 'autumn']\n"
                "Expected JSON output:\n"
                '{"watering_frequency": "weekly", "name": "Jasminum azoricum", "fertiliser": ["spring", "autumn"]}\n\n'
                "Now extract the information from the following text:\n"
            ),
        },
        {"role": "user", "content": ocr_text},
    ]

    async with httpx.AsyncClient(timeout=httpx.Timeout(60)) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False,
                "format": PlantCareModel.model_json_schema(),
            },
        )
        response.raise_for_status()
        content = response.json()["message"]["content"]
        print(content)
        try:
            return PlantCareModel.model_validate_json(content)
        except ValidationError as e:
            raise ValueError(
                f"Failed to parse LLM output: {e}\n\nResponse content: {content}"
            )


# used gemma3 which seemed to work okay
@app.post("/extract", response_model=PlantCareModel)
async def extract(ocr_text: OCRTextQuery) -> PlantCareModel:
    """Extract the plant care info"""
    # Handle bad responses and exceptions
    json_text = json.dumps(ocr_text.ocr_text, indent=2)
    try:
        result = await invoke_ollama_model(json_text)
        if not result.watering_frequency:
            raise HTTPException(
                status_code=400, detail={"error": "Failed to interpret label."}
            )
        return result
    except (ValueError, httpx.HTTPStatusError) as e:
        raise HTTPException(
            status_code=400, detail={"error": f"Failed to parse model response{e}"}
        )
