import sys, uuid
from datetime                       import datetime, date, timedelta

sys.path.append("/flowstacks/public-cloud-src")
from logger.logger import Logger
from modules.base_api.fs_web_tier_base_work_item     import FSWebTierBaseWorkItem
from connectors.redis.redis_pickle_application       import RedisPickleApplication
import tweepy

# FlowStacks Job for Posting Tweets to Twitter:
# Out of convention FlowStacks REST API Jobs begin with "RA_"
class RA_PostToTwitter(FSWebTierBaseWorkItem):

    def __init__(self, json_data):

        # The RA_PostToTwitter becomes the prefix for the Job when it is logged by the system
        FSWebTierBaseWorkItem.__init__(self, "RA_PTT", json_data)

        """ Constructor Serialization taking HTTP Post-ed JSON into Python members """
        # Define Inputs and Outputs for the Job to serialize over HTTP
        try:

            # INPUTS:
            self.m_consumer_key                     = str(json_data["Consumer Key"])
            self.m_consumer_secret                  = str(json_data["Consumer Secret"])
            self.m_access_token                     = str(json_data["Access Token"])
            self.m_access_token_secret              = str(json_data["Access Token Secret"])
            self.m_tweet_text                       = str(json_data["Tweet Text"])
        
            # OUTPUTS:
            self.m_results["Status"]                = "FAILED"
            self.m_results["Error"]                 = ""

            # MEMBERS:

        # Return the exact Error with the failure:
        except Exception,e:

            import os, traceback
            exc_type, exc_obj, exc_tb = sys.exc_info()
            reason = json.dumps({ "Module" : str(self.__class__.__name__), "Error Type" : str(exc_type.__name__), "Line Number" : exc_tb.tb_lineno, "Error Message" : str(exc_obj.message), "File Name" : str(os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]) })
            raise Exception(reason)

    # end of  __init__


###############################################################################
#
# Request Handle Methods
#
###############################################################################


    def handle_startup(self):

        self.lg("Start Handle Startup", 5)

        self.handle_posting_to_twitter()

        self.lg("Done Startup State(ENDING)", 5)

        return None
    # end of handle_startup


###############################################################################
#
# Helpers
#
###############################################################################


    def handle_posting_to_twitter(self):
        self.lg("Starting handle_posting_to_twitter", 5)
        
        try:
            consumer_key = self.m_consumer_key
            consumer_secret = self.m_consumer_secret
            access_token = self.m_access_token
            access_token_secret = self.m_access_token_secret
            tweet_text = self.m_tweet_text
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            api.update_status(tweet_text)
            self.m_results['Status'] = 'SUCCESS'

        except Exception,e:

            self.lg("Failed to Post to Twitter with Ex(" + str(e) + ")", 0)
            self.m_results['Status']    = 'FAILED'
            self.m_results['Error']     = 'Failed to Post to Twitter'
        
        self.lg("Done handle_posting_to_twitter", 5)
        
        return None
    # end of handle_posting_to_twitter


###############################################################################
#
# Request State Machine
#
###############################################################################


    # Needs to be state driven:
    def perform_task(self):

        if  self.m_state == "Startup":

            self.handle_startup()

            # found in the base
            self.lg("Result Cleanup", 5)
            self.base_handle_results_and_cleanup(self.m_result_details, self.m_completion_details)

        else:
            if self.m_log:
                self.lg("UNKNOWN STATE FOUND IN OBJECT(" + self.m_name + ") State(" + self.m_state + ")", 0)
            self.m_state = "Startup"

        # end of State Loop
        return self.m_is_done
    # end of perform_task

# end of RA_PostToTwitter


