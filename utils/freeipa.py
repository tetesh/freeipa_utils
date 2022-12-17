from python_freeipa import ClientMeta
from python_freeipa import exceptions as freeipa_exceptions

def session(ipa_host, user_bind, password_bind):
    try:
        client = ClientMeta(ipa_host)
        client.login(user_bind, password_bind)
        if client:
            return client
        else:
            raise SystemExit
    except Exception as e:
        print(e)

def create_user_ipa(ipa_host, user_bind, password_bind, created_user, sn, cn, givenname, group, created_user_passwd=None):
    try:
        conn = session(ipa_host, user_bind, password_bind)
        if conn:
            if created_user_passwd:
                user = conn.user_add(a_uid=created_user, o_sn=sn, o_cn=cn, o_givenname=givenname,
                                     o_userpassword=created_user_passwd)
                if "added user" in user['summary'].lower():
                    print(f"\nFreeipa user {created_user} successfully created, password: {created_user_passwd}")
                    group_member = conn.group_add_member(a_cn=group, o_user=created_user)
                    if group_member['completed']: print(f"\nFreeipa user {created_user} successfully add to group {group}")

            else:
                user = conn.user_add(a_uid=created_user, o_sn=sn, o_cn=cn, o_givenname=givenname,
                                     o_random=True)
                if "added user" in user['summary'].lower():
                    print(f"\nFreeipa user {created_user} successfully created, password: {user['result']['randompassword']}")
                    group_member = conn.group_add_member(a_cn=group, o_user=created_user)
                    if group_member['completed']: print(f"\nFreeipa user {created_user} successfully add to group {group}")
        else:
            print('Connection Error')
            raise SystemExit
    except freeipa_exceptions.DuplicateEntry:
        print(f"\nERROR: User {created_user} already exists")

def delete_user_ipa(ipa_host, user_bind, password_bind, user_deleted):
    conn = session(ipa_host, user_bind, password_bind)
    if conn:
        delete = conn.user_del(a_uid=user_deleted, o_continue=True)
        if user_deleted in delete['summary'].lower():
            print(f"\nFreeipa user {user_deleted} successfully deleted")
        else:
            print(f"\nUser {user_deleted} already deleted")
    else:
        print('Connection Error')
        raise SystemExit