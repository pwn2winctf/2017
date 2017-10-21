# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import

import time
import calendar

from ..proof import proof_open
from ..team import Team
from ..subrepo import SubRepo
from ..acceptedsubmissions import AcceptedSubmissions
from ..proposal import retry_push
from ..six import to_unicode, to_bytes

def accept(team_id, proof, accepted_time):
    team = Team(id=to_unicode(team_id))
    chall = proof_open(team, to_bytes(proof))

    timestamp = calendar.timegm(time.strptime(accepted_time,
                                              '%Y-%m-%dT%H:%M:%SZ'))

    for _ in retry_push('Accept challenge solution'):
        SubRepo.git(['checkout', 'master'])
        AcceptedSubmissions().add(chall, team, accepted_time=timestamp)
