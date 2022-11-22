import json

from django.apps import apps
from django.core.exceptions import FieldError, ObjectDoesNotExist, ValidationError

from nautobot.extras.jobs import Job, TextVar

name = "POC Jobs"

def replace_ref_new(ref):
    ref_split = ref.split(":")
    ref_split.pop(0)
    app_name = ref_split.pop(0)
    object_class = apps.get_model(app_name)
    fields = [k for k in ref_split[::2]]
    values = [k for k in ref_split[1::2]]
    filters = {fields[i]: values[i] for i in range (len(values))}
    return object_class.objects.get(**filters)


class IntendedState(Job):

    json_payload = TextVar()

    class Meta:
        name = "Intended State Job"
        description = "Create or update objects in Nautobot by passing in an intended state JSON payload."

    def run(self, data, commit):
        json_payload = data["json_payload"]
        intended_state = json.loads(json_payload)
        for object_name, objects in intended_state.items():
            object_class = apps.get_model(object_name)
            for object_data in objects:
                for key, value in object_data.items():   
                    if value.startswith("#ref"):
                        try:
                            object_data[key] = replace_ref_new(value)
                        except (AttributeError, ObjectDoesNotExist, ValidationError) as e:
                            self.log_warning(message=f"Error on key '{key}'. Error: {e}.")
                        continue
                try:        
                    obj, created = object_class.objects.update_or_create(**object_data)
                except (FieldError, ObjectDoesNotExist) as e:
                    self.log_warning(message=f"Unable to create object. Error: {e}.")    
                self.log_success(obj=obj, message=f"Object {obj} has been {'created' if created else 'updated'}.")

jobs = [IntendedState]
