from django.http import HttpResponse

def sitemap(request):
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://{request.get_host}/</loc></url>
      <url><loc>https://{request.get_host}/accounts/login/</loc></url>
      <url><loc>https://{request.get_host}/accounts/register/</loc></url>
    </urlset>"""
    return HttpResponse(xml, content_type="application/xml")
