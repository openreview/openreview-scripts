# Admin workflow
To kick off a conference, the OpenReview superuser needs to:
- Create a conference directory under openreview-scripts/venues
- Create and post the conference's root group to the system
- Create the conference administrator account (Optional)

the `superuser-init.py` script is responsible for performing all three of these tasks. Call it with the following arguments:

```
optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  the full path of the conference group to create
  --overwrite           if true, overwrites the conference directory
  --data DATA           a .json file containing parameters. For each parameter
                        present, the corresponding user prompt will be skipped
                        and replaced with that value.
  --baseurl BASEURL     base URL
  --username USERNAME
  --password PASSWORD
```

`superuser-init.py` also generates a file at the top level of the conference directory called `params.json`. This file contains all the parameters that were initially passed into the script's text prompts. Passing the path of `params.json` into the `--data` flag allows the user to skip the text prompts and generate new files using those parameters. When combined with the `--overwrite` flag, this is useful for making changes to the conference configuration.

```
Example:

>> superuser-init.py --conf myconf.org/MYCONF/2017 --data ./params.json 
```

Regardless of whether or not the conference directory already exists, `superuser-init.py` will create and post the conference's root group. It will also prompt the user to (optionally) create a conference administrator account.

## Example Workflow:

A program chair requests our support in creating an upcoming workshop. The OpenReview superuser runs the following:

`superuser-init.py --conf myconf.org/MYCONF/2017`

The superuser is then prompted for various information by the script. A directory under /venues is generated, and in that directory, the `params.json` file is saved. The conference root group is created, and the superuser has the opportunity to create/register an administrator group for the conference.

Suppose that the above took place in a test environment: this means that the conference root group and conference administrator accounts exist only in that test environment, not on the live site. The superuser can call `superuser-init.py` again (with the same parameters as above) to re-post the root group and administrator:

`superuser-init.py --conf myconf.org/MYCONF/2017`

Finally, suppose that minor changes need to be made to the conference's "display name". Edit the file `params.json`, then run the following to re-write the conference directory:

`superuser-init.py --conf myconf.org/MYCONF/2017 --overwrite --data openreview-scripts/venues/myconf.org/MYCONF/2017/params.json`

This will overwrite the existing conference directory with the new values in `params.json`
