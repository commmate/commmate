import os
import re
import json
import logging
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up OpenAI API key
client = OpenAI(
    organization=os.getenv('OPENAI_ORGANIZATION_ID'),
    project=os.getenv('OPENAI_PROJECT_ID')
)


# Set up YouTube Data API key
youtube_api_key = os.getenv('YOUTUBE_API_KEY')

# Set up directories
base_dir = 'training-data'
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Helper function to get video links from a YouTube channel
def get_video_links(channel_id):
    logging.debug(f'Fetching video links from channel ID: {channel_id}')
    url = f'https://www.googleapis.com/youtube/v3/search?key={youtube_api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=50'
    response = requests.get(url).json()
    video_links = ['https://www.youtube.com/watch?v=' + item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']
    logging.debug(f'Found {len(video_links)} video links')
    return video_links

# Helper function to get video details
def get_video_details(video_url):
    logging.debug(f'Fetching video details for: {video_url}')
    video_id = video_url.split('=')[-1]
    response = requests.get(f'https://www.youtube.com/watch?v={video_id}')
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('meta', {'name': 'title'})['content']
    description = soup.find('meta', {'name': 'description'})['content']
    return title, description

# Helper function to get YouTube transcript
def get_youtube_transcript(video_id):
    logging.debug(f'Fetching transcript for video ID: {video_id}')
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return " ".join([item['text'] for item in transcript])

# Helper function to call OpenAI API
def call_openai_api(prompt):
    logging.debug('Calling OpenAI API')
    system_message = [
        {"role": "system",
        "content":
            "You are youtube data orgabnier. You collect data from youtube and organized it to be stored in a pdf file. The PDFs will be used as tranning that for other GPTs. Informations as location, sailing condition, problems, fixes, anchorages, marinas, rules, safety mesures, routes, sea bottom, weather, tide, currents, and other relevant data for sailing are important. The data must be organized in a clear and objective way, with the most relevant information first. The data must be accurate and reliable, and the PDFs must be well-formatted and easy to read. The data must be organized in a clear and objective way, with the most relevant information first. The data must be accurate and reliable, and the PDFs must be well-formatted and easy to read."
        },
        {"role": "user", "content": (prompt)},
    ]    
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=system_message,
        stream=True,
    )
    # Constrói a resposta do assistente
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    return response

# Helper function to create a PDF
def create_pdf(content, file_path):
    logging.debug(f'Creating PDF at: {file_path}')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(file_path)

# Main function to process a YouTube channel
def process_youtube_channel(channel_url, channel_id):
    channel_name = re.sub(r'[^a-zA-Z0-9]', '_', channel_url.split('@')[-1])
    channel_dir = os.path.join(base_dir, channel_id)
    if not os.path.exists(channel_dir):
        os.makedirs(channel_dir)

    video_links = get_video_links(channel_id)
    for video_url in video_links:
        try:
            video_id = video_url.split('=')[-1]
            title, description = get_video_details(video_url)
            transcript = get_youtube_transcript(video_id)
            
            # Construct prompt for OpenAI
            prompt = (
                f"Title: {title}\n"
                f"Description: {description}\n"
                f"Transcript: {transcript}\n\n"
                "Organize the above information based on the most relevant sailing data for sailing."
            )
            
            organized_content = call_openai_api(prompt)
            
            file_path = os.path.join(channel_dir, f'{video_id}.pdf')
            create_pdf(organized_content, file_path)
            
        except Exception as e:
            logging.error(f'Failed to process video {video_url}: {e}', exc_info=True)

# Example usage
channel_url = 'https://www.youtube.com/@ParlayRevival'
channel_id = 'UCYrqanbSklKodK2Onpt6KgA'
process_youtube_channel(channel_url, channel_id)
