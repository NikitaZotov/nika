from typing import Dict, List, Tuple

from sc_client import client
from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScConstruction
from sc_kpm.identifiers import ActionStatus, ScAlias
from sc_kpm.sc_keynodes import Idtf, ScKeynodes
from sc_kpm.utils.common_utils import (
    check_connector,
    generate_non_role_relation,
)
from sc_kpm.utils.action_utils import (
    generate_action,
    wait_agent,
    call_action,
    add_action_arguments,
    IsDynamic,
    COMMON_WAIT_TIME
)



def execute_agent_tg_bot(
        arguments: Dict[ScAddr, IsDynamic],
        concepts: List[Idtf],
        initiation: Idtf = ActionStatus.ACTION_INITIATED,
        reaction: Idtf = ActionStatus.ACTION_FINISHED_SUCCESSFULLY,
        wait_time: float = COMMON_WAIT_TIME,
) -> Tuple[ScAddr, bool]:
    action = call_agent_tg_bot_test(arguments, concepts, initiation)
    wait_agent(wait_time, action)
    result = check_connector(sc_type.VAR_PERM_POS_ARC, ScKeynodes.resolve(reaction, sc_type.CONST_NODE_CLASS), action)
    return action, result


def call_agent_tg_bot_test(
        arguments: Dict[ScAddr, IsDynamic],
        concepts: List[Idtf],
        initiation: Idtf = ActionStatus.ACTION_INITIATED,
) -> ScAddr:
    question = generate_action(*concepts)
    construction = ScConstruction()
    construction.generate_node(sc_type.CONST_NODE, ScAlias.ACTION_NODE)
    user = client.generate_elements(construction)[0]
    nrel_authors = ScKeynodes.resolve('nrel_authors', sc_type.CONST_NODE_NON_ROLE)
    generate_non_role_relation(question, user, nrel_authors)
    add_action_arguments(question, arguments)
    call_action(question, initiation)
    return question
