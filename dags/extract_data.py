from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import re
from airflow.models import Variable

url = Variable.get('WEB_URL')

res = requests.get(url)
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, 'html.parser')

galleries = soup.find_all("div", attrs={"id" : "gallery-0"})
lightboxes = galleries[0].find_all('div', attrs={'class': 'lightbox-caption'})

url_name = []
character_name = []
revealed_date = []
image = []
origin = []
height = []
weight = []
age = []
gender = []

def extract_data():
  '''The function extract_data is used to extract data from a source.
  
  '''
  # scraping data from web
  for lightbox in lightboxes:

    # find url link
    link = lightbox.find('a', href=True)['href']
    url_name.append(link)

    # find name
    name = lightbox.select('a[href]')
    name = name[0].text
    character_name.append(name.title())

    # find date reveal
    revealed = lightbox.get_text("|", strip=True)
    revealed = revealed.split('|')[-1]
    revealed = revealed.split(' ')[1::]
    revealed = ' '.join(revealed).rstrip('.')
    parsed_date = datetime.strptime(revealed, "%B %d, %Y").date()
    revealed_date.append(parsed_date)

  # scraping data detail such as img, age, gender
  for detail in url_name:
    url = Variable.get('SUBWEB_URL') + f'{detail}'
    res = requests.get(url)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, 'html.parser')

    # find image link
    img_link = soup.find("a", attrs={"class": "image-thumbnail"}, href=True)['href']
    image.append(img_link)

    # find region
    region = soup \
              .find("div", attrs={"data-source" : "origin"}) \
              .find("div", attrs={"class": "pi-data-value"}) \
              .text.strip()
    pattern = re.compile(r'\b([A-Za-z\s]+)\b')
    new_region = pattern.findall(region)
    origin.append(new_region[0])

    # find height
    try:
      height_element = soup \
                        .find("div", attrs={"data-source": "height"}) \
                        .find("div", attrs={"class": "pi-data-value"})
      if height_element:
        h = height_element \
              .text.strip()
              
        if 'Unknown' in h or 'Infinite' in h:
          max_height = None
        else:
          pattern = re.compile(r'(\d+)\s*cm')
          heights = pattern.findall(h)

          max_height = max(map(int, heights))
        height.append(max_height)

      else:
        max_height = None
        height.append(max_height)

    except AttributeError:
      max_height = None
      height.append(max_height)

    # find weight
    try:
      weight_element = soup \
                        .find("div", attrs={"data-source": "weight"}) \
                        .find("div", attrs={"class": "pi-data-value"})

      if weight_element:
        w = weight_element \
              .text.strip()
        if 'Unknown' in w or 'Infinite' in w:
          max_weight = None
        else:
          pattern = re.compile(r'(\d+)\s*kg')
          weights = pattern.findall(w)
          max_weight = max(map(int, weights))
        weight.append(max_weight)
      else:
        max_weight = None
        weight.append(max_weight)

    except AttributeError:
      max_weight = None
      weight.append(max_weight)

    # find age
    try:
      age_element = soup \
                        .find("div", attrs={"data-source": "age"}) \
                        .find("div", attrs={"class": "pi-data-value"})

      if age_element:
        a = age_element \
              .text.strip() 
        if 'Unknown' in a or 'Infinite' in a:
          max_age = None

        else:
          pattern = re.compile(r'(\d+)')
          ages = pattern.findall(a)
          max_age = max(map(int, ages))
        age.append(max_age)

      else:
        max_age = None
        age.append(max_age)

    except AttributeError:
      max_age = None
      age.append(max_age)

    # find gender
    try:
      gender_element = soup \
                        .find("div", attrs={"data-source": "gender"}) \
                        .find("div", attrs={"class": "pi-data-value"})

      if gender_element:
        g = gender_element \
              .text.strip()
        pattern = re.compile(r'[A-Za-z]+')
        sex = pattern.search(g).group()
        gender.append(sex)

    except AttributeError:
      sex = None
      gender.append(sex)

  df = pd.DataFrame({
      'full_name': character_name,
      'gender': gender,
      'age': age,
      'height(cm)': height,
      'weight(kg)': weight,
      'region' : origin,
      'image_link' : image,
      'revealed_date': revealed_date,
  })

  # Reset the index starting from 1
  df.index = df.index + 1

  # Rename the index column to 'id'
  df.index.name = 'id'

  return df