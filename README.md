# nautobot-job-intended-state-poc

A proof of concept for sending the intended state of objects to a Job in Nautobot

## Why

This POC exists solely to present an alternative solution to creating or updating many items in Nautobot. Instead of doing a `GET` call for each object, determining the current state of that object, sending a `PUT/PATCH` call to update an object or `POST` to create an object, you can instead send in a large amount of data in a single API call to a Job and let it deal with determining state and what needs to be updated.

## Requirements

Nautobot v1.3+

## How to Use (as-is)

You can add this Job to any Nautobot instance by add it under [Extensibility > Git Repositories](https://docs.nautobot.com/projects/core/en/stable/models/extras/gitrepository/).

Once you have synced the repo, you can run the Job [via the GUI or an API call like any other Job](https://docs.nautobot.com/projects/core/en/stable/additional-features/jobs/#running-jobs). The only job data that is required is a JSON serialized object. Each top level key of the dictionary must be the app name and model in dot notation that you would like to create or update. The value of each `app.model` must be a list of dictionaries with field attributes. Here is an example:

```json
{
    "dcim.site": [
        {
            "name": "New Site",
            "status": ...,
            "region": ...,
        }
    ],
    "dcim.device": [
        {
            "name": "New Device",
            "device_role": ...,
            "device_type": ...,
        }
    ]
}
```

This payload must be sent as a string that will be serialized. Here is an example of an API payload:

```json
{
    "data": {
        "json_payload": "{\"extras.status\": [{\"name\": \"Test Status\"}]}"
    }
}
```

## Limitations

Note, this repo is not meant to be a perfect representation of how to implement this, but rather just a simple POC on how it _could_ be done. There are many considerations that this Job does not take into account, such as:

- Some objects are required to exist before others, so they must be sent in earlier in the payload
- Some fields need to be a UUID of an existing object instead of a name or slug
- There are no try/except blocks for catching errors

## Future

I hope that this has given you some idea on how you might accomplish a task of syncing items into Nautobot from an external system in a more efficient manner.
