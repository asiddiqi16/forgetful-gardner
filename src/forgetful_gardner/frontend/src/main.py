import os
from pathlib import Path
from datetime import datetime, timedelta

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from httpx import HTTPStatusError
import html
from jinja2 import Template

import traceback
import logging

logger = logging.getLogger(__name__)

from processing_labels.garden_label_processor import (
    get_plant_care_text_from_image_bytes,
)

# I used an LLM to come up with the skeleton code for using FastAPI and JINJA template
app = FastAPI()

TEMPLATES_DIR = Path("/home/forgetful_gardner/src/templates")
app.mount(
    "/static",
    StaticFiles(directory=Path("/home/forgetful_gardner/src/static")),
    name="static",
)
templates = Jinja2Templates(directory=TEMPLATES_DIR)

GARDEN_LABEL_PROCESSOR_URL = os.environ["BACKEND_URL"]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload(file: UploadFile = File(...)):
    # Forward the file to another backend
    async with httpx.AsyncClient() as client:
        image_bytes = await file.read()
        try:
            image_text_list = get_plant_care_text_from_image_bytes(image_bytes)
            if image_text_list is None:
                raise RuntimeError(f"Could not process image: {file.filename}")
            else:
                print("Processing Image")
                logger.info("Processing Image")
                image_text = "\n".join(image_text_list)
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        GARDEN_LABEL_PROCESSOR_URL,
                        json={"ocr_text": image_text},
                        timeout=60.0,
                    )
                    response.raise_for_status()
                result = response.json()
                # Set up start date for calendar event
                start_date = get_next_wednesday().strftime("%Y-%m-%d")
                # set calendar frequency
                match result["watering_frequency"]:
                    case "Weekly":
                        calendar_recurrence = (
                            "RRULE:FREQ=WEEKLY;INTERVAL=1;WKST=MO;BYDAY=WE"
                        )
                    case "Fortnightly":
                        calendar_recurrence = (
                            "RRULE:FREQ=WEEKLY;INTERVAL=2,;WKST=MO;BYDAY=WE"
                        )
                    case "Monthly":
                        calendar_recurrence = (
                            "RRULE:FREQ=MONTHLY;INTERVAL=1,;WKST=MO;BYDAY=WE"
                        )
                    case _:
                        calendar_recurrence = (
                            "RRULE:FREQ=WEEKLY;INTERVAL=1;WKST=MO;BYDAY=WE,FR;"
                        )

                if result["fertiliser"]:
                    template_str = """
                        <div class="success container d-flex col-sm">
                            <div class="calendar-button row g-1">
                                <div class="col-md">
                                    <add-to-calendar-button
                                        name="[Reminder] Water and Fertilise your {{ result.name }} plant"
                                        startDate={{ start_date }}
                                        timeZone="currentBrowser"
                                        location="Garden"
                                        description="Fertiliser your {{ result.name }} plant as per schedule:{{', '.join(result.fertiliser)}}.<br>{{image_text}}</br>"
                                        options="'Apple','Google','iCal','Outlook.com','Yahoo'"
                                        recurrence="{{ calendar_recurrence }}"
                                        lightMode="bodyScheme"
                                        buttonStyle="date"
                                        >
                                    </add-to-calendar-button>
                                    </div>
                                <div class="col-md result-values mx-5">
                                    <ul>
                                        <li><strong> Plant Name: </strong> {{ result.name }}</li>
                                            <li> <strong>Watering Frequency: </strong> {{ result.watering_frequency }}</li>
                                            <li><strong>Fertiliser Schedule:</strong>
                                            <ul class="fertiliser">
                                                {% for item in result.fertiliser %}
                                                <li>{{ item }}</li>
                                                {% endfor %}
                                            </ul>
                                            </li>
                                    </ul>
                                </div>
                            </div>               
                        </div>
                        """
                    template = Template(template_str)
                    rendered_html = template.render(
                        result=result,
                        calendar_recurrence=calendar_recurrence,
                        start_date=start_date,
                        image_text=image_text,
                    )
                else:
                    template_str = """
                        <div class="success container d-flex col-sm">
                            <div class="calendar-button row g-1">
                                <div class="col-md">
                                    <add-to-calendar-button
                                        name="[Reminder] Water and Fertilise your {{ result.name }} plant"
                                        startDate={{ start_date }}
                                        timeZone="currentBrowser"
                                        location="Garden"
                                        description="<br>{{image_text}}</br>"
                                        options="'Apple','Google','iCal','Outlook.com','Yahoo'"
                                        recurrence="{{ calendar_recurrence }}"
                                        lightMode="bodyScheme"
                                        buttonStyle="date"
                                        >
                                    </add-to-calendar-button>
                                    </div>
                                <div class="col-md result-values mx-5">
                                    <ul>
                                        <li><strong> Plant Name: </strong> {{ result.name }}</li>
                                            <li> <strong>Watering Frequency: </strong> {{ result.watering_frequency }}</li>
                                    </ul>
                                </div>
                            </div>               
                        </div>
                        """
                    template = Template(template_str)
                    rendered_html = template.render(
                        result=result,
                        calendar_recurrence=calendar_recurrence,
                        start_date=start_date,
                        image_text=image_text,
                    )
            return HTMLResponse(rendered_html)
        except httpx.TimeoutException:
            return HTMLResponse(
                """
                <div class="error">The backend took too long to respond. Please try again later.</div>
            """
            )
        except HTTPStatusError as e:
            detail = e.response.json().get("detail", {})
            error_msg = detail.get("error", "Unknown backend error")
            return HTMLResponse(
                f"""
                <div class="error">{error_msg}</div>
            """
            )

        except Exception as e:
            print(e)
            return HTMLResponse(
                f"""
            <div class="error">{e} Try again.</div>
        """
            )


def get_next_wednesday():
    # Get the current date and time
    now = datetime.now()

    # Get the current day of the week (Monday is 0, Sunday is 6)
    current_weekday = now.weekday()

    # Calculate the number of days until the next Wednesday
    # Wednesday is represented by 2
    days_until_wednesday = (2 - current_weekday + 7) % 7

    # If today is Wednesday, and we want the *next* Wednesday, add 7 days
    if days_until_wednesday == 0:
        days_until_wednesday = 7

    # Add the calculated days to the current date
    next_wednesday = now + timedelta(days=days_until_wednesday)

    return next_wednesday
