#!/usr/bin/env python
"""
"""
import logging
import os
import datetime as dt

from wfinterop.util import get_json, save_json

logger = logging.getLogger(__name__)


submission_queue = os.path.join(os.path.dirname(__file__),
                                'submission_queue.json')
if not os.path.exists(submission_queue):
    save_json(submission_queue, {})


def create_queue():
    pass


def create_submission(queue_id, submission_data, wes_id=None):
    """
    Submit a new job request to an evaluation queue.

    Both type and wf_name are optional but could be used with TRS.

    :param str queue_id: String identifying the workflow queue.
    :param dict submission_data:
    :param str wes_id:
    """
    submissions = get_json(submission_queue)
    submission_id = dt.datetime.now().strftime('%d%m%d%H%M%S%f')

    submission = {'status': 'RECEIVED',
                  'data': submission_data,
                  'wes_id': wes_id}
    submissions.setdefault(queue_id, {})[submission_id] = submission
    save_json(submission_queue, submissions)
    logger.info(" Queueing job for '{}' endpoint:"
                "\n - submission ID: {}".format(wes_id, submission_id))
    return submission_id


def get_submissions(queue_id,
                    status=['RECEIVED', 'SUBMITTED', 'VALIDATED', 'COMPLETE'],
                    exclude_status=[]):
    """
    Return all ids with the requested status.

    :param str queue_id: String identifying the workflow queue.
    :param list status:
    :param list exclude_status:
    """
    submissions = get_json(submission_queue)
    if len(exclude_status):
        status = [s for s in status if s not in exclude_status]
    try:
        return [id for id, bundle in submissions[queue_id].items()
                if bundle['status'] in status]
    except KeyError:
        return []


def get_submission_bundle(queue_id, submission_id):
    """
    Return the submission's info.

    :param str queue_id:
    :param str submission_id:
    """
    return get_json(submission_queue)[queue_id][submission_id]


def update_submission(queue_id, submission_id, param, value):
    """
    Update the status of a submission.

    :param str queue_id:
    :param str submission_id:
    :param str param:
    :param str value:
    """
    submissions = get_json(submission_queue)
    submissions[queue_id][submission_id][param] = value
    save_json(submission_queue, submissions)
