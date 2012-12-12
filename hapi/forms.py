import logging
logger = logging.getLogger(__name__)

from base import BaseClient


class FormSubmissionClient(BaseClient):

    def __init__(self, *args, **kwargs):
        super(FormSubmissionClient, self).__init__(*args, **kwargs)
        self.options['api_base'] = 'forms.hubspot.com'

    def _get_path(self, subpath):
        return '/uploads/form/v2/%s' % subpath

    def submit_form(self, portal_id, form_guid, data, **options):
        subpath = '%s/%s' % (portal_id, form_guid)
        opts = {'content_type': 'application/x-www-form-urlencoded'}
        options.update(opts)
        return self._call(
            subpath=None,
            url=self._get_path(subpath),
            method='POST',
            data=data,
            **options
        )
