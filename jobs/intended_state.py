import json

from nautobot.extras.jobs import Job, TextVar
from nautobot.utilities.utils import get_model_from_name

name = "POC Jobs"


class IntendedState(Job):

    json_payload = TextVar()

    class Meta:
        name = "Intended State Job POC"
        description = "Create or update objects in Nautobot by passing in an intended state JSON payload."

    def run(self, data, commit):
        json_payload = data["json_payload"]
        intended_state = json.loads(json_payload)
        for object_name, objects in intended_state.items():
            object_class = get_model_from_name(object_name)
            for object_data in objects:
                object_class.objects.update_or_create(**object_data)


jobs = [IntendedState]
