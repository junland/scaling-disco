import jinja2
import requests 

repo_url = 'https://api.github.com/repos/microsoft/app-store-badge/properties/values'

# Load the README file.
with open('README.md', 'r') as f:
    readme = f.read()

# Insert the properties into the README file inbetween <!-- BADGE_START --> and <!-- BADGE_END -->
start = readme.find('<!-- BADGE_START -->')
end = readme.find('<!-- BADGE_END -->')

# Get the properties from the repo.
response = requests.get(repo_url)

if response.status_code != 200:
    raise Exception(f'Failed to get properties from {repo_url}')
else:
    response_data = response.json()

# Create a Jinja2 environment
environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))

# Load the template
template = environment.get_template('badges_markdown.jinja')

# Render the template with the data
badge_markdown = template.render(properties=response_data)

# Output the rendered template
#print(badge_markdown)

# Insert the rendered template into the README file but do not overwrite the delimiters
readme = readme[:start + len('<!-- BADGE_START -->')] + "\n" + badge_markdown + "\n" + readme[end:]

print("=======================")

print(readme)
