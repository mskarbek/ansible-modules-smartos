#!/opt/local/bin/python

# (c) 2015, Marcin Skarbek <marcin@skarbek.name>
#
# Distributed under Apache License 2.0
# Full text of license in LICENSE file

###############################################################################

DOCUMENTATION = '''
---
module: imgadm
author: Marcin Skarbek
version_added: "0.1"
short_description: Manage SmartOS zones images
description:
     - This module allows you to manage zones images in SmartOS
options:
  source:
    description:
       - "URL to a server implementing the IMGAPI, or the Docker Registry API."
    required: true
  type:
    description:
      - "The source type for an added source. One of \"imgapi\" or \"docker\"."
    required: false
    default: imgapi
  insecure:
    description:
       - "Allow insecure access to the added HTTPS source URL."
    required: false
    default: "no"
  force:
    description:
       - "Force no \"ping check\" on new source URL."
    required: false
    default: "no"
  state:
    description:
       - "One of \"present\" or \"absent\"."
    required: false
    default: "present"
requirements: [ "python >= 2.7" ]
'''

EXAMPLES = ''''''


import json

def list_sources(module, params):
    imgadm_cmd = module.get_bin_path('imgadm', required=True)
    rc, out, err = module.run_command('{0} -E sources -j'.format(imgadm_cmd))
    if rc != 0:
        module.fail_json(msg='Can\'t list sources.', rc=rc, err=json.loads(err)['msg'])
    return json.loads(out)

def add_source(module, params):
    imgadm_cmd = module.get_bin_path('imgadm', required=True)
    opts = ''
    if params['force']:
        opt += ' -f'
    if params['insecure']:
        opt += ' -k'
    rc, out, err = module.run_command('{0} -E sources -a {1} -t {2}{3}'.format(imgadm_cmd, params['source'], params['type'], opts))
    if rc != 0:
        module.fail_json(msg='Can\'t add source {}.'.format(params['source']), rc=rc, err=json.loads(err)['msg'])

def delete_source(module, params):
    imgadm_cmd = module.get_bin_path('imgadm', required=True)
    rc, out, err = module.run_command('{0} -E sources -d {1}'.format(imgadm_cmd, params['source']))
    if rc != 0:
        module.fail_json(msg='Can\'t delete sources {}.'.format(params['source']), rc=rc, err=json.loads(err)['msg'])

def enforce_state(module, params):
    module.exit_json(changed=True, stdout='{}'.format(list_sources(module, params)), stderr=False)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            source   = dict(required=True, type='str'),
            type     = dict(required=False, type='str', default='imgapi', choices=['imgapi','docker']),
            insecure = dict(required=False, type='bool', default='no'),
            force    = dict(required=False, type='bool', default='no'),
            state    = dict(required=False, type='str', default='present', choices=['present','absent']),
        ),
        supports_check_mode = False
    )

    enforce_state(module, module.params)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
