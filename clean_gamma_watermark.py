import fitz  # PyMuPDF
import sys
import os

def clean_gamma_pdf(input_pdf_path, output_pdf_path=None):
    if not os.path.exists(input_pdf_path):
        print(f"Error: File {input_pdf_path} not found.")
        return False

    if output_pdf_path is None:
        base, ext = os.path.splitext(input_pdf_path)
        output_pdf_path = f"{base}_clean{ext}"

    doc = fitz.open(input_pdf_path)
    total_cleaned = 0

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        
        # 1. Search for "Gamma" or "Made with Gamma"
        text_instances = page.search_for("Gamma")
        text_instances += page.search_for("Made with Gamma")

        # Sample background color near bottom-left corner
        # Default dark background color for Obsidian theme is (9/255, 15/255, 23/255)
        bg_color = (9/255, 15/255, 23/255)
        
        # 2. Redact / draw rectangle over the badge area
        # Gamma watermark is consistently at bottom-left: x0 ~ 15-40, y0 ~ page.rect.height - 45 to height - 15
        rect_badge = fitz.Rect(10, page.rect.height - 50, 160, page.rect.height - 10)
        page.draw_rect(rect_badge, color=bg_color, fill=bg_color)

        # Also cover any found text instances for "Gamma"
        for inst in text_instances:
            expanded = fitz.Rect(inst.x0 - 5, inst.y0 - 5, inst.x1 + 5, inst.y1 + 5)
            page.draw_rect(expanded, color=bg_color, fill=bg_color)
            total_cleaned += 1

        # 3. Strip all hyperlinks referencing gamma.app
        links = page.get_links()
        for link in links:
            if "uri" in link and "gamma" in link["uri"].lower():
                page.delete_link(link)

        # 4. Remove /Annots references at the low level
        page_obj = page.xref
        doc.xref_set_key(page_obj, "Annots", "null")

    doc.save(output_pdf_path, garbage=4, deflate=True)
    doc.close()
    print(f"Cleaned PDF saved successfully to: {output_pdf_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inp = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else None
        clean_gamma_pdf(inp, out)
    else:
        print("Usage: python clean_gamma_watermark.py <input.pdf> [output.pdf]")
