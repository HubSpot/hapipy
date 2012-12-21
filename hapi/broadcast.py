from base import BaseClient

HUBSPOT_BROADCAST_API_VERSION = '1'


class BaseSocialObject(object):
    def _camel_case_to_underscores(self, text):
        result = []
        pos = 0
        while pos < len(text):
            if text[pos].isupper():
                if pos - 1 > 0 and text[pos - 1].islower() or pos - 1 > 0 and pos + 1 < len(text) and text[pos + 1].islower():
                    result.append("_%s" % text[pos].lower())
                else:
                    result.append(text[pos].lower())
            else:
                result.append(text[pos])
            pos += 1
        return "".join(result)

    def _underscores_to_camel_case(self, text):
        result = []
        pos = 0
        while pos < len(text):
            if text[pos] == "_" and pos + 1 < len(text):
                result.append("%s" % text[pos + 1].upper())
                pos += 1
            else:
                result.append(text[pos])
            pos += 1
        return "".join(result)

    def to_dict(self):
        dict_self = {}
        for key in vars(self):
            dict_self[self._underscores_to_camel_case(key)] = getattr(self, key)
        return dict_self

    def from_dict(self, data):
        accepted_fields = self.accepted_fields()
        for key in data:
            if key in accepted_fields:
                setattr(self, self._camel_case_to_underscores(key), data[key])


class Broadcast(BaseSocialObject):
    '''Defines a specific social media broadcast message for the broadcast api'''

    # Constants for remote content type
    COS_LP = "coslp"
    COS_BLOG = "cosblog"
    LEGACY_LP = "cmslp"
    LEGACY_BLOG = "cmsblog"

    def __init__(self, broadcast_data):
        self.data_parse(broadcast_data)

    def accepted_fields(self):
        # "clicks" is actually from ShrinkyLinks but passed along
        return [
            'broadcastGuid',
            'campaignGuid',
            'channel',
            'channelGuid',
            'clicks',
            'clientTag',
            'content',
            'createdAt',
            'createdBy',
            'finishedAt',
            'groupGuid',
            'interactions',
            'interactionCounts',
            'linkGuid',
            'message',
            'messageUrl',
            'portalId',
            'remoteContentId',
            'remoteContentType',
            'status',
            'triggerAt',
            'updatedBy'
        ]

    def data_parse(self, broadcast_data):
        self.from_dict(broadcast_data)


class BroadcastClient(BaseClient):
    '''
    Broadcast API to manage messages published to social networks
    '''
    def _get_path(self, method):
        return 'broadcast/v%s/%s' % (HUBSPOT_BROADCAST_API_VERSION, method)

    def get_broadcast(self, broadcast_guid, **kwargs):
        '''
        Get a specific broadcast by guid
        '''
        params = kwargs
        broadcast = self._call('broadcasts/%s' % broadcast_guid,
            params=params, content_type='application/json')
        return Broadcast(broadcast)

    def get_broadcasts(self, type="", page=None,
            remote_content_id=None, limit=None, **kwargs):
        '''
        Get all broadcasts, with optional paging and limits.
        Type filter can be 'scheduled', 'published' or 'failed'
        '''
        if remote_content_id:
            return self.get_broadcasts_by_remote(remote_content_id)

        params = {'type': type}
        if page:
            params['page'] = page

        params.update(kwargs)

        result = self._call('broadcasts', params=params,
            content_type='application/json')
        broadcasts = [Broadcast(b) for b in result]

        if limit:
            return broadcasts[:limit]
        return broadcasts

    def cancel_broadcast(self, broadcast_guid):
        '''
        Cancel a broadcast specified by guid
        '''
        subpath = 'broadcasts/%s/update' % broadcast_guid
        broadcast = {'status': 'CANCELED'}
        bcast_dict = self._call(subpath, method='POST', data=broadcast,
            content_type='application/json')
        return bcast_dict
