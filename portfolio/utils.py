from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.replace(u'\ufeff', '').encode("latin-1")), result)
    subject, from_email, to = 'hello', 'adapanaveena2526@gmail.com', 'adapanaveena2526@gmail.com'
    text_content = 'This is an important message.'
    # html_content = html_message = render_to_string('portfolio/Pdf.html', {'context': 'values'})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach("customer_portfolio", result.getvalue(),"application/pdf")
    msg.send()
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
