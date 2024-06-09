
import uuid
from uuid import UUID
from datetime import datetime
import json

from module.message_handler.messages.base_message import CustomMessage
from module.message_handler.messages.payloads.base_payload import BasePayload

from module.message_handler.messages.payloads.attack_payload import AttackPayload
from module.message_handler.messages.payloads.attack_conf_payload import AttackConfirmationPayload
from module.attacker_module.enums.attack_type import AttackType

from module.message_handler.messages.payloads.agent_init_payload import AgentInitializationPayload
from module.message_handler.messages.payloads.agent_info_payload import AgentInformationPayload

from module.message_handler.enums.message_type import MessageType

class MessageFactory:

    message_params = ["message_id", "message", "message_type", "creation_date", "payload"]
    
    @classmethod
    def compose_message(cls, message: CustomMessage) -> str:
        return json.dumps(message.to_dict())

    @classmethod
    def create_attack_message(cls,
                              message: str,
                              payload: AttackPayload) -> CustomMessage:
        return cls.create_message(message, 
                                  MessageType.ATTACK_PACKAGE, 
                                  payload)

    @classmethod
    def create_attack_confirmation_message(cls, 
                                           message: str,
                                           payload: AttackConfirmationPayload) -> CustomMessage:
        return cls.create_message(message, 
                                  MessageType.ATTACK_CONF_PACKAGE,
                                  payload)

    @classmethod
    def create_agent_initialization_message(cls, 
                                            message: str,
                                            payload: AgentInitializationPayload) -> CustomMessage:
        return cls.create_message(message, 
                                  MessageType.AGENT_INIT_PACKAGE, 
                                  payload)
    
    @classmethod
    def create_agent_information_message(cls,
                                         message: str,
                                         payload: AgentInformationPayload) -> CustomMessage:
        return cls.create_message(message,
                                  MessageType.AGENT_INFO_PACKAGE,
                                  payload)
    
    @staticmethod
    def create_message(message,
                       message_type: MessageType,
                       payload: BasePayload):
        
        payload.payload_id = uuid.uuid4()
        return CustomMessage(
            message_id=uuid.uuid4(), 
            message=message,
            message_type=message_type,
            creation_date=datetime.now(),
            payload=payload)
    
    @classmethod
    def parse_custom_message(cls, json_str :str):
        data = json.loads(json_str)
        data = cls.message_decoder(data)
        return data

    @classmethod
    def message_decoder(cls, data):

        for message in cls.message_params:
            if message not in data:
                return None

        message_id = UUID(data['message_id'])
        message = data['message']
        message_type = MessageType.from_string(data['message_type'])
        creation_date = datetime.fromisoformat(data['creation_date'])
        payload_data = data["payload"]
        
        if (message_type == None): return None

        payload: BasePayload
        
        "%Y-%m-%dT%H:%M:%S.%f"

        executed_at = None
        try:
            executed_at = datetime.strptime(payload_data["executed_at"], "%Y-%m-%dT%H:%M:%S")
            executed_at = datetime.strptime(payload_data["executed_at"], "%Y-%m-%dT%H:%M:%S.%f")
        except Exception as e:
            pass

        if message_type == MessageType.ATTACK_PACKAGE:
            payload = AttackPayload(
                payload_id = cls.uuid_from_str(payload_data["payload_id"]),
                attack_job_id = cls.uuid_from_str(payload_data["attack_job_id"]),
                log_block_id = cls.uuid_from_str(payload_data["log_block_id"]),
                attack_name = payload_data["attack_name"],
                attack_description = payload_data["attack_description"],
                attack_type = AttackType.from_string(payload_data["attack_type"]),
                executed_at = executed_at)
        else: return None

        return CustomMessage(
            message_id=message_id,
            message=message,
            message_type=message_type,
            creation_date=creation_date,
            payload=payload
        )
    
    @staticmethod
    def uuid_from_str(_id: str) -> UUID:
        return UUID(_id)