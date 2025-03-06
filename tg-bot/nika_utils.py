import logging

from sc_client.client import connect, search_by_template
from sc_client.client import generate_elements, generate_by_template
from sc_client.constants import sc_type
from sc_client.models import ScAddr, ScConstruction, ScTemplate
from sc_client.models import ScLinkContentType, ScLinkContent
from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.utils import get_link_content_data
from sc_kpm.utils.action_utils import get_action_result

from action_utils import execute_agent_tg_bot

url = "ws://localhost:8090/ws_json"
connect(url)

logging.basicConfig(level=logging.INFO)


def get_nika_response(user_message: str) -> str:
    """
       Get a user message from Telegram.
       Generate a template of question.

       Args:
           user_message(str): The message from user.

       Returns:
           str: Response from Nika.
       """
    logging.info(f"Received user message: {user_message}")

    lang = ScKeynodes.resolve('lang_ru', sc_type.CONST_NODE_CLASS)
    text = ScKeynodes.resolve('concept_text_file', sc_type.CONST_NODE_CLASS)
    concept_dialog = ScKeynodes.resolve('concept_dialog', sc_type.CONST_NODE_CLASS)

    template = ScTemplate()

    dialog_template = ScTemplate()
    dialog_template.triple(
        concept_dialog,
        sc_type.VAR_PERM_POS_ARC,
        sc_type.VAR_NODE >> "_dialog")

    search_results = search_by_template(dialog_template)
    if not search_results:
        dialog_construction = ScConstruction()
        dialog_construction.generate_node(sc_type.CONST_NODE, 'dialog')
        dialog = generate_elements(dialog_construction)[0]
        template.triple(
            concept_dialog,
            sc_type.VAR_PERM_POS_ARC,
            dialog)
        generate_by_template(template)
    else:
        dialog = search_results[0].get("_dialog")
    construction = ScConstruction()  # Create link for example
    construction.generate_link(sc_type.CONST_NODE_LINK, ScLinkContent(user_message, ScLinkContentType.STRING))
    message_link = generate_elements(construction)[0]

    template = ScTemplate()
    template.triple(
        lang,
        sc_type.VAR_PERM_POS_ARC,
        message_link
    )
    template.triple(
        text,
        sc_type.VAR_PERM_POS_ARC,
        message_link
    )
    generate_by_template(template)

    action_result, is_successfully = execute_agent_tg_bot(arguments={message_link: False, dialog: False},
                                                          concepts=["question", 'action_reply_to_message'], wait_time=3)

    if is_successfully:
        response = get_action_result(action_result)
        response_text = get_system_answer(response)
        print(response_text)
    else:
        response_text = "Я не могу ответить на ваш вопрос"

    return response_text


def get_system_answer(action_result: ScAddr) -> str:
    """
           Get ScAddr of a question template.
           Generate template of answer and convert it to a string.

           Args:
               action_result(ScAddr): The ScAddr that was sent.

           Returns:
               str: Nika answer.
           """
    message = ScKeynodes.resolve('concept_message', sc_type.CONST_NODE_CLASS)
    nrel_reply = ScKeynodes.resolve('nrel_reply', sc_type.CONST_NODE_NON_ROLE)
    nrel_translation = ScKeynodes.resolve('nrel_sc_text_translation', sc_type.CONST_NODE_NON_ROLE)
    template = ScTemplate()
    template.triple(
        action_result,
        sc_type.VAR_PERM_POS_ARC,
        sc_type.VAR_NODE >> "_message")
    template.triple(
        message,
        sc_type.VAR_PERM_POS_ARC,
        "_message")
    template.quintuple(
        "_message",
        sc_type.VAR_COMMON_ARC,
        "_answer_message",
        sc_type.VAR_PERM_POS_ARC,
        nrel_reply)
    template.quintuple(
        sc_type.VAR_NODE >> "_tuple",
        sc_type.VAR_COMMON_ARC,
        "_answer_message",
        sc_type.VAR_PERM_POS_ARC,
        nrel_translation)
    template.triple(
        "_tuple",
        sc_type.VAR_PERM_POS_ARC,
        sc_type.VAR_NODE_LINK >> "_link")

    search_results = search_by_template(template)
    answer_link = search_results[0].get("_link")

    answer_text = get_link_content_data(answer_link)
    return answer_text
