class LeadNurturingCampaign():
  '''Defines the HubSpot Lead Nurturing Campaign object for use in the PySpot Wrapper'''
  def __init__(self, lead_data):
    self.data_parse(lead_data)
  
  def data_parse(self, lead_data):
    self.guid = lead_data['guid']
    self.name = lead_data['name']
  

class CampaignLeads():
  '''Defines Leads in a Lead Nurturing Campaign for use in the PySpot Wrapper'''
  def __init__(self, lead_data):
    self.data_parse(lead_data)
  
  def data_parse(self, lead_data):
    self.status = lead_data['status']
    self.lead_guid = lead_data['leadGuid']
    self.campaign_guid = lead_data['campaignGuid']
  
