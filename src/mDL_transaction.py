from mDL import mDL

class mDL_transaction:
    def __init__(self, data=None):
        """
        Parâmetros
        ----------
        data : dict
            dicionário com os nomes das variáveis de instância como chaves
            e respetivo conteúdo como valor
        """
        self.mDL = mDL(data)

    def preselect(self, data_groups_available):
        allowed = {}
        for tag in data_groups_available:
            num_dg = self.mDL.TAGS[tag]
            allow = input(
                'Do you allow access to data group ' +
                str(num_dg) + ' (tag: ' + tag + ') ? [Y/N] '
            )
            if allow in ('yes', 'y', 'Y'): # Modify permissions
                allowed[num_dg] = tag
        return allowed

    def print_permissions(self):
        print('DG1', self.mDL.ef_groupAccess.is_allowed(1))
        print('DG6', self.mDL.ef_groupAccess.is_allowed(6))
        print('DG10', self.mDL.ef_groupAccess.is_allowed(10))

    def open(self):
        done = False
        while not done:
            permission = input('Do you want to preselect the data to be shared? [Y/N] ')
            if permission in ('yes', 'y', 'Y'): # Modify permissions
                data_groups_available = self.mDL.get_available_data_groups()
                allowed = self.preselect(data_groups_available)
                allowed_str = [str(num_dg) for num_dg in allowed.keys()]
                print('Allowing data groups: ' + ', '.join(allowed_str) + '.')
                self.mDL.set_permissions(allowed)
                print('Permissions updated with success.')
                done = True
            elif permission in ('no', 'n', 'N'): # Use default permissions
                print('Current permissions retained.')
                done = True
            else:
                print('Invalid answer.')

    def request_additional_data(self, data_group_tags):
        request = {}
        for tag in data_group_tags:
            num_dg = self.mDL.TAGS[tag]
            request[num_dg] = tag
        request_list = []
        for num_dg, tag in request.items():
            request_list.append(str(num_dg) + ' (tag: ' + tag + ')')
        done = False
        while not done:
            permission = input(
                'Do you allow, additionally, data groups\n\t' +
                '\n\t'.join(request_list) +
                '\nto be accessed? [Y/N] ')
            if permission in ('yes', 'y', 'Y'): # Update permissions
                print('Allowing data groups: ' + ', '.join(request_list) + '.')
                self.mDL.add_permissions(request)
                print('Permissions updated with success.')
                done = True
            elif permission in ('no', 'n', 'N'): # Use default permissions
                print('Current permissions retained.')
                done = True
            else:
                print('Invalid answer.')

    def transfer_data(self, data_group_tags):
        return self.mDL.get_data(data_group_tags)
