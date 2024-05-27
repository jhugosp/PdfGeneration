from jinja2 import Environment, FileSystemLoader

# Load the template
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)
template = env.get_template('static/sample_banco_bogota.html')

# Data to render in the template
elements = [
    {'id': 'element1', 'content': 'This is the first element'},
    {'id': 'element2', 'content': 'This is the second element'},
    {'id': 'element3', 'content': 'This is the third element'}
]

# Render the template with the data
output = template.render(elements=elements)

# Save the rendered HTML to a file
with open('static/sample_banco_bogota.html', 'w') as f:
    f.write(output)

print("HTML file generated successfully!")
