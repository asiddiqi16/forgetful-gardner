## 🌸 Forgetful Gardner 🌵

If you like gardening but are terrible of remembering to water and fertilise your plants, this might be for you!

Take a photo of your newly bought potted plant care label and upload it to the app.

The app will try to extract the care label text and presents you with a calendar invite your can download to remember to take of your plants!
It will have a digital copy of the text for your plant as a handy reference.

## The technical details

Run the application locally by running the docker compose file.

The program uses FASTAPI for serving the frontend and backend.
It uses pytesseract and the google tesseract engine to extract the text.

This text is sent to the gemma3:6 LLM model pulled with ollama to run locally. The LLM deciphers the text and produces a response in regards to the watering and fertiliser frequency.
The frontend uses this information to appropriately setup a calendar invite for you.

If you fail to get a result, make sure you get a clear view of the plant care label text with good contrast and clear background and try again!

The first time the docker compose is run, it will need to pull this model before you can use it.
Once up and running, simply navigate to localhost:8000 to see the application landing page!

Enjoy!
