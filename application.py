from flask import Flask, render_template, render_template_string, send_from_directory
from flask_flatpages import FlatPages, pygments_style_defs
import markdown

def my_renderer(text):
    prerendered_body = render_template_string(text)
    return markdown.markdown(prerendered_body, extensions=['codehilite', 'fenced_code'])

app = Flask(__name__)
app.config['FLATPAGES_HTML_RENDERER'] = my_renderer
pages = FlatPages(app)

@app.route('/')
def index():
    # Articles are pages with a publication date
    articles = (p for p in pages if 'published' in p.meta)
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True, key=lambda p: p.meta['published'])
    return render_template('index.html', articles=latest[:10])

@app.route('/.well-known/pki-validation/<path:filename>')
def wellKnownRoute(filename):
    print(app.root_path)
    return send_from_directory(app.root_path + '/.well-known/pki-validation/', filename, conditional=True)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'article.html')
    return render_template(template, page=page)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('xcode'), 200, {'Content-Type': 'text/css'}