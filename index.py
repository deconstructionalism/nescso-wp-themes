#!/usr/bin/env python3

import requests
import shutil
from bs4 import BeautifulSoup
import re

urls = [
  'https://wordpress.org/themes/medical-care/',
  'https://wordpress.org/themes/education-lms/',
  'https://wordpress.org/themes/consultera/',
  'https://wordpress.org/themes/versatile-business/',
  'https://wordpress.org/themes/quattuor/',
  'https://wordpress.org/themes/primer/',
  'https://wordpress.org/themes/education-business/',
  'https://wordpress.org/themes/creativ-university/',
  'https://wordpress.org/themes/materialis/',
  'https://wordpress.org/themes/blocksy/',
  'https://wordpress.org/themes/edu-axis/',
  'https://wordpress.org/themes/arilewp/',
  'https://wordpress.org/themes/mediclinic-lite/',
  'https://wordpress.org/themes/zita/',
  'https://wordpress.org/themes/rara-business/',
  'https://wordpress.org/themes/onepress/',
  'https://wordpress.org/themes/ascension/',
  'https://wordpress.org/themes/consulting/'
]

theme_sections = []

for url in urls:
    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')
    full_image_url = soup.select('picture > img')[0]['src']
    image_url = ''

    if '.jpg' in full_image_url:
        image_url = full_image_url.split('.jpg')[0] + '.jpg'

    if '.png' in full_image_url:
        image_url = full_image_url.split('.png')[0] + '.png'

    file_type = image_url.split('.')[-1]
    image_res = requests.get(image_url, stream=True)
    theme_name = url.split('/')[-2]
    image_save_path = 'images/{}.{}'.format(theme_name, file_type)

    with open(image_save_path, 'wb') as out_file:
        image_res.raw.decode_content = True
        shutil.copyfileobj(image_res.raw, out_file)

    display_theme_name = ' '.join([word.capitalize() for word in theme_name.split('-')])
    image_path = 'images/{}.{}'.format(theme_name, file_type)

    theme_sections.append('''
    <section>
      <h1><a href={} target="_blank">{}</a></h1>
      <a href={} target="_blank"><img src="{}" /></a>
    </section>
    '''.format(url, display_theme_name, url, image_path))

style = '''
<style>
  body {
    background: black;
    font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  }

  main {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  img {
    width: 100%;
  }

  h1 {
    color: white;
    font-size: 2rem;
  }

  a {
    color: white;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  a:hover {
    color: #c3c3c3;
  }

  section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 5rem;
    width: 50%;
  }
</style>
'''

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <main>
    {}
  </main>
</body>
{}
</html>
'''.format(''.join(theme_sections), style)

with open('index.html', 'w') as html_file:
    html_file.write(html)
