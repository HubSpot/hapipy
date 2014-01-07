from base import BaseClient
import simplejson as json

BLOG_API_VERSION = '2'

class COSBlogClient(BaseClient):
  
    # Blogs
    def _get_path(self, subpath):
        return 'content/api/v%s/%s' % (BLOG_API_VERSION, subpath)

    def get_blogs(self, **options):
        return self._call('blogs', **options)

    def get_blog(self, blog_id, **options):
        return self._call('blogs/%s' % blog_id, **options)

    def get_blog_versions(self, blog_id, **options):
        return self._call('blogs/%s/versions' % blog_id, **options)

    def get_blog_version(self, blog_id, version_id, **options):
        return self._call('blogs/%s/versions/%s' % (blog_id, version_id), **options)

    # Blog Posts

    # Blog Authors

    # Topics
