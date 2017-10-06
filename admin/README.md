# Admin workflow
To kick off a conference, the OpenReview superuser should:
- Create a conference directory under /venues (e.g. venues/MyConference.org/2018)
- Copy the file /admin/conference-template/config.properties and fill it in with conference-specific variables. Then save it in the conference directory.
- Run openreview-scripts/admin/superuser-init.py (see comments in that file for details)


Example:

```
>> superuser-init.py --conf myconf.org/MYCONF/2017 --data path/to/params.data
```

The script will generate a python script called `python/admin-init.py` in the conference's directory. This is used to initiate the conference.
