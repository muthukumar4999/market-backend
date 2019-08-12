import csv
import uuid
from io import BytesIO

import xlwt
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.response import Response
from xhtml2pdf import pisa
from django.utils.crypto import get_random_string

from market_backend.validator.errorcodemapping import ErrorMessage
from market_backend.validator.errormapping import ErrorCode


class Utils(object):

    @staticmethod
    def dispatch_failure(request, identifier, response=None, code=status.HTTP_400_BAD_REQUEST):
        """
        This method for dispatch the failure response
        :param request:
        :param identifier:
        :param response:
        :param code:
        :return:
        """

        if hasattr(ErrorCode, identifier):
            error_code = getattr(ErrorCode, identifier)
        else:
            error_code = code

        error_message = getattr(ErrorMessage, identifier)
        errors = {}
        if response is None:
            errors['status'] = 'failed'
            errors['code'] = error_code
            errors['message'] = error_message
        else:
            errors['status'] = 'failed'
            errors['code'] = error_code
            errors['message'] = error_message
            errors['errors'] = response

        return Response(data=errors, status=code)

    @staticmethod
    def dispatch_success(request, response, code=status.HTTP_200_OK, **kwargs):
        """
        This method for dispatch the success response
        :param request:
        :param response:
        :param code:
        :return:
        """

        if isinstance(response, list) or isinstance(response, dict):
            data = {'status': 'success', 'result': response, **kwargs}

        else:
            message = getattr(ErrorMessage, response)
            data = {'status': 'success', 'message': message, **kwargs}
            if 'DATA_NOT_FOUND' == response:
                data['code'] = ErrorCode.DATA_NOT_FOUND
            if 'NO_DATA_CHANGES' == response:
                data['code'] = ErrorCode.NO_DATA_CHANGES

        return Response(data=data, status=code)

    @staticmethod
    def validate_email_address(email):
        """
        This method validates whether the input is an email address or not.
        """
        try:
            validate_email(email)
            return True
        except Exception:
            return False

    @staticmethod
    def send_mail(email, subject, body, html_message=None):
        if not isinstance(email, list):
            email = [email, ]
        try:
            send_mail(
                from_email=settings.EMAIL_HOST_USER,
                subject=subject,
                message=body,
                recipient_list=email,
                fail_silently=False,
                html_message=html_message,
            )
        except Exception as e:
            print("Mail Fail to Sent: {}".format(e))

    @staticmethod
    def generate_unique_token():
        return str(uuid.uuid4().hex)

    @staticmethod
    def generate_token(length=64):
        return get_random_string(length=length)

    @staticmethod
    def generate_xls(filename=None, report_type=None, columns=None, data=None, extension='xls', from_date=None,
                     to_date=None, today=None, sheet_name='report'):
        wb = xlwt.Workbook(encoding='utf-8')

        bold_title_font_style = xlwt.XFStyle()  # For title font with bold style
        bold_title_font_style.font.bold = True

        font_style = xlwt.XFStyle()  # for Normal Font Style

        wb_report = wb.add_sheet(sheet_name)

        for col_no, col_title in enumerate(columns):  # for Header column
            wb_report.write(0, col_no, col_title, bold_title_font_style)

        for row_no, row in enumerate(data):
            for col_no, col_title in enumerate(columns):
                wb_report.write(row_no + 1, col_no, row[col_title], font_style)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}.{}"'.format(filename, extension)
        wb.save(response)
        return response

    @staticmethod
    def generate_csv(filename=None, report_type=None, columns=None, data=None, extension='csv', **kwargs):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.{}'.format(filename, extension)

        writer = csv.writer(response)  # Creating a csv file

        writer.writerow(columns)

        for row in data:
            writer.writerow([row[col_title] for col_title in columns])

        return response

    @staticmethod
    def generate_pdf(filename=None, report_type=None, columns=None, data=None, extension='xls', **kwargs):
        template = get_template(kwargs['pdf_template'])
        html = template.render(
            {'data': data, 'logo': settings.LOGO_LINK, 'columns': columns, 'from_date': kwargs['from_date'],
             'to_date': kwargs['to_date'],
             'today': kwargs['today'], 'report_type': report_type})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            response_pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
        else:
            response_pdf = None

        if pdf:
            response = HttpResponse(response_pdf, content_type='application/pdf')
            content = "attachment; filename={}.{}".format(filename, extension)
            response['Content-Disposition'] = content
            return response
