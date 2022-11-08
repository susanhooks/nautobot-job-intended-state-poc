import json
import re

from django.apps import apps

from nautobot.extras.jobs import Job, TextVar

name = "POC Jobs"


def replace_ref(ref):
    pattern = r"^#ref:(?P<app>.*):(?P<field>.*):(?P<value>.*)$"
    groups = re.match(pattern, ref)
    app_name = groups.group("app")
    obj_lookup = {groups.group("field"): groups.group("value")}
    object_class = apps.get_model(app_name)
    return object_class.objects.get(**obj_lookup)


class IntendedState(Job):

    json_payload = TextVar()

    class Meta:
        name = "Intended State Job POC"
        description = "Create or update objects in Nautobot by passing in an intended state JSON payload."

    def run(self, data, commit):
        json_payload = data["json_payload"]
        intended_state = json.loads(json_payload)
        for object_name, objects in intended_state.items():
            object_class = apps.get_model(object_name)
            for object_data in objects:
                for key, value in object_data.items():
                    if value.startswith("#ref"):
                        object_data[key] = replace_ref(value)
                obj, created = object_class.objects.update_or_create(**object_data)
                self.log_success(obj=obj, message=f"Object {obj} has been {'created' if created else 'updated'}.")

jobs = [IntendedState]
