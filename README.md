# Scripts
A repo to log all my general scripts for making my work more productive.

## List of useable scripts for full projects
- Slide Generation

# Slide Generation Script

This repository contains a script for automating the process of generating slides for presentations.

## Overview

The slide generation script uses the python-pptx library to create PowerPoint presentations. It also uses the OpenAI API to generate content for the slides based on a given script.

## How It Works

1. The script reads an input text file where each paragraph represents the notes for a single slide.
2. For each paragraph, the script makes an API call to OpenAI, which returns a title and bullet points for the slide.
3. The script then creates a new slide in the PowerPoint presentation, sets the title and adds the bullet points.
4. This process is repeated for each paragraph in the input text file.
5. Finally, the script saves the PowerPoint presentation to a specified location.

## Usage

To use the slide generation script, follow these steps:

1. Install the required Python libraries with `pip install -r requirements.txt`.
2. Set your OpenAI API key in the script.
3. Run the script with `python run.py`.
4. The PowerPoint presentation will be saved to the same location as the script.

## Future Improvements

Future versions of the script will include the ability to customize the design of the slides and to include images and other media.
