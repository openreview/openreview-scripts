# Admin workflow
To kick off a conference, the OpenReview superuser should:
- Create a conference directory under /venues (e.g. venues/MyConference.org/2018)
- Copy the file /admin/conference-template/config.properties and fill it in with conference-specific variables. Then save it in the conference directory.
- Run openreview-scripts/admin/superuser-init.py (see comments in that file for details)

Example:

```
>> superuser-init.py --venue myconf.org/MYCONF/2017
```

`superuser-init.py` will automatically look for a file called config.properties in the directory specified by the `--venue` argument. You can specify a .properties file by passing it into the `--config` argument.

The script will generate a python script called `python/admin-init.py` in the conference's directory. This is used to initiate the conference.
