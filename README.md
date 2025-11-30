## 🌸 Forgetful Gardener 🌵

### Video Demo: https://youtu.be/N31wxFZlOcE

## Description:

If you like gardening but are terrible of remembering to water and fertilise your plants, this might be for you!

Take a photo of your newly bought potted plant care label and upload it to the app.

The app will try to extract the care label text and presents you with a calendar invite your can download to remember to take of your plants!
It will have a digital copy of the text for your plant as a handy reference.

## The technical details

Run the application locally by running the docker compose file.

The program uses FASTAPI for serving the frontend and backend.
It uses pytesseract and the google tesseract engine to extract the text. You will need to have the tesseract engine installed.

This text is sent to the gemma3:6 LLM model pulled with ollama to run locally. The LLM deciphers the text and produces a response in regards to the watering and fertiliser frequency.
The frontend uses this information to appropriately setup a calendar invite for you.

If you fail to get a result, make sure you get a clear view of the plant care label text with good contrast and clear background and try again!

The first time the docker compose is run, it will need to pull this model before you can use it.
Once up and running, simply navigate to localhost:8000 to see the application landing page!

Enjoy!

### The nitty gritty

This project's repository has been divided into 3 main sections: the backend, the frontend and an llm runner. A docker compose file brings together the three elements to create the forgetful-garderner.

- llm_runner

  This folder contains a Dockerfile and a shell command to pull the gemma3 ollama model that is used to for interpreting the plant care label text into watering and fertiliser instructions.
  I experimented with different types of LLM models to determine the best one, and gemma3 performed the best based on its size and quality of output.

- backend

  This folder contains a Dockerfile and a fastapi source code to serve up the ollama model that was pulled in the llm_runner. The main.py script holds the code for providing an endpoint for the front end to send the request to the ollama model. This function then invokes the ollama model.
  There were two main challenges in testing this, I had to experiment with the system prompt instructions to the ollama model so that it would correctly give me the json response that I could pass to my frontend.
  I also debated using Flask or FastAPI. I ended up chosing the FastAPI approach as it allowed me to do async requests, so that in the future I could send multiple requests if I wanted to support multi image requests.

- frontend

  This folder contains a Dockerfile for setting up the frontend, the source code for serving up the frontend html using Jinja templating, and the html templates that make up the frontend. It also holds the image processing code that uses pytesseract engine to extract the text from the images.

The processing_labels folder holds the image processing code, and was extensively tested with some test images to refine the methods used to process the image. I used the OpenCV library to pre-process the image before passing it to the pytesseract functions to do the extraction. The main openCV functions used are described image_utils.py, and the extraction of text is described in image_reader.py. The image_processor.py and garden_label_processor.py provides the higher level API used by the FastAPI frontend code.

The main.py sets up the FastAPI and Jinja templates to serve up the frontend. The application accepts an image file in byte format, and passes it to the backend. Once a response is received, it setups a calendar invite html div to return to the jinja index.html.

I used htmx for setting up the form required for uploading files, and receiving a response from the frontend application. I used htmx as it minimised the amount of Javascript I would need, and I avoided the need to use a library like React for a single page application. Using React felt a bit overkill for this project, and htmx fit in quite nicely.

Finally, the docker compose file has been written to spin up the 3 dockerfiles as services. Once spun up, the front end application can be viewed on localhost.
