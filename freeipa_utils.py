import argparse, re, sys, secrets, os, datetime
import utils.freeipa as freeipa

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='freeipa_utils')
    subparsers = parser.add_subparsers()

    # Create freeipa user args
    user_create = subparsers.add_parser('user_create', help='Create freeipa user')
    user_create.add_argument('-u', '--user', required=True, help='Username User created. Required', type=str)
    user_create.add_argument('-p', '--user_password', required=False,
                             help='User created Password, if not define password set random. Not required', type=str)
    user_create.add_argument('-f', '--first_name', required=True, help='User created First name. Required', type=str)
    user_create.add_argument('-l', '--last_name', required=True, help='User created Last name. Required', type=str)
    user_create.add_argument('-F', '--full_name', required=True, help='User created Full name. Required', type=str)
    user_create.add_argument('-j', '--job_title', required=True, help='User created job_title. Required', type=str)
    user_create.add_argument('-g', '--group', required=True,
                             help='User created Group department. You can see the list of groups with the key freeipa_utils.py list_departments_ipa. Required',
                             type=str)
    # Delete freeipa user args
    user_delete = subparsers.add_parser('user_delete', help='Delete freeipa user')
    user_delete.add_argument('-u', '--user', required=True, help='User. Required', type=str)
    # Print list allowed Groups department
    list_departments_ipa = subparsers.add_parser('list_departments_ipa',
                                            help='Print list of allowed groups-departments_ipa to user_create and exit')
    # Print User info
    user_info = subparsers.add_parser('user_info', help='Show user info')
    user_info.add_argument('-u', '--user', required=True, help='Username. Required', type=str)
    # Disable User
    user_disable = subparsers.add_parser('user_disable', help='Disable user')
    user_disable.add_argument('-u', '--user', required=True, help='Username. Required', type=str)
    # Enable User
    user_enable = subparsers.add_parser('user_enable', help='Enable user')
    user_enable.add_argument('-u', '--user', required=True, help='Username. Required', type=str)
    # Show user status
    user_status = subparsers.add_parser('user_status', help='Show user status')
    user_status.add_argument('-u', '--user', required=True, help='Username. Required', type=str)
    # groups_add_members
    groups_add_members = subparsers.add_parser('groups_add_members', help='Add users to groups')
    groups_add_members.add_argument('-u', '--users', required=True,
                                    help='Users or users with separator ",". Required! Example: "test1,test2,test3"',
                                    type=str)
    groups_add_members.add_argument('-g', '--groups', required=True,
                                    help='Group or groups with separator ",". Required! Example: "group1,group2,group3"',
                                    type=str)
    groups_remove_members = subparsers.add_parser('groups_remove_members', help='Remove users for groups')
    groups_remove_members.add_argument('-u', '--users', required=True,
                                    help='Users or users with separator ",". Required! Example: "test.1,test2,test-3"',
                                    type=str)
    groups_remove_members.add_argument('-g', '--groups', required=True,
                                    help='Group or groups with separator ",". Required! Example: "group-1,group_2,group3"',
                                    type=str)
    # Collect Args
    args = parser.parse_args()

    # Run func user_create_ipa
    if sys.argv[1] == 'user_create':
        if args.user_password:
            user_create.set_defaults(
                func=freeipa.user_create_ipa(created_user=args.user, sn=args.last_name, cn=args.full_name,
                                             givenname=args.first_name, created_user_passwd=args.user_password,
                                             group=args.group, job_title=args.job_title))
        else:
            user_create.set_defaults(
                func=freeipa.user_create_ipa(
                    created_user=args.user, sn=args.last_name, cn=args.full_name,
                    givenname=args.first_name, group=args.group, job_title=args.job_title,
                    created_user_passwd=secrets.token_urlsafe(12)))

    # Run func user_create_ipa
    if sys.argv[1] == 'user_delete':
        user_delete.set_defaults(func=freeipa.user_delete_ipa(user_deleted=args.user))
    if sys.argv[1] == 'list_departments_ipa':
        list_departments_ipa.set_defaults(func=print(freeipa.allowed_groups_departments))

    if sys.argv[1] == 'user_info':
        user_info.set_defaults(func=freeipa.user_info_ipa(user=args.user))

    if sys.argv[1] == 'user_disable':
        user_disable.set_defaults(func=freeipa.user_disable_ipa(user=args.user))
    if sys.argv[1] == 'user_enable':
        user_enable.set_defaults(func=freeipa.user_enable_ipa(user=args.user))
    if sys.argv[1] == 'user_status':
        user_enable.set_defaults(func=freeipa.user_status_ipa(user=args.user))
    if sys.argv[1] == 'groups_add_members':
        list_users, pattern_users = args.users.split(","), '[a-z0-9-_.]+'
        list_groups, pattern_groups = args.groups.split(","), '[a-z0-9-_]+'
        print(f'\nUsers: {list_users}\nGroups: {list_groups}')
        for item in list_users:
            i = re.fullmatch(pattern_users, item)
            if not i:
                print(f'\nFailed regular expression check! user: {item} pattern: {pattern_users}')
                raise SystemExit
        for item in list_groups:
            i = re.fullmatch(pattern_groups, item)
            if not i:
                print(f'\nFailed regular expression check! group: {item} pattern: {pattern_groups}')
                raise SystemExit

        user_enable.set_defaults(func=freeipa.group_add_member(users=list_users, groups=list_groups))

    if sys.argv[1] == 'groups_remove_members':
        list_users, pattern_users = args.users.split(","), '[a-z0-9-_.]+'
        list_groups, pattern_groups = args.groups.split(","), '[a-z0-9-_]+'
        print(f'\nUsers: {list_users}\nGroups: {list_groups}')
        for item in list_users:
            i = re.fullmatch(pattern_users, item)
            if not i:
                print(f'\nFailed regular expression check! user: {item} pattern: {pattern_users}')
                raise SystemExit
        for item in list_groups:
            i = re.fullmatch(pattern_groups, item)
            if not i:
                print(f'\nFailed regular expression check! group: {item} pattern: {pattern_groups}')
                raise SystemExit

        user_enable.set_defaults(func=freeipa.group_remove_member(users=list_users, groups=list_groups))
