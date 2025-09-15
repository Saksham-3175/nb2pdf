from pathlib import Path
from playwright.sync_api import sync_playwright


def find_html_file(notebook_dir: Path) -> Path:
    """Find the .html file in the notebook folder."""
    html_files = list(notebook_dir.glob("*.html")) 

    if not html_files:
        raise FileNotFoundError("No HTML files found in the notebook folder.")
    
    return html_files[0] 


def open_html_in_browser(page, html_path: Path):
    """Load the html file in the headless browser."""
    page.goto(f"file://{html_path.resolve()}")


def convert_to_pdf(page, pdf_path: Path):
    """Render the html page as pdf."""
    page.emulate_media(media="screen")
    page.pdf(path=str(pdf_path), format="A4", print_background=True)

def main():
    
    notebooks_dir = Path("notebooks")
    pdf_dir = Path("pdf")
    pdf_dir.mkdir(exist_ok=True) 

    html_path = find_html_file(notebooks_dir)
    pdf_path = pdf_dir / (html_path.stem + ".pdf") 

    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        open_html_in_browser(page, html_path)
        convert_to_pdf(page, pdf_path)

        browser.close()
    
    print(f"Converted {html_path.name} -> {pdf_path.name}")

if __name__ == "__main__":
    main()
